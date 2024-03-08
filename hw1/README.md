# Homework 1: SKI Calculus

Implementing the rewrite rules was surprisingly easy.

Running the abstraction algorithm by hand was very hard. I found it incredibly easy to make mistakes, especially because the grouping could be unintuitive (it's left-associative). I eventually got frustrated and implemented abstraction in code, which I found much easier.

Part three was fun but the connection between numpy and Combinator Calculus wasn't entirely clear to me.

## Extensions

```
$ cd hw1
$ python enumerate_skis.py
...
```

This will enumerate all SKI expressions, trying to find the shortest ones that have the desired behaviors.

- or: `S I I`
- and: `S S K`
- not: `S (S I S) (K K)`
- is_odd: ??? requires at least 10 combinators.

The shortest expression we know of for `is_odd` is:

    S (S I (K (S (S I (K (S K))) (K K)))) (K (S K))

which has 15 combinators. This reaches a max size of 113 symbols while evaluating `is_odd _3`.
