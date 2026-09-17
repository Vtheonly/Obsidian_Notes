---
tags: [tree-generation, decoding]
---

# Tree Decoding

> **Definition.** *Tree decoding* generates a tree directly, rather than generating a sequence that happens to encode a tree.

## Three Approaches

1. **Sequence encoding of a tree**: serialize the tree (e.g. pre-order with brackets) and decode token by token. Tree is implicit in the sequence.
2. **Direct tree decoding**: at each step, attach a new node to an existing parent. Tree is explicit.
3. **Constrained tree decoding**: direct tree decoding with structural constraints (max children, allowed node types, etc.).

## Direct Tree Decoding Algorithm

```
Initialize tree with root node.
While not done:
  Pick an open node (one that can still have children).
  Predict: stop (no more children) OR add child of type T.
  If add child:
    Predict child attributes (text, geometry, properties).
    Attach child to parent.
    Add child to open list if it can have children.
Return tree.
```

## Order Matters

The order in which open nodes are expanded affects:

- the model's conditioning (it sees a partial tree),
- the validity of constraints (some constraints are easier to check incrementally),
- the diversity of outputs.

Common orderings: BFS (level by level), DFS (depth first), priority by depth.

## Comparison to Sequence

| Approach               | Pros                                       | Cons                                              |
| ---------------------- | ------------------------------------------ | ------------------------------------------------- |
| Sequence encoding      | Reuses standard Transformers.              | Tree structure is implicit; easy to corrupt.      |
| Direct tree decoding   | Tree is explicit; structure is by construction. | Requires custom decoder; harder to train.        |
| Constrained tree decoding | Hard structural guarantees.             | Most expensive; constraint checking per step.     |

See [[Tree Generation]], [[Top Down Generation]], [[Bottom Up Generation]].

## Related Concepts

- [[Tree Generation]]
- [[Top Down Generation]]
- [[Bottom Up Generation]]
- [[Tree Embeddings and Attention]]
- [[Constrained Decoding]]
