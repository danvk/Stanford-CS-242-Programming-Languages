# Homework 5

## Part 1

Straightforward implementation of the state transition diagram. Some things that tripped me up:

- Every loggged-in state is expected to implement acct_num() and tot_cost(). This isn't mentioned in the assignment.
- It's helpful to comment out "part2" in `Cargo.toml` while working on part 1.
- If you create a new, invalid, test, then its name must start with "cart_invalid" for the test runner to pick it up.
- I was surprised there wasn't an `order` method that we were supposed to call at the end.

It's important that methods take a `self` parameter, not `&self`. This means that calling the method ends the lifetime of `self`, so you can't access it any more.

## Part 2

The problem description is a huge wall of text. This is going to be a bit of a slog!
