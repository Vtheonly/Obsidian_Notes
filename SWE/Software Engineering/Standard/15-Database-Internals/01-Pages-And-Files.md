# Pages and Files

> Databases do not read rows. They read **pages** — fixed-size blocks of bytes, typically 8 KB. Every SQL statement that touches disk is, at the bottom, a sequence of page reads and page writes. Understanding the page format is the key to understanding why indexes help, why `VACUUM` exists, why `UPDATE` is sometimes as expensive as `INSERT`, and why TOAST exists.

## What you already know

From [[00-Storage-Hierarchy]]: the gap between RAM and disk is ~1000×, so databases move data in pages to amortize the cost of crossing that gap. From [[04-Abstraction-and-Models]]: SQL hides storage layout; this chapter opens the hood.

## Why this layer exists

Disk reads are expensive *per request*, not just per byte. Whether you read 8 bytes or 8 KB, the OS and the disk controller pay roughly the same fixed cost (a syscall, a context switch, an interrupt). So you batch: read 8 KB at a time even if you only need 12 bytes, because the marginal cost of those extra bytes is ~0, and the next row you need is probably in the same page.

This is why databases *never* expose "give me row 42." They expose "give me page 7, and let me parse out row 42 myself." The page is the unit of I/O, the unit of locking, the unit of caching (see [[02-Buffer-Pool]]), and the unit of WAL logging (see [[00-WAL-Logging]]).

## What is genuinely new here

The **slotted page** format — a layout that lets rows be added, deleted, and updated *inside* a fixed-size page without rewriting the whole page. And **TOAST** — the mechanism for storing values too large to fit in a page.

## Concepts

### The 8 KB page

PostgreSQL pages are 8 KB by default (configurable at compile time, rarely changed). Every table, every index, every TOAST table is a sequence of 8 KB pages on disk.

```
┌──────────────────────────────────────────────────────┐
│ Page Header (24 bytes)                                │
│   pd_lsn        — LSN of last change (for WAL)        │
│   pd_checksum   — page checksum                       │
│   pd_lower/pd_upper — free space boundaries           │
│   pd_special    — offset to special data (indexes)    │
├──────────────────────────────────────────────────────┤
│ Line Pointer 1   (4 bytes) ──► tuple at offset X      │
│ Line Pointer 2   (4 bytes) ──► tuple at offset Y      │
│ Line Pointer 3   (4 bytes) ──► tuple at offset Z      │
│ ...                                                   │
├──────────────────────────────────────────────────────┤
│                                                       │
│         FREE SPACE                                    │
│                                                       │
├──────────────────────────────────────────────────────┤
│ Tuple N    (variable length, grows downward)          │
│ ...                                                   │
│ Tuple 3                                               │
│ Tuple 2                                               │
│ Tuple 1                                               │
└──────────────────────────────────────────────────────┘
                       8192 bytes
```

Three regions:

1. **Header** (24 bytes) — page metadata, including the LSN of the last WAL record that touched this page (used by recovery; see [[00-WAL-Logging]]).
2. **Line pointer array** (item identifiers) — grows downward from the header. Each entry is 4 bytes pointing to a tuple's offset and length. The ith tuple on the page is "item i"; its line pointer never moves, even if the tuple does.
3. **Tuple area** — grows upward from the bottom. Tuples are appended at the bottom of the free space.

This layout is the **slotted page** design: line pointers are stable identifiers; tuples can move. A `VACUUM` compacts tuples upward, leaving all line pointers valid. An `UPDATE` writes a new tuple elsewhere and updates the line pointer's target (with MVCC, both versions coexist briefly; see [[04-MVCC]]).

### Tuples, not rows

What you call a "row" in SQL is a *tuple* on a page. A tuple is:

```
┌─────────────────────────────────────────┐
│ HeapTupleHeader (23 bytes + null bitmap)│
│   t_xmin   — XID that inserted this     │
│   t_xmax   — XID that deleted/updated   │
│   t_cid    — command ID within xact     │
│   t_ctid   — CTID of newer version      │
├─────────────────────────────────────────┤
│  Column 1 value                         │
│  Column 2 value                         │
│  ...                                    │
└─────────────────────────────────────────┘
```

