# Homework 3b (bonus): Hindley-Milner and Polymorphic Types

## Part 1: Hindley-Milner

Implement Hindley-Milner type inference in `typecheck.py`.

Use your solution for homework 3 as a starting point.
Note that `src/lam.py` has been extended in two ways:

- It includes a new `PolymorphicType` class. The `Type` class from homework 3 is a subclass of this, but there's also a new `QuantifiedType` class.
- It adds a boolean type, `BoolTp`. Both `BoolTp` and `IntTp` are subtypes of `PrimitiveTp`. The grammar has been extended to include `true` and `false` constants (`BoolConst`) and an `if` function. Having two primitive types makes it easier to test that polymorphism is behaving as expected.

Suggested implementation strategy:

- Add support for `BoolTp` to your homework 3 solution. You'll need to add `bool = int` and `bool = function` as invalid cases.
- Rework your homework 3 solution to saturate and canonicalize types for each definition one-by-one. A later definition should not influence the type of a previous definition. Note that you'll get more free type variables in your types for each definition than you did before.
- Implement `free_vars(A)` as described in the slides.
- Implement `generalize(A, type)` to generalize a type with type variables into a `QuantifiedType`.
- Update your code to collect types and constraints from homework 3 with the `Inst` rule for polymorphic types from the slides. Whenever you encounter a variable with a polymorphic type, create fresh type variables for each quantified variable in the polymorphic type.

In your `generalize`, you may wish to relabel type variables to make them more readable, e.g. `'a`, `'b`, etc. Quantified type variables only need to be unqiue within a definition, not across the whole program.

Test your solution with:

    python3 src/main.py tests/*.pt

Open Questions:

- How would you define a type constructor like `List('a)` in this system?
- The slides show `o → ∀⍺.o | t`. Is it `⍺.o` instead of `⍺.t` to support multiple type variables? If you support that directly, can it be `o → ∀⍺1,...,⍺N.t | t`?
- Is `free_vars` necessary? In my tests, it always evaluates to the empty set.
- I'm unable to use heterogeneous pair types in accumulators in `tests/y-hw2.pt`. Is this a bug in my implementation or a flaw in this type system?

## Part 2: Programming with Polymorphic Types

Implement these three functions in `problem.pt`:

- `map`
- `compose`
- `sum`

The tests are expected to type check and produce the expected results.

Once you've implemented part 1, you can run your code using:

    python3 src/main.py problem.pt
