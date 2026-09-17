---
tags: [concept, database, keys, constraints]
type: concept
status: complete
related:
  - [[09 - Normalization/00 - MOC - Normalization]]
  - [[11 - DB Performance and Indexing/16 - Indexing Foreign Keys]]
---

# Primary and Foreign Keys

## Primary Key (PK)

A **primary key** is a column (or set of columns) that uniquely identifies each row. Constraints:
- Not null.
- Unique.
- Minimal (no unnecessary columns).
- Stable (doesn't change often).

```sql
CREATE TABLE interns (
    intern_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ...
);
```

## Foreign Key (FK)

A **foreign key** is a column (or set of columns) that references the PK of another table. Enforces referential integrity — you can't insert an intern with `theme_id=99` if no theme 99 exists.

```sql
CREATE TABLE interns (
    ...
    theme_id NUMBER(10),
    CONSTRAINT fk_intern_theme FOREIGN KEY (theme_id) REFERENCES themes(theme_id)
);
```

## Cascade rules

When a parent row is deleted/updated, what happens to child rows?

| Rule | Behavior |
|---|---|
| `ON DELETE CASCADE` | Delete the children too. |
| `ON DELETE SET NULL` | Set the child's FK to NULL. |
| `ON DELETE RESTRICT` (default) | Prevent the delete if children exist. |
| `ON DELETE NO ACTION` | Same as RESTRICT. |
| `ON DELETE DEFAULT` | Set the child's FK to its default value. |

Choose carefully:
- `CASCADE` — use when children have no meaning without the parent (e.g., `intern_assignments` when an intern is deleted).
- `SET NULL` — use when children can exist without the parent (e.g., `intern.theme_id` when a theme is deleted).
- `RESTRICT` — use when you want to force explicit handling (e.g., can't delete a department that has users).

## Composite keys

A PK or FK can have multiple columns:
```sql
CREATE TABLE intern_assignments (
    intern_id NUMBER(10),
    intern_start_date DATE,
    theme_id NUMBER(10),
    CONSTRAINT pk_ia PRIMARY KEY (intern_id, intern_start_date, theme_id),
    CONSTRAINT fk_ia_intern FOREIGN KEY (intern_id, intern_start_date)
        REFERENCES interns(intern_id, start_date)
);
```

Composite keys are required when the parent has a composite PK (e.g., partitioned tables).

## Surrogate vs natural keys

- **Surrogate key** — an artificial ID (e.g., `intern_id NUMBER(10)`). No business meaning.
- **Natural key** — a real-world identifier (e.g., `email`, `SSN`). Has business meaning.

**Prefer surrogate keys.** They're stable (email can change), they're simple (one column), and they don't leak business rules into the schema.

## Project Connection

The project uses `NUMBER(10)` surrogate PKs — correct. But:
- `requstes.sql` uses `VARCHAR2(255)` PKs — wrong (strings as IDs).
- `requstes.sql` has a composite PK `(group_id, id)` on `intern` — unnecessary complexity.
- The advanced redesign uses composite PKs on `interns` (`intern_id, start_date`) because the table is partitioned by `start_date` — required for partitioned tables.

## Further reading

- *SQL Antipatterns* (Karwin), Chapter 2 (ID Required).
