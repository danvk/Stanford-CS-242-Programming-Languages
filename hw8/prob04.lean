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
    -- Here we have e1 = e1' = e; this is an instance of CRefl
    apply evals.CRefl,
  },
  case evals.CStep : e emid e' hsmall hbig hmide' {
    -- e ↦ emid and emid ↦* e'
    -- Goal: (Expr.Op op e e2) ↦* (Expr.Op op e' e2)
    -- hsmall: e ↦ emid
    -- We know that (Expr.Op op e e2) ↦ (Expr.Op op emid e2)
    --   via eval.CLeft
    -- hmide': (Expr.Op op emid e2) ↦* (Expr.Op op e' e2)
    -- I want to apply evals.CStep with:
    -- e = (Expr.Op op e e2)
    -- e' = (Expr.Op op emid e2)
    -- e'' = (Expr.Op op e' e2)
    apply evals.CStep (Expr.Op op e e2) (Expr.Op op emid e2) (Expr.Op op e' e2),
    apply eval.ELeft,
    exact hsmall,
    exact hmide',
  }
end
