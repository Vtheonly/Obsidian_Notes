---
tags: [concept, database, normalization, bcnf]
type: concept
status: complete
prerequisites:
  - [[09 - Normalization/08 - Third Normal Form (3NF)]]
related:
  - [[09 - Normalization/09 - What Is Normalization]]
---

# Boyce-Codd Normal Form (BCNF)

## What it is

A relation is in **Boyce-Codd Normal Form (BCNF)** if and only if, for every non-trivial functional dependency `A -> B`, **A is a superkey**. Equivalently: every determinant is a candidate key.

BCNF is slightly stricter than 3NF. The difference shows up only when a table has multiple overlapping candidate keys. 3NF allows a non-key attribute to determine part of a candidate key; BCNF does not.

## The classic BCNF violation

```sql
CREATE TABLE internship_advisor (
    intern_id   NUMBER,
    advisor_id  NUMBER,
    department  VARCHAR2(100),
    PRIMARY KEY (intern_id, advisor_id)
);
```

Business rule: an intern has one advisor per department, and an advisor belongs to exactly one department.

Functional dependencies:
- `(intern_id, advisor_id) -> department` (the PK)
- `advisor_id -> department` (an advisor is in one department)

`advisor_id -> department` has a determinant (`advisor_id`) that is **not a superkey**. BCNF is violated (and so is 2NF, since `department` partially depends on `advisor_id`).

## The BCNF fix

Split so the determinant becomes a key:

```sql
CREATE TABLE advisor (
    advisor_id NUMBER PRIMARY KEY,
    department VARCHAR2(100) NOT NULL
);

CREATE TABLE intern_advisor (
    intern_id  NUMBER,
    advisor_id NUMBER,
    PRIMARY KEY (intern_id, advisor_id),
    FOREIGN KEY (advisor_id) REFERENCES advisor(advisor_id)
);
```

Now `advisor_id -> department` lives in `advisor` where `advisor_id` is the key. BCNF restored.

## Why it matters

BCNF catches a subtle 3NF miss: 3NF says "no non-prime attribute is transitively dependent," but if the transitively-determined attribute is **part of a candidate key**, 3NF lets it slide. BCNF doesn't.

In practice, BCNF violations are rare - they require overlapping candidate keys, which most schemas avoid by using a single surrogate PK.

## Trade-offs

- Some schemas **cannot** be losslessly decomposed into BCNF while preserving all FDs (the dependency-preservation problem). In those cases, 3NF is the practical compromise.
- BCNF can require more tables than 3NF, which adds joins.

## Project Connection

`insertion.sql` uses surrogate PKs everywhere, so it has no overlapping candidate keys, so BCNF is satisfied by construction. The redesign in the reviews keeps this discipline:

```sql
CREATE TABLE intern (
    intern_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ...
    UNIQUE (email)        -- alternate key, not overlapping with PK
);
```

Single-column surrogate PK + UNIQUE alternate key is the simplest path to BCNF.

## Common pitfalls

- Decomposing into BCNF and losing the ability to enforce a CHECK that spans both tables - sometimes you accept 3NF to keep a constraint local.
- Forgetting that BCNF is about **all** candidate keys, not just the PK. A `UNIQUE` constraint creates a candidate key.

## Further reading

- Codd, "Recent Investigations into Relational Data Base Systems" (1974).
- [[09 - Normalization/08 - Third Normal Form (3NF)]]
