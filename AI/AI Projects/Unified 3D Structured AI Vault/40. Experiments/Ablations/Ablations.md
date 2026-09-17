---
tags: [experiments, ablations]
---

# Ablations

> **Definition.** Systematically removing components of a system to measure their contribution.

## Common Ablations for Structure-Aware AI

- Remove structural embeddings → measure contribution of structure representation.
- Remove structural attention → measure contribution of structural attention.
- Remove constraints → measure contribution of constraint enforcement.
- Remove validate-repair → measure contribution of repair.
- Remove hierarchy (flatten tree) → measure contribution of hierarchical structure.
- Remove graph relations (use only tree) → measure contribution of graph.

## Ablation Study Design

For each ablation:

1. Remove exactly one component.
2. Keep everything else identical.
3. Re-train (if training is involved).
4. Re-evaluate on the same test set.
5. Compare metrics to the full system.

## Common Pitfalls

- **Multiple ablations at once**: cannot tell which component contributed.
- **Retraining with different seeds**: noise from training, not ablation.
- **Different hyperparameters**: confounds the ablation.

## Why Ablations Matter

A new method may have many components. Without ablations, you cannot tell which component is responsible for the gains.

See [[Experiment Design]], [[Baselines]].

## Related Concepts

- [[Experiment Design]]
- [[Baselines]]
- [[Metrics]]
