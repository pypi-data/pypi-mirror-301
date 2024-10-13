from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)

from .constants import TitleHeader


# pragma: no cover
class CheckpadisRunner:
    def __init__(self):
        self.console = Console()

    def display_title(self):
        self.console.print(f"[bold white]{TitleHeader.TITLE.value}[/]")

    def display_progress(self, progress_state):
        self.display_title()

        with Progress(
            SpinnerColumn(),
            BarColumn(
                bar_width=50,
                style="grey23",
                complete_style="bright_green",
                finished_style="bright_cyan",
                pulse_style="bright_yellow",
            ),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(
                "Cargando", total=progress_state.total_checks
            )

            while True:
                with progress_state.lock:
                    completed, total = progress_state.get_progress()
                    progress.update(task, completed=completed)
                    if completed >= total:
                        break

                    progress_state.lock.wait()
