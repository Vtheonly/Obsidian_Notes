# Join Algorithms

> A `JOIN` in SQL is a declarative statement of *what* data you want. The join *algorithm* is the imperative *how*. PostgreSQL has three classic join algorithms — Nested Loop, Hash Join, and Merge Join — and the optimizer picks one per join in the plan. Knowing the algorithms and their selection rules is the difference between a query that finishes in 5 ms and one that finishes in 5 hours.

## What you already know

From [[04-Relational-Algebra]]: a join is a Cartesian product filtered by a predicate, possibly projected. From [[03-B-Tree-Indexes]]: point lookups are `O(log N)`. From [[08-Trade-offs-Everywhere]]: every algorithm trades something — memory vs CPU vs disk, build-time vs probe-time.

## Why this layer exists

A naive join of two tables — Cartesian product — is `O(N × M)`. For two 1-million-row tables, that is 10^12 comparisons. Unusable. Join algorithms exist to avoid the Cartesian product when the join predicate allows it. The three classic algorithms each exploit a different structure of the predicate or the data:

- **Nested Loop** exploits an index on the inner side.
- **Hash Join** exploits the ability to bucket both sides by a hash.
- **Merge Join** exploits both sides being sorted on the join key.

## What is genuinely new here

The **build side / probe side** distinction — every join algorithm has an asymmetric flow. The planner chooses which side is which. And the **cost formulas** that decide which algorithm wins for given table sizes.

## Concepts

### Nested Loop Join (NLJ)

The simplest possible join. For each row of the outer table, scan the inner table for matches.

```
function nested_loop_join(outer, inner, predicate):
    for o in outer:
        for i in inner:
            if predicate(o, i):
                emit(o, i)
```

Naive cost: `O(N × M)` where N and M are the row counts.

But the inner scan is usually *not* a full scan — it is an *index lookup*. If the inner table has an index on the join key, each inner "scan" becomes `O(log M)`:

```
function nested_loop_with_index(outer, inner, predicate):
    for o in outer:
        for i in inner.index_lookup(predicate.key(o)):    # O(log M)
            emit(o, i)
```

Cost: `O(N log M)`. For N = 1M, M = 1M with index, that is 1M × ~20 comparisons ≈ 20M — feasible.

When the planner picks NLJ:

- Outer is small (a few rows to a few thousand).
- Inner has a useful index on the join key.
- The join is an inequality (`>`, `<`) — only NLJ supports these.

PostgreSQL's NLJ also supports *inner unique* optimization: if the inner side is known unique (e.g., a primary key), NLJ stops at the first match per outer row.

### Hash Join

Build a hash table on the *smaller* side (the "build side"), then probe it with each row of the *larger* side (the "probe side").

```
function hash_join(build, probe, key):
    H = new hash table
    for b in build:
        H.insert(key(b), b)
    for p in probe:
        for b in H.find(key(p)):
            emit(p, b)
```

Cost: `O(N + M)` plus the cost of building/probing the hash table. This is asymptotically optimal — you cannot beat `O(N + M)` for joining two unsorted sets.

Memory: the hash table holds the entire build side. PostgreSQL limits this to `work_mem` (default 4 MB). If the build side is larger, PostgreSQL splits it into *batches* — each batch's hash table fits in `work_mem`, and the probe side is also partitioned into matching batches. Each batch is processed separately, with overflow batches spilled to disk.

When the planner picks Hash Join:

- Both sides are large.
- No useful index on the join key (or index lookups would be slower than a single hash pass).
- The join is an equality (`=`).
- `work_mem` can hold the build side (or batches are acceptable).

Hash join is the workhorse for analytical queries — large unsorted inputs joined on equality. PostgreSQL uses it heavily.

### Merge Join

Sort both sides on the join key, then walk both sorted streams in parallel.

```
function merge_join(left, right, key):
    sort(left, by=key)
    sort(right, by=key)
    l = left.first()
    r = right.first()
    while l and r:
        if key(l) == key(r):
            # Handle duplicates: emit all matches, advance the side that runs out
            emit_all_matches(l, r)
            advance appropriately
        elif key(l) < key(r):
            l = left.next()
        else:
            r = right.next()
```

Cost: `O(N log N + M log M)` for the sorts, plus `O(N + M)` for the merge itself.

When the planner picks Merge Join:

- Both sides are *already sorted* — typically because both have indexes on the join key, or because a previous Sort node in the plan already sorted them.
- The join is an equality (or a range; merge join supports range predicates too, with extra logic).
- Memory pressure: merge join needs only one row of each side in memory at a time (plus sort buffers if sorting is needed).

