---
tags: [experiments, design]
---

# Experiment Design

> **Definition.** Designing experiments to evaluate structure-aware, tree-aware, and 3D-aware AI systems.

## Components of an Experiment

1. **Research question**: what are we testing?
2. **Hypothesis**: what do we expect?
3. **Dataset**: training, validation, test.
4. **Metrics**: quantitative measures.
5. **Baselines**: comparison points.
6. **Ablations**: isolate the contribution of each component.
7. **Statistical analysis**: significance, confidence intervals.
8. **Qualitative analysis**: visual inspection, case studies.

## Common Pitfalls

- **No baseline**: a new method without comparison is meaningless.
- **No ablation**: which component contributes?
- **Cherry-picked examples**: show random samples, not just the best.
- **Wrong metric**: a metric that doesn't measure the property of interest.
- **Overfitting to test set**: tuning on test data leaks information.

## In This Vault

For BIM generation:

- Compare tree-aware vs sequence-aware.
- Compare constrained vs generate-validate-repair.
- Compare neural-only vs neural-formal hybrid.
- Ablate: remove structural embeddings, structural attention, constraints.
- Measure: validity rate, diversity, semantic correctness, structural correctness.

See [[Baselines]], [[Metrics]], [[Ablations]].

## Related Concepts

- [[Baselines]]
- [[Metrics]]
- [[Ablations]]
