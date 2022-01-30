from functools import wraps

from hbutils.reflection import import_object

_DEFAULT_FUNC_NAME = '__spj__'


def _load_func_from_string(string: str):
    splits = string.split(":", maxsplit=1)
    if len(splits) == 1:
        package_name, func_name = splits[0], _DEFAULT_FUNC_NAME
    else:
        package_name, func_name = splits

    return import_object(func_name, package_name)


def _post_check_func(func):
    """
    post process of load function
    :param func: original function
    :return: decorated function
    """

    @wraps(func)
    def _func(data):
        _result_func = func(data)
        if hasattr(_result_func, '__call__'):
            return _result_func
        else:
            raise TypeError(
                'Callable type expected but {actual} found.'.format(actual=repr(type(_result_func).__name__)))

    return _func


@_post_check_func
def _load_func(data):
    """
    load function from any kind of data
    :param data: raw data
    :return: loaded function
    """
    if isinstance(data, str):
        return _load_func_from_string(data)
    else:
        return data
