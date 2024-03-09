# Well-typed

def cons = \h.\t.\f.\x. f h (t f x);
def nil = \f.\x. x;
def sum = \l. l (\h.\x. ifz h x (+ h x)) 0;
def ls = cons 3 (cons 0 (cons 2 nil));
def result = sum ls;
