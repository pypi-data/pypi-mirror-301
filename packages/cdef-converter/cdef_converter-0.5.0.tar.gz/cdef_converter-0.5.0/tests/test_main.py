from unittest.mock import patch

from cdef_converter.main import main


@patch('cdef_converter.main.process_files_with_progress')
@patch('cdef_converter.main.print_summary_table')
@patch('cdef_converter.main.save_summary')
def test_main(mock_save_summary, mock_print_summary_table, mock_process_files, tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "test.csv").touch()

    main(input_dir, 2)

    mock_process_files.assert_called_once()
    mock_print_summary_table.assert_called_once()
    mock_save_summary.assert_called_once()
