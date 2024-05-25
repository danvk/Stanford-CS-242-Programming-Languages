-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat
import .prob01
import .prob04
import .prob05

theorem totality :
  ∀ e : Expr, ∃ e' : Expr, (val e') ∧ (e ↦* e') :=
begin
  intro e,
  induction e,
  case Num : n {
    existsi (Expr.Num n),  -- this feels roundabout; what happened to e?
    split,
    apply val.VNum,
    refl,
  },
  case Op : op e1 e2 h1 h2 {
    -- Goal: ∃ (e' : Expr), val e' ∧ Expr.Op op e1 e2↦*e'
    cases h1 with e1' x,
    cases x with ve1' he1e1',
    cases h2 with e2' x,
    cases x with ve2' he2e2',
    cases ve1' with n1,
    cases ve2' with n2,
    -- cases h2 with e2',
    existsi (Expr.Num (apply_op op n1 n2)),
    split,
    apply val.VNum,
    -- Goal: Expr.Op op e1 e2↦*Expr.Num (apply_op op n1 n2)
    -- Plan:
    -- 1. via transitive_left, we have:
    --    Expr.Op op e1 e2 ↦* Expr.Op op (Expr.Num n1) e2
    -- 2. via transitive_right, we have:
    --    Expr.Op op (Expr.Num n1) e2 ↦* Expr.Op op (Expr.Num n1) (Expr.Num n2)
    -- 3. via eval.EOp
    --    Expr.Op op (Expr.Num n1) (Expr.Num n2) ↦ Expr.Num (apply_op op n1 n2)
    -- put this all together via transitivity
    transitivity Expr.Op op (Expr.Num n1) (Expr.Num n2),
    transitivity Expr.Op op (Expr.Num n1) e2,
    apply transitive_left,
    assumption,
    apply transitive_right,
    assumption,
    assumption,
    -- Expr.Op op (Expr.Num n1) (Expr.Num n2)↦*Expr.Num (apply_op op n1 n2)
    apply evals.CStep,
    show Expr, from Expr.Num (apply_op op n1 n2),
    apply eval.EOp,
    apply evals.CRefl,
  },
end
