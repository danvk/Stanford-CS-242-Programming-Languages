-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

-- If e1 ↦∗ e1', then (e1 ⊛ e2) ↦∗ (e1' ⊛ e2)
-- - CRefl: If e1 == e1', then this is trivial
-- - CStep:

lemma transitive_left (op : Op) (e1 e1' e2 : Expr) :
  (e1 ↦* e1')
  → (Expr.Op op e1 e2 ↦* Expr.Op op e1' e2) :=
begin
  intros h1,
  induction h1,
  -- why can't I use case CRefl here? CRefl
  case evals.CRefl : e {

  },
  case evals.CStep : e emid e' {

  }
end
