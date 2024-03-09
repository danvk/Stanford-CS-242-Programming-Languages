def cons = \h.\t.\f.\x. f h (t f x);
def nil = \f.\x. x;

# def inc = \n.\f.\z. f (n f z);  # ((int -> int) -> int -> int) -> (int -> int) -> int -> int
# def _0 = \f.\z. z;  # (int -> int) -> int -> int
# def _1 = inc _0;    # (int -> int) -> int -> int
# def _2 = inc _1;    # (int -> int) -> int -> int

# def value: ((int -> int) -> int -> a11) -> a11
# (this is correct)
def value = \n. n (+ 1) 0;

# let double f x = f (f x);;
# val double : ('a -> 'a) -> 'a -> 'a = <fun>
# def double = \f. \x. f (f x);
# def s = \x. \y. \z. (x z) (y z);
