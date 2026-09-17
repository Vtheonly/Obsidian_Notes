---
tags: [trees, parse-tree, nlp]
---

# Parse Trees

> A **parse tree** is a tree that represents the syntactic structure of a string according to a formal grammar.

## Example

For the grammar:

```
Expr -> Expr + Expr | Expr * Expr | num
```

The string `3 + 4 * 5` parses to:

```
Expr(+)
  - Expr(num: 3)
  - Expr(*)
      - Expr(num: 4)
      - Expr(num: 5)
```

## Why Parse Trees Matter

- They make **syntax explicit**.
- They support **structural disambiguation**: `3 + 4 * 5` parses to `3 + (4 * 5)`, not `(3 + 4) * 5`.
- They are the natural input to compilers, interpreters, and structure-aware models.
- They are the basis for [[Structured Prediction]]: instead of predicting a string, predict the tree.

## Parse Trees vs Abstract Syntax Trees

A parse tree includes **all** grammar symbols (including intermediate non-terminals). An [[Abstract Syntax Trees|AST]] abstracts away intermediate nodes and keeps only semantically meaningful ones.

See [[Parse Trees]] vs [[Abstract Syntax Trees]].

## In This Vault

Parse trees appear in:

- Image-to-LaTeX (mathematical structure trees).
- Image-to-markup (HTML/XML structure trees).
- Code generation (programming language ASTs).
- BIM rule representations (shape grammar trees).

See [[What Is Tree Aware AI]], [[Tree Generation]], [[Grammar Induction]].

## Related Concepts

- [[Abstract Syntax Trees]]
- [[Expression Trees]]
- [[Grammar Constrained Generation]]
- [[Grammar Induction]]
