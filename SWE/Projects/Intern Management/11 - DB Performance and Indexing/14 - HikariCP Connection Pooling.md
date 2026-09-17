---
tags: [concept, database, performance, jdbc, connection-pool, hikaricp]
type: concept
status: complete
prerequisites:
  - [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]]
related:
  - [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
  - [[13 - JDBC and Data Access/18 - try-with-resources]]
  - [[10 - Transactions and Concurrency/02 - Auto-Commit Mode]]
---

# HikariCP Connection Pooling

## What it is

A **connection pool** maintains a set of open database connections and lends them out to callers. Each operation borrows a connection, uses it, returns it. No per-operation `DriverManager.getConnection()` (which is slow - TCP handshake + auth + session setup, ~50-200ms).

**HikariCP** is the fastest JDBC connection pool in the Java ecosystem. It's the default in Spring Boot.

## The basic setup

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:oracle:thin:@//localhost:1521/XEPDB1");
config.setUsername("app_user");
config.setPassword("...");
config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30_000);    // ms to wait for a free connection
config.setIdleTimeout(10 * 60_000);     // ms before an idle connection is closed
config.setMaxLifetime(30 * 60_000);     // ms before a connection is recycled
config.setPoolName("intern-pool");

HikariDataSource ds = new HikariDataSource(config);

// Borrow / use / return
try (Connection c = ds.getConnection()) {
    c.setAutoCommit(false);
    // ... use c ...
    c.commit();
}
```

## Pool sizing

The famous [HikariCP wiki article](https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing) argues for **smaller pools than you think**:

> The formula is: `connections = ((core_count * 2) + effective_spindle_count)`

For an 8-core app server against SSD storage, that's `8*2 + 1 = 17` - round to 10-20. A pool of 100 is almost always worse than a pool of 10, because:

- More connections = more contention on the database (each holds locks, undo space).
- The CPU can only run so many queries in parallel; queuing at the pool is better than queuing at the DB.

## What HikariCP does for you

- **Borrows fast** - lock-free, ~50ns per `getConnection()`.
- **Tests connections** - runs `isValid()` or a `connectionTestQuery` before lending.
- **Recycles stale connections** - `maxLifetime` ensures connections don't outlive DB-side timeouts (firewalls, idle kills).
- **Resets state on return** - autocommit, isolation level, read-only flag are reset to defaults so the next borrower gets a clean connection.
- **Detects leaks** - logs a warning if a connection is held longer than `leakDetectionThreshold`.

## Why it matters

A `DriverManager.getConnection()` is 50-200ms. A pool borrow is microseconds. For an app that does 100 DB operations per request, that's the difference between a 5-second page load and a 50ms one.

The pool also bounds the load on the database - if you have a pool of 10, the database sees at most 10 concurrent queries. Without a pool (or with `DriverManager.getConnection()` per operation), a spike in app traffic becomes a spike in DB connections, which can exhaust the DB's process limit.

## Project Connection

The project uses `DriverManager.getConnection()` once, statically:

```java
private static Connection connection = DriverManager.getConnection(...);
```

This is the worst of all worlds:

- One connection (no concurrency).
- Held forever (no recycling; if the DB kills the session, the app breaks).
- Shared across threads (not thread-safe - see [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]]).

The redesign replaces this with a HikariCP pool. Spring Boot auto-configures HikariCP from `application.yml`:

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
```

## Common pitfalls

- Setting `maximumPoolSize` to the number of concurrent users - that's 100x too high. Pool size = concurrent **queries**, not concurrent users.
- Forgetting `maxLifetime` - connections that live forever eventually hit a stale TCP state or DB-side kill.
- Holding a connection across a user-input wait - the pool runs dry; other requests block.
- Calling `close()` on a borrowed connection twice - the second call is a no-op, but it's a sign of confused ownership.

## Trade-offs

- **Pool size vs latency**: a bigger pool handles more concurrent requests but adds DB contention.
- **Borrow cost vs setup cost**: pools pay setup once and borrow cheaply; `DriverManager` pays setup every time.

## Further reading

- HikariCP wiki, "About Pool Sizing".
- [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
- [[10 - Transactions and Concurrency/03 - Connection Is Not Thread-Safe]]
