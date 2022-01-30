import codecs
import json

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

    def test_common(self):
        runner = CliRunner()
        result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-o', '15', '-s', 'test.entry.script.base:_spj_func'])

        assert result.exit_code == 0
        assert json.loads(result.stdout) == {'correctness': True, 'detail': 'Correct result.',
                                             'message': 'Correct result.'}

    def test_common_invalid(self):
        runner = CliRunner()
        result = runner.invoke(cli, args=['-o', '15', '-s', 'test.entry.script.base:_spj_func'])
        assert result.exit_code == 1

        runner = CliRunner()
        result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-s', 'test.entry.script.base:_spj_func'])
        assert result.exit_code == 1

    def test_file_stdin(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('input.txt', 'w') as stdin_file:
                stdin_file.write('1 2 3 4 5')
            result = runner.invoke(cli, args=['-I', 'input.txt', '-o', '15', '-s', 'test.entry.script.base:_spj_func'])

            assert result.exit_code == 0
            assert json.loads(result.stdout) == {'correctness': True, 'detail': 'Correct result.',
                                                 'message': 'Correct result.'}

    def test_file_stdout(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('output.txt', 'w') as stdout_file:
                stdout_file.write('15')
            result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-O', 'output.txt', '-s',
                                              'test.entry.script.base:_spj_func'])

            assert result.exit_code == 0
            assert json.loads(result.stdout) == {'correctness': True, 'detail': 'Correct result.',
                                                 'message': 'Correct result.'}

    def test_file_io(self):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with codecs.open('input.txt', 'w') as stdin_file:
                stdin_file.write('1 2 3 4 5')
            with codecs.open('output.txt', 'w') as stdout_file:
                stdout_file.write('15')
            result = runner.invoke(cli, args=['-I', 'input.txt', '-O', 'output.txt', '-s',
                                              'test.entry.script.base:_spj_func'])

            assert result.exit_code == 0
            assert json.loads(result.stdout) == {'correctness': True, 'detail': 'Correct result.',
                                                 'message': 'Correct result.'}

    def test_pretty(self):
        runner = CliRunner()
        result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-o', '15', '-s', 'test.entry.script.base:_spj_func'])

        assert result.exit_code == 0
        assert result.stdout.strip() == json.dumps({'correctness': True, 'detail': 'Correct result.',
                                                    'message': 'Correct result.'}, sort_keys=True).strip()

        runner = CliRunner()
        result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-o', '15',
                                          '-s', 'test.entry.script.base:_spj_func', '-p'])

        assert result.exit_code == 0
        assert result.stdout.strip() == json.dumps({'correctness': True, 'detail': 'Correct result.',
                                                    'message': 'Correct result.'}, sort_keys=True, indent=4).strip()

    def test_attached_values(self):
        runner = CliRunner()
        result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-o', '15',
                                          '-s', 'test.entry.script.base:_spj_func',
                                          '-V', 'fxxk=233'])

        assert result.exit_code == 0
        assert result.stdout.strip() == json.dumps({
            "correctness": False,
            "detail": "Result error because '233' detected in fxxk.",
            "message": "Result error because '233' detected in fxxk."
        }, sort_keys=True).strip()

        runner = CliRunner()
        result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-o', '15',
                                          '-s', 'test.entry.script.base:_spj_func',
                                          '-V', 'stdin=233', ])
        assert result.exit_code == 1

        runner = CliRunner()
        result = runner.invoke(cli, args=['-i', '1 2 3 4 5', '-o', '15',
                                          '-s', 'test.entry.script.base:_spj_func',
                                          '-V', 'fxxk=233', '-V', 'tf=233'])
        assert result.exit_code == 0
        assert "unexpected keyword argument 'tf'" in result.stdout.strip()
