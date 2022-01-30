import pytest

from pyspj.models import ContinuitySPJResult


@pytest.mark.unittest
class TestModelsContinuity:
    def test_simple(self):
        result = ContinuitySPJResult(True, 0.5, '123', '12345')
        assert result.correctness
        assert result.score == 0.5
        assert result.message == '123'
        assert result.detail == '12345'

    def test_invalid_score(self):
        with pytest.raises(ValueError):
            ContinuitySPJResult(True, -0.5, '123', '12345')
        with pytest.raises(ValueError):
            ContinuitySPJResult(True, 1.5, '123', '12345')

    def test_to_json(self):
        result = ContinuitySPJResult(True, 0.5, '123', '12345')
        assert result.to_json() == {'correctness': True, 'detail': '12345', 'message': '123', 'score': 0.5}

    def test_repr(self):
        result = ContinuitySPJResult(True, 0.5, '123', '12345')
        assert repr(result) == "<ContinuitySPJResult correctness: True, score: 0.500, message: '123'>"

    def test_eq(self):
        result = ContinuitySPJResult(True, 0.5, '123', '12345')
        assert result == result
        assert result == ContinuitySPJResult(True, 0.5, '123', '12345')
        assert result != 123

    def test_hash(self):
        _dict = {
            ContinuitySPJResult(True, 0.5, '123', '12345'): 1,
            ContinuitySPJResult(False, 0.5, '123', '12345'): 2,
        }

        assert _dict[ContinuitySPJResult(True, 0.5, '123', '12345')] == 1
        assert _dict[ContinuitySPJResult(False, 0.5, '123', '12345')] == 2
