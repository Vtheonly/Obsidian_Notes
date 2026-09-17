---
tags: [concept, database, triggers, plsql]
type: concept
status: complete
related:
  - [[08 - Relational DB Foundations/PL/SQL Basics]]
  - [[12 - Advanced Database Features/12 - Sequences and IDENTITY Columns]]
---

# Triggers

## What it is

A **trigger** is PL/SQL code that runs automatically when a specific event occurs on a table (INSERT, UPDATE, DELETE).

## Types

### Statement-level
Runs once per statement, regardless of rows affected.
```sql
CREATE TRIGGER audit_interns
AFTER INSERT OR UPDATE OR DELETE ON interns
BEGIN
    INSERT INTO audit_log (action, at_time) VALUES ('interns modified', SYSTIMESTAMP);
END;
```

### Row-level
Runs once per row.
```sql
CREATE TRIGGER update_interns_timestamp
BEFORE UPDATE ON interns
FOR EACH ROW
BEGIN
    :new.updated_at := SYSTIMESTAMP;
END;
```

`:new` refers to the new row values; `:old` refers to the old values.

### BEFORE vs AFTER
- **BEFORE** — can modify `:new` values (validation, default setting).
- **AFTER** — for side effects (audit log, notifications).

## Common uses

1. **Auto-maintain `updated_at`** — set `:new.updated_at = SYSTIMESTAMP` on UPDATE.
2. **Audit logging** — log every change to an audit table.
3. **Enforce complex constraints** — multi-row or cross-table checks.
4. **Derived columns** — compute a column value from others.
5. **Replication** — capture changes for downstream systems.

## Why triggers are controversial

- **Hidden behavior** — a trigger fires automatically; the developer writing the INSERT may not know about it.
- **Performance** — row-level triggers fire for every row; on bulk inserts, they're slow.
- **Cascading** — a trigger on table A updates table B, which has a trigger that updates table C... hard to debug.
- **Ordering** — multiple triggers on the same event fire in an unspecified order (Oracle 11g+ allows ordering with `FOLLOWS`).

## The modern approach: application-side

Many teams avoid triggers and put the logic in the application:
- `updated_at` — set by Hibernate `@PreUpdate` or Spring Data auditing.
- Audit log — written by the service layer.
- Complex constraints — validated in the service.

This makes the behavior visible and testable.

## When triggers are appropriate

- **`updated_at` maintenance** — simple, universal, low-risk.
- **When the application can't be trusted** — multiple apps access the same DB; the trigger enforces consistency.
- **DB-level audit** — for compliance, the audit must be in the DB (apps can be bypassed).

## Project Connection

The advanced redesign uses triggers to maintain `updated_at`:
```sql
CREATE OR REPLACE TRIGGER trg_interns_updated
BEFORE UPDATE ON interns
FOR EACH ROW
BEGIN
    :new.updated_at := SYSTIMESTAMP;
END;
```

This ensures `updated_at` is always correct, even if the application forgets to set it.

## Further reading

- Oracle Database PL/SQL Language Reference — Triggers.
