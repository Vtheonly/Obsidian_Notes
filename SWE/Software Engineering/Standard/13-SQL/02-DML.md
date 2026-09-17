# DML — Data Manipulation Language

> The SQL sub-language that writes data: `INSERT`, `UPDATE`, `DELETE`, and the upsert (`MERGE` / `ON CONFLICT`). DML is where invariants meet reality — every insert must satisfy every constraint, every update must respect every key, every delete must cascade or be restricted.

## What you already know

From [[02-Domain-Check-Constraints]]: every write is validated against the schema's constraints. From [[00-Banking-Case-Study]]: invariant 7 requires transfers to be idempotent — the same request, retried, must produce the same result. From [[05-Identity-State-Lifecycle]]: a surrogate key is generated; the application does not supply it. From [[00-ACID]]: a write is not durable until the transaction commits. From [[08-Trade-offs-Everywhere]]: every DML statement is a trade-off between safety (constraints, transactions) and speed (fewer round-trips, larger batches).

## Why this layer exists

DDL builds the schema; DML populates it. The two are paired: every DML statement is a contract between the application and the schema. If the application violates a constraint, the statement fails. If the application commits, the data is durable. DML is the language of *change* in a system designed to resist uncontrolled change.

## What is genuinely new here

The new idea is **idempotent writes** — the SQL pattern that makes retries safe. Combined with `RETURNING` and `ON CONFLICT`, modern SQL lets you express "insert this if absent, return the existing if present" in a single statement, without a SELECT-then-INSERT race.

## Concepts

### INSERT

The simplest DML statement. Inserts one or more rows:

```sql
INSERT INTO accounts (customer_id, iban, account_type)
VALUES (42, 'GB29NWBK60161331926819', 'CHECKING');
```

Notes:

- Columns not listed get their DEFAULT value (or NULL if no default).
- The order of columns in the VALUES list must match the column list.
- Multi-row inserts are supported and faster than per-row inserts:

```sql
INSERT INTO accounts (customer_id, iban, account_type)
VALUES
    (42, 'GB29NWBK60161331926819', 'CHECKING'),
    (42, 'GB29NWBK60161331926820', 'SAVINGS'),
    (43, 'GB29NWBK60161331926821', 'CHECKING');
```

### UPDATE

Modifies existing rows:

```sql
UPDATE accounts
SET balance = balance - 100, status = 'ACTIVE'
WHERE id = 42;
```

Notes:

- Without `WHERE`, updates every row in the table. Always include a `WHERE`.
- The right-hand side can reference the current row's columns (`balance = balance - 100`).
- `UPDATE` returns the number of rows affected. In PostgreSQL, `RETURNING *` returns the affected rows themselves.
- `UPDATE` is, in fact, a `DELETE` plus an `INSERT` internally in PostgreSQL (because of MVCC — see [[04-MVCC]]). This means an `UPDATE` of every column of every row rewrites the table.

### DELETE

Removes rows:

```sql
DELETE FROM ledger_entries WHERE occurred_at < '2020-01-01';
```

Notes:

- Without `WHERE`, deletes every row. (Use `TRUNCATE` instead if you really want all rows — it is faster.)
- `DELETE` does not reclaim disk space immediately; the space is reused by future inserts. `VACUUM` (PostgreSQL) reclaims it.
- Foreign key constraints are checked. `ON DELETE CASCADE` propagates the delete; `ON DELETE RESTRICT` blocks it.

### MERGE / UPSERT

`MERGE` (SQL:2003) is the standard upsert: "if the row exists, update it; otherwise, insert it." PostgreSQL historically used `INSERT ... ON CONFLICT` for the same purpose; PostgreSQL 15+ also supports `MERGE`.

```sql
-- PostgreSQL: ON CONFLICT upsert
INSERT INTO accounts (customer_id, iban, account_type, balance)
VALUES (42, 'GB29NWBK60161331926819', 'CHECKING', 100)
ON CONFLICT (iban) DO UPDATE
SET balance = accounts.balance + 100;
```

The `ON CONFLICT (iban)` clause says: if a row with the same `iban` already exists, instead of failing, do the `DO UPDATE` (or `DO NOTHING`). The special `EXCLUDED` table refers to the row that was *going* to be inserted.

### RETURNING (PostgreSQL)

`RETURNING` returns the affected rows, eliminating the need for a follow-up `SELECT`:

```sql
INSERT INTO accounts (customer_id, iban, account_type)
VALUES (42, 'GB29NWBK60161331926819', 'CHECKING')
RETURNING id, opened_at;
```

