-- IMPORTANT: See `src/lnat.lean` for the formalization of Lnat.
import .src.lnat

-- Condition 1: There exists an expression e2 such that e1 → e2.
-- Condition 2: The proof of e1 → e2 uses all the three inference rules for e → e′.

-- Rules:
-- 1. E-Left:          e1 → e1' -> e1 ⊛ e2 → e1' ⊛ e2
-- 2. E-Right: e1 val, e2 → e2' -> e1 ⊛ e2 → e1 ⊛ e2'
-- 3. E-Op:                        n1 ⊛ n2 → n1 * n2

-- e1: (1*2) + (4/2)
-- e2: 4

--    (1*2) + (4/2)
-- ->   2   + (4/2) E-Left
-- ->   2   +   2   E-Right
-- ->       4       E-Op

def e1left : Expr := Expr.Op Op.Mul (Expr.Num 1) (Expr.Num 2)
def e1right : Expr := Expr.Num 3

def e1 : Expr :=
  Expr.Op Op.Add
  -- (Expr.Num 2)
  e1left
  e1right
  -- (Expr.Op Op.Div (Expr.Num 4) (Expr.Num 2))

def e1b : Expr :=
  Expr.Op Op.Add
  (Expr.Num 2)
  (Expr.Num 3)

def e2 : Expr :=
  Expr.Num 5

lemma eval_e1be2 :
  e1b ↦ e2 :=
  eval.EOp Op.Add 2 3

-- e ↦ e' := eval e e'
lemma eval_e1e1b :
  e1 ↦ e1b :=
  eval.ELeft Op.Add e1left (Expr.Num 2) e1right (eval.EOp Op.Mul 1 2)

lemma eval_trans {a b c : Expr}
  (e1: a↦b) (e2: b↦c) : a ↦ c :=
  sorry

theorem eval_full :
  e1 ↦ e2 :=
  eval_trans eval_e1e1b eval_e1be2
  -- eval.ELeft Op.Add e1left (Expr.Num 2) e1right (eval.EOp Op.Mul 1 2)
  -- eval (Expr.Op Op.Add e1left e1right) (Expr.Num 5)

-- begin
--   apply eval.ELeft Op.Add,
--   apply eval.EOp,
-- end
