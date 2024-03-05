
from src.lam import CONSTS, App, Expr, Func, IntConst, IntTp, Lam, Prog, TpVar, Type, TypecheckingError, Var
from typing import List

def typecheck(prog: Prog) -> List[Type]:
    A = gen_constraints_prog(prog)
    # print(A)
    # print(type_constraints)
    saturate(type_constraints)
    # print(type_constraints)
    # for left, right in type_constraints:
    #     print(f'{left} = {right}')
    if is_ill_typed(type_constraints):
        raise TypecheckingError("ill-typed")

    for left, _ in type_constraints:
        canonicalize(type_constraints, left)

    # If there are no type errors, return a list of Types
    # returns a list of Types, one for each definition
    types = [
        canonicalize(type_constraints, A[defn.s]) for defn in prog.defns
    ]
    # for defn, type in zip(prog.defns, types):
    #     print(f'{defn.s}: {type}')
    return types


n = -1
def get_fresh_type():
    global n
    n += 1
    return TpVar(f'a{n}')


type_constraints: set[tuple[Type, Type]] = set()


def gen_constraints(A: dict[str, Type], e: Expr) -> Type:
    match e:
        case Var(s=s) if s in A:
            return A[s]
        case Var(s=s) if s in CONSTS:
            return CONSTS[s]
        case Var(s=s):
            # free variable
            raise TypecheckingError(f'undefined variable {s}')
        case IntConst():
            return IntTp()
        case Lam(s=s, e=e):
            prev = A.get(s)
            # s only has this type in this scope.
            # Unclear to me if they want us to track this.
            alpha = get_fresh_type()
            A[s] = alpha
            t = gen_constraints(A, e)
            if prev:
                A[s] = prev
            else:
                del A[s]
            return Func(alpha, t)
        case App(e1=e1, e2=e2):
            beta = get_fresh_type()
            tau = gen_constraints(A, e1)
            tau_p = gen_constraints(A, e2)
            type_constraints.add((tau, Func(tau_p, beta)))
            return beta


def gen_constraints_prog(prog: Prog):
    global type_constraints
    type_constraints = set()
    A = {}
    for defn in prog.defns:
        t = gen_constraints(A, defn.e)
        A[defn.s] = t
    return A


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
                to_add.add((right, r))

        for constraint in to_add:
            if constraint not in S:
                any_new = True
                S.add(constraint)


def is_ill_typed(S: set[tuple[TpVar, Type]]):
    # look for (t -> t' = int) in S
    for left, right in S:
        if right == IntTp() and isinstance(left, Func):
            print(f'Found {left} = {right}; ill-typed')
            return True

    return False


canonicalizing = set()


def canonicalize(S: set[tuple[Type, Type]], type: Type) -> Type:
    global canonicalizing
    if type in canonicalizing:
        raise TypecheckingError("infinite")
    canonicalizing.add(type)
    def get_type():
        match type:
            case IntTp():
                return type
            case Func(a=a, b=b):
                return Func(canonicalize(S, a), canonicalize(S, b))
            case TpVar(s=s):
                equivs = [right for left, right in S if left == type]
                for t in equivs:
                    if not isinstance(t, TpVar):
                        return t
                for t in equivs:
                    assert isinstance(t, TpVar)
                    if t.s < s:
                        return t
                return type
        raise ValueError(type)

    t = get_type()
    canonicalizing.remove(type)
    return t
