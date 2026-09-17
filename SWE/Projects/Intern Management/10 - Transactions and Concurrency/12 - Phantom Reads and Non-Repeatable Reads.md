---
tags: [concept, database, transactions, isolation]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/05 - Isolation Levels]]
related:
  - [[10 - Transactions and Concurrency/07 - Locking and Lock Types]]
  - [[10 - Transactions and Concurrency/09 - MVCC - Multi-Version Concurrency Control]]
---

# Phantom Reads and Non-Repeatable Reads

## What it is

Two of the three "read anomalies" the isolation levels trade off. (The third - dirty read - is universally prevented except at READ UNCOMMITTED.)

### Non-repeatable read

Transaction T1 reads a row. Transaction T2 updates or deletes that row and commits. T1 reads the same row again and sees the new value (or no row).

```sql
-- T1
SELECT balance FROM account WHERE id = 1;   -- 100
                                            -- T2: UPDATE account SET balance = 50 WHERE id = 1; COMMIT;
SELECT balance FROM account WHERE id = 1;   -- 50  (non-repeatable read)
```

### Phantom read

Transaction T1 runs a query that returns a set of rows. Transaction T2 inserts or deletes a row that matches T1's predicate and commits. T1 runs the same query and gets a different set.

```sql
-- T1
SELECT COUNT(*) FROM intern WHERE is_accepted = 'Pending';   -- 5
                                                             -- T2: INSERT INTO intern(..., is_accepted) VALUES(..., 'Pending'); COMMIT;
SELECT COUNT(*) FROM intern WHERE is_accepted = 'Pending';   -- 6  (phantom)
```

## The difference

- **Non-repeatable read** - the **same row** has different content. Fixed by REPEATABLE READ (lock the row, or use MVCC snapshot).
- **Phantom read** - the **set of rows** matching a predicate changes. Fixed by SERIALIZABLE (predicate locking, or repeatable snapshot).

You can prevent non-repeatable reads with `SELECT ... FOR UPDATE` even at READ COMMITTED - the lock prevents T2 from updating. But `FOR UPDATE` cannot prevent inserts (no row to lock yet), so phantoms still happen.

## Why it matters

Both anomalies can corrupt business logic that assumes consistency within a transaction:

- A transfer that reads balance, checks it, then debits - a non-repeatable read lets another transaction drain the account between the check and the debit.
- A "find all pending interns" report that pages through results - a phantom lets a new intern appear mid-pagination, getting skipped or duplicated.

## Defenses

| Anomaly | Defense |
|---|---|
| Non-repeatable read | `SELECT ... FOR UPDATE` (pessimistic lock), or REPEATABLE READ, or MVCC snapshot |
| Phantom | SERIALIZABLE, or predicate locking, or MVCC snapshot at transaction start |

Oracle's MVCC gives you **statement-level** snapshot isolation at READ COMMITTED, which prevents non-repeatable reads **within a single statement** but not across statements. At SERIALIZABLE, Oracle gives you **transaction-level** snapshot isolation, which prevents both anomalies.

## Project Connection

The project's `searchIntern` is vulnerable to both - but the symptom is masked by auto-commit. Each `getNameById` call is a separate transaction, so the department name can change between the `SELECT * FROM intern` and the per-row lookup. The user sees an intern listed with a department name that was just renamed.

## Common pitfalls

- Confusing the two. "I set REPEATABLE READ, why do I still see new rows?" - because REPEATABLE READ prevents non-repeatable reads, not phantoms (in the SQL standard; some engines extend it).
- Expecting `FOR UPDATE` to prevent phantoms - it locks existing rows, not future ones.
- Long-running reporting transactions at SERIALIZABLE - they can hit `ORA-01555: snapshot too old` if the undo tablespace is small.

## Further reading

- Berenson et al., "A Critique of ANSI SQL Isolation Levels" (1995).
- [[10 - Transactions and Concurrency/05 - Isolation Levels]]
- [[10 - Transactions and Concurrency/09 - MVCC - Multi-Version Concurrency Control]]
