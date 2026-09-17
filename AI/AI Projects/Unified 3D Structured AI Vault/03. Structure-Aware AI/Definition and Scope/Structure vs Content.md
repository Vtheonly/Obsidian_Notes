---
tags: [structure-aware, definition]
---

# Structure vs Content

Every piece of data carries two kinds of information:

- **Content**: what the elements are.
- **Structure**: how the elements are organized.

## Example

For the LaTeX expression `\frac{x+1}{y-2}`:

- **Content**: the tokens `\frac`, `x`, `+`, `1`, `y`, `-`, `2`.
- **Structure**: the fraction has two children; `x+1` is the numerator; `y-2` is the denominator; `+` is inside the numerator; `-` is inside the denominator.

## Why the Distinction Matters

A model can know all the content while ignoring the structure (e.g. a sequence model). A structure-aware model preserves and exploits the structure.

See [[What Is Structure Aware AI]], [[Learning vs Representing vs Using vs Constraining Structure]].

## Related Concepts

- [[What Is Structure Aware AI]]
- [[Learning vs Representing vs Using vs Constraining Structure]]
