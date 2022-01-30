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

    def test_eq(self):
        result = SimpleSPJResult(True, '123', '12345')
        assert result == result
        assert result == SimpleSPJResult(True, '123', '12345')
        assert result != 123

    def test_hash(self):
        _dict = {
            SimpleSPJResult(True, '123', '12345'): 1,
            SimpleSPJResult(False, '123', '12345'): 2,
        }

        assert _dict[SimpleSPJResult(True, '123', '12345')] == 1
        assert _dict[SimpleSPJResult(None, '123', '12345')] == 2
