from src.lam import Func, IntTp, QuantifiedType, TpVar
from typecheck import canonicalize, free_vars, generalize, saturate, subst_type


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


def test_saturate_and_canonicalize():
    a = TpVar('a0')
    b = TpVar('a1')
    c = TpVar('a2')
    d = TpVar('a3')
    t = Func(a, Func(b, c))
    # depending on the order it could produce either:
    # ('a -> 'b) -> 'a -> 'b
    # ('a -> 'a) -> 'b -> 'a
    S = set([
        (a, Func(b, d)),
        (a, Func(d, c)),
    ])
    print(t)
    print(S)
    saturate(S)
    print(S)
    t = canonicalize(S, t)
    print(t)
    assert t == Func(Func(a, a), Func(a, a))


def test_canonicalize():
    a0 = TpVar('a0')
    a1 = TpVar('a1')
    a2 = TpVar('a2')
    a3 = TpVar('a3')
    S = {
        (a1, a2),
        (a0, Func(a3, a2)),
        (a3, a2),
        (Func(a3, a2), Func(a1, a3)),
        (Func(a1, a3), a0),
        (a3, a1),
        (Func(a3, a2), a0),
        (a0, Func(a1, a3)),
        (Func(a1, a3), Func(a3, a2)),
        (a2, a3),
        (a1, a3),
        (a2, a1)
    }
    t = Func(a0, Func(a1, a2))
    print(t)
    t = canonicalize(S, t)
    print(t)
    assert t == Func(Func(a1, a1), Func(a1, a1))

# A: {}
# S: {
#    (a0, a1 -> a3),
#    (a0, a3 -> a2)
# }

"""
unit test:
a0 -> a1 -> a2
{(a0, a1 -> a3), (a0, a3 -> a2)}
{
    (a1, a2),
    (a0, a3 -> a2),
    (a3, a2),
    (a3 -> a2, a1 -> a3),
    (a1 -> a3, a0),
    (a3, a1),
    (a3 -> a2, a0),
    (a0, a1 -> a3),
    (a1 -> a3, a3 -> a2),
    (a2, a3),
    (a1, a3),
    (a2, a1)
}
(a1 -> a1) -> a2 -> a1

type checker:
a0 -> a1 -> a2
{}
{(a0, a1 -> a3), (a0, a3 -> a2)}

"""
