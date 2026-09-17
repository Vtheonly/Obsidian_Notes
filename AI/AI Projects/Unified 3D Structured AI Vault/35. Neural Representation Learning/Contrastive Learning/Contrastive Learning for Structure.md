---
tags: [neural-rep, contrastive]
---

# Contrastive Learning for Structure

> **Definition.** Learn structure-aware embeddings by contrasting positive pairs (similar structures) against negative pairs (dissimilar structures).

## Idea

Train a network to map similar structures to nearby embeddings and dissimilar structures to far embeddings:

$$\mathcal{L} = -\log \frac{\exp(\text{sim}(z_i, z_j^+) / \tau)}{\sum_k \exp(\text{sim}(z_i, z_k^-) / \tau)}$$

where $z_i$ is the embedding of an anchor, $z_j^+$ is a positive (similar structure), $z_k^-$ are negatives.

## What Counts as Similar?

For structure:

- Same structure type (e.g. two windows).
- Same context (e.g. two windows in similar walls).
- Same motif (e.g. two instances of the same facade motif).
- Augmented versions (e.g. rotated, scaled, re-textured).

## Methods

- **SimCLR**: contrastive learning with augmentations.
- **MoCo**: momentum encoder for more negatives.
- **BYOL**: no negatives; predictor + target network.
- **Structure-specific**: define positives based on structural similarity (e.g. tree edit distance below threshold).

## In Buildings

- Embed building elements by structural context.
- Discover "types" without labels.
- Find similar motifs across buildings.

See [[Embedding Spaces for Structure]], [[Self Supervised Structure Learning]].

## Related Concepts

- [[Embedding Spaces for Structure]]
- [[Self Supervised Structure Learning]]
- [[Embedding Based Clustering]]
