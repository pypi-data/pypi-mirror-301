import re
from tree_sitter import Parser
import subprocess
from py_mini_racer import MiniRacer

from padislib.jschecks.ast_nodes import FieldNames, NodeType
from padislib.jschecks.grammar import JSGrammar


def _get_js_language():
    js_language_singleton = JSGrammar()
    return js_language_singleton.get_language()


def _parse_js_code(js_code):
    js_language = _get_js_language()
    parser = Parser(js_language)
    tree = parser.parse(bytes(js_code, "utf-8"))
    return tree.root_node


def check_private_attribute(js_code, class_name, private_attribute):
    """
    Checks if a specific private attribute exists in a JavaScript class.

    Args:
        js_code (str): The JavaScript code to analyze.
        class_name (str): The name of the class to search in.
        private_attribute (str): The private attribute (e.g., '#age') to check
                                 for.

    Returns:
        bool: True if the private attribute is found, False otherwise.
    """

    root_node = _parse_js_code(js_code)

    class_node = _find_class_node(root_node, class_name)
    if not class_node:
        return False

    return _is_private_field_in_class(class_node, private_attribute)


def check_public_attribute(js_code, class_name, public_attribute):
    """
    Checks if a specific public attribute exists in a JavaScript class.

    Args:
        js_code (str): The JavaScript code to analyze.
        class_name (str): The name of the class to search in.
        public_attribute (str): The public attribute (e.g., 'name') to check
                                for.

    Returns:
        bool: True if the public attribute is found, False otherwise.
    """
    root_node = _parse_js_code(js_code)

    class_node = _find_class_node(root_node, class_name)
    if not class_node:
        return False

    return _is_public_field_in_class(class_node, public_attribute)


def check_static_attribute(js_code, class_name, static_attribute):
    """
    Checks if a specific static attribute exists in a JavaScript class.

    Args:
        js_code (str): The JavaScript code to analyze.
        class_name (str): The name of the class to search in.
        static_attribute (str): The static attribute (e.g., 'company') to
                                check for.

    Returns:
        bool: True if the static attribute is found, False otherwise.
    """
    root_node = _parse_js_code(js_code)

    class_node = _find_class_node(root_node, class_name)
    if not class_node:
        return False

    return _is_static_field_in_class(class_node, static_attribute)


def check_class_attribute(js_code, class_name, attribute):
    """
    Checks if a specific attribute (private, public, or static) exists in a
    JavaScript class.

    Args:
        js_code (str): The JavaScript code to analyze.
        class_name (str): The name of the class to search in.
        attribute (str): The attribute to check for.

    Returns:
        bool: True if the attribute (private, public, or static) is found,
              False otherwise.
    """
    root_node = _parse_js_code(js_code)

    class_node = _find_class_node(root_node, class_name)
    if not class_node:
        return False

    return (
        _is_private_field_in_class(class_node, attribute)
        or _is_public_field_in_class(class_node, attribute)
        or _is_static_field_in_class(class_node, attribute)
    )


def _find_class_node(root_node, class_name):
    return next(
        (
            child.child_by_field_name(FieldNames.BODY.value)
            for child in root_node.children
            if child.type == NodeType.CLASS_DECLARATION.value
            and child.child_by_field_name(FieldNames.NAME.value)
            and child.child_by_field_name(FieldNames.NAME.value).text.decode(
                "utf-8"
            )
            == class_name
        ),
        None,
    )


def _is_private_field_in_class(class_body, private_attribute):
    return any(
        child.type == NodeType.FIELD_DEFINITION.value
        and child.child_by_field_name(FieldNames.PROPERTY.value)
        and child.child_by_field_name(FieldNames.PROPERTY.value).text.decode(
            "utf-8"
        )
        == f"#{private_attribute}"
        for child in class_body.children
    )


def _is_public_field_in_class(class_body, public_attribute):
    return any(
        child.type == NodeType.FIELD_DEFINITION.value
        and child.child_by_field_name(FieldNames.PROPERTY.value)
        and child.child_by_field_name(FieldNames.PROPERTY.value).text.decode(
            "utf-8"
        )
        == public_attribute
        for child in class_body.children
    )


