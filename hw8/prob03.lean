-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat
import .prob01

-- We give the following hints only for this problem.
-- (1) Propositions used in the reference solution:
--       inversion, val.VNum, eval.ELeft, eval.ERight, eval.EOp.
-- (2) Tactics used in the reference solution:
--       intros, have, exact, assumption, apply,
--       left, right, existsi, cases ... with ...,
--       induction, case ... : ... { ... }, simp *.

--lemma inversion : ∀ e : Expr, (val e) → (∃ n : ℕ, e = Expr.Num n)

theorem progress :
  ∀ e : Expr, (val e) ∨ (∃ e', e ↦ e') :=
begin
  intro e,
  induction e,
  case Num: n {
    left,
    apply val.VNum,
  },
  case Op: op e1 e2 ihe1 ihe2 {
    right,
    cases ihe1 with e1val e1expr,
    {
      cases e1val with n1,
      cases ihe2 with e2val e2expr,
      {
        -- e1 and e2 are both values
        cases e2val with n2,
        -- Goal: Exists (eval (Expr.Op op (Expr.Num n1) (Expr.Num n2)))
        existsi (Expr.Num (apply_op op n1 n2)),
        apply eval.EOp,
      },
      {
        -- e1 is a value, e2 is an expression
        cases e2expr with e2p,  -- uses "cases" to get the witness
        existsi (Expr.Op op (Expr.Num n1) e2p),
        apply eval.ERight,
        repeat { assumption },
      }
    },
    {
      cases e1expr with e1p,
      cases ihe2 with e2val e2expr,
      {
        -- e1 is an expression, e2 is a value
        cases e2val with n2,
        existsi (Expr.Op op e1p (Expr.Num n2)),
        apply eval.ELeft,
        assumption,
      },
      {
        -- both are expressions; we'll apply ELeft
        existsi (Expr.Op op e1p e2),
        apply eval.ELeft,
        assumption,
      }
    }
  }
end
