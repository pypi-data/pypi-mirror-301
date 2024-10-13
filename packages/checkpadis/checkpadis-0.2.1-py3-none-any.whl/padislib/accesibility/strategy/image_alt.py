from padislib.accessibility.strategy.check_strategy import (
    AccessibilityCheckStrategy,
)

DEFAULT_ENFORCE_DESCRIPTIVE = False
RULE_NAME = "image-alt"


class ImageAltCheck(AccessibilityCheckStrategy):
    def __init__(
        self, enforce_descriptive: bool = DEFAULT_ENFORCE_DESCRIPTIVE
    ):
        self.enforce_descriptive = enforce_descriptive

    def _build_options(self) -> dict:
        options = {"runOnly": {"type": "rule", "values": [RULE_NAME]}}

        if self.enforce_descriptive:
            options["rules"] = {"image-alt": {"enabled": "true"}}
        return options

    def get_severity(self) -> str:
        return "Warning" if self.enforce_descriptive else "Info"
