#!/usr/bin/env python
"""Enumerate all SKI expressions to find the shortest one with some behavior."""

import itertools
import time
from pathlib import Path

from lark import Lark

from src import ski, ski_prog
import ski_eval

ski_syntax = Path('./src/ski_prog.lark').read_text()
ski_parser = Lark(ski_syntax, start='expr', parser='lalr')

ski_var = ski.Var('x')

def trees(n: int):
    """Return a list of all binary trees with n elements.

    A binary tree is represented as a tuple. This returns a list of tuples.
    A "1" appears wherever a value would go. An empty subtree is None.
    """
    if n == 0:
        return []
    if n == 1:
        return [ski_var]
    result = []
    for i in range(1, n):
        left = i
        right = n - i
        result += [
            ski.App(l, r) for l, r in itertools.product(trees(left), trees(right))
        ]
    return result


def all_combinators(expr: ski.Expr):
    """Replace each var with every possible combinator in expr, yielding new expressions."""
    match expr:
        case ski.Var():
            yield ski.I()
            yield ski.K()
            yield ski.S()
        case ski.App(e1=left, e2=right):
            yield from (
                ski.App(l, r)
                for l, r in itertools.product(
                    all_combinators(left),
                    all_combinators(right)
                )
            )
        case _:
            yield expr

S = ski.S()
K = ski.K()
App = ski.App

def parse_ski(s: str) -> ski.Expr:
    tree = ski_parser.parse(s)
    return ski_prog.TreeToProg().transform(tree)

tt = parse_ski('K')
ff = parse_ski('S K')
xx = ski.Var('x')
yy = ski.Var('y')
ski_0 = parse_ski('S K')
ski_inc = parse_ski('S (S (K S) K)')
ski_1 = App(ski_inc, ski_0)
ski_2 = App(ski_inc, ski_1)
ski_3 = App(ski_inc, ski_2)

expr_var = ski.Var('expr')

def subst(expr: ski.Expr, var: ski.Var, val: ski.Expr) -> ski.Expr:
    match expr:
        case ski.Var(s=s) if s==var.s:
            return val
        case ski.App(e1=left, e2=right):
            return ski.App(subst(left, var, val), subst(right, var, val))
        case _:
            return expr


ski_vars = {
    'tt': tt,
    'ff': ff,
    'inc': ski_inc,
    '_0': ski_0,
    '_1': ski_1,
    '_2': ski_2,
    '_3': ski_3,
}

def ski_expr(s: str) -> ski.Expr:
    """Parse a SKI expression and fill in known symbols."""
    e = parse_ski(s)
    for name, val in ski_vars.items():
        e = subst(e, ski.Var(name), val)
    return e


or_cases = [
    (ski_expr('(expr tt tt) x y'), xx),
    (ski_expr('(expr tt ff) x y'), xx),
    (ski_expr('(expr ff tt) x y'), xx),
    (ski_expr('(expr ff ff) x y'), yy),
]

and_cases = [
    (ski_expr('(expr tt tt) x y'), xx),
    (ski_expr('(expr tt ff) x y'), yy),
    (ski_expr('(expr ff tt) x y'), yy),
    (ski_expr('(expr ff ff) x y'), yy),
]

not_cases = [
    (ski_expr('(expr tt) x y'), yy),
    (ski_expr('(expr ff) x y'), xx),
]

is_odd_cases = [
    (ski_expr('(expr _0) x y'), yy),
    (ski_expr('(expr _1) x y'), xx),
    (ski_expr('(expr _2) x y'), yy),
    (ski_expr('(expr _3) x y'), xx),
]

all_cases = [
    ('or', or_cases),
    ('and', and_cases),
    ('not', not_cases),
    ('is_odd', is_odd_cases),
]


def find_minimal_expression(cases):
    start_secs = time.time()
    for n in range(10):
        all_forms = [*trees(n)]
        for i, tree in enumerate(all_forms):
            elapsed_secs = time.time() - start_secs
            print(f'{n=} {i} / {len(all_forms)}: {tree} {elapsed_secs:.1f} secs')
            for expr in all_combinators(tree):
                # print(f'  {expr}')
                failed = False
                for template, expected in cases:
                    e = subst(template, expr_var, expr)
                    result = ski_eval.eval(e, rewrite_limit=20, size_limit=300)
                    if isinstance(result, str):
                        s = ski_eval.format_compact(expr)
                        print(f'    {result}: {s}')
                    if result != expected:
                        failed = True
                        # print(f'    {e} -> {result} != {expected}')
                        break
                if not failed:
                    s = ski_eval.format_compact(expr)
                    print(f'We have a winner! {n=} {elapsed_secs:.1f}\n{s}')
                    return True
    return False


for fn_name, cases in all_cases:
    print(f'\n\n--- {fn_name} ----')
    find_minimal_expression(cases)
