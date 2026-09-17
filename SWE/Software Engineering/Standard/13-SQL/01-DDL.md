# DDL — Data Definition Language

> The SQL sub-language that creates, changes, and destroys schema objects. DDL is where the [[00-Schema-Design]] decisions become real — and where every choice has a runtime cost in locks, rewrites, and application compatibility.

## What you already know

From [[00-Schema-Design]]: a schema is tables + columns + types + constraints + indexes. DDL is the language that builds those five things. From [[04-Banking-Schema]]: the full Banking DDL with every constraint and index. From [[01-Primary-Foreign-Keys]] and [[02-Domain-Check-Constraints]]: the meaning of PKs, FKs, UNIQUE, CHECK, NOT NULL. From [[08-Trade-offs-Everywhere]]: every DDL change is a trade-off — between strictness and flexibility, between speed and safety, between reversible and irreversible migrations.

## Why this layer exists

The schema is not a static artifact. It evolves as the system evolves: tables are added, columns are renamed, indexes are created and dropped, constraints are tightened or relaxed. DDL is the language of that evolution. Without a disciplined DDL practice, schema changes become ad-hoc SQL run in production by a brave DBA at 2 AM.

## What is genuinely new here

The new idea is **the cost of DDL**. DDL is not free. `CREATE INDEX` reads every row. `ALTER TABLE ... ADD COLUMN ... DEFAULT ...` may rewrite the whole table. `DROP COLUMN` may take an exclusive lock. DDL is, in effect, a special class of writes that operates on the schema itself rather than the data — and it has the locking and performance characteristics of writes, magnified.

## Concepts

### The core verbs

| Verb | Effect |
|---|---|
| `CREATE` | Make a new schema object (table, index, view, type, function) |
| `ALTER` | Modify an existing object |
| `DROP` | Destroy an existing object |
| `TRUNCATE` | Empty a table (faster than `DELETE`; not standard DDL but adjacent) |

These apply to many object types: tables, indexes, views, materialized views, sequences, types, functions, triggers, constraints, schemas, databases.

### PostgreSQL column types

PostgreSQL has a rich type system. The most common in OLTP schemas:

| Type | Use | Notes |
|---|---|---|
| `BIGINT` | Surrogate PKs, foreign keys, counters | 8-byte integer; fits most IDs |
| `INTEGER` | Smaller integers | 4-byte; fine when 2^31 suffices |
| `NUMERIC(p,s)` | Money, exact decimal | Arbitrary precision; slower than float |
| `TEXT` | Variable-length strings | No length limit; preferred over `VARCHAR(n)` |
| `VARCHAR(n)` | Length-bounded strings | Use only when the bound is meaningful |
| `BOOLEAN` | True/false | Standard since SQL:1999 |
| `TIMESTAMPTZ` | Timestamps with time zone | PostgreSQL extension; preferred over `TIMESTAMP` |
| `DATE` | Calendar dates | No time component |
| `UUID` | Universally unique identifiers | PostgreSQL native; better than TEXT for UUIDs |
| `JSONB` | Structured documents, flexible payloads | Binary JSON; indexable |
| `BYTEA` | Binary blobs | Use sparingly |
| `SERIAL` / `BIGSERIAL` | Auto-incrementing integer | Legacy; prefer `GENERATED ALWAYS AS IDENTITY` |
| `ENUM` | Fixed set of string values | Useful but hard to evolve |

The modern PostgreSQL pattern for surrogate keys:

```sql
id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
```

This is SQL-standard (unlike `BIGSERIAL`) and gives you control over sequence behavior.

### Constraints

Every constraint is a guarantee the database makes about every row:

| Constraint | What it guarantees | Creates an index? |
|---|---|---|
| `PRIMARY KEY` | Unique, non-null | Yes (unique B-tree) |
| `UNIQUE` | Unique (NULLs allowed, multiple NULLs allowed) | Yes (unique B-tree) |
| `NOT NULL` | Every row has a value | No |
| `CHECK (expr)` | Expression evaluates to true | No |
| `FOREIGN KEY` | Values match a parent's PK or UNIQUE | Yes, on the FK column, by default |
| `EXCLUDE USING ...` | No two rows satisfy the operator | Yes (GiST or GIN) |

See [[02-Domain-Check-Constraints]] for the full treatment.

### Indexes

`CREATE INDEX` builds a physical access path. PostgreSQL supports:

- B-tree (default) — equality and range queries, ordered output.
- Hash — equality only.
- GIN — composite values (arrays, full-text, JSONB).
- GiST — geometric, range overlap.
- BRIN — block range min/max; tiny index for ordered tables.

Indexing strategy is a chapter of its own (see [[01-Indexing-Strategy]]). Here we focus on the syntax.

### The cost of DDL

