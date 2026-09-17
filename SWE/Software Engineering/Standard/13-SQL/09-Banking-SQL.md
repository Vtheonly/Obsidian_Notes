# Banking SQL — End to End

> The capstone SQL chapter. Every prior SQL concept — DDL, DML, joins, CTEs, window functions, transactions, views, procedures — applied to the Banking case study in production-shaped queries. This is the artifact the next chapter ([[09-Banking-Query-Plans]]) will dissect with `EXPLAIN`.

## What you already know

From [[04-Banking-Schema]]: the full schema — nine tables, every constraint, every index. From [[02-Use-Cases]]: the transfer flow as a sequence of steps with extensions and postconditions. From [[00-Banking-Case-Study]]: the ten invariants, including idempotency, double-entry, and atomicity. From [[02-DML]]: idempotent writes via `ON CONFLICT` and `RETURNING`. From [[06-Transactions-In-SQL]]: the transaction boundary around the transfer. From [[05-Window-Functions]]: running balances without O(N²) self-joins.

## Why this layer exists

Each prior SQL chapter taught one technique. This chapter shows them composed: the transfer as a single transactional unit; the balance query as a join with a window function; the daily interest accrual as a batch; the monthly statement as a procedural generation; the fraud query as a multi-condition SELECT against recent activity. The point is to see the SQL layer of the Banking system *as a whole*.

## What is genuinely new here

Nothing new conceptually. The new thing is *integration*: the same query touching five tables, the same transaction spanning idempotency, double-entry, and lifecycle rules, the same plan needing indexes from [[04-Banking-Schema]] and isolation from [[06-Transactions-In-SQL]].

## Concepts

This chapter has five sections, each a query the Banking system needs in production:

1. **The transfer** — the SQL of the canonical flow.
2. **The balance query** — a customer-facing read.
3. **The daily interest accrual batch** — overnight processing.
4. **The monthly statement generation** — a periodic batch.
5. **The fraud-detection query** — analytical SQL over recent activity.

Each query is followed by its *execution intuition* — what the database does to produce the result, and which indexes and plan choices matter. For the full `EXPLAIN` analysis, see [[09-Banking-Query-Plans]].

## Banking application

### Query 1 — the transfer (transaction)

The transfer as a single SQL transaction. This is the SQL the application submits (or that the stored procedure from [[08-Stored-Procedures]] wraps). Idempotent, atomic, isolated, with a savepoint around the fraud check.

```sql
-- PostgreSQL: the transfer as a single SQL transaction
BEGIN;
SET LOCAL transaction_isolation = 'serializable';

-- 1. Idempotent insert of the transfer row.
--    ON CONFLICT DO UPDATE is a no-op update that forces RETURNING to fire
--    even when the row already existed. (xmax = 0) distinguishes insert vs. update.
INSERT INTO transfers (from_account_id, to_account_id, amount, currency, status, idempotency_key)
VALUES ($1, $2, $3, 'USD', 'PENDING', $4)
ON CONFLICT (idempotency_key) DO UPDATE
SET status = transfers.status
RETURNING id, (xmax = 0) AS was_inserted
\gset

-- 2. If this was a retry, exit successfully — the prior result is the result.
IF NOT :was_inserted THEN
    COMMIT;
    -- Application reads the transfer's final status separately.
    RETURN;
END IF;

-- 3. Debit the source. The conditional WHERE enforces invariant 8 (closed cannot transact)
--    and invariant 2 (no negative beyond overdraft) atomically.
UPDATE accounts
SET balance = balance - $3
WHERE id = $1
  AND status = 'ACTIVE'
  AND balance - $3 >= -overdraft_limit;

-- If 0 rows affected: the account is closed, frozen, or has insufficient funds.
-- In PL/pgSQL, we'd check NOT FOUND; in application code, check the row count.
-- For this sketch, assume the application checks and calls ROLLBACK on failure.

-- 4. Credit the destination. Frozen accounts can receive (invariant 9).
UPDATE accounts
SET balance = balance + $3
WHERE id = $2
  AND status IN ('ACTIVE','FROZEN');

-- 5. Write the two ledger entries. Idempotency key per entry prevents double-writes on retry.
INSERT INTO ledger_entries (account_id, transfer_id, amount, idempotency_key)
VALUES
    ($1, :id, -$3, $4 || '-debit'),
    ($2, :id,  $3, $4 || '-credit')
ON CONFLICT (idempotency_key) DO NOTHING;

-- 6. Mark the transfer complete.
UPDATE transfers
SET status = 'COMPLETED', completed_at = now()
WHERE id = :id AND status = 'PENDING';

-- 7. Fraud check inside a savepoint so a failure does not abort the transfer.
SAVEPOINT before_fraud;
-- (In PL/pgSQL we'd use a BEGIN ... EXCEPTION block; in application code,
-- a SAVEPOINT and conditional ROLLBACK TO.)
-- PERFORM evaluate_fraud(:id);  -- if this raises, ROLLBACK TO before_fraud

COMMIT;
```

