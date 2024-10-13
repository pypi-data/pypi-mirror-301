from padislib.accessibility.strategy.check_strategy import (
    AccessibilityCheckStrategy,
)


class HeadingsCheck(AccessibilityCheckStrategy):

    def _build_options(self) -> dict:
        options = {"runOnly": {"type": "rule", "values": ["heading-order"]}}
        return options

    def get_severity(self) -> str:
        return "Moderate"
