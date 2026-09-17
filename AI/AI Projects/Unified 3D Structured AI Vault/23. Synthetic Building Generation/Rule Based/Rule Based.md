---
tags: [synthetic, rule-based]
---

# Rule-Based Generation

> **Definition.** Generate by applying explicit rules (logical predicates, geometric constraints, shape grammar rules).

See [[Procedural]], [[Shape Grammars]], [[Rule Based Verification]].

## Examples

```
Rule 1: Every building has at least 1 entrance.
Rule 2: Every room has at least 1 door.
Rule 3: Corridor width >= 1.2 m.
Rule 4: Travel distance from any point to exit <= 30 m.
Rule 5: Kitchens have a sink, a stove, a refrigerator.
Rule 6: Bathrooms have a toilet, a sink, a shower or bathtub.
```

A rule-based generator satisfies all rules by construction (or checks them after generation).

## Strengths

- **Transparent**: rules are explicit and auditable.
- **Verifiable**: easy to check rule satisfaction.
- **Domain-friendly**: experts can write rules.

## Limitations

- Rules are rigid; hard to capture preferences.
- Manual rule authoring is expensive.
- Some properties are hard to express as rules (e.g. "feels spacious").

See [[Procedural]], [[Rule Based Verification]], [[Shape Grammars]].

## Related Concepts

- [[Procedural]]
- [[Shape Grammars]]
- [[Rule Based Verification]]
- [[Constrained Generation]]
