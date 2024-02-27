import src.ski as ski

##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.

def eval(e: ski.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    # print(e)
    last = e  # str(e)  # seen = {str(e)}
    while True:
        e = rewrite_one(e)
        # s = str(e)
        if last == e:  # protects against infinite rewrite loops
            # print('  done')
            break
        last = e
        # seen.add(s)
        # print('  -> ', e)

    return e
    # END_YOUR_CODE


def rewrite_one(e: ski.Expr) -> ski.Expr:
    if isinstance(e, ski.App):
        return rewrite_app(e)
    return e


def rewrite_app(app: ski.App) -> ski.Expr:
    if isinstance(app.e1, ski.I):
        return app.e2
    elif isinstance(app.e1, ski.App):
        if isinstance(app.e1.e1, ski.K):
            return app.e1.e2
        elif isinstance(app.e1.e1, ski.App):
            if isinstance(app.e1.e1.e1, ski.S):
                return rewrite_s(app.e1.e1.e2, app.e1.e2, app.e2)

    e1 = rewrite_one(app.e1)
    e2 = rewrite_one(app.e2)
    if e1 == app.e1 and e2 == app.e2:
        return app
    else:
        return ski.App(e1, e2)


def rewrite_s(e1: ski.Expr, e2: ski.Expr, e3: ski.Expr) -> ski.Expr:
    return ski.App(
        ski.App(e1, e3),
        ski.App(e2, e3),
    )
