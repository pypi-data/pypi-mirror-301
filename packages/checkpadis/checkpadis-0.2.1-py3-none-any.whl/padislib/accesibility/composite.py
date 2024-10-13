from padislib.accessibility.strategy.check_strategy import (
    AccessibilityCheckStrategy,
)


class CompositeAccessibilityCheck(AccessibilityCheckStrategy):
    def __init__(self, strategies):
        self.strategies = strategies

    def run_tests(self, driver):
        all_results = []
        for strategy in self.strategies:
            results = strategy.run_tests(driver)
            if results["violations"]:
                all_results.append((strategy.get_severity(), results))
        return all_results

    def _build_options(self):
        # This method is intentionally left empty as it is meant to be
        # overridden by subclasses
        pass

    def get_severity(self):
        return "Composite"
