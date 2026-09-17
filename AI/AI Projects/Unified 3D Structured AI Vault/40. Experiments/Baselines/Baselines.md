---
tags: [experiments, baselines]
---

# Baselines

> **Definition.** Reference systems against which a new method is compared.

## Common Baselines for Structure-Aware AI

- **Sequence-only**: a Transformer that treats the output as a flat sequence.
- **Set-based**: DeepSets that treats the output as an unordered set.
- **No constraints**: same architecture but no constraint enforcement.
- **Generate-only**: no validate-repair loop.
- **Single representation**: e.g. mesh-only, no scene graph.

## Why Baselines Matter

Without baselines, you cannot tell whether your method's success is due to:

- the structure-awareness,
- the constraints,
- the architecture,
- the training data,
- the hyperparameters.

## Selecting Baselines

Choose baselines that isolate the contribution of your novelty:

- If your novelty is structure-awareness, compare to a non-structure-aware baseline with the same architecture.
- If your novelty is constraint enforcement, compare to a non-constrained baseline with the same architecture.
- If your novelty is the validate-repair loop, compare to a generate-only baseline.

See [[Experiment Design]], [[Ablations]].

## Related Concepts

- [[Experiment Design]]
- [[Ablations]]
- [[Metrics]]
