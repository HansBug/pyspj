import warnings
from abc import ABCMeta
from typing import Optional, Mapping

from ..utils import split_to_lines, get_repr_info, truncate

_DEFAULT_SUCCESS_MESSAGE = 'Congratulations, test passed!'
_DEFAULT_FAILURE_MESSAGE = 'Sorry, test failed!'


def _check_message(message: str) -> str:
    message = message.strip()
    _message_lines = split_to_lines(message)
    if not _message_lines:
        warnings.warn('Message contains 0 line, no message will be displayed.')
    elif len(_message_lines) > 1:
        warnings.warn('Message contains {n} lines, '
                      'we strongly recommend you to simplify the '
                      'message into exactly 1 line to keep its briefness.'.format(n=repr(len(_message_lines))))

    return message


class SPJResult(metaclass=ABCMeta):
    def __init__(self, correctness: bool, message: Optional[str] = None, detail: Optional[str] = None):
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
                ('correctness', lambda: repr(self.__correctness)),
                ('message', lambda: truncate(repr(self.__message), width=64, tail_length=16, show_length=True))
            ]
        )
