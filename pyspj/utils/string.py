import io
from textwrap import shorten as _shorten
from typing import List


def truncate(text: str, width: int = 70, tail_length: int = 0, show_length: bool = False):
    """
    truncate string into short form
    :param text: original text
    :param width: final width
    :param tail_length: tail's length
    :param show_length: show length in middle part or not
    :return: short-formed string
    """
    text = str(text)

    if show_length:
        omission = ' ..({length} chars).. '.format(length=len(text))
    else:
        omission = ' ... '
    if tail_length:
        omission += text[len(text) - tail_length:]

    return _shorten(text, width=width, placeholder=omission)


def split_to_lines(string: str) -> List[str]:
    """
    split string into lines
    :param string: original string
    :return: lines of string
    """
    with io.StringIO(string) as sf:
        return [line.rstrip('\r\n') for line in sf.readlines()]
