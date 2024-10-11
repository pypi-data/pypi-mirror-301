import os
from pathlib import Path
from typing import Annotated

import typer

from cdef_converter.config import DEFAULT_ENCODING_CHUNK_SIZE, OUTPUT_DIRECTORY
from cdef_converter.main import main

app = typer.Typer()


@app.command()
def convert(
    input_directory: Annotated[
        Path,
        typer.Argument(help="Path to the input directory containing CSV and/or Parquet files"),
    ],
    output_directory: Annotated[
        Path,
        typer.Option(
            help="Path to the output directory for converted Parquet files",
        ),
    ] = OUTPUT_DIRECTORY,
    processes: Annotated[
        int,
        typer.Option(help="Number of processes to use for parallel processing"),
    ] = 4,
    encoding_chunk_size: Annotated[
        int,
        typer.Option(
            help="Chunk size (in MB) for encoding detection",
            show_default="1 MB",
        ),
    ] = DEFAULT_ENCODING_CHUNK_SIZE,
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            "-r",
            help="Recursively search for files in subdirectories",
        ),
    ] = False,
) -> None:
    """
    Convert CSV/Parquet files to Parquet format and generate a summary.

    This script processes CSV and Parquet files in the input directory,
    converts them to Parquet format, and saves them in the output directory.
    It also generates a summary of the processed files.

    If the --recursive option is used, the script will search for files
    in all subdirectories of the input directory.

    The conversion process includes:
    1. Detecting file encoding for CSV files
    2. Reading the input files (CSV or Parquet)
    3. Writing the data to Parquet format
    4. Verifying the written data
    5. Generating a summary of processed files
    """
    os.environ["CDEF_OUTPUT_DIR"] = str(output_directory)
    # Convert MB to bytes
    encoding_chunk_size_bytes = encoding_chunk_size * 1024 * 1024
    main(input_directory, processes, encoding_chunk_size_bytes, recursive)


def run_convert() -> None:
    app()
