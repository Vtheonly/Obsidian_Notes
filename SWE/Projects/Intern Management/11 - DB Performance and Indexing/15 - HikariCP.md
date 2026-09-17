---
tags: [concept, database, hikaricp, pool]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/09 - Connection Pooling]]
related:
  - [[13 - JDBC and Data Access/05 - DataSource]]
---

# HikariCP

## What it is

**HikariCP** (Hikari = "light" in Japanese) is the fastest JDBC connection pool for Java. It's the default pool in Spring Boot 2+.

## Maven dependency

```xml
<dependency>
    <groupId>com.zaxxer</groupId>
    <artifactId>HikariCP</artifactId>
    <version>5.1.0</version>
</dependency>
```

## Configuration

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl(System.getenv("DB_URL"));
config.setUsername(System.getenv("DB_USER"));
config.setPassword(System.getenv("DB_PASSWORD"));

config.setMaximumPoolSize(10);
config.setMinimumIdle(2);
config.setConnectionTimeout(30_000);   // 30 sec
config.setIdleTimeout(600_000);        // 10 min
config.setMaxLifetime(1_800_000);      // 30 min

config.setConnectionTestQuery("SELECT 1 FROM DUAL");  // Oracle

// Oracle optimizations
config.addDataSourceProperty("implicitCachingEnabled", "true");
config.addDataSourceProperty("maxStatements", "250");

HikariDataSource dataSource = new HikariDataSource(config);

// Use it
try (Connection conn = dataSource.getConnection()) {
    // ...
}
```

## Why HikariCP is fast

- **Bytecode-level optimization** — uses `ConcurrentBag` (custom concurrent collection) instead of synchronized lists.
- **No proxy objects** — connections are used directly.
- **Fast validation** — uses JDBC4 `isValid()` when available.
- **Small footprint** — ~130 KB.

## HikariCP MXBean

HikariCP exposes JMX metrics:
```java
HikariPoolMXBean pool = dataSource.getHikariPoolMXBean();
System.out.println("Active: " + pool.getActiveConnections());
System.out.println("Idle: " + pool.getIdleConnections());
System.out.println("Total: " + pool.getTotalConnections());
System.out.println("Threads waiting: " + pool.getThreadsAwaitingConnection());
```

Use this for the diagnostics dashboard.

## Project Connection

The project's `static Connection` is replaced by HikariCP:
```java
public class DbConnectionPool {
    private static final HikariDataSource dataSource;

    static {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(System.getenv("DB_URL"));
        // ... configuration
        dataSource = new HikariDataSource(config);
    }

    public static DataSource getDataSource() {
        return dataSource;
    }
}
```

Repositories receive the `DataSource` via constructor injection.

## Common pitfalls

- **Too large a pool** — `maximumPoolSize=100` on a 4-core DB. More connections = more context switching = slower. Stick to the formula.
- **No `maxLifetime`** — connections go stale after DB restarts or network blips. Set `maxLifetime` below the DB's `idle_time`.
- **Hardcoded credentials** — use environment variables or secrets management.

## Further reading

- HikariCP GitHub — wiki and README.
