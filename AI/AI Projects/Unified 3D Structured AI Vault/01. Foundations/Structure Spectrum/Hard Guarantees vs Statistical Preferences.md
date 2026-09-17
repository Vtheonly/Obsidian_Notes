---
tags: [foundations, spectrum, guarantees]
---

# Hard Guarantees vs Statistical Preferences

> **The single most important distinction in this vault.** Does the system *guarantee* a property, or does it merely *prefer* it statistically?

## Hard Guarantee

A hard guarantee means the property *cannot* be violated by any output the system can produce.

Examples:

- A grammar-constrained decoder *cannot* emit syntactically invalid code.
- A tree decoder *cannot* emit a non-tree (by construction).
- An SMT-verified generator *cannot* emit a structure that violates the verified property.

Hard guarantees come from:
- architectural construction (decoder shape),
- constraints enforced at decode time (grammar masks),
- formal verification (proof certificates).

## Statistical Preference

A statistical preference means the system's outputs *tend to* satisfy the property, but violations are possible.

Examples:

- A language model trained on LaTeX *usually* produces valid LaTeX, but sometimes produces unmatched braces.
- A diffusion model trained on watertight meshes *usually* produces watertight meshes, but sometimes produces self-intersecting surfaces.
- A BIM generator trained on real IFC files *usually* produces valid IFC, but sometimes omits required relations.

Statistical preferences come from:
- training data bias,
- loss shaping,
- attention bias,
- embeddings.

## Why This Distinction Is Critical

A paper that says "structure-aware" might mean either. Without checking, you cannot tell whether the system is *safe to deploy* in a setting where invalid outputs matter (engineering, construction, safety-critical code).

## Decision Tree

```
Is the property guaranteed?
  - Yes → Hard guarantee (architectural, constraint, or formal).
  - No  → Statistical preference.
            - How strong is the preference?
                - Strong (low violation rate on test set)
                - Weak (high violation rate)
            - Is there a validator that catches violations?
                - Yes → Detectable (post-hoc)
                - No  → Silent failures possible
```

## Related Concepts

- [[Learning vs Representing vs Using vs Constraining Structure]]
- [[Validating vs Verifying vs Repairing Structure]]
- [[The Awareness Spectrum]]
- [[Explicit Structure vs Implicit Structure]]
