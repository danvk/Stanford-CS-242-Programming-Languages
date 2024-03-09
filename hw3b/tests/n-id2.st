# Ill-typed

# Id can't be both int -> int and (int -> int) -> (int -> int)
def id = \x. x;
def _ = id 0;
def _ = (id id) 0;