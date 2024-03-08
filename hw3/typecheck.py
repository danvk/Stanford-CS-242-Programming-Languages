
from src.lam import CONSTS, App, Expr, Func, IntConst, IntTp, Lam, PolymorphicType, Prog, QuantifiedType, TpVar, Type, TypecheckingError, Var
from typing import List

def typecheck(prog: Prog) -> List[Type]:
    A = get_prog_env(prog)

    # for s, t in A.items():
    #     print(f'{s}: {t}')

    types = [*A.values()]
    return types


n = -1
def get_fresh_type():
    global n
    n += 1
    return TpVar(f'a{n}')


def get_type_and_constraints(
    A: dict[str, PolymorphicType],
    e: Expr,
    S: set[tuple[Type, Type]],
) -> Type:
    """Get the type of e according to the environment A.

    This may return a fresh type variable if doesn't have a type in A.
    S is an output variable of constraints.
    """
    match e:
        case Var(s=s) if s in CONSTS:
            return CONSTS[s]
        case Var(s=s) if s in A:
            t = A[s]
            match t:
                case QuantifiedType(vars=vars, o=o):
                    # Create a fresh type variable for each of vars
                    for var in vars:
                        o = subst_type(o, var, get_fresh_type())
                    return o
                case _:
                    return t
        case Var(s=s):
            # free variable
            raise TypecheckingError(f'undefined variable {s}')
        case IntConst():
            return IntTp()
        case Lam(s=s, e=e):
            alpha = get_fresh_type()
            t = get_type_and_constraints({**A, s: alpha}, e, S)
            return Func(alpha, t)
        case App(e1=e1, e2=e2):
            beta = get_fresh_type()
            tau = get_type_and_constraints(A, e1, S)
            tau_p = get_type_and_constraints(A, e2, S)
            S.add((tau, Func(tau_p, beta)))
            return beta


def get_prog_env(prog: Prog):
    """Gather the environment and constraints for a program."""
    global n
    n = -1
    A = {}
    for defn in prog.defns:
        S = set()
        t = get_type_and_constraints(A, defn.e, S)
        saturate(S)
        check_ill_typed(S)
        t = canonicalize(S, t)
        o = generalize(A, t)
        A[defn.s] = o
        assert len(canonicalizing) == 0, f'{canonicalizing=}'
    return A


def saturate(S: set[tuple[TpVar, Type]]):
    """Saturate a set of constraints in-place."""
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
    """Look for (t -> t' = int) in S and throw if it's found."""
    for left, right in S:
        if right == IntTp() and isinstance(left, Func):
            raise TypecheckingError(f'ill-typed: Found {left} = {right}')


canonicalizing = set()


def canonicalize(S: set[tuple[Type, Type]], type: Type) -> Type:
    """Get the canonical form of the type according to a saturated set of constraints.

    Throws if the type is infinite.
    """
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


def get_polymorphic_type_var(i: int) -> TpVar:
    c = chr(ord('a') + i)
    return TpVar(f"'{c}")


def generalize(env: dict[TpVar, PolymorphicType], type: Type) -> PolymorphicType:
    fv = free_vars(env)
    vars = [v for v in all_vars_in_order(type) if v not in fv]
    if vars:
        o = type
        pvars = set()
        for i, var in enumerate(vars):
            pv = get_polymorphic_type_var(i)
            o = subst_type(o, var, pv)
            pvars.add(pv)
        return QuantifiedType(vars=pvars, o=o)
    return type


def free_vars(env_or_type: dict[TpVar, PolymorphicType] | PolymorphicType) -> set[TpVar]:
    if isinstance(env_or_type, dict):
        out = set()
        for x, t in env_or_type.items():
            out.update(free_vars(t))
        return out
    match env_or_type:
        case IntTp():
            return set()
        case Func(a=a, b=b):
            return free_vars(a).union(free_vars(b))
        case TpVar() as t:
            return set([t])
        case QuantifiedType(vars=vars, o=o):
            return free_vars(o).difference(vars)


def all_vars(type: Type) -> set[TpVar]:
    """Find all type variables mentioned in a Type."""
    match type:
        case IntTp():
            return set()
        case TpVar():
            return {type}
        case Func(a=a, b=b):
            return all_vars(a).union(all_vars(b))
    raise ValueError(type)


def all_vars_in_order(type: Type) -> list[TpVar]:
    match type:
        case IntTp():
            return []
        case TpVar():
            return [type]
        case Func(a=a, b=b):
            vars = all_vars_in_order(a)
            vars_b = all_vars_in_order(b)
            return vars + [v for v in vars_b if v not in vars]
    raise ValueError(type)


def subst_type(type: Type, old: TpVar, new: TpVar) -> Type:
    match type:
        case TpVar():
            return new if type == old else type
        case IntTp():
            return type
        case Func(a=a, b=b):
            return Func(subst_type(a, old, new), subst_type(b, old, new))

    raise ValueError(type)
