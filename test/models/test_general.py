import os

import pytest

from pyspj.models import load_result, SimpleSPJResult, ContinuitySPJResult


@pytest.mark.unittest
class TestModelsGeneral:
    def test_simple(self):
        result = SimpleSPJResult(True, '123', '12345')
        assert load_result(result) == result
        assert load_result(result.to_json()) == result
        assert load_result((True,)) == SimpleSPJResult(True, )
        assert load_result(True) == SimpleSPJResult(True, )
        assert load_result(None) == SimpleSPJResult(False, )
        assert load_result((True, '123')) == SimpleSPJResult(True, '123')
        assert load_result((True, '123', '12345')) == result

    def test_continuity(self):
        result = ContinuitySPJResult(True, 0.5, '123', '12345')
        assert load_result(result) == result
        assert load_result(result.to_json()) == result
        assert load_result(((True, 0.5),)) == ContinuitySPJResult(True, 0.5)
        assert load_result(((True, 0.5), '123')) == ContinuitySPJResult(True, 0.5, '123')
        assert load_result(((True, 0.5), '123', '12345')) == result

    def test_invalid(self):
        with pytest.raises(ValueError):
            assert load_result(())
        with pytest.raises(ValueError):
            assert load_result((1, 2, 3, 4))


if __name__ == "__main__":
    pytest.main([os.path.abspath(__file__)])
