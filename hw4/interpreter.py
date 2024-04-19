import src.objc as objc
from typing import Optional, Set


# free_vars_method is a helper function for the implementation
# of subst that collects all free variables in a method.
def free_vars_method(f: objc.Method) -> Set[objc.Var]:
    fv = free_vars(f.body)
    fv.discard(f.var)
    return fv

# free_vars is a helper function for the implementation of
# subst that collects all free variables present in an expression.
def free_vars(e: objc.Expr) -> Set[objc.Var]:
    match e:
        case objc.Var():
            return {e}
        case objc.FieldAccess():
            return free_vars(e.expr)
        case objc.Object():
            return {
                var
                for m in e.fields.values()
                for var in free_vars_method(m)
            }
        case objc.MethodOverride():
            return free_vars(e.expr).union(free_vars_method(e.method))

    print(e, type(e))
    raise ValueError(e)

# subset_method substitutes expressions for variables within
# a method.
def subst_method(f: objc.Method, x: objc.Var, e: objc.Expr) -> objc.Method:
    fv = free_vars_method(f).union({x}).union(free_vars(e))
    i = 0
    while True:
        y = objc.Var(f.var.name + str(i))
        if y not in fv:
            break
        i += 1
    return objc.Method(
        var=y,
        body=subst(subst(f.body, f.var, y), x, e)
    )

# subst implements substitution of variables into expressions. In particular,
# subst(e1, x, e2) substitutes e2 for x in e1, written as e1{x := e2}.
def subst(e1: objc.Expr, x: objc.Var, e2: objc.Expr) -> objc.Expr:
    match e1:
        case objc.Var():
            return e2 if e1 == x else e1
        case objc.FieldAccess(expr=e, field=field):
            return objc.FieldAccess(expr=subst(e, x, e2), field=field)
        case objc.Object(fields=fields):
            return objc.Object([
                [field, subst_method(method, x, e2)] for field, method in fields.items()
            ])
        case objc.MethodOverride(expr=e, field=field, method=method):
            return objc.MethodOverride(
                expr=subst(e, x, e2),
                field=field,
                method=subst_method(method, x, e2)
            )

# try_step implements the small-step operational semantics for the
# object calculus. try_step takes an expression e and returns None
# if the expression cannot take a step, or e', where e -> e' in one
# step.
def try_step(e: objc.Expr) -> Optional[objc.Expr]:
    match e:
        case objc.Object():
            return None  # An object is a concrete value that cannot take any steps.
        case objc.Var():
            return None
        case objc.FieldAccess(expr=expr, field=field):
            # Field-Access-Step
            ep = try_step(expr)
            if ep:
                return objc.FieldAccess(expr=ep, field=field)
            # Field-Access-Eval
            assert isinstance(expr, objc.Object)
            method: objc.Method = expr.fields[field]
            return subst(method.body, method.var, expr)
        case objc.MethodOverride(expr=expr, field=field, method=method):
            # Override-Step
            ep = try_step(expr)
            if ep:
                return objc.MethodOverride(expr=ep, field=field, method=method)
            # Override-Eval
            assert isinstance(expr, objc.Object)
            return objc.Object([
                [f, m] for f, m in expr.fields.items() if f != field
            ] + [[field, method]])
