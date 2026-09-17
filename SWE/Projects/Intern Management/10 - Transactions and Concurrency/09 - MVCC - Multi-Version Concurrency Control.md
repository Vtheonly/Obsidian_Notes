---
tags: [concept, database, transactions, mvcc]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/05 - Isolation Levels]]
related:
  - [[10 - Transactions and Concurrency/07 - Locking and Lock Types]]
  - [[10 - Transactions and Concurrency/12 - Phantom Reads and Non-Repeatable Reads]]
---

# MVCC - Multi-Version Concurrency Control

## What it is

**MVCC** is the concurrency strategy used by Oracle, PostgreSQL, MySQL/InnoDB, and others: each transaction sees a **snapshot** of the database as of a specific point in time. Writers do not block readers; readers do not block writers. Each row may have multiple versions coexisting in the undo tablespace (Oracle) or in row headers (PostgreSQL).

## How Oracle does it

- Every statement gets a **System Change Number (SCN)** - a logical timestamp.
- When a statement reads a row, Oracle reconstructs the row's value **as of the statement's SCN** by applying undo records from the undo tablespace.
- When a transaction updates a row, the old version goes to undo; the new version goes to the data block. Both versions exist until no transaction needs the old one.
- A commit records the new SCN; the undo becomes reclaimable once no active transaction has an older SCN.

The upshot:

- **Readers never block writers, writers never block readers.** A long SELECT does not prevent UPDATEs on the same rows.
- **Statement-level read consistency** at READ COMMITTED: each statement sees the committed data as of its start.
- **Transaction-level read consistency** at SERIALIZABLE: each transaction sees the committed data as of its start (the first statement's SCN).

## The `ORA-01555: snapshot too old` error

MVCC's Achilles heel: if the undo tablespace is too small, old undo records get overwritten before all readers are done with them. A long-running query then hits `ORA-01555`.

Mitigations:
- Size the undo tablespace for your longest expected query (`UNDO_RETENTION`).
- Avoid long-running queries during peak write load.
- Use `DBMS_FLASHBACK.ENABLE_AT_SYSTEM_CHANGE_NUMBER` carefully.

## Why it matters

MVCC is why Oracle can run a 10-second reporting query against a table that's being updated 1000 times per second, with **no blocking**. Lock-based systems (older SQL Server, IBM DB2 with default settings) would block either the reader or the writer for the duration of the query.

MVCC is also why **read-only transactions don't need locks** - they read a consistent snapshot. This dramatically reduces lock contention in read-heavy workloads.

## Trade-offs

- **Space**: MVCC keeps old versions around, so tables and undo tablespaces grow. Vacuuming (PostgreSQL) or undo retention (Oracle) is essential.
- **Write amplification**: every update creates an undo record and a redo log entry, doubling the write IO.
- **Snapshot staleness**: at READ COMMITTED, two statements in the same transaction may see different data (because a new SCN is assigned per statement).

## Project Connection

Oracle's MVCC actually **saves** the project from some of its bugs. The `searchIntern` per-row `getNameById` calls, each a separate auto-commit transaction, see consistent snapshots per-call - so they don't read uncommitted data. But they can see a renamed department mid-iteration, because each call gets a fresh SCN.

The `MAX(id)+1` race, however, MVCC cannot save. Both transactions read the same snapshot, both compute the same max, both try to insert the same ID. The unique constraint on the PK catches the second one - which is the right outcome, but the application gets an exception it didn't expect.

## Common pitfalls

- Assuming MVCC means "no locks at all" - it doesn't. Writers still take row locks (so two concurrent updates to the same row serialize). MVCC only decouples readers from writers.
- Forgetting to size the undo tablespace - long queries hit `ORA-01555`.
- Expecting REPEATABLE READ in Oracle - it's not a separate level; Oracle maps it to SERIALIZABLE.

## Further reading

- Oracle Docs, "Data Concurrency and Consistency".
- Berenson et al., "A Critique of ANSI SQL Isolation Levels" (1995) - the snapshot-isolation framing.
- [[10 - Transactions and Concurrency/05 - Isolation Levels]]
