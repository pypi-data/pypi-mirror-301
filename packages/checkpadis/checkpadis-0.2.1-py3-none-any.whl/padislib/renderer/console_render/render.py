import time

from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.text import Text

from padislib.renderer.constants import StatusIcon, TitleHeader
from padislib.renderer.reports.render_strategy import ReportTemplate


class ConsoleReportTemplate(ReportTemplate):
    def __init__(self):
        self.console = Console()

    def render(self, data, file_path=None):
        self._render_loading_animation()
        self.console.print(Padding(TitleHeader.TITLE._value_, (0, 0, 1, 0)))

        passed_tests, failed_tests = 0, 0

        for test_group in data["test"]:
            self._render_test_group(test_group)

            for test in test_group["test"]:
                passed_tests += 1 if test["result"] == 1 else 0
                failed_tests += 1 if test["result"] == 0 else 0

                self._render_test_row(
                    test["title"],
                    test["result"],
                    test.get("hints"),
                )

        self._render_summary(passed_tests, failed_tests)

    def _render_loading_animation(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Cargando...[/]"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("Cargando", total=100)
            while not progress.finished:
                progress.update(task, advance=5)
                time.sleep(0.1)

        self.console.print(
            "\n[bold green]¡Pruebas iniciadas![/]", style="bold green")

    def _render_test_group(self, test_group):
        group_title = f"[bold bright_cyan]{
            test_group['title'].upper()}[/bold bright_cyan]"
        group_description = test_group["description"]
        self.console.print(f"\n{group_title}\n{group_description}", end="\n\n")

    def _render_test_row(self, title, result, hints):
        test_content = ""

        if result == 1:
            test_content += f"\t[bold green]{
                StatusIcon.SUCCESS.value} {title}[/bold green]"
        else:
            test_content += f"\t[bold red]{
                StatusIcon.FAILURE.value} {title}[/bold red]"

            if hints:
                for hint in hints:
                    test_content += f"\n\t\t[bold yellow]Sugerencia: {
                        hint}[/bold yellow]"

        self.console.print(test_content)

    def _render_summary(self, passed, failed):
        total = passed + failed
        summary_content = (
            f"[bold white]Total de pruebas:[/bold white] {total}\n"
            f"[bold green]Pruebas exitosas:[/bold green] {passed}\n"
            f"[bold red]Pruebas fallidas:[/bold red] {failed}\n"
        )
        summary_panel = Panel(
            Text.from_markup(summary_content),
            title="[bold]Resumen de Pruebas[/bold]",
            border_style="white",
            padding=(1, 1),
        )

        self.console.print(Padding(summary_panel, (1, 1)))
