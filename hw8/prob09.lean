-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus
import .prob08

-- lemma substitution :
--   ∀ e e' e'' : Expr, ∀ i : ℕ,
--   (typnat i e) → (typnat (i+1) e')
--   → (subst i e e' e'') → (typnat i e'') :=

theorem type_preserve :
  ∀ e e' : Expr, (typnat 0 e) → (e ↦ e') → (typnat 0 e') :=
begin
  intros e e' tn0e heval,
  induction heval,
  case ELeft: _ _ _ _ _ tne1e1' {
    cases typnat_op tn0e with tne1 tne2,
    apply typnat.TOp,
    exact tne1e1' tne1,
    assumption,
  },
  case ERight: _ _ _ _ _ _ tne2e2' {
    cases typnat_op tn0e with tne1 tne2,
    apply typnat.TOp,
    exact tne1,
    exact tne2e2' tne2,
  },
  case EOp: e e' op {
    apply typnat.TNum,
  },
  case DLet: _ _ _ hsubst {
    cases tn0e,
    rename tn0e_ᾰ → tn0e1,
    rename tn0e_ᾰ_1 → tn1e2,
    -- Why doesn't `exact substitution tn0e1 tn1e2 hsubst` work here?
    apply substitution,
    exact tn0e1,
    exact tn1e2,
    exact hsubst,
  }
end
