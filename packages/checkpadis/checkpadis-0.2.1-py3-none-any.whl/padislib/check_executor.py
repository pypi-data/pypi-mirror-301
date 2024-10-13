import inspect


def get_relevant_functions():
    stack = inspect.stack()
    calling_frame = stack.pop()
    calling_module = inspect.getmodule(calling_frame[0])
    functions = inspect.getmembers(calling_module, inspect.isfunction)

    relevant_functions = [
        (name, func)
        for name, func in functions
        if name not in ["group_description", "title", "hints", "group"]
    ]
    return relevant_functions


def execute_checks(progress_state, relevant_functions):
    total_relevant_functions = len(relevant_functions)

    if total_relevant_functions == 0:
        print("No hay funciones para ejecutar.")
        return

    with progress_state.lock:
        progress_state.update_total_checks(total_relevant_functions)

    for name, func in relevant_functions:
        try:
            func()
            progress_state.increment()
        except Exception as e:
            print(f"Error executing {name}: {e}")
