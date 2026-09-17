---
tags: [tree-generation, embeddings, attention]
---

# Tree Embeddings and Attention

> How to embed tree nodes and structure attention so the model exploits the tree.

## Tree Embeddings

Each node $v$ is embedded as:

$$e(v) = f_{\text{content}}(\text{content}(v)) + f_{\text{structure}}(\text{position}(v))$$

where:

- $f_{\text{content}}$ is a content embedding (token embedding, attribute embedding).
- $f_{\text{structure}}$ encodes structural position (depth, path from root, parent type, etc.).

See [[Tree Positional Encodings]], [[Structural Embeddings]].

## Tree Attention

Modify attention with structural bias:

$$\text{Attn}_{\text{tree}}(i, j) = \text{softmax}_j\left(\frac{q_i k_j}{\sqrt{d}} + b_{ij}\right)$$

where $b_{ij}$ depends on the tree relationship:

- $b_{ij} = +\infty$ for hard masks (e.g. only attend to descendants).
- $b_{ij} = \beta \cdot g(\text{rel}(i, j))$ for soft bias.

See [[Structural Attention]].

## Tree-Aware Decoding

When decoding a tree, the model conditions on the **partial tree** built so far:

- encode all current nodes (with structural embeddings),
- apply tree-structured attention,
- predict the next action (add child / stop / move to next open node).

This is the core of [[Tree Based Transformers]] and [[Tree Decoding]].

## Related Concepts

- [[Tree Positional Encodings]]
- [[Structural Embeddings]]
- [[Structural Attention]]
- [[Tree Based Transformers]]
- [[Tree Decoding]]
