# Homework 3b (bonus): Hindley-Milner

Implement Hindley-Milner type inference in `typecheck.py`.

Use your solution for homework 3 as a starting point.
Note that `src/lam.py` has been extended to include a new `PolymorphicType` class. The `Type` class from homework 3 is a subclass of this, but there's also a new `QuantifiedType` class.

Suggested implementation strategy:

- Rework your homework 3 solution to saturate and canonicalize types for each definition one-by-one. A later definition should not influence the type of a previous definition. Note that you'll get more free type variables in your types for each definition than you did before.
- Implement `free_vars(A)` as described in the slides.
- Implement `generalize(A, type)` to generalize a type with type variables into a `QuantifiedType`.
- Update your code to collect types and constraints from homework 3 with the `Inst` rule for polymorphic types from the slides. Whenever you encounter a variable with a polymorphic type, create fresh type variables for each quantified variable in the polymorphic type.

In your `generalize`, you may wish to relabel type variables to make them more readable, e.g. `'a`, `'b`, etc. Quantified type variables only need to be unqiue within a definition, not across the whole program.

Test your solution with:

    python3 src/main.py tests/*.pt
