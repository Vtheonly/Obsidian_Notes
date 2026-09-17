---
tags: [validation, bim, rules]
---

# Rule-Based Verification

> **Definition.** *Rule-based verification* encodes domain rules as logical predicates and checks each one against the model.

## Example Rules

```
RULE every-space-has-a-door:
  FORALL space IN spaces:
    EXISTS door IN doors:
      door.connects(space)

RULE corridor-width:
  FORALL corridor IN corridors:
    corridor.width >= 1.2

RULE travel-distance:
  FORALL point IN building:
    EXISTS exit IN exits:
      distance(point, exit) <= 30.0
```

## Engines

- Prolog / Datalog (logic programming).
- Drools (production rule system).
- Custom Python with rule DSL.

## Strengths

- Transparent: rules are readable and auditable.
- Composable: rules can be added incrementally.
- Domain-friendly: architects and engineers can write rules.

## Limitations

- Rules must be encoded manually.
- Some properties are hard to express (e.g. stability, which requires simulation).
- Performance can degrade for large rule sets and large models.

See [[BIM Validation]], [[Model Checking]], [[Formal Verification]].

## Related Concepts

- [[BIM Validation]]
- [[Model Checking]]
- [[Formal Verification]]
- [[Semantic Validation]]
