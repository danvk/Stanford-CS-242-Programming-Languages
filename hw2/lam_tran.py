import src.lam as lam
import src.ski as ski

##########
# PART 3 #
##########
# TASK: Implement the below function `tran`.
# You can define helper functions outside `tran` and use them inside `tran`.

def tran(e: lam.Expr) -> ski.Expr:
    # BEGIN_YOUR_CODE
    return tran_t(e)
    # END_YOUR_CODE


def tran_t(e: lam.Expr) -> ski.Expr:
    match e:
        case lam.Var(s=s):
            return ski.Var(s)
        case lam.Lam(s=s, e=e):
            return tran_u(s, tran_t(e))
        case lam.App(e1=e1, e2=e2):
            return ski.App(tran_t(e1), tran_t(e2))
    raise ValueError(e)


def tran_u(var: str, e: ski.Expr) -> ski.Expr:
    match e:
        case ski.S():  # Do I have to instantiate a ski.S() here to pattern match?
            return ski.App(ski.K(), ski.S())
        case ski.K():
            return ski.App(ski.K(), ski.K())
        case ski.I():
            return ski.App(ski.K(), ski.I())
        case ski.Var(s=s) if s == var:
            return ski.I()
        case ski.Var(s=s) if s != var:
            return ski.App(ski.K(), ski.Var(s))
        case ski.App(e1=e1, e2=e2):
            return ski.App(ski.App(ski.S(), tran_u(var, e1)), tran_u(var, e2))
    raise ValueError(e)
