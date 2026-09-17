# Banking Transaction Walkthrough — End to End

> The transfer flow, traced through every transactional layer: SQL, isolation, locking, MVCC, recovery. This is the integration chapter that ties [[00-ACID]] together.

## What you already know

From [[00-ACID]]: a transaction is atomic, consistent, isolated, durable. From [[02-Isolation-Levels]]: PostgreSQL's levels are READ COMMITTED, REPEATABLE READ (snapshot isolation), SERIALIZABLE (SSI). From [[04-MVCC]]: each row has versions; readers see snapshots. From [[03-Two-Phase-Locking]] and [[06-Deadlocks]]: explicit locking and lock ordering. From [[00-WAL-Logging]] and [[01-ARIES]]: the WAL and recovery.

This note applies all of it to one operation: a transfer of $500 from Alice's checking account to Bob's savings account.

## Why this layer exists

Each transactional concept was taught in isolation in its own chapter. This walkthrough shows them operating *together*, in the order they actually fire, on a single concrete operation. Without this integration, the concepts remain abstract.

## What is genuinely new here

Nothing — by design. This chapter is the integration test. If you understand it, you understand the transactional half of the vault.

## The scenario

- Alice has account #1 (checking), balance $1000, overdraft limit $500.
- Bob has account #2 (savings), balance $200.
- At time T0, Alice initiates a transfer of $500 to Bob.
- Concurrently, another transfer of $700 from Alice to Charlie is in flight.
- The database crashes at a critical moment in one of the variants.

We trace the happy path, then four failure variants.

## The transfer SQL (recap)

From [[09-Banking-SQL]]:

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Lock both accounts in ID order to prevent deadlocks
SELECT id, balance, status, account_type, overdraft_limit
FROM accounts
WHERE id IN (1, 2)
ORDER BY id
FOR UPDATE;

-- Validate source
DO $$ ... $$;  -- check status ACTIVE, balance + overdraft >= amount

-- Insert transfer record (idempotent)
INSERT INTO transfers (source_account_id, destination_account_id, amount, status, idempotency_key)
VALUES (1, 2, 500.00, 'COMPLETED', 'abc-123')
ON CONFLICT (idempotency_key) DO NOTHING
RETURNING id;

-- Debit source
UPDATE accounts SET balance = balance - 500.00, updated_at = NOW() WHERE id = 1;
INSERT INTO ledger_entries (account_id, amount, transfer_id, occurred_at)
VALUES (1, -500.00, (SELECT id FROM transfers WHERE idempotency_key = 'abc-123'), NOW());

-- Credit destination
UPDATE accounts SET balance = balance + 500.00, updated_at = NOW() WHERE id = 2;
INSERT INTO ledger_entries (account_id, amount, transfer_id, occurred_at)
VALUES (2, 500.00, (SELECT id FROM transfers WHERE idempotency_key = 'abc-123'), NOW());

