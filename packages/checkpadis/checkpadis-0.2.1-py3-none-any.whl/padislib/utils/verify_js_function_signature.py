import re
from py_mini_racer import py_mini_racer


def verify_js_function_signature(
        js_code,
        expected_function_name,
        expected_params):

    function_regex = r"function\s+(\w+)\s*\((.*?)\)"
    matches = re.findall(function_regex, js_code)

    if not matches:
        raise AssertionError("No functions found in the JS code")

    for function_name, params_str in matches:
        params = params_str.replace(" ", "").split(",") if params_str else []

        if function_name == expected_function_name:
            if len(params) != len(expected_params):
                raise AssertionError(
                    f"The JS function '{function_name}' "
                    f"has {len(params)} parameters, "
                    f"but {len(expected_params)} were expected"
                )
            if params != expected_params:
                raise AssertionError(
                    f"The expected parameters do not match. "
                    f"Expected {expected_params} but found {params}"
                )

            try:
                ctx = py_mini_racer.MiniRacer()
                ctx.eval(js_code)
            except Exception as e:
                raise Exception(f"Error while executing the JS code: {str(e)}")

            return True

    raise AssertionError(
        f"No function with the name '{expected_function_name}' and "
        f"parameters {expected_params} found"
    )
