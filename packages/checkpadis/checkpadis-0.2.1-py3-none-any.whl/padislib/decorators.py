def base_decorator(api, key, arg):
    if api is None:
        return None

    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            last_item = api.metadata.pop()
            last_item[key] = arg
            api.metadata.append(last_item)

        return wrapper

    return decorator


def group(api=None, text=None):
    return base_decorator(api, "group", text)


def group_description(api=None, text=None):
    return base_decorator(api, "group_description", text)


def title(api=None, text=None):
    return base_decorator(api, "title", text)


def hints(api=None, hints=None):
    return base_decorator(api, "hints", hints)
