---
tags: [exercise, ast, trees]
---

# Exercise — AST Construction

## Problem

Construct the AST for the Python expression:

```python
(x + 1) * (y - 2)
```

(a) Draw the AST.
(b) Identify the root, leaves, internal nodes.
(c) Compute the depth of each node.
(d) Explain why an AST-aware code generator would benefit from this structure.

## Required Background

- An **AST** is a tree representation of source code. See [[Abstract Syntax Trees]].
- Leaves are operands; internal nodes are operators.
- Depth = distance from the root.

## Correct Answers

### (a) AST

```
        Multiply
        /           Add       Subtract
    /   \      /        x     1    y       2
```

### (b) Root, Leaves, Internal Nodes

- Root: `Multiply`.
- Leaves: `x`, `1`, `y`, `2`.
- Internal nodes: `Multiply`, `Add`, `Subtract`.

### (c) Depths

- `Multiply`: depth 0.
- `Add`, `Subtract`: depth 1.
- `x`, `1`, `y`, `2`: depth 2.

### (d) Why AST-Awareness Helps

An AST-aware code generator:

- Knows that `x + 1` is the left operand of the multiplication, not an independent statement.
- Knows that operator precedence is encoded in the tree (no need to re-derive from parentheses).
- Can use tree-structured attention to focus on the relevant subtree.
- Can constrain generation so the output is always a valid AST (using a tree decoder or grammar mask).

Without AST awareness, a sequence model treats the expression as `x + 1 * y - 2` and may misinterpret precedence.

## Common Mistakes

- Confusing AST with parse tree (parse tree includes intermediate non-terminals; AST does not).
- Forgetting that ASTs are ordered (left child = left operand).

## Edge Cases

- For an expression with associativity (e.g. `a - b - c`), the AST is left-associative: `Subtract(Subtract(a, b), c)`.
- For function calls, the AST has a `Call` node with a function and arguments.

## Implementation Considerations

In Python, the `ast` module provides ASTs. In a code generator, you can use `ast.parse` to validate generated code (a form of post-hoc validation).

## Related Concepts

- [[Abstract Syntax Trees]]
- [[Parse Trees]]
- [[Expression Trees]]
- [[What Is Tree Aware AI]]
- [[Tree Generation]]
