---
sources:
  - "[[Master Class Database Transactions & Integrity]]"
  - "[[Stopping BEFORE Transaction]]"
  - "[[Transaction Skeleton MySQL]]"
  - "[[Rollback and Commit]]"
  - "[[Savepoint]]"
  - "[[01_ACID_Properties]]"
  - "[[02_Concurrency_Control_and_Isolation]]"
  - "[[03_Crash_Recovery_Mechanisms]]"
---
> [!question] In the context of database recovery, a **Checkpoint** forces the system to re-read the entire log file from the very beginning of the server's history.
>> [!success]- Answer
>> False

> [!question] If a transaction is in the **Active** state and an internal error occurs, the transaction moves to the **Failed** state.
>> [!success]- Answer
>> True

> [!question] The **READ UNCOMMITTED** isolation level is the safest level and prevents all concurrency anomalies, but it is very slow.
>> [!success]- Answer
>> False

> [!question] A **Savepoint** is automatically destroyed if you issue a `COMMIT` command for the transaction that contains it.
>> [!success]- Answer
>> True

> [!question] **Pessimistic Locking** means the database assumes collisions will happen and locks data *before* updating it (e.g., using `FOR UPDATE`).
>> [!success]- Answer
>> True

> [!question] If you perform a `ROLLBACK` (without a savepoint name), the database restores the state to how it was at the last created Savepoint, not the beginning of the transaction.
>> [!success]- Answer
>> False

> [!question] **Atomicity** ensures that money is not created or destroyed during a transfer; the sum of accounts must remain constant.
>> [!success]- Answer
>> False

> [!question] In a **Lost Update** scenario, the final value of a data item is incorrect because one transaction overwrote the results of another transaction without reading its changes.
>> [!success]- Answer
>> True

> [!question] The **Write-Ahead Logging (WAL)** protocol dictates that data modifications must be written to the data file on disk *before* they are written to the log file.
>> [!success]- Answer
>> False

> [!question] If a crash occurs **during** the execution of a `ROLLBACK` command, the system will complete the rollback upon restart to ensure the database is clean.
>> [!success]- Answer
>> True

> [!question] Which Isolation Level is required to prevent **Phantom Reads**?
> a) READ COMMITTED
> b) READ UNCOMMITTED
> c) REPEATABLE READ
> d) SERIALIZABLE
>> [!success]- Answer
> d) SERIALIZABLE

> [!question] When a deadlock is detected between two transactions, what does the DBMS typically do?
> a) It pauses both transactions indefinitely.
> b) It rolls back both transactions completely.
> c) It selects one transaction as a "Victim" and kills/rolls it back.
> d) It automatically commits the transaction that started first.
>> [!success]- Answer
> c) It selects one transaction as a "Victim" and kills/rolls it back.

> [!question] What is the correct SQL syntax to undo changes made only *after* a specific marker named `Step1`?
> a) UNDO Step1;
> b) ROLLBACK TO SAVEPOINT Step1;
> c) GOTO SAVEPOINT Step1;
> d) REVERT TRANSACTION Step1;
>> [!success]- Answer
> b) ROLLBACK TO SAVEPOINT Step1;

> [!question] In the transaction lifecycle, what state is reached immediately after the last SQL statement is executed but *before* the log is safely written to disk?
> a) Active
> b) Committed
> c) Partially Committed
> d) Aborted
>> [!success]- Answer
> c) Partially Committed

> [!question] Which concept allows a user to "undo" a mistake (like `Ctrl+Z`) before making the changes permanent?
> a) Checkpoint
> b) Rollback
> c) Redo
> d) Commit
>> [!success]- Answer
> b) Rollback

> [!question] Why is **Auto-Commit** generally disabled when scripting complex business logic (like a bank transfer)?
> a) To increase the speed of the server.
> b) To prevent the database from saving partial updates if a script fails halfway.
> c) To allow multiple users to edit the same row simultaneously without locks.
> d) To save disk space.
>> [!success]- Answer
> b) To prevent the database from saving partial updates if a script fails halfway.

> [!question] What happens to a transaction that has started (`BEGIN`) but has not yet been committed if the internet connection is lost?
> a) It is automatically committed to save progress.
> b) It pauses and waits for the user to reconnect.
> c) It undergoes an implicit Rollback (Automatic Rollback).
> d) It is saved to a temporary file called a Checkpoint.
>> [!success]- Answer
> c) It undergoes an implicit Rollback (Automatic Rollback).

> [!question] Which anomaly is defined as: "You read a row, someone else updates it and commits, and when you read it again, the value has changed"?
> a) Dirty Read
> b) Non-Repeatable Read
> c) Phantom Read
> d) Lost Update
>> [!success]- Answer
> b) Non-Repeatable Read

