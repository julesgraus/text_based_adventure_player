import inspect

def value(to_resolve) -> int | float | str | bool | dict | set | tuple | object:

    if inspect.isfunction(to_resolve):
        return to_resolve()
    else:
        return to_resolve
