import http.server
import os
import socketserver
import webbrowser

from jinja2 import Environment, FileSystemLoader

from padislib.renderer.constants import StatusIcon, TitleHeader
from padislib.renderer.reports.report_template import ReportTemplate


class HtmlReportTemplate(ReportTemplate):
    def __init__(self):
        super().__init__()
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("template.html")
        self.current_directory = os.getcwd()

    def output(self, processed_data, file_path):
        html_content = self.template.render(
            title="Informe de Pruebas 📝",
            passed_tests=self.total_passed_tests,
            failed_tests=self.total_failed_tests,
            total_tests=self.total_tests,
            css_content=self._get_css_content(),
            test_groups=processed_data,
            title_ascii=TitleHeader.TITLE.value,
        )

        full_file_path = os.path.join(self.current_directory, file_path)
        self._save_html_report(html_content, full_file_path)
        if "CODESPACES" in os.environ:
            self._serve_html_report()
        else:
            link = f"{full_file_path}"
            print(f"El reporte ha sido generado: {link}")
            input("Presiona Enter para abrir el reporte en tu navegador...")

            webbrowser.open(link)

    def _get_css_content(self):
        css_path = os.path.join(
            os.path.dirname(__file__), "./templates/style.css"
        )
        with open(css_path, "r") as css_file:
            return css_file.read()

    def _serve_html_report(self):
        port = 8000
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(
                f"Sirviendo en el puerto {port}, abre el navegador en el enlace correspondiente de Codespaces"
            )
            httpd.serve_forever()

    def _save_html_report(self, html_content, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

    def process_group(self, test_group):
        processed_group = super().process_group(test_group)
        processed_group["id"] = test_group["title"].replace(" ", "-")
        processed_group["emoji"] = (
            StatusIcon.SUCCESS.value
            if self.get_group_failed_tests_count(test_group["title"]) == 0
            else StatusIcon.FAILURE.value
        )
        return processed_group
