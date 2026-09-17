# Views and Materialized Views

> Two ways to save a query and give it a name. A `VIEW` is a saved query — it runs each time it is read. A `MATERIALIZED VIEW` is a saved result — it is read fast, refreshed periodically. The same idea (a named, queryable shape) at two different points on the freshness-vs-speed axis.

## What you already know

From [[04-Abstraction-and-Models]]: an abstraction is selective forgetting for a purpose. A view is an abstraction over the underlying tables — it hides the join, the filter, the projection, and exposes only the result's shape. From [[03-Dependency-As-Root-Concept]]: introducing an abstraction reduces or inverts dependencies; depending on a view instead of on the underlying tables reduces the dependency on physical schema changes. From [[08-Trade-offs-Everywhere]]: views are always fresh but slow; materialized views are fast but stale. The trade-off is the point.

## Why this layer exists

Two recurring problems in database design:

1. **The same query is written in fifty places.** Every service that needs "the current balance of an account" re-implements the join of `accounts` and `ledger_entries`. When the join changes (a new table is added, a column is renamed), every service breaks.
2. **The expensive query is run on every read.** A reporting dashboard runs a six-table join with an aggregate; it takes 30 seconds; users complain.

A view solves problem 1: define the query once, name it, let everyone query the name. A materialized view solves problem 2: run the expensive query once, store the result, let everyone read the stored result.

## What is genuinely new here

The new idea is **the query as a schema object**. A view is not just a saved query in your editor — it is a first-class schema object, with permissions, dependencies, and a name. Applications depend on the view, not on the underlying tables. The schema can evolve (rename a column, split a table, denormalize) without breaking the view's callers, as long as the view's definition is updated to compensate.

## Concepts

### VIEW — a saved query

```sql
CREATE VIEW account_balances AS
SELECT a.id, a.iban, a.customer_id,
       a.balance AS cached_balance,
       COALESCE(SUM(le.amount), 0) AS ledger_balance,
       a.balance - COALESCE(SUM(le.amount), 0) AS discrepancy
FROM accounts a
LEFT JOIN ledger_entries le ON le.account_id = a.id
GROUP BY a.id, a.iban, a.customer_id, a.balance;
```

Now `SELECT * FROM account_balances WHERE iban = 'GB29...';` is a valid query. The view's definition is expanded inline at parse time; the optimizer sees the full query and can optimize across the view boundary.

Properties of a regular view:

- **No stored data.** The view is a definition, not a table. Every read runs the underlying query.
- **Always fresh.** The view reflects the current state of the underlying tables.
- **Slow if the underlying query is slow.** Reading a view that joins six tables and aggregates still joins six tables and aggregates.
- **Updatable (with restrictions).** A view on a single table, with no aggregation, can be inserted into, updated, and deleted. The database translates the view operation into an operation on the underlying table. PostgreSQL extends this with `INSTEAD OF` triggers on views, allowing arbitrary updatable views.

### MATERIALIZED VIEW — a saved result

```sql
CREATE MATERIALIZED VIEW daily_balances AS
SELECT DATE(le.occurred_at) AS day,
       le.account_id,
       SUM(le.amount) AS daily_change,
       SUM(SUM(le.amount)) OVER (PARTITION BY le.account_id ORDER BY DATE(le.occurred_at)
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance
FROM ledger_entries le
GROUP BY DATE(le.occurred_at), le.account_id, le.occurred_at
ORDER BY le.account_id, DATE(le.occurred_at);

CREATE UNIQUE INDEX idx_daily_balances_pk ON daily_balances (account_id, day);
```

A materialized view stores the result of the query as a physical table. Reads are fast (it is just a table scan). The data is stale until the view is refreshed:

```sql
REFRESH MATERIALIZED VIEW daily_balances;
```

Properties:

- **Stored data.** The materialized view occupies disk space.
- **Stale until refreshed.** Changes to the underlying tables are not visible until `REFRESH`.
- **Fast to read.** It is a table; you can index it, partition it, scan it.
- **Slow to refresh.** `REFRESH` recomputes the entire view (by default).

### REFRESH MATERIALIZED VIEW CONCURRENTLY (PostgreSQL)

A regular `REFRESH` takes an exclusive lock on the materialized view — readers are blocked for the duration. On a large view, this can be minutes.

PostgreSQL offers `REFRESH MATERIALIZED VIEW CONCURRENTLY`, which:

- Allows reads during the refresh.
- Requires a unique index on the materialized view (so the database can identify rows to update).
- Is slower than a non-concurrent refresh (it does a diff, not a rebuild).

```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_balances;
```

### When to use each

