import os

import pytest

from pyspj.models.simple import SimpleSPJResult


@pytest.mark.unittest
class TestModelsSimple:
    def test_simple(self):
        result = SimpleSPJResult(True, '123', '12345')
        assert result.correctness
        assert result.message == '123'
        assert result.detail == '12345'

    def test_to_json(self):
        result = SimpleSPJResult(True, '123', '12345')
        assert result.to_json() == {'correctness': True, 'detail': '12345', 'message': '123'}

    def test_repr(self):
        result = SimpleSPJResult(True, '123', '12345')
        assert repr(result) == "<SimpleSPJResult correctness: True, message: '123'>"

    def test_message_warning_greater_than_1(self):
        with pytest.warns(Warning):
            SimpleSPJResult(True, '1 2 3 4 5\nskdjflsd', '12345')


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
