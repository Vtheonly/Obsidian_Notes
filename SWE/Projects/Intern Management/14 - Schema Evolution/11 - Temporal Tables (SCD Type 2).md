---
tags: [concept, database, temporal, scd]
type: concept
status: complete
related:
  - [[14 - Schema Evolution/01 - Audit Columns]]
  - [[28 - Observability/01 - Audit Logging]]
---

# Temporal Tables (SCD Type 2)

## What it is

**Slowly Changing Dimensions (SCD)** track how data changes over time. SCD Type 2 keeps the full history by adding a new row for each change, with effective dates.

```sql
CREATE TABLE interns_history (
    intern_id NUMBER,
    name VARCHAR2(100),
    department_id NUMBER,
    valid_from TIMESTAMP,
    valid_to TIMESTAMP,
    PRIMARY KEY (intern_id, valid_from)
);
```

When an intern changes department:
```sql
-- Close the old record
UPDATE interns_history
SET valid_to = SYSTIMESTAMP
WHERE intern_id = 123 AND valid_to IS NULL;

-- Insert the new record
INSERT INTO interns_history (intern_id, name, department_id, valid_from, valid_to)
VALUES (123, 'Alice', 6, SYSTIMESTAMP, NULL);
```

To query "what was Alice's department on 2025-06-01?":
```sql
SELECT department_id FROM interns_history
WHERE intern_id = 123
  AND valid_from <= TIMESTAMP '2025-06-01 00:00:00'
  AND (valid_to IS NULL OR valid_to > TIMESTAMP '2025-06-01 00:00:00');
```

## Why

- **Audit** — full history, not just the last change.
- **Reporting** — "as-of" reports (what was the state on date X?).
- **Compliance** — financial records require historical accuracy.

## Alternatives

- **Event sourcing** — store events (intern_created, intern_department_changed) instead of state. Reconstruct state by replaying.
- **Audit log table** — log every change to a separate `audit_logs` table (see [[28 - Observability/01 - Audit Logging]]).

## Project Connection

The project has no history tracking. The advanced redesign has an `audit_logs` table with before/after JSON snapshots — effectively SCD Type 2 for any table.

For the intern assignments (which change over time), the `intern_assignments` table tracks historical assignments:
```sql
CREATE TABLE intern_assignments (
    assignment_id NUMBER PRIMARY KEY,
    intern_id NUMBER,
    theme_id NUMBER,
    assigned_by NUMBER,
    assignment_date TIMESTAMP,
    status VARCHAR2(20),  -- 'Active', 'Completed', 'Revoked'
    notes VARCHAR2(500)
);
```

An intern can have multiple assignments over time, each with its own status.

## Further reading

- *The Data Warehouse Toolkit* (Kimball) — SCD types.