| Situation | Use |
|---|---|
| The query is used by many callers; it is fast enough | VIEW |
| The query is slow; reads must be fast; staleness is acceptable | MATERIALIZED VIEW |
| The query must always reflect current data | VIEW |
| The query is for reporting; staleness of minutes/hours is fine | MATERIALIZED VIEW |
| You want to hide schema complexity from callers | VIEW |
| You want to pre-aggregate for a dashboard | MATERIALIZED VIEW |
| The underlying query changes often | VIEW (it is just a definition) |
| The underlying data changes often but the result is small | MATERIALIZED VIEW (cheap to refresh) |

### Updatable views

A view is *automatically updatable* if it is a simple projection of a single table (no joins, no aggregates, no DISTINCT). Inserts, updates, and deletes on the view are translated to operations on the underlying table.

```sql
CREATE VIEW active_accounts AS
SELECT id, iban, balance FROM accounts WHERE status = 'ACTIVE';

-- This INSERT goes to the underlying accounts table,
-- with status defaulted (or set explicitly)
INSERT INTO active_accounts (id, iban, balance) VALUES (..., 'GB29...', 100);
-- WARNING: this inserts a row with status = NULL (or the column default),
-- not 'ACTIVE'. The view's WHERE does not auto-apply to inserts.
```

The `CHECK OPTION` clause forces inserts and updates to satisfy the view's `WHERE`:

```sql
CREATE VIEW active_accounts AS
SELECT id, iban, balance FROM accounts WHERE status = 'ACTIVE'
WITH CHECK OPTION;

-- Now this insert fails: status is not ACTIVE
INSERT INTO active_accounts (id, iban, balance) VALUES (..., 'GB29...', 100);
```

For more complex views (with joins), PostgreSQL's `INSTEAD OF` triggers allow arbitrary updatable behavior.

### Views and dependencies

A view depends on its underlying tables. If you `ALTER TABLE` a column that a view references, the alteration may fail (or the view may be invalidated). PostgreSQL is conservative: dropping a column that a view uses requires `CASCADE`, which also drops the view.

This is a feature: views make schema dependencies explicit. You cannot silently break a view by dropping a column.

## Banking application

### View 1: account balances (always fresh, for OLTP)

```sql
CREATE OR REPLACE VIEW account_balances AS
SELECT a.id, a.iban, a.customer_id,
       a.balance AS cached_balance,
       COALESCE(SUM(le.amount), 0) AS ledger_balance,
       a.balance - COALESCE(SUM(le.amount), 0) AS discrepancy
FROM accounts a
LEFT JOIN ledger_entries le ON le.account_id = a.id
GROUP BY a.id, a.iban, a.customer_id, a.balance;

-- Usage: a reconciliation query
SELECT id, iban, cached_balance, ledger_balance, discrepancy
FROM account_balances
WHERE discrepancy <> 0;
```

This view is used by the reconciliation job (a few times a day). It is always fresh — no staleness to worry about. The underlying join is expensive, but the reconciliation job runs rarely.

### View 2: customer summary (always fresh, for the customer-facing app)

```sql
CREATE OR REPLACE VIEW customer_summary AS
SELECT c.id, c.legal_name, c.email,
       COUNT(a.id) FILTER (WHERE a.status = 'ACTIVE') AS active_accounts,
       COUNT(a.id) FILTER (WHERE a.status = 'CLOSED') AS closed_accounts,
       COALESCE(SUM(a.balance) FILTER (WHERE a.status = 'ACTIVE'), 0) AS total_balance
FROM customers c
LEFT JOIN accounts a ON a.customer_id = c.id
GROUP BY c.id, c.legal_name, c.email;
```

The customer-facing app reads this view to render the dashboard. It joins two tables and aggregates, but the query is well-indexed and fast enough.

### Materialized view: daily balances (refreshed nightly, for reporting)

```sql
CREATE MATERIALIZED VIEW daily_balances AS
SELECT DATE(le.occurred_at) AS day,
       le.account_id,
       SUM(le.amount) AS daily_change,
       SUM(SUM(le.amount)) OVER (PARTITION BY le.account_id
                                 ORDER BY DATE(le.occurred_at)
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_balance
FROM ledger_entries le
GROUP BY DATE(le.occurred_at), le.account_id
ORDER BY le.account_id, DATE(le.occurred_at);

CREATE UNIQUE INDEX idx_daily_balances_pk ON daily_balances (account_id, day);

-- Refresh nightly
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_balances;
```

The reporting dashboard reads from `daily_balances`. The query is a simple `SELECT` on a small materialized view — milliseconds. The cost is paid once a night in the refresh.

### Materialized view: monthly statement summary

```sql
CREATE MATERIALIZED VIEW monthly_summary AS
SELECT DATE_TRUNC('month', le.occurred_at)::DATE AS month,
       a.id AS account_id,
       COUNT(*) AS transaction_count,
       SUM(le.amount) AS net_change,
       SUM(le.amount) FILTER (WHERE le.amount > 0) AS total_credits,
       SUM(le.amount) FILTER (WHERE le.amount < 0) AS total_debits
FROM ledger_entries le
JOIN accounts a ON a.id = le.account_id
GROUP BY DATE_TRUNC('month', le.occurred_at), a.id;

CREATE UNIQUE INDEX idx_monthly_summary_pk ON monthly_summary (account_id, month);

-- Refreshed monthly, but can be refreshed on-demand for the current month
REFRESH MATERIALIZED VIEW monthly_summary;
```

