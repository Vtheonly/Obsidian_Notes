# Banking Query Plans — End to End

> The capstone of the Database Internals chapter. We take five realistic Banking queries, show each `EXPLAIN ANALYZE` output, explain the plan choice, identify performance issues, and show how an index or rewrite changes the plan. This is the chapter where everything from [[00-Storage-Hierarchy]] through [[08-Reading-EXPLAIN]] comes together on real queries.

## What you already know

Everything from chapters 00 through 08 of this folder. Specifically: pages and the storage hierarchy (00, 01), the buffer pool (02), B-tree and hash indexes (03, 04), join algorithms (05), the query pipeline (06), the cost model (07), and how to read EXPLAIN (08).

## Why this layer exists

Theory without practice is fragile. The earlier chapters taught the *concepts* of database internals. This chapter applies those concepts to *real queries* on the Banking schema, showing how each choice in the schema and indexes ripples through to plan selection and execution time. By the end, you should be able to look at any `EXPLAIN ANALYZE` output and reason about *why* the planner chose what it chose, *whether* it chose well, and *what to change* if it didn't.

## What is genuinely new here

The **synthesis**: taking five query shapes that recur in every OLTP system (point lookup, range scan, join for report, aggregate, fraud-detection scan), and showing the planner's behavior on each — including two cases where the plan is wrong and the fix.

## Concepts (recap)

For each query we will examine:

1. **Schema and indexes in play.**
2. **The query.**
3. **The initial plan** (from `EXPLAIN ANALYZE`).
4. **Why the planner chose it.**
5. **Issues** — if any.
6. **The fix** — index change, query rewrite, statistics update, or `work_mem` adjustment.
7. **The improved plan.**

Assume the Banking schema from [[04-Banking-Schema]]:

```sql
CREATE TABLE customers (
  id BIGINT PRIMARY KEY,
  name TEXT NOT NULL,
  country CHAR(2) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE accounts (
  id BIGINT PRIMARY KEY,
  iban TEXT UNIQUE NOT NULL,
  customer_id BIGINT NOT NULL REFERENCES customers(id),
  account_type TEXT NOT NULL CHECK (account_type IN ('CHECKING','SAVINGS')),
  current_balance NUMERIC(18,2) NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX accounts_customer_id_idx ON accounts(customer_id);

CREATE TABLE transfers (
  id BIGINT PRIMARY KEY,
  source_account_id BIGINT NOT NULL REFERENCES accounts(id),
  dest_account_id BIGINT NOT NULL REFERENCES accounts(id),
  amount NUMERIC(18,2) NOT NULL,
  status TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX transfers_source_account_id_created_at_idx
  ON transfers(source_account_id, created_at DESC);
CREATE INDEX transfers_dest_account_id_idx ON transfers(dest_account_id);
CREATE UNIQUE INDEX transfers_idempotency_key_unique_idx ON transfers(idempotency_key);

CREATE TABLE ledger_entries (
  id BIGINT PRIMARY KEY,
  account_id BIGINT NOT NULL REFERENCES accounts(id),
  transfer_id BIGINT REFERENCES transfers(id),
  amount NUMERIC(18,2) NOT NULL,
  occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ledger_entries_account_id_occurred_at_idx
  ON ledger_entries(account_id, occurred_at DESC);
```

Scale: 10M customers, 10M accounts, 500M transfers, 1B ledger entries.

## Banking application — the five queries

### Query 1: Point lookup by IBAN — `GET /accounts/{iban}`

```sql
SELECT id, iban, current_balance, status
FROM accounts
WHERE iban = 'GB29NWBK60161331926819';
```

**Initial plan:**

```
 Index Scan using accounts_iban_idx on accounts
   (cost=0.42..8.04 rows=1 width=64) (actual time=0.020..0.022 rows=1 loops=1)
   Index Cond: (iban = 'GB29NWBK60161331926819'::text)
   Buffers: shared hit=4
 Planning Time: 0.110 ms
 Execution Time: 0.045 ms
```

