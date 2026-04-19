###  Sources
*   *Based on Images: 1, 4*

### 1. The Transaction Lifecycle
A transaction is a sequence of operations treated as a single unit.

**Standard Cycle:**
1.  **`START TRANSACTION` (or `BEGIN`):** Marks the start.
2.  **Execution:** SQL queries run.
3.  **`COMMIT`:** Saves all changes permanently (Validates).
4.  **`ROLLBACK`:** Cancels all changes since `BEGIN` (used if an error occurs).

> [!TIP] Auto-Commit
> By default, MySQL is in `autocommit` mode (every single line is a transaction). To use multi-line transactions, you must explicitly `START TRANSACTION`.

---

### 2. Concurrency Control & Isolation
When multiple users access data simultaneously, "race conditions" create anomalies.

#### The 4 Concurrency Problems
1.  **Dirty Read:** Transaction A reads data that Transaction B has changed but *not yet committed*. If B rolls back, A has "dirty" (invalid) data.
2.  **Non-Repeatable Read:** Transaction A reads a row. Transaction B updates that row and commits. Transaction A reads the row *again* and gets a different value.
3.  **Phantom Read:** Transaction A reads a set of rows (e.g., `WHERE age > 20`). Transaction B *inserts* a new row that matches that condition. Transaction A runs the query again and sees a "phantom" row appearing out of nowhere.
4.  **Deadlock:** Two transactions block each other.
    *   *Scenario:* A waits for B to release a lock, B waits for A.
    *   *Solution:* The DBMS detects the cycle and kills one transaction (Rollback).

#### Isolation Levels (SQL Standard)
You can set the level using: `SET TRANSACTION ISOLATION LEVEL [LEVEL];`

| Isolation Level | Dirty Read? | Non-Repeatable Read? | Phantom Read? | Locking Strategy |
| :--- | :---: | :---: | :---: | :--- |
| **READ UNCOMMITTED** | ️ Yes | ️ Yes | ️ Yes | No shared locks. Fastest but dangerous. |
| **READ COMMITTED** |  No | ️ Yes | ️ Yes | Locks rows only while reading. (Default in many DBs). |
| **REPEATABLE READ** |  No |  No | ️ Yes | Locks rows found in the first read until commit. (MySQL Default). |
| **SERIALIZABLE** |  No |  No |  No | Locks the entire range/table. Safest but slowest. |

---

### 3. Recovery Mechanisms (Crash Survival)
How does the database ensure **Durability** (the 'D' in ACID) if the server crashes?

#### The Write-Ahead Log (WAL) Principle
**Rule:** The database *must* write the change to the **Log File** (on disk) *before* it writes the change to the actual data file.

**Recovery Process (After a Crash):**
1.  **Detection:** The DB restarts and detects an improper shutdown.
2.  **Analysis:** Reads the Log from the last checkpoint.
3.  **REDO (Roll Forward):** Replays transactions that were **Committed** in the log but hadn't been written to the data file yet.
4.  **UNDO (Roll Back):** Reverses transactions that were **Active (Incomplete)** when the crash happened.

#### Checkpoints
A mechanism to keep the log file size manageable.
*   The DBMS freezes briefly, writes all "dirty pages" (modified data in RAM) to the disk.
*   It marks a "Checkpoint" in the log.
*   **Benefit:** Recovery only needs to scan from the last checkpoint, not the beginning of time.

#### Failure Types
1.  **Transaction Failure:** Logical error (divide by zero) or deadlock. -> *Solved by Rollback.*
2.  **System Crash:** Power loss, OS freeze. RAM is lost. -> *Solved by WAL (Redo/Undo).*
3.  **Disk Failure:** Physical damage to hard drive. -> *Solved by Backups & Replication.*
4.  **Catastrophe:** Fire, flood. -> *Solved by Off-site Backups.*

---