-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

import .prob06

-- (1*2) + (4/2) ↦* 4

def a := Expr.Op Op.Mul (Expr.Num 1) (Expr.Num 2)
def b := Expr.Op Op.Div (Expr.Num 4) (Expr.Num 2)

def e1 := Expr.Op Op.Add a b

def e2 := Expr.Num 4

lemma evals_example :
  (val e2) ∧ (e1 ↦* e2) :=
begin
  split,
  apply val.VNum,
  transitivity, -- Expr.Op Op.Add (Expr.Num 2) b,
  {
    apply small_to_big,
    apply eval.ELeft,
    apply eval.EOp,
  },
  transitivity, -- Expr.Op Op.Add (Expr.Num 2) (Expr.Num 2),
  {
    apply small_to_big,
    apply eval.ERight,
    apply eval.EOp,
    apply val.VNum,
  },
  apply small_to_big,
  apply eval.EOp,
end
