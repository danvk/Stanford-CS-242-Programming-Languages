from src.lam import Func, IntTp, QuantifiedType, TpVar
from typecheck import free_vars, generalize, subst_type


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


def test_generalize():
    x = TpVar('x')
    assert generalize({}, Func(x, x)) == QuantifiedType(vars={x}, o=Func(x, x))
    y = TpVar('y')
    z = TpVar('z')
    assert generalize({}, Func(x, y)) == QuantifiedType(vars={x, y}, o=Func(x, y))
    assert generalize({z: y}, Func(x, y)) == QuantifiedType(vars={x}, o=Func(x, y))
    assert generalize({z: Func(x, y)}, Func(x, y)) == Func(x, y)


def test_subst():
    x = TpVar('x')
    y = TpVar('y')
    z = TpVar('z')
    assert subst_type(x, x, y) == y
    assert subst_type(Func(x, z), x, y) == Func(y, z)
    assert subst_type(Func(x, z), z, y) == Func(x, y)
    assert subst_type(Func(IntTp(), Func(x, y)), y, z) == Func(IntTp(), Func(x, z))
