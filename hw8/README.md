# Homework 8: Lean

This homework was significantly longer and more involved than any of the others. It's worth doing, but be aware of what you're getting into!

## Install / Setup

On a Mac, install Lean via:

    brew install lean

I used the VS Code Lean extension. I got the following error, but it proved inconsequential: "You are running Lean in a directory without a leanpkg.toml file, this is NOT supported."

## Notes on Lean

The homework suggests reading most of the [Lean 3 docs]. They're good, but they're lengthy and they may not make that much sense until you've played around with Lean. My suggestion would be to:

1. Read [Chapter 1] to get a quick overview of Lean.
2. Read the quick synopsis below.
3. Do `exercises.lean`
4. Read through the rest of the Lean docs.
5. Do problems 1–11.

All my solutions were in "tactics mode." This is where you want to be working. The tactics I used most were:

1. `split`
2. `assume`
3. `cases`
4. `assumption`
5. `apply`
6. `left` and `right`
7. `contradiction`

### split, assume, cases, exact, assumption

In Lean, you always have one or more goal types and a "state," which is a set of terms and their types. Your objective is to produce a term with the goal type, at which point you can write `assumption` to complete the proof.

For example, if you write this:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  -- cursor here
end
```

Then you should see the following in the "Lean Infoview":

    Tactic state:
    1 goal
    p q: Prop
    ⊢ p ∧ q → q ∧ p

Your goal is to produce a term with type `p ∧ q → q ∧ p`. We have terms `p` and `q` of type `Prop`.

Whenver your goal is an implication / function type, you can use `assume` to introduce a term of the left-hand type and change the goal to the right-hand type. So in this case:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  -- cursor here
end
```

Now we have:

    Tactic state:
    p q: Prop
    h: p ∧ q
    ⊢ q ∧ p

So there's a new term, `h: p ∧ q`, and the goal is to produce a term of type `q ∧ p`. (`∧` means "and" and is written `\and`.)

The `cases` tactic can be used to "destructure" constructs like `p ∧ q`. We can use it to get terms of type `p` and `q`:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h with hp hq,
  -- cursor here
end
```

    Tactic state:
    p q: Prop
    hp: p
    hq: q
    ⊢ q ∧ p

The goal hasn't changed, but the `h` term has disappeared and been replaced with terms `hp: p` and `hq: q`.

At this point, one option is to construct the goal term directly with `exact`:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h with hp hq,
  exact ⟨ hq, hp ⟩
end
```

The angle braces are written `\<` and `\>`. You can't write `hq ∧ hp`, I think because that's an operation on the types rather than the terms?

This works, but there's another option that doesn't require us to write out the term explicitly. Whenever your goal is a conjunction ("and" / `∧`), you can use the `split` tactic to break it up into two goals. You can then meet these goals one-by-one:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h with hp hq,
  split,
  -- cursor here
end
```

    2 goals
    p q: Prop
    hp: p
    hq: q
    ⊢ q
    p q: Prop
    hp: p
    hq: q
    ⊢ p

We now have two goals, `q` and `p`, each of which has the same state. `split` can break up other constructs, too, for example `↔` into two `→`s. You can "focus" on the first goal by writing `{}`. But in this case, we have a term of the goal type. You can tell Lean about this using the `exact` tactic: `exact hq`. Or you use `assumption` to tell it to look for itself:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h with hp hq,
  split,
  assumption,
  -- cursor here
end
```

    1 goal
    p q: Prop
    hp: p
    hq: q
    ⊢ p

This is the same situation, so you can just write `assumption` again to complete the proof:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h with hp hq,
  split,
  assumption,
  assumption,
end
```

In this case the `exact` forms were quite legible, but the `assumption` form is convenient when the goal term is one that some other tactic has automatically generated and named. If you don't name variables, Lean will name them for you automatically. By using `assumption`, you can keep the names out of your proof entirely. For example, we could drop the `with` clause from `cases`:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h,
  split,
  assumption,
  assumption,
end
```

