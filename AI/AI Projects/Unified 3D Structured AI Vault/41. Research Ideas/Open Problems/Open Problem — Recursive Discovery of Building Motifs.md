---
tags: [research, open-problem, discovery]
---

# Open Problem — Recursive Discovery of Building Motifs

> **Problem.** Discover recurring structural motifs in buildings at multiple scales (element → component → room → storey → building), and use them as building blocks for generation.

## Why It's Open

- Existing discovery methods focus on single scales.
- Cross-scale motif discovery is hard (different features at different scales).
- Motif overlap and ambiguity.
- Lack of ground truth for evaluation.

## Sub-Problems

1. **Multi-scale feature extraction**: how to extract features at each scale?
2. **Cross-scale motif matching**: how to match motifs across scales?
3. **Motif compression**: which motifs to keep (MDL)?
4. **Generation from motifs**: how to assemble new buildings from discovered motifs?

See [[Recursive Component Discovery]], [[Structural Motif Discovery]], [[Minimum Description Length]].

## Related Concepts

- [[Recursive Component Discovery]]
- [[Structural Motif Discovery]]
- [[Minimum Description Length]]
