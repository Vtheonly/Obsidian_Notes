---
tags: [tree-generation, top-down]
---

# Top-Down Generation

> **Definition.** *Top-down tree generation* starts from the root and recursively generates children, depth-first or breadth-first.

## Algorithm (DFS)

```
generate(node):
  predict node type and attributes
  predict number of children (or use a stop signal)
  for i in 1..k:
    child = generate_child(parent=node)
    generate(child)  # recurse
  return node
```

## Pros

- Each decision is conditioned on the **complete ancestor path**, which is structurally meaningful.
- Easy to enforce parent-type constraints (e.g. an `If` node must have a `test` and a `body`).
- Natural fit for grammars and schemas.

## Cons

- Errors propagate: a wrong decision at the root affects all descendants.
- Long generation paths; harder to revise early decisions.
- May miss global structure (the model commits to a subtree before seeing siblings).

## Use Cases

- AST generation (root = program node).
- BIM hierarchy generation (root = building).
- Math expression generation (root = top-level operator).

## Comparison

| Approach        | Decides first          | Pros                              | Cons                            |
| --------------- | ---------------------- | --------------------------------- | ------------------------------- |
| Top-down        | Root and ancestors.    | Strong structural conditioning.   | Hard to revise.                 |
| Bottom-up       | Leaves and subtrees.   | Local decisions; easy to compose. | Lacks global context initially. |
| Hybrid          | Skeleton then fill.    | Balance of both.                  | More complex.                   |

See [[Bottom Up Generation]], [[Tree Generation]].

## Related Concepts

- [[Tree Generation]]
- [[Bottom Up Generation]]
- [[Tree Decoding]]
