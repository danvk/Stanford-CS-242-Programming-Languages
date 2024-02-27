# Homework 2

## Part 1

This is a straightforward translation of the `T` and `U` transformations.

This was my first time using Python's [`match` statement][match]. A few thoughts:

- Overall this is really nice!
- It feels a little strange that I have to construct a class to match against it. I guess you mostly want to match about small dataclasses in this way.
- It feels a little strange that I have to write
  ```
  - case lam.App(e1, e2)
  + case lam.App(e1=e1, e2=e2)
  ```
  What does the first one do? Match against an `App` with `e1` set to a local var `e1`?
- I wanted `match` to be an expression, so that I could do `return match…`

## Part 2

I had a few insights about the Lambda Calculus while doing this, so I think the exercise worked! This is dramatically easier to work with than the SKI calculus from part 1.

- Insight: The representation of lists in the lambda calculus _is_ the reduce function. You can implement any list processing operation using `reduce`, so this works out.
- Insight: The number N is a function that applies another function `f` N times. It does pass the numbers 0..N to that function `f`. If you want those numbers, you need to accumulate them yourself.
- Insight: You can implement the last three problems by defining helper functions that operate on pairs.
- Insight: When you have a type error, you get SKI symbols back, rather than lambda calculus symbols.

I had to optimize `ski_eval.py` a bit to get Fibonacci to run. I Ctrl-C'd fib(3) after ~15 minutes and saw this stack trace:

```
  File "/Users/danvk/github/Stanford-CS-242-Programming-Languages/hw2/src/ski.py", line 32, in <lambda>
    __str__ = lambda self: "({} {})".format(self.e1, self.e2)
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  [Previous line repeated 73 more times]
KeyboardInterrupt
```

So `ski_eval.py` was spending all its time formatting SKI expressions. I'd set it up this way as a cheap "deep equals" for the last homework. But since we're not concerned with infinite loops here, I [was able to rewrite it][rewrite] to use reference equality for a dramatic speedup. Still not fast, but better!

I'm able to run `problem.ski` in ~5 minutes.

Rylan's code runs in ~2 minutes! His `problem.lam` is nearly identical. So is his `ski_eval.py` just that much faster? Yes. He's still using string comparison, but he's mutating `ski.App` objects in-place rather than treating them as immutable. Applying that optimization to my `ski_eval.py` gets me down to ~39 seconds. Nearly TA-level performance! Using mutation within `rewrite_s` gets me all the way down to ~2 seconds. WOW!

- `is_zero` is straightforward
- `len`
  - This requires me to understand the list constructors.
  - Intuitively I want to pass in `inc` and `zero` in some way that applies `inc` once for each element of the list.
  - Applying `list` is like calling `reduce`. It takes a base case and a reducer function. I tried passing `inc` as the reducer, but it needs to be `\el. inc` instead.
  - Previously I had `\el. \acc. inc acc` and WOW was that slow!
- `num_zero`
  - Straightforward given the previous idea around lists being reduce
- `fib`
  - I’m packaging `F(n-1)` and `F(n)` in a pair
  - Step: `(a, b) -> (b, a + b)`, base: `(1, 1)`
  - This is really, really slow.
- `dec`
  - Solution is similar to fib
  - Step: `(a, b) -> (b, b + 1)`, base: `(0, 0)`
  - This is also pretty slow, though nowhere near so slow as `fib`.
- `half`
  - Idea: implement in terms of `is_even`. If you’re even, add one. Otherwise don’t.
  - I initially hoped I wouldn't need to use the pair/accumulator trick but I did.
  - Step: `(is_even, count) -> (!is_even, count + is_even ? 1 : 0)`, base: `(0, 0)`

[match]: https://peps.python.org/pep-0636/#pep-636-appendix-a
[rewrite]: https://github.com/danvk/Stanford-CS-242-Programming-Languages/commit/a79d2e996455bdc9a344851e336a5e5ff8113e64
