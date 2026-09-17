# Transactions in SQL

> The SQL sub-language that groups writes into atomic units. `BEGIN`, `COMMIT`, `ROLLBACK`, `SAVEPOINT` are the four verbs that turn a database from a fast key-value store into a correctness-preserving system. This chapter is the SQL surface of [[00-ACID]] — the concepts live there; the syntax lives here.

## What you already know

From [[00-ACID]]: a transaction is a unit of work that is Atomic, Consistent, Isolated, and Durable. From [[02-Isolation-Levels]]: isolation is a trade-off between correctness and concurrency, and the SQL standard defines four levels (READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE). From [[02-Use-Cases]]: the transfer flow is the canonical multi-statement transaction — debit, credit, two ledger entries, status update, all atomic. From [[00-Banking-Case-Study]] invariant 5: a transfer either completely succeeds or completely fails; no partial state.

## Why this layer exists

Without transactions, every statement is its own atomic unit. A transfer is four statements (debit, credit, two ledger entries); if the database crashes after the debit, the money is gone. Transactions group the four statements into one unit: either all four commit, or none of them do. The transaction is the database's contribution to correctness under failure and concurrency.

## What is genuinely new here

The new idea is **transaction control as an explicit SQL statement**. The application decides where a transaction begins and ends. The database enforces the ACID guarantees within those boundaries. Getting the boundaries right is the application's job — and the most common source of production bugs.

## Concepts

### The four verbs

| Verb | Effect |
|---|---|
| `BEGIN` (or `START TRANSACTION`) | Start a transaction. Subsequent statements run in the same transaction until `COMMIT` or `ROLLBACK`. |
| `COMMIT` | End the transaction successfully. All changes become durable and visible to other transactions. |
| `ROLLBACK` (or `ROLLBACK TRANSACTION`) | End the transaction by undoing all changes. The database state returns to the start of the transaction. |
| `SAVEPOINT name` | Create a named savepoint within the transaction. Can be rolled back to with `ROLLBACK TO name` without aborting the whole transaction. |

In PostgreSQL, statements outside an explicit `BEGIN` block run in *autocommit* mode: each statement is its own transaction, automatically committed on success. This is the default for most database drivers.

### The transaction as the unit of atomicity

From [[00-ACID]]: atomicity means "all or nothing." Within a transaction, partial failures are impossible. If the application crashes mid-transaction, the database rolls back on reconnect. If a constraint is violated, the whole transaction fails (or, with `SAVEPOINT`, just the part after the savepoint).

### Isolation levels

Set with `SET TRANSACTION ISOLATION LEVEL ...` (inside the transaction, before any data access):

```sql
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- ... statements ...
COMMIT;
```

The four standard levels, from weakest to strongest:

| Level | Prevents | Allows |
|---|---|---|
| READ UNCOMMITTED | (nothing useful) | Dirty reads, non-repeatable reads, phantoms |
| READ COMMITTED (PostgreSQL default) | Dirty reads | Non-repeatable reads, phantoms |
| REPEATABLE READ | Dirty reads, non-repeatable reads | Phantoms (in standard; PostgreSQL's RR prevents phantoms via MVCC) |
| SERIALIZABLE | All anomalies | (nothing) |

See [[02-Isolation-Levels]] for the anomalies and the trade-offs. The SQL syntax is the surface; the behavior is the substance.

### PostgreSQL's default: READ COMMITTED

PostgreSQL defaults to READ COMMITTED. Each statement sees a snapshot of committed data *as of the start of that statement*. Two reads of the same row in the same transaction can see different values if another transaction committed between them.

Why READ COMMITTED as the default? Because:

- It is fast — locks are short-lived, and MVCC snapshots are per-statement.
- It is "good enough" for most queries — the anomalies it allows (non-repeatable reads, phantoms) are rarely problematic for OLTP.
- Stronger levels (REPEATABLE READ, SERIALIZABLE) have higher costs and a real risk of serialization failures that the application must handle.

The trade-off: READ COMMITTED is the lazy default. For transactions that *need* consistency (transfers, balance updates), choose SERIALIZABLE or use explicit row locks. See [[02-Isolation-Levels]] for the decision tree.

### SAVEPOINT — partial rollback

A savepoint lets you roll back part of a transaction without aborting the whole thing:

```sql
BEGIN;
INSERT INTO transfers (...) VALUES (...);
SAVEPOINT before_fraud_check;
-- Run the fraud check; if it fails, roll back to the savepoint
-- without losing the transfer row
BEGIN;
  -- Inline block (PostgreSQL supports nested transactions via savepoints)
  SELECT check_fraud($transfer_id);
EXCEPTION WHEN OTHERS THEN
  ROLLBACK TO before_fraud_check;
  UPDATE transfers SET status = 'FRAUD_REVIEW' WHERE id = $transfer_id;
END;
COMMIT;
```

Savepoints are the SQL implementation of "try/except within a transaction." They are essential for:

- **Idempotent retries within a transaction.** Try an operation; if it fails, roll back to a savepoint and try a fallback.
- **Bulk operations with error tolerance.** Insert 1000 rows; if one fails, roll back to the savepoint and continue with the rest, logging the failure.
- **Application-level exception handling.** Map a unique-constraint violation to "already exists" without aborting the transaction.

Savepoints are not free — each one holds resources until commit. Use them sparingly.

### Transaction boundaries and the application

The application decides where transactions begin and end. The common patterns:

- **Per-statement (autocommit).** Each statement is its own transaction. Fine for simple reads; wrong for multi-statement writes.
- **Per-request.** A web request opens a transaction at the start and commits at the end. The default in many frameworks (Spring's `@Transactional`, Rails' `around_action`).
- **Per-use-case.** The transaction boundary aligns with a use case (one transfer, one account opening, one statement generation). This is the pattern this vault recommends; see [[04-Unit-of-Work]].
- **Per-batch.** A long-running batch processes many items; each item is its own transaction. Avoids holding locks for the whole batch.

The wrong boundary is a common bug: a transaction that includes a slow external call (an HTTP request, a user prompt) holds locks for the duration of the call. Keep transactions short; move external calls outside.

## Banking application — the transfer transaction

From [[02-Use-Cases]] step 7–11: open a transaction, debit, credit, write ledger entries, mark transfer complete, commit.

```sql
-- PostgreSQL: the transfer as a single SQL transaction
BEGIN;
SET LOCAL transaction_isolation = 'serializable';
-- SET LOCAL scopes the change to this transaction

-- 1. Insert the transfer row (idempotent)
INSERT INTO transfers (from_account_id, to_account_id, amount, currency, status, idempotency_key)
VALUES ($1, $2, $3, 'USD', 'PENDING', $4)
ON CONFLICT (idempotency_key) DO UPDATE
SET status = transfers.status
RETURNING id, (xmax = 0) AS was_inserted
\gset

-- 2. Debit the source account
UPDATE accounts
SET balance = balance - $3
WHERE id = $1
  AND status = 'ACTIVE'
  AND balance - $3 >= -overdraft_limit;
-- If 0 rows affected, the account is closed, frozen, or insufficient balance: ROLLBACK

-- 3. Credit the destination account
UPDATE accounts
SET balance = balance + $3
WHERE id = $2
  AND status IN ('ACTIVE','FROZEN');  -- frozen can receive, not send

-- 4. Write the two ledger entries (idempotent)
INSERT INTO ledger_entries (account_id, transfer_id, amount, idempotency_key)
VALUES
    ($1, :id, -$3, $4 || '-debit'),
    ($2, :id,  $3, $4 || '-credit')
ON CONFLICT (idempotency_key) DO NOTHING;

-- 5. Mark the transfer complete
UPDATE transfers
SET status = 'COMPLETED', completed_at = now()
WHERE id = :id AND status = 'PENDING';

-- 6. Savepoint before the fraud check (optional)
SAVEPOINT before_fraud;
-- Run the fraud check; if it raises, roll back to the savepoint
-- The transfer is already complete; the fraud check is a side effect.
BEGIN
  PERFORM evaluate_fraud(:id);
EXCEPTION WHEN OTHERS THEN
  ROLLBACK TO before_fraud;
  -- The transfer stays COMPLETED; fraud is reviewed out-of-band
  INSERT INTO audit_log (table_name, row_id, action, changed_to)
  VALUES ('transfers', :id, 'UPDATE', jsonb_build_object('fraud_check_error', SQLERRM));
END;

COMMIT;
```

Notes on this transaction:

- `SET LOCAL` scopes the isolation level to this transaction only. The default isolation is unchanged for other transactions.
- The idempotency key on `transfers` and `ledger_entries` makes the transaction safe to retry.
- The savepoint lets the fraud check fail without aborting the transfer.
- The whole transaction is short — no external calls, no user prompts, no sleeps.
- If anything fails before `COMMIT`, the entire transfer is rolled back. No partial state.

### The savepoint pattern in Java

The same transaction in Java (using JDBC):

```java
Connection conn = dataSource.getConnection();
try {
    conn.setAutoCommit(false);
    conn.setTransactionIsolation(Connection.TRANSACTION_SERIALIZABLE);

    // 1. Insert transfer (idempotent)
    long transferId = insertTransfer(conn, req);

    // 2-4. Debit, credit, ledger entries
    debit(conn, req.fromAccountId(), req.amount());
    credit(conn, req.toAccountId(), req.amount());
    insertLedgerEntries(conn, transferId, req);

    // 5. Mark complete
    markComplete(conn, transferId);

    // 6. Savepoint for fraud check
    Savepoint sp = conn.setSavepoint("before_fraud");
    try {
        evaluateFraud(conn, transferId);
    } catch (SQLException e) {
        conn.rollback(sp);
        auditFraudError(conn, transferId, e);
    }

    conn.commit();
} catch (SQLException e) {
    conn.rollback();
    throw e;
} finally {
    conn.close();
}
```

This is the JDBC equivalent of the SQL above. Spring's `@Transactional` and `TransactionTemplate` abstract this further; see [[04-Unit-of-Work]].

## Code — common transaction patterns

```sql
-- Pattern 1: short OLTP transaction
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Pattern 2: batch with per-item transactions
-- (In PostgreSQL, this is best done in the application; PL/pgSQL can also do it)
DO $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN SELECT id FROM pending_notifications WHERE status = 'QUEUED' LOOP
        BEGIN
            PERFORM send_notification(rec.id);
            UPDATE notifications SET status = 'SENT', sent_at = now() WHERE id = rec.id;
        EXCEPTION WHEN OTHERS THEN
            UPDATE notifications SET status = 'FAILED' WHERE id = rec.id;
            -- Continue with the next item; do not abort the batch
        END;
    END LOOP;
END $$;

-- Pattern 3: read-only transaction with REPEATABLE READ for consistency
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ, READ ONLY;
-- Two reads that must see the same snapshot
SELECT SUM(amount) FROM ledger_entries WHERE account_id = 42;
SELECT COUNT(*) FROM ledger_entries WHERE account_id = 42;
COMMIT;

-- Pattern 4: advisory lock to serialize a critical section (PostgreSQL)
BEGIN;
SELECT pg_advisory_xact_lock(42);  -- lock held until COMMIT
-- Only one transaction can be here at a time
UPDATE counters SET value = value + 1 WHERE id = 1;
COMMIT;
```

## What can go wrong

- **Long-running transactions.** Hold locks, bloat the table (PostgreSQL's MVCC keeps old row versions until no transaction needs them — see [[04-MVCC]]), and block vacuuming. Keep transactions short.
- **Transactions that include external calls.** An HTTP call inside a transaction holds locks for the duration. Move external calls outside.
- **Forgot to commit.** The transaction stays open, holding locks, until the connection closes or times out. Use try/finally in application code to always commit or roll back.
- **Forgot to roll back on error.** After an exception, the transaction is in an aborted state (PostgreSQL); further statements fail until `ROLLBACK`. Always roll back in the exception handler.
- **Wrong isolation level.** Using READ COMMITTED for a transfer can produce a lost update under concurrency. Use SERIALIZABLE or explicit locks for money-moving operations.
- **Serialization failures.** Under SERIALIZABLE, the database may abort a transaction with `40001 serialization_failure`. The application must retry. Many frameworks (Spring, Hibernate) handle this automatically with a retry interceptor.
- **Savepoint leaks.** Each savepoint holds resources. If you forget to release or roll back to it, you pay until commit.
- **Nested transactions.** SQL does not have true nested transactions; savepoints simulate them. A `ROLLBACK` of the outer transaction undoes everything, including work after a savepoint release.
- **Autocommit surprises.** Some drivers default to autocommit; others do not. Know your driver's default.
- **DDL inside a transaction.** PostgreSQL allows most DDL inside a transaction (and it rolls back cleanly). Other databases (MySQL) do not. Mixing DDL and DML in the same transaction is occasionally useful for migrations.

## Trade-offs

- **Isolation vs concurrency.** Stronger isolation means fewer anomalies but more serialization failures and lower throughput. Pick the level that matches the operation's correctness requirement.
- **Transaction length vs lock contention.** Longer transactions hold locks longer, blocking other writers. Keep transactions short, even at the cost of more transactions.
- **Savepoints vs sub-transactions.** Savepoints are the SQL primitive; sub-transactions are an application-layer abstraction. Use savepoints directly when the logic is simple; use sub-transactions (Spring's `Propagation.REQUIRES_NEW`, etc.) when the structure is complex.
- **Per-statement vs per-use-case transactions.** Per-statement is too coarse for multi-step operations; per-use-case is the right granularity. Per-request is a useful default in web frameworks.
- **Advisory locks vs row locks.** Row locks protect specific rows; advisory locks serialize arbitrary code paths. Use row locks for data; advisory locks for operations (e.g., "only one balance recalculation at a time").
- **Autocommit vs explicit transactions.** Autocommit is simpler but offers no atomicity across statements. Use explicit transactions for any multi-statement operation.

## Forward links

- [[00-ACID]] — the concepts behind the SQL syntax.
- [[02-Isolation-Levels]] — the four levels and their anomalies.
- [[04-MVCC]] — how PostgreSQL implements isolation without locking readers.
- [[09-Banking-Transaction-Walkthrough]] — the full transfer transaction under the microscope.
- [[04-Unit-of-Work]] — the ORM pattern that wraps transactions.
- [[02-DML]] — the statements inside a transaction.
- [[09-Banking-SQL]] — the transfer transaction in context.
