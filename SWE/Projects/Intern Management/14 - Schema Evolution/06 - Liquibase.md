---
tags: [concept, database, migration, liquibase]
type: concept
status: complete
related:
  - [[14 - Schema Evolution/05 - Flyway]]
---

# Liquibase

## What it is

**Liquibase** is another database migration tool, alternative to Flyway. It supports XML, YAML, and JSON changesets (in addition to raw SQL).

## Differences from Flyway

| | Flyway | Liquibase |
|---|---|---|
| Migration format | SQL files | XML/YAML/JSON/SQL |
| Database portability | SQL is vendor-specific | XML changesets are vendor-neutral |
| Rollback | Manual (write undo SQL) | Automatic (Liquibase generates rollback) |
| Diff tool | No | Yes (compare two DBs) |
| Complexity | Simple | More features, more complex |

## Example changeset (YAML)

```yaml
databaseChangeLog:
  - changeSet:
      id: 1
      author: alice
      changes:
        - createTable:
            tableName: interns
            columns:
              - column:
                  name: intern_id
                  type: NUMBER(10)
                  autoIncrement: true
                  constraints:
                    primaryKey: true
              - column:
                  name: name
                  type: VARCHAR2(100)
                  constraints:
                    nullable: false
              - column:
                  name: email
                  type: VARCHAR2(100)
                  constraints:
                    unique: true
        - createIndex:
            indexName: idx_interns_email
            tableName: interns
            columns:
              - column:
                  name: email
```

## Why choose Liquibase over Flyway

- **Multi-database support** — write changesets once, deploy to Oracle, PostgreSQL, MySQL.
- **Automatic rollback** — `liquibase rollback` undoes changesets.
- **Diff tool** — `liquibase diff` compares two DBs and generates changesets.
- **Contexts** — apply different changesets in dev vs. prod.

## Why choose Flyway over Liquibase

- **Simpler** — SQL files, no XML.
- **More popular** — larger community.
- **Easier to learn** — if you know SQL, you know Flyway.

## Project Connection

Either Flyway or Liquibase would fix the project's schema management. The reviews recommend Flyway for simplicity. Choose Liquibase if you need multi-database support.

## Further reading

- Liquibase documentation (liquibase.org).
