import re
import subprocess
import json

COVERAGE_PATTERN = re.compile(
    r"""
        All\s+files\s*\|\s*
        (\d+(\.\d+)?)\s*\|\s*
        (\d+(\.\d+)?)\s*\|\s*
        (\d+(\.\d+)?)\s*\|\s*
        (\d+(\.\d+)?)\s*\|\s*
        (.*?)
        \s*
    """,
    re.VERBOSE,
)


def get_coverage_from_jest():
    try:
        result = subprocess.run(
            ["npx", "jest", "--coverage"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout
    except Exception as e:
        raise RuntimeError(f"Error running tests: {e.stderr}") from e


def get_total_tests_from_jest():
    try:
        result = subprocess.run(
            ["npx", "jest", "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        output = json.loads(result.stdout)

        return output.get("numTotalTests", 0)
    except Exception as e:
        raise RuntimeError(f"Error running tests: {e.stderr}") from e


def extract_coverage(output):
    """
    Extracts the coverage information from the Jest output.
    Parameters:
    - output (str): The output string from the Jest tests.
    Returns:
    - dict: A dictionary containing the statement,
     branch, function, and line coverage.
    """
    match = COVERAGE_PATTERN.search(output)

    if match:
        numbers = []

        for group in match.groups():
            if group is not None and group[0] != ".":
                numbers.append(float(group))
            if len(numbers) == 4:
                break

        return {
            "statements": numbers[0],
            "branches": numbers[1],
            "functions": numbers[2],
            "lines": numbers[3],
        }
    else:
        raise ValueError("Could not find coverage information in the output.")


def check_jest_coverage(metric, min_coverage):
    """
    Runs the Jest tests and checks if the coverage for a specific metric
    meets the minimum requirement.

    Parameters:
    - metric (str): The coverage metric to check ('statements',
        'branches', 'functions', 'lines').
    - min_coverage (float): The minimum coverage percentage required
        for the specified metric (between 0 and 100).

    Returns:
    - bool: True if the coverage for the specified metric meets or
        exceeds the minimum required coverage, False otherwise.

    Raises:
    - KeyError: If the specified metric is not found in the
        coverage report.
    - ValueError: If the Jest output does not contain
        valid coverage information.
    """
    output = get_coverage_from_jest()
    coverage_dict = extract_coverage(output)
    return coverage_dict[metric] >= min_coverage


def check_jest_tests(min_tests: int) -> bool:
    """
    Checks if the number of Jest tests is
    equal to or greater than a specified value.

    Parameters:
    - min_tests (int): The minimum number of
    tests to check for.

    Returns:
    - bool: True if the number of tests is equal
    or greater than min_tests, False otherwise.
    """
    output = get_total_tests_from_jest()

    return output >= min_tests