This is the part most teams learn the hard way. DDL operations have a *lock level* and a *rewrite behavior*:

| Operation | Lock | Rewrite? | Cost |
|---|---|---|---|
| `CREATE INDEX` | Share lock on table | No (reads all rows) | O(N) reads, concurrent writes allowed |
| `CREATE INDEX CONCURRENTLY` (PostgreSQL) | Minimal lock | No | O(N) reads, slower but non-blocking |
| `ALTER TABLE ADD COLUMN ... NULL` | Brief exclusive lock | No | Cheap |
| `ALTER TABLE ADD COLUMN ... NOT NULL DEFAULT x` | Brief exclusive lock | No (PG 11+) | Cheap (metadata only) |
| `ALTER TABLE ADD COLUMN ... NOT NULL DEFAULT x` (pre-PG 11) | Exclusive lock | Yes (full rewrite) | O(N) reads and writes |
| `ALTER TABLE DROP COLUMN` | Brief exclusive lock | No (just metadata; old data lingers) | Cheap, but `VACUUM` later |
| `ALTER TABLE ALTER COLUMN TYPE` | Exclusive lock | Yes (full rewrite) | O(N) reads and writes |
| `ALTER TABLE ADD CONSTRAINT CHECK` | Share lock | No (validates existing rows) | O(N) reads to validate |
| `ALTER TABLE ADD CONSTRAINT FK` | Share lock | No | O(N) reads to validate |
| `ALTER TABLE ADD CONSTRAINT UNIQUE` | Exclusive lock | Yes (builds index) | O(N) reads and writes |
| `DROP INDEX` | Brief exclusive lock | No | Cheap |
| `DROP INDEX CONCURRENTLY` (PostgreSQL) | Minimal lock | No | Slower but non-blocking |
| `TRUNCATE` | Exclusive lock | No (just empties) | O(1) but blocks everything |

The two expensive classes are *full table rewrites* (ALTER COLUMN TYPE, pre-PG-11 NOT NULL DEFAULT) and *index builds* (UNIQUE constraint, non-concurrent CREATE INDEX). Both can take hours on large tables and block writes the entire time.

### Zero-downtime schema changes

The pattern for evolving a schema without downtime:

1. **Add the new column nullable.** `ALTER TABLE ... ADD COLUMN new_col INTEGER;` — cheap.
2. **Backfill in batches.** `UPDATE ... WHERE id BETWEEN ... AND ...` in a loop, with sleeps. Each batch holds a lock briefly.
3. **Add a CHECK constraint with NOT VALID.** `ALTER TABLE ... ADD CONSTRAINT chk_new CHECK (new_col IS NOT NULL) NOT VALID;` — does not scan existing rows.
4. **Validate the constraint.** `ALTER TABLE ... VALIDATE CONSTRAINT chk_new;` — scans rows but takes only a SHARE lock, allowing writes.
5. **Make the column NOT NULL** (PG 12+). The validator counts as proving non-null; the column can be marked NOT NULL without a rewrite.
6. **Deploy the application code that uses the new column.**

The same pattern applies to type changes (add new column, backfill, switch reads, switch writes, drop old column later), to index additions (`CREATE INDEX CONCURRENTLY`), and to constraint additions (NOT VALID then VALIDATE).

## Banking application — the full DDL

See [[04-Banking-Schema]] for the complete schema. Here we add the migration perspective: how the schema *evolves*.

```sql
-- Migration 001: initial schema (omitted — see 04-Banking-Schema)

-- Migration 002: add a daily transfer limit (additive, non-breaking)
ALTER TABLE accounts ADD COLUMN daily_transfer_limit NUMERIC(18,2);
-- Backfill existing accounts
UPDATE accounts SET daily_transfer_limit = 10000 WHERE daily_transfer_limit IS NULL;
-- Validate
ALTER TABLE accounts ADD CONSTRAINT chk_daily_limit
    CHECK (daily_transfer_limit >= 0) NOT VALID;
ALTER TABLE accounts VALIDATE CONSTRAINT chk_daily_limit;
-- Make NOT NULL
ALTER TABLE accounts ALTER COLUMN daily_transfer_limit SET NOT NULL;

-- Migration 003: add a partial index for fraud review (concurrent)
CREATE INDEX CONCURRENTLY idx_transfers_fraud_review
    ON transfers (created_at)
    WHERE status = 'FRAUD_REVIEW';

-- Migration 004: rename a column (two-step, backward compatible)
-- Step A: add new name
ALTER TABLE accounts ADD COLUMN currency_code TEXT DEFAULT 'USD';
UPDATE accounts SET currency_code = currency;
ALTER TABLE accounts VALIDATE CONSTRAINT chk_currency_code_present;  -- assumed
-- Step B: deploy app code that writes both columns
-- Step C: deploy app code that reads only the new column
-- Step D: drop the old column
ALTER TABLE accounts DROP COLUMN currency;
```