**Execution intuition.** The transaction holds a `SERIALIZABLE` snapshot. The two `UPDATE accounts` statements use the primary-key index for lookup, plus row-level locks that prevent concurrent writers from modifying the same accounts. The `INSERT INTO ledger_entries` writes two rows to the hot table and updates the `(account_id, occurred_at DESC)` index. The `ON CONFLICT` lookup uses the unique index on `idempotency_key`. The total work is O(log N) per index lookup plus O(1) row writes — fast on the schema's indexes.

The savepoint is cheap — it is just a marker in the transaction's WAL stream. If the fraud check raises, `ROLLBACK TO before_fraud` undoes only the fraud check's writes; the transfer stays committed at step 6.

### Query 2 — the balance query (customer-facing read)

```sql
-- The current balance and last 5 transactions for a customer's account, in one round-trip.
SELECT a.iban, a.balance, a.status, a.opened_at,
       (SELECT SUM(amount) FROM ledger_entries WHERE account_id = a.id) AS ledger_sum,
       recent.amount, recent.occurred_at, recent.id AS ledger_entry_id
FROM accounts a
LEFT JOIN LATERAL (
    SELECT id, amount, occurred_at
    FROM ledger_entries le
    WHERE le.account_id = a.id
    ORDER BY occurred_at DESC
    LIMIT 5
) recent ON true
WHERE a.id = $1;
```

**Execution intuition.** The query uses `LATERAL` to run a subquery per row of the outer query — but the outer query is one row (`a.id = $1`), so the lateral subquery runs once. The primary-key index on `accounts.id` finds the account in O(log N). The `(account_id, occurred_at DESC)` index on `ledger_entries` supports the lateral subquery's `ORDER BY occurred_at DESC LIMIT 5` with an index scan — no sort needed. The scalar subquery for `ledger_sum` is a single aggregate; with the same index, it can be answered by an index-only scan summing the indexed `amount` values (if the index includes amount; otherwise a heap fetch per row).

The denormalized `balance` column makes the customer-facing read O(1) for the balance itself; the `ledger_sum` is computed for reconciliation and shown to the customer as a sanity check.

### Query 3 — daily interest accrual (batch)

```sql
-- PostgreSQL: accrue daily interest on all active savings accounts.
-- Designed to be idempotent (re-running for the same day is a no-op).

WITH accounts_to_accrue AS (
    SELECT sa.account_id, sa.interest_rate, a.balance
    FROM savings_accounts sa
    JOIN accounts a ON a.id = sa.account_id
    WHERE a.status = 'ACTIVE'
      AND a.balance > 0
      -- Skip accounts already accrued today
      AND (sa.last_accrual_at IS NULL
           OR sa.last_accrual_at < date_trunc('day', now()))
),
accruals AS (
    SELECT account_id,
           ROUND(balance * interest_rate / 365, 2) AS interest_amount,
           'interest-' || account_id || '-' || to_char(now(), 'YYYY-MM-DD') AS idem
    FROM accounts_to_accrue
    WHERE ROUND(balance * interest_rate / 365, 2) > 0
),
inserted_entries AS (
    INSERT INTO ledger_entries (account_id, amount, idempotency_key)
    SELECT account_id, interest_amount, idem FROM accruals
    ON CONFLICT (idempotency_key) DO NOTHING
    RETURNING account_id, amount
),
updated_accounts AS (
    UPDATE accounts a
    SET balance = balance + ie.amount
    FROM inserted_entries ie
    WHERE a.id = ie.account_id
    RETURNING a.id
),
updated_savings AS (
    UPDATE savings_accounts sa
    SET interest_accrued = interest_accrued + ie.amount,
        last_accrual_at = now()
    FROM inserted_entries ie
    WHERE sa.account_id = ie.account_id
    RETURNING sa.account_id
)
SELECT COUNT(*) AS entries_written FROM inserted_entries;
```

