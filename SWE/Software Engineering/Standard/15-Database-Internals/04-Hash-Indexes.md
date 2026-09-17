# Hash Indexes

> Hash indexes offer `O(1)` point lookups — but only for equality predicates. They are a useful tool in a narrow niche, and PostgreSQL's history with them is a useful lesson in why "theoretically faster" rarely beats "generally good enough."

## What you already know

From [[03-B-Tree-Indexes]]: B-trees give `O(log N)` lookups and support range queries, ordering, and uniqueness. They are the default index type in PostgreSQL and the right choice 95% of the time. From [[08-Trade-offs-Everywhere]]: every optimization trades something. The hash index's trade is: *faster lookup, narrower query support*.

## Why this layer exists

A B-tree lookup is `O(log N)` — for 10M rows, that is ~3-4 page reads. Each page read is a cache lookup (hopefully a hit). What if we could do it in 1 page read? A hash index can.

The hash index trades the *generality* of B-trees (ranges, ordering, prefix matches, `LIKE`) for the *speed* of direct bucket access. It supports *only* equality: `WHERE col = $1`. Nothing else.

The legitimate niche: a column where you do millions of pure equality lookups and never need anything else — idempotency keys, session tokens, deduplication keys. In those cases, a hash index is marginally faster than a B-tree and noticeably smaller.

## What is genuinely new here

Two things:

1. The **hash collision strategy** — buckets with overflow pages, and how that affects the `O(1)` claim.
2. The **historical lesson** — hash indexes were unsafe before PostgreSQL 10 (not WAL-logged, lost on crash). The history is a teaching moment about durability and the cost of "fast."

## Concepts

### Hash index structure

A hash index has three kinds of pages:

```
┌─────────────────────┐
│   Meta page (page 0)│
│   - bucket count    │
│   - split pointer   │
│   - hash function   │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────────────────────────────┐
│   Bucket directory (in meta page or         │
│   overflow into dedicated "bucket" pages)   │
├──────┬──────┬──────┬──────┬──────┬─────────┤
│  B0  │  B1  │  B2  │  B3  │  B4  │  ...    │
└──┬───┴──┬───┴──┬───┴──┬───┴──┬───┴─────────┘
   │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼
[Leaf]  [Leaf]  [Leaf]  [Leaf]  [Leaf]
  │              │
  ▼              ▼
[Overflow]    [Overflow]
  │              │
  ▼              ▼
[Overflow]
```

1. **Meta page** — bookkeeping: bucket count, split pointer, hash function OID.
2. **Bucket pages** — primary pages for each bucket. A bucket holds all keys whose `hash(key) mod N` equals the bucket index.
3. **Overflow pages** — when a bucket's primary page fills, additional pages are chained. Collisions create chains.

### Lookup

```
function hash_lookup(key):
    h = hash_function(key)
    bucket = h mod N          # N = current bucket count
    page = read_page(bucket)
    for entry in page.entries:
        if entry.key == key:   # real equality check, not just hash
            return entry.ctid
    while page.overflow:
        page = read_page(page.overflow)
        for entry in page.entries:
            if entry.key == key:
                return entry.ctid
    return not_found
```

One bucket page read (plus possibly overflow pages). If the hash function is good and the table is not overloaded, average lookup is `O(1)` page reads. Worst case (bad hash, all keys collide) is `O(N)` — but a decent hash function makes this astronomically unlikely.

### Linear hashing — growth strategy

PostgreSQL uses **linear hashing** to grow the index incrementally:

- The bucket count `N` doubles in batches as the index grows.
- A "split pointer" tracks which bucket to split next.
- Splits happen one bucket at a time, distributing load gradually.

This avoids the "rehash the whole table" cost of naive hash table growth. The trade-off is that some buckets belong to "the old world" (smaller N) and some to "the new world" (larger N), so lookups must check which side of the split pointer their bucket is on. This is internal bookkeeping, but it is why hash indexes are not *strictly* `O(1)` in space terms.

