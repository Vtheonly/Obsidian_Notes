---
tags: [concept, database, indexing, foreign-keys]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/01 - B-Tree Index]]
  - [[08 - Relational DB Foundations/10 - Primary and Foreign Keys]]
related:
  - [[10 - Transactions and Concurrency/06 - Locking (Row, Table, TM, TX)]]
---

# Indexing Foreign Keys

## The rule

**Index every foreign key column** unless you have a specific reason not to.

## Why

### 1. Query performance
Joins on unindexed FKs are full scans:
```sql
-- Without index on interns.theme_id:
SELECT * FROM interns i JOIN themes t ON i.theme_id = t.theme_id WHERE t.theme_id = 5;
-- Full scan of interns.
```

### 2. Lock escalation
When you delete or update a parent row, Oracle locks the child table to enforce the FK. Without an index on the child's FK, Oracle escalates to a **table lock**.

```
DELETE FROM departments WHERE department_id = 5;
-- If interns.department_id is NOT indexed: table lock on interns.
-- Every login (which reads users, which may join departments) is blocked.
```

### 3. ON DELETE CASCADE performance
If you have `ON DELETE CASCADE` and the child FK is unindexed, deleting a parent does a full scan of the child for each parent row.

## The exception

If the child table is tiny (e.g., a lookup table with 10 rows), the index may not help. But "tiny" is subjective — when in doubt, index.

## Oracle's behavior

Oracle does **not** automatically index FK columns (unlike what some people assume). You must create the index explicitly.

## Project Connection

The project's schema has FKs but no indexes on FK columns:
- `interns.theme_id` — FK to themes, no index.
- `interns.department_id` — FK to departments, no index.
- `worker_user.department_id` — no index.
- `worker_user.role_id` — no index.
- `worker_user.supervisor_id` — no index.
- `themes.department_id` — no index.

This causes:
- Slow joins (full scans).
- Table locks when deleting parents.
- Slow `ON DELETE CASCADE` / `SET NULL`.

The fix:
```sql
CREATE INDEX idx_interns_theme ON interns(theme_id);
CREATE INDEX idx_interns_dept ON interns(department_id);
CREATE INDEX idx_users_dept ON users(department_id);
CREATE INDEX idx_users_role ON users(role_id);
CREATE INDEX idx_users_supervisor ON users(supervisor_id);
CREATE INDEX idx_themes_dept ON themes(department_id);
```

The advanced redesign includes all these plus local partitioned versions for the partitioned `interns` table.

## Further reading

- Oracle Database SQL Tuning Guide — Indexing Foreign Keys.