If the inputs are already sorted, merge join is `O(N + M)` — even better than hash join, because no hash table is built. If the inputs are not sorted, the sort cost can dominate. The planner makes this trade-off.

### How the optimizer chooses

The cost-based optimizer (see [[07-Cost-Based-Optimizer]]) estimates the cost of each viable join algorithm and picks the cheapest. The estimates depend on:

- Estimated row counts (from `pg_class.reltuples` and `pg_statistic`).
- Whether useful indexes exist on the join keys.
- Available memory (`work_mem`).
- Whether the data is already sorted (from a previous Sort node or an index scan).
- Whether the join is equality or inequality.

A typical decision tree:

| Outer size | Inner size | Inner index on key? | Join type | Likely choice |
|---|---|---|---|---|
| Tiny (10) | Large (10M) | Yes | Equality | Nested Loop (with index probe) |
| Tiny (10) | Large (10M) | No | Equality | Hash Join (build on the tiny side) |
| Large (1M) | Large (1M) | Yes (both) | Equality | Merge Join (both sides sorted by index) |
| Large (1M) | Large (1M) | No | Equality | Hash Join (build on smaller, batch if needed) |
| Any | Any | Any | Inequality (`>`) | Nested Loop (only option) |
| Large | Large | Sorted by previous op | Equality | Merge Join |

### Outer joins

For `LEFT`, `RIGHT`, and `FULL` joins, the algorithms must emit unmatched rows from the preserved side(s) with NULLs on the other. All three algorithms can do this, but with different costs:

- NLJ: easy — emit NULL-extended outer row when no inner match found.
- Hash Join: the build side must be the *non-preserved* side (so the probe side is the preserved side). PostgreSQL enforces this.
- Merge Join: easy — emit unmatched rows during the merge.

### Join reorder

For a 3-table join `A JOIN B JOIN C`, the join order matters: `(A JOIN B) JOIN C` may be much cheaper than `A JOIN (B JOIN C)`. The optimizer searches join orders using dynamic programming (up to ~12 tables; above that, GEQO heuristic kicks in — see [[07-Cost-Based-Optimizer]]).

The choice of join algorithm interacts with join order. The optimizer considers both simultaneously: for each pair (order, algorithm), estimate cost, pick the best.

## Banking application

The Banking system has many joins. Three representative queries:

### Query 1: customer statement — `transfers` joined to `accounts`

```sql
SELECT t.*, a.iban
FROM transfers t
JOIN accounts a ON t.source_account_id = a.id
WHERE a.customer_id = $1
  AND t.created_at >= now() - interval '30 days';
```

Sizes (estimated):

- `accounts` for this customer: ~5 rows.
- `transfers` in last 30 days: ~5M rows (across all customers).

The planner will:

1. Use the index on `accounts(customer_id)` to fetch the 5 accounts.
2. Use those 5 account IDs to probe `transfers(source_account_id, created_at)`.

Plan: **Nested Loop** with index probe on the inner. Outer = 5 rows, inner = 5M rows but indexed on the join key. Each probe is `O(log 5M)` ≈ 4 page reads. Total: ~20 page reads.

### Query 2: monthly aggregate — all transfers joined to all accounts

```sql
SELECT a.customer_id, SUM(t.amount)
FROM transfers t
JOIN accounts a ON t.source_account_id = a.id
WHERE t.created_at >= '2024-01-01' AND t.created_at < '2024-02-01'
GROUP BY a.customer_id;
```

Sizes:

- `transfers` in January: ~1M rows.
- `accounts`: ~10M rows, but only ~50K distinct accounts touched by those transfers.

The planner will:

1. Scan `transfers` for January (using a partial or range index, ~1M rows).
2. Hash-join against `accounts` — build hash on the smaller side (the 1M `transfers`, hashed by `source_account_id`), probe with `accounts`. Or vice versa.

Plan: **Hash Join** — `O(N + M)` with one hash pass. The hash table fits in `work_mem` (~256 MB) for 1M rows.

### Query 3: reconcile ledger entries — both sides sorted

```sql
SELECT le.account_id, le.amount, t.id AS transfer_id
FROM ledger_entries le
JOIN transfers t ON le.transfer_id = t.id
WHERE le.occurred_at >= '2024-01-01'
ORDER BY le.account_id, le.occurred_at;
```

If both `ledger_entries(transfer_id)` and `transfers(id)` (the PK) are B-tree indexes, the planner can read both sides in sorted order on `transfer_id`. Plan: **Merge Join**, no explicit sort.

