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
> [!question] According to the ACID properties, **Atomicity** means that if a transaction fails halfway through, the database performs a partial save of the successful operations.
>> [!success]- Answer
>> False

> [!question] In the Write-Ahead Logging (WAL) protocol, the database writes the operation to the log file **before** modifying the actual data files on the disk.
>> [!success]- Answer
>> True

> [!question] Executing a `ROLLBACK TO SAVEPOINT my_marker;` command will automatically end the transaction and release all locks.
>> [!success]- Answer
>> False

> [!question] A **Dirty Read** occurs when a transaction reads data that has been modified by another transaction but has not yet been committed.
>> [!success]- Answer
>> True

> [!question] The **SERIALIZABLE** isolation level offers the highest performance (speed) but the lowest data safety.
>> [!success]- Answer
>> False

> [!question] If a system crashes **after** the `COMMIT` record is written to the log, the recovery process will use the **REDO** mechanism to ensure the data is saved.
>> [!success]- Answer
>> True

> [!question] By default, MySQL runs with `AUTOCOMMIT` enabled, meaning every individual SQL statement is treated as a complete transaction.
>> [!success]- Answer
>> True

> [!question] The **Durability** property guarantees that once a transaction is committed, the changes are permanent, even in the event of a power failure immediately afterward.
>> [!success]- Answer
>> True

> [!question] A **Phantom Read** happens when you read the same row twice within a transaction and get different values because someone else updated that specific row.
>> [!success]- Answer
>> False

> [!question] Using `START TRANSACTION;` inside MySQL will implicitly commit any currently active transaction before starting the new one.
>> [!success]- Answer
>> True

> [!question] Which ACID property ensures that the database moves from one valid state to another, respecting all integrity constraints (like Primary Keys and Foreign Keys)?
> a) Atomicity
> b) Consistency
> c) Isolation
> d) Durability
>> [!success]- Answer
> b) Consistency

> [!question] What is the correct SQL command to manually take control of a transaction and disable the automatic saving of every line?
> a) SET TRANSACTION MANUAL;
> b) START LOGGING;
> c) SET AUTOCOMMIT = 0;
> d) DISABLE COMMIT;
>> [!success]- Answer
> c) SET AUTOCOMMIT = 0;

> [!question] In a Crash Recovery scenario, what action does the DBMS take if it finds a transaction in the log with a `BEGIN` tag but **no** `COMMIT` tag?
> a) REDO
> b) UNDO
> c) ARCHIVE
> d) CHECKPOINT
>> [!success]- Answer
> b) UNDO

> [!question] Which Isolation Level prevents "Dirty Reads" but still allows "Non-Repeatable Reads" and "Phantom Reads"?
> a) READ UNCOMMITTED
> b) READ COMMITTED
> c) REPEATABLE READ
> d) SERIALIZABLE
>> [!success]- Answer
> b) READ COMMITTED

> [!question] What is the specific purpose of the command `SELECT ... FOR UPDATE` inside a transaction?
> a) To speed up the query.
> b) To create a savepoint automatically.
> c) To lock the selected rows so no other transaction can modify them until you commit.
> d) To read data from the archive logs.
>> [!success]- Answer
> c) To lock the selected rows so no other transaction can modify them until you commit.

> [!question] If you execute `ROLLBACK;` (without a savepoint name), what happens to any Savepoints created inside that transaction?
> a) They are saved to a separate file.
> b) They remain active for the next transaction.
> c) They are destroyed/deleted.
> d) They are converted into Commits.
>> [!success]- Answer
> c) They are destroyed/deleted.

> [!question] Which concurrency anomaly involves two transactions reading the same value, both adding to it, and overwriting each other's work (e.g., final stock is 95 instead of 85)?
> a) Dirty Read
> b) Phantom Read
> c) Lost Update
> d) Deadlock
>> [!success]- Answer
> c) Lost Update

> [!question] What defines the "Point of No Return" in a standard SQL transaction?
> a) The `UPDATE` command.
> b) The `SAVEPOINT` command.
> c) The `COMMIT` command.
> d) The `START TRANSACTION` command.
>> [!success]- Answer
> c) The `COMMIT` command.

> [!question] Which mechanism is primarily responsible for ensuring the **Durability** property?
> a) Locking
> b) Write-Ahead Logging (WAL)
> c) Savepoints
> d) Foreign Keys
>> [!success]- Answer
> b) Write-Ahead Logging (WAL)

> [!question] A "Phantom Read" occurs when:
> a) You read uncommitted data.
> b) A row you previously read has been modified by someone else.
> c) You run a query twice and get a different *number* of rows because someone inserted new data.
> d) The database crashes during a read operation.
>> [!success]- Answer
> c) You run a query twice and get a different *number* of rows because someone inserted new data.