The `t_xmin` / `t_xmax` transaction IDs are the heart of MVCC. A tuple is visible to a transaction `T` iff `t_xmin` is committed and visible to `T`, and (`t_xmax` is invalid, or `t_xmax` is not yet visible to `T`). This is how snapshot isolation is implemented — see [[04-MVCC]].

`t_ctid` points to the *next* version of the tuple. On `UPDATE`, PostgreSQL writes a brand-new tuple elsewhere on disk and updates the old tuple's `t_ctid` to point at it. A row's logical identity is the chain; its physical reality is many tuples.

### CTID — the physical address

Every tuple has a `CTID` = `(page_number, line_pointer_index)`. This is the physical address. It is exposed:

```sql
SELECT ctid, iban FROM accounts LIMIT 3;
--    ctid  │        iban
-- ─────────┼─────────────────────
--  (0,1)   │ GB29NWBK60161331926819
--  (0,2)   │ GB29NWBK60161331926820
--  (0,3)   │ GB29NWBK60161331926821
```

`(0,1)` means page 0, line pointer 1. CTIDs change after `VACUUM` — never store them as data.

### The free space map (FSM)

PostgreSQL tracks how much free space each page has, in a side file called the **Free Space Map**. When you `INSERT`, PostgreSQL consults the FSM to find a page with enough free space; if none, it extends the file with a new page. The FSM is critical for performance: without it, every `INSERT` would have to scan pages looking for room.

### TOAST — The Oversized-Attribute Storage Technique

A tuple must fit in a page. A page is 8 KB. So a single tuple's data must be ≤ ~2 KB (after header and overhead). What happens when you store a 50 KB JSON document in a `ledger_entries.metadata` column?

PostgreSQL **TOASTs** it:

1. The large value is compressed (LZ-family) — if it now fits, store inline.
2. If still too big, the value is *moved out* to a separate **TOAST table** — a side table named `pg_toast_<oid>`, with the same 8 KB page format. Each TOAST row is a ~2 KB chunk. The original column stores a 18-byte pointer to the first chunk.
3. On read, PostgreSQL follows the pointer, fetches the chunks, reassembles, decompresses, and returns the value.

The user-visible effect: a `SELECT metadata FROM ledger_entries WHERE id = 42` quietly becomes two reads — one of the heap page, one (or several) of the TOAST table. This is invisible in `EXPLAIN` unless you add `BUFFERS`:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT metadata FROM ledger_entries WHERE id = 42;
-- Index Scan using ledger_entries_pkey
--   Buffers: shared hit=4   ← 1 heap page + 3 TOAST pages
```

### Heaps, indexes, and the difference

A **heap** is a table — an unordered bag of tuples. There is no implied order on disk. The only way to find a row by `id` is to scan the heap, *or* use an index.

An **index** is a separate on-disk structure (a B-tree, a hash, a GiST, etc.) that maps a key to a `CTID`. Looking up `accounts WHERE iban = $1`:

1. Read the index's B-tree, find the leaf with `iban = $1`, get its `CTID`.
2. Read the heap page that `CTID` points to.
3. Return the tuple.

Two page reads (probably three or four with B-tree internal nodes — see [[03-B-Tree-Indexes]]). Without the index: a sequential scan of the whole heap, reading every page.

## Banking application

A `ledger_entries` row is ~150 bytes (id, account_id, amount, occurred_at, transfer_id, metadata-ish fields). An 8 KB page holds ~50 such rows after header and overhead.

Practical consequences:

- **Reading 100 entries is 2 page reads**, not 100. If you read a customer's recent 100 ledger entries via the `(account_id, occurred_at DESC)` index, the index points to maybe 3-5 heap pages. Each heap page gives you 50 rows. The 100 rows are read in 3-5 disk reads, not 100. This is the entire point of batching.
- **Inserting 1,000 transfers in a batch** appends to ~20 new heap pages and updates ~20 index pages. Sequential I/O. Fast.
- **Random `UPDATE`s to a hot account's `current_balance`** write a new tuple on the same page (likely still in the buffer pool). The old tuple becomes a dead tuple, waiting for `VACUUM`. After many updates, a page can fill with dead tuples — that's bloat.
- **TOAST on `transfers.fraud_metadata` JSONB** — large fraud payloads spill to the TOAST table. A query that selects only `amount` does not touch TOAST. A query that selects `fraud_metadata` does. Read only what you need.

## Code / diagrams

Inspecting page-level reality in PostgreSQL:

```sql
-- How big is my table on disk?
SELECT pg_size_pretty(pg_relation_size('ledger_entries'));
-- 124 MB

