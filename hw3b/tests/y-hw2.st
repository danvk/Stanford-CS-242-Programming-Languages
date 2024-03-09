
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

# List
def cons = \h.\t.\f.\x. f h (t f x);
def nil  = \f.\x. x;

##########
# PART 4 #
##########
# TASK: Implement the following functions.

# BEGIN_YOUR_CODE
def is_zero  = \n. n (\z. ff) tt;
def len      = \l. l (\z. inc) _0;
def num_zero = \l. l (\el. \acc. (is_zero el) (inc acc) acc) _0;

# helpers
def add      = \m.\n. m inc n;
def not      = \b. b ff tt;
def value    = \n. n (+ 1) 0;

# END_YOUR_CODE

#########
# TESTS #
#########
# NOTE: Expected outputs are given as comments on each line.

def section_is_zero = 0;
def r1 = (is_zero _0) 1 0;
def r0 = (is_zero _1) 1 0;
def r0 = (is_zero _2) 1 0;
def r0 = (is_zero _3) 1 0;

def section_len = 0;
def r0 = value (len nil);
def r1 = value (len (cons tt nil));
def r2 = value (len (cons tt (cons ff nil)));
def r3 = value (len (cons tt (cons ff (cons tt nil))));
