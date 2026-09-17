---
tags: [validation, semantic]
---

# Semantic Validation

> **Definition.** *Semantic validation* checks that the semantic content of the model is meaningful: types, attributes, co-occurrences, roles.

## Checks

| Check                       | Description                                                            |
| --------------------------- | --------------------------------------------------------------------- |
| Type correctness            | A "door" has the geometry of a door; a "wall" has the geometry of a wall. |
| Attribute correctness       | A "fire-rated door" has a fire-rating attribute ≥ some threshold.      |
| Co-occurrence               | A "kitchen" contains a sink, a stove, a refrigerator.                 |
| Role correctness            | A "load-bearing wall" is marked as load-bearing in the structural model. |
| Domain rules                | A residential building has at least one bathroom per dwelling.         |

## Algorithms

- **Rule-based**: encode domain rules as logical predicates; check all hold.
- **Learned**: train a classifier to detect semantically anomalous configurations.
- **Knowledge graph**: check that the model's entities and relations are consistent with a domain ontology.

## When It Catches Errors

- A "door" that is actually a wall.
- A "kitchen" without a sink.
- A "fire-rated door" missing the fire-rating attribute.
- A residential unit without a bathroom.

## When It Misses

- Wrong geometry (geometric).
- Wrong topology (topological).
- Insufficient support (structural).

See [[Semantic Constraints]], [[BIM Validation]].

## Related Concepts

- [[Geometric Validation]]
- [[Topological Validation]]
- [[Structural Validation]]
- [[Semantic Constraints]]
