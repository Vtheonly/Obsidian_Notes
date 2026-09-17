---
tags: [concept, database, schema, evolution]
type: concept
status: complete
---

# The Schema Evolution Problem

## The problem

Databases change over time:
- Add a column.
- Drop a column.
- Rename a table.
- Add an index.
- Change a constraint.
- Split a table.
- Merge tables.

Each change is a **migration**. Without a disciplined approach:
- Dev DB has schema v3, test has v5, prod has v4 — chaos.
- A new developer can't set up the DB.
- Rollbacks are impossible.
- Manual SQL scripts get lost.

## The solution: migration tools

Tools like **Flyway** and **Liquibase** version-control the schema:
- Each migration is a file (SQL or XML/YAML).
- Migrations are applied in order.
- A history table (`flyway_schema_history` or `DATABASECHANGELOG`) tracks applied migrations.
- The tool runs migrations automatically on app startup.

## Project Connection

The project has two conflicting SQL files (`insertion.sql`, `requstes.sql`) with no versioning, no tracking, no rollback. The `docker-compose.yml` mounts `./sql-scripts` (which doesn't exist) to `container-entrypoint-initdb.d` — neither SQL file is ever executed automatically. The schema is created manually, off-script.

The fix: Flyway migrations in `src/main/resources/db/migration/`:
- `V1__create_baseline.sql`
- `V2__add_audit_columns.sql`
- `V3__add_indexes.sql`
- `V4__identity_columns.sql`
- `V5__soft_delete.sql`

## Further reading

- *Refactoring Databases* (Ambler & Sadalage).
