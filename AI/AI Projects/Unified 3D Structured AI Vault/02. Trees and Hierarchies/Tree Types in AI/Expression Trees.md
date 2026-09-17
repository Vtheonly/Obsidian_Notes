---
tags: [trees, expression, math]
---

# Expression Trees

> An **expression tree** is a tree that represents a mathematical expression, where leaves are operands and internal nodes are operators.

## Example

For `(a + b) * c - d`:

```
Subtract
  - Multiply
      - Add
          - a
          - b
      - c
  - d
```

## Why Expression Trees Matter

- They make **operator precedence** and **associativity** explicit (no parentheses needed in the tree).
- They are the natural output of math parsers.
- They are the natural input to math-aware models (e.g. symbolic regression, image-to-LaTeX).
- They are the basis for tree-structured losses in image-to-LaTeX.

## In Image-to-LaTeX

The LaTeX string `\frac{x+1}{y-2}` corresponds to the tree:

```
Fraction
  - Numerator: Add(x, 1)
  - Denominator: Subtract(y, 2)
```

A tree-aware model predicts this tree directly (or uses it to bias token-level prediction).

See [[What Is Tree Aware AI]], [[Paper — Tree Based Structure Aware Transformer Decoder for Image To Markup]].

## Related Concepts

- [[Parse Trees]]
- [[Abstract Syntax Trees]]
- [[Tree Generation]]
