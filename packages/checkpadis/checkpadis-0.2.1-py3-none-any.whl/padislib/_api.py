from padislib.check_executor import execute_checks, get_relevant_functions
from padislib.enums.render_types import RenderTypes
from padislib.htmlchecks import (
    find_label_in_html,
    has_specific_html5_tag_with_args,
)
from padislib.jestchecks import check_jest_coverage, check_jest_tests
from padislib.jschecks import run_javascript_code
from padislib.plaintextchecks import check_file_content
from padislib.progress_manager import ProgressManager
from padislib.versioncontrolchecks import (
    check_issue_or_pr_exists,
    is_branch_merged,
    verify_branch_parent,
    verify_file_content_in_branch,
    verify_last_commit_tag_text,
)


class padisapi:
    metadata = []
    progress_manager = None

    def __init__(self):
        self.progress_manager = ProgressManager()

    def wrapper(self, func, *args, **kwargs):
        result = 0
        try:
            result = func(*args, **kwargs)
        except Exception:
            result = 0
        self.metadata.append({"result": 1 if result else 0})

    def check_file_content(self, file, content):
        self.wrapper(check_file_content, file, content)

    def is_branch_merged(self, branch_name, target_branch):
        self.wrapper(is_branch_merged, branch_name, target_branch)

    def check_issue_exists(self, title, body=None):
        self.wrapper(check_issue_or_pr_exists, title, body)

    def check_pr_exists(self, title, body=None):
        self.wrapper(check_issue_or_pr_exists, title, body, True)

    def verify_file_content_in_branch(self, branch, file, content):
        self.wrapper(verify_file_content_in_branch, branch, file, content)

    def verify_last_commit_tag_text(self, branch, tag):
        self.wrapper(verify_last_commit_tag_text, branch, tag)

    def verify_branch_parent(self, branch, parent_branch):
        self.wrapper(verify_branch_parent, branch, parent_branch)

    def check_jest_coverage(self, metric, min_coverage):
        self.wrapper(check_jest_coverage, metric, min_coverage)

    def check_jest_tests(self, min_tests):
        self.wrapper(check_jest_tests, min_tests)

    def find_label_in_html(self, route, label_id):
        self.wrapper(find_label_in_html, route, label_id)

    def has_specific_html5_tag_with_args(self, route, tag, args):
        self.wrapper(has_specific_html5_tag_with_args, route, tag, args)

    def run_javascript_code(self, file_path, expresion, result):
        self.wrapper(run_javascript_code, file_path, expresion, result)

    def parse_metadata(self):
        parsed_data = {"test": []}
        for item in self.metadata:
            item["group"] = item.get("group") or "General"
            item["title"] = item.get("title") or ""
            item["group_description"] = item.get("group_description") or ""

            saved_tests = parsed_data["test"]
            indexes = [
                index
                for index, obj in enumerate(saved_tests)
                if obj.get("title") == item.get("group")
            ]
            saved_index = indexes[0] if indexes else None

            if saved_index is None:
                saved_tests.append(
                    {
                        "title": item.get("group"),
                        "description": item.get("group_description"),
                        "test": [item],
                    }
                )
            else:
                saved_tests[saved_index]["test"].append(item)
        return parsed_data

    def end(self):
        try:
            relevant_functions = get_relevant_functions()

            self.progress_manager.start_progress()

            execute_checks(
                self.progress_manager.progress_state, relevant_functions
            )

            self.progress_manager.stop_progress()

            metadata = self.parse_metadata()
            RenderTypes.CONSOLE.get_strategy().render(metadata)
            RenderTypes.HTML.get_strategy().render(metadata, "output.html")

        except Exception as e:
            print(e)
