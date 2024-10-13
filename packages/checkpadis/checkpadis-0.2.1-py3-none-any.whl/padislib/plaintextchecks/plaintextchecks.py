import re


def check_file_content(file_path, regex):
    """
    Check if a file contains a pattern specified by a regular
    expression.

    Args:
        file_path (str): The path to the file to be checked.
        regex (str): The regular expression pattern to search for in the file.

    Returns:
        bool: True if the pattern is found in the file, False otherwise.
    """
    with open(file_path, "r") as file:
        content = file.read()
        return bool(re.search(regex, content))
