# Homework 4

## Part 1

Part 1 assumes you have an Object Calculus interpreter. For the course, they provided a binary that you could use, but that doesn't work for us. At least it doesn't work on my Mac.

Instead, I used Rylan's solution.

    git checkout rylan -- hw4/interpreter.py

Then you can test your own solution using:

    cd hw4
    python src/main_objc.py problem.objc problem_test.objc --verify problem.objc.golden

You can use the files in `test` to get a sense for how Object Calculus syntax works.

### Problem 1

I had to look at `problem_test.objc` for a bit to understand what the intended usage of `noter` was. It's confusing that there's `noter.eval.eval` (two `eval`s!). I found it helpful to think about which object each "self" variable referred to in any position.

### Problem 2

I had to wrap `b1.onfalse` in an `[ eval ]` object so that I could access `.eval` on both the false and true sides. Rylan did something a little different. He doesn’t do `.eval.eval`; he evals once, then overrides the `ontrue` / `onfalse` of the result.

### Problem 3

I’m pretty happy with my solution to problem 3! The trick is to tweak your adder so that it adds `n1.pred` and `n2`, then access the `succ` on that. I stored this recursive result in a `result` field and made `iszero`, `succ` and `pred` access that.

My one problem was a misplaced parenthesis that threw everything into disarray:

```
-         .onfalse <- (\x. a.n1 <- \z. a.n1.pred).eval.succ
+         .onfalse <- \x. (a.n1 <- \z. a.n1.pred).eval.succ
```

This runs very quickly: ~2s for all three problems. So what the hell was Rylan doing that his solution takes 90+ seconds?

→ He implemented `iszero`, `pred` and `succ` independently of one another. So probably he’s running the addition many, many times. I’m not convinced his code is correct, this looks suspicious: `succ = \o. o.n1 <- \d. o.n1.succ`. Doesn’t it need to be `(n1+n2).succ`? Maybe this just isn’t tested. Or maybe this is why he only got an A-. 😜

## Part 2

This is mostly straightforward application of the rules in the PDF and pattern matching on the Python class hierarchy.

A few things that tripped me up:

- You can't run their tests until you implement all three parts, so it's hard to tell if you have a bug in tasks 1 or 2.
- You _do_ need to implement both Field-Access-Step and Field-Access-Eval. They correspond to two ways in which you can apply one step a field access `e.f`.
  - If `e -> ep`, then you just return `ep.f` (Field-Access-Step)
  - Otherwise, you apply Field-Access-Eval
- An object maps `str` -> `Method`, not `objc.Var` -> `Method`.
- A MethodOverride can add a new method, not just override an existing one.

This runs my solutions from part 1 in ~1.4s, a little faster than Rylan's!
