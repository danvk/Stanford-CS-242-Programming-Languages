import src.ski as ski

##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.

def eval(e: ski.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    # print(e)
    # last = e  # str(e)  # seen = {str(e)}
    while True:
        changed, e = rewrite_one(e)
        # s = str(e)
        if not changed:
            # print('  done')
            break
        # seen.add(s)
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
                return True, rewrite_s(e1.e1.e2, e1.e2, e2)

    app.e1 = e1
    app.e2 = e2
    return changed, app

def rewrite_s(e1: ski.Expr, e2: ski.Expr, e3: ski.Expr) -> ski.Expr:
    return ski.App(
        ski.App(e1, e3),
        ski.App(e2, e3),
    )
