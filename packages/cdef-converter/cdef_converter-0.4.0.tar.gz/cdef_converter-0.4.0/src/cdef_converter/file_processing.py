import multiprocessing
from pathlib import Path
from queue import Queue
from typing import Any

import polars as pl
import pyarrow.parquet as pq
from charset_normalizer import from_bytes

from cdef_converter.config import DEFAULT_ENCODING_CHUNK_SIZE, FILE_PATTERN_REGEX, OUTPUT_DIRECTORY
from cdef_converter.exceptions import EncodingDetectionError, FileProcessingError, ParquetWriteError
from cdef_converter.logging_config import log, logger


def detect_encoding_incrementally(
    file_path: Path, chunk_size: int = DEFAULT_ENCODING_CHUNK_SIZE * 1024 * 1024
) -> str:
    """
    Detect the encoding of a file incrementally.

    Args:
        file_path (Path): Path to the file to detect encoding for.
        chunk_size (int): Size of the chunk to read in bytes (default is 1 MB)

    Returns:
        str: Detected encoding of the file.
    """
    try:
        file_size = file_path.stat().st_size

        # Adjust chunk size based on file size
        if file_size < chunk_size:
            chunk_size = file_size
        elif file_size > 100 * chunk_size:  # For very large files
            chunk_size = file_size // 100  # Read 1% of the file

        with open(file_path, "rb") as file:
            chunk = file.read(chunk_size)
            result = from_bytes(chunk).best()

        if result is None:
            return "utf-8"

        if result.encoding == "ascii":
            return "utf-8"

        return result.encoding
    except Exception as err:
        raise EncodingDetectionError(f"Error detecting encoding for {file_path}") from err


def read_file(
    file_path: Path, encoding_chunk_size: int = DEFAULT_ENCODING_CHUNK_SIZE
) -> pl.DataFrame:
    """
    Read a CSV or Parquet file into a Polars DataFrame.

    Args:
        file_path (Path): Path to the file to read.

    Returns:
        pl.DataFrame: DataFrame containing the file contents.

    Raises:
        ValueError: If the file format is not supported.
    """
    try:
        if file_path.suffix.lower() == ".parquet":
            return pl.read_parquet(file_path)
        elif file_path.suffix.lower() == ".csv":
            encoding = detect_encoding_incrementally(file_path, encoding_chunk_size)
            return pl.read_csv(
                file_path,
                encoding=encoding,
                null_values=["", "NULL", "null", "NA", "na", "NaN", "nan"],
                ignore_errors=False,
                low_memory=False,
                sample_size=10000,
                infer_schema=False,
            )
        else:
            raise FileProcessingError(f"Unsupported file format: {file_path.suffix}")
    except Exception as err:
        raise FileProcessingError(f"Error reading file {file_path.name}") from err


def write_parquet_fast(df: pl.DataFrame, path: Path) -> None:
    try:
        arrow_table = df.to_arrow()
        pq.write_table(arrow_table, path)
    except Exception as err:
        raise ParquetWriteError(f"Error writing Parquet file {path}") from err


def process_file(
    file_path: Path,
    progress_queue: Queue[Any],
    encoding_chunk_size: int = DEFAULT_ENCODING_CHUNK_SIZE,
) -> None:
    try:
        file_stem = file_path.stem

        match = FILE_PATTERN_REGEX.match(file_stem)

        if match:
            register_name = match.group(1).lower().rstrip("_")
            year = match.group(2)
            output_filename = f"{year}.parquet"
        else:
            register_name = file_stem.lower()
            year = ""
            output_filename = f"{register_name}.parquet"

        output_path = OUTPUT_DIRECTORY / "registers" / register_name / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists():
            if output_path.stat().st_size <= 1_048_576:  # 1 MB threshold
                log(f"Deleting small Parquet file for reprocessing: {output_path}")
                output_path.unlink()
            else:
                log(f"Skipping already processed file: {file_path}")
                df = pl.read_parquet(output_path)
                progress_queue.put(
                    (
                        multiprocessing.current_process().name,
                        file_path.name,
                        "Completed",
                        (
                            register_name,
                            year,
                            {
                                "file_name": file_path.name,
                                "num_rows": len(df),
                                "num_columns": len(df.columns),
                                "column_names": df.columns,
                            },
                        ),
                    )
                )
                return

        progress_queue.put(
            (multiprocessing.current_process().name, file_path.name, "Processing", None)
        )
        df = read_file(file_path, encoding_chunk_size)
        write_parquet_fast(df, output_path)

        read_back_df = pl.read_parquet(output_path)
        if not df.equals(read_back_df):
            raise ValueError("Verification failed: written data does not match original data")

        log_message = f"Processed {file_path.name} -> {output_path}"

        progress_queue.put(
            (
                multiprocessing.current_process().name,
                file_path.name,
                "Completed",
                (
                    register_name,
                    year,
                    {
                        "file_name": file_path.name,
                        "num_rows": len(df),
                        "num_columns": len(df.columns),
                        "column_names": df.columns,
                    },
                ),
                log_message,
            )
        )

    except (FileProcessingError, EncodingDetectionError, ParquetWriteError) as e:
        progress_queue.put((multiprocessing.current_process().name, file_path.name, "Error", None))
        logger.exception(f"Error processing file {file_path}: {str(e)}")
    except Exception as e:
        progress_queue.put((multiprocessing.current_process().name, file_path.name, "Error", None))
        logger.exception(f"Unexpected error processing file {file_path}: {str(e)}")
