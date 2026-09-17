---
tags: [concept, database, performance, connection-pool]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]]
related:
  - [[11 - DB Performance and Indexing/15 - HikariCP]]
---

# Connection Pooling

## What it is

A **connection pool** is a cache of database connections. Instead of opening a new connection for each operation (expensive — TCP handshake, authentication, session setup), the application borrows a connection from the pool, uses it, and returns it.

```
[App] → [Pool: conn1, conn2, conn3, ...] → [DB]
```

## Why it exists

Opening a JDBC connection costs ~50-100 ms (TCP + auth + session). If every operation opens a new connection, you spend more time connecting than querying.

A pool keeps connections open. Borrow is ~0 ms (just mark it as in-use). Return is ~0 ms (mark as available).

## Pool lifecycle

1. **Init** — pool opens `minimumIdle` connections.
2. **Borrow** — `dataSource.getConnection()` returns an idle connection (or opens a new one if below `maximumPoolSize`).
3. **Use** — the application uses the connection.
4. **Return** — `connection.close()` (in try-with-resources) returns it to the pool, doesn't close it.
5. **Validation** — the pool may test the connection (`SELECT 1 FROM DUAL`) before lending it.
6. **Eviction** — idle connections above `minimumIdle` are closed after `idleTimeout`.
7. **Max lifetime** — connections are recycled after `maxLifetime` (30 min default) to prevent stale connections.

## Configuration

| Parameter | Typical | Purpose |
|---|---|---|
| `maximumPoolSize` | 10 | Max connections. More isn't always better — the DB has limits. |
| `minimumIdle` | 2 | Keep this many idle connections ready. |
| `connectionTimeout` | 30 sec | How long to wait for a connection before failing. |
| `idleTimeout` | 10 min | How long an idle connection sits before being closed. |
| `maxLifetime` | 30 min | Max connection age; recycle to prevent staleness. |
| `connectionTestQuery` | `SELECT 1 FROM DUAL` | Validation query. |

## Pool sizing rule of thumb

> `pool_size = (core_count × 2) + effective_spindle_count`

For a 4-core server with 1 disk: `(4 × 2) + 1 = 9`. Round to 10.

More connections don't help — the DB has limited cores, and too many connections cause context-switching overhead. See HikariCP's wiki on pool sizing.

## Project Connection

The project uses a single static `Connection` — no pool. Every operation serializes through it. The fix: HikariCP pool with `maximumPoolSize=10`.

## Further reading

- HikariCP wiki — About Pool Sizing.
- *Database Internals* (Petrov).
