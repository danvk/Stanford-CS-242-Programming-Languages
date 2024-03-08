#!/usr/bin/env python

import itertools
from src import ski
import ski_eval

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
        result += [ski.App(l, r) for l, r in itertools.product(trees(left), trees(right))]
    return result


def all_combinators(expr: ski.Expr):
    """Replace each var with every possible combinator in expr, yielding new expressions."""
    match expr:
        case ski.Var():
            yield ski.S()
            yield ski.K()
            yield ski.I()
        case ski.App(e1=left, e2=right):
            yield from (ski.App(l, r) for l, r in itertools.product(all_combinators(left), all_combinators(right)))
        case _:
            yield expr

tt = ski.K()
ff = ski.App(ski.S(), ski.K())
xx = ski.Var('x')
yy = ski.Var('y')
expr_var = ski.Var('expr')

def subst(expr: ski.Expr, var: ski.Var, val: ski.Expr) -> ski.Expr:
    match expr:
        case ski.Var(s=s) if s==var.s:
            return val
        case ski.App(e1=left, e2=right):
            return ski.App(subst(left, var, val), subst(right, var, val))
        case _:
            return expr


or_cases = [
    (ski.App(ski.App(ski.App(ski.App(expr_var, tt), tt), xx), yy), xx),
    (ski.App(ski.App(ski.App(ski.App(expr_var, tt), ff), xx), yy), xx),
    (ski.App(ski.App(ski.App(ski.App(expr_var, ff), tt), xx), yy), xx),
    (ski.App(ski.App(ski.App(ski.App(expr_var, ff), ff), xx), yy), yy),
]

and_cases = [
    (ski.App(ski.App(ski.App(ski.App(expr_var, tt), tt), xx), yy), xx),
    (ski.App(ski.App(ski.App(ski.App(expr_var, tt), ff), xx), yy), yy),
    (ski.App(ski.App(ski.App(ski.App(expr_var, ff), tt), xx), yy), yy),
    (ski.App(ski.App(ski.App(ski.App(expr_var, ff), ff), xx), yy), yy),
]

not_cases = [
    (ski.App(ski.App(ski.App(expr_var, tt), xx), yy), yy),
    (ski.App(ski.App(ski.App(expr_var, ff), xx), yy), xx),
]


S = ski.S()
K = ski.K()
App = ski.App
ski_0 = App(S, K)
ski_inc = App(S, App(App(S, App(K, S)), K))
ski_1 = App(ski_inc, ski_0)
ski_2 = App(ski_inc, ski_1)
ski_3 = App(ski_inc, ski_2)

is_odd_cases = [
    (App(App(App(expr_var, ski_0), xx), yy), yy),
    (App(App(App(expr_var, ski_1), xx), yy), xx),
    (App(App(App(expr_var, ski_2), xx), yy), yy),
    (App(App(App(expr_var, ski_3), xx), yy), xx),
]

# Rhea's solutions (found by hand -- more concise!):
# def or = S I (K tt);
# def and = S S K;
# def not = S (S I (K ff)) (K tt);
# def is_odd = S (S I (K not)) (K ff);

cases = not_cases

have_winner = False
for n in range(10):
    for tree in trees(n):
        print(f'{tree}')
        for expr in all_combinators(tree):
            print(f'  {expr}')
            failed = False
            for template, expected in cases:
                e = subst(template, expr_var, expr)
                result = ski_eval.eval(e, rewrite_limit=20)
                if result != expected:
                    failed = True
                    # print(f'    {e} -> {result} != {expected}')
                    break
            if not failed:
                have_winner = True
                print(f'We have a winner! {n=}\n{expr}')
                break
        if have_winner:
            break
    if have_winner:
        break
