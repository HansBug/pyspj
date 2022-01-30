import warnings
from abc import ABCMeta
from typing import Optional, Mapping

from hbutils.string import truncate

from ..utils import get_repr_info

_DEFAULT_SUCCESS_MESSAGE = 'Congratulations, test passed!'
_DEFAULT_FAILURE_MESSAGE = 'Sorry, test failed!'


def _check_message(message: str) -> str:
    message = message.strip()
    _message_lines = message.splitlines()
    if len(_message_lines) > 1:
        warnings.warn('Message contains {n} lines, '
                      'we strongly recommend you to simplify the '
                      'message into exactly 1 line to keep its briefness.'.format(n=repr(len(_message_lines))))

    return message


class SPJResult(metaclass=ABCMeta):
    def __init__(self, correctness: bool,
                 message: Optional[str] = None, detail: Optional[str] = None, **kwargs):
        """
        :param correctness: correctness of result
        :param message: message of result
        :param detail: detail of result
        """
        self.__correctness = not not correctness
        self.__message = _check_message(
            message or (_DEFAULT_SUCCESS_MESSAGE if self.__correctness else _DEFAULT_FAILURE_MESSAGE))
        self.__detail = (detail or self.__message).rstrip()

    @property
    def correctness(self) -> bool:
        return self.__correctness

    @property
    def message(self) -> str:
        return self.__message

    @property
    def detail(self) -> str:
        return self.__detail

    def to_json(self) -> Mapping[str, str]:
        return dict(
            correctness=self.correctness,
            message=self.message,
            detail=self.detail,
        )

    def __repr__(self):
        return get_repr_info(
            cls=self.__class__,
            args=[
                ('correctness', lambda: repr(self.correctness)),
                ('message', lambda: truncate(repr(self.message), width=64, tail_length=16, show_length=True))
            ]
        )

    def _tuple(self):
        return self.__correctness, self.__message, self.__detail

    def __eq__(self, other):
        if other is self:
            return True
        elif isinstance(other, self.__class__):
            return type(self) == type(other) and self._tuple() == other._tuple()
        else:
            return False

    def __hash__(self):
        return hash(self._tuple())
