from padislib.accessibility.strategy.check_strategy import (
    AccessibilityCheckStrategy,
)


class FormLabelCheck(AccessibilityCheckStrategy):

    def _build_options(self) -> dict:
        options = {"runOnly": {"type": "rule", "values": ["label"]}}
        return options

    def get_severity(self) -> str:
        return "Critical"