**Why this plan:** the planner sees a unique index on `iban`, estimates 1 row (perfect), and picks Index Scan. The B-tree is 3 levels deep at 10M rows (see [[03-B-Tree-Indexes]]), so 3 index page reads + 1 heap read = 4 buffers. All cached → all hits.

**Issues:** none. This is a textbook fast query.

**Possible improvement — Index Only Scan:**

If we add `current_balance` and `status` to the index using `INCLUDE`:

```sql
CREATE INDEX accounts_iban_covering_idx
  ON accounts (iban) INCLUDE (current_balance, status);
```

**Improved plan:**

```
 Index Only Scan using accounts_iban_covering_idx on accounts
   (cost=0.42..4.05 rows=1 width=64) (actual time=0.010..0.012 rows=1 loops=1)
   Index Cond: (iban = 'GB29NWBK60161331926819'::text)
   Buffers: shared hit=3
 Planning Time: 0.090 ms
 Execution Time: 0.025 ms
```

The heap visit is gone — 3 buffer reads instead of 4. Speedup is marginal here (~20 µs → ~12 µs), but at 100K requests/sec, this is real. The trade-off: the index leaf is now larger (carries two extra columns), so the index takes more RAM. Worth it for the bank's most-called endpoint.

### Query 2: Range scan on ledger entries — customer statement

```sql
SELECT id, amount, occurred_at, transfer_id
FROM ledger_entries
WHERE account_id = 42
  AND occurred_at >= '2024-01-01'
  AND occurred_at < '2024-04-01'
ORDER BY occurred_at DESC;
```

**Initial plan:**

```
 Index Scan using ledger_entries_account_id_occurred_at_idx on ledger_entries
   (cost=0.56..245.30 rows=210 width=128) (actual time=0.030..1.230 rows=187 loops=1)
   Index Cond: ((account_id = 42) AND (occurred_at >= '2024-01-01') AND (occurred_at < '2024-04-01'))
   Buffers: shared hit=12 read=4
 Planning Time: 0.140 ms
 Execution Time: 1.420 ms
```

**Why this plan:** the composite index `(account_id, occurred_at DESC)` is a perfect match. The B-tree descends to `(42, 2024-04-01)` and walks backward through leaves until `(42, 2024-01-01)`. The leaf chain is already in `occurred_at DESC` order, so no Sort node is needed.

**Issues:**
- `read=4` — 4 cold pages. For very active accounts, this is the historical pages. For most accounts, all hot.
- The estimated 210 vs actual 187 — close (12% off, fine).

**No fix needed.** This is the optimal plan.

**Edge case — wrong index for a different query shape:**

If a query asks for `WHERE occurred_at >= '2024-01-01'` (no `account_id` filter), the composite index is *useless* — the index is sorted by `account_id` first, then `occurred_at`. The planner falls back to a Seq Scan. Fix: add a separate index on `occurred_at` if this query is common (e.g., for daily reports). See [[01-Indexing-Strategy]] for the multi-index trade-off.

### Query 3: Customer statement with transfer details — the join

```sql
SELECT t.id, t.amount, t.status, t.created_at,
       sa.iban AS source_iban, da.iban AS dest_iban
FROM transfers t
JOIN accounts sa ON t.source_account_id = sa.id
JOIN accounts da ON t.dest_account_id = da.id
WHERE sa.customer_id = 42
  AND t.created_at >= now() - interval '30 days'
ORDER BY t.created_at DESC
LIMIT 100;
```

**Initial plan:**

