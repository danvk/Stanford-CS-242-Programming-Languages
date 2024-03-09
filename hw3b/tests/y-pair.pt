def pair = \x.\y.\f. f x y;
def fst  = \p. p (\x.\y.x);
def snd  = \p. p (\x.\y.y);
def p = pair 2 0;
def q = ifz (snd p) (fst p) (snd p);