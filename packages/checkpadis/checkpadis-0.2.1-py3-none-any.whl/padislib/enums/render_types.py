from enum import Enum


class RenderTypes(Enum):
    HTML = "HTML"
    CONSOLE = "CONSOLE"

    def get_strategy(self):
        match self:
            case RenderTypes.HTML:
                from padislib.renderer.reports.html.report_html import (
                    HtmlReportTemplate,
                )

                return HtmlReportTemplate()
            case RenderTypes.CONSOLE:
                from padislib.renderer.reports.console.report_console import (
                    ConsoleReportTemplate,
                )

                return ConsoleReportTemplate()
