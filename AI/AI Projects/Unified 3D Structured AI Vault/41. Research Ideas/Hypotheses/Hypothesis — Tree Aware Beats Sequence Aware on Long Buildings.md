---
tags: [research, hypothesis, tree-aware]
---

# Hypothesis — Tree-Aware Beats Sequence-Aware on Long Buildings

> **Hypothesis.** Tree-aware BIM generation outperforms sequence-aware generation on long, hierarchical buildings.

## Reasoning

- Sequence-aware models treat BIM as a flat sequence; long buildings produce very long sequences.
- Tree-aware models exploit the hierarchy; long buildings are still manageable because each level is short.
- Tree structure provides natural locality (a wall's children are its windows/doors, not random elements far away in the sequence).

## Experiment

1. Take a corpus of large buildings.
2. Train two generators: sequence-aware (Transformer on serialized BIM) vs tree-aware (Tree Transformer).
3. Compare on generation quality, validity, scalability to long buildings.

## Expected Outcome

- Tree-aware wins on long buildings.
- Sequence-aware may be competitive on small buildings.

See [[Tree Based BIM]], [[Tree Based Transformers]], [[Autoregressive BIM]].

## Related Concepts

- [[Tree Based BIM]]
- [[Tree Based Transformers]]
- [[Autoregressive BIM]]
