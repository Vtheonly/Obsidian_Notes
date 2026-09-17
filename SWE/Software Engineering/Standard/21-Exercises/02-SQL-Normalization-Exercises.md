# SQL + Normalization Exercises

> Exercises for the data modeling half: relational theory, functional dependencies, normalization, schema design, SQL.

## How to use this file

See [[00-Exercise-Index]] for the workflow. Attempt each problem before reading hints or solutions.

---

## Exercise 1 — Discover Functional Dependencies

**Problem.** Consider the following denormalized relation for a banking ledger:

```
Transactions(tid, customer_id, customer_name, customer_email, account_id, iban,
             account_type, balance_at_time, amount, occurred_at, transfer_id,
             transfer_status, fraud_score)
```

Identify the functional dependencies. Then identify the candidate keys.

**Hints.**
- Ask: "If I know X, do I know Y?"
- `tid` is a transaction identifier — likely a candidate key.
- Some attributes depend on `customer_id`, some on `account_id`, some on `transfer_id`, some on `tid`.
- Cross-link [[03-Functional-Dependencies]], [[02-Keys-Superkeys-Candidate-Keys]].

**Solution.**

Functional dependencies:

```
tid → all attributes (tid is a candidate key)
account_id → iban, account_type, balance_at_time (at the time of this transaction)
iban → account_id  (iban is also a candidate key for the account-level attributes)
customer_id → customer_name, customer_email
account_id → customer_id  (an account belongs to one customer)
transfer_id → transfer_status, fraud_score
tid → transfer_id  (a transaction belongs to one transfer)
```

Candidate keys:
- `{tid}` — minimal, unique.
- `{iban, occurred_at}` — also unique if no two transactions on the same account can share a timestamp to the microsecond. (Risky — better to keep `tid`.)

The non-trivial FDs that violate BCNF: `customer_id → customer_name, customer_email` (customer_id is not a candidate key of Transactions); `account_id → iban, account_type, balance_at_time`; `transfer_id → transfer_status, fraud_score`. Each of these must be eliminated by decomposition (next exercise).

**What this teaches.** [[03-Functional-Dependencies]] are discovered by asking "what determines what." The FDs reveal the hidden entities (Customer, Account, Transfer) hiding inside the denormalized table.

---

## Exercise 2 — Decompose to BCNF

**Problem.** Take the `Transactions` relation from Exercise 1 and its functional dependencies. Decompose it into BCNF. Show each step and verify the lossless join property.

**Hints.**
- Apply the BCNF decomposition algorithm: find a violating FD, decompose, recurse.
- Cross-link [[07-BCNF]], [[11-Banking-Normalization-Walkthrough]].

**Solution.**

Step 1: Violation — `customer_id → customer_name, customer_email` (customer_id is not a superkey). Decompose:

- `R1(customer_id, customer_name, customer_email)` — FDs: `customer_id → customer_name, customer_email`. BCNF.
- `R2(tid, customer_id, account_id, iban, account_type, balance_at_time, amount, occurred_at, transfer_id, transfer_status, fraud_score)` — FDs: the rest.

Step 2: Violation in R2 — `account_id → iban, account_type, balance_at_time`. Decompose:

- `R3(account_id, iban, account_type, balance_at_time, customer_id)` — FDs: `account_id → iban, account_type, balance_at_time, customer_id`; `iban → account_id`. BCNF.
- `R4(tid, account_id, amount, occurred_at, transfer_id, transfer_status, fraud_score)` — FDs: `tid → all`; `transfer_id → transfer_status, fraud_score`.

Step 3: Violation in R4 — `transfer_id → transfer_status, fraud_score`. Decompose:

- `R5(transfer_id, transfer_status, fraud_score)` — BCNF.
- `R6(tid, account_id, amount, occurred_at, transfer_id)` — FDs: `tid → all`. BCNF.

Final relations:

```
Customers(customer_id, customer_name, customer_email)
Accounts(account_id, iban, account_type, balance_at_time, customer_id)
Transfers(transfer_id, transfer_status, fraud_score)
Transactions(tid, account_id, amount, occurred_at, transfer_id)
```

