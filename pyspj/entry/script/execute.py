import io
import sys
import traceback
from functools import wraps

from .decorator import string_support, file_trans
from .imports import _load_func
from ...models import load_result, SPJResult


def _basic_process(spj):
    """
    process spj to be safe
    :param spj: original function
    :return: processed special judge
    """
    spj = _load_func(spj)

    @wraps(spj)
    def _func(*args, **kwargs):
        try:
            return spj(*args, **kwargs)
        except Exception as err:
            with io.StringIO() as eis:
                traceback.print_exception(*sys.exc_info(), file=eis)
                err_info = eis.getvalue()

            return False, 'Exception occurred while special judge - {cls}.'.format(cls=repr(err)), err_info

    return _func


def execute_spj(spj, stdin, stdout, type_=None) -> SPJResult:
    """
    execute special judge
    :param spj: special judge function
    :param stdin: stdin stream
    :param stdout: stdout stream
    :param type_: load type
    :return: special judge result
    """
    return load_result(_basic_process(spj)(stdin=stdin, stdout=stdout), type_)


def execute_spj_from_string(spj, stdin, stdout, type_=None) -> SPJResult:
    """
    execute special judge with string value
    :param spj: special judge function
    :param stdin: stdin string
    :param stdout: stdout string
    :param type_: load type
    :return: special judge result
    """
    return execute_spj(string_support(_basic_process(spj)), stdin, stdout, type_)


def execute_spj_from_file(spj, stdin_file, stdout_file, type_=None) -> SPJResult:
    """
    execute special judge with string file
    :param spj: special judge function
    :param stdin_file: stdin filename
    :param stdout_file: stdout filename
    :param type_: load type
    :return: special judge result
    """
    return execute_spj(file_trans(_basic_process(spj)), stdin_file, stdout_file, type_)
