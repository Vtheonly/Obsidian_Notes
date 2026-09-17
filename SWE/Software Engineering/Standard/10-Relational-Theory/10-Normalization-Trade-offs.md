# Normalization Trade-offs — When to Stop

> Normalization removes redundancy and anomalies. Denormalization adds redundancy for read speed, simplicity, or scale. Neither is universally right. The job is to know which trade-off you are making and *why*. This chapter is the explicit declaration of the trade-off space introduced in [[08-Trade-offs-Everywhere]].

## What you already know

From [[08-Trade-offs-Everywhere]]: every design decision is a trade-off with four parts — axis, two ends, current position, the force pushing. Normalization is one such axis.

From [[06-1NF-2NF-3NF]] through [[09-DKNF]]: normalization is a sequence of increasingly strict constraints on dependencies, each removing a class of redundancy and its associated anomalies.

From [[06-Coupling-and-Cohesion]]: normalization is functional cohesion for tables; a denormalized table is a low-cohesion module that mixes fact types.

From [[03-Dependency-As-Root-Concept]]: redundancy is an uncontrolled dependency — change one copy, and the others become inconsistent. Normalization removes the redundancy; denormalization re-introduces it deliberately, with the dependency made explicit (via a trigger, a materialized view, or an application-level refresh).

## Why this layer exists

Engineers often treat normalization as a checkbox ("we normalized to 3NF, we're done") and denormalization as a sin. Both are wrong. Normalization and denormalization are *tools*, each suited to a different problem:

- **Normalize** the source of truth — the tables that are the system of record.
- **Denormalize** the read models — the tables (or views, or materialized views) that serve specific queries.

This separation is the foundation of CQRS (Command-Query Responsibility Segregation). The source of truth is normalized for integrity; the read models are denormalized for speed. The two are kept in sync by the write side (via triggers, materialized view refreshes, or event subscriptions).

This chapter formalizes the trade-off and gives rules for when to land on each end.

## What is genuinely new

- The **trade-off axes** of normalization: write cost vs. read cost; integrity vs. performance; simplicity vs. flexibility.
- The **rule**: normalize the source of truth, denormalize the read models.
- The **specific denormalization patterns**: materialized views, summary tables, denormalized columns, cached aggregates.
- The **costs** of denormalization: update anomalies (re-introduced), consistency windows, trigger overhead.

## Concepts

### The trade-off axes

| Axis | Normalized end | Denormalized end |
|---|---|---|
| **Write cost** | Low (one fact in one place) | High (update many copies) |
| **Read cost** | High (joins, aggregations) | Low (single-table read) |
| **Storage** | Compact (no redundancy) | Larger (redundant copies) |
| **Integrity** | Strong (one fact, no drift) | Weak (drift possible between copies) |
| **Schema complexity** | More tables, more FKs | Fewer tables, more columns |
| **Query complexity** | Complex (multi-join) | Simple (single-table) |
| **Change cost** | High (renormalization needed if FDs change) | Lower (denormalized table is more localized) |
| **Concurrency** | Fine-grained locks (different tables) | Coarse locks (one big table) |

There is no free lunch. Each cell on the right is paid for by a cell on the left. The question is: which cells matter for *this* workload?

### The rule: normalize the source of truth, denormalize the read models

This rule resolves 80% of normalization questions:

