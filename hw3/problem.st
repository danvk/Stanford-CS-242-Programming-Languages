
def inc = \n.\f.\z. f (n f z);  # ((int -> int) -> int -> int) -> (int -> int) -> int -> int
def _0 = \f.\z. z;  # (int -> int) -> int -> int
def _1 = inc _0;    # (int -> int) -> int -> int
def _2 = inc _1;    # (int -> int) -> int -> int

# Should return a church encoding of the sum of n and m
# Must have:
# z: int
# f: int -> int
# So we can't use inc with the church-encoded z=_0.
def sum = \n. \m. \f. \z. n f (m f z);

# Should take a church encoded number and produce a regular int.
def value = \n. n (\x. + x 1) 0;

# Should take two ints x y and produce 1 if x is divisible by y, 0 otherwise
def is_div = \x. \y. ifz (- x (* (/ x y) y)) 1 0;

def v1 = value _1;
def v2 = value _2;
def v3 = value (sum _2 _1);
def v4 = value (sum _2 _2);
def v5 = value (sum (sum _2 _1) _2);

def t1 = is_div 6 (value _2);
def f1 = is_div 4 3;
def t2 = is_div 1 1;
def f2 = is_div 9 8;
