import inspect


def call_functions():
    stack = inspect.stack()
    calling_frame = stack.pop()
    calling_module = inspect.getmodule(calling_frame[0])
    functions = inspect.getmembers(calling_module, inspect.isfunction)

    for name, func in functions:
        if (
            name == "description"
            or name == "title"
            or name == "hints"
            or name == "group"
        ):
            continue
        try:
            func()
        except Exception as e:
            print(e)
            pass
