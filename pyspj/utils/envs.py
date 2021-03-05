from typing import List, Mapping


def string_to_env(string: str):
    """
    get environ tuple from single string
    :param string: env string
    :return: env name, env value
    """
    _name, _value = string.split('=', maxsplit=1)
    return _name, _value


def list_to_envs(strings: List[str]) -> Mapping[str, str]:
    """
    get environs from list of strings
    :param strings: list of strings
    :return: environ dict
    """
    return dict([string_to_env(_item) for _item in strings])


def env_to_string(name, value) -> str:
    """
    get string from env name and value
    :param name: environ name
    :param value: environ value
    :return: environ full string
    """
    return '{name}={value}'.format(name=name, value=value)


def envs_to_list(envs: Mapping[str, str]) -> List[str]:
    """
    get list of strings from envs dict
    :param envs: envs dict
    :return: list of strings
    """
    return [env_to_string(_name, _value) for _name, _value in envs.items()]
