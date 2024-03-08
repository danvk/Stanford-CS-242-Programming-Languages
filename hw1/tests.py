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


def test_parse_and_print_compact():
    tree = ski_parser.parse('S (S I S) (K K)')
    prog = ski_prog.TreeToProg().transform(tree)
    assert ski_eval.format_non_rec(prog) == '((S ((S I) S)) (K K))'