Without `RETURNING`, the application would have to run a separate `SELECT currval('accounts_id_seq')` and `SELECT opened_at FROM accounts WHERE id = ?` — two round-trips and a race condition. With `RETURNING`, the database returns the generated values atomically.

`RETURNING` works on `INSERT`, `UPDATE`, and `DELETE`. It is a PostgreSQL extension (also supported by SQLite; not in the SQL standard until SQL:2023).

### Idempotent writes

The pattern that makes retries safe. From [[00-Banking-Case-Study]] invariant 7: a transfer request with the same idempotency key produces the same result, even if retried.

The naive (wrong) pattern:

```sql
-- BAD: race condition between SELECT and INSERT
SELECT id FROM transfers WHERE idempotency_key = 'abc';
-- if no row:
INSERT INTO transfers (...) VALUES (...);
```

Two concurrent retries can both see "no row" and both insert. The idempotency key is violated; one insert fails.

The correct pattern uses `ON CONFLICT`:

```sql
-- PostgreSQL: idempotent insert
INSERT INTO transfers (from_account_id, to_account_id, amount, idempotency_key, status)
VALUES ($1, $2, $3, 'abc', 'PENDING')
ON CONFLICT (idempotency_key) DO NOTHING
RETURNING id, status;
```

- If the key is new: insert succeeds, returns the new row.
- If the key exists: insert is skipped, returns the existing row.
- Concurrent retries: one wins the insert; the other gets the existing row. No race.

This is the SQL implementation of invariant 7. The same pattern works for ledger entries (each entry has an idempotency key), for notifications (one per event), and for any "exactly-once" write.

### Idempotent updates

For updates, idempotency means: applying the same update twice has the same effect as applying it once.

```sql
-- Idempotent: setting an absolute value
UPDATE accounts SET status = 'ACTIVE' WHERE id = 42;

-- Non-idempotent: relative update
UPDATE accounts SET balance = balance - 100 WHERE id = 42;
-- Running this twice debits 200.
```

For relative updates, the idempotency key pattern is essential: only apply the update if the key has not been seen.

```sql
-- PostgreSQL: idempotent debit
WITH new_entry AS (
    INSERT INTO ledger_entries (account_id, amount, idempotency_key)
    VALUES (42, -100, 'debit-abc')
    ON CONFLICT (idempotency_key) DO NOTHING
    RETURNING id
)
UPDATE accounts
SET balance = balance - 100
WHERE id = 42
  AND EXISTS (SELECT 1 FROM new_entry);
```

If the idempotency key is already present, no new entry is created, the `EXISTS` is false, and the `UPDATE` does nothing. Retry-safe.

## Banking application — the idempotent transfer

The transfer flow from [[02-Use-Cases]] as idempotent SQL:

```sql
-- PostgreSQL: idempotent transfer creation
INSERT INTO transfers (from_account_id, to_account_id, amount, currency, idempotency_key, status)
VALUES ($1, $2, $3, 'USD', $4, 'PENDING')
ON CONFLICT (idempotency_key) DO UPDATE
SET status = transfers.status  -- no-op update to force RETURNING of existing row
RETURNING id, status, (xmax = 0) AS was_inserted;
```

The `(xmax = 0)` trick (PostgreSQL) lets the application distinguish "I just inserted this" from "this already existed." See [[04-MVCC]] for what `xmax` means.

After the transfer row exists, the application proceeds:

```sql
-- PostgreSQL: idempotent ledger entries
INSERT INTO ledger_entries (account_id, transfer_id, amount, idempotency_key)
VALUES
    ($from_acct, $transfer_id, -$amount, $idem_key || '-debit'),
    ($to_acct,   $transfer_id,  $amount, $idem_key || '-credit')
ON CONFLICT (idempotency_key) DO NOTHING;

-- Idempotent balance update (only if entries were inserted)
UPDATE accounts SET balance = balance - $amount WHERE id = $from_acct;
UPDATE accounts SET balance = balance + $amount WHERE id = $to_acct;

-- Mark transfer complete
UPDATE transfers SET status = 'COMPLETED', completed_at = now()
WHERE id = $transfer_id AND status = 'PENDING';
```

The full transfer is one transaction (see [[06-Transactions-In-SQL]]). Each piece is idempotent, so retries anywhere in the flow are safe.

## Code — common DML patterns