If you're feeling fancy, you can use `repeat` to repeat the `assumption` tactic as many times as possible:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h,
  split,
  repeat { assumption },
end
```

Many of my proofs in this homework ended with `repeat { assumption }`.

### apply

The `apply` tactic applies a function to the _goal_. If our goal is `B` and we have `h: A → B`, then `apply h` changes our goal to `A`. This the reverse of ordinary function application! We're working backward from a goal, rather than forwards from out state.

For example, the constructor `and.intro` has the following type:

```lean
and.intro : ∀ {a b : Prop}, a → b → a ∧ b
```

In the previous problem, our goal had the form `q ∧ p`. Since this matches the right-hand side of `and.intro`, we could have written `apply and.intro` instead of `split`:

```lean
lemma and_commute1 (p q : Prop) :
  (p ∧ q → q ∧ p) :=
begin
  assume h,
  cases h with hp hq,
  apply and.intro,
  -- cursor here
end
```

    2 goals
    p q: Prop
    hp: p
    hq: q
    ⊢ q
    p q: Prop
    hp: p
    hq: q
    ⊢ p

You can use `split` intead of `apply` when the type has only one constructor, like `and`. But when we're working with inductive data types with multiple constructors in the later problems, you have to say which constructor you want to `apply`.

## Falsehoods / Negations

When you're working with negations, it's important to remember that `¬p` is just shorthand for `p → false`.

For example, in the `demorgan` exercise, you might wind up in this state:

    1 goal
    p q: Prop
    hh: ¬(p ∨ q)
    ⊢ ¬p

What can you do here? If you mentally rewrite the negations, your options become more apparent:

    1 goal
    p q: Prop
    hh: (p ∨ q) → false
    ⊢ p → false

Since the goal is an implication, we can use `assume` to assume the hypothesis, for example `assume hp`:

    p q: Prop
    hh: ¬(p ∨ q)
    hp: p
    ⊢ false

Since our goal is `false` and we have `hh: (p ∨ q) → false`, we can `apply hh`:

    p q: Prop
    hh: ¬(p ∨ q)
    hp: p
    ⊢ p ∨ q

Now the proof can be completed with `left` (which focuses on the left-hand side of an "or") and `assumption`.

## Other tactics

Here are some other tactics I used in my solutions. You can read more about these in the [tactics chapter] of the Lean docs.

- `existsi`: If your goal has the form `∃ x, p x`, then you use `existsi` to provide the "witness" to the "existential quantifier." Your goal will then be to prove `p x`.
- `intro` / `intros`: If your goal is `∀ e...`, then you can use `intro e` to get a term `e`.
- `let`: This tactic lets you introduce a new term into the state via `let x := expression`. This isn't usually required in a final solution, but it can be very helpful as a way of exploring and expanding your state.
- `rename`: You can write `rename a → b` to rename a term in your state. This can be a useful way to rename the terms that Lean automatically generates.
- `refl`: If your goal is something like `x=x`, then you can write `refl` to prove it.

## Part 1 (Problems 1-3): Progress and Induction

For these problems it's important to note that `→` is a "small step." So while

    (1*2) + 3 ↦ 2 + 3

It's _not_ the case that:

    (1*2) + 3 ↦ 5

This is really important for constructing your example in problem 2!

Problem 3 is the first use of the `induction` tactic. It's useful to look at the state / goals after applying it to the expression:

```lean
theorem progress :
  ∀ e : Expr, (val e) ∨ (∃ e', e ↦ e') :=
begin
  intro e,
  induction e,
  -- cursor here