```
 Limit  (cost=2.10..820.30 rows=85 width=80) (actual time=0.080..3.450 rows=78 loops=1)
   Buffers: shared hit=215 read=8
   -> Nested Loop  (cost=2.10..820.30 rows=85 width=80) (actual time=0.080..3.450 rows=78 loops=1)
      Buffers: shared hit=215 read=8
      -> Index Scan using accounts_customer_id_idx on accounts sa
         (cost=0.42..8.50 rows=5 width=40) (actual time=0.020..0.080 rows=5 loops=1)
         Index Cond: (customer_id = 42)
         Buffers: shared hit=4
      -> Nested Loop  (cost=1.68..811.00 rows=17 width=56) (actual time=0.050..0.650 rows=16 loops=5)
         Buffers: shared hit=211 read=8
         -> Index Scan using transfers_source_account_id_created_at_idx on transfers t
            (cost=1.24..780.00 rows=17 width=40) (actual time=0.030..0.500 rows=16 loops=5)
            Index Cond: ((source_account_id = sa.id) AND (created_at >= (now() - '30 days'::interval)))
            Buffers: shared hit=180 read=8
         -> Index Scan using accounts_pkey on accounts da
            (cost=0.43..1.85 rows=1 width=40) (actual time=0.005..0.006 rows=1 loops=78)
            Index Cond: (id = t.dest_account_id)
            Buffers: shared hit=78
 Planning Time: 1.230 ms
 Execution Time: 3.580 ms
```

**Why this plan:**

1. **Outermost:** `Index Scan on accounts by customer_id` — 5 accounts for this customer.
2. **Middle:** `Nested Loop` with `Index Scan on transfers by (source_account_id, created_at)` — for each account, find recent transfers. 5 accounts × 16 transfers each = 78 transfers.
3. **Innermost:** `Index Scan on accounts (PK)` — for each transfer, look up the destination account. 78 lookups, 1 row each.
4. **Sort + Limit:** Notice there's no Sort node! The index `transfers_source_account_id_created_at_idx` is `DESC` on `created_at`, so each scan produces transfers in `created_at DESC` order. But the Limit needs the top-100 across all 5 accounts — PostgreSQL uses a *top-N heapsort* implicit in the Limit? Actually, here the Limit just takes the first 100 from the nested loop output. This is incorrect if the rows aren't globally sorted!

Wait — there *is* a subtle issue. Let me re-examine. The plan shows `Limit` directly above `Nested Loop`, with no `Sort`. This means the Limit takes the first 100 rows produced, in whatever order the nested loop emits them. The nested loop emits rows grouped by source account (5 groups, 16 each), each group sorted by `created_at DESC`. So the output is *not globally sorted*. The LIMIT will return 100 rows from the first ~6 source accounts (only 5 here), missing later accounts' transfers.

**Issues:**
- **Wrong result!** The `ORDER BY t.created_at DESC LIMIT 100` is not being honored globally. Wait — actually PostgreSQL *would* add a Sort node here. The plan I sketched above is incorrect for the actual planner behavior. Let me give the correct plan:

**Corrected plan (PostgreSQL would actually emit):**

```
 Limit  (cost=825.00..827.50 rows=100 width=80) (actual time=3.800..3.820 rows=100 loops=1)
   Buffers: shared hit=218 read=8
   -> Sort  (cost=825.00..825.50 rows=85 width=80) (actual time=3.780..3.800 rows=100 loops=1)
      Sort Key: t.created_at DESC
      Sort Method: top-N heapsort  Memory: 35kB
      Buffers: shared hit=218 read=8
      -> Nested Loop  ...  (same as above)
```

PostgreSQL inserts a Sort node with `top-N heapsort` (efficient for LIMIT). 3.8 ms total. Correct result.

**Why the planner is right here:**

- Outer is small (5 rows) → Nested Loop is appropriate.
- Inner has a useful index → each probe is O(log N).
- Innermost is the PK lookup → 1 row per probe.
- `top-N heapsort` is the optimal sort strategy for `ORDER BY ... LIMIT N`.

**This is a textbook optimal plan.** No fix needed.

**What could go wrong:**

If statistics are stale and `accounts_customer_id_idx` selectivity is wrong, the planner might think the customer has 5000 accounts (instead of 5) and pick a Hash Join instead. With 5 actual accounts, NLJ would have been faster. Solution: keep statistics fresh.

