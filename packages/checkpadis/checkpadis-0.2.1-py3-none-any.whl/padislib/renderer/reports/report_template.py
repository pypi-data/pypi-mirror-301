from abc import ABC, abstractmethod


class ReportTemplate(ABC):
    def __init__(self):
        self.total_passed_tests = 0
        self.total_failed_tests = 0
        self.total_tests = 0
        self.statistics_per_test_group_dict = {}

    def render(self, data, file_path=None):
        self.count_tests(data)
        processed_data = self.process_data(data)
        self.output(processed_data, file_path)

    def count_tests(self, data):
        for test_group in data["test"]:
            group_test_passed = 0
            group_test_failed = 0
            for test in test_group["test"]:
                group_test_passed += 1 if test["result"] == 1 else 0
                group_test_failed += 1 if test["result"] == 0 else 0
            self.statistics_per_test_group_dict[test_group["title"]] = (
                group_test_passed,
                group_test_failed,
            )
            self.total_passed_tests += group_test_passed
            self.total_failed_tests += group_test_failed
        self.total_tests = self.total_failed_tests + self.total_passed_tests

    def get_group_failed_tests_count(self, group_title):
        return self.statistics_per_test_group_dict.get(group_title, (0, 0))[1]

    def get_group_passed_tests_count(self, group_title):
        return self.statistics_per_test_group_dict.get(group_title, (0, 0))[0]

    def process_data(self, data):
        processed = []
        for group in data["test"]:
            processed.append(self.process_group(group))
        return processed

    def process_group(self, group):
        return {
            "title": group["title"],
            "description": group["description"],
            "tests": [
                self.process_individual_test(test) for test in group["test"]
            ],
        }

    def process_individual_test(self, test):
        hints = test.get("hints", []) if test["result"] == 0 else []
        return {
            "title": test["title"],
            "result": test["result"],
            "hints": hints,
        }

    @abstractmethod
    def output(self, processed_data, file_path):
        pass
