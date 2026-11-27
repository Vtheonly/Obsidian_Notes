

# Concurrency & Isolation Levels

When multiple users access data at the same time, anomalies occur. Isolation levels prevent them.

## Concurrency Anomalies
1.  **Dirty Read:** Reading uncommitted data from another transaction (which might later rollback).
2.  **Non-Repeatable Read:** Reading the same row twice gets different data because someone else updated it.
3.  **Phantom Read:** Running the same query twice returns a different *number* of rows (someone inserted/deleted).

## Isolation Levels (SQL Standard)
These levels determine how isolated a transaction is from the changes made by concurrent transactions, and what locking mechanisms the engine typically employs to enforce them.

| Level | Prevents Dirty? | Prevents Non-Repeatable? | Prevents Phantom? | Typical Lock Mechanism Employed | Performance |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **READ UNCOMMITTED** | No | No | No | No shared locks are acquired for reads. Fast, but dangerous. | Fastest |
| **READ COMMITTED** | Yes | No | No | Short-lived shared locks (released immediately after the read statement completes). | Fast (Default) |
| **REPEATABLE READ** | Yes | Yes | No | Long-lived shared locks (held until the end of the transaction). | Medium |
| **SERIALIZABLE** | Yes | Yes | Yes | Range-locks / Predicate locks on the index, or complete table locking. | Slowest |

> [!IMPORTANT] Engine-Specific Behavior (e.g., MySQL InnoDB)
> It is important to note that databases can differ from the standard SQL specification. For example, MySQL's default storage engine, **InnoDB**, uses Multi-Version Concurrency Control (MVCC) and next-key locking. This allows its **REPEATABLE READ** isolation level to prevent phantom reads without the high overhead of full serializability.

## Deadlocks
A situation where Trans A waits for Trans B, and Trans B waits for Trans A.
*   **Solution:** The DBMS detects the cycle and kills one transaction (Victim).