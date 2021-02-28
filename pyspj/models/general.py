from typing import Tuple, Optional

from .base import SPJResult
from .continuity import ContinuitySPJResult
from .simple import SimpleSPJResult


def _load_from_values(correctness, score, message, detail) -> SPJResult:
    if score is None:
        return SimpleSPJResult(correctness, message, detail)
    else:
        return ContinuitySPJResult(correctness, score, message, detail)


def _load_result_from_dict(data: dict) -> SPJResult:
    _correctness = data['correctness']
    _score = data.get('score', None)
    _message = data.get('message', None)
    _detail = data.get('detail', None)

    return _load_from_values(_correctness, _score, _message, _detail)


def _load_core_result_from_tuple(head) -> Tuple[bool, Optional[float]]:
    if isinstance(head, (list, tuple)):
        _correctness, _score = tuple(head)
    else:
        _correctness, _score = head, None

    return _correctness, _score


def _load_result_from_tuple(data: tuple) -> SPJResult:
    if not data:
        raise ValueError(
            'Tuple result should has no less than 1 object but {actual} found.'.format(actual=repr(len(data))))
    elif len(data) == 1:
        _core, _message, _detail = data[0], None, None
    elif len(data) == 2:
        (_core, _message), _detail = data, None
    elif len(data) == 3:
        _core, _message, _detail = data
    else:
        raise ValueError(
            'Tuple result should has no more than 3 object but {actual} found.'.format(actual=repr(len(data))))

    _correctness, _score = _load_core_result_from_tuple(_core)
    return _load_from_values(_correctness, _score, _message, _detail)


def load_result(data) -> SPJResult:
    """
    load result from all kinds of data
    :param data: raw data
    :return: spj result
    """
    if isinstance(data, SimpleSPJResult):
        return data
    elif isinstance(data, ContinuitySPJResult):
        return data
    elif isinstance(data, dict):
        return _load_result_from_dict(data)
    elif isinstance(data, (list, tuple)):
        return _load_result_from_tuple(tuple(data))
    else:
        return SimpleSPJResult(not not data)
