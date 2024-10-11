import shutil
import sys
import os
from datetime import datetime

from .config import DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES

from . import spark
from . import default
from . import validate
from .utils import get_report_outcome, read_config
from .schemas import ValidationOutcome


def run(
        input_path: str,
        config_path: str,
        report_path: str,
        types_path: str,
        output_path: str,
        force_spark: bool = False,
        spark_threshold_bytes: int = DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES,
        temp_dir: str = "/scratch",
        drop_invalid_rows: bool = False,
):
    config = read_config(config_path)

    does_input_file_exist = os.path.exists(input_path)
    if not does_input_file_exist:
        raise Exception("Input file does not exist")

    input_file_size = os.path.getsize(input_path)
    print(f"Input file size: {round(input_file_size / 1000000, 2)} MB")

    if force_spark or input_file_size > spark_threshold_bytes:
        use_spark = True
    else:
        use_spark = False

    # Whether this pipeline should produce parquet or csv file output.
    should_write_parquet = output_path.endswith(".parquet")

    # Check whether we should detect duplicates.
    should_check_uniqueness = (
        config.root.config.table is not None
        and config.root.config.table.uniqueness is not None
        and config.root.config.table.uniqueness.uniqueKeys is not None
    )

    # Where to store the annotated output of the validation pipeline
    annotated_dataset_path = os.path.join(temp_dir, "_annotated_dataset")

    before = datetime.now()
    validate.run_validation_program(
        input_path=input_path,
        config_path=config_path,
        output_path=report_path,
        types_path=types_path,
        annotated_dataset_path=annotated_dataset_path,
    )
    after = datetime.now()
    print(f"Validation pipeline took {(after - before).total_seconds() / 60} min")

    # Check if we can perform an early exit.
    did_pre_validation_pass = get_report_outcome(report_path) == ValidationOutcome.PASSED
    if did_pre_validation_pass:
        if not should_check_uniqueness and not should_write_parquet:
            shutil.copyfile(input_path, output_path)
            sys.exit(0)
    else:
        if not drop_invalid_rows:
            sys.exit(0)

    print(f"Continue w/ pipeline (use spark: {use_spark})")

    if not use_spark:
        default.run(
            annotated_dataset_path=annotated_dataset_path,
            should_write_parquet=should_write_parquet,
            should_check_uniqueness=should_check_uniqueness,
            config_path=config_path,
            report_path=report_path,
            output_path=output_path,
            drop_invalid_rows=drop_invalid_rows
        )
    else:
        spark.run(
            annotated_dataset_path=annotated_dataset_path,
            should_write_parquet=should_write_parquet,
            should_check_uniqueness=should_check_uniqueness,
            config_path=config_path,
            report_path=report_path,
            output_path=output_path,
            temp_dir=temp_dir,
            drop_invalid_rows=drop_invalid_rows
        )
