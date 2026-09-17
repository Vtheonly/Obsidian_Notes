---
tags: [research, hypothesis, mdl]
---

# Hypothesis — MDL Beats Raw Frequency for Motif Discovery

> **Hypothesis.** Motif discovery using Minimum Description Length (MDL) finds more meaningful motifs than raw frequency counting.

## Reasoning

- Raw frequency counts all repeating patterns, including noise and artifacts.
- MDL penalizes complexity: a motif is kept only if it reduces total description length.
- MDL naturally balances frequency, complexity, and reusability.

## Experiment

1. Take a corpus of buildings.
2. Run two discovery methods: raw frequency counting vs MDL.
3. Compare motifs discovered.
4. Evaluate meaningfulness (human eval, downstream task performance).

## Expected Outcome

- MDL discovers fewer motifs but they are more meaningful.
- Raw frequency discovers many motifs but most are noise / artifacts.

See [[Minimum Description Length]], [[Frequency vs Meaning]], [[Structural Motif Discovery]].

## Related Concepts

- [[Minimum Description Length]]
- [[Frequency vs Meaning]]
- [[Structural Motif Discovery]]
