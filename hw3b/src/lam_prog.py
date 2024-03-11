from collections import namedtuple
from lark import Transformer
from typing import List

import src.lam as lam

# Convert Tree to Prog.
class TreeToProg(Transformer):
    # start
    def start(self, items): return lam.Prog(*items)
    def defn(self, items): return lam.Defn(*items)

    def defns(self, items): return items
    def exprs(self, items): return items

    def IDENT(self, s): return str(s)
    def NUMBER(self, s): return int(s)

    def app(self, items): return lam.App(*items)
    def var(self, items):
        if items[0] == 'true':
            return lam.BoolConst(True)
        elif items[0] == 'false':
            return lam.BoolConst(False)
        return lam.Var(*items)
    def lam(self, items):
        if items[0] in lam.CONSTS: raise ValueError("Can't use {} as variable".format(items[0]))
        return lam.Lam(*items)
    def num(self, items): return lam.IntConst(int(items[0]))
    def let(self, items):
        if items[0] in lam.CONSTS: raise ValueError("Can't use {} as variable".format(items[0]))
        return lam.Let(*items)
