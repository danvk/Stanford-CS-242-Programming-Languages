
from src.lam import CONSTS, App, Expr, Func, IntConst, IntTp, Lam, Prog, TpVar, Type, TypecheckingError, Var
from typing import List

def typecheck(prog: Prog) -> List[Type]:
    S = gen_constraints_prog(prog)
    print(S)
    print(type_constraints)
    # S = saturate(S)
    # if is_ill_typed(S):
    #     raise TypecheckingError("ill-typed")
    # if is_infinite(S):
    #     raise TypecheckingError("infinite")

    # C = canonicalize(S)
    # If there are no type errors, return a list of Types
    # Otherwise,
    raise TypecheckingError('not implemented')


n = -1
def get_fresh_type():
    global n
    n += 1
    return TpVar(f'a{n}')


type_constraints: set[tuple[TpVar, Func]] = set()


def gen_constraints(A: dict[str, Type], e: Expr) -> Type:
    match e:
        case Var(s=s) if s in A:
            return A[s]
        case Var(s=s) if s in CONSTS:
            return CONSTS[s]
        case Var(s=s):
            # free variable
            raise KeyError(s)
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
