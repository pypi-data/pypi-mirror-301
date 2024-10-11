from pathlib import Path

import pytest

from cdef_converter.exceptions import EncodingDetectionError
from cdef_converter.file_processing import detect_encoding_incrementally, read_file


def test_detect_encoding_incrementally_error():
    with pytest.raises(EncodingDetectionError):
        detect_encoding_incrementally(Path("non_existent_file.txt"))


def test_detect_encoding_incrementally():
    # Create a temporary file with known encoding
    temp_file = Path("temp_test_file.txt")
    temp_file.write_text("Hello, world!", encoding="utf-8")

    assert detect_encoding_incrementally(temp_file) == "utf-8"

    temp_file.unlink()  # Clean up


def test_read_file():
    # Create a temporary CSV file
    temp_file = Path("temp_test_file.csv")
    temp_file.write_text("column1,column2\n1,2\n3,4", encoding="utf-8")

    df = read_file(temp_file)
    assert len(df) == 2
    assert df.columns == ["column1", "column2"]

    temp_file.unlink()  # Clean up


# Add more tests for other functions
