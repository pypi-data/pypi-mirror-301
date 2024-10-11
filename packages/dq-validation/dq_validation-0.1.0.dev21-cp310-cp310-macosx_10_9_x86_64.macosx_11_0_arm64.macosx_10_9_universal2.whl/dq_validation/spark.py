import sys
import tempfile
import shutil
import functools

import os
import subprocess
from typing import List
from datetime import datetime
from collections import defaultdict
from . import validate

from decentriq_util.spark import spark_session
import pyspark.sql.functions as F
from pyspark.sql import DataFrame, Window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType
from pyspark.storagelevel import StorageLevel
from .schemas import ValidationConfig, ValidationReport

from .schemas import *
from .config import *
from .utils import (
    read_config,
    get_report_outcome,
    update_report_with_uniqueness_check_result,
    update_report_with_invalid_row_removal_result,
)
from pyspark.sql.types import StringType, IntegerType, DoubleType, LongType, StructType


HAS_ERROR_COL = "__has_error"

ROW_NUM_COLUMN = "__row_nr"

CURRENT_FILE_PATH = os.path.abspath(__file__)

SPARK_TYPE_BY_FORMAT_TYPE = {
    "STRING": StringType(),
    "INTEGER": IntegerType(),
    "FLOAT": FloatType(),
    "EMAIL": StringType(),
    "DATE_ISO_8601": StringType(),
    "PHONE_NUMBER_E164": StringType(),
    "HASH_SHA_256_HEX": StringType(),
}


def write_df_as_single_file(df: DataFrame, path: str, temp_dir: str):
    """Write a dataframe into a single CSV file and store the result at `path`"""
    filename = os.path.basename(path)
    with tempfile.TemporaryDirectory(dir=temp_dir) as d:
        csv_parts_dir = os.path.join(d, filename)
        df.write.csv(csv_parts_dir, header=False)
        csv_parts = [
            os.path.join(csv_parts_dir, f)
            for f in os.listdir(csv_parts_dir)
            if f.endswith(".csv")
        ]
        temp_merged_path = os.path.join(d, "__temp-merged.csv")
        with open(temp_merged_path, "wb") as temp_out:
            for part in csv_parts:
                with open(part, "rb") as f:
                    shutil.copyfileobj(f, temp_out)
        shutil.move(temp_merged_path, path)


def add_erroneous_row_ids(df: DataFrame, row_nrs_df: DataFrame) -> DataFrame:
    assert HAS_ERROR_COL in df.columns
    has_error_col_new = f"{HAS_ERROR_COL}_new"
    df = (
        df
        .join(row_nrs_df.withColumn(has_error_col_new, F.lit(True)), on=ROW_NUM_COLUMN, how="left_outer")
        .na.fill(False, subset=[has_error_col_new])
        .withColumn(HAS_ERROR_COL, F.col(HAS_ERROR_COL) | F.col(has_error_col_new))
        .drop(has_error_col_new)
    )
    return df


def create_spark_schema_from_validation_config(config: ValidationConfig, string_only: bool = False) -> List[StructField]:
    col_ix = 0
    col_fields = []
    for column in config.root.config.columns:
        col_name = column.name
        allow_null = column.allowNull
        if not col_name:
            col_name = f"c{col_ix}"
        if column.formatType:
            format_type = column.formatType.value
            spark_type = StringType() if string_only else SPARK_TYPE_BY_FORMAT_TYPE.get(format_type, StringType())
        else:
            spark_type = StringType()
        col_fields.append(StructField(col_name, spark_type, allow_null))
        col_ix += 1
    return col_fields


def find_duplicates_spark(df: DataFrame, unique_keys: List[List[int]], row_nr_column: str, has_error_col: str):
    """
    Try to find duplicates in the given DataFrame and report the
    line numbers of where such duplicates where found.
    """
    errors = []
    num_duplicates_total = 0
    before = datetime.now()

    duplicated_dfs = []
    for subset_columns_ix in unique_keys:
        df_columns = [column for column in df.columns if column != row_nr_column and column != has_error_col]
        subset_columns = [df_columns[col_ix] for col_ix in subset_columns_ix]

        # Check for duplicates based on the subset of columns
        window_spec = Window.partitionBy(*subset_columns)
        min_row_nr_column = f"{ROW_NUM_COLUMN}_min"
        df_with_dup_flag = (
            df
            .withColumn(min_row_nr_column, F.min(ROW_NUM_COLUMN).over(window_spec))
            .withColumn("is_duplicated", F.col(ROW_NUM_COLUMN) > F.col(min_row_nr_column))
            .drop(min_row_nr_column)
        )

        # TODO: Only mark the subsequent occurrences as dupes

        # Filter duplicates
        duplicated_df = df_with_dup_flag.filter("is_duplicated == true").select(row_nr_column).cache()
        num_duplicates = duplicated_df.count()
        num_duplicates_total += num_duplicates

        # Collect the row numbers of duplicates (limited to NUM_ERRORS_RECORD_BY_KEY_TUPLE)
        duplicated_rows_subset = (
            duplicated_df
            .sort(row_nr_column)
            .limit(NUM_ERRORS_RECORD_BY_KEY_TUPLE)
            .collect()
        )

        duplicated_dfs.append(duplicated_df)

        for row in duplicated_rows_subset:
            errors.append({
                "code": "DUPLICATE_VALUES",
                "location": {
                    "row": row[row_nr_column],
                    "columns": subset_columns_ix
                }
            })

    after = datetime.now()
    print(f"Finding duplicates took {(after - before).total_seconds() / 60} min")

    duplicated_df = functools.reduce(lambda a, b: a.union(b), duplicated_dfs).distinct()

    return duplicated_df, num_duplicates_total, errors


