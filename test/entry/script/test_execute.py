import io
import pathlib
import tempfile

import pytest

from pyspj.entry.script import execute_spj, execute_spj_from_string, execute_spj_from_file
from pyspj.models import SimpleSPJResult
from pyspj.utils import split_to_lines
from .base import _spj_func


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestEntryScriptExecute:
    def test_execute_spj(self):
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  15 ') as stdout:
            assert execute_spj(_spj_func, stdin, stdout) == SimpleSPJResult(True, 'Correct result.')
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  16 ') as stdout:
            assert execute_spj(_spj_func, stdin, stdout) == SimpleSPJResult(False, 'Result 15 expected but 16 found.')
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('') as stdout:
            result = execute_spj(_spj_func, stdin, stdout)
            assert not result.correctness
            assert result.message.startswith('Exception occurred while special judge - '
                                             'ValueError("invalid literal for int() with base 10:')
            assert len(split_to_lines(result.detail)) >= 3

    def test_execute_spj_string(self):
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  15 ') as stdout:
            assert execute_spj_from_string(_spj_func, stdin, stdout) == SimpleSPJResult(True, 'Correct result.')
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  16 ') as stdout:
            assert execute_spj_from_string(_spj_func, stdin, stdout) == \
                   SimpleSPJResult(False, 'Result 15 expected but 16 found.')
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('') as stdout:
            result = execute_spj_from_string(_spj_func, stdin, stdout)
            assert not result.correctness
            assert result.message.startswith('Exception occurred while special judge - '
                                             'ValueError("invalid literal for int() with base 10:')
            assert len(split_to_lines(result.detail)) >= 3

        assert execute_spj_from_string(_spj_func, '1 2 3 4  5', '  15 ') == SimpleSPJResult(True, 'Correct result.')
        assert execute_spj_from_string(_spj_func, '1 2 3 4  5', '  16 ') == \
               SimpleSPJResult(False, 'Result 15 expected but 16 found.')

        result = execute_spj_from_string(_spj_func, '1 2 3 4  5', '')
        assert not result.correctness
        assert result.message.startswith('Exception occurred while special judge - '
                                         'ValueError("invalid literal for int() with base 10:')

    def test_execute_spj_file(self):
        with tempfile.NamedTemporaryFile() as stdin_file, \
                tempfile.NamedTemporaryFile() as stdout_file:
            pathlib.Path(stdin_file.name).write_text('1 2 3  4  5')
            pathlib.Path(stdout_file.name).write_text('  15 ')

            result = execute_spj_from_file(_spj_func, stdin_file.name, stdout_file.name)
            assert result == SimpleSPJResult(True, 'Correct result.')

        with tempfile.NamedTemporaryFile() as stdin_file, \
                tempfile.NamedTemporaryFile() as stdout_file:
            pathlib.Path(stdin_file.name).write_text('1 2 3  4  5')
            pathlib.Path(stdout_file.name).write_text('  16 ')

            result = execute_spj_from_file(_spj_func, stdin_file.name, stdout_file.name)
            assert result == SimpleSPJResult(False, 'Result 15 expected but 16 found.')

        with tempfile.NamedTemporaryFile() as stdin_file, \
                tempfile.NamedTemporaryFile() as stdout_file:
            pathlib.Path(stdin_file.name).write_text('1 2 3  4  5')
            pathlib.Path(stdout_file.name).write_text('')

            result = execute_spj_from_file(_spj_func, stdin_file.name, stdout_file.name)
            assert not result.correctness
            assert result.message.startswith('Exception occurred while special judge - '
                                             'ValueError("invalid literal for int() with base 10:')
