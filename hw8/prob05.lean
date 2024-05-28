-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

lemma transitive_right (op : Op) (e1 e2 e2' : Expr) :
  (val e1) → (e2 ↦* e2')
  → (Expr.Op op e1 e2 ↦* Expr.Op op e1 e2') :=
begin
  intros hv1 h2big,
  induction h2big,
  case CRefl : e {
    apply evals.CRefl,
  },
  case evals.CStep : e2 emid e2' hsmall hbig hmide' {
    -- goal: Expr.Op op e1 e2↦*Expr.Op op e1 e2'
    --   e = Expr.Op op e1 e2
    --  e' = Expr.Op op e1 emid
    -- e'' = Expr.Op op e1 e2'
    apply evals.CStep,  -- (Expr.Op op e1 e2) (Expr.Op op e1 emid) (Expr.Op op e1 e2'),
    apply eval.ERight,
    repeat { assumption },
  }
end
