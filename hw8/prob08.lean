-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus

-- You can define and prove auxiliary lemmas here.

lemma typnat_op { i : ℕ } { op : Op } { e1 e2 : Expr } :
  typnat i (Expr.Op op e1 e2) →
  typnat i e1 ∧ typnat i e2 :=
begin
  intro h,
  cases h,
  -- this is kind of cryptic! Why can't I give these variables names?
  exact ⟨ h_ᾰ, h_ᾰ_1 ⟩,
end

-- TVar (j i : ℕ) : j < i → typnat i (Expr.Var j)
lemma typnat_var { i j : ℕ } :
  typnat i (Expr.Var j) →
  i > j :=
begin
  intro h,
  cases h,
  assumption,
end

-- If $Γ ⊢ e : nat$, then $(Γ+1) ⊢ e : nat$ as well
lemma typnat_more { i : ℕ } { expr: Expr } :
  typnat i expr → typnat (i + 1) expr :=
begin
  intro h,
  induction h,
  case TNum: {
    apply typnat.TNum,
  },
  case TOp: op e1 e2 i _ _ tn11 tn12 {
    apply typnat.TOp,
    assumption,
    assumption,
  },
  case TVar: j i j_lt_i {
    -- TVar (j i : ℕ) : j < i → typnat i (Expr.Var j)
    -- need: j < i + 1
    let z := j_lt_i.step,
    apply typnat.TVar,
    exact z,
  },
  case TLet: e1 e2 i tn1 tn2 tn11 tn12 {
    apply typnat.TLet,
    assumption,
    assumption,
  },
end

-- If i ⊢ e : nat and i+1 ⊢ e' : nat, then i ⊢ e'[ˆı:=e] : nat
-- We can substitute an expression from (typnat i) into an
-- expression from (typenat i+1) and get an expression of (typenat i).
lemma substitution :
  ∀ e e' e'' : Expr, ∀ i : ℕ,
  (typnat i e) → (typnat (i+1) e')
  → (subst i e e' e'') → (typnat i e'') :=
begin
  intros _ _ _ _ h h' hsubst,
  -- ideas:
  -- induction on h or h'.
  -- induction on hsubst
  induction hsubst,
  case SNum: i n ex {
    apply typnat.TNum,
  },
  case SOp: op i e1 e2 e1' e2' e' hsubste1 hsubste2 htne1 htne2 {
    -- There's a "let" tactic for introducing new variables!
    cases (typnat_op h') with tn1e1 tn2e2,
    apply typnat.TOp,
    exact htne1 h tn1e1,
    exact htne2 h tn2e2,
  },
  case SVarEq: i j e' ieqj {
    assumption,
  },
  case SVarNeq: i j e' inej {
    -- have h: typnat (i + 1) (Expr.Var j)
    -- TVar (j i : ℕ) : j < i → typnat i (Expr.Var j)
    let jlei := nat.le_of_lt_succ (typnat_var h'),
    let jnei := ne.symm inej,  -- i≠j → j≠i
    let jlti := lt_of_le_of_ne jlei jnei,  -- j≤i ∧ j≠i -> j < i
    apply typnat.TVar,
    assumption,
  },
  case SLet: e1 e2 e1' e2' e' i hsubste1 hsubste2 htne1 htne2 {
    -- are all these terms coming from recursively applying this lemma? (YES)
    cases h',
    rename h'_ᾰ tne1,   -- typnat (i+1) e1
    rename h'_ᾰ_1 tne2, -- typnat (i+2) e2
    apply typnat.TLet,
    exact htne1 h tne1,
    let hplus := typnat_more h,
    exact htne2 hplus tne2,
  },
end
