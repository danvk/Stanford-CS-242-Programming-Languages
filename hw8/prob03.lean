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
  case Op: op e1 e2 v1 v2 {
    cases v1,
    {
      cases v2,
      {
        left,
        apply (exists.elim (inversion e1 v1)),
        intros n1 hn1,
        apply (exists.elim (inversion e2 v2)),
        intros n2 hn2,
        simp*,
        -- maybe this isn't true?
      },
      {
        right,
        apply (exists.elim v2),
        intros e2' he,
        existsi e2',
        -- Goal: (Expr.Op op e1 e2)↦e'
        -- I don't think this is true?
      }
    }
  }
end

