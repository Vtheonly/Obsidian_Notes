---
tags: [concept, jdbc, java, data-access, connection-pool]
type: concept
status: complete
prerequisites:
  - [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
related:
  - [[11 - DB Performance and Indexing/14 - HikariCP Connection Pooling]]
  - [[13 - JDBC and Data Access/18 - try-with-resources]]
---

# Connection Pooling

## What it is

A **connection pool** maintains a set of open database connections and lends them to callers. Each operation borrows a connection, uses it, returns it. The pool avoids the 50-200ms cost of opening a fresh connection per operation.

From the JDBC perspective, the pool is a `DataSource` implementation: you call `ds.getConnection()`, you get a `Connection` (which is actually a thin wrapper around a pooled physical connection), and when you call `close()`, the wrapper returns the physical connection to the pool instead of closing it.

## The pool lifecycle

1. **Borrow** - `ds.getConnection()` either returns an idle connection immediately or waits for one to become idle (up to `connectionTimeout`).
2. **Use** - the caller runs SQL on the connection.
3. **Return** - `close()` (typically via try-with-resources) returns the wrapper to the pool. The pool resets the connection state (auto-commit, isolation level) so the next borrower gets a clean slate.
4. **Health check** - the pool may run `isValid()` or a `connectionTestQuery` before lending, to avoid handing out a dead connection.
5. **Recycle** - connections older than `maxLifetime` are closed and replaced, to avoid DB-side idle kills and firewall timeouts.

## Why pools matter

- **Latency** - a pool borrow is microseconds; `DriverManager.getConnection()` is 50-200ms.
- **Throughput** - the pool bounds the number of concurrent DB connections, preventing the DB from being overwhelmed.
- **Resource hygiene** - the pool's `maxLifetime` and `idleTimeout` prevent stale connections.
- **Reset on return** - the pool resets state, so one borrower's `setAutoCommit(false)` doesn't leak to the next.

## Pool implementations

| Pool | Notes |
|---|---|
| **HikariCP** | Fastest, smallest, default in Spring Boot. See [[11 - DB Performance and Indexing/14 - HikariCP Connection Pooling]]. |
| **Tomcat JDBC** | Older, decent, comes with Tomcat. |
| **Apache DBCP** | Oldest, slowest, avoid for new projects. |
| **Oracle UCP** | Oracle's pool, tightly integrated with Oracle DB. |
| **c3p0** | Legacy; avoid for new projects. |

For Oracle XE with Spring Boot, **HikariCP** is the default and the right choice.

## Sizing the pool

The famous HikariCP wiki formula:

> `connections = ((core_count * 2) + effective_spindle_count)`

For an 8-core app server against SSD: `8*2 + 1 = 17` - round to 10-20.

Bigger is **not** better. A pool of 100 means up to 100 concurrent queries hit the DB; the DB spends more time coordinating than executing. A pool of 10 queues excess requests at the app (cheap) rather than at the DB (expensive).

## Leaks

A connection leak is when a borrower forgets to `close()`. The pool thinks the connection is in use; it never returns to the idle set. Eventually the pool runs dry; new requests block on `getConnection()` until `connectionTimeout` and then throw.

HikariCP's `leakDetectionThreshold` (default disabled) logs a stack trace if a connection is held longer than the threshold - the stack trace points at the code that forgot to close.

```java
config.setLeakDetectionThreshold(60_000);   // warn if held > 60s
```

The fix for leaks is **always try-with-resources**. See [[13 - JDBC and Data Access/18 - try-with-resources]].

## Why it matters

Without a pool, every request opens a connection (50-200ms), runs a few queries (1-10ms each), and closes it. The open/close dominates. With a pool, open/close is amortized to near-zero, and the per-request time is the query time.

## Project Connection

The project has no pool - one static `Connection`. See [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]]. The redesign replaces this with HikariCP, configured in `application.yml`:

```yaml
spring:
  datasource:
    url: jdbc:oracle:thin:@//localhost:1521/XEPDB1
    username: app_user
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 10
      minimum-idle: 2
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 60000
      pool-name: intern-pool
```

## Common pitfalls

- Setting `maximumPoolSize` to the concurrent user count - that's 100x too high. Pool size = concurrent **queries**.
- Forgetting `maxLifetime` - connections that live forever eventually hit a stale TCP state.
- Holding a connection across a user-input wait - the pool runs dry.
- Calling `close()` on a borrowed connection twice - the second is a no-op but signals confused ownership.

## Further reading

- HikariCP wiki, "About Pool Sizing".
- [[11 - DB Performance and Indexing/14 - HikariCP Connection Pooling]]
