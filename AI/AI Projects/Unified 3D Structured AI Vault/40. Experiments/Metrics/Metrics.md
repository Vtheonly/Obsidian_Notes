---
tags: [experiments, metrics]
---

# Metrics

> **Definition.** Quantitative measures for evaluating structure-aware, tree-aware, and 3D-aware AI systems.

## Validity Metrics

- **Syntactic validity rate**: fraction of outputs that are syntactically valid (parseable).
- **Schema validity rate**: fraction that satisfy the schema.
- **Geometric validity rate**: fraction with valid geometry (watertight, manifold, etc.).
- **Topological validity rate**: fraction with valid topology (connected, no isolated parts).
- **Semantic validity rate**: fraction with valid semantics (correct types, attributes).
- **Code compliance rate**: fraction that satisfy building codes.

## Quality Metrics

- **Per-token accuracy** (for sequence outputs).
- **Tree edit distance** (for tree outputs).
- **Graph edit distance** (for graph outputs).
- **Chamfer distance** (for point clouds).
- **IoU** (for voxel grids / bounding boxes).
- **FID / KID** (for image / 3D generation quality).

## Diversity Metrics

- **Unique outputs**: number of distinct outputs in a sample.
- **Coverage**: fraction of training distribution covered.
- **Mode collapse**: does the model produce only a few modes?

## Efficiency Metrics

- **Inference time**: time per output.
- **Memory**: peak memory.
- **Number of parameters**.

## Why Multiple Metrics

No single metric captures everything. A model can:

- have high validity but low quality (always produces the same trivial output),
- have high quality but low diversity (mode collapse),
- have high diversity but low validity (generates invalid outputs).

See [[Experiment Design]], [[Looks Plausible vs Is Valid]].

## Related Concepts

- [[Experiment Design]]
- [[Baselines]]
- [[Looks Plausible vs Is Valid]]
