from padislib.accessibility.web_driver_runner import WebDriverRunner
from padislib.accessibility.parsers.parse_report import generate_clean_report
from padislib.accessibility.strategy import (
    ButtonNameCheck,
    ColorContrastCheck,
    CompositeAccessibilityCheck,
    HeadingsCheck,
    ImageAltCheck,
)
from padislib.accessibility.strategy.form_label import FormLabelCheck


class AccessibilityRunner:
    def __init__(self):
        self._strategies = []

    def verify_color_contrast_check(self, contrast_level="AA"):
        """
        Adds a color contrast check strategy to the list of strategies.
        This method appends a `ColorContrastCheck` strategy to the
        `_strategies` list with the specified contrast level.

        Args:
            contrast_level (str):
            The level of contrast to check for.
            Defaults to "AA". Possible values are "AA" and "AAA".
        """
        self._strategies.append(
            ColorContrastCheck(contrast_level=contrast_level)
        )

    def verify_image_alt_check(self, enforce_descriptive=False):
        """
        Adds an ImageAltCheck strategy to the list of strategies.
        This method appends an ImageAltCheck strategy to the internal list of
        strategies. The ImageAltCheck strategy is used to verify the presence
        and descriptiveness of alt attributes in images.

        Args:
            enforce_descriptive (bool, optional):
            If True, the check will enforce
            that alt attributes are descriptive. Defaults to False.
        """
        self._strategies.append(
            ImageAltCheck(enforce_descriptive=enforce_descriptive)
        )

    def verify_form_labels_check(self):
        """
        Adds a FormLabelsCheck strategy to the list of strategies.
        This method appends a FormLabelsCheck strategy to the internal list of
        strategies. The FormLabelsCheck strategy is used to verify that form
        elements have associated labels.
        """
        self._strategies.append(FormLabelCheck())

    def verify_headings_check(self):
        """
        Adds a HeadingsCheck strategy to the list of strategies.
        This method appends a HeadingsCheck strategy to the internal list of
        strategies. The HeadingsCheck strategy is used to verify that headings
        are used correctly in the HTML document.
        """
        self._strategies.append(HeadingsCheck())

    def verify_button_name_check(self):
        """
        Adds a ButtonNameCheck strategy to the list of strategies.
        This method appends a ButtonNameCheck strategy to the internal list of
        strategies. The ButtonNameCheck strategy is used to verify that buttons
        have accessible names.
        """
        self._strategies.append(ButtonNameCheck())

    def run_checks(self, html_path, detailed_report=False):
        composite_check = CompositeAccessibilityCheck(self._strategies)
        checker = WebDriverRunner(composite_check)
        results = checker.run(html_path)

        if detailed_report:
            parsed_report = generate_clean_report(results)
            return parsed_report
        else:
            return not any(results)
