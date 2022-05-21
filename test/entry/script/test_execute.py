import io
import pathlib

import pytest
from hbutils.testing import isolated_directory

from pyspj.entry.script import execute_spj, execute_spj_from_string, execute_spj_from_file
from pyspj.models import SimpleSPJResult
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
            assert len(result.detail.splitlines()) >= 3

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
            assert len(result.detail.splitlines()) >= 3

        assert execute_spj_from_string(_spj_func, '1 2 3 4  5', '  15 ') == SimpleSPJResult(True, 'Correct result.')
        assert execute_spj_from_string(_spj_func, '1 2 3 4  5', '  16 ') == \
               SimpleSPJResult(False, 'Result 15 expected but 16 found.')

        result = execute_spj_from_string(_spj_func, '1 2 3 4  5', '')
        assert not result.correctness
        assert result.message.startswith('Exception occurred while special judge - '
                                         'ValueError("invalid literal for int() with base 10:')

    def test_execute_spj_file_correct(self):
        with isolated_directory():
            pathlib.Path('input.txt').write_text('1 2 3  4  5')
            pathlib.Path('output.txt').write_text('  15 ')

            result = execute_spj_from_file(_spj_func, 'input.txt', 'output.txt')
            assert result == SimpleSPJResult(True, 'Correct result.')

    def test_execute_spj_file_wrong_answer(self):
        with isolated_directory():
            pathlib.Path('input.txt').write_text('1 2 3  4  5')
            pathlib.Path('output.txt').write_text('  16 ')

            result = execute_spj_from_file(_spj_func, 'input.txt', 'output.txt')
            assert result == SimpleSPJResult(False, 'Result 15 expected but 16 found.')

    def test_execute_spj_file_error(self):
        with isolated_directory():
            pathlib.Path('input.txt').write_text('1 2 3  4  5')
            pathlib.Path('output.txt').write_text('')

            result = execute_spj_from_file(_spj_func, 'input.txt', 'output.txt')
            assert not result.correctness
            assert result.message.startswith('Exception occurred while special judge - '
                                             'ValueError("invalid literal for int() with base 10:')
