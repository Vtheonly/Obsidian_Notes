---
tags: [concept, database, oracle, sequences, identity]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/07 - Keys - Primary, Foreign, Candidate, Surrogate]]
related:
  - [[12 - Advanced Database Features/04 - IDENTITY Columns]]
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
---

# Sequences

## What it is

A **sequence** is a database object that generates unique integers, typically used for surrogate primary keys. Each call to `seq.NEXTVAL` returns the next number; `seq.CURRVAL` returns the most recent number your session generated.

```sql
CREATE SEQUENCE intern_seq
    START WITH 1
    INCREMENT BY 1
    NOCYCLE
    CACHE 20;     -- cache 20 values in memory for speed

-- Use it
INSERT INTO intern(intern_id, name) VALUES (intern_seq.NEXTVAL, 'Alice');
INSERT INTO intern(intern_id, name) VALUES (intern_seq.NEXTVAL, 'Bob');
```

## Sequence properties

- **`INCREMENT BY n`** - step size. `1` is default; use `-1` for descending.
- **`START WITH n`** - first value.
- **`MINVALUE`/`MAXVALUE`** - bounds.
- **`CYCLE`/`NOCYCLE`** - what to do at MAX. `NOCYCLE` (default) errors; `CYCLE` wraps to MIN.
- **`CACHE n`** - cache n values in the SGA for fast `NEXTVAL`. Default 20. Set higher for high-throughput inserts.
- **`ORDER`/`NOORDER`** - in RAC, `ORDER` guarantees time-ordered values across nodes (slower). `NOORDER` (default) does not.

## Why sequences exist

The alternatives are all worse:

- **`MAX(id)+1`** - race condition. Two concurrent inserts compute the same max; one fails with PK violation. (This is the project's bug.)
- **Application-generated GUID** - larger indexes, slower joins.
- **Application counter** - not durable; restart loses the count.
- **A `next_id` table** - one row, every insert locks it; serializes all inserts.

A sequence is a **single highly-optimized atomic counter** in the SGA. `NEXTVAL` is essentially free.

## The gap caveat

Sequences are **not gap-free**. A transaction that gets `NEXTVAL` and then rolls back "loses" that value - the next call returns `NEXTVAL + 1`, not the same value. Similarly, cached values are lost on instance restart.

This is **by design**. Gap-free sequences would require serializing all transactions on the sequence, killing concurrency. If your business requires gap-free invoice numbers (for legal reasons), use a separate `counter_table` with row-level locks - and accept the throughput cost.

## Caching

`CACHE 20` (default) means the SGA holds 20 sequence values. When the 20th is consumed, the SGA fetches the next 20 in one operation. This makes `NEXTVAL` nearly free.

For high-throughput inserts, increase the cache:

```sql
ALTER SEQUENCE intern_seq CACHE 1000;
```

In RAC, each node has its own cache - so values from node A may interleave with values from node B. `ORDER` forces serialization across nodes; use only if you must.

## Project Connection

`insertion.sql` does not declare any sequences. The Java code generates IDs via `MAX(id)+1`:

```java
int newId = oracleConnector.getMaxId("intern", "intern_id") + 1;
```

This is the race condition described in [[10 - Transactions and Concurrency/01 - ACID Properties]]. The fix is a sequence:

```sql
CREATE SEQUENCE intern_seq START WITH 1 CACHE 100;
```

...or, better, an IDENTITY column - see [[12 - Advanced Database Features/04 - IDENTITY Columns]].

## Common pitfalls

- Using `MAX(id)+1` "to keep IDs gap-free" - they aren't gap-free anyway (deletes leave gaps); and you've introduced a race.
- Setting `CACHE 0` (no cache) - serializes all inserts on the sequence; throughput collapses.
- Forgetting to grant `SELECT` on the sequence to the app user.
- Sharing one sequence across tables - works, but conflates two domains; use one sequence per table.

## Further reading

- Oracle Docs, "CREATE SEQUENCE".
- [[12 - Advanced Database Features/04 - IDENTITY Columns]]
