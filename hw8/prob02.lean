-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

-- Condition 1: There exists an expression e2 such that e1 → e2.
-- Condition 2: The proof of e1 → e2 uses all the three inference rules for e → e′.

-- Rules:
-- 1. E-Left:          e1 → e1' -> e1 ⊛ e2 → e1' ⊛ e2
-- 2. E-Right: e1 val, e2 → e2' -> e1 ⊛ e2 → e1 ⊛ e2'
-- 3. E-Op:                        n1 ⊛ n2 → n1 * n2

--    1 + ((2*3) + 1)
-- -> 1 + (  6   + 1)

def e1 : Expr :=
  Expr.Op Op.Add
  (Expr.Num 1)
  (Expr.Op Op.Add
    (Expr.Op Op.Mul (Expr.Num 2) (Expr.Num 3))
    (Expr.Num 1))

def e2 : Expr :=
  Expr.Op Op.Add
  (Expr.Num 1)
  (Expr.Op Op.Add
    (Expr.Num 6)
    (Expr.Num 1))

lemma eval_example :
   e1 ↦ e2 :=
begin
  apply eval.ERight,
  apply eval.ELeft,
  apply eval.EOp,
  apply val.VNum,
end
