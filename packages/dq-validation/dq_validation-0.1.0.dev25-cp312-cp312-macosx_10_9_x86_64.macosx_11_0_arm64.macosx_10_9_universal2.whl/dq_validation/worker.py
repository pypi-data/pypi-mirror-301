import json
import os
import sys
import subprocess
import argparse
import shutil
import pandas as pd
import pyarrow
import pyarrow as pa
import pyarrow.parquet as pq
from typing import List, Optional, Tuple, Any
from datetime import datetime
from collections import defaultdict
import tempfile
import multiprocessing
import math
import psutil

from decentriq_util.spark import spark_session
from pyspark.sql.functions import count
from pyspark.sql import SparkSession, DataFrame, Window
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from pyspark.storagelevel import StorageLevel
from .schemas import ValidationConfig, ValidationReport
from . import default
from . import spark


CURRENT_FILE_PATH = os.path.abspath(__file__)


def read_config(path: str) -> ValidationConfig:
    with open(path, "r") as file:
        data = json.load(file)
        return ValidationConfig(**data)


def read_report(path: str) -> ValidationReport:
    with open(path, "r") as file:
        data = json.load(file)
        return ValidationReport(**data)


def write_df_as_single_file(df: DataFrame, path: str, temp_dir: str):
    """Write a dataframe into a single CSV file and store the result at `path`"""
    filename = os.path.basename(path)
    with tempfile.TemporaryDirectory(dir=temp_dir) as d:
        csv_parts_dir = os.path.join(d, filename)
        df.coalesce(1).write.csv(csv_parts_dir, header=False)
        csv_parts = [
            os.path.join(csv_parts_dir, f)
            for f in os.listdir(csv_parts_dir)
            if f.endswith(".csv")
        ]
        assert len(csv_parts) == 1
        single_csv_part = csv_parts[0]
        shutil.move(single_csv_part, path)


def _get_uncompressed_parquet_size(path: str):
    def is_parquet(filename: str):
        return filename.endswith(".parquet")

    def get_uncompressed_size(file_path: str):
        parquet_file = pq.ParquetFile(file_path)
        metadata = parquet_file.metadata
        uncompressed_size = 0
        for i in range(metadata.num_row_groups):
            row_group = metadata.row_group(i)
            for j in range(row_group.num_columns):
                column = row_group.column(j)
                uncompressed_size += column.total_uncompressed_size
        return uncompressed_size

    if os.path.isfile(path) and is_parquet(path):
        uncompressed_size = get_uncompressed_size(path)
        return uncompressed_size
    # Path might be a subdir as obtained by `partitionBy`
    elif os.path.isdir(path):
        total_uncompressed_size = 0
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            total_uncompressed_size += _get_uncompressed_parquet_size(file_path)
        return total_uncompressed_size
    else:
        return 0


def _get_cgroup_memory() -> int:
    max_memory_str = None
    if os.path.isfile("/sys/fs/cgroup/memory.max"):
        with open("/sys/fs/cgroup/memory.max", "r") as f:
            max_memory_str = f.read().strip()
    elif os.path.isfile("/sys/fs/cgroup/memory/memory.limit_in_bytes"):
        with open("/sys/fs/cgroup/memory/memory.limit_in_bytes", "r") as f:
            max_memory_str = f.read().strip()

    max_memory = None
    if max_memory_str == "max":
        # Fallback to available virtual memory size
        max_memory = psutil.virtual_memory().available
    elif max_memory_str is not None:
        max_memory = int(max_memory_str)

    if max_memory is not None:
        return max_memory
    else:
        print("Unable to determine available memory from cgroup, assuming 4G")
        return 4 * 1024 * 1024 * 1024


