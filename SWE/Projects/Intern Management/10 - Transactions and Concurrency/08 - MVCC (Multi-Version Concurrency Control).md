---
tags: [concept, database, mvcc, concurrency]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/05 - Isolation Levels]]
---

# MVCC (Multi-Version Concurrency Control)

## What it is

**MVCC** is a concurrency control technique where each transaction sees a **snapshot** of the database at a point in time. Writers don't block readers; readers don't block writers.

## How it works (Oracle, PostgreSQL)

1. Each row has a **system change number (SCN)** (Oracle) or **xmin/xmax** (PostgreSQL) recording when it was created/deleted.
2. When a transaction starts, it gets a snapshot — "the state of the DB at this SCN."
3. When reading, the transaction sees only rows that existed at its snapshot SCN.
4. When writing, the transaction creates a **new version** of the row; old versions remain for in-progress transactions.

```
Transaction A starts at SCN 100.
Transaction B updates row R (creates version 2 at SCN 101).
Transaction A reads R — still sees version 1 (SCN < 100).
Transaction B commits (SCN 101).
Transaction A still sees version 1 until it ends.
```

## Benefits

- **Readers don't block writers** — readers see the old version.
- **Writers don't block readers** — readers see the old version.
- **Consistent reads** — a transaction sees a stable snapshot.
- **No read locks** — reads don't acquire locks.

## Trade-offs

- **Storage** — old row versions accumulate until no transaction needs them. Vacuuming (PostgreSQL) or undo tablespace (Oracle) cleans up.
- **Write skew** — at REPEATABLE READ, two transactions can each update based on a snapshot, producing an inconsistent result. SERIALIZABLE prevents this.
- **Long-running transactions** — they prevent cleanup of old versions, bloating the table.

## Oracle's undo

Oracle stores old versions in the **undo tablespace**. When a transaction needs an old version, Oracle reconstructs it from the undo. The undo is also used for ROLLBACK.

## Project Connection

The project doesn't use transactions explicitly, so MVCC isn't directly relevant. But the fix (explicit transactions) benefits from MVCC — readers (search) don't block writers (insert).

## Further reading

- *Designing Data-Intensive Applications* (Kleppmann), Chapter 7.
- Oracle Database Concepts — Data Concurrency.
