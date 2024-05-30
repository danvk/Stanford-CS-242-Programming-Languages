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

theorem progress :
  ∀ e : Expr, (val e) ∨ (∃ e', e ↦ e') :=
begin
  assume e,
  induction e,
  case Num: n {
    left,
    apply val.VNum,
  },
  case Op: op e1 e2 p1 p2 {
    cases p1,
    {
      cases p2,
      {
        right,
        cases p1 with n1,
        cases p2 with n2,
        existsi (Expr.Num (apply_op op n1 n2)),
        apply eval.EOp,
      },
      {

      }
    },
    {

    }
  }
end