**Execution intuition.** This is a single statement that uses CTEs to compose what would otherwise be a loop. PostgreSQL 12+ inlines the CTEs, so the optimizer can see the whole query. The `accounts_to_accrue` CTE uses the primary key on `savings_accounts.account_id` and a sequential scan of `savings_accounts` (typically a small table). The `INSERT ... SELECT` writes one row per account into `ledger_entries`, using the `(idempotency_key)` unique index to enforce idempotency. The two `UPDATE ... FROM` statements update the affected accounts and savings subtypes in bulk.

The idempotency key `interest-<account>-<date>` ensures that re-running the batch for the same day is a no-op. The `ON CONFLICT DO NOTHING` skips already-written entries; the `RETURNING` clause feeds only the newly-written entries to the updates, so the balances are not double-credited on retry.

### Query 4 — monthly statement generation (batch)

```sql
-- PostgreSQL: generate monthly statements for all active accounts.
-- One statement row per (account, month).

WITH period AS (
    SELECT date_trunc('month', now()) - interval '1 month' AS start_date,
           date_trunc('month', now()) AS end_date
),
account_periods AS (
    SELECT a.id AS account_id, p.start_date, p.end_date, a.balance AS closing_balance
    FROM accounts a, period p
    WHERE a.status IN ('ACTIVE','FROZEN')
      AND NOT EXISTS (
          SELECT 1 FROM statements s
          WHERE s.account_id = a.id
            AND s.period_start = p.start_date
            AND s.period_end = p.end_date
      )
),
opening_and_activity AS (
    SELECT ap.account_id, ap.start_date, ap.end_date, ap.closing_balance,
           COALESCE((
               SELECT a2.balance
               FROM accounts a2
               -- (In production this would be a balance as-of the start date,
               -- reconstructed from the ledger; simplified here.)
               WHERE a2.id = ap.account_id
           ), 0) AS opening_balance,
           COALESCE(SUM(le.amount) FILTER (WHERE le.amount > 0), 0) AS total_credits,
           COALESCE(SUM(le.amount) FILTER (WHERE le.amount < 0), 0) AS total_debits,
           COUNT(*) AS transaction_count
    FROM account_periods ap
    LEFT JOIN ledger_entries le
      ON le.account_id = ap.account_id
     AND le.occurred_at >= ap.start_date
     AND le.occurred_at <  ap.end_date
    GROUP BY ap.account_id, ap.start_date, ap.end_date, ap.closing_balance
)
INSERT INTO statements (
    account_id, period_start, period_end,
    opening_balance, closing_balance, interest_accrued
)
SELECT account_id, start_date, end_date,
       opening_balance, closing_balance,
       0  -- (interest is accrued separately; see Query 3)
FROM opening_and_activity
ON CONFLICT (account_id, period_start, period_end) DO NOTHING;
```

**Execution intuition.** The CTEs compute, for each active account that does not yet have a statement for the period, the opening balance, closing balance, and activity summary. The `NOT EXISTS` check uses the unique index on `(account_id, period_start, period_end)` to skip accounts that already have a statement (idempotent retry). The join to `ledger_entries` uses the `(account_id, occurred_at)` and `(occurred_at)` indexes; for a small set of accounts in a one-month window, the planner should choose an index scan on `account_id` then filter by date.

