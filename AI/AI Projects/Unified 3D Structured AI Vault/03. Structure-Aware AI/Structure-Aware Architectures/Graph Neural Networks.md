---
tags: [structure-aware, architecture, gnn]
---

# Graph Neural Networks (GNNs)

> **Definition.** A *GNN* learns node embeddings by message passing along graph edges.

## Message Passing

At layer $l$:

$$h_i^{(l+1)} = \phi\left(h_i^{(l)}, \bigoplus_{j \in \mathcal{N}(i)} \psi(h_i^{(l)}, h_j^{(l)}, e_{ij})\right)$$

where $\bigoplus$ is a permutation-invariant aggregator (sum, mean, max), $\phi, \psi$ are learned functions, and $e_{ij}$ are edge features.

## Common Variants

- **GCN** (Kipf & Welling): $h_i' = \sigma(\tilde D^{-1/2} \tilde A \tilde D^{-1/2} H W)$.
- **GAT**: attention-weighted aggregation, see [[Graph Attention]].
- **GIN** (Graph Isomorphism Network): sum aggregator + MLP; as powerful as Weisfeiler-Lehman test.
- **MPNN** (Message Passing Neural Network): general framework for chemical graphs.

## When To Use

- Scene graphs (objects as nodes, relations as edges).
- Building scene graphs (walls/rooms/doors, adjacency).
- Molecular graphs.
- Code graphs (data-flow, control-flow).

## Limitations

- **Over-smoothing**: many layers cause all embeddings to converge.
- **Scalability**: large graphs are expensive.
- **Expressivity**: standard GNNs cannot distinguish all graph pairs (Weisfeiler-Lehman limit).

## Related Concepts

- [[Graph Attention]]
- [[Scene Graph Fundamentals]]
- [[Structural Attention]]
