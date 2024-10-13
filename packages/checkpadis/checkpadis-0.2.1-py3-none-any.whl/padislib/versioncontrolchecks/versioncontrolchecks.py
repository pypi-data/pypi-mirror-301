import os
import subprocess
import inspect
import requests
import re

from ..utils.list_processor import remove_asterisk
from ..utils.repository import get_repo_info


def get_merged_branches(target_branch):
    """
    Get a list of branches that have been merged into the target branch.

    Args:
        target_branch (str): The target branch to check against.

    Returns:
        list: A list of branches that have been merged into the target branch.
    """
    result = subprocess.run(
        ["git", "branch", "-a", "--merged", target_branch],
        check=True,
        capture_output=True,
        text=True,
    )
    branches = result.stdout.split("\n")
    cleaned_branches = [branch for branch in branches if branch]
    cleaned_branches = list(map(remove_asterisk, cleaned_branches))
    return cleaned_branches


def is_branch_merged(source_branch, target_branch):
    """
    Check if a branch has been merged into the target branch.

    Args:
        source_branch (str): The name of the branch to check.
        target_branch (str): The target branch to check against.

    Returns:
        str: A message indicating whether the branch has been merged or not.
    Raises:
        BranchMergeCheckError: If an error occurs while checking
        branch merge status.
    """
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_branch, target_branch],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.returncode == 0


