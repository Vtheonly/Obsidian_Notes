---
tags: [concept, database, migration, flyway]
type: concept
status: complete
related:
  - [[14 - Schema Evolution/06 - Liquibase]]
---

# Flyway

## What it is

**Flyway** is a database migration tool. It version-controls your schema by applying SQL scripts in order.

## How it works

1. Migrations live in `src/main/resources/db/migration/`.
2. Each migration is named `V<version>__<description>.sql` (e.g., `V1__create_baseline.sql`).
3. Flyway creates a `flyway_schema_history` table in your DB, tracking applied migrations.
4. On app startup, Flyway scans for migrations, applies unapplied ones in order.

## Migration naming

```
V1__create_baseline.sql
V2__add_audit_columns.sql
V3__add_indexes.sql
V4__identity_columns.sql
V5__soft_delete.sql
V6__add_audit_logs_table.sql
```

- `V` prefix = versioned migration (runs once).
- `R` prefix = repeatable migration (re-runs when the file changes).
- `__` (double underscore) separates version from description.
- Versions are numeric (1, 2, 3) or dotted (1.1, 1.2, 2.0).

## Example migration

```sql
-- V1__create_baseline.sql
CREATE TABLE roles (
    role_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name VARCHAR2(50) NOT NULL UNIQUE
);

CREATE TABLE departments (
    department_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR2(100) NOT NULL UNIQUE,
    location VARCHAR2(200),
    created_at TIMESTAMP WITH LOCAL TIME ZONE DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH LOCAL TIME ZONE,
    deleted_at TIMESTAMP WITH LOCAL TIME ZONE
);

CREATE TABLE interns (
    intern_id NUMBER(10) GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100) NOT NULL,
    age NUMBER(3),
    email VARCHAR2(100) NOT NULL UNIQUE,
    department_id NUMBER(10) NOT NULL,
    theme_id NUMBER(10),
    status VARCHAR2(20) DEFAULT 'Pending' NOT NULL,
    created_at TIMESTAMP WITH LOCAL TIME ZONE DEFAULT SYSTIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH LOCAL TIME ZONE,
    deleted_at TIMESTAMP WITH LOCAL TIME ZONE,
    CONSTRAINT fk_interns_dept FOREIGN KEY (department_id) REFERENCES departments(department_id),
    CONSTRAINT fk_interns_theme FOREIGN KEY (theme_id) REFERENCES themes(theme_id),
    CONSTRAINT chk_intern_status CHECK (status IN ('Pending', 'Accepted', 'Rejected'))
);

CREATE INDEX idx_interns_theme ON interns(theme_id);
CREATE INDEX idx_interns_dept ON interns(department_id);
CREATE INDEX idx_interns_status ON interns(status);
```

## Spring Boot integration

Add `flyway-core` to your dependencies. Spring Boot auto-runs Flyway on startup:

```xml
<dependency>
    <groupId>org.flywaydb</groupId>
    <artifactId>flyway-core</artifactId>
</dependency>
```

Configure in `application.yml`:
```yaml
spring:
  flyway:
    enabled: true
    locations: classpath:db/migration
    baseline-on-migrate: true
```

## Why Flyway (vs. manual SQL)

- **Versioning** — every change is tracked.
- **Reproducibility** — any environment can be set up from scratch.
- **Order** — migrations apply in order.
- **History** — `flyway_schema_history` shows what was applied when.
- **CI/CD** — migrations run automatically on deploy.

## Project Connection

The project has two conflicting SQL files with no versioning. The fix: Flyway migrations replacing both files.

## Further reading

- Flyway documentation (flywaydb.org).
