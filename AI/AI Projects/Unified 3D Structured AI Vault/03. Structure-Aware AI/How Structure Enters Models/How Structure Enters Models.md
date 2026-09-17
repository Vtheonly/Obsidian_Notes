---
tags: [structure-aware, architecture]
---

# How Structure Enters Models

When a paper claims structure-awareness, the structural information must enter the model *somewhere*. There are only a few possibilities:

## 1. Structural Embeddings

Augment each token/node embedding with structural features:

- parent identity,
- depth,
- position among siblings,
- subtree size,
- path from root.

Effect: structure influences attention *statistically*. Invalid structures are still possible.

See [[Structural Embeddings]], [[Tree Positional Encodings]].

## 2. Structural Attention

Modify attention to bias toward structurally related elements:

- tree-structured mask (attend to ancestor, descendants, siblings),
- graph attention (attend to neighbors in a graph),
- relative positional encoding by tree distance.

Effect: structure influences attention *statistically*.

See [[Structural Attention]], [[Graph Attention]].

## 3. Structural Constraints

Restrict the decoder so invalid structures cannot be produced:

- grammar mask (next token must match grammar),
- schema validator (reject invalid candidates),
- tree decoder (each step attaches a node to an existing parent).

Effect: **hard guarantee** on syntactic structure.

See [[Structural Constraints]], [[Grammar Constrained Generation]].

## 4. Generate Structure First

Predict the skeleton (tree shape, node types) before filling in details:

```
input → predict skeleton → fill attributes → finalize
```

Effect: structure is decided before content. Easier to constrain.

See [[Generate Structure First]], [[Hierarchical Decoders]].

## 5. Tree or Graph Decoder

Emit a tree or graph directly, not a sequence:

- predict parent of each new node,
- predict children of each existing node,
- predict edges between nodes.

Effect: output is a tree/graph by construction.

See [[Tree Decoding]], [[Tree Generation]].

## 6. Grammar-Guided Decoding

Use a grammar to constrain next-token distribution at each step:

- next token must continue a valid prefix of the grammar,
- pre-compute valid next-token mask for each parser state.

Effect: **hard guarantee** on grammatical validity.

See [[Grammar Constrained Generation]], [[Grammar Guided Decoders]].

## 7. Schema Validation in the Loop

After each generation step (or at the end), validate against a schema:

- if valid, accept;
- if invalid, reject and resample (or repair).

Effect: invalid outputs are **detectable** and **recoverable**, not impossible.

See [[Schema Constrained Generation]], [[Generate Validate Repair]].

## How to Read a Paper

For any "X-aware" claim, identify which of the seven mechanisms is used. Each gives a different strength of guarantee — see [[Hard Guarantees vs Statistical Preferences]].

## Related Concepts

- [[Structural Embeddings]]
- [[Structural Attention]]
- [[Structural Constraints]]
- [[Generate Structure First]]
- [[Tree Positional Encodings]]
- [[Graph Attention]]
- [[Tree Based Transformers]]
- [[Graph Neural Networks]]
- [[Hierarchical Decoders]]
- [[Grammar Guided Decoders]]
