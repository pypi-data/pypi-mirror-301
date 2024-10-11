NUM_ERRORS_RECORD_BY_KEY_TUPLE = 10
ROW_NUM_COLUMN = "__row_nr"
DEFAULT_NUM_RECORD_CELL_ERRORS = 500
DEFAULT_NUM_RECORD_SCHEMA_ERRORS = 500
# If the input file is smaller or equal to that threshold, use
# pandas instead of spark to check for duplicates or writing parquet.
# This way we avoid spinning up a spark session (especially important
# during CI runs where we work with small test files).
DEFAULT_USE_SPARK_FILE_SIZE_THRESHOLD_BYTES = 5 * 10 ** 9
