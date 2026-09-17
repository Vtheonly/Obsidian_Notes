---
tags: [discovery, scoring]
---

# Candidate Component Scoring

> **Definition.** A scoring function that evaluates whether a candidate component is "worth keeping" as a discovered structure.

## Multi-Criteria Score

A candidate component $c$ is scored as:

$$S(c) = w_1 \cdot \text{freq}(c) + w_2 \cdot \text{sim}(c) + w_3 \cdot \text{geom}(c) + w_4 \cdot \text{struct}(c) + w_5 \cdot \text{sem}(c) + w_6 \cdot \text{ctx}(c) + w_7 \cdot \text{topo}(c) + w_8 \cdot \text{reuse}(c) - w_9 \cdot \text{complex}(c)$$

where:

- `freq`: number of occurrences.
- `sim`: average internal similarity (coherence).
- `geom`: geometric consistency (sizes, angles within tolerance).
- `struct`: structural consistency (e.g. always has the same children).
- `sem`: semantic consistency (e.g. always a kitchen-with-island).
- `ctx`: context consistency (always appears in the same setting).
- `topo`: topological consistency (always has same adjacency pattern).
- `reuse`: reusability (how easily can it be parameterized and reused).
- `complex`: complexity (number of parts, parameters).

## MDL Alternative

A more principled approach is MDL — see [[Minimum Description Length]]. The score is the description length reduction:

$$S(c) = L(D | \text{without } c) - L(D | \text{with } c)$$

A component is worth keeping if $S(c) > 0$.

## Practical Considerations

- Weights are hard to set; MDL avoids them.
- Some criteria are expensive to compute (topology, context).
- Trade-offs are domain-specific.

See [[Frequency vs Meaning]], [[Minimum Description Length]], [[Structural Motif Discovery]].

## Related Concepts

- [[Frequency vs Meaning]]
- [[Minimum Description Length]]
- [[Structural Motif Discovery]]
- [[Recursive Component Discovery]]
