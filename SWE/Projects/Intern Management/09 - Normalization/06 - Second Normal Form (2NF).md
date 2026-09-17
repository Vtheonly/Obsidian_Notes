---
tags: [concept, database, normalization, 2nf]
type: concept
status: complete
prerequisites:
  - [[09 - Normalization/04 - First Normal Form (1NF)]]
---

# Second Normal Form (2NF)

## The rule

A table is in **2NF** if:
1. It is in 1NF.
2. No **partial dependency** — every non-key column depends on the *entire* primary key, not just part of it.

2NF only matters for tables with **composite primary keys**. Tables with single-column PKs are automatically in 2NF if they're in 1NF.

## Violation

```sql
CREATE TABLE intern_assignments (
    intern_id NUMBER,
    theme_id NUMBER,
    intern_name VARCHAR2(100),    -- depends only on intern_id, not on (intern_id, theme_id)
    theme_name VARCHAR2(100),     -- depends only on theme_id
    assignment_date DATE,
    PRIMARY KEY (intern_id, theme_id)
);
```

`intern_name` depends only on `intern_id` (part of the PK). `theme_name` depends only on `theme_id`. These are partial dependencies.

Problems:
- **Redundancy** — `intern_name` is repeated for every theme the intern is assigned to.
- **Update anomaly** — rename the intern in one row, others stay old.
- **Insert anomaly** — can't store an intern's name until they're assigned to a theme.

## Fix

Split into three tables:
```sql
CREATE TABLE interns (intern_id NUMBER PRIMARY KEY, name VARCHAR2(100));
CREATE TABLE themes (theme_id NUMBER PRIMARY KEY, theme_name VARCHAR2(100));
CREATE TABLE intern_assignments (
    intern_id NUMBER REFERENCES interns(intern_id),
    theme_id NUMBER REFERENCES themes(theme_id),
    assignment_date DATE,
    PRIMARY KEY (intern_id, theme_id)
);
```

`intern_name` and `theme_name` live in their own tables. `intern_assignments` only has the FKs and the assignment-specific data.

## Project Connection

The project's `requstes.sql` has `intern` with a composite PK `(group_id, id)` — if any column depends only on `id` (not `group_id`), it's a 2NF violation. The `insertion.sql` schema uses single-column PKs, so it's automatically in 2NF.

## Further reading

- *An Introduction to Database Systems* (Date).
