-- IMPORTANT: See `src/lnatplus.lean` for the formalization of Lnat+.
import .src.lnatplus

def e1 : Expr :=
  Expr.Let (Expr.Num 2) (Expr.Var 1)

def e2 : Expr :=
  Expr.Var 1

def i : ℕ :=
  1

lemma type_preserve_gen_counterexample :
  (typnat i e1) ∧ (e1 ↦ e2) ∧ ¬(typnat i e2) :=
begin
  split,
  {
    apply typnat.TLet,
    apply typnat.TNum,
    apply typnat.TVar,
    unfold i,  -- had to ask ChatGPT for this!
    exact nat.lt_succ_self 1,
  },
  split,
  {
    apply eval.DLet,
    apply subst.SVarNeq,
    exact nat.zero_ne_one,
  },
  {
    assume h,
    cases h,
    exact nat.lt_irrefl 1 h_ᾰ
  }
end

-- let 2 in 1^  -- typnat 1
-- 1^           -- typnat 2!
