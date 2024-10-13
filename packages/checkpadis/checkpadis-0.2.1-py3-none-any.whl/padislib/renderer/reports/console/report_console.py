from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

from padislib.renderer.constants import StatusIcon
from padislib.renderer.reports.report_template import ReportTemplate


class ConsoleReportTemplate(ReportTemplate):
    def __init__(self):
        super().__init__()
        self.console = Console()
        self.console.tab_size = 4

    def output(self, processed_data, file_path):
        for test_group in processed_data:
            self._render_test_group(test_group)
            for test in test_group["tests"]:
                title = test.get("title")
                if test.get("result"):
                    self._render_success_test_row(title)
                else:
                    self._render_failure_test_row(title, test.get("hints"))
        self._render_summary()

    def _render_test_group(self, test_group):
        color = "bright_cyan"
        group_title = (
            f"[bold {color}]{test_group['title'].upper()}[/bold {color}]"
        )
        group_description = test_group["description"] or "Sin descripción"
        self.console.print(f"\n{group_title}\n{group_description}", end="\n")

    def _render_success_test_row(self, title):
        test_content = (
            f"\t[bold green]{StatusIcon.SUCCESS.value} {title}[/bold green]"
        )
        self.console.print(test_content)

    def _render_failure_test_row(self, title, hints):
        test_content = (
            f"\t[bold red]{StatusIcon.FAILURE.value} {title}[/bold red]"
        )
        if hints:
            test_content += "".join(
                [
                    f"\n\t\t[bold yellow]Sugerencia: {hint}[/bold yellow]"
                    for hint in hints
                ]
            )
        self.console.print(test_content)

    def _render_summary(self):
        summary_content = (
            f"[bold white]Total de pruebas:[/bold white] "
            f"{self.total_tests}\n"
            f"[bold green]Pruebas exitosas:[/bold green] "
            f"{self.total_passed_tests}\n"
            f"[bold red]Pruebas fallidas:[/bold red] "
            f"{self.total_failed_tests}"
        )
        summary_panel = Panel(
            Text.from_markup(summary_content),
            title="[bold]Resumen de Pruebas[/bold]",
            border_style="white",
        )
        self.console.print(Padding(summary_panel, (1, 1)))
