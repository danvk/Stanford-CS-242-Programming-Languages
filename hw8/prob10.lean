-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus

-- e1: (1+1) + 1^
def e1 : Expr :=
  Expr.Op Op.Add
    (Expr.Op Op.Add (Expr.Num 1) (Expr.Num 1))
    (Expr.Var 1)

-- e2: 2 + 1^
def e2 : Expr :=
  Expr.Op Op.Add
    (Expr.Num 2)
    (Expr.Var 1)

lemma type_preserve_nonexample :
  (e1 ↦ e2) ∧ ¬(typnat 0 e1) ∧ ¬(typnat 0 e2) :=
begin
  split,
  {
    apply eval.ELeft,
    apply eval.EOp,
  },
  split,
  -- The proofs for ¬(typnat 0 e1) and ¬(typnat 0 e2) are identical
  repeat {
    assume tn0,
    cases tn0,
    rename tn0_ᾰ_1 → badvar,
    cases badvar,  -- have 1 < 0, want to prove false
    apply nat.not_succ_le_zero 0,
    apply le_of_lt,
    assumption,
  }
end