def _get_num_partitions(
        paths: list[str],
        available_memory: int,
        cpu_count: int,
) -> int:
    """Determine the number of partitions s.t. each partition is as big as possible
    while still making sure all cores are occupied."""

    def get_file_or_dir_size(path):
        if path.endswith(".parquet"):
            return _get_uncompressed_parquet_size(path)
        else:
            if os.path.isfile(path):
                size = os.path.getsize(path)
            elif os.path.isdir(path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                size = total_size
            else:
                raise ValueError(f"The path {path} is neither a file nor a directory.")
        return size

    file_size = max([get_file_or_dir_size(path) for path in paths])
    if file_size == 0:
        return 200  # default number of partitions in spark

    # Don't make the partitions smaller than 36MiB
    megabyte_in_bytes = 1024 * 1024
    min_partition_size = 32 * megabyte_in_bytes

    # Try to make partitions as big as possible s.t. each CPU is saturated,
    # while accounting for 50% overhead in spark.
    # task_per_cpu = 3  # try to get at least this many tasks/partitions per CPU
    task_per_cpu = 3  # try to get at least this many tasks/partitions per CPU
    max_target_partition_size = max(
        int(0.5 * available_memory / (task_per_cpu * cpu_count)) // megabyte_in_bytes * megabyte_in_bytes,
        min_partition_size
    )

    target_partition_size = max_target_partition_size
    while (
            # If the file is small enough that it cannot be split across all cores,
            # divide the partition size further.
            int(file_size / target_partition_size) < (task_per_cpu * cpu_count)
    ):
        # Don't go smaller than the minimum parition size
        if target_partition_size / 2 < min_partition_size:
            break
        target_partition_size = target_partition_size / 2

    print(f"File size: {file_size}")
    print(f"Max target partition size: {max_target_partition_size}")
    print(f"Target partition size: {target_partition_size}")

    num_partitions = int(math.ceil(file_size / target_partition_size))

    return num_partitions


def get_spark_config(
        files: list[str],
        heap_size_extra_room: Optional[int] = 2 * 512 * 1024 * 1024
) -> list[Tuple[str, str]]:
    def get_spark_memory() -> int:
        """Determine the amount of memory available to spark"""
        cgroup_memory = _get_cgroup_memory()
        spark_memory = cgroup_memory - (heap_size_extra_room or 512 * 1024 * 1024)
        return spark_memory

    spark_memory = get_spark_memory()
    spark_memory_4096 = (spark_memory // 4096) * 4096
    cpu_count = multiprocessing.cpu_count()
    num_partitions = _get_num_partitions(files, spark_memory, cpu_count)

    settings = [
        ("spark.sql.shuffle.partitions", str(num_partitions)),
        ("spark.default.parallelism", str(num_partitions)),
        ("spark.driver.cores", str(cpu_count)),
        ("spark.driver.memory", str(spark_memory_4096)),
    ]
    print("Spark settings:\n" + f"\n".join([str(x) for x in settings]))

    return settings


# If the input file is smaller or equal to that threshold, use
# pandas instead of spark to check for duplicates or writing parquet.
# This way we avoid spinning up a spark session (especially important
# during CI runs where we work with small test files).
DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES = 5 * 10 ** 9

NUM_ERRORS_RECORD_BY_KEY_TUPLE = 10

ROW_NUM_COLUMN = "row_nr"

PYARROW_TYPE_BY_FORMAT_TYPE = {
    "STRING": pa.string(),
    "INTEGER": pa.int32(),
    "FLOAT": pa.float32(),
    "EMAIL": pa.string(),
    "DATE_ISO_8601": pa.string(),
    "PHONE_NUMBER_E164": pa.string(),
    "HASH_SHA_256_HEX": pa.string(),
}

SPARK_TYPE_BY_FORMAT_TYPE = {
    "STRING": StringType(),
    "INTEGER": IntegerType(),
    "FLOAT": FloatType(),
    "EMAIL": StringType(),
    "DATE_ISO_8601": StringType(),
    "PHONE_NUMBER_E164": StringType(),
    "HASH_SHA_256_HEX": StringType(),
}

os.environ["RUST_BACKTRACE"] = "1"

def find_duplicates_pandas(csv: pd.DataFrame, unique_keys: List[List[int]]):
    """
    Try to find duplicates in the given CSV file and report the line
    numbers of where such duplicates where found.
    """
    csv.columns = range(csv.shape[1])
    errors = []
    num_duplicates_total = 0
    for subset_columns in unique_keys:
        csv.columns = list(range(csv.shape[1]))
        is_duplicated = csv.duplicated(
            subset=subset_columns,
            # Consider every occurrence as a "duplicate, not just
            # the first one (if one row is repeated 10 times, it should
            # be reported as 10 duplicate rows).
            # This matches the Spark implementation.
            keep=False
        )
        num_duplicates_total += sum(is_duplicated)
        duplicated_rows_subset = list(csv.index[is_duplicated][:NUM_ERRORS_RECORD_BY_KEY_TUPLE])
        for row in duplicated_rows_subset:
            errors.append({
                "code": "DUPLICATE_KEY",
                "location": {
                    "row": row,
                    "columns": subset_columns
                }
            })
    return csv, num_duplicates_total, errors


def find_duplicates_spark(df: DataFrame, unique_keys: List[List[int]], row_nr_column: str):
    """
    Try to find duplicates in the given DataFrame and report the
    line numbers of where such duplicates where found.
    """
    errors = []
    num_duplicates_total = 0
    before = datetime.now()

    for subset_columns_ix in unique_keys:
        df_columns = [column for column in df.columns if column != row_nr_column]
        subset_columns = [df_columns[col_ix] for col_ix in subset_columns_ix]

        # Check for duplicates based on the subset of columns
        window_spec = Window.partitionBy(*subset_columns)
        df_with_dup_flag = df.withColumn("is_duplicated", count("*").over(window_spec) > 1)

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

        for row in duplicated_rows_subset:
            errors.append({
                "code": "DUPLICATE_KEY",
                "location": {
                    "row": row[row_nr_column],
                    "columns": subset_columns_ix
                }
            })

    after = datetime.now()
    print(f"Finding duplicates took {(after - before).total_seconds() / 60} min")

    return duplicated_df, num_duplicates_total, errors


# Top-level "driver script" of the parallelized validation. Uses split to split the input
# into fixed-sized chunks and fifos for communication and to apply backpressure
run_sh = '''
#!/usr/bin/env bash
set -euo pipefail

BIN="$1"
CONFIG="$2"
INPUT="$3"
REPORT="$4"
TYPES="$5"
CHUNK_SIZE="$6"
WORKER_PY="$7"
# Can be set to gstat on mac
STAT_BIN="${STAT_BIN:-stat}"

# If the size of the input is small (<64M), run the validation in non-parallel mode
if [[ $($STAT_BIN --printf="%s" "$INPUT") -lt $((64 * 1024 * 1024)) ]]
then
  # Remove all leading line numbers that were artificially added to the file.
  cut -d, -f2- "$INPUT" > "$INPUT.temp"
  function cleanup {
    rm -f "$INPUT.temp"
  }
  trap cleanup EXIT
  "$BIN" "$CONFIG" "$INPUT.temp" "$REPORT" "$TYPES"
  exit 0
fi

# First determine the parallelism based on nproc and the cgroup memory
if [[ -f /sys/fs/cgroup/memory.max ]]
then
  AVAILABLE_MEMORY=$(cat /sys/fs/cgroup/memory.max)
elif [[ -f /sys/fs/cgroup/memory/memory.limit_in_bytes ]]
then
  AVAILABLE_MEMORY=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes)
else
  echo "Cannot determine available memory"
  exit 1
fi

PARALLELISM_MEMORY=$((($AVAILABLE_MEMORY - 64 * 1024 * 1024) / (128 * 1024 * 1024 + $CHUNK_SIZE)))
PARALLELISM_CPU=$(($(nproc) - 1))
if [[ "$PARALLELISM_MEMORY" -gt "$PARALLELISM_CPU" ]]
then
  PARALLELISM="$PARALLELISM_CPU"
else
  PARALLELISM="$PARALLELISM_MEMORY"
fi
if [[ "$PARALLELISM" -gt 12 ]]
then
  PARALLELISM=12
fi
echo Parallelism is "$PARALLELISM"

# Create fifo queues.
# The task queue is consumed by filter.sh and used to provide backpressure to split so it doesn't "run ahead".
# The result queue is consumed by the final merge.sh
mkfifo /tmp/task
mkfifo /tmp/result
function cleanup {
  rm -f /tmp/task /tmp/result
}
exec 3<>/tmp/task
exec 4<>/tmp/result

for i in $(seq 1 "$PARALLELISM")
do
  echo "$BIN" "$CONFIG" >&3
done

bash /tmp/merge.sh "$REPORT" "$TYPES" "$WORKER_PY" &
MERGE_PID=$!

split -C "$CHUNK_SIZE" --filter="bash /tmp/filter.sh" "$INPUT"
CHUNK_COUNT=$(cat /tmp/chunk_count)
echo "chunk_count $CHUNK_COUNT" >&4

wait $MERGE_PID
'''

# Passed to split. Reads a task from the task fifo, dumps stdin to an input file, runs the validation program in the background
# return early to split, and then when processing is finished writes the next task to the task queue as well as writes
# to the result queue, to be processed by merge.sh.
# FD 3: task fifo
# FD 4: result fifo
filter_sh = '''
#!/usr/bin/env bash
set -euo pipefail

read -u 3 line
read -a task <<<"$line"

if [[ "$line" = "error" ]]
then
  exit 1
fi

BIN=${task[0]}
CONFIG=${task[1]}

if [[ -f /tmp/chunk_count ]]
then
  I=$(($(cat /tmp/chunk_count) + 1))
else
  I=1
fi
echo -n "$I" > /tmp/chunk_count

INPUT=/tmp/input_"$I".csv
OUTPUT=/tmp/output_"$I".json
TYPES=/tmp/types_"$I"
ROW_COUNT=/tmp/row_count_"$I"

# Remove all leading line numbers that were artificially added to the file.
cut -d, -f2- < /dev/stdin > "$INPUT"

(
  function cleanup {
    rm -f "$INPUT"
  }
  trap cleanup EXIT
  function error {
    echo error >&3
    echo error >&4
  }
  trap error ERR
  "$BIN" "$CONFIG" "$INPUT" "$OUTPUT" "$TYPES"
  wc -l < "$INPUT" > "$ROW_COUNT"
  echo "result $OUTPUT $TYPES $ROW_COUNT" >&4
  echo "$BIN $CONFIG" >&3
) &
'''

# Merges individual validation results
merge_sh = '''
#!/usr/bin/env bash
set -euo pipefail

REPORT="$1"
TYPES_FINAL="$2"
WORKER_PY="$3"

WORKER_MODULE_NAME="$(basename ${WORKER_PY%.*})"
DONE=0
CHUNK_COUNT=
while ! [[ "$DONE" = "$CHUNK_COUNT" ]]
do
  read -u 4 line
  read -a result <<<"$line"
  if [[ "${result[0]}" = "chunk_count" ]]
  then
    CHUNK_COUNT=${result[1]}
    continue
  fi

  if [[ "${result[0]}" = "error" ]]
  then
    echo "Error during validation"
    exit 1
  fi

  OUTPUT=${result[1]}
  TYPES=${result[2]}
  ROW_COUNT=${result[3]}

  DONE=$(($DONE + 1))
  if [[ $(($DONE % 64)) -eq 0 ]]
  then
    echo Merge high=$DONE
    cd $(dirname "$WORKER_PY") && python3 -c "from $WORKER_MODULE_NAME import merge_result; merge_result()" "$DONE"
  fi
done
cd $(dirname "$WORKER_PY") && python3 -c "from $WORKER_MODULE_NAME import merge_result; merge_result()" "$DONE"
mv /tmp/merge_current "$REPORT"
# /tmp/merge_types may not exist if validation failed
if [[ -f /tmp/merge_types ]]
then
  mv /tmp/merge_types "$TYPES_FINAL"
fi
'''


# This may be called out of order, so we need to buffer until we "fill the holes". We do this by utilizing $DONE from
# merge.sh which indicates the "high watermark" of results, namely how many chunks have been processed.
# merge_result() then keeps a "low watermark" which indicates the last successfully merged chunk.
# On each call we process the outputs from low_watermark up until we have a "hole" or we reach the high_watermark.
def merge_result():
    high_watermark = int(sys.argv[1])
    if os.path.isfile("/tmp/merge_low_watermark"):
        with open("/tmp/merge_low_watermark", "r") as file:
            low_watermark = int(file.read())
    else:
        low_watermark = 0

    if os.path.isfile("/tmp/merge_row_offset"):
        with open("/tmp/merge_row_offset", "r") as file:
            row_offset = int(file.read())
    else:
        row_offset = 0

    if os.path.isfile("/tmp/merge_current"):
        with open("/tmp/merge_current", "r") as file:
            merge_current = json.load(file)
    else:
        merge_current = {
            "version": "v0",
            "report": {
                "columns": [],
                "schema": {
                    "recordedErrors": [],
                    "numErrorsTotal": 0,
                },
                "table": {
                    "recordedErrors": [],
                    "numErrorsTotal": 0,
                },
                "outcome": "PASSED",
                "numInvalidRowsTotal": 0,
            },
        }

    i = low_watermark
    for i in range(low_watermark, high_watermark):
        report_path = f"/tmp/output_{i + 1}.json"
        if os.path.isfile(report_path):
            with open(report_path, "r") as file:
                report_json = json.load(file)
            os.remove(report_path)
            row_count_path = f"/tmp/row_count_{i + 1}"
            with open(row_count_path) as file:
                row_count = int(file.read())
            os.remove(row_count_path)
            merge_current = merge_single(merge_current, report_json, row_offset)
            types_path = f"/tmp/types_{i + 1}"
            if os.path.isfile(types_path):
                shutil.copyfile(types_path, "/tmp/merge_types")
                os.remove(types_path)
            row_offset += row_count
        else:
            i -= 1
            break
    next_low_watermark = i + 1

    with open("/tmp/merge_low_watermark", "w") as file:
        file.write(str(next_low_watermark))
    with open("/tmp/merge_row_offset", "w") as file:
        file.write(str(row_offset))
    with open("/tmp/merge_current", "w") as file:
        json.dump(merge_current, file)


def dump_report(report):
    dump = {
        "columns": list(map(lambda column: {
            "column": column["column"],
            "recordedErrors": len(column["recordedErrors"]),
            "numErrorsTotal": column["numErrorsTotal"],
        }, report["report"]["columns"])),
        "schema": {
            "recordedErrors": len(report["report"]["schema"]["recordedErrors"]),
            "numErrorsTotal": report["report"]["schema"]["numErrorsTotal"],
        },
        "table": {
            "recordedErrors": len(report["report"]["table"]["recordedErrors"]),
            "numErrorsTotal": report["report"]["table"]["numErrorsTotal"],
        },
        "outcome": report["report"]["outcome"],
        "numInvalidRowsTotal": report["report"]["numInvalidRowsTotal"],
    }
    print(json.dumps(dump, indent=2))


def merge_single(report_current, report, row_offset):
    # Cell errors
    current_cell_error_count = 0
    for column in report_current['report']['columns']:
        current_cell_error_count += len(column['recordedErrors'])
    maximum_cell_errors = 499
    for column in report['report']['columns']:
        column_number = column['column']
        existing = [col for i, col in enumerate(report_current['report']['columns']) if col['column'] == column_number]

        if len(existing) == 0:
            column_to_add_to = {
                'column': column_number,
                'recordedErrors': [],
                'numErrorsTotal': 0,
            }
            report_current['report']['columns'].append(column_to_add_to)
        else:
            column_to_add_to = existing[0]
        added_error_count = min(len(column['recordedErrors']), maximum_cell_errors - current_cell_error_count)
        column_to_add_to['numErrorsTotal'] += column['numErrorsTotal']
        added_errors = column['recordedErrors'][:added_error_count]
        for error in added_errors:
            error['location']['row'] += row_offset
        column_to_add_to['recordedErrors'].extend(added_errors)
        current_cell_error_count += added_error_count

    # Schema errors
    maximum_schema_errors = 499
    added_error_count = min(len(report['report']['schema']['recordedErrors']),
                            maximum_schema_errors - len(report_current['report']['schema']['recordedErrors']))
    added_errors = report['report']['schema']['recordedErrors'][:added_error_count]
    for error in added_errors:
        error['row'] += row_offset
    report_current['report']['schema']['recordedErrors'].extend(added_errors)
    report_current['report']['schema']['numErrorsTotal'] += report['report']['schema']['numErrorsTotal']

    # Table errors
    maximum_table_errors = 499
    added_error_count = min(len(report['report']['table']['recordedErrors']),
                            maximum_table_errors - len(report_current['report']['table']['recordedErrors']))
    added_errors = report['report']['table']['recordedErrors'][:added_error_count]
    report_current['report']['table']['recordedErrors'].extend(added_errors)
    report_current['report']['table']['numErrorsTotal'] += report['report']['table']['numErrorsTotal']

    report_current['report']['outcome'] = "PASSED" if report_current['report']['outcome'] == "PASSED" and \
                                                      report['report']['outcome'] == "PASSED" else "FAILED"
    report_current['report']['numInvalidRowsTotal'] += report['report']['numInvalidRowsTotal']
    return report_current


def create_pyarrow_schema_from_validation_config(config: ValidationConfig) -> pyarrow.Schema:
    col_ix = 0
    col_fields = []
    for column in config.root.config.columns:
        col_name = column.name
        allow_null = column.allowNull
        if not col_name:
            col_name = f"c{col_ix}"
        if column.formatType:
            format_type = column.formatType.value
            tpe = PYARROW_TYPE_BY_FORMAT_TYPE.get(format_type, pa.string())
        else:
            tpe = pa.string()
        col_fields.append(pa.field(col_name, tpe, nullable=allow_null))
        col_ix += 1
    schema = pa.schema(col_fields)
    return schema


def create_spark_schema_from_validation_config(config: ValidationConfig) -> List[StructField]:
    col_ix = 0
    col_fields = []
    for column in config.root.config.columns:
        col_name = column.name
        allow_null = column.allowNull
        if not col_name:
            col_name = f"c{col_ix}"
        if column.formatType:
            format_type = column.formatType.value
            spark_type = SPARK_TYPE_BY_FORMAT_TYPE.get(format_type, StringType())
        else:
            spark_type = StringType()
        col_fields.append(StructField(col_name, spark_type, allow_null))
        col_ix += 1
    return col_fields


def remove_line_numbers_from_file_and_write_file(input_file, output_file):
    with open(output_file, "w") as f:
        process = subprocess.run(
            ["cut", "-d,", "-f2-", input_file],
            stdout=f,
            text=True
        )
        if process.returncode != 0:
            raise Exception(f"Failed to remove line numbers")


def update_report_with_uniqueness_check_result(
        report_path: str,
        duplication_errors,
        num_duplication_errors_total: int
):
    with open(report_path, "r") as f:
        report = json.load(f)
    report["report"]["uniqueness"] = {
        "recordedErrors": duplication_errors,
        "numErrorsTotal": num_duplication_errors_total
    }
    if num_duplication_errors_total and num_duplication_errors_total > 0:
        report["report"]["outcome"] = "FAILED"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)


def update_report_with_deduplication_result(
        report_path: str,
        duplication_errors,
        num_duplicates_removed: int
):
    with open(report_path, "r") as f:
        report = json.load(f)
    report["report"]["deduplication"] = {
        "recordedDuplicationErrors": duplication_errors,
        "numDuplicatesRemoved": num_duplicates_removed
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)


def run(
        bin_path: str,
        input_path: str,
        config_path: str,
        report_path: str,
        types_path: str,
        output_path: str,
        force_spark: bool = False,
        worker_py: str = CURRENT_FILE_PATH,
        spark_threshold_bytes: int = DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES,
        temp_dir: str = "/scratch",
        drop_invalid_rows: bool = False,
):
    input_file_path = os.path.join(temp_dir, "dataset.csv")

    does_input_file_exist = os.path.exists(input_path)
    if not does_input_file_exist:
        raise Exception("Input file does not exist")

    input_file_size = os.path.getsize(input_path)

    if force_spark or input_file_size > spark_threshold_bytes:
        use_spark = True
    else:
        use_spark = False

    if not use_spark:
        default.run(
            input_path=input_path,
            config_path=config_path,
            report_path=report_path,
            types_path=types_path,
            output_path=output_path,
            temp_dir=temp_dir,
            drop_invalid_rows=drop_invalid_rows
        )
    else:
        spark.run(
            input_path=input_path,
            config_path=config_path,
            report_path=report_path,
            types_path=types_path,
            output_path=output_path,
            temp_dir=temp_dir,
            drop_invalid_rows=drop_invalid_rows
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Validation",
        description="Validation of input data"
    )
    parser.add_argument(
        "-i", "--input",
        help="Path to the data to be validated"
    )
    parser.add_argument(
        "-c", "--config",
        help="Path to the validation config in JSON format"
    )
    parser.add_argument(
        "-b", "--bin",
        help="Path to the validation program"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to where the validated results should be stored"
    )
    parser.add_argument(
        "-r", "--report",
        help="Path to where the final report should be stored"
    )
    parser.add_argument(
        "-t", "--types",
        help="Path to where the types info file should be stored"
    )
    parser.add_argument(
        "--force-spark",
        dest="force_spark",
        action="store_true",
        help="Whether to force the validation to use spark (e.g. for testing)"
    )
    parser.add_argument(
        "--spark-threshold-bytes",
        dest="spark_threshold_bytes",
        type=int,
        required=False,
        default=DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES,
        help=(
            "Input files bigger than the given threshold are processed using pyspark."
        )
    )
    args = parser.parse_args()
    worker_py = sys.argv[0]
    run(
        worker_py=worker_py,
        input_path=args.input,
        report_path=args.report,
        types_path=args.types,
        output_path=args.output,
        force_spark=args.force_spark,
        spark_threshold_bytes=args.spark_threshold_bytes,
        bin_path=args.bin,
        config_path=args.config,
    )
