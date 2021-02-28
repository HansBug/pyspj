from typing import Optional, Mapping

from .base import SPJResult
from ..utils import get_repr_info, truncate


def _check_score(score: float) -> float:
    score = float(score)
    if score < 0:
        raise ValueError('Score value should be no less than 0 but {actual} found.'.format(actual=repr(score)))
    elif score > 1:
        raise ValueError('Score value should be no greater than 1 but {actual} found.'.format(actual=repr(score)))

    return score


class ContinuitySPJResult(SPJResult):
    def __init__(self, correctness: bool, score: float,
                 message: Optional[str] = None, detail: Optional[str] = None, **kwargs):
        """
        :param correctness: correctness of result
        :param score: score of result
        :param message: message of result
        :param detail: detail of result
        """
        SPJResult.__init__(self, correctness, message, detail, **kwargs)
        self.__score = _check_score(score)

    @property
    def score(self) -> float:
        return self.__score

    def to_json(self) -> Mapping[str, str]:
        _result = dict(SPJResult.to_json(self))
        _result.update(**dict(
            score=self.score,
        ))
        return _result

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('correctness', lambda: repr(self.__correctness)),
                ('score', lambda: '%.3f' % self.__score),
                ('message', lambda: truncate(repr(self.__message), width=64, tail_length=16, show_length=True)),
            ]
        )
