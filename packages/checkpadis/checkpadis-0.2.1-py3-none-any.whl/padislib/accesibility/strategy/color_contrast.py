from padislib.accessibility.strategy.check_strategy import (
    AccessibilityCheckStrategy,
)

DEFAULT_CONTRAST_LEVEL = "AA"
HIGH_CONTRAST_LEVEL = "AAA"


class ColorContrastCheck(AccessibilityCheckStrategy):
    def __init__(self, contrast_level: str = DEFAULT_CONTRAST_LEVEL):
        self.contrast_level = contrast_level

    def _build_options(self) -> dict:
        options = {"runOnly": {"type": "rule", "values": ["color-contrast"]}}

        if self.contrast_level == HIGH_CONTRAST_LEVEL:
            options["rules"] = {
                "color-contrast": {
                    "options": {"level": HIGH_CONTRAST_LEVEL.lower()},
                }
            }
        return options

    def get_severity(self):
        return "Critical"
