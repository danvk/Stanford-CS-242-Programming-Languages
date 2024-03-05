
# Allow importing student code from parent directory (outside of ./src)
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path
from lark import Lark
import argparse

import src.lam_prog as lam_prog
import src.lam as lam
from src.eval import eval_lam

lam_syntax = Path('./src/lam_prog.lark').read_text()
lam_parser = Lark(lam_syntax, start='start', parser='lalr')
env = {}

def lam_to_prog(fname, type_check, execute, echo_name: bool = False):

    try:
        text = Path(fname).read_text()
    except Exception as err:
        print(">>>>> Error occured when reading: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # parse
    try:
        tree = lam_parser.parse(text)
        # print(tree.pretty())
    except Exception as err:
        print(">>>>> Syntax error occured when parsing: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # convert `tree` to `prog`.
    prog: lam.Prog = lam_prog.TreeToProg().transform(tree)
    # print(tree.pretty())
    # print(prog)
    if echo_name:
        print('---', fname, '---')

    # type-check
    if type_check:
        print("type-checking... ")
        from typecheck import typecheck
        try:
            types = typecheck(prog)
            if not isinstance(types, list) or len(types) != len(prog.defns):
                raise lam.TypecheckingError("Result types not of correct form")
            print("Typings:")
            for defn, tp in zip(prog.defns, types):
                print(f"def {defn.s}: {tp}")
            if os.path.basename(fname).startswith('n-'):
                print(f">>> Warning: file {fname} expected to fail typechecking, but typechecking succeeded <<<")

        except lam.TypecheckingError as e:
            print("Typechecking failed:", e)
            if os.path.basename(fname).startswith('y-'):
                print(f">>> Warning: file {fname} expected to typecheck, but typechecking failed <<<")
            execute = False
    # execute
    if execute:
        print("executing...")
        try:
            eval_lam(prog)
        except lam.TypecheckingError as e:
            print(f">>> Warning: file {fname} runtime produced an error: {e} <<<")




if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("input", nargs='+', type=str, help="file")
    argparser.add_argument("--no-type-check", dest='type_check', action='store_false', default=True, help="don't perform typechecking")
    argparser.add_argument("--no-execute", dest='execute', action='store_false', default=True, help="don't execute any expressions")
    args = argparser.parse_args()

    for i in args.input:
        lam_to_prog(i, args.type_check, args.execute, len(args.input) > 1)
