from enum import unique, IntEnum
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


@unique
class ResultType(IntEnum):
    FREE = 0
    SIMPLE = 1
    CONTINUITY = 2

    @classmethod
    def loads(cls, value) -> 'ResultType':
        """
        Load result type from value
        :param value: raw value
        :return: result type object
        """
        if isinstance(value, cls):
            return value
        elif isinstance(value, str):
            if value.upper() in cls.__members__.keys():
                return cls.__members__[value.upper()]
            else:
                raise KeyError('Unknown result type - {actual}.'.format(actual=repr(value)))
        elif isinstance(value, int):
            _mapping = {v.value: v for k, v in cls.__members__.items()}
            if value in _mapping.keys():
                return _mapping[value]
            else:
                raise ValueError('Unknown result type value - {actual}'.format(actual=repr(value)))
        else:
            raise TypeError('Int, str or {cls} expected but {actual} found.'.format(
                cls=cls.__name__,
                actual=repr(type(value).__name__)
            ))


def load_result(data, type_=None) -> SPJResult:
    """
    load result from all kinds of data
    :param data: raw data
    :param type_: result type
    :return: spj result
    """

    def _func():
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

    _result = _func()
    type_ = ResultType.loads(type_ or ResultType.FREE)
    if type_ == ResultType.SIMPLE:
        return to_simple(_result)
    elif type_ == ResultType.CONTINUITY:
        return to_continuity(_result)
    else:
        return _result


def to_simple(data) -> SimpleSPJResult:
    """
    to simple result
    :param data: original data
    :return: simple spj result
    """
    return SimpleSPJResult(**load_result(data).to_json())


def to_continuity(data) -> ContinuitySPJResult:
    """
    to continuity result
    :param data: original data
    :return: continuity spj result
    """
    _dict = dict(load_result(data).to_json())
    if 'score' not in _dict:
        _dict['score'] = 0.0
    return ContinuitySPJResult(**_dict)
