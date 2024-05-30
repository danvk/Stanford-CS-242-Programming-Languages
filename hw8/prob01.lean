-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

@[simp]
lemma inversion :
  ∀ e : Expr, (val e) → (∃ n : ℕ, e = Expr.Num n) :=
begin
  assume e v,
  cases v with vn,
  existsi vn,
  refl,
end
