---
tags: [concept, database, normalization]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/13 - Relational Model (Codd)]]
---

# What Is Normalization?

## What it is

**Normalization** (Codd, 1970s) is the process of organizing a database schema to reduce redundancy and improve data integrity. Each "normal form" is a rule that the schema must satisfy.

## The normal forms

| Form | Rule (informal) | Catches |
|---|---|---|
| 1NF | Atomic values, no repeating groups | Lists in columns |
| 2NF | No partial dependencies (only relevant for composite PKs) | Fields depending on part of a composite key |
| 3NF | No transitive dependencies | Fields depending on non-key fields |
| BCNF | Every determinant is a candidate key | Subtle 3NF violations |
| 4NF | No multi-valued dependencies | Independent multi-valued attributes |
| 5NF | No join dependencies | Decomposition anomalies |
| 6NF | Irreducible (only for temporal DBs) | |

Most practical schemas stop at 3NF or BCNF.

## Why normalize

- **No redundancy** — each fact stored once.
- **No anomalies**:
  - **Insert anomaly** — can't add a department until it has an intern.
  - **Update anomaly** — changing a department's name requires updating every intern in it.
  - **Delete anomaly** — deleting the last intern in a department loses the department.
- **Data integrity** — constraints enforce correctness.
- **Smaller rows** — less storage, faster scans.

## Why denormalize

- **Performance** — joins are expensive. Storing a denormalized copy can be faster for reads.
- **Reporting** — star schemas for OLAP are deliberately denormalized.
- **Caching** — materialized views are denormalized snapshots.

Denormalization is a trade-off: faster reads vs. slower writes + redundancy + anomaly risk.

## Project Connection

The project's schema is mostly normalized (3NF), but:
- `theme.responsible` stores a name (string) instead of a FK — denormalized, causes update anomalies.
- Two conflicting schemas — one normalized, one not.
- Dead tables (`profile`, `function_and_menu`) add noise.

The fix: normalize `theme.responsible` to `theme.responsible_id` (FK to `users`). Drop dead tables.

## Further reading

- Codd, "Further Normalization of the Data Base Relational Model" (1971).
- *An Introduction to Database Systems* (C. J. Date).
