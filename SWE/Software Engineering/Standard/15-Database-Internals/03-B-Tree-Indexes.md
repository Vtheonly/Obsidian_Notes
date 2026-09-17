# B-Tree Indexes

> The B-tree (Bayer & McCreight, 1970) is the single most important data structure in databases. It is the structure behind every PostgreSQL default index, every primary key, every unique constraint. Understanding the B-tree is understanding why an index lookup is `O(log N)` page reads instead of `O(N)`.

## What you already know

From [[01-Pages-And-Files]]: tables are heaps of 8 KB pages; finding a row by scanning is `O(N)`. From [[00-Storage-Hierarchy]]: each page read is expensive; we want to minimize them. From [[03-Dependency-As-Root-Concept]]: an index is a dependency — the query depends on the index's structure to find rows fast.

## Why this layer exists

Without an index, the only way to find rows matching `WHERE iban = $1` is to scan every page of the heap — `O(N)` page reads. For a 10-million-row `accounts` table, that is hundreds of thousands of page reads. With an index, you can find the matching rows in `O(log N)` page reads — typically 3-4 page reads for a 10-million-row table. The index converts a linear scan into a logarithmic descent.

The B-tree is the chosen structure because:

1. It is **balanced** — every leaf is at the same depth, so worst-case performance equals average-case performance.
2. It is **page-friendly** — its nodes are sized to match the database's page size, maximizing fan-out (the number of children per node) and minimizing the depth of the tree.
3. It supports **range queries** natively — leaves are linked in sorted order, so a range scan is `O(log N + K)` where K is the number of matching rows.
4. It supports **ordered output** — `ORDER BY col` with an index on `col` can be satisfied without a Sort node.

## What is genuinely new here

The **B+tree** variant — the structure PostgreSQL actually uses — and the algorithms for **search, insert, and split**. The B+tree's defining feature: *all data lives in leaves; internal nodes are pure routing*. This maximizes fan-out and minimizes tree depth.

## Concepts

### Structure

A B+tree has three kinds of pages:

```
                    ┌─────────────────────┐
                    │   Root (internal)   │
                    │ [k1   k2   k3   k4] │
                    └──┬────┬────┬────┬───┘
            ┌──────────┘    │    │    └──────────┐
            ▼               ▼    ▼               ▼
       ┌─────────┐    ┌─────────┐  ┌─────────┐  ┌─────────┐
       │ Internal│    │ Internal│  │ Internal│  │ Internal│
       │[k...]   │    │[k...]   │  │[k...]   │  │[k...]   │
       └──┬─┬────┘    └──┬─┬────┘  └──┬─┬────┘  └──┬─┬────┘
          │ │            │ │          │ │          │ │
          ▼ ▼            ▼ ▼          ▼ ▼          ▼ ▼
       [Leaf]──►[Leaf]──►[Leaf]──►[Leaf]──►[Leaf]──►[Leaf]
       (data)  (data)    (data)    (data)    (data)    (data)
       ◄─────── doubly-linked list of leaves ────────►
```

- **Root**: the top node. Small enough to fit in one page.
- **Internal nodes**: store `(key, child_pointer)` pairs; their job is *routing* — guide the search to the right child.
- **Leaf nodes**: store `(key, CTID)` pairs — the actual pointers to heap tuples. Linked left-to-right and right-to-left for range scans.

A node fills one 8 KB page. With a 24-byte key and an 8-byte CTID, a leaf holds roughly `(8192 - header) / 32 ≈ 250` entries. An internal node holds `(8192 - header) / (key_size + 8) ≈ 250` routing entries too. So a 3-level B+tree can address `250 × 250 × 250 ≈ 15.6 million` rows. A 4-level tree addresses ~4 billion.

**This is the magic of B-trees**: even billions of rows require only 4 page reads for a point lookup. And those 4 pages are very likely cached in `shared_buffers` (the root and upper internal pages are touched by every lookup and stay hot).

### The search algorithm

```
function btree_search(root, key):
    page = root
    while not is_leaf(page):
        # Binary search within the page's key array
        i = binary_search(page.keys, key)
        page = read_page(page.children[i])
    # We're at a leaf
    i = binary_search(page.keys, key)
    return page.ctids[i]   # or scan forward for range
```

Each iteration is one page read (unless cached). The binary search within a page is `O(log fan-out)` ≈ `O(log 250)` ≈ 8 comparisons — negligible compared to the page read itself.

### The insertion algorithm