If `ledger_entries(transfer_id)` has no index, the planner might still pick merge join but add a Sort node — costing `O(N log N)` for the sort. Hash join might then be cheaper. The planner decides based on statistics.

## Code / diagrams

```sql
-- Force the planner to show all three algorithms on the same join:

-- Nested Loop (with index)
SET enable_hashjoin = off;
SET enable_mergejoin = off;
EXPLAIN SELECT * FROM accounts a JOIN transfers t ON a.id = t.source_account_id
  WHERE a.iban = 'GB29NWBK60161331926819';
-- Nested Loop
--   -> Index Scan using accounts_iban_idx on accounts a
--   -> Index Scan using transfers_source_account_id_idx on transfers t

-- Hash Join
SET enable_hashjoin = on;
SET enable_mergejoin = off;
SET enable_nestloop = off;
EXPLAIN SELECT * FROM accounts a JOIN transfers t ON a.id = t.source_account_id;
-- Hash Join
--   Hash Cond: (a.id = t.source_account_id)
--   -> Seq Scan on accounts a
--   -> Hash
--       -> Seq Scan on transfers t

-- Merge Join (both sides need to be sorted; indexes provide that)
SET enable_mergejoin = on;
SET enable_hashjoin = off;
SET enable_nestloop = off;
EXPLAIN SELECT * FROM accounts a JOIN transfers t ON a.id = t.source_account_id;
-- Merge Join
--   Merge Cond: (a.id = t.source_account_id)
--   -> Index Scan using accounts_pkey on accounts a
--   -> Index Scan using transfers_source_account_id_idx on transfers t
```

The `enable_*` flags are for debugging only — never set them in production. They let you see what the planner *would* pick under different choices, useful for understanding plan selection.

## What can go wrong

- **Stale statistics → wrong algorithm.** If `pg_class.reltuples` says `transfers` has 10K rows but it actually has 10M, the planner may pick NLJ when Hash Join would be 100× faster. Symptom: query that was fast last week is slow today after a bulk load.
- **Hash join batch spills.** When the build side exceeds `work_mem`, batches spill to disk. Each spill adds disk I/O. Mitigation: raise `work_mem` for the session, or partition the query.
- **Bad join order.** Even with the right algorithm, joining the wrong tables first can explode intermediate result size. The optimizer usually catches this, but complex queries (10+ tables) may defeat dynamic programming.
- **Parameterized nested loops.** A query like `WHERE a.x = $1` may estimate well, but a query like `WHERE a.x IN (SELECT ...)` may not. The inner NLJ runs once per outer row, and if the outer row count is mis-estimated, the total cost is wildly off.
- **Cross joins (Cartesian products).** A missing join condition produces `O(N × M)` regardless of algorithm. The planner will warn (huge estimated row count) but the query will still run.
- **Outer join reordering constraints.** The planner cannot freely reorder outer joins — the semantics fix the join order in some cases. This can force a suboptimal plan.

## Trade-offs

- **Memory vs CPU.** Hash Join uses memory to save CPU. NLJ uses CPU (no hash table) but no extra memory. Merge Join uses memory for sort buffers.
- **Build vs probe.** Hash Join pays the build cost up front; NLJ pays per probe. For small outer tables, NLJ avoids the build cost entirely.
- **Sorted vs hashed.** Merge Join exploits sorted inputs; Hash Join exploits hashable keys. If inputs are already sorted, Merge Join wins. If not, the sort cost may exceed the hash cost.
- **Generality vs efficiency.** NLJ supports any predicate (equality, inequality, complex expressions). Hash Join and Merge Join support only equality (merge join also some inequalities). NLJ is the fallback for unusual predicates.
- **Work_mem vs concurrency.** Higher `work_mem` lets each query build bigger hash tables but reduces the number of concurrent queries the server can run. Trade per-query speed for throughput.

## Forward links

- [[06-Query-Processing-Pipeline]] — joins are operators in the volcano executor.
- [[07-Cost-Based-Optimizer]] — how the planner estimates each join's cost.
- [[08-Reading-EXPLAIN]] — `Hash Join`, `Nested Loop`, `Merge Join` are common nodes.
- [[09-Banking-Query-Plans]] — five real join plans analyzed.
- [[00-Query-Optimization-Strategy]] — tuning join performance.
- Back to [[03-Select-Join-Group]] — SQL syntax of joins.
- Back to [[04-Relational-Algebra]] — the formal foundation (θ-join, natural join, semijoin).
