---
tags: [concept, database, normalization, bcnf]
type: concept
status: complete
prerequisites:
  - [[09 - Normalization/08 - Third Normal Form (3NF)]]
---

# BCNF (Boyce-Codd Normal Form)

## The rule

A table is in **BCNF** if, for every non-trivial functional dependency `X → Y`, X is a superkey.

Informally: BCNF is stricter than 3NF. 3NF allows a non-key column to depend on another non-key column if that column is a candidate key. BCNF doesn't.

## Example

```sql
CREATE TABLE intern_subjects (
    intern_id NUMBER,
    subject VARCHAR2(50),
    instructor VARCHAR2(100),
    PRIMARY KEY (intern_id, subject)
);
```

Rule: each subject has exactly one instructor (so `subject → instructor`), but each instructor teaches only one subject (so `instructor → subject`).

- `subject → instructor` — subject is not a superkey (intern_id+subject is). 3NF violation? No, because `instructor` is part of a candidate key (intern_id+instructor). 3NF allows this.
- But BCNF requires `subject` to be a superkey, which it isn't. BCNF violation.

## Fix

Split:
```sql
CREATE TABLE subjects (subject VARCHAR2 PRIMARY KEY, instructor VARCHAR2);
CREATE TABLE intern_subjects (intern_id NUMBER, subject VARCHAR2 REFERENCES subjects(subject), PRIMARY KEY (intern_id, subject));
```

## When BCNF matters

BCNF violations are rare in practice. Most 3NF schemas are already in BCNF. The cases where 3NF allows but BCNF forbids are subtle (overlapping candidate keys).

## Project Connection

The project's schema doesn't have BCNF violations (no overlapping candidate keys). The advanced redesign maintains BCNF.

## Further reading

- *An Introduction to Database Systems* (Date).
