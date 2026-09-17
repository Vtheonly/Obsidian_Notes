# The Cost-Based Optimizer

> The cost-based optimizer (CBO) is the brain of the database. Given a query, it searches a space of equivalent execution plans, estimates the cost of each, and picks the cheapest. Get the CBO right, and queries are fast. Get it wrong — by feeding it stale statistics, or by structuring queries in ways that defeat estimation — and even simple queries become slow.

## What you already know

From [[06-Query-Processing-Pipeline]]: the planner translates a logical plan into a physical plan. From [[05-Join-Algorithms]]: there are usually several viable physical operators per logical operator. From [[08-Trade-offs-Everywhere]]: the CBO is making a trade-off — *plan time* (searching more plans) vs *execution time* (finding a better plan).

## Why this layer exists

A SQL query does not specify *how* to execute — only *what* to compute. For a 5-table join, there are 5! = 120 join orders, and for each join there are 3 algorithms, so 120 × 3^4 = 9,720 plans to consider (the last join doesn't vary, simplifying slightly). For each plan, the optimizer must estimate the cost without running it.

Without a CBO, the database would pick plans heuristically ("always use an index when available") — which is wrong surprisingly often. A full scan can be faster than an index scan when the index matches most of the table. A hash join can be faster than a nested loop even with an index, if the outer table is large. The CBO exists to make these calls correctly, by estimating costs numerically.

## What is genuinely new here

Three things:

1. **Statistics** — what the planner knows about your data (`pg_class`, `pg_statistic`, MCV lists, histograms, correlation).
2. **The cost model** — the numbers (`seq_page_cost`, `random_page_cost`, `cpu_tuple_cost`, etc.) that translate estimates into a single comparable cost.
3. **Selectivity estimation** — how the planner turns `WHERE col = $1` into a row-count estimate.

## Concepts

### Statistics

The planner maintains statistics about every table:

- **`pg_class.reltuples`** — estimated row count.
- **`pg_class.relpages`** — page count (size in 8 KB pages).
- **`pg_statistic`** (exposed via `pg_stats` view) — per-column statistics:
  - `null_frac` — fraction of NULLs.
  - `n_distinct` — number of distinct values (negative means fraction of rows).
  - `most_common_vals` (MCV) — most frequent values, with their frequencies.
  - `histogram_bounds` — histogram of value distribution (excluding MCVs).
  - `correlation` — physical clustering of the column. 1.0 means perfectly ascending with physical order; -1.0 means descending. Affects index scan cost (high correlation = sequential page reads = cheap).

The planner runs `ANALYZE` (or autovacuum does it automatically) to refresh these. Statistics are *samples* — by default 30,000 rows — not full scans. For very large or skewed tables, increase `default_statistics_target` (default 100, max 10,000).

```sql
-- View column statistics
SELECT * FROM pg_stats WHERE tablename = 'accounts' AND attname = 'current_balance';
-- schemaname | tablename | attname          | inherited | null_frac | n_distinct | ...
-- public     | accounts  | current_balance  | f         | 0.00      | -0.95      | ...
```

A negative `n_distinct` means "fraction of rows" — `-0.95` means "95% of rows have distinct values" (i.e., near-unique). A positive `n_distinct` is an absolute count.

### The cost model

The planner computes a cost number for each plan. The cost is unitless — it's only meaningful relative to other plans. The components:

| Parameter | Default | Meaning |
|---|---|---|
| `seq_page_cost` | 1.0 | Cost of a sequential page read. The baseline unit. |
| `random_page_cost` | 4.0 | Cost of a random page read. 4× sequential on HDD; closer to 1.1-2.0 on NVMe. |
| `cpu_tuple_cost` | 0.01 | Cost of processing one tuple (CPU). |
| `cpu_index_tuple_cost` | 0.005 | Cost of processing one index entry. |
| `cpu_operator_cost` | 0.0025 | Cost of evaluating an operator (=, >, +, etc.). |
| `parallel_setup_cost` | 1000 | Cost of starting a parallel worker. |
| `parallel_tuple_cost` | 0.1 | Cost of transferring a tuple between workers. |

A plan's total cost is the sum of (page reads × page cost) + (tuples × cpu_tuple_cost) + (operators × cpu_operator_cost) + ...

The numbers in `EXPLAIN` look like `cost=0.00..8.02`:
- The first number (0.00) is **startup cost** — how much work before the first tuple is produced. A Seq Scan has startup cost 0. A Sort has startup cost = full sort cost (no tuples until sorting is done).
- The second number (8.02) is **total cost** — work to produce all tuples.

The planner minimizes total cost for non-`LIMIT` queries, and a combination of startup + total for `LIMIT` queries (because early termination matters).

### Selectivity estimation

For each predicate, the planner estimates *selectivity* — the fraction of rows that match.

| Predicate | Selectivity estimate |
|---|---|
| `col = $1` (no stats) | 1 / `n_distinct` |
| `col = $1` (in MCV list) | MCV frequency for that value |
| `col = $1` (not in MCV, has histogram) | even split of non-MCV rows |
| `col IS NULL` | `null_frac` |
| `col > $1` | histogram lookup |
| `col BETWEEN $1 AND $2` | histogram range |
| `col LIKE 'abc%'` | histogram-based, with heuristic |
| `col1 = $1 AND col2 = $2` | `sel(col1) × sel(col2)` (assumes independence) |
| `col1 = $1 OR col2 = $2` | `sel(col1) + sel(col2) - sel(col1)×sel(col2)` |
| `NOT p` | `1 - sel(p)` |

The independence assumption (AND = multiply selectivities) is the CBO's biggest weakness. Real columns are correlated: `zip_code` and `state` are not independent; `country` and `currency` are not independent. The planner assumes they are, and underestimates selectivity.

PostgreSQL has **extended statistics** (multivariate) to address this:

```sql
CREATE STATISTICS accounts_country_currency_stats (dependencies)
  ON country, currency FROM accounts;
ANALYZE accounts;
```

Now the planner knows `country` and `currency` are correlated and estimates `WHERE country = 'US' AND currency = 'USD'` correctly.

### Join order search

For an N-table join, the planner searches join orders. The naive search is `O(N!)`. PostgreSQL uses **dynamic programming** (System R algorithm):

- For 1 table: cost = scan cost.
- For 2 tables: cost = best(1 table) + join cost with the other.
- For 3 tables: cost = best(2 tables) + join cost with the third, considering all pairs.
- ...

The DP explores `O(3^N)` plans — much better than `N!`. Up to ~12 tables, this is feasible.

For ≥ 12 tables (default `geqo_threshold`), PostgreSQL switches to **GEQO** (Genetic Query Optimization) — a genetic algorithm that explores a sample of plans. GEQO is faster but may not find the optimal plan. For most queries this is fine; for complex analytical queries on 15+ tables, it can occasionally pick a bad plan.

### Why the planner can be wrong

1. **Stale statistics.** `ANALYZE` hasn't run since a bulk load. `reltuples` says 10K rows; actual is 10M. The planner underestimates every join.
2. **Skewed distributions not captured.** MCV lists store the top ~100 values. A long-tail distribution can have heavy frequencies below the cutoff.
3. **Correlated columns.** The independence assumption underestimates. (Fix with extended stats.)
4. **Parameterized queries with skewed parameter values.** A query `WHERE status = $1` may be highly selective for `status = 'CLOSED'` (rare) but unselective for `status = 'ACTIVE'` (common). Generic plans assume average; custom plans use the actual value. PostgreSQL's plan caching may pick the wrong one.
5. **Functions in predicates.** `WHERE lower(email) = $1` — the planner cannot estimate this without a statistics object on the expression. Use expression indexes with `ANALYZE` on the expression.
6. **Cross-column dependencies.** Even with multivariate stats, 3+ columns are hard.
7. **Data outside the planner's model.** Triggers, foreign keys with cascade, rules — these add hidden costs the planner doesn't account for.

## Banking application

Consider this query — a transfer summary:

```sql
SELECT t.id, t.amount, sa.iban AS source, da.iban AS dest
FROM transfers t
JOIN accounts sa ON t.source_account_id = sa.id
JOIN accounts da ON t.dest_account_id = da.id
WHERE sa.customer_id = $1
  AND t.created_at >= now() - interval '30 days';
```

The planner's options:

1. **Start from `transfers`.** Scan recent transfers (~5M rows), hash-join to accounts twice. Cost: high (5M × 2 hash builds).
2. **Start from `accounts` (for the customer).** Index lookup → 5 accounts. Then nested-loop into `transfers(source_account_id, created_at)` for each. Cost: 5 × O(log 5M) ≈ 20 page reads.

If statistics are fresh, the planner picks option 2. But:

- If `pg_class.reltuples` for `transfers` is stale (says 100K, actually 5M), the planner may think option 1 is cheaper — underestimating the scan.
- If `accounts.customer_id` statistics say `n_distinct = 10000` (so 1/10000 selectivity), but actually the table has 10M customers (1/10M selectivity), the planner will overestimate the number of accounts returned and may pick a different plan.
- If the customer has 1 account vs 10,000 accounts, the optimal plan differs. A generic plan picks one and may be wrong for both extremes.

The fix:

```sql
-- Refresh statistics after bulk loads
ANALYZE transfers;
ANALYZE accounts;

-- Add extended stats for correlated columns
CREATE STATISTICS accounts_customer_country_stats (dependencies)
  ON customer_id, country FROM accounts;
ANALYZE accounts;

-- Use bind variables with the right type (avoid implicit coercion)
PREPARE transfer_summary(bigint) AS
  SELECT ... WHERE sa.customer_id = $1;
EXECUTE transfer_summary(42);
```

## Code / diagrams

Inspect the planner's estimates:

```sql
-- What does the planner think the table looks like?
SELECT relname, reltuples, relpages FROM pg_class WHERE relname = 'transfers';
--  relname  │ reltuples  │ relpages
-- ──────────┼────────────┼──────────
--  transfers │ 5234188.0  │ 65477

-- What does it know about column 'status'?
SELECT * FROM pg_stats WHERE tablename = 'transfers' AND attname = 'status';
-- schemaname | tablename | attname | null_frac | n_distinct | most_common_vals     | most_common_freqs
-- public     | transfers | status  | 0.00       | 5          | {PENDING,COMPLETED}  | {0.30,0.65,...}

-- See the plan and its estimates
EXPLAIN SELECT * FROM transfers WHERE status = 'PENDING';
-- Seq Scan on transfers
--   Filter: (status = 'PENDING'::text)
--   Rows: 1570257  (estimated 30% × 5.23M rows)

-- Compare to actual
EXPLAIN (ANALYZE) SELECT * FROM transfers WHERE status = 'PENDING';
-- Seq Scan on transfers
--   Filter: (status = 'PENDING'::text)
--   Rows: 1570257  (estimated)  ... actual=1570193  ... Execution Time: 234 ms
```

When estimated and actual row counts differ by more than ~10×, the planner's cost model is being misled. Investigate.

### Cost computation example

For `Seq Scan on transfers`:

```
cost = relpages × seq_page_cost + reltuples × cpu_tuple_cost
     = 65477 × 1.0 + 5234188 × 0.01
     = 65477 + 52341
     = 117818
```

For an `Index Scan` on a 4-row result:

```
cost = 4 × random_page_cost + 4 × cpu_index_tuple_cost + 4 × cpu_operator_cost
     = 4 × 4.0 + 4 × 0.005 + 4 × 0.0025
     ≈ 16.03
```

The index scan wins by a factor of 7000. The planner picks it.

### The cost of a wrong choice

```sql
EXPLAIN (ANALYZE) SELECT * FROM transfers WHERE status = 'COMPLETED';
-- (estimated 65% = 3.4M rows)
-- Seq Scan on transfers
--   Filter: (status = 'COMPLETED'::text)
--   Rows: 3402242  (estimated)  ... actual=3402218
-- Execution Time: 412 ms

-- But what if stats were stale and said only 1% = 50K rows?
-- (hypothetical) The planner might pick:
-- Bitmap Heap Scan on transfers
--   Recheck Cond: (status = 'COMPLETED'::text)
--   -> Bitmap Index Scan on transfers_status_idx
-- Rows: 50000  (estimated)  ... actual=3402218
-- Execution Time: 28 seconds   ← bitmap explodes
```

A 70× slowdown from one stale statistic. This is why `ANALYZE` matters.

## What can go wrong

- **Stale statistics.** The #1 cause of bad plans. Mitigation: tune autovacuum to analyze more aggressively on high-churn tables.
- **Wrong `random_page_cost` on SSD.** Default 4.0 is HDD-era. On NVMe, set to 1.1-2.0. Otherwise the planner over-prefers seq scans.
- **Wrong `effective_cache_size`.** If set too low, the planner assumes the index won't be cached and prefers seq scans. Set to ~75% of RAM.
- **Parameter sniffing.** A prepared statement gets a plan based on the first parameter values. Later calls with different values get a suboptimal plan. PostgreSQL mitigates with custom plans, but it's not perfect.
- **Correlated columns.** Default stats assume independence. Use extended stats.
- **Functions in predicates.** Without expression statistics, the planner guesses.
- **Data skew.** A few "heavy" customers can break generic plans.
- **`LIMIT` interactions.** The planner may pick a plan optimized for `LIMIT 10` that is terrible for `LIMIT 100000`. Use `FETCH FIRST n ROWS ONLY` deliberately.
- **Outer join reordering.** Semantic constraints prevent some reorderings, occasionally forcing a suboptimal plan.

## Trade-offs

- **Plan time vs plan quality.** Searching more plans = better plan but slower parse. DP up to 12 tables; GEQO above.
- **Statistics sample size vs accuracy.** Larger sample = more accurate stats but slower `ANALYZE`. Default 30K rows is a compromise; raise for skewed columns.
- **Generic vs custom plans.** Generic = fast prepare, possibly wrong plan. Custom = slow prepare, right plan. PostgreSQL adapts.
- **Cost model simplicity vs accuracy.** The default cost model is simple (one `random_page_cost` for all pages). Reality is more complex (cached pages vs cold pages have different costs). Some databases track this; PostgreSQL mostly doesn't.
- **Heuristic vs cost-based.** Some decisions (like join reordering for outer joins) are heuristic; the CBO doesn't fully explore them.

## Forward links

- [[08-Reading-EXPLAIN]] — see the CBO's output.
- [[09-Banking-Query-Plans]] — real plans, real misestimates, real fixes.
- [[00-Query-Optimization-Strategy]] — when to fight the CBO and when to help it.
- [[01-Indexing-Strategy]] — the CBO uses indexes; bad indexes waste its time.
- Back to [[04-Abstraction-and-Models]] — the cost model is itself an abstraction over reality; it leaks.
- Back to [[08-Trade-offs-Everywhere]] — every tuning knob is a trade-off.