> [!question] What is the primary goal of the **Isolation** property in ACID?
> a) To ensure data is written to the hard drive.
> b) To group operations into a single unit.
> c) To ensure transactions run as if they are the only ones in the system.
> d) To check for syntax errors in SQL.
>> [!success]- Answer
> c) To ensure transactions run as if they are the only ones in the system.

> [!question] If the log shows `START T1` and `COMMIT T1` upon restart, what action does the recovery manager take?
> a) UNDO T1
> b) REDO T1
> c) DELETE T1
> d) IGNORE T1
>> [!success]- Answer
> b) REDO T1

> [!question] Match the SQL command with its effect on the Transaction Lifecycle.
>> [!example] Group A
>> a) START TRANSACTION
>> b) UPDATE ...
>> c) ROLLBACK
>> d) COMMIT
>
>> [!example] Group B
>> n) Moves transaction from Active to Aborted/Ended.
>> o) Moves transaction from Active to Committed/Ended.
>> p) Keeps transaction in Active state but modifies data in memory.
>> q) Moves transaction from None to Active state.
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> o)

> [!question] Match the Isolation Level with its typical performance impact.
>> [!example] Group A
>> a) READ UNCOMMITTED
>> b) READ COMMITTED
>> c) REPEATABLE READ
>> d) SERIALIZABLE
>
>> [!example] Group B
>> n) Medium Performance.
>> o) Lowest Performance (Slowest).
>> p) High Performance (Standard Default).
>> q) Highest Performance (Fastest, but unsafe).
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> n)
>> d) -> o)

> [!question] Match the real-world scenario with the ACID failure.
>> [!example] Group A
>> a) Money leaves Account A but never arrives at Account B.
>> b) A user sees a deposit, but the deposit is later cancelled.
>> c) Two users book the last seat on a flight at the same time.
>> d) A confirmed purchase disappears after a server restart.
>
>> [!example] Group B
>> n) Violation of Isolation.
>> o) Violation of Atomicity.
>> p) Violation of Durability.
>> q) Dirty Read (Visibility issue).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the implementation technique with the ACID property it supports.
>> [!example] Group A
>> a) Locking / MVCC
>> b) Write-Ahead Logging (WAL)
>> c) Constraints (FK, PK, Check)
>> d) Commit / Rollback Logic
>
>> [!example] Group B
>> n) Consistency
>> o) Isolation
>> p) Durability
>> q) Atomicity
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the Savepoint action with its description.
>> [!example] Group A
>> a) Define Savepoint
>> b) Rollback To Savepoint
>> c) Release Savepoint
>> d) Nested Savepoint
>
>> [!example] Group B
>> n) Creating a bookmark inside a transaction.
>> o) Reverting changes to a specific point without stopping the transaction.
>> p) Removing a savepoint from memory (happens automatically on commit).
>> q) Creating a savepoint (B) after another savepoint (A) already exists.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Crash Recovery concept with its definition.
>> [!example] Group A
>> a) Transaction Log
>> b) Roll Forward
>> c) Roll Back
>> d) Checkpoint
>
>> [!example] Group B
>> n) Another name for REDO (Re-applying committed changes).
>> o) A sequential file recording all database changes.
>> p) Another name for UNDO (Reversing uncommitted changes).
>> q) A point where memory is synced to disk to shorten recovery time.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)

> [!question] Match the Concurrency Anomaly with the "Read" behavior.
>> [!example] Group A
>> a) Dirty Read
>> b) Non-Repeatable Read
>> c) Phantom Read
>
>> [!example] Group B
>> n) Reading valid data twice gives different values.
>> o) Reading valid data twice gives a different *count* of rows.
>> p) Reading invalid (temporary) data.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the Transaction State with the triggering event.
>> [!example] Group A
>> a) Start -> Active
>> b) Active -> Failed
>> c) Failed -> Aborted
>> d) Partially Committed -> Committed
>
>> [!example] Group B
>> n) Execution of `ROLLBACK`.
>> o) Successful write of the Log to disk.
>> p) Execution of `BEGIN`.
>> q) Logical error (e.g., division by zero) or system crash.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the lock type with its behavior.
>> [!example] Group A
>> a) Shared Lock (Read)
>> b) Exclusive Lock (Write)
>> c) Deadlock
>> d) Auto-Commit
>
>> [!example] Group B
>> n) Allows others to read, but not modify.
>> o) Prevents others from reading or modifying.
>> p) A cycle of waiting that requires a victim.
>> q) Treats every statement as an immediate transaction.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the outcome of a "Stop" (Crash) with the timing.
>> [!example] Group A
>> a) Stop BEFORE Commit
>> b) Stop DURING Commit (Log Write Success)
>> c) Stop DURING Commit (Log Write Fail)
>> d) Stop DURING Rollback
>
>> [!example] Group B
>> n) Data Saved (REDO).
>> o) Data Lost (Implicit Rollback).
>> p) Data Lost (UNDO).
>> q) Data Lost (Rollback completes).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)