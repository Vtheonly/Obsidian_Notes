---
tags: [structure-aware, embeddings]
---

# Structural Embeddings

> **Definition.** A *structural embedding* is a vector added to (or concatenated with) a content embedding to encode the structural position of an element.

## Common Structural Features

For a tree node $v$:

- `depth(v)`: distance from root.
- `path_from_root(v)`: list of edge labels.
- `position_among_siblings(v)`: index in parent's children list.
- `parent_type(v)`: type of the parent node.
- `subtree_size(v)`: number of descendants.
- `is_leaf(v)`: boolean.

For a graph node $u$:

- `degree(u)`: number of neighbors.
- `neighbors_types(u)`: types of neighbors.
- `community_id(u)`: cluster assignment.

## Encoding Schemes

- **One-hot**: each depth, each type, etc. has its own dimension. Simple but high-dimensional.
- **Learned**: a small embedding table for each structural feature. Compact and learnable.
- **Fourier**: continuous structural features (like depth, position) encoded with sinusoidal features. Smooth.
- **Path encoding**: the path from root is encoded as a sum (or RNN) of edge embeddings.

## Where It Enters

```
content_embedding(x) + structure_embedding(s) -> fused_embedding -> attention/decoder
```

## Strength and Limitation

- **Strength**: cheap, easy to add, works with any architecture.
- **Limitation**: only a *statistical* preference. Invalid structures are still possible.

See [[Hard Guarantees vs Statistical Preferences]].

## Related Concepts

- [[How Structure Enters Models]]
- [[Tree Positional Encodings]]
- [[Structural Attention]]
