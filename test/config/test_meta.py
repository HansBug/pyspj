import os

import pytest

from pyspj.config.meta import __TITLE__


@pytest.mark.unittest
class TestConfigMeta:
    def test_title(self):
        assert __TITLE__ == 'pyspj'


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
