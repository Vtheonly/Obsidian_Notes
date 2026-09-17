---
tags: [trees, ast, code]
---

# Abstract Syntax Trees (ASTs)

> An **AST** is a tree representation of the syntactic structure of source code, abstracting away concrete syntax details (whitespace, comments, parentheses) and keeping only semantically meaningful constructs.

## Example

For Python:

```python
if x > 5:
    print(x)
```

The AST is:

```
If
  - test: Compare
      - left: Name(x)
      - op: Gt
      - right: Constant(5)
  - body:
      - Expr
          - Call(func=Name(print), args=[Name(x)])
```

## AST vs Parse Tree

| Parse Tree                     | AST                                          |
| ------------------------------ | -------------------------------------------- |
| Includes all grammar symbols.  | Only semantically meaningful nodes.          |
| Includes parentheses, commas.  | Drops syntactic sugar.                       |
| Verbose.                       | Compact.                                     |
| Used by parsers.               | Used by compilers, analyzers, and AI models. |

## AST-Aware Models

A code generation model is **AST-aware** if it:

- conditions on the AST of the partial output (not just the token sequence),
- predicts the next AST node (not just the next token),
- constrains generation so the output is always a valid AST.

See [[What Is Tree Aware AI]], [[Paper — Tree Based Structure Aware Transformer Decoder for Image To Markup]].

## AST as Tree

ASTs are n-ary rooted ordered trees. They have:

- typed nodes (`If`, `Call`, `Name`, `Constant`),
- typed children (`test`, `body`, `args`),
- order (statements in a block are ordered).

See [[N-ary Trees]], [[Ordered Trees]].

## Related Concepts

- [[Parse Trees]]
- [[Expression Trees]]
- [[Feature Trees]]
- [[What Is Tree Aware AI]]
- [[Grammar Constrained Generation]]
