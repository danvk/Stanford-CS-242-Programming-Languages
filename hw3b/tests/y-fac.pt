# Bool
def tt   = \x.\y. x;
def ff   = \x.\y. y;

# Numeral
def inc  = \n.\f.\x. f (n f x);
def _0   = \f.\x. x;
def _1   = inc _0;
def _2   = inc _1;
def _3   = inc _2;
def _4   = inc _3;

# Pair
def pair = \x.\y.\f. f x y;
def fst  = \p. p tt;
def snd  = \p. p ff;

def plus1 = \n. + 1 n;

# acc = (n, n!)
def fac_help = \acc. pair (plus1 (fst acc)) (* (plus1 (fst acc)) (snd acc));
def fac      = \n. snd (n fac_help (pair 0 1));

# should have int types.
def r1 = fac _0;
def r1 = fac _1;
def r2 = fac _2;
def r6 = fac _3;
def r24 = fac _4;
