---
tags: [concept, database, keys, relational-model]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/18 - The Relational Model]]
related:
  - [[09 - Normalization/07 - Surrogate vs Natural Keys]]
  - [[08 - Relational DB Foundations/02 - Constraints]]
---

# Keys - Primary, Foreign, Candidate, Surrogate

## What it is

A **key** is a minimal set of attributes that uniquely identifies a tuple.

- **Superkey** - any set of attributes that's unique. `(intern_id, name)` is a superkey if `intern_id` alone is.
- **Candidate key** - a *minimal* superkey. `(intern_id)` is a candidate key; `(intern_id, name)` is not minimal.
- **Primary key (PK)** - the candidate key the designer chooses. Exactly one per table.
- **Alternate key** - a candidate key that wasn't chosen; declared `UNIQUE NOT NULL`.
- **Foreign key (FK)** - an attribute (or set) referencing a PK elsewhere; enforces referential integrity.
- **Surrogate key** - an artificial, system-generated key with no business meaning (an IDENTITY column, a sequence).
- **Natural key** - a key with business meaning (e.g., SSN, email, ISO country code).

## Why it matters

Keys are how the relational model enforces **entity integrity** (you can tell two rows apart) and **referential integrity** (a child points at a real parent). Without them, the database is just a flat file with a query engine.

## SQL declarations

```sql
CREATE TABLE department (
    department_id NUMBER(10)     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name          VARCHAR2(100)  NOT NULL UNIQUE,  -- alternate key
    code          VARCHAR2(10)   NOT NULL UNIQUE
);

CREATE TABLE intern (
    intern_id     NUMBER(10)     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_id NUMBER(10)     NOT NULL,
    name          VARCHAR2(100)  NOT NULL,
    CONSTRAINT fk_intern_department
        FOREIGN KEY (department_id) REFERENCES department(department_id)
        ON DELETE SET NULL
);
```

## Trade-offs: surrogate vs natural

| Aspect | Surrogate | Natural |
|---|---|---|
| Stability | Never changes | Can change (email, SSN) |
| Size | Fixed, small (NUMBER) | Variable (VARCHAR) |
| Meaning | None | Self-describing |
| Joins | Cheap if indexed | Cheaper if already a FK |
| Disclosure | Safe to expose | May leak PII |

See [[09 - Normalization/07 - Surrogate vs Natural Keys]].

## Project Connection

The project has **two conflicting key schemes**:

- `insertion.sql` uses `NUMBER(10)` surrogate keys (`intern_id`, `department_id`, `user_id`).
- `requstes.sql` uses `VARCHAR2(255)` natural-ish keys and even a composite PK `(group_id, id)` on `intern`.

The Java code matches `insertion.sql`, so the surrogate-key choice is "correct," but the IDs are generated in Java via `MAX(id)+1` instead of `IDENTITY` or a `SEQUENCE` - the worst of both worlds. See [[12 - Advanced Database Features/04 - IDENTITY Columns]] for the fix.

## Common pitfalls

- Choosing a natural key that turns out not to be stable (email addresses change).
- Composite PKs that grow with the schema until every child table has a 4-column FK.
- Forgetting that FKs need an index on the child column - see [[11 - DB Performance and Indexing/17 - Missing Indexes on Foreign Keys]].

## Further reading

- [[09 - Normalization/07 - Surrogate vs Natural Keys]]
- [[08 - Relational DB Foundations/02 - Constraints]]
