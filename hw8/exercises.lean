--=======================
-- Proving the following propositions is not mandatory,
-- but is highly recommended. You will not submit this file.
--=======================

constants p q : Prop
theorem t1 : p → q → p := λ hp : p, λ hq : q, hp

lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
  assume h : p ∧ q,
  -- assume hq : q,
  -- assume hp : p,
  -- and.intro (and.elim_right h) (and.elim_left h)
  -- ⟨ (and.elim_right h), (and.elim_left h) ⟩
  -- ⟨ (and.right h), (and.left h) ⟩
  ⟨ h.right, h.left ⟩

theorem test (p q : Prop) (hp : p) (hq : q) : p ∧ q ∧ p :=
begin
  apply and.intro hp,
  exact and.intro hq hp
  -- apply and.intro,
  -- exact hp,
  -- apply and.intro,
  -- exact hq,
  -- exact hp
end

-- #print test

variables (α : Type*) (r : α → α → Prop)
variable  trans_r : ∀ x y z, r x y → r y z → r x z

variables a b c : α
variables (hab : r a b) (hbc : r b c)

#check trans_r    -- ∀ (x y z : α), r x y → r y z → r x z
#check trans_r a b c
#check trans_r a b c hab
#check trans_r a b c hab hbc

-- Exercise: introduction and elimination rules of ∧ and →.
-- Tactics used in reference solution:
--   split, cases, intros, assumption.
theorem and_commute (p q : Prop) :
  (p ∧ q → q ∧ p) ∧
  (q ∧ p → p ∧ q) :=
begin
  apply and.intro,
    intro h,
    -- apply and.cases_on h,
    --  intros p q,
    cases h with p q,
      -- exact (and.intro q p),
      exact ⟨ q, p ⟩,
    intro h,
    apply and.cases_on h,
      intros q p,
      exact (and.intro p q),
end
-- how would I use and_commute1 here?
-- could this be rewritten using ↔?

-- Exercise: introduction and elimination rules of ∨ and ¬.
-- Tactics used in reference solution:
--   left, right, cases, intros, apply, split, assumption.
theorem demorgan (p q : Prop) :
  (¬(p ∨ q) → (¬p ∧ ¬q)) ∧
  ((¬p ∧ ¬q) → ¬(p ∨ q)) :=
begin
  -- FILL IN HERE.
  apply and.intro,
  intro h,
    -- apply or.elim,
    sorry,
  intro h,
    cases h with hnp hnq,
    apply not.intro,
    sorry
end

-- Exercise: introduction and elimination rules of ∀.
-- Tactics used in the reference solution:
--   intros, apply, have, split, cases, assumption.
theorem and_forall_distribute (α : Type) (p q : α → Prop) :
  ((∀ x, p x ∧ q x) → (∀ x, p x) ∧ (∀ x, q x)) ∧
  ((∀ x, p x) ∧ (∀ x, q x) → (∀ x, p x ∧ q x)) :=
begin
  -- FILL IN HERE.
  sorry
end

-- Exercise: introduction and elimination rules of ∃.
-- Tactics used in the reference solution:
--   existsi, cases ... with ..., split, cases,
--   intros, left, right, assumption.
theorem or_exists_distribute (α : Type) (p q : α → Prop) :
  ((∃ x, p x ∨ q x) → (∃ x, p x) ∨ (∃ x, q x)) ∧
  ((∃ x, p x) ∨ (∃ x, q x) → (∃ x, p x ∨ q x)) :=
begin
  -- FILL IN HERE.
  sorry
end
