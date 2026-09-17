---
tags: [research, hypothesis, constrained, repair]
---

# Hypothesis — Constrained Generation vs Generate-Repair

> **Hypothesis.** Constrained generation produces more diverse outputs than generate-validate-repair at similar validity rates, when constraints are cheap to enforce.

## Reasoning

- Constrained generation prevents invalid outputs at each step (hard guarantee).
- Generate-validate-repair generates freely then repairs (may reject many samples).
- If constraints are cheap, constrained generation has lower latency per valid sample.
- Constrained generation may over-restrict diversity if constraints are too tight.

## Experiment

1. Take a BIM generation task with known constraints.
2. Implement two generators: constrained vs generate-validate-repair.
3. Compare validity rate, diversity (e.g. number of unique outputs), and latency.

## Expected Outcome

- Constrained wins on latency.
- Generate-repair wins on diversity (if constraints are tight).
- Trade-off depends on constraint tightness.

See [[Constrained Decoding]], [[Generate Validate Repair]], [[Hard Guarantees vs Statistical Preferences]].

## Related Concepts

- [[Constrained Decoding]]
- [[Generate Validate Repair]]
- [[Hard Guarantees vs Statistical Preferences]]
