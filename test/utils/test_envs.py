import pytest

from pyspj.utils import string_to_env, list_to_envs, env_to_string, envs_to_list


@pytest.mark.unittest
class TestUtilsEnvs:
    def test_string_to_env(self):
        assert string_to_env('1=2') == ('1', '2')
        assert string_to_env('THIS=') == ('THIS', '')
        assert string_to_env('THIS=1=2') == ('THIS', '1=2')

    def test_list_to_envs(self):
        assert list_to_envs([
            '1=2',
            'THIS=',
            'OK=kjsdlf-2398',
            'THISX=1=2',
        ]) == {
                   '1': '2',
                   'THIS': '',
                   'OK': 'kjsdlf-2398',
                   'THISX': '1=2',
               }

    def test_env_to_string(self):
        assert env_to_string('1', '2') == '1=2'
        assert env_to_string('THIS', '') == 'THIS='
        assert env_to_string('THIS', '1=2') == 'THIS=1=2'

    def test_envs_to_list(self):
        assert set(envs_to_list({
            '1': '2',
            'THIS': '',
            'OK': 'kjsdlf-2398',
            'THISX': '1=2',
        })) == {'1=2', 'THIS=', 'OK=kjsdlf-2398', 'THISX=1=2'}
