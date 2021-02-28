import os

import pytest

from pyspj.utils import truncate, split_to_lines


@pytest.mark.unittest
class TestUtilsString:
    def test_truncate(self):
        assert truncate(
            'this is the first time we do this kind of thing') == 'this is the first time we do this kind of thing'
        assert truncate('this is the first time we do this kind of thing', width=30) == 'this is the first time we ... '
        assert truncate('this is the first time we do this kind of thing', width=40, tail_length=12,
                        show_length=True) == 'this is the ..(47 chars).. ind of thing'

    def test_split_to_lines(self):
        assert split_to_lines('this is a line\n') == [
            'this ia a line',
        ]


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
