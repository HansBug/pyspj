import io

import pytest

from pyspj.entry.script import execute_spj
from pyspj.models import SimpleSPJResult
from .base import _spj_func


# noinspection DuplicatedCode
@pytest.mark.unittest
class TestEntryScriptImports:
    def test_func(self):
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  15 ') as stdout:
            assert execute_spj(_spj_func, stdin, stdout) == SimpleSPJResult(True, 'Correct result.')
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  16 ') as stdout:
            assert execute_spj(_spj_func, stdin, stdout) == SimpleSPJResult(False, 'Result 15 expected but 16 found.')

    def test_string(self):
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  15 ') as stdout:
            assert execute_spj('test.entry.script.base:_spj_func', stdin, stdout) == \
                   SimpleSPJResult(True, 'Correct result.')
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  16 ') as stdout:
            assert execute_spj('test.entry.script.base:_spj_func', stdin, stdout) == \
                   SimpleSPJResult(False, 'Result 15 expected but 16 found.')

    def test_string_simple(self):
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  15 ') as stdout:
            assert execute_spj('test.entry.script.base', stdin, stdout) == \
                   SimpleSPJResult(True, 'Correct result.')
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  16 ') as stdout:
            assert execute_spj('test.entry.script.base', stdin, stdout) == \
                   SimpleSPJResult(False, 'Result 15 expected but 16 found.')

    def test_string_invalid(self):
        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  15 ') as stdout:
            with pytest.raises(TypeError):
                execute_spj(None, stdin, stdout)

        with io.StringIO('1 2 3  4  5') as stdin, io.StringIO('  15 ') as stdout:
            with pytest.raises(TypeError):
                execute_spj('test.entry.script.base:_another_value', stdin, stdout)
