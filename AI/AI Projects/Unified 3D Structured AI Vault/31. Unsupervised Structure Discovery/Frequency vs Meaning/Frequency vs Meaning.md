---
tags: [discovery, frequency, meaning]
---

# Frequency vs Meaning

> **The core question of unsupervised structure discovery.**
>
> Repeated observation ≠ meaningful component.

## The Problem

If we observe the same configuration many times, does that mean it's a meaningful component?

- A wall + window + window + door configuration appears 500 times in a building → **probably meaningful** (a typical facade unit).
- A 5-cm sliver of wall appears 10,000 times → **not meaningful** (an artifact of discretization).
- A pair of pixels with the same color appears millions of times → **not meaningful** (raw frequency of low-level features).

## What Makes a Component Meaningful?

A candidate component should be evaluated on multiple criteria, not just frequency:

```text
frequency
+
similarity (internal coherence)
+
geometric consistency
+
structural consistency
+
semantic consistency
+
context consistency
+
topological consistency
+
reusability
−
complexity
```

## Mathematical View

A common formulation is **Minimum Description Length** (MDL):

$$\text{Cost}(D, C) = L(D | C) + L(C)$$

where $D$ is the data, $C$ is the set of discovered components, $L(D | C)$ is the cost of encoding $D$ given $C$, and $L(C)$ is the cost of encoding the components themselves. The best $C$ minimizes total cost.

A component is "worth keeping" if it reduces the total cost — i.e. if encoding its instances plus the residual is cheaper than encoding the raw data.

See [[Minimum Description Length]], [[Candidate Component Scoring]].

## Implication

Naive clustering on raw features (e.g. K-Means on color histograms) finds frequent patterns but not necessarily meaningful ones. To find meaningful components:

1. Use structural features (not just appearance).
2. Score candidates by MDL or similar.
3. Hierarchical / recursive discovery.
4. Context-aware (a component is meaningful if it appears in consistent contexts).

See [[Candidate Component Scoring]], [[Recursive Component Discovery]], [[Minimum Description Length]].

## Related Concepts

- [[Candidate Component Scoring]]
- [[Minimum Description Length]]
- [[Recursive Component Discovery]]
- [[Structural Motif Discovery]]
