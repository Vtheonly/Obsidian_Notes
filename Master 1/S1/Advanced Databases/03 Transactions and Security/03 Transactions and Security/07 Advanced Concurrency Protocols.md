# Advanced Concurrency Protocols

While SQL Isolation Levels (Read Committed, Serializable) tell the DBMS *what* anomalies to prevent, **Concurrency Control Protocols** define *how* the engine actually achieves this internally.

There are two primary paradigms: **Pessimistic** (locking) and **Optimistic** (assuming conflicts are rare).

## 1. Lock-Based Protocols (Pessimistic)
Before reading or writing a data item, a transaction acquires an appropriate lock.

### Types of Locks
* **Shared Lock (S-Lock):** Used for reading. Multiple transactions may hold compatible shared locks simultaneously.
* **Exclusive Lock (X-Lock):** Used for writing. Only one transaction can hold an exclusive lock on the item, and it conflicts with shared and exclusive locks from other transactions.

### Lock Compatibility
| Requested / Existing | Shared (S) | Exclusive (X) |
| :--- | :---: | :---: |
| **Shared (S)** | Compatible | Not compatible |
| **Exclusive (X)** | Not compatible | Not compatible |

### Two-Phase Locking (2PL)
To guarantee conflict serializability, a transaction is divided into two phases:

1. **Growing phase:** Acquire locks; no lock is released.
2. **Shrinking phase:** Release locks; no new lock may be acquired after the first release.

Basic 2PL may permit **cascading rollbacks** when a transaction releases an exclusive lock before it commits.

### Strict 2PL
Strict 2PL keeps exclusive locks until `COMMIT` or `ROLLBACK`. This prevents other transactions from reading uncommitted writes and therefore prevents cascading rollback chains caused by dirty writes.

## 2. Timestamp Ordering Protocol (TO)

Timestamp ordering is a non-locking approach. Every transaction receives a unique timestamp `TS(Ti)` when it begins. Each data item `Q` records:

* `read_TS(Q)`: the largest timestamp of a transaction that has successfully read `Q`;
* `write_TS(Q)`: the largest timestamp of a transaction that has successfully written `Q`.

### Read Rule
When `Ti` requests `READ(Q)`:

* If `TS(Ti) < write_TS(Q)`, a newer transaction has already written `Q`, so allowing `Ti` to read it would violate the timestamp order; `Ti` is aborted/restarted.
* Otherwise the read is allowed and `read_TS(Q)` is updated to `max(read_TS(Q), TS(Ti))`.

### Write Rule
For `WRITE(Q)`:

* If `TS(Ti) < read_TS(Q)`, a newer transaction has already read the value, so the write would violate ordering and `Ti` must be aborted under basic timestamp ordering.
* If `TS(Ti) < write_TS(Q)`, a newer transaction has already written `Q`, so the older write is obsolete and is rejected/aborted under the basic protocol.
* Otherwise the write is accepted and `write_TS(Q)` becomes `TS(Ti)`.

### Thomas Write Rule
A refinement called the **Thomas Write Rule** can ignore certain obsolete writes rather than aborting the whole transaction when `TS(Ti) < write_TS(Q)`, provided the write cannot affect the serially ordered result. This can reduce unnecessary aborts.

**Advantage:** No lock waiting means the protocol cannot create classical lock-based deadlocks.

**Disadvantage:** Transactions may be repeatedly aborted and restarted under contention.

## 3. Optimistic Concurrency Control (OCC)

OCC assumes conflicts are rare and postpones conflict checking until commit.

1. **Read/Execute phase:** Read database values and perform changes in private workspace.
2. **Validation phase:** At commit time, check whether concurrent transactions invalidated the assumptions made during execution.
3. **Write phase:** If validation succeeds, publish the private changes; otherwise abort and restart.

Validation may be described using **backward validation** or **forward validation**, depending on which active transactions are compared and how conflicts are detected.

## 4. MVCC (Multi-Version Concurrency Control)

MVCC keeps multiple committed versions of a row rather than forcing every reader to wait for writers.

* An update creates or exposes a new row version.
* A reader uses the version appropriate to its transaction snapshot/isolation semantics.
* Old versions remain temporarily so transactions that still need them can continue reading consistently.
* A background cleanup process eventually removes versions that are no longer visible to any active transaction.

MVCC improves read/write concurrency, but it introduces storage and version-maintenance overhead.

## 5. Deadlocks and Prevention

A deadlock occurs when transactions form a cycle of waits. A wait-for graph represents transactions as nodes and waiting relationships as directed edges.

### Detection
The DBMS can periodically inspect the wait-for graph. A cycle indicates a deadlock. One transaction is selected as the **victim**, rolled back, and its locks are released.

### Wait-Die
A common timestamp-based prevention policy:

* an **older** transaction may wait for a younger transaction;
* a **younger** transaction requesting a lock held by an older transaction is aborted (dies) and restarts with a new timestamp.

### Wound-Wait
Another policy:

* an **older** transaction may abort/wound a younger transaction holding the needed lock;
* a **younger** transaction waits for an older transaction.

These policies impose an ordering on waits so that cycles cannot form.
