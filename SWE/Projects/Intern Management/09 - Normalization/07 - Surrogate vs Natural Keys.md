---
tags: [concept, database, keys]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/10 - Primary and Foreign Keys]]
---

# Surrogate vs Natural Keys

## Surrogate key
An artificial ID with no business meaning.
```sql
CREATE TABLE interns (intern_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY, ...);
```
- Pro: stable, simple, no business meaning to change.
- Pro: uniform (every table has `id`).
- Con: an extra column; the "real" identifier still needs a unique constraint.

## Natural key
A real-world identifier used as the PK.
```sql
CREATE TABLE users (email VARCHAR2(100) PRIMARY KEY, ...);
```
- Pro: no extra column.
- Pro: self-documenting (the PK is meaningful).
- Con: can change (user changes email) → cascade updates.
- Con: may not be unique (two people with the same name).
- Con: may be too wide (a long string PK slows joins).

## The recommendation

**Prefer surrogate keys.** Use natural keys as unique constraints:
```sql
CREATE TABLE users (
    user_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email VARCHAR2(100) NOT NULL UNIQUE,
    username VARCHAR2(50) NOT NULL UNIQUE,
    ...
);
```

The surrogate `user_id` is the PK (stable, simple, fast joins). The natural keys (`email`, `username`) are unique constraints (business rules enforced).

## When natural keys are OK

- **Lookup tables** with a stable code: `CREATE TABLE countries (iso_code CHAR(2) PRIMARY KEY, name VARCHAR2(100));`
- **Junction tables** where the composite PK is meaningful: `intern_themes (intern_id, theme_id)`.

## Project Connection

The project uses surrogate keys (`intern_id NUMBER(10)`) — correct. The `requstes.sql` schema uses `VARCHAR2(255)` natural-ish keys — wrong (strings as IDs are slow and fragile).

## Further reading

- *SQL Antipatterns* (Karwin), "ID Required" and "Keyless Entry".