Lossless join verification: each decomposition step uses a common attribute that is a candidate key in one of the resulting relations (`customer_id`, `account_id`, `transfer_id`), so the joins are lossless.

**Note:** `balance_at_time` is a snapshot of the account balance at the transaction time. In practice this is denormalized — the canonical balance is the sum of transactions. If we keep `balance_at_time` purely as a historical snapshot for fast reporting, it is acceptable denormalization (see [[10-Normalization-Trade-offs]]); if it is the source of truth, it must come from the transaction log.

**What this teaches.** [[07-BCNF]] decomposition is mechanical once the FDs are known. The art is in *finding* the FDs (Exercise 1).

---

## Exercise 3 — Write the SQL for the Transfer

**Problem.** Write a single SQL transaction that performs a transfer between two accounts, enforcing:

- Source account must be ACTIVE.
- Source balance (plus overdraft, if checking) must cover the amount.
- Two ledger entries are written (debit, credit).
- The transfer record is marked COMPLETED.
- All in one atomic transaction.

Use the schema from [[04-Banking-Schema]]. Use PostgreSQL features where appropriate.

**Hints.**
- Use `SELECT ... FOR UPDATE` to lock the source account.
- Use `RETURNING` to capture inserted IDs.
- Cross-link [[02-DML]], [[06-Transactions-In-SQL]], [[00-ACID]].

**Solution.**

```sql
-- PostgreSQL
BEGIN;

-- Lock the source account row for the duration of the transaction
SELECT id, balance, status, account_type, overdraft_limit
FROM accounts
WHERE id = :from_id
FOR UPDATE;

-- Check status
DO $$
DECLARE
    src_status TEXT;
    src_balance NUMERIC;
    src_overdraft NUMERIC;
    src_type TEXT;
BEGIN
    SELECT status, balance, COALESCE(overdraft_limit, 0), account_type
    INTO src_status, src_balance, src_overdraft, src_type
    FROM accounts WHERE id = :from_id;

    IF src_status <> 'ACTIVE' THEN
        RAISE EXCEPTION 'Source account not active: %', src_status
            USING ERRCODE = 'check_violation';
    END IF;

    IF src_balance + src_overdraft < :amount THEN
        RAISE EXCEPTION 'Insufficient funds: balance %, overdraft %, amount %',
            src_balance, src_overdraft, :amount
            USING ERRCODE = 'check_violation';
    END IF;
END $$;

-- Insert the transfer record
INSERT INTO transfers (source_account_id, destination_account_id, amount, status, idempotency_key)
VALUES (:from_id, :to_id, :amount, 'COMPLETED', :idempotency_key)
ON CONFLICT (idempotency_key) DO NOTHING
RETURNING id;

-- Debit source
UPDATE accounts SET balance = balance - :amount, updated_at = NOW()
WHERE id = :from_id;

INSERT INTO ledger_entries (account_id, amount, transfer_id, occurred_at)
VALUES (:from_id, -:amount, (SELECT id FROM transfers WHERE idempotency_key = :idempotency_key), NOW());

-- Credit destination
UPDATE accounts SET balance = balance + :amount, updated_at = NOW()
WHERE id = :to_id;

INSERT INTO ledger_entries (account_id, amount, transfer_id, occurred_at)
VALUES (:to_id, :amount, (SELECT id FROM transfers WHERE idempotency_key = :idempotency_key), NOW());

COMMIT;
```

**What this teaches.** [[02-DML]] in a transaction is not just "run the statements in order." It includes locking (`FOR UPDATE`), idempotency (`ON CONFLICT`), validation (the `DO` block), and atomicity (BEGIN/COMMIT). Each element maps to a requirement: locking prevents lost updates, idempotency prevents double-debits on retry, validation enforces invariants, atomicity prevents partial state.

---

## Exercise 4 — Diagnose a Slow Query

**Problem.** The following query is slow (4.5 seconds on a 50M-row `ledger_entries` table). Diagnose and fix it.

