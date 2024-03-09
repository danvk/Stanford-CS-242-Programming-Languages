
### PROGRAMS ###

# A program is just a sequence of definitions
class Prog:
    def __init__(self, defns): self.defns = defns
    def __repr__(self): return "\n".join(map(str, self.defns))
# A definition is just a var and an expression
class Defn:
    def __init__(self, s, e): self.s, self.e = s, e
    def __repr__(self): return "def {} = {};".format(self.s, self.e)

### Expressions ###
class Expr:
    pass

# Var also represents constants; see below
class Var(Expr):
    def __init__(self, s: str): self.s = s
    def __repr__(self): return "{}".format(self.s)

class Lam(Expr):
    def __init__(self, s: str, e: Expr): self.s, self.e = s, e
    def __repr__(self): return "\{}.{}".format(self.s, self.e)

class App(Expr):
    def __init__(self, e1: Expr, e2: Expr): self.e1, self.e2 = e1, e2
    def __repr__(self): return "({} {})".format(self.e1, self.e2)

class IntConst(Expr):
    def __init__(self, i: int): self.i = i
    def __repr__(self): return "{}".format(self.i)

class BoolConst(Expr):
    def __init__(self, b: bool): self.b = b
    def __repr__(self): return "true" if self.b else "false"

### Types ###

class PolymorphicType:
    def __eq__(self, other) -> bool: raise NotImplementedError()
    def __hash__(self) -> int: raise NotImplementedError()

# Note, Type is an abstract base class; all instances are expected to be one of the cases below.
# Type objects can be compared for structural equality, and thus stored in sets/maps/etc.
# For example, Func(IntType(), IntType()) == Func(IntType(), IntType()) is true, even though the
# actual objects at runtime are different. Note this is *structural equality*, so
# IntType() != TypeVar('x') even if we have an equation somewhere saying TypeVar('x') is IntType().
class Type(PolymorphicType):
    def __eq__(self, other) -> bool: raise NotImplementedError()
    def __hash__(self) -> int: raise NotImplementedError()

class PrimitiveTp(Type):
    def __eq__(self, other) -> bool: raise NotImplementedError()
    def __hash__(self) -> int: raise NotImplementedError()

class IntTp(Type):
    def __eq__(self, other) -> bool:
        return isinstance(other, IntTp)
    def __hash__(self): return hash('Int')
    def __repr__(self): return "int"

class BoolTp(Type):
    def __eq__(self, other) -> bool:
        return isinstance(other, BoolTp)
    def __hash__(self): return hash('Bool')
    def __repr__(self): return "bool"

class Func(Type):
    def __init__(self, a: Type, b: Type): self.a, self.b = a, b
    def __eq__(self, other) -> bool:
        if not isinstance(other, Func): return False
        return self.a == other.a and self.b == other.b
    def __hash__(self): return hash(('Func', self.a, self.b))
    def __repr__(self):
        a = self.a if not isinstance(self.a, Func) else "({})".format(self.a)
        return "{} -> {}".format(a, self.b)

class TpVar(Type):
    def __init__(self, s: str): self.s = s
    def __eq__(self, other) -> bool:
        if not isinstance(other, TpVar): return False
        return self.s == other.s
    def __hash__(self): return hash(('TpVar', self.s))
    def __repr__(self): return self.s

class QuantifiedType(PolymorphicType):
    def __init__(self, vars: list[TpVar], o: PolymorphicType):
        self.vars = vars
        self.o = o

    def __eq__(self, other) -> bool:
        if not isinstance(other, QuantifiedType):
            return False
        return self.vars == other.vars and self.o == other.o

    def __hash__(self) -> int:
        return hash(('QuantifiedType', self.vars, self.o))

    def __repr__(self):
        return self.o.__repr__()

### CONSTANTS ###

# Constants have a fixed type supplied by the following table. Var('x') is a constant
# if 'x' in CONSTS. Otherwise, it is a variable. The parser we have supplied will ensure
# bound variables are never equal to constants.

_I = IntTp()
_B = BoolTp()
a = TpVar("'a")
CONSTS = {
    '+': Func(_I, Func(_I, _I)),
    '-': Func(_I, Func(_I, _I)),
    '/': Func(_I, Func(_I, _I)),
    '*': Func(_I, Func(_I, _I)),
    'ifz': Func(_I, Func(_I, Func(_I, _I))),
    'if': QuantifiedType([a], Func(_B, Func(a, Func(a, a)))),
}

### TYPECHECKING ###

# Throw the following error if you detect that the input program is not type-correct:
#   raise TypecheckingError("reason")
# The reason message is optional, but may help you debug your own code  if you get a
# type error when you don't expect it. Don't confuse this with Python's TypeError.
class TypecheckingError(Exception):
    pass
