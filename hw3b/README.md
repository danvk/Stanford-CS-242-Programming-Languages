# Homework 3

## Part 1

This was the most confusing assignment so far. Having implemented it now, I don't think it's _actually_ that confusing, there's just a lot of notation.

Following the instructions as literally as possible helped. The expectations for the "Generating Constraints" section were the least clear to me. Once I was doing something sensible or that, I felt more confident that I could implement the rest.

One key insight was that in the inference rules, the taus indicate types that are already in your environment, whereas alpha and beta indicate "fresh" type variables.

This approach to constraint solving is pretty funny. Blunt but effective!

I had some trouble getting the "infinite" check to work, and I was getting more free type variables in my output than I should have (according to the test file and the `rylan` branch). It turned out that these were the same problem. I was missing a recursive call in `canonicalize`.

Cleaning up the `canonicalizing` set just right proved surprisingly tricky. I wound up using `try/except/finally`, but I'm not totally happy with it.

A final source of confusion was that `tests/n-app-copy.st` just seems wrong:

```
# Ill-typed

def dbl = \x. * x 2;%
```

My program (and Rylan's) both report a type of `dbl: int -> int` which seems correct.

Your program is expected to return a list of types, but the test harness doesn't check them: it only checks whether you say the program is valid or invalid. It would have been nice if it checked the types, too. Some of the comments in the assignment seem wrong, for example:

```
$ cat tests/y-id-check.st
# Well-typed

# Id has inferred type int -> int
def id = \x. x;
```

Both Rylan and I infer the type as `id: a0 -> a0` which, again, seems more correct. I don't know how you'd get an `int` in there.

## Part 2

Part 2 was much easier than part 1.

My initial versions of `value` and `is_div` type checked and ran correctly.

I had more trouble with `sum`. Eventually I realized that the trick was to avoid using `inc`, because the types require that `z: int` and `f: int -> int` in the Church encoding. You can’t have `z` be a Church-encoded number. So you need access to `f` and `z` in the definition of `sum`.

This definitely makes you want polymorphism!
