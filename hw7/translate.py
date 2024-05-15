import src.lam as lam
import src.pi as pi


var_counter = 0

def get_fresh_var(prefix: str):
    global var_counter
    n = var_counter
    var_counter += 1
    return f'_{prefix}{n}'


PI0 = pi.Parallel([])

# notation:
# T(x, f) := \overline x f . 0
# \overline a x . P = send a message x on channel a, then P
#                   = x -> c . P

# f is the result channel
def translate(e: lam.Expr, channel: str) -> pi.Proc:
    match e:
        case lam.Var(s=x):
            # T(x, f) := \overline x f . 0 := x -> c. P
            return pi.Send(channel, x, PI0)

        case lam.Lam(s=x, e=m):
            # T(λx.M, f) := f(x).f(u).T(M, u)
            #            := (x <- f).(u <- f).T(M, u)
            u = get_fresh_var('u')
            return pi.Receive(x, channel, pi.Receive(u, channel, translate(m, u)))

        case lam.App(e1=m, e2=n):
            # T (M N,f) := νc.νd. (T (M,c) | cd.cf.0 | !d(v).T (N,v))
            c = get_fresh_var('c')
            d = get_fresh_var('d')
            v = get_fresh_var('v')
            return pi.Nu(c, pi.Nu(d, pi.Parallel((
                translate(m, c),
                pi.Send(d, c, pi.Send(channel, c, PI0)),
                pi.Replicate(pi.Receive(v, d, translate(n, v)))
            ))))

    raise ValueError(e)
