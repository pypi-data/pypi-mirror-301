import json

from cdef_converter.utils import print_summary_table, save_summary


def test_save_summary(tmp_path):
    summary = {
        "test": {
            "2021": {
                "file_name": "test.csv",
                "num_rows": 100,
                "num_columns": 5,
                "column_names": ["A", "B", "C", "D", "E"],
            }
        }
    }
    output_file = tmp_path / "test_summary.json"
    save_summary(summary, output_file)
    assert output_file.exists()
    with open(output_file) as f:
        loaded_summary = json.load(f)
    assert loaded_summary == summary


def test_print_summary_table():
    summary = {
        "test": {
            "2021": {
                "file_name": "test.csv",
                "num_rows": 100,
                "num_columns": 5,
                "column_names": ["A", "B", "C", "D", "E"],
            }
        }
    }
    panel = print_summary_table(summary)
    assert panel is not None
