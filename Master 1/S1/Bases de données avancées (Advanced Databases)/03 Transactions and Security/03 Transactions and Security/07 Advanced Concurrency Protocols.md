# Advanced Concurrency Protocols

While SQL Isolation Levels (Read Committed, Serializable) tell the DBMS *what* anomalies to prevent, **Concurrency Control Protocols** define *how* the engine actually achieves this internally.

There are two primary paradigms: **Pessimistic** (Locking, assuming conflicts will happen) and **Optimistic** (Versioning, assuming conflicts are rare).

## 1. Lock-Based Protocols (Pessimistic)
Before reading or writing a data item, a transaction must acquire a lock.

### Types of Locks
*   **Shared Lock (S-Lock):** Required for reading. Multiple transactions can hold S-locks on the same data simultaneously.
*   **Exclusive Lock (X-Lock):** Required for writing/updating. Only **one** transaction can hold an X-lock at a time. It blocks all other S-locks and X-locks.

### Two-Phase Locking (2PL)
To guarantee "Serializability" (the highest isolation level resulting in math strictly equivalent to executing transactions one by one), the DBMS uses the **2PL protocol**. 
A transaction is divided into exactly two phases:
1.  **Growing Phase:** The transaction requests and acquires locks. It *cannot release* any lock.
2.  **Shrinking Phase:** The transaction begins releasing locks. Once it releases its first lock, it *cannot acquire* any new locks.

**The Problem with Basic 2PL:** It can lead to **Cascading Rollbacks**. If Trans A releases an X-lock during its shrinking phase, Trans B might read it. If Trans A then crashes and rolls back, Trans B has read "dirty" data and must also be rolled back.

### Strict 2PL (S2PL)
To fix cascading rollbacks, databases use Strict 2PL.
*   **Rule:** A transaction obeys basic 2PL, but it **holds all Exclusive (X) locks until the very end** (`COMMIT` or `ROLLBACK`). It does not release them gradually. 

## 2. Timestamp Ordering Protocol (TO)
This is a non-locking protocol. Instead of waiting for locks, the system assigns a **Timestamp (TS)** to every transaction when it starts. 

Every piece of data (row or block) keeps track of two timestamps:
*   `Read_TS(Q)`: The timestamp of the youngest transaction that successfully read Q.
*   `Write_TS(Q)`: The timestamp of the youngest transaction that successfully wrote Q.

### The Algorithm Rule
When Transaction $T_i$ issues a command, the DBMS compares $T_i$'s timestamp against the data's timestamps.
*   **Rule of thumb:** "You cannot mess with the future." If a transaction from the "future" (a higher timestamp) has already read or written the data, the older transaction $T_i$ is too late. It is aborted and restarted with a new timestamp.

**Advantages of TO:** No locks mean **Deadlocks are impossible**.
**Disadvantages:** High abort/restart rates in heavily contested environments. 

## 3. Optimistic Concurrency Control (OCC)
In environments where conflicts are very rare (e.g., mostly reading data, like a Wiki or an analytics dashboard), managing locks is a waste of CPU. OCC assumes everything will be fine.

OCC has three phases for a transaction:
1.  **Read & Execute Phase:** The transaction reads data without taking any locks. It performs its updates on a *private local copy* in RAM.
2.  **Validation Phase:** When the transaction attempts to `COMMIT`, the DBMS checks if any other transaction modified the data while we were working.
3.  **Write Phase:** If validation succeeds, the private local changes are copied to the actual database on disk. If it fails, the transaction is discarded (rolled back).

> [!INFO] MVCC (Multi-Version Concurrency Control)
> Modern DBMS like PostgreSQL heavily use MVCC. When you update a row, it doesn't overwrite it. It creates a *new version* of the row. This allows readers to read the old version without being blocked by writers taking X-locks, elegantly solving many concurrency bottlenecks.