end
```

    2 goals
    case Expr.Num
    e: ℕ
    ⊢ val (Expr.Num e) ∨ ∃ (e' : Expr), Expr.Num e↦e'
    case Expr.Op
    e_ᾰ: Op
    e_ᾰ_1e_ᾰ_2: Expr
    e_ih_ᾰ: val e_ᾰ_1 ∨ ∃ (e' : Expr), e_ᾰ_1↦e'
    e_ih_ᾰ_1: val e_ᾰ_2 ∨ ∃ (e' : Expr), e_ᾰ_2↦e'
    ⊢ val (Expr.Op e_ᾰ e_ᾰ_1 e_ᾰ_2) ∨ ∃ (e' : Expr), Expr.Op e_ᾰ e_ᾰ_1 e_ᾰ_2↦e'

It becomes a little clearer what's going on if you name these terms in each case:

```lean
theorem progress :
  ∀ e : Expr, (val e) ∨ (∃ e', e ↦ e') :=
begin
  intro e,
  induction e,
  case Num: n {
    sorry,
  },
  case Op: op e1 e2 ihe1 ihe2 {
    -- cursor here
  }
end
```

    1 goal
    case Expr.Op
    op: Op
    e1 e2: Expr
    ihe1: val e1 ∨ ∃ (e' : Expr), e1↦e'
    ihe2: val e2 ∨ ∃ (e' : Expr), e2↦e'
    ⊢ val (Expr.Op op e1 e2) ∨ ∃ (e' : Expr), Expr.Op op e1 e2↦e'

Here's the definition of `Expr`:

```lean
inductive Expr
| Num : ℕ → Expr
| Op  : Op → Expr → Expr → Expr
```

The first three variables after `case Op` (`op`, `e1`, `e2`) correspond to the `Expr.Op` constructor. But crucially, the next two correspond to recursively applying `progress` to `e1` and `e2`! This seems to be how recursion works in Lean. Rather that applying yourself recursively in ways that may or may not be valid, Lean gives you terms for all valid (structural) recursive applications. (NB: It seems like this would preclude mutual recursion?)

Remember that you can use `cases` to unpack a lot of constructs. For example:

- If you have `h1: val e1`, you can use `cases h1 with n1` to extract the number.
- If you have `h: ∃ (e' : Expr), e↦e'`, you can use `cases h with e'` to extract the witness.

I didn't wind up using the `inversion` lemma from problem 1 in either problem 2 or 3. I also didn't use `simp*`, which the homework suggests.

## Part 2 (Problems 4-7): Totality

After you write `induction h`, it's a good idea to stub out all the cases with variables and `{ sorry }` blocks. I found that Lean sometimes reported errors in surprising places if I didn't do this.

For problems 4 and 5, I found it helpful to write out exactly what I expected the arguments to `evals.CStep` to be.

In problem 6, if your goal is `A ↦* C`, then you can write `transitivity B` to split it into two goals, `A ↦* B` and `B ↦* C`. You can also write `transitivity` without an argument to leave the intermediate state implicit. This is more concise but also more confusing! Remember that while `A↦*A`, it's not the case that `A↦A`.

## Part 3 (Problems 8-11): Type Preservation

This part was optional but I found it quite interesting since it forces you to start proving things about natural numbers.

For problem 8, I found it useful to factor out "helper functions" (lemmas) for statements that I thought were true but didn't want to prove just yet. By implementing them with `sorry`, I could stay focused on the big proof and fill in the lemmas later.

It's tricky to go from obvious contradictions like `1 < 0` to your goal of `false`. I found that ChatGPT was really good at knowing exactly which lemma in the Lean library to apply.

I was able to complete problems 8, 9 and 10 mostly through symbol manipulation. But problem 11 forced me to understand how the language actually worked. As a hint, the try to figure out why the `i + 1` is need in problem 8/9. The counterexample expression is very short, but it took me a while to come up with it.

[Lean 3 docs]: https://leanprover.github.io/theorem_proving_in_lean/index.html
[Chapter 1]: https://leanprover.github.io/theorem_proving_in_lean/introduction.html
[tactics chapter]: https://leanprover.github.io/theorem_proving_in_lean/tactics.html