```sql
SELECT a.iban, a.balance, COUNT(le.id) AS entry_count, SUM(le.amount) AS total_movement
FROM accounts a
LEFT JOIN ledger_entries le ON le.account_id = a.id
WHERE a.status = 'ACTIVE'
  AND le.occurred_at >= '2025-01-01'
GROUP BY a.iban, a.balance
ORDER BY total_movement DESC
LIMIT 100;
```

The `EXPLAIN ANALYZE` output shows:

```
Limit (cost=1234567.89..1234567.99 rows=100) (actual time=4521.34..4521.56 rows=100)
  -> Sort (cost=1234567.89..1234890.12 rows=128901) (actual time=4521.33..4521.55 rows=100)
        Sort Key: total_movement DESC
        -> HashAggregate (cost=1234000.11..1234123.45 rows=128901) (actual time=4498.12..4510.22 rows=128901)
              -> Hash Join (cost=123.45..987654.32 rows=1289012) (actual time=12.34..3200.11 rows=9876543)
                    Hash Cond: (le.account_id = a.id)
                    -> Seq Scan on ledger_entries le (cost=0.00..234567.89 rows=9876543) (actual time=0.12..2100.34 rows=9876543)
                          Filter: (occurred_at >= '2025-01-01')
                    -> Hash (cost=89.12..89.12 rows=8901) (actual time=12.10..12.10 rows=8901)
                          -> Seq Scan on accounts a (cost=0.00..89.12 rows=8901) (actual time=0.05..8.90 rows=8901)
                                Filter: (status = 'ACTIVE')
```

Identify the bottleneck, propose a fix, and predict the new plan.

**Hints.**
- The seq scan on `ledger_entries` is reading 9.8M rows to filter down.
- Is there an index on `occurred_at`? On `account_id`?
- The LEFT JOIN becomes effectively an INNER JOIN because of the WHERE on `le.occurred_at`.
- Cross-link [[08-Reading-EXPLAIN]], [[01-Indexing-Strategy]], [[00-Query-Optimization-Strategy]].

**Solution.**

**Bottleneck:** The seq scan on `ledger_entries` reads 9.8M rows (~2.1 seconds) just to filter by `occurred_at >= '2025-01-01'`. With no index on `occurred_at`, the planner has no choice but to scan the whole table.

**Fix 1:** Add an index on `(account_id, occurred_at)` — composite, supports the join and the filter, and is the most-used access pattern for ledger queries:

```sql
CREATE INDEX idx_ledger_account_time ON ledger_entries (account_id, occurred_at);
```

**Fix 2:** Change the LEFT JOIN to an INNER JOIN (the WHERE clause on `le.occurred_at` already turns it into one implicitly; making it explicit helps the planner and the reader):

```sql
SELECT a.iban, a.balance, COUNT(le.id), SUM(le.amount)
FROM accounts a
JOIN ledger_entries le ON le.account_id = a.id
WHERE a.status = 'ACTIVE' AND le.occurred_at >= '2025-01-01'
GROUP BY a.iban, a.balance
ORDER BY SUM(le.amount) DESC
LIMIT 100;
```

**Predicted new plan:** With the composite index, the planner can do an index scan on `ledger_entries` for each ACTIVE account, dramatically reducing the rows read. Expected: from 4.5s to ~50ms (90x improvement).

**Additional fix (if needed):** If the result is computed frequently, materialize it as a materialized view refreshed nightly (cross-link [[07-Views-Materialized-Views]], [[02-Denormalization-For-Reads]]).

**What this teaches.** [[08-Reading-EXPLAIN]] is about reading the plan and identifying the bottleneck (seq scan on 9.8M rows is the smoking gun). [[01-Indexing-Strategy]] is about choosing the right composite index for the access pattern.

---

## Exercise 5 — Write a Recursive CTE for Compound Interest

**Problem.** Write a SQL query (PostgreSQL) that, given an initial balance, an annual interest rate, and a number of years, produces a table of `(year, balance)` showing compound interest year over year.

**Hints.**
- Use `WITH RECURSIVE`.
- Anchor: year 0 = initial balance.
- Recursion: year N = year N-1 × (1 + rate).
- Cross-link [[04-Subqueries-CTEs]].

**Solution.**