-- How many 8 KB pages is that?
SELECT pg_relation_size('ledger_entries') / 8192 AS pages;
-- 15872

-- Average rows per page (rough):
SELECT reltuples::float / (pg_relation_size('ledger_entries') / 8192)
FROM pg_class WHERE relname = 'ledger_entries';
-- ~48 rows/page  (close to our 50 estimate)

-- Where does TOAST live?
SELECT reltoastrelid::regclass FROM pg_class WHERE relname = 'ledger_entries';
-- pg_toast_16423

-- Inspect tuple headers (requires the pageinspect extension)
CREATE EXTENSION pageinspect;
SELECT t_xmin, t_xmax, t_ctid, * FROM heap_page_items(get_raw_page('accounts', 0)) LIMIT 5;
```

The `pageinspect` extension is your microscope. Use it to see bloat, tuple chaining, and free space directly.

## What can go wrong

- **Bloat.** Repeated `UPDATE`s leave dead tuples behind. Until `VACUUM` reclaims them, the table grows. A 100 MB table can balloon to 2 GB. Every read of a bloated table reads more pages than necessary. Solution: aggressive autovacuum, or `VACUUM FULL` (which locks the table).
- **Tuple chaining.** An `UPDATE` of a row that no longer fits in its original page (because the new value is larger) creates a *redirected* tuple. Reads follow the chain — slower. Frequent updates to a row whose size grows (e.g., appending to a JSONB column) are worst case.
- **Line pointer overflow.** A page with many tiny rows can fill its line pointer array before its tuple area. Rare in practice, but possible.
- **TOAST penalty on small selects.** `SELECT *` when you only need three columns triggers TOAST reads for every large column. Use explicit column lists.
- **Page checksums.** Enabled by default since PostgreSQL 12. If a page is corrupted on disk (bad RAM, dying disk), PostgreSQL detects it on read and refuses to return corrupt data — but the query fails. Monitor `pg_stat_database.checksum_failures`.
- **CTID assumptions.** Code that stores `CTID` for later reuse is broken — `VACUUM` moves tuples. Always go through the primary key.

## Trade-offs

- **Page size: 8 KB vs 16 KB vs 32 KB.** Bigger pages = better throughput for sequential scans and higher B-tree fan-out (fewer levels, fewer reads). Smaller pages = less waste for sparse access, less lock contention. PostgreSQL's 8 KB is a conservative default inherited from BSD filesystem conventions.
- **Inline vs TOAST.** Smaller inline values = faster selects, but forces large values out to TOAST. You can tune `STORAGE` per column (`PLAIN`, `EXTERNAL`, `EXTENDED`, `MAIN`) — but defaults are almost always right.
- **Heap vs index-organized table.** PostgreSQL always uses a heap (the row lives in the heap, the index points to it). MySQL/InnoDB's tables are index-organized (the row lives in the B-tree leaf). Index-organized tables are faster for primary-key lookups but slower for secondary index reads (each secondary index lookup must traverse the PK again). This is a deep architectural trade-off.
- **Compression.** TOAST compression saves disk and RAM but costs CPU. For OLAP workloads on cold data, it is almost always worth it; for hot OLTP, sometimes not.

## Forward links

- [[02-Buffer-Pool]] — pages live in `shared_buffers` when they are hot.
- [[03-B-Tree-Indexes]] — index pages have a different (but related) layout.
- [[00-WAL-Logging]] — the `pd_lsn` field is how recovery knows which pages need redo.
- [[04-MVCC]] — `t_xmin` / `t_xmax` and the tuple chain.
- Back to [[00-Schema-Design]] and [[01-Primary-Foreign-Keys]] — schema choices have physical consequences you only see at the page layer.
- Back to [[04-Abstraction-and-Models]] — the page is the leak in SQL's "row" abstraction.
