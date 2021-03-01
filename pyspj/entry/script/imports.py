import importlib

_DEFAULT_FUNC_NAME = '__spj__'


def _load_func_from_package(package_name: str, func_name: str):
    module = importlib.import_module(package_name)
    if hasattr(module, func_name):
        _func = getattr(module, func_name)
        if hasattr(_func, '__call__'):
            return _func
        else:
            raise TypeError('Callable type expected but {actual} found.'.format(actual=repr(type(_func).__name__)))
    else:
        raise AttributeError('Module {module} does not contain the function {func}.'.format(
            module=repr(module.__name__), func=repr(func_name)))


def _load_func_from_string(string: str):
    splits = string.split(":", maxsplit=2)
    if len(splits) == 0:
        raise ValueError('Invalid package - {string}.'.format(string=repr(string)))
    elif len(splits) == 1:
        package_name, func_name = splits[0], _DEFAULT_FUNC_NAME
    else:
        package_name, func_name = splits

    return _load_func_from_package(package_name, func_name)


def _load_func_from_func(func):
    return func


def _load_func(data):
    """
    load function from any kind of data
    :param data: raw data
    :return: loaded function
    """
    if hasattr(data, '__call__'):
        return _load_func_from_func(data)
    elif isinstance(data, str):
        return _load_func_from_string(data)
    else:
        raise TypeError('Callable or string object expected but {actual} found.'.format(
            actual=repr(type(data).__name__)))
