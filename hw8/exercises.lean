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
    intro h, -- h: ¬(p ∨ q); goal: ¬p ∧ ¬q; aka p ∨ q → false
    by_cases hp : p, -- Consider cases for P
    {
      -- Case 1: p is true; goal is ¬p ∧ ¬q
      -- idea: since p is true, ¬p is false, so ¬p ∧ ¬q is also false
      split,
      {
        -- goal: ¬p; this feels too roundabout! I have p and need to prove ¬p.
        intro nhp,
        apply h,
        left,
        exact nhp,
      },
      {
        -- goal: ¬q
        intro hq,
        apply h,
        -- Either of these works… is there a better way to do this?
        -- exact (or.intro_left q hp)
        exact (or.intro_right  p hq)
      }
    },
    {
      -- Case 2: ¬p, goal is ¬p ∧ ¬q
      split,
      {
        -- goal is ¬p
        exact hp,
      },
      {
        -- goal is ¬q
        intro hq,
        apply h,
        right,
        exact hq,
      }
    }
  },
  {
    -- Goal: ¬p ∧ ¬q → ¬(p ∨ q)
    intro h, -- h: ¬p ∧ ¬q
    intro hpq, -- hpq: p ∨ q
    cases h with nhp nhq, -- Consider cases for ¬P ∨ ¬Q
    {
      -- hp: ¬p, hq: ¬q, goal: false
      cases hpq with hp hq,
      {
        apply nhp,
        exact hp,
      },
      {
        apply nhq,
        exact hq,
      }
    },
  }
end

-- This is ChatGPT's version of DeMorgan's Law
theorem demorgan2 (P Q : Prop) : ¬ (P ∧ Q) ↔ (¬ P ∨ ¬ Q) :=
begin
  split, -- Split the bi-implication into two implications
  {
    -- First direction: ¬ (P ∧ Q) → (¬ P ∨ ¬ Q)
    intro h, -- Assume ¬ (P ∧ Q)
    by_cases hp : P, -- Consider cases for P
    {
      -- Case 1: P is true; goal is ¬P ∨ ¬Q
      -- right, -- goal is now ¬Q
      apply or.inr,
      intro hq, -- Assume Q; why are we able to do this? goal is now false
      -- hqn : ¬Q
      apply h, -- Derive a contradiction; goal is now P ∧ Q
      -- The definition of "negation": ¬X := X → false
      -- If our goal is B and h: A → B, then "apply h" changes the goal to A.
      exact ⟨hp, hq⟩, -- From P and Q, we have P ∧ Q
    },
    {
      -- Case 2: P is false; goal is ¬P ∨ ¬Q
      -- hp: P -> false
      left, -- We need to show ¬P
      exact hp, -- This follows from the assumption
    }
  },
  {
    -- Second direction: (¬ P ∨ ¬ Q) → ¬ (P ∧ Q)
    intro h, -- Assume ¬ P ∨ ¬ Q
    intro hpq, -- Assume P ∧ Q
    cases h, -- Consider cases for ¬ P ∨ ¬ Q
    {
      -- Case 1: ¬ P
      apply h, -- Derive a contradiction
      exact hpq.1, -- From P ∧ Q, we have P
    },
    {
      -- Case 2: ¬ Q
      apply h, -- Derive a contradiction
      exact hpq.2, -- From P ∧ Q, we have Q
    }
  }
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
