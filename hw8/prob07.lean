-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

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
  apply evals.CStep,
  show Expr, from Expr.Op Op.Add (Expr.Num 2) b,
  {
    -- (1*2) + (4/2) ↦ 2 + (4/2)
    apply eval.ELeft,
    apply eval.EOp,
  },
  apply evals.CStep,
  show Expr, from Expr.Op Op.Add (Expr.Num 2) (Expr.Num 2),
  {
    -- 2 + (4/2) ↦ 2 + 2
    apply eval.ERight,
    apply eval.EOp,
    apply val.VNum,
  },
  apply evals.CStep,
  show Expr, from Expr.Num 4,
  -- 2 + 2 ↦ 4
  apply eval.EOp,
  apply evals.CRefl,
end
