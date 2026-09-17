---
tags: [concept, database, junction-table]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/10 - Primary and Foreign Keys]]
---

# Junction Tables (Associative Entities)

## What it is

A **junction table** (also called bridge table, linking table, associative entity) resolves a many-to-many relationship. It has FKs to both parent tables, and usually a composite PK of those two FKs.

## Many-to-many example

Interns ↔ Themes: an intern can have multiple themes; a theme can have multiple interns.

```sql
CREATE TABLE interns (intern_id NUMBER PRIMARY KEY, ...);
CREATE TABLE themes (theme_id NUMBER PRIMARY KEY, ...);

CREATE TABLE intern_themes (
    intern_id NUMBER REFERENCES interns(intern_id),
    theme_id NUMBER REFERENCES themes(theme_id),
    assigned_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    PRIMARY KEY (intern_id, theme_id)
);
```

`intern_themes` is the junction table. The composite PK `(intern_id, theme_id)` ensures uniqueness. `assigned_at` is extra data specific to the relationship.

## When the junction has its own identity

If the junction has many fields or needs to be referenced by other tables, give it a surrogate PK:
```sql
CREATE TABLE intern_assignments (
    assignment_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    intern_id NUMBER REFERENCES interns(intern_id),
    theme_id NUMBER REFERENCES themes(theme_id),
    assigned_by NUMBER REFERENCES users(user_id),
    assigned_at TIMESTAMP DEFAULT SYSTIMESTAMP,
    status VARCHAR2(20),
    notes VARCHAR2(500),
    UNIQUE (intern_id, theme_id, assigned_at)  -- allow reassignment over time
);
```

Now `intern_assignments` can be referenced by `audit_logs.record_id`.

## Project Connection

The project's `insertion.sql` defines `department_theme`, `responsible_theme`, `theme_intern` junction tables — but none are used by the Java code. The advanced redesign introduces `intern_assignments` (a junction with temporal tracking) to record an intern's movement across themes over time.

## Further reading

- *SQL for Smarties* (Celko).
