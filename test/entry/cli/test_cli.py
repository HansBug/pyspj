import os

import pytest
from click.testing import CliRunner

from pyspj.entry.cli import cli


@pytest.mark.unittest
class TestEntryCliCli:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, args=['-v'])

        assert result.exit_code == 0
        assert "pyspj" in result.stdout.lower()


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
