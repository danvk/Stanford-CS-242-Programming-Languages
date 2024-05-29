--=======================
-- Proving the following propositions is not mandatory,
-- but is highly recommended. You will not submit this file.
--=======================

lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h with hp hq,
  apply and.intro,
  assumption,
  assumption,
end

theorem test (p q : Prop) (hp : p) (hq : q) : p ∧ q ∧ p :=
begin
  split,
  assumption,
  split,
  assumption,
  assumption,
  -- apply and.intro hp,
  -- exact and.intro hq hp
end


-- Exercise: introduction and elimination rules of ∧ and →.
-- Tactics used in reference solution:
--   split, cases, intros, assumption.
theorem and_commute (p q : Prop) :
  p ∧ q ↔ q ∧ p :=
  -- (p ∧ q → q ∧ p) ∧
  -- (q ∧ p → p ∧ q) :=
begin
  split,
  apply and_commute1,
  apply and_commute1,
end

-- Exercise: introduction and elimination rules of ∨ and ¬.
-- Tactics used in reference solution:
--   left, right, cases, intros, apply, split, assumption.

-- This is the CS242 version of DeMorgan's Law
theorem demorgan (p q : Prop) : ¬(p ∨ q) ↔ (¬p ∧ ¬q) :=
begin
  split, -- Split the bi-implication into two implications
  {
    assume hh,
    split,
    -- any way to consolidate these two cases?
    {
      assume hp,
      apply hh,
      left,
      assumption,
    },
    {
      assume hq,
      apply hh,
      right,
      assumption,
    }
  },
  {
    assume h,
    intro hh,
    cases h with np nq,
    cases hh,
    contradiction,
    contradiction,
  }
end

-- "The canonical way to prove ∀ x : α, p x is to take an arbitrary x, and prove p x."

-- Exercise: introduction and elimination rules of ∀.
-- Tactics used in the reference solution:
--   intros, apply, have, split, cases, assumption.
theorem and_forall_distribute (α : Type) (p q : α → Prop) :
  ((∀ x, p x ∧ q x) ↔ (∀ x, p x) ∧ (∀ x, q x)) :=
begin
  split,
  {
    intro h,
    split,
    {
      assume x,
      exact (h x).left,
    },
    {
      assume x,
      exact (h x).right,
    }
  },
  {
    intro h,
    cases h with hp hq,  -- "cases" splits an and
    -- goal: ∀ (x : α), p x ∧ q x
    assume x,
    split,
    apply (hp x),
    apply (hq x)
    -- exact ⟨ (hp x), (hq x) ⟩
  }
end

-- Exercise: introduction and elimination rules of ∃.
-- Tactics used in the reference solution:
--   existsi, cases ... with ..., split, cases,
--   intros, left, right, assumption.
theorem or_exists_distribute (α : Type) (p q : α → Prop) :
  ((∃ x, p x ∨ q x) ↔ ((∃ x, p x) ∨ (∃ x, q x))) :=
begin
  split,
  {
    intro h,
    cases h with x hpq,
    cases hpq,
    { left, existsi x, assumption },
    { right, existsi x, assumption }
  },
  {
    intro h,
    cases h,
    { cases h with x, existsi x, left, assumption },
    { cases h with x, existsi x, right, assumption }
  }
end
