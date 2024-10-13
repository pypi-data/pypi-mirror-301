from padislib.accessibility.strategy.check_strategy import (
    AccessibilityCheckStrategy,
)


class ButtonNameCheck(AccessibilityCheckStrategy):

    def _build_options(self) -> dict:
        options = {"runOnly": {"type": "rule", "values": ["button-name"]}}
        return options

    def get_severity(self) -> str:
        return "Serious"
