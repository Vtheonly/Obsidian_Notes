---
tags: [validation, bim, model-checking]
---

# Model Checking

> **Definition.** *Model checking* systematically checks whether a model satisfies a set of formally specified properties.

In BIM, model checking typically:

1. Translates the BIM model into a logical representation.
2. Encodes the properties to check as logical predicates.
3. Uses a solver or rule engine to evaluate each predicate.
4. Reports violations.

## Property Languages

- **BCF** (BIM Collaboration Format): issue-oriented.
- **IDS** (Information Delivery Specification): machine-readable requirements.
- **mvdXML**: Model View Definition rules.
- **Custom DSLs**: project-specific rule languages.

## Solvers

- Rule engines (Drools, CLIPS).
- SMT solvers (Z3) for arithmetic and logical constraints.
- Custom interpreters for BIM-specific rules.

## Outputs

- Pass/fail per rule.
- Detailed violation report (which entity, which attribute, what value, what was expected).

See [[BIM Validation]], [[Rule Based Verification]], [[Formal Verification]].

## Related Concepts

- [[BIM Validation]]
- [[Rule Based Verification]]
- [[Formal Verification]]