```sql
-- PostgreSQL
WITH RECURSIVE compound_interest AS (
    SELECT 0 AS year, 10000.00 AS balance, 0.05 AS rate
    UNION ALL
    SELECT year + 1, balance * (1 + rate), rate
    FROM compound_interest
    WHERE year < 10
)
SELECT year, balance, balance - LAG(balance) OVER (ORDER BY year) AS interest_earned
FROM compound_interest;
```

Output:

```
year | balance   | interest_earned
0    | 10000.00  | NULL
1    | 10500.00  | 500.00
2    | 11025.00  | 525.00
3    | 11576.25  | 551.25
...
10   | 16288.95  | 776.14
```

**What this teaches.** [[04-Subqueries-CTEs]] are not just for query reuse; recursive CTEs can express iterative computations that would otherwise require procedural code. The LAG window function (cross-link [[05-Window-Functions]]) computes the per-year delta without a self-join.

---

## Exercise 6 — Design a Schema for Multi-Currency

**Problem.** Extend the Banking schema to support multiple currencies. Each account has one currency; transfers between accounts of different currencies require an exchange rate. The exchange rate is captured at transfer time (historical).

**Requirements:**
- An account is opened in a specific currency; it cannot change.
- A transfer between accounts of the same currency uses amount = amount.
- A transfer between accounts of different currencies records: source amount (in source currency), destination amount (in destination currency), exchange rate (source → destination), and a snapshot of the rate used.
- The ledger entries must record the amount in the account's currency (so the account's balance is always in its own currency).

**Hints.**
- Add `currency` to `accounts`.
- Add `source_currency`, `destination_currency`, `source_amount`, `destination_amount`, `exchange_rate` to `transfers`.
- The ledger entry amount is in the account's currency (negative for source, positive for destination).
- Cross-link [[04-Banking-Schema]], [[00-ER-Modeling]], [[02-Aggregates]].

**Solution.**

```sql
-- Schema changes
ALTER TABLE accounts ADD COLUMN currency CHAR(3) NOT NULL DEFAULT 'USD';
ALTER TABLE accounts ADD CONSTRAINT valid_currency CHECK (currency IN ('USD','EUR','GBP','JPY'));

ALTER TABLE transfers ADD COLUMN source_currency CHAR(3) NOT NULL DEFAULT 'USD';
ALTER TABLE transfers ADD COLUMN destination_currency CHAR(3) NOT NULL DEFAULT 'USD';
ALTER TABLE transfers ADD COLUMN source_amount NUMERIC(18,2) NOT NULL;
ALTER TABLE transfers ADD COLUMN destination_amount NUMERIC(18,2) NOT NULL;
ALTER TABLE transfers ADD COLUMN exchange_rate NUMERIC(18,8) NOT NULL DEFAULT 1.0;
ALTER TABLE transfers ADD CONSTRAINT currency_consistency
    CHECK (
        (source_currency = destination_currency AND source_amount = destination_amount AND exchange_rate = 1.0)
        OR
        (source_currency <> destination_currency AND destination_amount = source_amount * exchange_rate)
    );
```

The `transfers` row now records everything needed to reconstruct the transfer: source amount, destination amount, and the rate used. The `ledger_entries` rows record amounts in each account's own currency:

- Source ledger entry: amount = -source_amount (in source currency).
- Destination ledger entry: amount = +destination_amount (in destination currency).

The CHECK constraint enforces the invariant: either same currency (rate = 1, amounts equal) or different currency (destination = source × rate).

**Aggregate boundary:** the `Transfer` aggregate now owns the invariant "source and destination amounts are consistent with the exchange rate." This invariant is enforced in the schema (CHECK) and in the application (the `Transfer` entity validates before persisting).

**What this teaches.** [[00-ER-Modeling]] and schema design are iterative: new requirements (multi-currency) reveal new attributes and invariants, which are added to the schema as constraints. The CHECK constraint is the database's enforcement of the domain invariant — defense in depth.

---

## What's next

- [[03-Transactions-Concurrency-Exercises]] — the hard correctness problems.
- [[04-End-To-End-Capstone]] — put it all together.