## Code — common patterns

```sql
-- Pattern 1: rename a column without breaking callers
CREATE VIEW accounts_public AS
SELECT id, iban, balance AS current_balance, status
FROM accounts;
-- Callers query accounts_public; the underlying accounts table can rename balance
-- without breaking them.

-- Pattern 2: hide soft-deleted rows
CREATE VIEW active_customers AS
SELECT * FROM customers WHERE status <> 'CLOSED';
-- Application code never sees closed customers.

-- Pattern 3: row-level security via view
CREATE VIEW my_accounts AS
SELECT a.* FROM accounts a
WHERE a.customer_id = current_setting('app.customer_id')::BIGINT;
-- Each user sees only their own accounts. Pair with SET LOCAL app.customer_id.

-- Pattern 4: refresh a materialized view in a transaction
BEGIN;
REFRESH MATERIALIZED VIEW daily_balances;
-- The refresh is atomic; readers see either the old or the new version, never partial.
COMMIT;

-- Pattern 5: schedule a refresh (PostgreSQL: pg_cron extension)
-- SELECT cron.schedule('refresh_daily', '0 3 * * *', 'REFRESH MATERIALIZED VIEW CONCURRENTLY daily_balances');
```

## What can go wrong

- **Views that hide expensive queries.** A view that joins six tables looks like a simple table to callers. They write `SELECT * FROM the_view` and wonder why it is slow.
- **Materialized views that grow stale.** A reporting dashboard that shows yesterday's data because nobody refreshed the materialized view. Set up monitoring on refresh time and staleness.
- **Refresh failures.** If the underlying schema changes (a column is dropped), the refresh fails. The materialized view keeps its old data, which becomes increasingly stale. Alert on refresh failures.
- **`CONCURRENTLY` requirements.** It requires a unique index. Forgetting the index means `CONCURRENTLY` fails. Always create the unique index when you create the materialized view.
- **Materialized view bloat.** A materialized view that is refreshed often may bloat (dead rows from updates). `VACUUM` it periodically.
- **Updatable view surprises.** Inserting into a view that has a `WHERE` clause does not auto-apply the `WHERE` to the inserted row. Use `WITH CHECK OPTION`.
- **View dependency chains.** A view on a view on a view is hard to debug. The optimizer usually flattens them, but plan complexity grows.
- **Materialized views as a substitute for proper schema design.** If every query goes through a materialized view, the underlying schema is probably wrong. Reconsider.
- **Permissions.** A view's owner must have permissions on the underlying tables. Callers need permissions on the view, not on the underlying tables. This is a feature (security via views) and a surprise (callers cannot query the underlying tables directly).

## Trade-offs

- **VIEW vs MATERIALIZED VIEW.** VIEW is fresh and slow; MATERIALIZED VIEW is fast and stale. Pick based on the read pattern and the staleness tolerance.
- **VIEW vs denormalized column.** A view computes on read; a denormalized column is computed on write. The view is always correct; the column is fast. See [[02-Denormalization-For-Reads]].
- **Refresh frequency vs freshness.** More frequent refreshes mean fresher data but more load. The right frequency depends on the read pattern.
- **Refresh strategy: full vs incremental.** A full refresh is simple but expensive. An incremental refresh (update only changed rows) is fast but complex. PostgreSQL does not support incremental refresh natively; you must build it with triggers or a custom refresh function.
- **CONCURRENTLY vs non-concurrent refresh.** `CONCURRENTLY` does not block readers but is slower and requires a unique index. The trade-off is reader availability vs refresh speed.
- **View-based security vs row-level security (RLS).** Views can implement per-user filtering; PostgreSQL's RLS does it natively. RLS is more robust; views are simpler.
- **Updatable views vs direct table access.** Updatable views add a layer of indirection; direct table access is simpler. Use updatable views when you need to enforce a constraint or hide a column.

## Forward links

- [[04-Abstraction-and-Models]] — the conceptual foundation.
- [[00-Schema-Design]] — views as schema objects.
- [[01-DDL]] — `CREATE VIEW` and `CREATE MATERIALIZED VIEW` syntax.
- [[03-Select-Join-Group]] — the queries views save.
- [[02-Denormalization-For-Reads]] — the trade-off between views and denormalized columns.
- [[03-Caching]] — materialized views as a database-level cache.
- [[04-Partitioning-And-Sharding]] — materialized views can be partitioned like tables.
- [[09-Banking-SQL]] — the Banking views and materialized views in action.
