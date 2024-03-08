class Expr(object):
    pass

class S(Expr):
    # `S()` denotes the S combinator.
    __str__ = lambda self: "S"
    __repr__ = __str__

class K(Expr):
    # `K()` denotes the K combinator.
    __str__ = lambda self: "K"
    __repr__ = __str__

class I(Expr):
    # `I()` denotes the I combinator.
    __str__ = lambda self: "I"
    __repr__ = __str__

class Var(Expr):
    # `Var("x")` denotes the variable x.
    def __init__(self, s):
        self.s = s

    __str__ = lambda self: "{}".format(self.s)
    __repr__ = __str__

    def __eq__(self, other):
        return isinstance(other, Var) and other.s == self.s

class App(Expr):
    # `App(e1,e2)` denotes the application (e1 e2).
    def __init__(self, e1, e2):
        self.e1, self.e2 = e1, e2

    __str__ = lambda self: "({} {})".format(self.e1, self.e2)
    __repr__ = __str__
