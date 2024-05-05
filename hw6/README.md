# Homework 6: Continuations

I downloaded Racket from the [downloads] page. In retrospect the [minimal] version would have sufficed, though I did find DrRacket useful for interactive Racketeering. I installed the [Racket extension] for VS Code to get syntax highlighting. Magic Racket looks way fancier, but it also looks harder to set up.

PLT Scheme was [renamed] Racket in 2010. I remember using DrScheme in COMP 210 at Rice way back in 2002.

## Part 1: Exception handling

### Problem 1: throw and try_except

I found this to be the hardest problem by far, mostly because it forced me to understand how `call/cc` worked. Key was realizing that in their example expression:

    (+ 2 (call/cc (lambda (k) (+ 3 (k 4)))))

The `3` is completely irrelevant. It could be anything and this expression would still evaluate to `6`. Any part of your expression after you evaluate the continuation (`k`) is dropped.

The stack stuff was straightforward, the hard part was figuring out how much of the `try_execpt` function needed to be wrapped in `call/cc`. Answer: all of it! You can only "skip" code that's inside `call/cc`, not outside it.

Some Racket notes:

- Lambdas can contain multiple expressions. All are evaluated, with the lambda evaluating to the last one.
- To have multiple expressions in a different context, use `let*`: `(let* () a b c)`.
- For pairs, use `(list a b)`, `(first p)`, `(second p)`.

### Problem 2: Error-detecting calculator

This was very straightforward with `try_except` and `throw`. The important thing is to define an `eval_help` function so that you don't nest `try_except` invocations.

## Part 2: Backtracking algorithm

### Problem 3: attempt and assert

Back to using `call/cc` directly. No hint on this one! The key realization for me was that you can use the same continuation multiple times to create a looping construct.

When I hit an `attempt`, my strategy was to push a `(continuation, rest of options)` pair onto the stack and return `first of options`. Then `assert` can go back when you assert something false. If there are no remaining options, it just pops the stack and returns false. Otherwise it pops the stack, pulls off the next option, and pushes the remaining options (if any) back onto the stack.

I don’t usually think of Scheme as having control flow or an execution order in the way that imperative languages do, but I guess with `let*` it does. It’s interesting that you can re-use a continuation to create looping constructs.

### Problem 4: Sudoku Solver

They give you enough helper functions that this is pretty straightforward. The one wrinkle is that you have to assert that a number is valid *as soon as you add it*. If you attempt all the numbers and only check validity at the end, you get a crazy blowup. This is kind of an elegant way to implement pruning.

With that, I’m able to solve all the Sudokus in less than a second!

[downloads]: https://download.racket-lang.org/
[minimal]: https://download.racket-lang.org/releases/8.12/
[Racket extension]: https://marketplace.visualstudio.com/items?itemName=karyfoundation.racket
[renamed]: http://racket-lang.org/new-name.html