- **Source-of-truth tables** (the OLTP tables that record the system's authoritative state): normalize to BCNF. They are written often, queried in flexible ways, and must never drift. Denormalizing them invites anomalies.
- **Read-optimized tables** (the tables or materialized views that serve specific dashboards, reports, or APIs): denormalize freely. They are read often, written rarely (refreshed periodically), and serve one or a small set of queries.

The two layers are connected by an *update pipeline*: when the source of truth changes, the read models are updated (synchronously via trigger, asynchronously via event, or periodically via refresh job). The pipeline is the cost you accept for denormalization.

This is the same separation as **command** (write) and **query** (read) in CQRS — see [[04-Enterprise-Patterns]].

### When denormalization is right

- **Reporting / OLAP workloads**: queries scan large ranges and aggregate; joins are expensive; freshness is not critical (a few minutes stale is fine). Materialized views and star schemas are appropriate.
- **Pre-computed aggregates**: "current balance," "last 30 days transaction count," "average transaction value." Computing these on every read is expensive; storing them as columns or summary tables is cheaper.
- **Read-heavy APIs**: an API that returns a customer's full profile (with accounts, recent transactions, balance) can read from a denormalized view rather than joining five tables on every request.
- **Search indexes**: a search index is a denormalized projection optimized for keyword lookup. The source of truth is the relational schema; the search index is a read model.

### When denormalization is wrong

- **OLTP source-of-truth tables**: the tables that record transactions, accounts, customers. They must be normalized; denormalizing them creates anomalies that will eventually corrupt the data.
- **High-churn data**: if the denormalized column updates frequently (e.g., a `last_login_at` column on `customers`), the write cost of keeping it consistent may exceed the read benefit. Consider a separate `auth_log` table.
- **Distributed transactions**: if a denormalized column requires a cross-shard transaction to stay consistent, the latency cost is enormous. Keep it normalized (and accept eventual consistency for the read view) instead.

### Specific denormalization patterns

1. **Denormalized column** — add a redundant column to a table (e.g., `accounts.balance` as a denormalized copy of `SUM(ledger_entries.amount)`). Maintained by a trigger. Cost: trigger overhead on every write.

2. **Summary table** — a separate table that holds aggregates (e.g., `daily_account_balances(account_id, date, balance)`). Refreshed by a periodic job. Cost: staleness between refreshes.

3. **Materialized view** — a database-managed denormalized projection. Refreshed on demand or on schedule. PostgreSQL supports this natively — see [[07-Views-Materialized-Views]].

4. **Cached aggregate** — an application-level cache (Redis, Memcached) that holds the result of an expensive query. Refreshed on write or on TTL expiry. Cost: cache invalidation complexity.

5. **Read-optimized table** — a separate table that is a denormalized projection of the source of truth, updated by application code or event subscription. This is the CQRS pattern.

Each pattern has its own cost profile. Pick the one whose costs you can afford.

### The cost of denormalization

Denormalization is not free. You pay in three ways:

1. **Update anomalies re-introduced.** Every redundant copy is a place where data can drift. You need a mechanism (trigger, job, event handler) to keep them in sync. The mechanism has its own bugs.
2. **Consistency windows.** Asynchronous denormalization introduces a window during which the read model is stale. Applications must tolerate the staleness — or be designed to read from the source of truth when freshness matters.
3. **Schema evolution cost.** Adding a column to a denormalized table is cheap; changing the structure of a denormalized projection is expensive (you must rebuild it). Plan for migrations.

### The reconciliation job

For performance-critical denormalizations, a *reconciliation job* runs periodically to verify the denormalized data against the source of truth. Discrepancies are logged and (optionally) repaired. This is the safety net for when the trigger or event handler fails.

Example: a nightly job that checks `accounts.balance = SUM(ledger_entries.amount) WHERE account_id = accounts.id` for every account, and logs any mismatch. The mismatch is a bug in the write path; the reconciliation catches what the trigger missed.

## Banking application

The banking system ([[00-Banking-Case-Study]]) has both source-of-truth and read-optimized tables.

### Source of truth (normalized, BCNF)

- `customers`, `accounts`, `ledger_entries`, `transfers`, `account_signatories` — all in BCNF.
- These are the system of record. Every monetary movement is recorded here, immutably, with full transactional integrity.

### Read models (denormalized)

- `account_balances(account_id, current_balance, last_updated_at)` — a denormalized column on `accounts`, updated by a trigger when a ledger entry is written. Read by every API that displays an account.
- `daily_account_summary(account_id, date, opening_balance, closing_balance, transaction_count, total_credit, total_debit)` — a summary table, populated nightly by a job. Read by the statement-generation service.
- `customer_dashboard_view` — a PostgreSQL materialized view joining customer + accounts + recent transactions. Refreshed every 5 minutes. Read by the customer-facing dashboard API.
- `recent_transactions_cache` — a Redis cache of the last 10 transactions per account, populated on write. Read by the mobile app's "recent activity" widget.

Each read model is denormalized for a specific query pattern. The source of truth remains normalized.

### The reconciliation job

A nightly job:

```sql
-- Find accounts where the denormalized balance disagrees with the ledger sum.
SELECT a.id, a.balance AS denormalized,
       COALESCE(SUM(le.amount), 0) AS computed,
       a.balance - COALESCE(SUM(le.amount), 0) AS discrepancy
FROM accounts a
LEFT JOIN ledger_entries le ON le.account_id = a.id
GROUP BY a.id, a.balance
HAVING a.balance <> COALESCE(SUM(le.amount), 0);
```

Any rows returned are bugs. They are logged, alerts fire, and an on-call engineer investigates. The reconciliation does not fix the data automatically — that requires understanding *why* the drift occurred.

## Code

### Trigger-maintained denormalized column

```sql
-- Maintain accounts.balance as a denormalized copy of SUM(ledger_entries.amount)
CREATE OR REPLACE FUNCTION update_account_balance() RETURNS TRIGGER AS $$
BEGIN
    UPDATE accounts
    SET balance = balance + NEW.amount
    WHERE id = NEW.account_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER maintain_account_balance
AFTER INSERT ON ledger_entries
FOR EACH ROW EXECUTE FUNCTION update_account_balance();
```

This is denormalization in its simplest form: a column that is a function of other tables, kept in sync by a trigger. The trade-off: every `ledger_entries` insert now also updates `accounts`, adding write cost. The benefit: reading the balance is a single-column read, not an aggregate.

### PostgreSQL: materialized view for read-heavy queries

```sql
CREATE MATERIALIZED VIEW customer_dashboard AS
SELECT c.id            AS customer_id,
       c.legal_name,
       COUNT(DISTINCT a.id) AS account_count,
       COALESCE(SUM(a.balance), 0) AS total_balance,
       MAX(le.occurred_at) AS last_transaction_at
FROM customers c
LEFT JOIN accounts a ON a.customer_id = c.id
LEFT JOIN ledger_entries le ON le.account_id = a.id
GROUP BY c.id, c.legal_name
WITH DATA;

-- Refresh (PostgreSQL-specific syntax)
REFRESH MATERIALIZED VIEW CONCURRENTLY customer_dashboard;
```

`CONCURRENTLY` allows reads during refresh (PostgreSQL extension; requires a unique index on the materialized view). The trade-off: refresh cost (a full recomputation) vs. read speed (a single-table scan).

### Summary table populated by a periodic job

```sql
CREATE TABLE daily_account_summary (
    account_id        BIGINT NOT NULL,
    summary_date      DATE NOT NULL,
    opening_balance   NUMERIC(18,2) NOT NULL,
    closing_balance   NUMERIC(18,2) NOT NULL,
    transaction_count INTEGER NOT NULL,
    total_credit      NUMERIC(18,2) NOT NULL,
    total_debit       NUMERIC(18,2) NOT NULL,
    CONSTRAINT daily_summary_pk PRIMARY KEY (account_id, summary_date)
);

-- Populated nightly:
INSERT INTO daily_account_summary
SELECT a.id, CURRENT_DATE - 1,
       a.balance - COALESCE(SUM(le.amount), 0),   -- opening = closing - today's delta
       a.balance,                                   -- closing = current
       COUNT(le.id),
       COALESCE(SUM(le.amount) FILTER (WHERE le.amount > 0), 0),
       COALESCE(SUM(le.amount) FILTER (WHERE le.amount < 0), 0)
FROM accounts a
LEFT JOIN ledger_entries le
    ON le.account_id = a.id
   AND le.occurred_at >= CURRENT_DATE - 1
   AND le.occurred_at < CURRENT_DATE
GROUP BY a.id, a.balance;
```

This is the classic OLAP pattern — a denormalized summary table, populated by a job, read by reporting queries. The source of truth (`accounts`, `ledger_entries`) remains normalized and authoritative.

## What can go wrong

- **Denormalizing the source of truth.** This is the cardinal sin. Once the system of record has redundancy, you have anomalies — and anomalies in financial data cost real money.
- **Forgetting the reconciliation.** A denormalized column without a reconciliation job will eventually drift, silently. The first time you notice is when a customer complains.
- **Trigger cascades.** A trigger that maintains a denormalized column can fire other triggers, which fire others. The write path becomes a chain of implicit updates that is hard to reason about and slow under load.
- **Stale reads from materialized views.** `REFRESH MATERIALIZED VIEW` is not free; running it on every write defeats the purpose. Find the right cadence (5 minutes? hourly?) and document the staleness.
- **Cache invalidation.** The hardest problem in computer science. A denormalized cache that is not invalidated when the source changes serves stale data. Use either write-through invalidation or TTL with a short window.
- **Mixing read and write models in the same transaction.** A common CQRS mistake: writing to the read model in the same transaction as the source of truth. This couples them, defeating the purpose of separation.

## Trade-offs

- **Normalization vs. read performance.** The fundamental axis. Pick a position based on the read-to-write ratio and the latency budget.
- **Strong vs. eventual consistency for read models.** Synchronous trigger-maintained columns are strongly consistent but slow writes. Asynchronous event-driven read models are eventually consistent but fast writes. Pick based on whether stale reads are tolerable.
- **Schema complexity vs. query complexity.** Normalized schemas have more tables but simpler queries per table. Denormalized schemas have fewer tables but more columns. Pick based on the query patterns.
- **Storage cost vs. compute cost.** Denormalization trades storage (redundant copies) for compute (avoiding joins at read time). Storage is cheaper than compute at scale; the trade-off favors denormalization as data grows.
- **Trigger overhead vs. job overhead.** Triggers add per-write cost; jobs add periodic cost and staleness. Pick based on write volume and freshness requirements.

## Forward links

- [[11-Banking-Normalization-Walkthrough]] — full end-to-end decomposition from denormalized to BCNF.
- [[02-Denormalization-For-Reads]] — the dedicated chapter on denormalization patterns.
- [[07-Views-Materialized-Views]] — PostgreSQL's native denormalization tools.
- [[08-Trade-offs-Everywhere]] — the meta-force this chapter instantiates.
- [[04-Enterprise-Patterns]] — CQRS, the architectural pattern built on this separation.
- [[02-Aggregates]] — aggregate boundaries as the design-time version of "what to denormalize together."
- [[00-ACID]] and [[04-Eventual-Consistency]] — the consistency models that govern denormalized read models.
- [[00-Banking-Case-Study]] — the source of truth for the banking system.
