import pytest

from pyspj.models import load_result, SimpleSPJResult, ContinuitySPJResult, ResultType


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

    def test_simple_force(self):
        result = SimpleSPJResult(True, '123', '12345')
        assert load_result(result, 'simple') == result
        assert load_result(result.to_json(), 'simple') == result
        assert load_result((True,), 'simple') == SimpleSPJResult(True, )
        assert load_result(True, 'simple') == SimpleSPJResult(True, )
        assert load_result(None, 'simple') == SimpleSPJResult(False, )
        assert load_result((True, '123'), 'simple') == SimpleSPJResult(True, '123')
        assert load_result((True, '123', '12345'), 'simple') == result

        result = ContinuitySPJResult(True, 0.5, '123', '12345')
        assert load_result(result, 'simple') == SimpleSPJResult(True, '123', '12345')
        assert load_result(result.to_json(), 'simple') == SimpleSPJResult(True, '123', '12345')
        assert load_result(((True, 0.5),), 'simple') == SimpleSPJResult(True)
        assert load_result(((True, 0.5), '123'), 'simple') == SimpleSPJResult(True, '123')
        assert load_result(((True, 0.5), '123', '12345'), 'simple') == SimpleSPJResult(True, '123', '12345')

    def test_continuity_force(self):
        result = SimpleSPJResult(True, '123', '12345')
        assert load_result(result, 'continuity') == ContinuitySPJResult(True, 0.0, '123', '12345')
        assert load_result(result.to_json(), 'continuity') == ContinuitySPJResult(True, 0.0, '123', '12345')
        assert load_result((True,), 'continuity') == ContinuitySPJResult(True, 0.0)
        assert load_result(True, 'continuity') == ContinuitySPJResult(True, 0.0)
        assert load_result(None, 'continuity') == ContinuitySPJResult(False, 0.0, )
        assert load_result((True, '123'), 'continuity') == ContinuitySPJResult(True, 0.0, '123')
        assert load_result((True, '123', '12345'), 'continuity') == ContinuitySPJResult(True, 0.0, '123', '12345')

        result = ContinuitySPJResult(True, 0.5, '123', '12345')
        assert load_result(result, 'continuity') == result
        assert load_result(result.to_json(), 'continuity') == result
        assert load_result(((True, 0.5),), 'continuity') == ContinuitySPJResult(True, 0.5)
        assert load_result(((True, 0.5), '123'), 'continuity') == ContinuitySPJResult(True, 0.5, '123')
        assert load_result(((True, 0.5), '123', '12345'), 'continuity') == result

    def test_invalid(self):
        with pytest.raises(ValueError):
            assert load_result(())
        with pytest.raises(ValueError):
            assert load_result((1, 2, 3, 4))

    def test_result_type(self):
        assert ResultType.loads(ResultType.FREE) == ResultType.FREE
        assert ResultType.loads(ResultType.SIMPLE) == ResultType.SIMPLE
        assert ResultType.loads(ResultType.CONTINUITY) == ResultType.CONTINUITY

        assert ResultType.loads('free') == ResultType.FREE
        assert ResultType.loads('simple') == ResultType.SIMPLE
        assert ResultType.loads('continuity') == ResultType.CONTINUITY
        with pytest.raises(KeyError):
            ResultType.loads('sdkfjlsd')

        assert ResultType.loads(0) == ResultType.FREE
        assert ResultType.loads(1) == ResultType.SIMPLE
        assert ResultType.loads(2) == ResultType.CONTINUITY
        with pytest.raises(ValueError):
            ResultType.loads(-100)

        with pytest.raises(TypeError):
            ResultType.loads([])
