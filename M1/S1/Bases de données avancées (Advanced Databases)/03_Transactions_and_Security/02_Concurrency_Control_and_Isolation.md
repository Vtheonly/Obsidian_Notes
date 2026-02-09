

# Concurrency & Isolation Levels

When multiple users access data at the same time, anomalies occur. Isolation levels prevent them.

## Concurrency Anomalies
1.  **Dirty Read:** Reading uncommitted data from another transaction (which might later rollback).
2.  **Non-Repeatable Read:** Reading the same row twice gets different data because someone else updated it.
3.  **Phantom Read:** Running the same query twice returns a different *number* of rows (someone inserted/deleted).

## Isolation Levels (SQL Standard)
| Level | Prevents Dirty? | Prevents Non-Repeatable? | Prevents Phantom? | Performance |
| :--- | :---: | :---: | :---: | :--- |
| **READ UNCOMMITTED** | ❌ | ❌ | ❌ | Fastest |
| **READ COMMITTED** | ✅ | ❌ | ❌ | Fast (Default) |
| **REPEATABLE READ** | ✅ | ✅ | ❌ | Medium |
| **SERIALIZABLE** | ✅ | ✅ | ✅ | Slowest |

## Deadlocks
A situation where Trans A waits for Trans B, and Trans B waits for Trans A.
*   **Solution:** The DBMS detects the cycle and kills one transaction (Victim).