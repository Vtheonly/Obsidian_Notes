---
tags: [tree-generation, bottom-up]
---

# Bottom-Up Generation

> **Definition.** *Bottom-up tree generation* starts from leaves and recursively combines them into larger subtrees until the root is reached.

## Algorithm

```
generate_bottom_up(input):
  leaves = detect_or_predict_leaves(input)
  agenda = priority_queue(leaves)
  while agenda has more than one item:
    pick a subset of items from agenda
    combine into a parent node
    add parent to agenda
  return agenda.pop()  # the root
```

## Pros

- Local decisions are well-grounded in concrete data (leaves).
- Easy to compose: small pieces are merged into bigger ones.
- Naturally parallelizable at each level.

## Cons

- Lacks global context: leaves are decided before the root exists.
- Combining step can be expensive (many possible combinations).
- Hard to enforce top-down constraints (e.g. "the root must be of type X").

## Use Cases

- Scene graph generation (detect objects, then predict relations, then aggregate).
- Constituent parsing in NLP (bottom-up CYK-style).
- Hierarchical clustering.

## Comparison

See [[Top Down Generation]].

## Hybrid

A common hybrid:

1. **Bottom-up**: detect leaves and small motifs.
2. **Top-down**: predict high-level skeleton.
3. **Match**: attach detected leaves to skeleton slots.

See [[Hierarchical Decoders]], [[Generate Structure First]].

## Related Concepts

- [[Top Down Generation]]
- [[Tree Generation]]
- [[Hierarchical Decoders]]