> [!question] Match the ACID property with its definition.
>> [!example] Group A
>> a) Atomicity
>> b) Consistency
>> c) Isolation
>> d) Durability
>
>> [!example] Group B
>> n) Transactions must not interfere with each other; intermediate states are invisible to others.
>> o) Changes are permanent once committed, surviving crashes.
>> p) All or Nothing; either all operations succeed or none are applied.
>> q) The transaction must respect all data integrity rules and constraints.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> n)
>> d) -> o)

> [!question] Match the SQL Command with its function.
>> [!example] Group A
>> a) COMMIT
>> b) ROLLBACK
>> c) SAVEPOINT
>> d) START TRANSACTION
>
>> [!example] Group B
>> n) Creates a marker within a transaction to allow partial cancellation.
>> o) Validates changes and makes them visible to other users.
>> p) Marks the beginning of a logical unit of work.
>> q) Cancels all changes and returns the database to its previous state.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> q)
>> c) -> n)
>> d) -> p)

> [!question] Match the Concurrency Anomaly with its description.
>> [!example] Group A
>> a) Dirty Read
>> b) Non-Repeatable Read
>> c) Phantom Read
>> d) Lost Update
>
>> [!example] Group B
>> n) Two users modify the same data, and one overwrite is ignored.
>> o) Reading a row twice yields different values because another user committed an update in between.
>> p) Reading data that has been added by another transaction but not yet committed.
>> q) A query returns a different set of rows (count) when executed a second time due to inserts/deletes.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> q)
>> d) -> n)

> [!question] Match the Isolation Level with its capability.
>> [!example] Group A
>> a) READ UNCOMMITTED
>> b) READ COMMITTED
>> c) REPEATABLE READ
>> d) SERIALIZABLE
>
>> [!example] Group B
>> n) Prevents Dirty Reads, Non-Repeatable Reads, and Phantom Reads.
>> o) Prevents Dirty Reads and Non-Repeatable Reads, but allows Phantom Reads.
>> p) The default in many DBs; prevents Dirty Reads only.
>> q) Allows Dirty Reads, Non-Repeatable Reads, and Phantom Reads (Lowest Safety).
>
>> [!success]- Answer
>> a) -> q)
>> b) -> p)
>> c) -> o)
>> d) -> n)

> [!question] Match the Crash Recovery term with its meaning.
>> [!example] Group A
>> a) WAL
>> b) REDO
>> c) UNDO
>> d) Checkpoint
>
>> [!example] Group B
>> n) Replaying committed transactions found in the log after a crash.
>> o) Reversing uncommitted transactions found in the log after a crash.
>> p) Write-Ahead Logging; writing to the log before the data file.
>> q) A periodic save of memory to disk to speed up recovery.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)
>> d) -> q)

> [!question] Match the Transaction State with its description.
>> [!example] Group A
>> a) Active
>> b) Partially Committed
>> c) Committed
>> d) Aborted
>
>> [!example] Group B
>> n) The transaction has been rolled back and the database is restored.
>> o) The transaction has successfully written the log to disk.
>> p) The initial state where SQL statements are being executed.
>> q) The final statement has been executed, but the log is not yet safely written.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> q)
>> c) -> o)
>> d) -> n)

> [!question] Match the Savepoint scenario with the result.
>> [!example] Group A
>> a) ROLLBACK TO SAVEPOINT X
>> b) ROLLBACK
>> c) COMMIT
>> d) SAVEPOINT Y (created after X)
>
>> [!example] Group B
>> n) Destroys all savepoints (including X and Y) and saves changes.
>> o) Undoes operations done after X, but keeps operations done before X.
>> p) Destroys all savepoints and cancels all changes.
>> q) Creates a new marker; if we roll back to X later, this marker is destroyed.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
>> d) -> q)

> [!question] Match the locking concept with its context.
>> [!example] Group A
>> a) Pessimistic Locking
>> b) Deadlock
>> c) Victim
>> d) Lock Duration (Commit)
>
>> [!example] Group B
>> n) A transaction selected by the DBMS to be killed to resolve a deadlock.
>> o) Situation where Transaction A waits for B, and B waits for A.
>> p) Using `SELECT ... FOR UPDATE` to prevent others from touching data.
>> q) Locks are held until this command is issued.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
>> d) -> q)

> [!question] Match the banking scenario with the required property.
>> [!example] Group A
>> a) Money leaves A and must arrive at B.
>> b) Money cannot be created or destroyed.
>> c) User A cannot see User B's transfer mid-process.
>> d) Server crash cannot erase a confirmed deposit.
>
>> [!example] Group B
>> n) Consistency
>> o) Durability
>> p) Atomicity
>> q) Isolation
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> q)
>> d) -> o)

> [!question] Match the crash timing with the system action.
>> [!example] Group A
>> a) Crash BEFORE Commit
>> b) Crash AFTER Commit (Log written)
>> c) Crash DURING Rollback
>> d) Crash during READ only
>
>> [!example] Group B
>> n) System performs REDO (Roll Forward).
>> o) System performs UNDO (Rollback).
>> p) System continues the UNDO process upon restart.
>> q) No data recovery action needed (no changes pending).
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)
>> d) -> q)