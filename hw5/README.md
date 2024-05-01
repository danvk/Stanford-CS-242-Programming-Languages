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

It was helpful to disable part 3. This required commenting out lines in two files:

    part2/src/lib.rs
    part2/tests/lib.rs

Getting errors in VS Code seems to require running `cargo build` with the relevant source file included in the dependency tree.

I didn't bother writing custom tests for part 2.

## Part 3

I found the comment about N=100 in the assignment to be pretty confusing. Is this just saying that infinite recursion is OK because the server will eventually acknowledge all packets that I send? The type signatures of the skeleton code imply that this is the case.

I didn't bother writing custom tests for part 3.
