import os

from selenium import webdriver

from padislib.accessibility.strategy.check_strategy import (
    AccessibilityCheckStrategy,
)


class AccessibilityChecker:
    def __init__(self, strategy: AccessibilityCheckStrategy):
        self.strategy = strategy

    def run(self, html_path):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--allow-file-access-from-files")

        driver = webdriver.Chrome(options=options)

        file_path = f"file://{os.path.abspath(html_path)}"

        driver.get(file_path)

        results = self.strategy.run_tests(driver)
        driver.quit()
        return results
