--=======================
-- Proving the following propositions is not mandatory,
-- but is highly recommended. You will not submit this file.
--=======================
#eval let v := lean.version in let s := lean.special_version_desc in string.join
["Lean (version ", v.1.repr, ".", v.2.1.repr, ".", v.2.2.repr, ", ",
if s ≠ "" then s ++ ", " else s, "commit ", (lean.githash.to_list.take 12).as_string, ")"]

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

-- A ↔ B
-- (A → B) ∧ (B → A)

-- Exercise: introduction and elimination rules of ∧ and →.
-- Tactics used in reference solution:
--   split, cases, intros, assumption.
theorem and_commute (p q : Prop) :
  p ∧ q ↔ q ∧ p :=
  -- (p ∧ q → q ∧ p) ∧
  -- (q ∧ p → p ∧ q) :=
begin
  -- apply and.intro,
  split,
    intro h,
    -- apply and.cases_on h,
    --  intros p q,
    cases h with hp hq,
      exact (and.intro hq hp),
      -- exact ⟨ hq, hp ⟩,
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

-- This is the CS242 version of DeMorgan's Law
theorem demorgan (p q : Prop) : ¬(p ∨ q) ↔ (¬p ∧ ¬q) :=
begin
  split, -- Split the bi-implication into two implications
  {
    -- Goal: ¬(p ∨ q) → ¬p ∧ ¬q
    intro h, -- h: ¬(p ∨ q); goal: ¬p ∧ ¬q; (equivalently, h : p ∨ q → false)
    split,
    {
      -- goal: ¬p; this feels too roundabout! I have p and need to prove ¬p.
      intro hp,
      apply h,
      left,
      assumption
    },
    {
      -- goal: ¬q
      intro hq,
      apply h,
      right,
      assumption
    }
  },
  {
    -- Goal: ¬p ∧ ¬q → ¬(p ∨ q)
    intro h, -- h: ¬p ∧ ¬q
    intro hpq, -- hpq: p ∨ q
    cases hpq with hp hq,
    {
      -- goal: false
      apply h.left,
      assumption,
    },
    {
      apply h.right,
      assumption,
    }
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
      -- goal: ∀ (x : α), p x
      assume x : α,  -- assume introduces x : α but also changes the goal to p x
      exact (h x).left,
      -- more long-winded version:
      -- have hpx: p x, from (h x).left,
      -- assumption
    },
    {
      -- goal: ∀ (x : α), q x
      assume x : α,
      exact (h x).right,
    }
  },
  {
    intro h,
    cases h with hp hq,  -- is it weird to have "cases" with only one case?
    -- goal: ∀ (x : α), p x ∧ q x
    assume x : α,
    exact ⟨ (hp x), (hq x) ⟩
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