The final `INSERT ... ON CONFLICT DO NOTHING` makes the batch safely re-runnable: if it crashes halfway through, re-running picks up where it left off.

### Query 5 — suspicious transfers (fraud detection)

```sql
-- Find suspicious transfers: large amount, sent to a beneficiary the customer
-- has never sent to before, in the last 24 hours.

WITH recent_transfers AS (
    SELECT t.id, t.from_account_id, t.to_account_id, t.amount, t.created_at,
           fa.customer_id AS from_customer
    FROM transfers t
    JOIN accounts fa ON fa.id = t.from_account_id
    WHERE t.status = 'COMPLETED'
      AND t.created_at > now() - interval '24 hours'
),
known_beneficiaries AS (
    -- Customers the source customer has transferred to before (any time before today)
    SELECT DISTINCT t2.from_account_id AS prior_from, t2.to_account_id AS prior_to
    FROM transfers t2
    WHERE t2.status = 'COMPLETED'
      AND t2.created_at < date_trunc('day', now())
),
flagged AS (
    SELECT rt.id, rt.from_account_id, rt.to_account_id, rt.amount, rt.created_at, rt.from_customer,
           CASE
               WHEN rt.amount > 10000 THEN 'large_amount'
               WHEN kb.prior_to IS NULL THEN 'new_beneficiary'
               WHEN rt.amount > 5000 AND kb.prior_to IS NULL THEN 'large_and_new'
           END AS flag_reason
    FROM recent_transfers rt
    LEFT JOIN known_beneficiaries kb
      ON kb.prior_from = rt.from_account_id
     AND kb.prior_to   = rt.to_account_id
    WHERE (rt.amount > 10000)
       OR (kb.prior_to IS NULL)
)
SELECT f.*, c.legal_name AS customer_name
FROM flagged f
JOIN customers c ON c.id = f.from_customer
ORDER BY f.amount DESC
LIMIT 200;
```

**Execution intuition.** This query benefits from the `(from_account_id, created_at)` and `(to_account_id, created_at)` indexes on `transfers`. The `recent_transfers` CTE filters by date — the `idx_transfers_status_created` partial-style index (or a sequential scan with a date filter) reduces the working set. The `known_beneficiaries` CTE is the expensive part: it scans all historical transfers. In production, this would be pre-computed into a materialized view of "customer-beneficiary pairs" refreshed nightly.

The `LEFT JOIN` to `known_beneficiaries` returns NULL for new beneficiaries; the `CASE` expression produces the flag reason. The final `ORDER BY amount DESC LIMIT 200` caps the output for analyst review.

This query is the bridge to [[09-Banking-Query-Plans]]: the same query, run under `EXPLAIN ANALYZE`, reveals which CTE is the bottleneck and which index is missing.

## Code — common SQL patterns from this chapter

```sql
-- Pattern 1: idempotent insert with insert-vs-update detection
INSERT INTO transfers (...) VALUES (...) ON CONFLICT (idempotency_key) DO UPDATE
SET status = transfers.status RETURNING id, (xmax = 0) AS was_inserted;

-- Pattern 2: conditional update that enforces invariants
UPDATE accounts SET balance = balance - $1
WHERE id = $2 AND status = 'ACTIVE' AND balance - $1 >= -overdraft_limit;

-- Pattern 3: bulk insert from a CTE
WITH src AS (...) INSERT INTO t (...) SELECT ... FROM src ON CONFLICT DO NOTHING;

-- Pattern 4: bulk update from a CTE
UPDATE accounts a SET balance = a.balance + s.amount
FROM src s WHERE a.id = s.account_id;

-- Pattern 5: lateral subquery for "top N per parent"
SELECT a.*, recent.* FROM accounts a
LEFT JOIN LATERAL (
    SELECT * FROM ledger_entries le
    WHERE le.account_id = a.id
    ORDER BY occurred_at DESC LIMIT 5
) recent ON true;

-- Pattern 6: set-based interest accrual
WITH accounts_to_accrue AS (...),
     accruals AS (SELECT ..., balance * rate / 365 AS interest FROM accounts_to_accrue),
     inserted AS (INSERT INTO ledger_entries ... SELECT ... FROM accruals RETURNING *)
UPDATE accounts SET balance = balance + i.amount FROM inserted i WHERE accounts.id = i.account_id;
```

