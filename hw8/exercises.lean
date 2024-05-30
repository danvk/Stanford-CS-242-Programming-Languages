--=======================
-- Proving the following propositions is not mandatory,
-- but is highly recommended. You will not submit this file.
--=======================

-- Exercise: introduction and elimination rules of ∧ and →.
-- Tactics used in reference solution:
--   split, cases, intros, assumption.
theorem and_commute (p q : Prop) :
  (p ∧ q ↔ q ∧ p) :=
begin
  split,
  repeat {
    intro pq,
    cases pq,
    split,
    repeat { assumption },
  }
end

-- Exercise: introduction and elimination rules of ∨ and ¬.
-- Tactics used in reference solution:
--   left, right, cases, intros, apply, split, assumption.
theorem demorgan (p q : Prop) :
  ¬(p ∨ q) ↔ (¬p ∧ ¬q) :=
begin
  split,
  {
    intro npq, -- ¬(p ∨ q) = (p ∨ q) -> false
    split,
    {
      -- Goal: ¬p = p -> false
      intro hp,
      apply npq,
      left,
      assumption,
    },
    {
      intro hp,
      apply npq,
      right,
      assumption,
    }
  },
  {
    intro npq,
    cases npq,
    intro pq,
    cases pq,
    repeat { contradiction },
  }
end

-- Exercise: introduction and elimination rules of ∀.
-- Tactics used in the reference solution:
--   intros, apply, have, split, cases, assumption.
theorem and_forall_distribute (α : Type) (p q : α → Prop) :
  (∀ x, p x ∧ q x) ↔ (∀ x, p x) ∧ (∀ x, q x) :=
begin
  -- FILL IN HERE.
  sorry
end

-- Exercise: introduction and elimination rules of ∃.
-- Tactics used in the reference solution:
--   existsi, cases ... with ..., split, cases,
--   intros, left, right, assumption.
theorem or_exists_distribute (α : Type) (p q : α → Prop) :
  (∃ x, p x ∨ q x) ↔ (∃ x, p x) ∨ (∃ x, q x) :=
begin
  -- FILL IN HERE.
  sorry
end
