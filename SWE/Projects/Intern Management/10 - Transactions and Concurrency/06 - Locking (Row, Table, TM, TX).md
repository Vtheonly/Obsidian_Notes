---
tags: [concept, database, locking, concurrency]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
related:
  - [[10 - Transactions and Concurrency/04 - Deadlocks]]
  - [[11 - DB Performance and Indexing/16 - Indexing Foreign Keys]]
---

# Locking (Row, Table, TM, TX)

## What it is

**Locking** is how a database prevents concurrent modifications from corrupting data. When a transaction modifies a row, it locks that row; other transactions wait.

## Oracle lock types

### TX (Transaction) lock
A lock on a transaction's data. Acquired when a transaction modifies a row. Held until COMMIT or ROLLBACK.

### TM (DML) lock
A lock on a table, ensuring the table's structure doesn't change during DML. Acquired during INSERT/UPDATE/DELETE.

### Row-level locks (TX)
- A transaction updating row R holds a lock on R.
- Other transactions can read R (via MVCC) but must wait to update it.
- Row locks are stored in the data block, not in a lock table — scalable.

### Table-level locks (TM)
- Acquired for the duration of a DML statement.
- Modes: Row Share (RS), Row Exclusive (RX), Share (S), Share Row Exclusive (SRX), Exclusive (X).

## The importance of FK indexes

**Unindexed foreign keys cause table-level locks.** When you delete or update a parent row, Oracle locks the child table to enforce the FK constraint. If the FK column is indexed, Oracle can find the affected child rows quickly. If not, Oracle escalates to a **table lock**.

```
DELETE FROM departments WHERE department_id = 5;
-- If interns.department_id is NOT indexed:
--   Oracle locks the entire interns table.
-- If interns.department_id IS indexed:
--   Oracle locks only the affected rows.
```

## Locking modes summary

| Mode | Acronym | Allows |
|---|---|---|
| Row Share | RS | Others to read/write, but not exclusive table lock |
| Row Exclusive | RX | Others to read/write, but not any table lock |
| Share | S | Others to read, but not write |
| Share Row Exclusive | SRX | Others to read, nothing else |
| Exclusive | X | Nothing else |

## Project Connection

The project's schema has no indexes on FK columns:
- `interns.theme_id` — not indexed.
- `interns.department_id` — not indexed.
- `worker_user.department_id`, `worker_user.role_id`, `worker_user.supervisor_id` — not indexed.
- `themes.department_id` — not indexed.

Deleting a department locks the entire `interns` and `worker_user` tables. With indexes, only the affected rows lock.

The fix:
```sql
CREATE INDEX idx_interns_theme ON interns(theme_id);
CREATE INDEX idx_interns_dept ON interns(department_id);
CREATE INDEX idx_users_dept ON worker_user(department_id);
CREATE INDEX idx_users_role ON worker_user(role_id);
CREATE INDEX idx_users_supervisor ON worker_user(supervisor_id);
CREATE INDEX idx_themes_dept ON themes(department_id);
```

See [[11 - DB Performance and Indexing/16 - Indexing Foreign Keys]].

## Further reading

- Oracle Database Concepts — How Oracle Locks Data.
