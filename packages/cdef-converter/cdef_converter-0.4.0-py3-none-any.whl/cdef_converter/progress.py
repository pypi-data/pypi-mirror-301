import time
from queue import Queue
from typing import Any

from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.text import Text

from cdef_converter.config import GREEN
from cdef_converter.utils import create_status_table, create_summary_table

console = Console()


def display_progress(progress_queue: Queue[Any], total_files: int, summary: dict[str, Any]) -> None:
    completed_files = 0
    process_status: dict[str, tuple[str, str]] = {}
    start_time = time.time()
    latest_log = ""

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

        status_table = create_status_table(process_status)
        summary_table = create_summary_table(summary)

        layout = Layout()
        layout.split_row(Layout(status_table, name="status"), Layout(summary_table, name="summary"))
        layout.split_column(Layout(layout, name="tables"), Layout(name="progress_and_log"))

        with Live(layout, refresh_per_second=4) as live:
            while completed_files < total_files:
                current_time = time.time()
                while not progress_queue.empty():
                    item = progress_queue.get()
                    if item is None:  # Termination signal
                        return
                    process_name, file_name, status, result, log_message = item
                    process_status[process_name] = (file_name, status)
                    if status == "Completed":
                        completed_files += 1
                        progress.update(
                            task, advance=1, speed=completed_files / (current_time - start_time)
                        )
                        if result:
                            register_name, year, data = result
                            if register_name not in summary:
                                summary[register_name] = {}
                            summary[register_name][year or register_name] = data
                            layout["tables"]["summary"].update(create_summary_table(summary))

                    latest_log = log_message

                layout["tables"]["status"].update(create_status_table(process_status))
                layout["progress_and_log"].update(
                    Group(progress, Panel(latest_log, title="Latest Log", border_style="blue"))
                )
                live.refresh()

                time.sleep(0.1)

    console.print(Panel(Text("Processing complete!", style=GREEN), expand=False))
