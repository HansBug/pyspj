import json

import pytest
from click.testing import CliRunner

from pyspj.config.meta import __VERSION__
from pyspj.entry import pyspj_entry
from ..script.base import _spj_func


@pytest.mark.unittest
class TestEntryCliEntry:
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(pyspj_entry('mytest', _spj_func), args=['-v'])

        assert result.exit_code == 0
        assert "mytest" in result.stdout.lower()
        assert "pyspj" in result.stdout.lower()
        assert __VERSION__ in result.stdout.lower()

        runner = CliRunner()
        result = runner.invoke(pyspj_entry('mytest', _spj_func, version='10.3.7'), args=['-v'])

        assert result.exit_code == 0
        assert "mytest" in result.stdout.lower()
        assert '10.3.7' in result.stdout.lower()
        assert "pyspj" in result.stdout.lower()
        assert __VERSION__ in result.stdout.lower()

        runner = CliRunner()
        result = runner.invoke(pyspj_entry('mytest', _spj_func, author='bullshit'), args=['-v'])

        assert result.exit_code == 0
        assert "mytest" in result.stdout.lower()
        assert "pyspj" in result.stdout.lower()
        assert __VERSION__ in result.stdout.lower()
        assert 'bullshit' in result.stdout.lower()

        runner = CliRunner()
        result = runner.invoke(pyspj_entry('mytest', _spj_func, author='bullshit', email='bs@gmail.com'),
                               args=['-v'])

        assert result.exit_code == 0
        assert "mytest" in result.stdout.lower()
        assert "pyspj" in result.stdout.lower()
        assert __VERSION__ in result.stdout.lower()
        assert 'bullshit' in result.stdout.lower()
        assert 'bs@gmail.com' in result.stdout.lower()

    def test_common(self):
        runner = CliRunner()
        result = runner.invoke(pyspj_entry('mytest', _spj_func), args=['-i', '1 2 3 4 5', '-o', '15'])

        assert result.exit_code == 0
        assert json.loads(result.stdout) == {'correctness': True, 'detail': 'Correct result.',
                                             'message': 'Correct result.'}
