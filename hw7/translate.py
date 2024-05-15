import src.lam as lam
import src.pi as pi


var_counter = 0

def get_fresh_var():
    global var_counter
    n = var_counter
    var_counter += 1
    return f'_c{n}'


PI0 = pi.Parallel([])

# notation:
# T(x, f) := \overline x f . 0
# \overline a x . P = send a message x on channel a, then P
#                   = x -> c . P


# f is the result channel
def translate(e: lam.Expr, channel: str) -> pi.Proc:
    print(f'{e=}, {channel=}')
    match e:
        case lam.Var(s=x):
            # T(x, f) := \overline x f . 0 := x -> c. P
            return pi.Send(channel, x, PI0)

        case lam.Lam(s=x, e=m):
            # T(λx.M, f) := f(x).f(u).T(M, u)
            #            := (x <- f).(u <- f).T(M, u)
            u = get_fresh_var()
            return pi.Receive(x, channel, pi.Receive(u, channel, translate(m, channel)))

        case lam.App(e1=m, e2=n):
            # T (M N,f) := νc.νd. (T (M,c) | cd.cf.0 | !d(v).T (N,v))
            c = get_fresh_var()
            d = get_fresh_var()
            v = get_fresh_var()
            return pi.Nu(c, pi.Nu(d, pi.Parallel((
                translate(m, c),
                pi.Send(c, d, pi.Send(c, channel, PI0)),
                pi.Replicate(pi.Receive(v, d, translate(n, v)))
            ))))

    raise ValueError(e)