```
function btree_insert(root, key, ctid):
    # 1. Descend to the correct leaf
    path = []
    page = root
    while not is_leaf(page):
        path.append(page)
        i = binary_search(page.keys, key)
        page = read_page(page.children[i])
    leaf = page

    # 2. Insert into leaf in sorted order
    insert_into_leaf(leaf, key, ctid)

    # 3. If leaf has space, done
    if leaf.fits():
        write_page(leaf)
        return

    # 4. Otherwise split
    split_and_propagate(leaf, path)

function split_and_propagate(node, path):
    new_node = allocate_page()
    move half of node's entries to new_node
    copy_up_key = smallest key in new_node
    write_page(node)
    write_page(new_node)
    if path is empty:
        # We split the root: create a new root
        new_root = allocate_page()
        new_root.children = [node, new_node]
        new_root.keys = [copy_up_key]
        write_page(new_root)
    else:
        parent = path.pop()
        insert_into_parent(parent, copy_up_key, new_node)
        if not parent.fits():
            split_and_propagate(parent, path)
```

Note: in a B+tree, when a leaf splits, the *smallest key in the new leaf* is *copied up* to the parent. (In a B-tree proper, the median key is *moved up* and disappears from the leaf. The B+tree keeps all keys in leaves, so the routing key in internal nodes is a *copy* of a leaf key.) This distinction matters for range scans — you always reach the leaf.

### Why B-trees are balanced

Splits propagate upward *only when a node is full*. The tree grows in height only when the *root* splits, and the root split creates a new root with two children. Every leaf is therefore at exactly the same depth from the root.

Consequence: worst-case lookup cost = average-case lookup cost = `O(log N)`. There is no degenerate tree. Contrast with binary search trees, which can degrade to `O(N)` if inserted in sorted order (hence AVL/red-black trees).

### The B+tree variant — what PostgreSQL actually uses

PostgreSQL's `btree` (the default index type) is a B+tree with one extra feature: **High Keys**. Each page stores a "high key" — the maximum key that page can hold. This makes rightward scans efficient: you know when to stop on the current page without reading the next.

### Cost model: `O(log N)` page reads

A point lookup costs:

```
cost = depth * random_page_cost + leaf_cpu_cost
     ≈ 4 * 4.0 + small ≈ 16 cost units
```

Compare to a sequential scan of the same table:

```
cost = N_pages * seq_page_cost
     = 100000 * 1.0 = 100000 cost units
```

The index wins by ~6000×. This is why indexes matter. See [[07-Cost-Based-Optimizer]] for the full cost model.

### Index-only scans

If all the columns a query needs are in the index, PostgreSQL can satisfy the query *without visiting the heap* — an **Index Only Scan**. This requires the **visibility map** to confirm that all tuples on the relevant heap pages are visible to all transactions (otherwise PostgreSQL must visit the heap to check `t_xmin`/`t_xmax`). After `VACUUM`, the visibility map is up to date and index-only scans become possible.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT iban FROM accounts WHERE iban = 'GB29NWBK60161331926819';
-- Index Only Scan using accounts_iban_idx
--   Buffers: shared hit=3
-- (no heap visit!)
```

### Covering indexes (INCLUDE)

PostgreSQL 11+ supports `INCLUDE` columns — extra columns stored in the leaf but not used as keys:

```sql
CREATE INDEX accounts_iban_covering_idx ON accounts (iban) INCLUDE (current_balance, status);
```

Now `SELECT iban, current_balance, status FROM accounts WHERE iban = $1` is an Index Only Scan. The extra columns bloat the leaf but avoid the heap visit. This is the bridge between normalization (many columns on one row) and read performance (one index lookup).

## Banking application

The `accounts` table has 10 million rows. Without an index, `SELECT * FROM accounts WHERE iban = $1` reads ~200,000 pages (a full scan). With a B-tree on `iban`:

```
depth = ceil(log_250(10,000,000)) ≈ 3
page reads = 3 (internal) + 1 (leaf) + 1 (heap) = 5
```

5 page reads vs 200,000. That is the value of an index.

The composite index on `ledger_entries(account_id, occurred_at DESC)` supports the two most common ledger queries:

- "Show me the last 50 entries for account X" — descend the B-tree to `(account_id=X, occurred_at=∞)` and walk forward 50 leaves.
- "Show me all entries for account X in date range" — descend to the lower bound, walk leaves until the upper bound.

For a customer statement query (one account, six months of entries), the index gives `O(log N + K)` where K is the number of entries in range — typically 100-500 page reads instead of a 12-million-page full scan.

### Why this matters for the transfer flow

The transfer flow (see [[00-Banking-Case-Study]]) reads two `accounts` rows (by `id`, via the primary key B-tree) and reads/writes their `ledger_entries`. Every lookup is `O(log N)`. Without indexes, each transfer would scan the whole `accounts` table — a bank could not process more than a few transfers per second. With indexes, a transfer is a few hundred µs. The index is the difference between "the database works" and "the database is unusable."

## Code / diagrams

PostgreSQL B-tree introspection:

```sql
-- Create the index
CREATE INDEX accounts_iban_idx ON accounts (iban);