### What hash indexes do NOT support

- `WHERE col > 5` — range, no.
- `WHERE col BETWEEN 1 AND 10` — range, no.
- `ORDER BY col` — no ordering.
- `WHERE col LIKE 'abc%'` — prefix, no.
- `WHERE col IS NULL` — actually yes, hash indexes do index NULLs (since PG 10).
- Unique constraint — yes, since PG 10, hash indexes can enforce uniqueness.

If your query has *any* comparison other than `=`, the hash index is useless. The planner will fall back to a seq scan.

### The historical lesson: pre-PG-10 hash indexes

Before PostgreSQL 10, hash indexes were:

- **Not WAL-logged.** Crash recovery did not replay hash index changes. After a crash, the index could be corrupt.
- **Not replicated.** Streaming replication only ships WAL records; without WAL logging, replicas had no hash index updates.
- **Marked as "not recommended for production use"** in the documentation.

PostgreSQL 10 (2017) rewrote hash indexes to be fully WAL-logged, crash-safe, and replicable. They are now production-quality — but the reputation lingers, and adoption remains low. The lesson: *durability and replication are not optional features*. An index that is faster but cannot survive a crash is not faster; it is broken.

## Banking application

The Banking system has a few columns that are *pure* equality lookups:

- `transfers.idempotency_key` — every retry looks up `WHERE idempotency_key = $1`. Never range-scanned.
- `sessions.token` — every API request looks up `WHERE token = $1`. Never range-scanned.
- `webhooks.delivery_id` — deduplication of incoming webhook deliveries.

Each is a candidate for a hash index. In practice, however, **a B-tree is usually chosen anyway**, for two reasons:

1. **Flexibility.** Today you query by equality. Tomorrow you need `ORDER BY created_at DESC` for the same column, or a `LIKE` for partial matches. A B-tree supports all of them. A hash index does not.
2. **Maturity.** B-trees are the most-tested, most-optimized index type. Hash indexes work, but they receive less attention. The performance gap is small.

A real-world case where a hash index is clearly the right call: a 500M-row `audit_log` table with an `event_uuid` column that is only ever queried as `WHERE event_uuid = $1`. The B-tree on `event_uuid` is 30 GB; the hash index is 8 GB. Both lookups are 1-2 µs. The hash index saves 22 GB of RAM for the same speed.

For the Banking case study, we'll prefer B-trees. The marginal speed of a hash index is rarely worth giving up range queries. We mention hash indexes here because they are *conceptually* important: they illustrate the equality/range trade-off, and they show how `O(1)` is not always better than `O(log N)` when N is small and log N is essentially constant.

## Code / diagrams

```sql
-- Create a hash index
CREATE INDEX transfers_idempotency_hash_idx
  ON transfers USING hash (idempotency_key);

-- Hash indexes support equality only:
EXPLAIN SELECT * FROM transfers WHERE idempotency_key = 'abc-123';
-- Index Scan using transfers_idempotency_hash_idx on transfers
--   Index Cond: (idempotency_key = 'abc-123'::text)

-- But not range:
EXPLAIN SELECT * FROM transfers WHERE idempotency_key > 'abc';
-- Seq Scan on transfers   ← planner ignores the hash index
--   Filter: (idempotency_key > 'abc'::text)

-- Inspect bucket layout
CREATE EXTENSION pageinspect;
SELECT * FROM hash_metap('transfers_idempotency_hash_idx');
--  magic  │ version │ nbuckets │ bucketsize │ ...
-- --------+---------+----------+------------+-----
--  654378 │       4 │   16384  │    8192    │ ...

SELECT hash_page_type(get_raw_page('transfers_idempotency_hash_idx', 0));
--  bucket
```

The `nbuckets` value tells you how many primary bucket pages the index has. As the table grows, splits increase `nbuckets` gradually.

### Hash vs B-tree size comparison

