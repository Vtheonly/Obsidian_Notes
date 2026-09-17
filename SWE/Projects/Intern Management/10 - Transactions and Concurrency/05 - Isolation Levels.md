---
tags: [concept, database, transactions, isolation]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
related:
  - [[10 - Transactions and Concurrency/08 - MVCC (Multi-Version Concurrency Control)]]
---

# Isolation Levels

## The four standard levels (SQL standard)

| Level | Dirty Read | Non-Repeatable Read | Phantom Read |
|---|---|---|---|
| READ UNCOMMITTED | Possible | Possible | Possible |
| READ COMMITTED | Not | Possible | Possible |
| REPEATABLE READ | Not | Not | Possible |
| SERIALIZABLE | Not | Not | Not |

### Dirty read
Transaction A reads uncommitted data from transaction B. If B rolls back, A read data that never existed.

### Non-repeatable read
Transaction A reads a row, then B updates/deletes it, then A reads again — different result.

### Phantom read
Transaction A runs a query, then B inserts a matching row, then A runs the same query — different number of rows.

## Oracle's levels

Oracle supports **READ COMMITTED** (default) and **SERIALIZABLE**. It does not support READ UNCOMMITTED (never dirty reads) and achieves REPEATABLE READ via MVCC.

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;  -- default
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

## Choosing a level

- **READ COMMITTED** (default) — good for most apps. No dirty reads. Some non-repeatable reads and phantoms, but usually acceptable.
- **REPEATABLE READ** — for reports that need consistency within a transaction.
- **SERIALIZABLE** — strictest. Slowest. Use only when correctness requires it (e.g., financial transactions).

Higher isolation = more locking = less concurrency = slower.

## Project Connection

The project uses auto-commit (effectively READ COMMITTED, one statement per transaction). The fix: explicit transactions with `setAutoCommit(false)` for multi-step operations, keeping the default READ COMMITTED isolation.

## Further reading

- *Designing Data-Intensive Applications* (Kleppmann), Chapter 7.
- Oracle Database Concepts — Data Concurrency and Consistency.