CHECK_FN_BY_FORMAT_TYPE = {
    "STRING": lambda _cell, _row, _colum: None,
    "INTEGER": validate.check_integer_str,
    "FLOAT": validate.check_float_str,
    "EMAIL": validate.check_email_str,
    "DATE_ISO8601": validate.check_date_str,
    "PHONE_NUMBER_E164": validate.check_phone_nr_e164_str,
    "HASH_SHA256_HEX": validate.check_hash_sha256_hex_str,
}


os.environ["RUST_BACKTRACE"] = "1"


def run(
        annotated_dataset_path: str,
        config_path: str,
        report_path: str,
        output_path: str,
        should_write_parquet: bool,
        should_check_uniqueness: bool,
        temp_dir: str = "/scratch",
        drop_invalid_rows: bool = False,
):
    config = read_config(config_path)

    with spark_session(
        temp_dir, name="Validation", input_files=[annotated_dataset_path]
    ) as ss:
        spark_schema = StructType(
            # These columns were added by the validation pipeline
            [
                StructField(ROW_NUM_COLUMN, IntegerType()),
                StructField(HAS_ERROR_COL, BooleanType()),
            ] +
            create_spark_schema_from_validation_config(config, string_only=True)
        )

        df = (
            ss.read
            .option("header", "false")
            .option("multiLine", "true")
            .option("mode", "DROPMALFORMED")
            .csv(annotated_dataset_path, schema=spark_schema)
            .persist(StorageLevel.MEMORY_AND_DISK)
        )

        print(f"Persisted input DF with {df.count()} columns")
        # Remove input DF as we might need the space later when also writing out
        # the final file again.
        # In local run mode this should be fine since there are no nodes that could go down,
        # so that parts of the files would need to be re-read.
        shutil.rmtree(annotated_dataset_path)

        if should_check_uniqueness:
            assert config.root.config.table is not None,\
                "Table validation settings must be defined"
            assert config.root.config.table.uniqueness is not None,\
                "Uniqueness validations settings must be defined"

            before = datetime.now()
            unique_keys: list[list[int]] = [
                [ix for ix in tpl.columns] for tpl in config.root.config.table.uniqueness.uniqueKeys
            ]
            print(f"Checking uniqueness for keys: {unique_keys}")
            duplicate_row_nrs_df, num_duplication_errors_total, duplication_errors = \
                find_duplicates_spark(df, unique_keys, ROW_NUM_COLUMN, HAS_ERROR_COL)
            update_report_with_uniqueness_check_result(
                report_path, duplication_errors, num_duplication_errors_total
            )
            after = datetime.now()
            print(f"Uniqueness check took {(after - before).total_seconds() / 60} min")
            df = add_erroneous_row_ids(df, duplicate_row_nrs_df)

        if drop_invalid_rows:
            print("Dropping invalid rows")
            num_invalid_rows = df.filter(F.col(HAS_ERROR_COL) == True).count()
            df = df.filter(F.col(HAS_ERROR_COL) == False)
            update_report_with_invalid_row_removal_result(report_path, num_invalid_rows)

        df = df.drop(HAS_ERROR_COL, ROW_NUM_COLUMN)

        is_passed = get_report_outcome(report_path) == ValidationOutcome.PASSED
        if is_passed:
            # Copy over the input data so that downstream computations can read it.
            before = datetime.now()
            if should_write_parquet:
                with tempfile.TemporaryDirectory(dir=temp_dir) as d:
                    temp_output_path = os.path.join(d, "_temp-dataset.parquet")
                    df.write.parquet(temp_output_path)
                    shutil.copytree(temp_output_path, output_path)
            else:
                write_df_as_single_file(df, output_path, temp_dir=temp_dir)
            after = datetime.now()
            fmt = "parquet" if should_write_parquet else "csv"
            print(f"Writing out {fmt} file took {(after - before).total_seconds() / 60} min")

        df.unpersist()

    #     columns = config.root.config.columns
    #
    #     check_exprs = []
    #     for jx, column in enumerate(columns):
    #         format_type = column.formatType.value
    #         column_name = column.name
    #         assert column_name is not None
    #         check_fn = CHECK_FN_BY_FORMAT_TYPE[format_type]
    #         check_udf = F.udf(check_fn, StringType())
    #         # bla = df.select(check_udf(F.col(column_name), F.lit(jx), F.col(ROW_NUM_COLUMN)))
    #
    #         check_expr = check_udf(F.col(column_name), F.lit(jx), F.col(ROW_NUM_COLUMN))
    #         check_expr_arr = F.when(check_expr.isNotNull(), F.array(check_expr)).otherwise(F.array())
    #         check_exprs.append(check_expr_arr)
    #
    #     df = df.withColumn("__errors", F.concat(*check_exprs))

            # import ipdb; ipdb.set_trace()
            # df_with_errors = df.withColumn("__errors",
            #                    F.when(check_expr.isNotNull(), F.concat(F.col("__errors"), F.array(check_expr))).otherwise(F.col("__errors")))
            # check_udf(F.col(jx))
