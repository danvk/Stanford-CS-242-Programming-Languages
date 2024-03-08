import src.ski as ski

##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.

def eval(e: ski.Expr, rewrite_limit=None, size_limit=1000) -> ski.Expr:
    # BEGIN_YOUR_CODE
    # print(e)
    # last = e  # str(e)  # seen = {str(e)}
    seen = {format_non_rec(e)}
    count = 0
    while True:
        changed, e = rewrite_one(e)
        if not changed:
            # print('  done')
            break
        count += 1
        if rewrite_limit and count > rewrite_limit:
            return 'infinite loop!'
        s = format_non_rec(e)
        if s in seen:  # protects against infinite rewrite loops
            # print('  done')
            break
        if size_limit and len(s) > size_limit:
            return f'too long {len(s)}'
        seen.add(s)
        # print('  -> ', e)

    return e
    # END_YOUR_CODE


def rewrite_one(e: ski.Expr) -> tuple[bool, ski.Expr]:
    if isinstance(e, ski.App):
        return rewrite_app(e)
    return False, e


def rewrite_app(app: ski.App) -> tuple[bool, ski.Expr]:
    change_e1, e1 = rewrite_one(app.e1)
    change_e2, e2 = rewrite_one(app.e2)
    changed = change_e1 or change_e2
    if isinstance(e1, ski.I):
        return True, e2
    elif isinstance(e1, ski.App):
        if isinstance(e1.e1, ski.K):
            return True, e1.e2
        elif isinstance(e1.e1, ski.App):
            if isinstance(e1.e1.e1, ski.S):
                se1 = e1.e1.e2
                se2 = e1.e2
                se3 = e2
                # We can't do this because app.e1 may be referenced elsewhere
                # app.e1.e1 = se1
                # app.e1.e2 = se3
                # app.e1 = ski.App(se1, se3)
                # app.e2 = ski.App(se2, se3)
                # return True, app
                return True, ski.App(ski.App(se1, se3), ski.App(se2, se3))
    if not changed:
        return False, app
    return changed, ski.App(e1, e2)


# K e1 e2   = ((K e1) e2)     = e2
# S e1 e2 e3 = (((S e1) e2) e3) = (e1 e3) (e2 e3)

#    S K x y
# -> (K y) (x y)
# -> y

# A(E1 E2, x) = S A(E1, x) A(E2, x)
# A(E1 E2, x) x = E1 E2 by definition
#    S A(E1, x) A(E2, x) x
# -> (A(E1, x) x) (A(E2, x) x)
# -> E1 E2

def get_vars(e: ski.Expr) -> set[str]:
    if isinstance(e, ski.App):
        return get_vars(e.e1).union(get_vars(e.e2))
    elif isinstance(e, ski.Var):
        return {e.s}
    else:
        return set()

def contains_ref(e: ski.Expr, var: str) -> bool:
    if isinstance(e, ski.App):
        return contains_ref(e.e1, var) or contains_ref(e.e2, var)
    elif isinstance(e, ski.Var):
        if e.s == var:
            return True
        else:
            return False
    else:
        return False


def abstract(e: ski.Expr, var: str) -> ski.Expr:
    if not contains_ref(e, var):
        return ski.App(ski.K(), e)
    elif isinstance(e, ski.App):
        return ski.App(ski.App(ski.S(), abstract(e.e1, var)), abstract(e.e2, var))
    elif isinstance(e, ski.Var):
        if e.s == var:
            return ski.I()
    else:
        return ski.App(ski.K(), e)


def format_non_rec(expr: ski.Expr) -> str:
    out: list[str] = []
    stack = [expr]
    while stack:
        e = stack.pop()
        if isinstance(e, str):
            out.append(e)
        elif isinstance(e, ski.App):
            stack.append(')')
            stack.append(e.e2)
            stack.append(e.e1)
            stack.append('(')
        else:
            stack.append(str(e))

    return ' '.join(out).replace('( ', '(').replace(' )', ')')


def format_compact(expr: ski.Expr) -> str:
    match expr:
        case ski.App(e1=e1, e2=e2):
            left = format_compact(e1)
            right = format_compact(e2)
            if isinstance(e2, ski.App):
                return f'{left} ({right})'
            else:
                return f'{left} {right}'
        case _:
            return str(expr)
