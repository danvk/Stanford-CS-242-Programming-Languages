
from typing import Dict, Tuple, Set
from src.lam import *

_ops = {'+': lambda x,y: x+y,
        '-': lambda x,y: x-y,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x//y}

def _fold_app(e: Tuple[Expr, ...]) -> Expr:
    if 1 < len(e):
        return App(_fold_app(e[:-1]), e[-1])
    return e[0]

def fv(e: Expr) -> Set[str]:
    if isinstance(e, Var):
        return set([e.s])
    if isinstance(e, App):
        return fv(e.e1).union(fv(e.e2))
    if isinstance(e, Lam):
        x = fv(e.e)
        x.discard(e.s)
        return x
    else:
        return set()

def fresh_wrt(vs: Set[str], hint: str = 'x') -> str:
    v = hint
    i = 0
    while v in vs:
        v = f'{hint}{i}'
        i += 1
    return v

# Implementation of capture avoiding substitution substituting e for s in a
def subst(e: Expr, s: str, a: Expr) -> Expr:
    if isinstance(a, (IntConst, BoolConst)):
        return a
    if isinstance(a, Var):
        return e if a.s == s else a
    if isinstance(a, App):
        return App(subst(e, s, a.e1), subst(e, s, a.e2))
    if isinstance(a, Lam):
        if a.s == s:
            return a
        fv_e = fv(e)
        if a.s not in fv_e:
            return Lam(a.s, subst(e, s, a.e))
        else:
            z = fresh_wrt(fv_e, a.s)
            return Lam(z, subst(e, s, subst(Var(z), a.s, a.e)))
    assert False

def _eval(e: Expr) -> Expr:
    return _fold_app(_eval_app((e,)))

def _eval_app(app: Tuple[Expr, ...]) -> Tuple[Expr, ...]:
    if len(app) == 0: return ()
    # print(app)
    h = app[0]
    if isinstance(h, App):
        return _eval_app((h.e1, h.e2, *app[1:]))
    elif isinstance(h, Lam) and len(app) > 1:
        return _eval_app((subst(app[1], h.s, h.e), *app[2:]))
    elif isinstance(h, Var):
        if h.s in ['+', '-', '*', '/'] and len(app) > 2:
            (op, a, b, *rest) = app
            a = _eval(a)
            b = _eval(b)
            if isinstance(a, IntConst) and isinstance(b, IntConst):
                if h.s == '/' and b.i == 0: raise TypecheckingError("Division by zero")
                return _eval_app((IntConst(_ops[h.s](a.i, b.i)), *rest))
            else:
                raise TypecheckingError(f"Expected {h.s} argument to be an int")
        elif h.s == 'ifz' and len(app) > 3:
            (op, a, b, c, *rest) = app
            a = _eval(a)
            if isinstance(a, IntConst):
                return _eval_app((b if a.i == 0 else c, *rest))
            else:
                raise TypecheckingError("Expected ifz argument to be an int")
        elif h.s == 'if' and len(app) > 3:
            (op, a, b, c, *rest) = app
            a = _eval(a)
            if isinstance(a, BoolConst):
                return _eval_app((b if a.b else c, *rest))
            else:
                raise TypecheckingError("Expected if argument to be a bool")
        return (h, *(_eval(a) for a in app[1:]))
    elif isinstance(h, (IntConst, BoolConst)):
        return (h, *_eval_app(app[1:]))
    elif isinstance(h, Lam):
        return app
    else: assert False

def eval_lam(p: Prog) -> None:
    for i, defn in enumerate(p.defns):
        term = defn.e
        for p_def in reversed(p.defns[:i]):
            term = subst(p_def.e, p_def.s, term)
        print(defn.s, '=', _eval(term))
