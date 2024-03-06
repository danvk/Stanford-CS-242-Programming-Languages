
from src.lam import CONSTS, App, Expr, Func, IntConst, IntTp, Lam, Prog, TpVar, Type, TypecheckingError, Var
from typing import List

def typecheck(prog: Prog) -> List[Type]:
    A, S = gen_constraints_prog(prog)
    saturate(S)
    check_ill_typed(S)

    # If there are no type errors, return a list of Types, one for each definition
    types = []
    for defn in prog.defns:
        types.append(canonicalize(S, A[defn.s]))
        assert len(canonicalizing) == 0, f'{canonicalizing=}'
    return types


n = -1
def get_fresh_type():
    global n
    n += 1
    return TpVar(f'a{n}')


def gen_constraints(
    A: dict[str, Type],
    e: Expr,
    S: set[tuple[Type, Type]],
) -> Type:
    match e:
        case Var(s=s) if s in CONSTS:
            return CONSTS[s]
        case Var(s=s) if s in A:
            return A[s]
        case Var(s=s):
            # free variable
            raise TypecheckingError(f'undefined variable {s}')
        case IntConst():
            return IntTp()
        case Lam(s=s, e=e):
            prev = A.get(s)
            # s only has this type in this scope, so we need to reset it after.
            alpha = get_fresh_type()
            A[s] = alpha
            t = gen_constraints(A, e, S)
            if prev:
                A[s] = prev
            else:
                del A[s]
            return Func(alpha, t)
        case App(e1=e1, e2=e2):
            beta = get_fresh_type()
            tau = gen_constraints(A, e1, S)
            tau_p = gen_constraints(A, e2, S)
            S.add((tau, Func(tau_p, beta)))
            return beta


def gen_constraints_prog(prog: Prog):
    global n
    n = -1
    S = set()
    A = {}
    for defn in prog.defns:
        t = gen_constraints(A, defn.e, S)
        A[defn.s] = t
    return A, S


def saturate(S: set[tuple[TpVar, Type]]):
    """operates in-place"""
    any_new = True
    while any_new:
        any_new = False
        to_add = set()
        for left, right in S:
            to_add.add((right, left))  # refl
            match (left, right):
                case (Func(a=t1, b=t2), Func(a=t3, b=t4)):
                    # struct
                    to_add.add((t1, t3))
                    to_add.add((t2, t4))
            other_rights = [r for (l, r) in S if l == left and r != right]
            for r in other_rights:
                to_add.add((right, r))  # trans

        for constraint in to_add:
            if constraint not in S:
                any_new = True
                S.add(constraint)


def check_ill_typed(S: set[tuple[TpVar, Type]]):
    # look for (t -> t' = int) in S
    for left, right in S:
        if right == IntTp() and isinstance(left, Func):
            raise TypecheckingError(f'ill-typed: Found {left} = {right}')


canonicalizing = set()


def canonicalize(S: set[tuple[Type, Type]], type: Type) -> Type:
    global canonicalizing
    try:
        if type in canonicalizing:
            raise TypecheckingError("infinite")
        canonicalizing.add(type)

        match type:
            case IntTp():
                return type
            case Func(a=a, b=b):
                return Func(canonicalize(S, a), canonicalize(S, b))
            case TpVar():
                equivs = [right for left, right in S if left == type]
                for t in equivs:
                    if not isinstance(t, TpVar):
                        return canonicalize(S, t)
                if equivs:
                    for t in equivs:
                        assert isinstance(t, TpVar)
                    return min(equivs, key=lambda t: t.s)
                return type
        raise ValueError(type)

    except (TypecheckingError, ValueError) as e:
        canonicalizing = {type}  # gets cleared below
        raise e

    finally:
        canonicalizing.remove(type)
