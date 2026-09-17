---
tags: [concept, jdbc, architecture]
type: concept
status: complete
---

# JDBC Architecture

## What it is

**JDBC** (Java Database Connectivity) is Java's standard API for accessing relational databases. It's a specification (in `java.sql`) implemented by vendor drivers.

## Core interfaces

| Interface | Purpose |
|---|---|
| `Driver` | Loads and connects to a DB. |
| `DriverManager` | Maintains a registry of drivers; creates connections. |
| `DataSource` | A factory for connections. Preferred over DriverManager. |
| `Connection` | A session with the DB. |
| `Statement` | Executes static SQL. |
| `PreparedStatement` | Executes parameterized SQL. |
| `CallableStatement` | Calls stored procedures. |
| `ResultSet` | Iterates over query results. |
| `ResultSetMetaData` | Describes a ResultSet's columns. |
| `DatabaseMetaData` | Describes the DB (tables, columns, etc.). |

## JDBC URL formats

```
jdbc:oracle:thin:@host:port:SID           -- Oracle SID
jdbc:oracle:thin:@//host:port/service     -- Oracle service name
jdbc:postgresql://host:port/database      -- PostgreSQL
jdbc:mysql://host:port/database           -- MySQL
jdbc:sqlserver://host:port;databaseName=  -- SQL Server
```

## JDBC 4.0+ auto-loading

Before JDBC 4.0, you had to `Class.forName("oracle.jdbc.OracleDriver")` to load the driver. JDBC 4.0+ uses `META-INF/services/java.sql.Driver` — drivers auto-register when on the classpath. No `Class.forName` needed.

## Project Connection

The project uses `DriverManager.getConnection` (via static import) — works but `DataSource` is preferred for production (enables pooling, JNDI lookup). The fix: HikariCP `DataSource`.

## Further reading

- JDBC 4.3 Specification.
- *JDBC API Tutorial and Reference* (White et al.).