COMMIT;
```

## Happy path — step by step

### Step 1: BEGIN

The client sends `BEGIN`. PostgreSQL starts a transaction, assigns it a transaction ID (e.g., `xid = 1005`). The transaction's snapshot is taken (for SERIALIZABLE, the snapshot is fixed for the whole transaction).

**MVCC state**: the transaction will see data as of this snapshot. Other transactions' uncommitted changes are invisible.

### Step 2: SET TRANSACTION ISOLATION LEVEL SERIALIZABLE

PostgreSQL enables SSI (Serializable Snapshot Isolation). The transaction will track its reads so that conflicts can be detected at commit time.

**WAL**: nothing logged yet.

### Step 3: SELECT ... FOR UPDATE (locks accounts 1 and 2)

PostgreSQL acquires `FOR UPDATE` locks on the rows for accounts 1 and 2 (in ID order — account 1 first, then account 2). These are row-level exclusive locks; they persist until COMMIT or ROLLBACK.

**Lock ordering**: We lock account 1 before account 2 because `1 < 2`. The concurrent transfer (Alice → Charlie, where Charlie is account 3) will also lock account 1 first. This prevents a cycle (cross-link [[06-Deadlocks]]).

**MVCC**: The `SELECT` reads the current committed values (balance = 1000, status = ACTIVE, etc.). Under SSI, this read is tracked as a "read predicate" — if another transaction modifies these rows before our commit, SSI will detect the conflict.

**WAL**: Nothing yet — `SELECT` does not generate WAL.

### Step 4: Validate (DO block)

The PL/pgSQL block checks:
- Source account (1) status is ACTIVE — yes.
- Source balance + overdraft (1000 + 500 = 1500) >= amount (500) — yes.

If either check fails, the block raises an exception, which aborts the transaction (effectively `ROLLBACK`).

**WAL**: Nothing yet.

### Step 5: INSERT into transfers (with ON CONFLICT)

PostgreSQL inserts a new row into `transfers` with status = COMPLETED. The `ON CONFLICT (idempotency_key)` clause means: if a transfer with key `abc-123` already exists, do nothing (and `RETURNING id` returns the existing ID).

**Idempotency**: If the client retries this exact request, the second attempt hits the conflict and returns the existing transfer ID. No double-debit.

**MVCC**: The new row is visible only to this transaction (until commit). Other transactions see nothing.

**WAL**: A WAL record is written for the insert. The record includes the new row's contents and its LSN.

### Step 6: UPDATE accounts (debit source)

```sql
UPDATE accounts SET balance = balance - 500.00, updated_at = NOW() WHERE id = 1;
```

PostgreSQL does not modify the existing row in place. Instead:

1. A *new version* of the row is created with balance = 500.
2. The old version (balance = 1000) is marked as expired (its `xmax` is set to this transaction's xid).
3. The new version's `xmin` is set to this transaction's xid.
4. The new version is written to the page (which may trigger a page split or a new page allocation).

The `FOR UPDATE` lock from step 3 is upgraded to a stronger lock on the new version.

**MVCC**: Other transactions running under READ COMMITTED or REPEATABLE READ still see the old version (balance = 1000) until this transaction commits. Under SERIALIZABLE, they track that they read this row, and SSI will detect the conflict at their commit time.

**WAL**: A WAL record is written for the update. The record includes the before-image (old row) and after-image (new row), or a physiological record (page-level operation).

### Step 7: INSERT into ledger_entries (debit)

A new row is inserted into `ledger_entries` with `amount = -500.00` for account 1.

**WAL**: WAL record written.

### Step 8: UPDATE accounts (credit destination)

Same as step 6, but for account 2: new version with balance = 700, old version (balance = 200) marked expired.

**WAL**: WAL record written.

### Step 9: INSERT into ledger_entries (credit)

A new row with `amount = +500.00` for account 2.

**WAL**: WAL record written.

### Step 10: COMMIT

The client sends `COMMIT`. PostgreSQL:

1. Writes a "commit" WAL record (with the transaction's xid and the commit timestamp).
2. Flushing the WAL to disk (`fsync`) — this is the durability point. Once the commit record is on disk, the transaction is durable.
3. Marks the transaction as committed in shared memory.
4. Releases all locks (the `FOR UPDATE` locks on accounts 1 and 2).
5. Makes the new row versions visible to other transactions.

**After commit**:
- Account 1 balance = 500.
- Account 2 balance = 700.
- Two new ledger entries.
- One new transfer record with status = COMPLETED.
- All locks released.

**WAL**: The commit record is the critical one. If the system crashes after the commit record is flushed, the transaction survives (cross-link [[01-ARIES]] redo pass).

## Variant 1 — Concurrent transfer (the lost update scenario)

Now the concurrent transfer (Alice → Charlie, $700) is in flight. It started after our transaction but before our COMMIT.

### Timeline

```
Time  Our Txn (Alice → Bob, $500)        Concurrent Txn (Alice → Charlie, $700)
T0    BEGIN
T1    SET ISOLATION SERIALIZABLE
T2    SELECT FOR UPDATE accounts 1, 2
T3                                         BEGIN
T4                                         SET ISOLATION SERIALIZABLE
T5                                         SELECT FOR UPDATE accounts 1, 3
T6                                         (blocks — we hold the lock on account 1)
T7    validate, INSERT transfers
T8    UPDATE account 1 (balance 1000→500)
T9    INSERT ledger_entries
T10   UPDATE account 2 (balance 200→700)
T11   INSERT ledger_entries
T12   COMMIT
T13                                        (unblocked — we released the lock)
T14                                        validate: balance = 500, overdraft = 500, 500+500=1000 >= 700 — OK
T15                                        UPDATE account 1 (balance 500→-200)
T16                                        INSERT ledger_entries
T17                                        UPDATE account 3
T18                                        INSERT ledger_entries
T19                                        COMMIT
```

### What happened

At T6, the concurrent transaction tried to lock account 1, but we held the lock. It blocked.

At T12, we committed and released the lock. The concurrent transaction unblocked.

At T14, the concurrent transaction re-read account 1's balance. Under READ COMMITTED, it would see the new balance ($500). Under SERIALIZABLE, SSI detects that the row we modified was one the concurrent transaction had read (in its `SELECT FOR UPDATE`), and aborts it with `SQLSTATE 40001`.

So under SERIALIZABLE, the concurrent transaction is aborted. The application retries it. On retry, it reads balance = $500, checks $500 + $500 >= $700 — yes — and proceeds.

**The point**: SERIALIZABLE prevented a lost update at the cost of one retry. Under READ COMMITTED, the concurrent transaction would have proceeded based on the stale balance ($1000), checked $1000 + $500 >= $700 — yes — and debited $700, leaving balance = $500 - $700 = -$200. This is within the overdraft, so no constraint violation — but the *check* was based on stale data. The customer might not have wanted to overdraw that far.

Under SERIALIZABLE, the system correctly detects that the two transactions conflicted and forces one to retry.

## Variant 2 — The deadlock

Suppose we did *not* lock in ID order. Our transaction locks account 1, then account 2. The concurrent transaction locks account 3, then account 1. No cycle, no deadlock — fine.

But suppose the concurrent transaction is Alice → Bob in the opposite direction (Bob → Alice, $200 — a refund). It would lock account 2 first, then account 1. Our transaction locks account 1 first, then account 2. Cycle!

```
Time  Our Txn (lock 1, then 2)            Concurrent Txn (lock 2, then 1)
T0    lock 1
T1                                         lock 2
T2    wait for 2                           wait for 1
T3    (deadlock detector fires after 1s)
T4    ABORT one of us
```

PostgreSQL's deadlock detector runs every 1 second (configurable). It builds the wait-for graph, finds the cycle, and aborts the transaction that has done the least work (or the one that started later). The aborted transaction gets `SQLSTATE 40P01`.

**The fix**: Always lock in ID order. Our transaction locks 1 then 2; the concurrent transaction also locks 1 then 2 (because `min(2,1) = 1`). No cycle.

## Variant 3 — Crash mid-transaction

Suppose the database crashes at T9 (after the debit UPDATE, before the credit UPDATE).

### What the client sees

The client's connection drops. The client does not know whether the transaction committed. The client must retry (with the same idempotency key) once the database is back.

### What PostgreSQL does on restart

ARIES recovery runs (cross-link [[01-ARIES]]):

1. **Analysis pass**: scan the WAL from the last checkpoint. Rebuild the transaction table. Our transaction (xid = 1005) is in the table, status = active (no commit record found).
2. **Redo pass**: replay all WAL records from the earliest dirty page LSN. The debit UPDATE (T8) is replayed — account 1's balance is set to 500. The credit UPDATE was never written, so nothing to redo for it.
3. **Undo pass**: roll back uncommitted transactions. Our transaction is active (no commit), so its changes are undone. The debit UPDATE is reversed: account 1's balance is restored to 1000. The ledger entry we inserted (T9) is marked as deleted. CLRs (Compensation Log Records) are written so that a subsequent crash during undo is safe.

**Final state**: account 1 balance = 1000, account 2 balance = 200. The transaction is fully rolled back. No partial state.

When the client retries with the same idempotency key, the transfer runs cleanly.

## Variant 4 — Crash after COMMIT, before client receives acknowledgment

Suppose the COMMIT succeeds (the WAL commit record is flushed at T12), but the network connection drops before the client receives the "committed" response.

### What the client sees

The client does not know whether the transaction committed. It retries with the same idempotency key.

### What happens on retry

The retry hits the `INSERT INTO transfers ... ON CONFLICT (idempotency_key) DO NOTHING RETURNING id` clause. The transfer record already exists (it was committed), so the conflict fires. The `RETURNING id` returns the existing transfer ID. The application recognizes this and returns "success" to the client — without re-debiting or re-crediting.

**The point**: Idempotency keys make retried transactions safe. Without them, the retry would re-debit Alice and re-credit Bob, leaving Alice with $0 and Bob with $1200.

## Variant 5 — Two-phase commit (cross-bank transfer)

If the transfer is to an external bank (different database), we cannot use a single transaction. We use a saga or 2PC (cross-link [[07-Distributed-Transactions]], [[08-Two-Phase-Commit]]).

### Saga flow

1. Coordinator: insert transfer record with status = PENDING.
2. Bank A (local transaction): debit Alice, insert ledger entry, mark transfer step as DEBITED in the saga log.
3. Coordinator: call Bank B.
4. Bank B (local transaction): credit Bob, insert ledger entry, return success.
5. Coordinator: mark transfer as COMPLETED.
6. If Bank B fails: coordinator calls Bank A to reverse the debit (compensating transaction), marks transfer as REVERSED.

The intermediate state (Alice debited, Bob not yet credited) is visible. The customer sees the transfer as PENDING until it completes or reverses.

### 2PC flow

1. Coordinator: send PREPARE to Bank A and Bank B.
2. Bank A (local): write a "prepared" WAL record, lock the account, respond YES.
3. Bank B (local): write a "prepared" WAL record, lock the account, respond YES.
4. Coordinator: write a "commit decision" to its own log.
5. Coordinator: send COMMIT to both.
6. Bank A and Bank B: write commit records, release locks, respond ACK.
7. Coordinator: write "transaction complete" to its log.

The intermediate state is locked (accounts are frozen between PREPARE and COMMIT). No partial state visible to other transactions. But if the coordinator crashes after step 4, Bank A and Bank B are stuck holding locks until the coordinator recovers — the "blocking problem" of 2PC.

## The complete picture

| Concern | Mechanism | Chapter |
|---|---|---|
| Atomicity | BEGIN/COMMIT/ROLLBACK | [[06-Transactions-In-SQL]] |
| Isolation | SERIALIZABLE (SSI) | [[02-Isolation-Levels]], [[05-Serializability]] |
| Concurrency control | MVCC + row-level locks | [[04-MVCC]], [[03-Two-Phase-Locking]] |
| Deadlock prevention | Lock ordering by ID | [[06-Deadlocks]] |
| Lost update prevention | SERIALIZABLE / FOR UPDATE | [[01-Concurrency-Anomalies]] |
| Idempotency | ON CONFLICT on idempotency_key | [[02-DML]] |
| Durability | WAL flush on COMMIT | [[00-WAL-Logging]] |
| Recovery | ARIES (Analysis, Redo, Undo) | [[01-ARIES]] |
| Cross-database atomicity | Saga or 2PC | [[07-Distributed-Transactions]], [[08-Two-Phase-Commit]] |

## What is genuinely new here

Nothing. Every piece was taught in its own chapter. The value of this walkthrough is *integration*: seeing the pieces fire in order, on one operation, with the failure variants made explicit.

If you can trace this walkthrough from memory, you have internalized the transactional half of the vault.

## Where this goes next

- [[04-Banking-Recovery-Scenario]] — the disaster-recovery version of variant 3.
- [[05-Banking-Distributed-Design]] — the distributed version of variant 5.
- [[04-End-To-End-Capstone]] — apply the same walkthrough to a different domain.
