import os

from jinja2 import Environment, FileSystemLoader

from padislib.renderer.constants import TitleHeader
from padislib.renderer.reports.render_strategy import ReportTemplate


class HtmlReportTemplate(ReportTemplate):
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template('template.html')
        self.current_directory = os.getcwd()

    def render(self, data, file_path):
        passed_tests, failed_tests = 0, 0
        test_groups = []
        html_output_path = os.path.join(self.current_directory, file_path)

        for test_group in data["test"]:
            group_data, group_passed, group_failed = self._process_test_group(
                test_group)
            test_groups.append(group_data)
            passed_tests += group_passed
            failed_tests += group_failed

        css_path = os.path.join(os.path.dirname(
            __file__), "./templates/style.css")
        with open(css_path, "r") as css_file:
            css_content = css_file.read()

        total_tests = passed_tests + failed_tests

        html_content = self.template.render(
            title="Informe de Pruebas 📝",
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            total_tests=total_tests,
            css_content=css_content,
            test_groups=test_groups,
            title_ascii=TitleHeader.TITLE._value_
        )

        self._save_html_report(html_content, html_output_path)

    def _process_test_group(self, test_group):
        group_result_class = "failed" if any(
            t["result"] == 0 for t in test_group["test"]) else "passed"
        emoji = "✅" if group_result_class == "passed" else "❌"
        group_id = test_group['title'].replace(' ', '-')
        group_tests = []

        passed_tests, failed_tests = 0, 0

        for test in test_group["test"]:
            test_data = self._process_individual_test(test)
            group_tests.append(test_data)
            passed_tests += 1 if test["result"] == 1 else 0
            failed_tests += 1 if test["result"] == 0 else 0

        group_data = {
            "id": group_id,
            "emoji": emoji,
            "title": test_group['title'],
            "description": test_group['description'],
            "tests": group_tests
        }

        return group_data, passed_tests, failed_tests

    def _process_individual_test(self, test):
        hints = test.get("hints", []) if test["result"] == 0 else []
        return {
            "title": test["title"],
            "hints": hints,
            "result": test["result"]
        }

    def _save_html_report(self, html_content, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