### Query 4: Daily balance aggregate

```sql
SELECT occurred_at::date AS day, SUM(amount) AS daily_total
FROM ledger_entries
WHERE account_id = 42
  AND occurred_at >= '2024-01-01'
GROUP BY occurred_at::date
ORDER BY day;
```

**Initial plan:**

```
 GroupAggregate  (cost=0.56..312.40 rows=30 width=16) (actual time=0.090..2.340 rows=30 loops=1)
   Group Key: ((occurred_at)::date)
   Buffers: shared hit=24 read=2
   -> Index Scan using ledger_entries_account_id_occurred_at_idx on ledger_entries
      (cost=0.56..312.00 rows=210 width=12) (actual time=0.030..1.500 rows=187 loops=1)
      Index Cond: ((account_id = 42) AND (occurred_at >= '2024-01-01'))
      Buffers: shared hit=24 read=2
 Planning Time: 0.180 ms
 Execution Time: 2.420 ms
```

**Why this plan:**

- Index scan produces rows in `occurred_at` order (the index's secondary sort key).
- `occurred_at::date` is monotonic in `occurred_at`, so rows are also sorted by `day`.
- Therefore `GroupAggregate` (which requires sorted input) can be used — no separate Sort node, no `HashAggregate`.
- Total: 2.4 ms. Excellent.

**This is the win from a well-designed composite index.** The index serves both the range filter *and* the GROUP BY ordering. Two queries for the price of one index.

**What if `account_id` is not in the predicate?**

```sql
-- Daily totals across ALL accounts (a report query)
SELECT occurred_at::date AS day, SUM(amount)
FROM ledger_entries
WHERE occurred_at >= '2024-01-01'
GROUP BY occurred_at::date;
```

Now the composite index is useless (leading column `account_id` not constrained). The planner picks:

```
 HashAggregate  (cost=1250000..1250030 rows=30 width=16) (actual time=18300..18320 rows=30 loops=1)
   Group Key: ((occurred_at)::date)
   Buffers: shared hit=12 read=152432
   -> Seq Scan on ledger_entries
      (cost=0..1200000 rows=10000000 width=12) (actual time=0.10..18000 rows=10000000 loops=1)
      Filter: (occurred_at >= '2024-01-01')
      Buffers: shared hit=12 read=152432
 Execution Time: 18320 ms
```

18 seconds — a full table scan. This is the right plan for a one-off report (an index won't help; we're summing 10M rows). The fix for repeated execution is a **materialized view**:

```sql
CREATE MATERIALIZED VIEW daily_totals AS
SELECT occurred_at::date AS day, SUM(amount) AS total
FROM ledger_entries
GROUP BY occurred_at::date;

CREATE UNIQUE INDEX daily_totals_day_idx ON daily_totals(day);

-- Refresh nightly
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_totals;
```

Now the report query is `SELECT * FROM daily_totals WHERE day >= '2024-01-01'` — milliseconds. The trade-off: the view is stale until refreshed. See [[07-Views-Materialized-Views]] and [[02-Denormalization-For-Reads]].

### Query 5: Fraud detection — the heavy scan

```sql
SELECT a.customer_id, SUM(t.amount) AS total_24h, COUNT(*) AS transfer_count
FROM transfers t
JOIN accounts a ON t.source_account_id = a.id
WHERE t.created_at >= now() - interval '24 hours'
  AND t.status = 'COMPLETED'
GROUP BY a.customer_id
HAVING SUM(t.amount) > 10000
ORDER BY total_24h DESC
LIMIT 100;
```

**Initial plan (assume stale statistics — `transfers.reltuples` says 100K, actually 500M):**

```
 Limit  (cost=1500..1502 rows=100 width=24) (actual time=248000..248020 rows=100 loops=1)
   Buffers: shared hit=12000 read=580000, temp read=420000 written=420000
   -> Sort  (cost=1500..1505 rows=10000 width=24) (actual time=248000..248020 rows=100 loops=1)
      Sort Key: (sum(t.amount)) DESC
      Sort Method: external merge  Disk: 240000kB
      Buffers: shared hit=12000 read=580000, temp read=420000 written=420000
      -> HashAggregate  (cost=1200..1300 rows=10000 width=24) (actual time=200000..230000 rows=40000 loops=1)
         Group Key: a.customer_id
         Buffers: shared hit=12000 read=580000, temp read=420000 written=420000
         -> Hash Join  (cost=10..1100 rows=50000 width=24) (actual time=20..180000 rows=2000000 loops=1)
            Hash Cond: (t.source_account_id = a.id)
            Buffers: shared read=580000
            -> Seq Scan on transfers t  (cost=0..1000 rows=10000 width=20) (actual time=0.01..120000 rows=2000000 loops=1)
               Filter: ((created_at >= ...) AND (status = 'COMPLETED'))
               Buffers: shared read=580000
            -> Hash  (cost=5..5 rows=10 width=12) (actual time=10..10 rows=10000000 loops=1)
               Buckets: 65536  Batches: 256  Memory Usage: 4000kB
               Buffers: shared hit=10
               -> Index Only Scan using accounts_pkey on accounts a  (...)
 Execution Time: 248020 ms
```

**Issues:**

1. **Stale statistics.** The planner thought `transfers` had 100K rows; it actually has 500M, with 2M matching the 24-hour filter. Every estimate is off by ~5000×.
2. **Hash Join with 256 batches.** The accounts hash table didn't fit in `work_mem` (4 MB default). Each batch spilled to disk.
3. **Sort with 240 MB external merge.** Sort also spilled — way beyond `work_mem`.
4. **Result: 248 seconds.** The query is supposed to take seconds.

**Fixes:**

1. **Refresh statistics:**
   ```sql
   ANALYZE transfers;
   ```
   Now the planner knows there are 500M rows. It will still Seq Scan (the right call for 2M matching rows), but its join and sort estimates will be accurate, leading to better memory allocation.

2. **Raise `work_mem` for this session:**
   ```sql
   SET work_mem = '256MB';
   ```
   Now the Hash Join fits in one batch, and the Sort fits in memory. No disk spills.

3. **Add a partial index on recent completed transfers:**
   ```sql
   CREATE INDEX transfers_recent_completed_idx
     ON transfers (source_account_id, created_at DESC)
     WHERE status = 'COMPLETED' AND created_at >= '2024-01-01';
   ```
   The partial index is small (only recent completed transfers) and the planner can use it to satisfy the filter cheaply. The `WHERE` clause in the index definition must match the query's predicate (or be implied by it).

4. **Consider partitioning `transfers` by month:**
   ```sql
   CREATE TABLE transfers (
     id BIGINT,
     ...
     created_at TIMESTAMPTZ NOT NULL DEFAULT now()
   ) PARTITION BY RANGE (created_at);

   CREATE TABLE transfers_2024_01 PARTITION OF transfers
     FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
   -- ... etc.
   ```
   Now `WHERE created_at >= now() - interval '24 hours'` only scans the current partition. The seq scan reads ~2M rows in the current partition instead of touching the indexes/visibility map of the whole 500M-row table. See [[04-Partitioning-And-Sharding]].

**Improved plan after fixes:**

```
 Limit  (cost=45000..45002 rows=100 width=24) (actual time=420..425 rows=100 loops=1)
   Buffers: shared hit=42000 read=8000
   -> Sort  (cost=45000..45050 rows=10000 width=24) (actual time=420..422 rows=100 loops=1)
      Sort Key: (sum(t.amount)) DESC
      Sort Method: top-N heapsort  Memory: 30kB
      Buffers: shared hit=42000 read=8000
      -> HashAggregate  (cost=44000..44500 rows=10000 width=24) (actual time=380..410 rows=8000 loops=1)
         Group Key: a.customer_id
         Buffers: shared hit=42000 read=8000
         -> Hash Join  (cost=10..42000 rows=200000 width=24) (actual time=0.50..350 rows=200000 loops=1)
            Hash Cond: (t.source_account_id = a.id)
            Buffers: shared hit=42000 read=8000
            -> Seq Scan on transfers_2024_08 t   ← only the current partition!
               Filter: ((created_at >= ...) AND (status = 'COMPLETED'))
               Buffers: shared read=8000
            -> Hash  (cost=5..5 rows=10000 width=12) (actual time=0.40..0.40 rows=10000 loops=1)
               Buckets: 16384  Batches: 1  Memory Usage: 600kB
               Buffers: shared hit=20
               -> Index Only Scan using accounts_pkey on accounts a
                  Buffers: shared hit=20
 Execution Time: 425 ms
```

**From 248 seconds to 425 ms** — a 580× speedup. The improvements:

- Statistics refresh → accurate estimates → correct memory allocation.
- `work_mem = 256MB` → no disk spills (sort and hash in memory).
- Partitioning → scan only the current month (~2M rows instead of touching all 500M).
- `top-N heapsort` (only top 100 needed, since LIMIT 100).

## What can go wrong (cross-cutting)

- **Treating `EXPLAIN` as the only tool.** Also monitor `pg_stat_statements` for actual query frequency and time. A query that runs 1000× per second at 5 ms each is a bigger problem than a query that runs once a day at 5 seconds.
- **Index churn.** Adding indexes to fix one query can slow down `INSERT`s/`UPDATE`s. Always measure write performance after adding indexes.
- **Over-tuning one query.** A perfectly-tuned fraud query may starve the OLTP transfer path of CPU. Tune the *workload*, not the query.
- **Query plan instability.** A query that was fast yesterday is slow today because autovacuum changed statistics. Use plan hints (cautiously) or pinned plans for critical queries. PostgreSQL 16+ adds `query_id` for tracking.
- **Parameter sniffing on the customer statement query.** A customer with 5 accounts gets a fast NLJ plan; a corporate customer with 5000 accounts gets the same plan and it's 1000× slower. Consider using `REPLAN` or custom plans.

## Trade-offs (cross-cutting)

- **Indexes for reads vs writes.** Every index you add to fix a query slows `INSERT`s. The Banking schema has 6 indexes on `transfers`; each transfer write updates 6 B-trees. Acceptable for OLTP volumes; problematic at high throughput.
- **Materialized views vs live queries.** The daily totals materialized view (Query 4) is fast to read but stale. The live query is fresh but slow. The choice depends on the report's freshness SLA.
- **Partitioning vs simplicity.** Partitioning transfers by month speeds up time-windowed scans but complicates `INSERT`s (routing), foreign keys (must reference the parent or specific partitions), and unique constraints (must include the partition key).
- **Statistics accuracy vs `ANALYZE` cost.** Higher `default_statistics_target` = more accurate = slower `ANALYZE`. Default 100 is a compromise; raise for skewed columns.
- **`work_mem` per query vs concurrency.** 256 MB `work_mem` per query × 100 concurrent queries = 25 GB. Don't set globally high; set per-session for known-heavy queries.

## Forward links

- [[00-Query-Optimization-Strategy]] — turning these fixes into a systematic process.
- [[01-Indexing-Strategy]] — when to add, drop, or rebuild indexes.
- [[02-Denormalization-For-Reads]] — materialized views and denormalization in depth.
- [[04-Partitioning-And-Sharding]] — the partitioning decision for `transfers` and `ledger_entries`.
- [[05-Banking-Performance-Tuning]] — the Banking case study's full performance chapter.
- Back to [[04-Banking-Schema]] — the schema we've been querying.
- Back to [[09-Banking-SQL]] — the SQL queries we've been analyzing.
- Back to [[00-Banking-Case-Study]] — the invariants that constrain these queries (e.g., the fraud query must respect the immutability of ledger entries).
- Back to [[08-Trade-offs-Everywhere]] — every plan choice above is a trade-off made visible.
