---
tags: [concept, database, oracle, schemas]
type: concept
status: complete
prerequisites:
  - [[08 - Relational DB Foundations/18 - The Relational Model]]
related:
  - [[08 - Relational DB Foundations/12 - Quoted Identifiers]]
  - [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
---

# Schemas and Users in Oracle

## What it is

In Oracle, **a schema IS a user**. There is no separate "schema" object you create independently. When you `CREATE USER app_owner IDENTIFIED BY ...`, you have created an empty schema owned by that user. Every table you then create lives in that schema and is namespaced as `APP_OWNER.intern`.

This is different from PostgreSQL (schemas are namespaces inside a database, separate from users) and SQL Server (schemas are namespaces inside a database, owned by users but transferable).

## The two-user pattern

The standard secure setup uses **two users**:

- **`app_owner`** - owns the tables, sequences, packages. Has DDL privileges. Application **never** connects as this user.
- **`app_user`** - has only DML privileges (`SELECT, INSERT, UPDATE, DELETE`) on the owner's tables, granted via `GRANT ... ON app_owner.intern TO app_user` or via roles. The application connects as this user.

```sql
-- As DBA
CREATE USER app_owner IDENTIFIED BY "...";
GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE TO app_owner;
ALTER USER app_owner QUOTA UNLIMITED ON users;

CREATE USER app_user IDENTIFIED BY "...";
GRANT CREATE SESSION TO app_user;

-- As app_owner
CREATE TABLE intern (...);
GRANT SELECT, INSERT, UPDATE, DELETE ON intern TO app_user;
CREATE SYNONYM intern FOR app_owner.intern;  -- so app_user can write "intern"
-- (synonyms must be created by app_user or via "CREATE SYNONYM app_user.intern ...")
```

This way, even if the app is compromised, the attacker cannot `DROP TABLE` - the app user lacks DDL privileges.

## Multitenant architecture (12c+)

Modern Oracle (XE 18c+) is a **CDB** (Container Database) with one or more **PDBs** (Pluggable Databases). XE ships with one PDB: `XEPDB1`. The CDB root (`CDB$ROOT`) holds infrastructure; user data lives in the PDB. Your connection string is:

```
jdbc:oracle:thin:@//localhost:1521/XEPDB1
```

The service name `XEPDB1` (not `XE`) is what routes you into the PDB.

## Why it matters

- Connecting as `SYS` or `SYSTEM` from the application is an anti-pattern - those users can drop the database.
- The "schema = user" model means renaming a schema is hard (you'd have to export/import). Plan names up front.
- Privilege separation is your last defense against SQL injection - see [[12 - Advanced Database Features/16 - VPD - Virtual Private Database]] for row-level defense.

## Project Connection

The project connects as a single user that owns the tables **and** runs the application:

```java
// oracleConnector.java
private static final String URL = "jdbc:oracle:thin:@localhost:1521:XE";
private static final String USER = "sys as sysdba";  // or some overloaded user
```

This is the database equivalent of running your web app as `root`. The fix:

1. Create `app_owner` and `app_user` per the two-user pattern above.
2. Connect as `app_user` from JDBC.
3. Add a flyway user for migrations.

## Common pitfalls

- Connecting as `SYS AS SYSDBA` from the app - `SYS` owns the data dictionary; a typo can drop a system view.
- Putting application tables in the `SYSTEM` tablespace - it's reserved for the data dictionary; mixing slows both.
- Forgetting to grant on the **sequence** too - `GRANT SELECT ON intern_seq TO app_user` is needed for `intern_seq.NEXTVAL`.

## Further reading

- Oracle Docs, "Database Administrator's Guide", "Managing Users and Schema Objects".
- [[13 - JDBC and Data Access/04 - DataSource vs DriverManager]]
- [[12 - Advanced Database Features/16 - VPD - Virtual Private Database]]