-- How big is it?
SELECT pg_size_pretty(pg_relation_size('accounts_iban_idx'));
-- 285 MB

-- How many leaf pages?
SELECT pg_relation_size('accounts_iban_idx') / 8192 AS pages;
-- 36572

-- What's the tree depth? (requires bt_page_items / pageinspect)
CREATE EXTENSION pageinspect;
SELECT * FROM bt_metap('accounts_iban_idx');
--  magic | version | root | level | fastroot | fastlevel
-- -------+---------+------+------+----------+----------
--  654378|       1 |  412 |     3|      412 |        3
--                                                       ^
--                                          tree depth = 3
```

A depth-3 B-tree on 10M rows. Every point lookup descends 3 index pages + 1 heap page = 4 page reads (cached, usually).

Inspecting a B-tree leaf:

```sql
SELECT ctid, itemoffset, lower(itemdata), itemdata
FROM bt_page_items('accounts_iban_idx', 412)
LIMIT 5;
--    ctid   │ itemoffset │     lower      │            itemdata
-- ──────────┼────────────┼────────────────┼────────────────────────────
--  (0,1)    │          1 │ (0,1)          │ GB29NWBK60161331926819
--  (0,2)    │          2 │ (0,2)          │ GB29NWBK60161331926820
--  (0,3)    │          3 │ (0,3)          │ GB29NWBK60161331926821
```

Each leaf entry is `(key=iban, ctid)` — the physical address of the heap tuple. The `ctid` is what gets followed to fetch the actual row.

## What can go wrong

- **Index bloat.** Just like tables, indexes accumulate dead entries after `DELETE`/`UPDATE`. PostgreSQL's autovacuum reclaims them, but a high-update table can bloat faster than autovacuum keeps up. `REINDEX` rebuilds the index.
- **Random-insert UUID indexes.** A UUID v4 primary key scatters inserts across all leaves of the B-tree. Each insert may split a different leaf — write amplification, fragmentation, larger index than necessary. UUID v7 / ULID (time-ordered) fix this.
- **Page splits on monotonic inserts.** Inserting strictly increasing keys (e.g., a `BIGSERIAL`) causes splits only on the rightmost leaf — not bad. Inserting random keys causes splits across the tree — worse.
- **Stale statistics on indexes.** The planner uses `pg_class.reltuples` to estimate index selectivity. After bulk deletes, statistics are stale and the planner may misestimate. Run `ANALYZE`.
- **Index corruption.** Rare, but possible after hardware failures. The `amcheck` extension (`CREATE EXTENSION amcheck; SELECT bt_index_check('accounts_iban_idx');`) verifies structural integrity.
- **Too many indexes.** Every index slows writes (each `INSERT`/`UPDATE`/`DELETE` must update every index). A table with 15 indexes can be 5× slower to write than one with 3. See [[01-Indexing-Strategy]].
- **Index scan vs seq scan crossover.** For a query that matches a large fraction of rows, a sequential scan is faster than an index scan (which would do random I/O for each row). The planner makes this call, but only if statistics are accurate. See [[07-Cost-Based-Optimizer]].

## Trade-offs

- **Read speed vs write speed.** More indexes = faster reads, slower writes. The fundamental indexing trade-off.
- **Fan-out vs key size.** Smaller keys = more entries per page = higher fan-out = shallower tree = fewer page reads. A 16-byte UUID index is 4 levels deep at 10M rows; a 100-byte string index might be 5 levels. Use surrogate keys when natural keys are wide.
- **Index-only scans vs leaf bloat.** `INCLUDE` columns make index-only scans possible but bloat the leaf. Trade storage for read speed.
- **Clustered (index-organized) vs heap.** PostgreSQL tables are heaps (separate from any index). MySQL/InnoDB tables are clustered (the primary key *is* the table layout). Clustered = faster PK lookup but slower secondary index lookup. Trade on workload.
- **B-tree vs other index types.** B-trees handle equality and range queries well. For full-text search, use GIN. For geometric data, use GiST. For very large data with skewed distribution, consider BRIN. See [[01-Indexing-Strategy]].

## Forward links

- [[04-Hash-Indexes]] — when equality-only is enough, hash indexes are simpler (but rarely faster).
- [[07-Cost-Based-Optimizer]] — how the planner chooses between index scan and seq scan.
- [[08-Reading-EXPLAIN]] — Index Scan, Index Only Scan, Bitmap Heap Scan all use B-trees.
- [[01-Indexing-Strategy]] — when to add, when to drop, what to cover.
- Back to [[01-Primary-Foreign-Keys]] — every PK and FK is backed by a B-tree.
- Back to [[03-Dependency-As-Root-Concept]] — an index is a dependency the query relies on; a missing index is a dependency failure.