```sql
CREATE TABLE demo AS SELECT g::bigint AS id, md5(g::text) AS k
  FROM generate_series(1, 10000000) g;

CREATE INDEX demo_btree ON demo (k);
CREATE INDEX demo_hash  ON demo USING hash (k);

SELECT pg_size_pretty(pg_relation_size('demo_btree')) AS btree_size,
       pg_size_pretty(pg_relation_size('demo_hash'))  AS hash_size;
--  btree_size │ hash_size
-- ────────────┼──────────
--  678 MB     │ 384 MB
```

The hash index is roughly 60% the size of the B-tree (no internal routing nodes, no high keys). Both lookups are sub-millisecond.

### Lookup performance

```sql
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM demo WHERE k = 'b9f1c0f4d8e2a7b6c1d3e5f8a9b0c2d4';
-- Index Scan using demo_hash on demo
--   Index Cond: (k = 'b9f1c0f4d8e2a7b6c1d3e5f8a9b0c2d4'::text)
--   Buffers: shared hit=2
--   Execution Time: 0.06 ms

EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM demo WHERE k = 'b9f1c0f4d8e2a7b6c1d3e5f8a9b0c2d4';
-- (with the btree index instead)
-- Index Scan using demo_btree on demo
--   Index Cond: (k = 'b9f1c0f4d8e2a7b6c1d3e5f8a9b0c2d4'::text)
--   Buffers: shared hit=4
--   Execution Time: 0.08 ms
```

Hash index: 2 page reads (bucket + maybe overflow). B-tree: 4 page reads (3 internal + 1 leaf). Both fit in `shared_buffers` and execute in under 100 µs. The gap is real but tiny.

## What can go wrong

- **Bad hash function.** If your DB's hash function clusters certain values, buckets become uneven. PostgreSQL uses a well-tested internal hash (murmur-style), so this is rarely an issue for built-in types. For custom types, you must define a good `HASH` operator class.
- **Skewed key distribution.** Even with a good hash function, if 80% of your rows have the same key (e.g., a status column with three values), hash index buckets for those keys become huge with long overflow chains.
- **Loss of generality.** The hash index is a one-way door for query patterns. If a future requirement adds `ORDER BY`, you must rebuild the index. Most teams would rather pay the small B-tree cost up front.
- **No `Index Only Scan` (as of PostgreSQL 16).** Hash indexes don't store the actual key in a way that supports index-only scans efficiently. B-trees win here.
- **No partial matches.** `LIKE 'abc%'` works on B-trees (with the right operator class); it does not work on hash indexes.
- **Reputation.** Junior engineers may have heard "hash indexes are unsafe." They were, before PG 10. They are not anymore. Document the choice if you use them.

## Trade-offs

- **`O(1)` vs `O(log N)` with small N.** For 10M rows, B-tree depth is 3. The "log N" term is essentially constant. The hash index's `O(1)` saves one or two page reads. Whether that matters depends on your latency budget.
- **Generality vs speed.** B-tree supports ranges, ordering, uniqueness, prefix matches. Hash supports equality only. Trade generality for ~2 page reads saved per lookup.
- **Size vs query support.** Hash indexes are smaller. If RAM is tight and the column is equality-only, hash wins on cache efficiency.
- **Operational maturity.** B-trees have decades of tuning and tooling. Hash indexes work but receive less attention. Pick B-trees unless you have a strong reason.
- **Future-proofing.** Today's equality query is tomorrow's range query. B-trees survive requirement changes; hash indexes do not.

## Forward links

- [[03-B-Tree-Indexes]] — the default and almost-always-right choice.
- [[01-Indexing-Strategy]] — when to deviate from B-trees.
- [[07-Cost-Based-Optimizer]] — the planner picks hash only when the predicate is `=`.
- Back to [[08-Trade-offs-Everywhere]] — the speed-vs-generality trade is a textbook case.
- Back to [[00-WAL-Logging]] — why an index without WAL is broken, even if "fast."
