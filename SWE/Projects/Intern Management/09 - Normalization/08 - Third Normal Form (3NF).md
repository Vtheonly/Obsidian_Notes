---
tags: [concept, database, normalization, 3nf]
type: concept
status: complete
prerequisites:
  - [[09 - Normalization/06 - Second Normal Form (2NF)]]
---

# Third Normal Form (3NF)

## The rule

A table is in **3NF** if:
1. It is in 2NF.
2. No **transitive dependency** — every non-key column depends on the key, the whole key, and nothing but the key.

Informally: "no non-key column depends on another non-key column."

## Violation

```sql
CREATE TABLE interns (
    intern_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    department_id NUMBER,
    department_name VARCHAR2(100),   -- depends on department_id, not intern_id
    department_location VARCHAR2(200)  -- same
);
```

`department_name` and `department_location` depend on `department_id` (a non-key column), not on `intern_id` (the key). Transitive dependency.

Problems:
- **Redundancy** — department name repeated for every intern in the department.
- **Update anomaly** — rename the department, update 1000 intern rows.
- **Insert anomaly** — can't add a department until it has an intern.

## Fix

Split:
```sql
CREATE TABLE departments (
    department_id NUMBER PRIMARY KEY,
    department_name VARCHAR2(100),
    location VARCHAR2(200)
);

CREATE TABLE interns (
    intern_id NUMBER PRIMARY KEY,
    name VARCHAR2(100),
    department_id NUMBER REFERENCES departments(department_id)
);
```

## Project Connection

The project's `insertion.sql` schema is in 3NF — departments are in their own table, interns reference them via FK. Good.

But `theme.responsible` (a name string, not a FK) is a 3NF violation — `responsible` depends on the responsible person, not on the theme. The fix: `theme.responsible_id` FK to `users.user_id`.

## Further reading

- *An Introduction to Database Systems* (Date).
