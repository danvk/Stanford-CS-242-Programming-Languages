-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus

-- You can define and prove auxiliary lemmas here.

-- if a ≤ b and a ≠ b, then a < b
-- I think this is the same as order.lt_or_gt_of_ne
-- lemma le_ne_to_lt { a b : ℕ } : a ≠ b → a ≤ b → a < b := sorry
-- If a < b then a ≠ b.
-- lemma lt_to_ne {a b : ℕ } : a < b → a ≠ b := sorry

lemma plus1_cases { a b : ℕ } : a+1 > b → a=b ∨ a>b :=
begin
  intro a1gtb,
  cases lt_trichotomy a b,
  {
    rename h a_lt_b,
    -- a_lt_b: a < b
    -- b < succ a => b <= a
    -- a_lt_b -> a != b
    -- let a_ne_b := lt_to_ne a_lt_b,
    let b_le_a := nat.le_of_lt_succ a1gtb,
    let w := not_lt_of_ge b_le_a,
    contradiction,
  },
  cases h,
  {
    -- a = b
    left,
    exact h,
  },
  {
    -- b < a
    right,
    exact h,
  }
end

lemma typnat_op { i : ℕ } { op : Op } { e1 e2 : Expr } :
  typnat i (Expr.Op op e1 e2) →
  typnat i e1 ∧ typnat i e2 := sorry

-- TVar (j i : ℕ) : j < i → typnat i (Expr.Var j)
lemma typnat_var { i j : ℕ } :
  typnat i (Expr.Var j) →
  i > j := sorry

lemma substitution :
  ∀ e e' e'' : Expr, ∀ i : ℕ,
  (typnat i e) → (typnat (i+1) e')
  → (subst i e e' e'') → (typnat i e'') :=
begin
  intros e e' e'' i hnatie hnati1e' hsubst,
  -- ideas:
  -- induction on hnati1e' or hnatie.
  -- induction on hsubst
  induction hsubst,
  case SNum: i n ex {
    apply typnat.TNum,
  },
  case SOp: op i e1 e2 e1' e2' e' hsubste1 hsubste2 htne1 htne2 {
    -- There's a "let" tactic for introducing new variables!
    cases (typnat_op hnati1e') with tn1e1 tn2e2,
    apply typnat.TOp,
    exact htne1 hnatie tn1e1,
    exact htne2 hnatie tn2e2,
  },
  case SVarEq: i j e' ieqj {
    assumption,
  },
  case SVarNeq: i j e' inej {
    -- have hnati1e': typnat (i + 1) (Expr.Var j)
    -- TVar (j i : ℕ) : j < i → typnat i (Expr.Var j)
    cases (plus1_cases (typnat_var hnati1e')),
    {
      contradiction,
    },
    {
      apply typnat.TVar,
      exact h,
    },
  },
  case SLet: e1 e2 e1' e2' e' i hsubste1 hsubste2 htne1 htne2 {
    -- are all these terms coming from recursively applying this lemma?
    let x := htne1 hnatie,

    sorry,
  },
end