## What can go wrong

- **Long-running transactions in the transfer.** The fraud check inside the savepoint must be fast. A slow fraud check holds locks on both accounts for the duration. Move slow fraud checks out of the transaction; mark the transfer `FRAUD_PENDING` and review asynchronously.
- **The balance query without the denormalized column.** Computing `balance` from `ledger_entries` on every read is O(N) per account. The denormalized `balance` column on `accounts` makes it O(1). The two must be kept in sync — see the reconciliation query in [[07-Views-Materialized-Views]].
- **The interest batch on a large table.** With millions of savings accounts, the single-statement batch may be too large for one transaction. Split into chunks (e.g., 10,000 accounts per chunk) and run each in its own transaction.
- **Statement generation races.** If a transfer commits while statement generation is running, the statement may or may not include it. Use `REPEATABLE READ` (or `SERIALIZABLE`) for the statement-generation transaction to get a consistent snapshot.
- **The fraud query scanning all history.** The `known_beneficiaries` CTE scans all completed transfers. Materialize it nightly (see [[07-Views-Materialized-Views]]) and read from the materialized view.
- **Lock ordering.** The transfer locks the source account before the destination. A reverse transfer (B → A) locks B before A. Two concurrent transfers in opposite directions can deadlock. Always lock in a canonical order (e.g., by account ID ascending) to prevent deadlocks — see [[06-Deadlocks]].
- **Idempotency key collisions.** If two different operations generate the same idempotency key, one will be silently dropped. Use a key format that includes the operation type and a unique request identifier.

## Trade-offs

- **Denormalized balance vs computed balance.** The denormalized `balance` column makes reads fast and writes slightly slower (two writes: the ledger entry and the balance update). The computed balance makes reads slow and writes simple. The vault's choice: denormalize, with a reconciliation job that periodically verifies equality.
- **Application transaction vs stored procedure.** The transfer can be a `@Transactional` method in Java or a `PROCEDURE` in PL/pgSQL. The application version is testable; the procedure version is faster (one round-trip). The vault's choice: application, for testability — see [[08-Stored-Procedures]].
- **Set-based batch vs procedural loop.** The interest batch can be a single statement (set-based) or a loop (procedural). Set-based is faster; procedural is easier to debug. The vault's choice: set-based for the common case; fall back to procedural for edge cases.
- **Synchronous fraud check vs asynchronous.** Synchronous gives an immediate answer but couples transfer to fraud service. Asynchronous decouples but introduces `PENDING` transfers. The vault's choice: synchronous for low-risk, asynchronous for high-risk — see [[08-Trade-offs-Everywhere]].
- **Read consistency vs read speed.** `REPEATABLE READ` gives a consistent snapshot; `READ COMMITTED` gives the latest data with possible inconsistencies. The vault's choice: `READ COMMITTED` for customer-facing reads (fast, mostly consistent); `SERIALIZABLE` for transfers (correct).
- **Materialized view vs live view for reporting.** Materialized is fast but stale; live is fresh but slow. The vault's choice: materialized for nightly reports; live for customer-facing dashboards.

## Forward links

- [[09-Banking-Query-Plans]] — these same queries, dissected under `EXPLAIN ANALYZE`.
- [[00-ACID]] — the transaction guarantees behind the transfer.
- [[02-Isolation-Levels]] — why `SERIALIZABLE` for transfers, `READ COMMITTED` for reads.
- [[04-Banking-Schema]] — the schema these queries run against.
- [[01-Indexing-Strategy]] — which indexes these queries need.
- [[05-Banking-Performance-Tuning]] — production tuning of these queries at scale.
- [[09-Banking-Transaction-Walkthrough]] — the transfer under the microscope.
- [[00-ORM-Impedance-Mismatch]] — what happens when the ORM tries to generate these queries.