Notice the discipline: every migration is reversible (in principle), additive by default, and uses `CONCURRENTLY` and `NOT VALID` to avoid blocking writes.

## Code — DDL patterns to memorize

```sql
-- Pattern 1: surrogate primary key
CREATE TABLE t (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- ...
);

-- Pattern 2: composite primary key
CREATE TABLE account_counterparties (
    account_id      BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    counterparty_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    PRIMARY KEY (account_id, counterparty_id)
);

-- Pattern 3: partial unique index (PostgreSQL)
CREATE UNIQUE INDEX idx_accounts_iban_active
    ON accounts (iban)
    WHERE status <> 'CLOSED';

-- Pattern 4: concurrent index build (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_ledger_occurred_at
    ON ledger_entries (occurred_at);

-- Pattern 5: deferred foreign key (for cycles)
ALTER TABLE accounts
    ADD CONSTRAINT fk_default_counterparty
    FOREIGN KEY (default_counterparty_id) REFERENCES accounts(id)
    DEFERRABLE INITIALLY DEFERRED;

-- Pattern 6: ENUM type (use sparingly; hard to evolve)
CREATE TYPE account_status AS ENUM ('PENDING','ACTIVE','FROZEN','CLOSED');
ALTER TABLE accounts ALTER COLUMN status TYPE account_status USING status::account_status;

-- Pattern 7: adding a NOT NULL column with default (PG 11+, cheap)
ALTER TABLE accounts ADD COLUMN currency TEXT NOT NULL DEFAULT 'USD';
```

## What can go wrong

- **`ALTER TABLE` that rewrites.** On a 100M-row table, an unintended rewrite can take hours and block writes. Always check the lock level before running DDL.
- **`CREATE INDEX` without `CONCURRENTLY`.** Blocks writes for the duration of the build. On large tables in production, this is an outage.
- **`DROP COLUMN` that leaves data.** PostgreSQL marks the column dead but does not reclaim space until `VACUUM`. Disk usage looks unchanged.
- **`ALTER COLUMN TYPE` that breaks dependent views.** Changing a column type invalidates every view that references it. Drop the views, alter, recreate.
- **Adding a CHECK constraint without `NOT VALID`.** Scans the entire table with a SHARE lock. Use `NOT VALID` then `VALIDATE` for large tables.
- **Forgetting that DDL in PostgreSQL is transactional.** `CREATE TABLE`, `CREATE INDEX`, and most `ALTER` statements can be run inside a transaction and rolled back. (Exceptions: `CREATE INDEX CONCURRENTLY`, `DROP INDEX CONCURRENTLY`, `VACUUM` — these run outside transactions.)
- **ENUM evolution.** Adding a value to a PostgreSQL ENUM is cheap; removing or renaming one is painful (requires a full rewrite). Prefer a CHECK constraint over an ENUM for types that may evolve.
- **Migrations that are not reversible.** A `DROP COLUMN` cannot be undone by `ADD COLUMN` — the data is gone. Always have a rollback plan; for irreversible migrations, take a backup of the affected data first.

## Trade-offs

- **Inline constraints vs separate `ALTER TABLE`.** Inline is more readable and atomic; separate is more flexible (can be deferred, can be NOT VALID). Use inline for the initial schema; use `ALTER` for migrations.
- **`IDENTITY` vs `SERIAL`.** `IDENTITY` is SQL-standard and gives better control; `SERIAL` is older and creates a loose sequence. Modern PostgreSQL prefers `IDENTITY`.
- **ENUM vs CHECK vs reference table.** ENUM is fast and inline; CHECK is portable and flexible; reference table is the most flexible (you can add attributes to each value) but requires a JOIN. Use ENUM only for truly stable enumerations.
- **`VARCHAR(n)` vs `TEXT`.** `VARCHAR(n)` documents intent and is enforced; `TEXT` is unlimited. Use `VARCHAR(n)` when the bound is meaningful (IBAN has a fixed length); use `TEXT` otherwise.
- **Concurrent vs non-concurrent DDL.** `CONCURRENTLY` is slower and cannot run inside a transaction, but does not block writes. The trade-off is migration duration vs application availability. In production, almost always prefer `CONCURRENTLY`.

## Forward links

- [[02-DML]] — the language that operates on what DDL defines.
- [[00-Schema-Design]] — the conceptual layer.
- [[04-Banking-Schema]] — the Banking DDL in full.
- [[03-B-Tree-Indexes]] — what `CREATE INDEX` actually builds.
- [[01-Indexing-Strategy]] — choosing which indexes to create.
- [[08-Reading-EXPLAIN]] — seeing the cost of DDL choices in plans.
- [[04-Unit-of-Work]] — how ORM migrations interact with the schema.