def get_commits_on_branch_with_message(branch, message):
    try:
        return subprocess.run(
            ["git", "rev-list", f"--grep={message}", branch],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def check_commit_message(branch, message):
    """
    Check if there is a commit with a specific message.
    Args:
        branch (str): The branch that should have the commit.
        message (str): The message the commit should have
    Returns:
        bool: Returns true if there is a commit on that branch with
        that message.
    Raises:
        subprocess.CalledProcessError: If an error occurs while executing a
        subprocess.
        Exception: If any other error occurs.
    """
    return bool(get_commits_on_branch_with_message(branch, message))


def check_git_command(command):
    """
    Check if a git command was excecuted.
    Args:
        command (str): The git command to check.
    Returns:
        bool: Returns true if the command was excecuted.
    Raises:
        subprocess.CalledProcessError: If an error occurs while executing a
        subprocess.
        Exception: If any other error occurs.
    """
    try:
        git_commands = subprocess.run(
            ["git", "reflog"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        ).stdout.split("\n")

        for git_command in git_commands:
            if command in git_command:
                return True

        return False

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_git_diff():
    try:
        result = subprocess.run(
            ["git", "diff"], capture_output=True, encoding="utf-8", text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")


def get_diff_section(diff_output):
    """Splits the git diff output to get
    the modifications in each class"""
    diffs = re.split(r"(diff --git)", diff_output)
    diffs = [diffs[i] + diffs[i + 1] for i in range(1, len(diffs), 2)]
    return diffs


def get_diff_section_data(diff_section):
    """Splis each section of the git diff
    and returns a list with all the modifications"""
    split_diffs = []
    for diff in diff_section:
        # Split by "@@" and preserve the split marker
        sections = re.split(r"(@@.*?@@)", diff)
        # Recombine the @@ marker with the following section content
        sections = [
            sections[i].strip()
            + "\n"
            + "\n".join(
                line.strip() for line in sections[i + 1].splitlines()
            ).strip()
            for i in range(1, len(sections), 2)
        ]
        split_diffs.append(sections)

    return split_diffs


def get_code_from_diff(sections):
    """It recieves each modification in the
    file and returns the code without the part modified"""
    code_fragments = []

    for section in sections:
        code_lines = []
        inside_method = False

        # Process each line in the section
        for line in section.splitlines():
            stripped_line = line.lstrip()

            # Skip metadata and changes
            if stripped_line.startswith(
                ("diff --git", "index", "---", "+++", "@@", "+", "-")
            ):
                continue

            # Skip class definitions
            if stripped_line.startswith("class "):
                continue

            # Check if the line starts with 'def ',
            # and skip it if it follows a method
            if inside_method and stripped_line.startswith("def "):
                # If this is a new method definition,
                # ignore the remaining lines
                continue

            # Add line to code fragment
            code_lines.append(stripped_line)

            # Set flag if current line starts a new method
            if stripped_line.startswith("def "):
                inside_method = True

        # Join the lines and add to the code fragments list
        code_fragment = "\n".join(code_lines).strip()
        code_fragments.append(code_fragment)

    return code_fragments


def check_func_code(code_fragment, func):
    source_code = inspect.getsource(func)

    # Normalize the code fragment and source code
    normalized_fragment = normalize_code(code_fragment)
    normalized_source = normalize_code(source_code)

    # Check if the normalized code fragment is in the normalized source code
    return contains_substring(normalized_fragment, normalized_source)


def normalize_code(code):
    """Normalize code by removing leading/trailing
    whitespace and standardizing indentation.
    """
    lines = code.splitlines()
    normalized_lines = [line.strip() for line in lines if line.strip()]

    return "\n".join(normalized_lines)


def contains_substring(substring, string):
    """Checks if the substring is contained within the
        string, even if not continuously.

    Parameters:
        substring (str): The string to search for.
        string (str): The string to search within.

    Returns:
        bool: True if all characters of substring
        are found in string in order, False otherwise.
    """
    iter_string = iter(string)
    return all(char in iter_string for char in substring)


def check_function_change(function):
    """
    Checks if a function's name, parameters,
    or implementation has been altered.

    Returns:
        bool: True if the function has changed
        in any way; False otherwise.
    """
    git_diff = get_git_diff()
    if not git_diff:
        return False

    diff_sections = get_diff_section(git_diff)
    section_data = get_diff_section_data(diff_sections)

    # Flatten the list of lists
    flattened_sections = [
        section for sections in section_data for section in sections
    ]

    function_code = get_code_from_diff(flattened_sections)

    return any(
        check_func_code(fragment, function) for fragment in function_code
    )


def verify_commit_in_branch(branch_name, commit_hash):
    """
    Verify if a specific commit exists in a given branch.

    Args:
        branch_name (str): The name of the branch to check.
        commit_hash (str): The hash of the commit to verify.

    Returns:
        bool: True if the commit exists in the branch, False otherwise.
    """
    try:
        commits = (
            subprocess.check_output(
                ["git", "log", branch_name, "--pretty=format:%H"]
            )
            .decode("utf-8")
            .split("\n")
        )
        return commit_hash in commits
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return False


def check_tags_in_commit(commit_hash, tags):
    """
    Check if the given commit hash contains the specified tags.
    Args:
        commit_hash (str): The hash of the commit to check.
        tags: Union[str, List[str]] = (
            str or list
        )
        # The tag(s) to check for. Can be a single tag or a list of tags.
    Returns:
        str: A message indicating the tags found and the tags missing
             in the commit.
    Raises:
        subprocess.CalledProcessError: If an error occurs while executing a "
        "subprocess.
        Exception: If any other error occurs.
    """
    if isinstance(tags, str):
        tags = [tags]
    try:
        tags_found = []
        tags_missing = []

        for tag in tags:
            if _check_tag_in_commit(commit_hash, tag):
                tags_found.append(tag)
            else:
                tags_missing.append(tag)
        return _generate_tag_check_message(
            commit_hash, tags_found, tags_missing
        )
    except subprocess.CalledProcessError as e:
        return e
    except Exception as e:
        return e


def _check_tag_in_commit(commit_hash, tag):
    result = subprocess.run(
        ["git", "tag", "--contains", commit_hash],
        capture_output=True,
        text=True,
        check=True,
    )
    commit_tags = result.stdout.strip().split("\n")
    return tag in commit_tags


def _generate_tag_check_message(commit_hash, tags_found, tags_missing):
    if tags_missing:
        return (
            f"The following tags were not found in commit {commit_hash}: "
            f'{", ".join(tags_missing)}.'
        )

    return (
        f"All tags are present in commit {commit_hash}: "
        f'{", ".join(tags_found)}.'
    )


class BranchNotFoundError(Exception):
    """
    Exception raised when a specified branch does not exist.

    Attributes:
        branch_name (str): The name of the branch that was not found.
    """

    def __init__(self, branch_name):
        self.branch_name = branch_name

    def __str__(self):
        return f"Branch {self.branch_name} does not exist."


class BranchDoesNotHaveCommitsError(Exception):
    """
    Exception raised when a specified branch does not have any new commits.

    Attributes:
        branch_name (str): The name of the branch that does not have new
        commits.
    """

    def __init__(self, branch_name):
        self.branch_name = branch_name

    def __str__(self):
        return f"Branch {self.branch_name} does not have any new commits."


def verify_branch_parent(child_branch_name, parent_branch_name):
    """
    Verify if a branch was created from another branch.

    Args:
        child_branch_name (str): The name of the child branch.
        parent_branch_name (str): The name of the parent branch.

    Returns:
        tuple: A tuple containing a boolean indicating if the child branch
        was created from the parent branch,
               and a message string.
    """
    try:
        branches = (
            subprocess.check_output(["git", "branch"])
            .decode()
            .strip()
            .split("\n")
        )
        branches = [branch.strip("* ").strip() for branch in branches]

        if child_branch_name not in branches:
            raise BranchNotFoundError(child_branch_name)
        if parent_branch_name not in branches:
            raise BranchNotFoundError(parent_branch_name)

        child_commits = (
            subprocess.check_output(["git", "rev-list", child_branch_name])
            .decode()
            .strip()
            .split("\n")
        )

        if not child_commits or (
            len(child_commits) == 1 and child_commits[0] == ""
        ):
            raise BranchDoesNotHaveCommitsError(child_branch_name)

        first_commit_in_child_branch = child_commits[-1]

        merge_base = (
            subprocess.check_output(
                [
                    "git",
                    "merge-base",
                    first_commit_in_child_branch,
                    parent_branch_name,
                ]
            )
            .decode()
            .strip()
        )

        if merge_base == first_commit_in_child_branch:
            return True, (
                f"Branch '{child_branch_name}' was created from '"
                f"{parent_branch_name}'."
            )
        else:
            return False, (
                f"Branch '{child_branch_name}' was NOT "
                f"created from '{parent_branch_name}'."
            )
    except subprocess.SubprocessError as e:
        return e


def check_issue_or_pr_exists(expected_title, expected_body=None, is_pr=False):
    auth_token = os.getenv("GITHUB_TOKEN")

    _, organization, repo_name = get_repo_info()

    url = f"https://api.github.com/repos/{organization}/{repo_name}/issues"

    headers = {
        "Authorization": f"token {auth_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    issues_and_prs = response.json()

    def check_condition(item):
        return (is_pr and "pull_request" in item) or (
            not is_pr and "pull_request" not in item
        )

    filtered_items = [item for item in issues_and_prs if check_condition(item)]

    for item in filtered_items:
        title = item.get("title", "")
        body = item.get("body", "")
        state = item.get("state", "")

        if state != "open":
            continue

        if expected_title.lower() in title.lower() and (
            expected_body.lower() in body.lower() if expected_body else True
        ):
            return True
    return False


def verify_file_content_in_branch(branch_name, file_path, content):
    """
    Verifies if a specific file exists in a given branch.

    Args:
        branch_name (str): The branch where the file is being checked.
        file_path (str): The file path to check within the repository.
        content (str): The content to check within the file.

    Returns:
        bool: True if the file exists in the branch, False if it doesn't
        or if an error occurs.
    """
    try:
        result = subprocess.run(
            ["git", "show", f"{branch_name}:{file_path}"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return False

        return content in result.stdout
    except subprocess.CalledProcessError as e:
        return e


def verify_last_commit_tag_text(branch_name, tag_name):
    """
    Verifies if the last commit in a branch contains a specific tag text.

    Args:
        branch_name (str): The branch where the commit is being checked.
        tag_name (str): The tag text to check within the commit.

    Returns:
        bool: True if the tag text is found in the last commit in the branch,
        False if it isn't or if an error occurs.
    """
    try:
        result = subprocess.run(
            ["git", "show", f"{branch_name}"], capture_output=True, text=True
        )
        last_commit_sha = result.stdout.strip().split("\n")[0].split(" ")[1]

        result = subprocess.run(
            ["git", "tag", "--contains", last_commit_sha],
            capture_output=True,
            text=True,
            check=True,
        )
        tags = result.stdout.strip().split("\n")

        return tag_name in tags
    except Exception as e:
        return e
