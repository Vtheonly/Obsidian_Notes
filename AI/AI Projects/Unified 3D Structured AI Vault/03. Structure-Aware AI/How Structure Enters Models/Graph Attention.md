---
tags: [structure-aware, graph, attention]
---

# Graph Attention

> **Definition.** *Graph attention* modifies self-attention so that each node attends (preferentially or exclusively) to its graph neighbors.

## Graph Attention Network (GAT)

For a graph $G = (V, E)$, the attention from node $i$ to node $j$ is:

$$\alpha_{ij} = \frac{\exp(\text{LeakyReLU}(a^T [Wh_i || Wh_j]))}{\sum_{k \in \mathcal{N}(i)} \exp(\text{LeakyReLU}(a^T [Wh_i || Wh_k]))}$$

where $\mathcal{N}(i)$ is the neighborhood of $i$ (sometimes including $i$ itself).

The new embedding is:

$$h_i' = \sigma\left(\sum_{j \in \mathcal{N}(i)} \alpha_{ij} W h_j\right)$$

## Variants

- **Multi-head GAT**: multiple attention heads, concatenated or averaged.
- **Edge-typed GAT**: separate attention parameters per edge type.
- **Sparse vs dense**: sparse if $|\mathcal{N}(i)|$ is small; dense if attention is over all nodes.

## Where It Appears

- Scene graph reasoning.
- Molecular graphs.
- Code graphs (data-flow, control-flow).
- Building scene graphs (walls, rooms, doors as nodes; adjacency as edges).

## Strength and Limitation

- **Strength**: lets the model focus on local graph structure.
- **Limitation**: requires the graph to be known (or predicted); still a statistical preference, not a guarantee.

See [[Graph Neural Networks]], [[Structural Attention]].

## Related Concepts

- [[How Structure Enters Models]]
- [[Structural Attention]]
- [[Graph Neural Networks]]
- [[Scene Graph Fundamentals]]
