from multiprocessing import Queue

from cdef_converter.progress import display_progress


def test_display_progress(capsys):
    progress_queue = Queue()
    total_files = 2
    progress_queue.put(("Process1", "file1.csv", "Processing"))
    progress_queue.put(("Process1", "file1.csv", "Completed"))
    progress_queue.put(("Process2", "file2.csv", "Processing"))
    progress_queue.put(("Process2", "file2.csv", "Completed"))

    display_progress(progress_queue, total_files)

    captured = capsys.readouterr()
    assert "Processing complete!" in captured.out