def _is_static_field_in_class(class_body, static_attribute):
    return any(
        child.type == NodeType.FIELD_DEFINITION.value
        and child.child_by_field_name(FieldNames.PROPERTY.value)
        and child.child_by_field_name(FieldNames.PROPERTY.value).text.decode(
            "utf-8"
        )
        == static_attribute
        for child in class_body.children
    )


def find_functions(node, functions):
    if node.type == NodeType.FUNCTION_DECLARATION.value:
        function_name_node = node.child_by_field_name(FieldNames.NAME.value)
        function_name = (
            function_name_node.text.decode("utf8")
            if function_name_node
            else None
        )

        params_node = node.child_by_field_name(FieldNames.PARAMETERS.value)
        params = []

        if params_node and params_node.type == (
            FieldNames.FORMAL_PARAMETERS.value
        ):
            params = [
                param.text.decode("utf8").strip()
                for param in params_node.children
                if param.type == NodeType.IDENTIFIER.value
            ]

        if function_name:
            functions.append((function_name, params))

    for child in node.children:
        find_functions(child, functions)


def get_function_signature(root_node):
    functions = []

    find_functions(root_node, functions)
    return functions


def check_js_function_signature(
    js_code, expected_function_name, expected_params
):
    """
    Checks if a function with a specific name and parameters exists in the
    provided JavaScript code.

    Args:
        js_code (str): The JavaScript code containing the function to check.
        expected_function_name (str): The name of the function expected to be
        found.
        expected_params (list of str): A list of parameter names that the
        function
            should have to be considered a match.

    Returns:
        bool: Returns True if a function with the expected name and parameters
        is found. Returns False if no match is found.
    """
    root_node = _parse_js_code(js_code)
    functions = get_function_signature(root_node)
    return any(
        function_name == expected_function_name and params == expected_params
        for function_name, params in functions
    )


def get_source_code(route):
    try:
        with open(route, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise RuntimeError(f"Error: File not found at {route}")


def normalize_code(code):
    """
    Normalize code by removing leading/trailing
    whitespace and standardizing indentation.
    """
    lines = code.splitlines()
    normalized_lines = [line.strip() for line in lines if line.strip()]

    return "\n".join(normalized_lines)


def get_code_from_file(route):
    """
    Returns a string containing
    the source code of a file in a
    specific route.
    Parameters:
        route (str): The route of the file.

    Returns:
        string: The source code of the
        file
    """
    code = get_source_code(route)
    return normalize_code(code)


def run_npm_lint():
    try:
        result = subprocess.run(
            ["npm", "run", "lint"], check=True, capture_output=True, text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error running tests: {e.stderr}") from e


def has_lint_problems(output):
    lines = output.strip().split("\n")

    for line in lines:
        if line.strip().startswith("✖"):
            return True
    if "eslint" in output and len(lines) <= 3:
        return False


def check_has_lint_errors():
    npm_run_lint_output = run_npm_lint()
    return has_lint_problems(npm_run_lint_output)


def run_javascript_code(file_path, exp, result):
    """
    Executes JavaScript code from a specified file and evaluates an expression
    against an expected result.

    This function reads the contents of a JavaScript file located at
    `file_path`,
    compiles and executes the code using the MiniRacer engine, and evaluates
    the
    provided JavaScript expression `exp`. It then compares the evaluated
    result
    to the expected `result`.

    Parameters:
    - file_path (str): The path to the JavaScript file to be executed.
    - exp (str): The JavaScript expression to evaluate after executing the
    file.
    - result: The expected result of the evaluated expression.

    Returns:
        bool: True if the evaluated expression matches the expected result,
        False otherwise.
    """
    with open(file_path, "r") as file:
        content = file.read()

    content = re.sub(r"export\s+default\s+.*?;\s*", "", content)

    ctx = MiniRacer()
    ctx.eval(content)

    return ctx.eval(exp) == result
