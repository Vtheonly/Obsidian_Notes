---
tags: [exercise, foundations, spectrum]
---

# Exercise — Structure Spectrum

## Problem

For each of the following mechanisms, identify where it sits on the [[The Awareness Spectrum]] (Implicit / Represented / Used / Constraining / Validating / Verifying / Repairing):

1. A language model trained on LaTeX that tends to produce balanced braces.
2. An AST-aware code generator with a parser-based grammar mask.
3. A BIM generator that emits IFC and then runs IfcOpenShell validation to check the schema.
4. A system that uses an SMT solver to prove every generated wall is vertical.
5. A system that detects an invalid subtree and regenerates it.

## Required Background

- [[The Awareness Spectrum]]: Implicit → Represented → Used → Constraining → Validating → Verifying → Repairing.
- Implicit: structure is only in the data distribution.
- Represented: structure is explicit in inputs/outputs.
- Used: structure influences attention/loss.
- Constraining: structure restricts the output space.
- Validating: a checker tests the output.
- Verifying: a formal prover certifies a property.
- Repairing: invalid parts are rewritten.

## Correct Answers

1. **Implicit**: the model has no explicit structure; it has *learned* that braces tend to balance.
2. **Constraining**: the grammar mask prevents invalid tokens; the output is always syntactically valid.
3. **Validating**: the validator runs after generation and tests schema validity.
4. **Verifying**: the SMT solver provides a formal proof.
5. **Repairing**: the system detects and rewrites invalid parts.

## Step-by-Step Reasoning

For each case, ask:

- Is the structure explicit (data structure) or implicit (in embeddings/distribution)?
- Is the structure used to influence attention/loss, or to restrict output?
- Is there a checker after generation?
- Is there a formal prover?
- Is there a repair loop?

### Case 1

The model has no explicit brace structure. The structure is implicit in the training distribution. So: **Implicit**.

### Case 2

The grammar mask restricts the next token at each step. Invalid tokens are impossible. So: **Constraining**.

### Case 3

The validator runs after generation. It checks but does not prevent. So: **Validating**.

### Case 4

The SMT solver proves a property (verticality). This is a formal certificate. So: **Verifying**.

### Case 5

The system detects and rewrites invalid parts. So: **Repairing**.

## Common Mistakes

- Confusing Constraining and Validating: constraining prevents; validating detects.
- Confusing Verifying and Validating: verifying proves; validating checks.
- Forgetting that Implicit is also a valid stage (not every "structure-aware" claim is explicit).

## Edge Cases

- A system can be at multiple stages simultaneously (e.g. constraining + validating + repairing).
- The strength of the guarantee increases as you move right on the spectrum.

## Related Concepts

- [[The Awareness Spectrum]]
- [[Learning vs Representing vs Using vs Constraining Structure]]
- [[Validating vs Verifying vs Repairing Structure]]
- [[Hard Guarantees vs Statistical Preferences]]
