---
tags: [verification, neural]
---

# Neural Verification

> **Definition.** *Neural verification* uses a learned model to estimate whether an output satisfies a property.

Unlike [[Formal Verification|formal verification]], neural verification gives a *probabilistic* answer, not a proof.

## Mechanisms

- **Learned validator**: train a classifier on (valid, invalid) pairs; predict validity of new outputs.
- **Critic model**: train a model to predict a score; threshold the score.
- **Adversarial probing**: perturb the input and check if the output remains valid.
- **Differentiable simulation**: run a (differentiable) physics or geometry simulator; the loss is the violation magnitude.

## Strengths

- Fast (one forward pass).
- Handles properties that are hard to formalize.
- Can be trained from data.

## Limitations

- **No guarantee**: a learned validator can be wrong.
- **Generalization**: may fail on out-of-distribution inputs.
- **Adversarial fragility**: small perturbations can fool the validator.

See [[Hard Guarantees vs Statistical Preferences]], [[Formal Verification]], [[Hybrid Verification]].

## Related Concepts

- [[Formal Verification]]
- [[Hybrid Verification]]
- [[Hard Guarantees vs Statistical Preferences]]
