from pathlib import Path
from lark import Lark
import src.ski_prog as ski_prog
import ski_eval

ski_syntax = Path('./src/ski_prog.lark').read_text()
ski_parser = Lark(ski_syntax, start='expr', parser='lalr')


def test_parse_and_print():
    tree = ski_parser.parse('S (S I S) (K K)')
    prog = ski_prog.TreeToProg().transform(tree)
    assert f'{prog}' == '((S ((S I) S)) (K K))'


def test_parse_and_print_non_rec():
    tree = ski_parser.parse('S (S I S) (K K)')
    prog = ski_prog.TreeToProg().transform(tree)
    assert ski_eval.format_non_rec(prog) == '((S ((S I) S)) (K K))'


def parse_and_print(s: str) -> str:
    tree = ski_parser.parse(s)
    prog = ski_prog.TreeToProg().transform(tree)
    return ski_eval.format_compact(prog)


def test_parse_and_print_compact():
    assert parse_and_print('S (S I S) (K K)') == 'S (S I S) (K K)'
    # removes some unnecessary parens
    assert parse_and_print('S ((S I) (K not)) (K ff)') == 'S (S I (K not)) (K ff)'
    assert parse_and_print('((S ((S I) (K (S K)))) (K K))') == 'S (S I (K (S K))) (K K)'
