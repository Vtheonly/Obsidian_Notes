---
tags: [moc, database, transactions, concurrency]
type: moc
status: complete
---

# MOC — Transactions and Concurrency

## Notes (read in order)

1. [[10 - Transactions and Concurrency/01 - ACID Properties]] — Atomicity, Consistency, Isolation, Durability.
2. [[10 - Transactions and Concurrency/05 - Isolation Levels]] — READ UNCOMMITTED to SERIALIZABLE.
3. [[10 - Transactions and Concurrency/08 - MVCC (Multi-Version Concurrency Control)]] — how Oracle/PostgreSQL do it.
4. [[10 - Transactions and Concurrency/06 - Locking (Row, Table, TM, TX)]] — pessimistic locking.
5. [[10 - Transactions and Concurrency/04 - Deadlocks]] — detection and prevention.
6. [[10 - Transactions and Concurrency/11 - Optimistic vs Pessimistic Locking]] — two strategies.
7. [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]] — the project's static Connection bug.
8. [[10 - Transactions and Concurrency/13 - Savepoints and Nested Transactions]] — partial rollback.
9. [[10 - Transactions and Concurrency/14 - Transaction Propagation (Spring)]] — REQUIRED, REQUIRES_NEW, NESTED.
