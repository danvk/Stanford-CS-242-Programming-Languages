import src.ski as ski

##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.

should_abstract = False

def eval(e: ski.Expr, rewrite_limit=None) -> ski.Expr:
    # BEGIN_YOUR_CODE
    # print(e)
    seen = {str(e)}
    count = 0
    while True:
        e = rewrite_one(e)
        s = str(e)
        if s in seen:  # protects against infinite rewrite loops
            # print('  done')
            break
        seen.add(s)
        count += 1
        if rewrite_limit and count > rewrite_limit:
            print('infinite loop!')
            break
        # print('  -> ', e)

    if should_abstract:
        ea = e
        vars = get_vars(ea)
        if vars == {'x', 'y'} or vars == {'n'} or vars == {'x'}:
            while vars:
                var = list(vars)[0]
                vars.remove(var)
                abstracted = abstract(ea, var)
                print('  A(', str(ea), f', {var}) = ', str(abstracted))
                ea = abstracted

    return e
    # END_YOUR_CODE


def rewrite_one(e: ski.Expr) -> ski.Expr:
    if isinstance(e, ski.App):
        return rewrite_app(e)
    return e


def rewrite_app(app: ski.App) -> ski.Expr:
    e1 = rewrite_one(app.e1)
    e2 = rewrite_one(app.e2)
    if isinstance(e1, ski.I):
        return e2
    elif isinstance(e1, ski.App):
        if isinstance(e1.e1, ski.K):
            return e1.e2
        elif isinstance(e1.e1, ski.App):
            if isinstance(e1.e1.e1, ski.S):
                return rewrite_s(e1.e1.e2, e1.e2, e2)

    return ski.App(e1, e2)


def rewrite_s(e1: ski.Expr, e2: ski.Expr, e3: ski.Expr) -> ski.Expr:
    return ski.App(
        ski.App(e1, e3),
        ski.App(e2, e3),
    )

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
        match e:
            case ski.Var(s=s):
                stack.append(s)
            case ski.S():
                stack.append('S')
            case ski.K():
                stack.append('K')
            case ski.I():
                stack.append('I')
            case ski.App(e1=e1, e2=e2):
                stack.append(')')
                stack.append(e2)
                stack.append(e1)
                stack.append('(')

    return ' '.join(out).replace('( ', '(').replace(' )', ')')

