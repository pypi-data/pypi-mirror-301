import time
from queue import Queue
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.text import Text

from cdef_converter.config import GREEN

console = Console()


def display_progress(progress_queue: Queue[Any], total_files: int, summary: dict[str, Any]) -> None:
    completed_files = 0
    process_status: dict[str, tuple[str, str]] = {}
    start_time = time.time()

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        TextColumn("{task.fields[speed]:.2f} files/sec"),
        console=console,
        expand=True,
    ) as progress:
        task = progress.add_task("[cyan]Processing files...", total=total_files, speed=0)

        while completed_files < total_files:
            if not progress_queue.empty():
                item = progress_queue.get()
                if item is None:  # Termination signal
                    break
                process_name, file_name, status, result = item
                process_status[process_name] = (file_name, status)
                if status == "Completed":
                    completed_files += 1
                    current_time = time.time()
                    progress.update(
                        task, advance=1, speed=completed_files / (current_time - start_time)
                    )
                    if result:
                        register_name, year, data = result
                        if register_name not in summary:
                            summary[register_name] = {}
                        summary[register_name][year or register_name] = data

            time.sleep(0.1)

    console.print(Panel(Text("Processing complete!", style=GREEN), expand=False))
