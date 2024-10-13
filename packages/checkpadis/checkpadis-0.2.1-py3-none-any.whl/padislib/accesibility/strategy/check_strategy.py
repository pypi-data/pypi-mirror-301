from abc import ABC, abstractmethod

from axe_selenium_python import Axe


class AccessibilityCheckStrategy(ABC):
    @abstractmethod
    def _build_options(self) -> dict:
        pass

    @abstractmethod
    def get_severity(self) -> str:
        pass

    def run_tests(self, driver) -> dict:
        """
        Executes accessibility tests using the Axe tool.
        Args:
            driver: The WebDriver instance used to interact with the web page.
        Returns:
            dict: A dictionary containing the results of the accessibility
            tests.
        """
        axe = Axe(driver)
        axe.inject()
        options = self._build_options()
        return axe.run(options)
