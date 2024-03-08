from src.lam import Func, IntTp, QuantifiedType, TpVar
from typecheck import free_vars


def test_free_vars():
    assert free_vars({}) == set()
    assert free_vars(IntTp()) == set()
    x = TpVar('x')
    y = TpVar('y')
    assert free_vars(x) == {x}
    assert free_vars({x: IntTp()}) == set()
    assert free_vars({x: y}) == {y}
    assert free_vars(Func(IntTp(), y)) == {y}
    assert free_vars(Func(x, y)) == {x, y}
    assert free_vars(QuantifiedType({x}, Func(x, y))) == {y}
