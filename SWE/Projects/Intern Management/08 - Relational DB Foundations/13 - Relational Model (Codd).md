---
tags: [concept, database, relational-model]
type: concept
status: complete
related:
  - [[09 - Normalization/00 - MOC - Normalization]]
---

# Relational Model (Codd)

## What it is

The **relational model** (Edgar F. Codd, 1970) organizes data into **relations** (tables) of **tuples** (rows) with **attributes** (columns). The model is grounded in set theory and predicate logic.

## Core concepts

- **Relation** — a table with a header (column names + types) and a body (rows).
- **Tuple** — a row; an unordered set of attribute values.
- **Attribute** — a column; a named, typed value.
- **Domain** — the set of allowed values for an attribute.
- **Schema** — the structure (tables, columns, types, constraints).
- **Instance** — the data at a moment in time.

## Relational algebra (the theory)

Operations on relations:
- **Selection** (σ) — filter rows. SQL: `WHERE`.
- **Projection** (π) — pick columns. SQL: `SELECT col1, col2`.
- **Cartesian product** (×) — combine all rows. SQL: `CROSS JOIN`.
- **Join** (⋈) — combine matching rows. SQL: `INNER JOIN`.
- **Union** (∪) — combine same-schema relations. SQL: `UNION`.
- **Difference** (−) — rows in A not in B. SQL: `EXCEPT` / `MINUS`.
- **Rename** (ρ) — rename a relation. SQL: `AS`.

SQL is essentially relational algebra + practical syntax sugar.

## Why this matters

- Tables are sets; SQL operations are set operations. Thinking in sets (not loops) is the key to good SQL.
- The relational model is mathematical — it has well-defined properties (normal forms) that guarantee consistency.
- Understanding the model explains why `NULL` is tricky (it's not a value; it's the absence of a value), why duplicates matter (`SELECT` vs `SELECT DISTINCT`), and why joins work the way they do.

## Project Connection

The project's schema is relational in structure (tables, keys, FKs) but violates the model's spirit:
- `Map<String, Object>` in Java loses the typed attributes.
- Quoted identifiers (`"intern"`) make table names case-sensitive (Codd's model is case-insensitive).
- `theme.responsible` stores a name as a string, not a FK — violates relational integrity.

## Further reading

- Codd, "A Relational Model of Data for Large Shared Data Banks" (1970).
- *SQL and Relational Theory* (C. J. Date).
