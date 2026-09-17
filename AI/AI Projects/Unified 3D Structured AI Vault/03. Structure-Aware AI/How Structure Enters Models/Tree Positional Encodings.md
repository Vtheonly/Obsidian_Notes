---
tags: [structure-aware, positional-encoding]
---

# Tree Positional Encodings

> **Definition.** A *tree positional encoding* is a vector that encodes the position of a node in a tree, analogous to how sinusoidal positional encodings encode position in a sequence.

## Why It Is Needed

Sequence Transformers use positional encodings like:

$$PE(pos, 2i) = \sin(pos / 10000^{2i/d})$$

But trees have no linear order. A node has a *path* from the root, not a position.

## Path-Based Encoding

The path from root to node $v$ is a sequence of edge labels (e.g. `left`, `right`, or child indices). Encode this path:

- **RNN**: feed the path through an RNN; final hidden state is the positional encoding.
- **Sum of edge embeddings**: $\text{PE}(v) = \sum_{e \in \text{path}(v)} \phi(e)$.
- **Concatenation**: $\text{PE}(v) = [\phi(e_1); \phi(e_2); \dots]$ (padded to max depth).

## Relative Tree Position

Instead of absolute path, encode the *relative* position between two nodes $u, v$:

- tree distance $d(u, v)$,
- lowest common ancestor $\text{LCA}(u, v)$,
- path from $u$ to $v$ through LCA.

This is the tree analogue of relative positional encoding in sequences.

## Strength and Limitation

- **Strength**: gives the model explicit structural information; improves long-range coherence.
- **Limitation**: only a *statistical* preference.

See [[Structural Embeddings]], [[Structural Attention]].

## Related Concepts

- [[How Structure Enters Models]]
- [[Structural Embeddings]]
- [[Structural Attention]]
- [[Tree Based Transformers]]
