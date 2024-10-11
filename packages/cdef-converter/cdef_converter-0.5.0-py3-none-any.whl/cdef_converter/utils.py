import json
from pathlib import Path
from typing import Any, TypedDict

from rich import box
from rich.table import Table

from cdef_converter.logging_config import log


class SummaryData(TypedDict):
    file_name: str
    num_rows: int
    num_columns: int
    column_names: list[str]


def save_summary(summary: dict[str, Any], output_file: Path) -> None:
    try:
        with output_file.open("w") as f:
            json.dump(summary, f, indent=2)
        log(f"Summary updated in {output_file}")
    except (OSError, json.JSONDecodeError) as e:
        log(f"Error saving summary to {output_file}: {e}")


def create_summary_table(summary: dict[str, Any]) -> Table:
    table = Table(
        title="Processing Summary", show_header=True, header_style="bold magenta", box=box.ROUNDED
    )
    table.add_column("Register", style="cyan", no_wrap=True)
    table.add_column("Year", style="magenta")
    table.add_column("File Name", style="green")
    table.add_column("Rows", justify="right", style="yellow")
    table.add_column("Columns", justify="right", style="yellow")

    for register, years in summary.items():
        total_rows = 0
        total_columns = set()
        for year, data in years.items():
            table.add_row(
                register,
                year,
                data["file_name"],
                f"{data['num_rows']:,}",
                str(data["num_columns"]),
            )
            total_rows += data["num_rows"]
            total_columns.update(data["column_names"])

        # Add total row for each register
        table.add_row(
            f"[bold]{register} Total[/bold]",
            "",
            "",
            f"[bold]{total_rows:,}[/bold]",
            f"[bold]{len(total_columns)}[/bold]",
            style="on dark_green",
        )

    return table


def create_status_table(process_status: dict[str, tuple[str, str]]) -> Table:
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Process", style="cyan", no_wrap=True)
    table.add_column("Current File", style="green")
    table.add_column("Status", style="yellow")

    for process_name, (file_name, status) in process_status.items():
        status_icon = "🟢" if status == "Completed" else "🔵" if status == "Processing" else "🔴"
        table.add_row(process_name, file_name, f"{status_icon} {status}")

    return table