```sql
-- Pattern 1: bulk insert
INSERT INTO notifications (customer_id, channel, template, payload)
SELECT id, 'EMAIL', 'monthly_statement', jsonb_build_object('month', $1)
FROM customers WHERE status = 'VERIFIED';

-- Pattern 2: update with RETURNING for atomic read-after-write
UPDATE accounts SET status = 'CLOSED', closed_at = now()
WHERE id = 42 AND status <> 'CLOSED'
RETURNING id, closed_at;

-- Pattern 3: delete with RETURNING for audit
DELETE FROM pending_transfers
WHERE created_at < now() - interval '24 hours'
RETURNING id, idempotency_key;  -- application logs each deleted row

-- Pattern 4: upsert with conditional update (only update if newer)
INSERT INTO account_balances (account_id, balance, as_of)
VALUES ($1, $2, now())
ON CONFLICT (account_id) DO UPDATE
SET balance = EXCLUDED.balance,
    as_of = EXCLUDED.as_of
WHERE account_balances.as_of < EXCLUDED.as_of;

-- Pattern 5: MERGE (SQL:2003, PostgreSQL 15+)
MERGE INTO account_summary AS t
USING (SELECT account_id, SUM(amount) AS bal FROM ledger_entries GROUP BY account_id) AS s
ON t.account_id = s.account_id
WHEN MATCHED THEN UPDATE SET balance = s.bal
WHEN NOT MATCHED THEN INSERT (account_id, balance) VALUES (s.account_id, s.bal);
```

## What can go wrong

- **`UPDATE` without `WHERE`.** Updates every row. A classic production incident. Some databases (and most ORM tools) refuse to run an `UPDATE` or `DELETE` without a `WHERE` without an explicit override.
- **`DELETE` that cascades unexpectedly.** `ON DELETE CASCADE` on a foreign key can wipe out a tree of data with one statement. Always check the FK definitions before deleting.
- **Race conditions in SELECT-then-INSERT.** The non-idempotent pattern. Always use `ON CONFLICT` (PostgreSQL) or `MERGE` (SQL:2003).
- **Non-idempotent updates applied on retry.** A retry of `UPDATE accounts SET balance = balance - 100` debits twice. Either use absolute values ("set balance to X") or guard with an idempotency key.
- **Locking the whole table.** An `UPDATE` that matches many rows takes row-level locks, but if the rows are most of the table, the engine may escalate to a table lock. Use batches.
- **Long-running transactions holding locks.** An `UPDATE` in a transaction that takes 10 seconds to commit holds its locks for 10 seconds. Other writers block. Keep transactions short.
- **`RETURNING` not supported.** On databases without `RETURNING` (older SQL Server, Oracle before 12c), the application must run a separate `SELECT` after the insert — and use a sequence or `OUTPUT` clause to get the generated ID.
- **`ON CONFLICT` on the wrong column.** The conflict target must be a unique constraint or unique index. If the column is not unique, `ON CONFLICT` errors.
- **Triggers firing invisibly.** DML can fire triggers (see [[03-Triggers-As-Constraints]]) that modify or reject the operation. Always know which triggers exist on the tables you write to.

## Trade-offs

- **Idempotency vs simplicity.** Idempotent writes are safer but more verbose (extra column, extra index, `ON CONFLICT` clause). The trade-off is worth it for any write that may be retried.
- **Single-row vs batch.** Single-row inserts are simple and easy to reason about; batch inserts are 5-10x faster. Use batches for high-volume writes (ledger entries, notifications).
- **`ON CONFLICT DO NOTHING` vs `DO UPDATE`.** DO NOTHING is simpler; DO UPDATE lets you return the existing row. Use DO UPDATE when you need to know whether the row was inserted or already existed.
- **`MERGE` vs `ON CONFLICT`.** `MERGE` is standard; `ON CONFLICT` is PostgreSQL-specific. `ON CONFLICT` is more concise for the common upsert case; `MERGE` is more general (can express conditional logic).
- **Absolute vs relative updates.** Absolute (`SET balance = X`) is idempotent; relative (`SET balance = balance - X`) is not. Relative is sometimes necessary (concurrent updates to the same row); in that case, combine with an idempotency key.
- **`RETURNING` vs separate SELECT.** `RETURNING` saves a round-trip and is atomic. Use it whenever supported.

## Forward links

- [[03-Select-Join-Group]] — what to do with the data you inserted.
- [[06-Transactions-In-SQL]] — wrapping DML in atomic units.
- [[00-ACID]] — what atomicity, isolation, and durability mean for DML.
- [[04-MVCC]] — how PostgreSQL isolates concurrent DML without locking readers.
- [[04-Unit-of-Work]] — the ORM pattern that batches DML.
- [[00-Banking-Case-Study]] — invariant 7 (idempotency) is the driver.
- [[09-Banking-SQL]] — full transfer transaction using these patterns.
