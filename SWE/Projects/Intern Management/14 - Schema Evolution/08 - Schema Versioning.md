---
tags: [concept, database, schema-evolution, versioning]
type: concept
status: complete
prerequisites:
  - [[14 - Schema Evolution/05 - Flyway]]
related:
  - [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
  - [[14 - Schema Evolution/04 - Database Refactoring]]
---

# Schema Versioning

## What it is

**Schema versioning** is the practice of tracking the schema's state with explicit version numbers, so that any database instance can be identified as "at version N" and brought to "version N+1" with a known, ordered set of changes.

Without schema versioning:

- "Is this dev database up to date?" - you don't know.
- "Did the prod database get last week's schema change?" - you don't know.
- "Two developers added columns to the same table - which one wins?" - chaos.

With schema versioning:

- Every database has a version (stored in a history table).
- Every change is a versioned migration (in source control).
- "Bring this database to version 47" is a one-command operation.

## The version as a sequence of migrations

The schema version is the **highest applied migration version**. If migrations V1, V2, V3 are applied, the database is "at version 3." V4 is pending.

This means the version is **derived**, not declared. You don't write "this database is at version 3" anywhere - you look at the history table and compute it.

## The history table

Both Flyway (`flyway_schema_history`) and Liquibase (`DATABASECHANGELOG`) maintain a history table:

```sql
SELECT version, description, installed_on
FROM   flyway_schema_history
ORDER  BY installed_rank;
```

This is the source of truth for "where is this database?" Every environment (dev, test, staging, prod) has its own history table.

## Versioning strategies

### Sequential integers (Flyway default)

`V1, V2, V3, ...` - simple, unambiguous.

### Semver (some teams)

`V1.0.0, V1.0.1, V1.1.0, V2.0.0` - maps to release versions. More meaningful to humans, but Flyway sorts lexically (`V1.10.0` < `V1.9.0` - wrong!) unless you zero-pad (`V1.09.0`).

### Timestamps (some teams)

`V20240315_120000` - encodes when the migration was created. Avoids collisions when two developers create migrations simultaneously. Verbose.

Pick one and stick with it. Sequential integers are the safest.

## Branching and merging

When two developers branch and each adds a migration:

- Dev A: `V15__add_email_column.sql`
- Dev B: `V15__add_phone_column.sql`

Both used `V15`. On merge, one has to renumber. This is the most common schema-versioning pain.

Mitigations:

- Use timestamps instead of integers (avoids collisions).
- Communicate: a shared "next version" counter (a wiki page, a Slack channel).
- Merge frequently; renumber on merge.

## Why it matters

Schema versioning is what makes **continuous delivery** possible for databases. Without it, schema changes are manual, error-prone, and untracked - the database becomes a hand-maintained artifact that drifts from the code. With it, the schema is code: versioned, tested, deployed.

## Project Connection

The project has **no schema versioning**. The schema is whatever's in `insertion.sql` (or `requstes.sql`, depending on which the developer ran). There's no record of which version is applied to which database. There's no way to incrementally evolve - any change requires re-running the entire script, which drops and recreates all tables (losing data).

The reviews' redesign proposes Flyway with sequential versions:

```
V1__create_baseline.sql
V2__add_audit_columns.sql
V3__add_indexes_on_fks.sql
...
V10__sample_data_with_argon2.sql
```

Each migration is a small, focused change. The history table records what's applied. The schema is now code.

## Common pitfalls

- Editing an applied migration - changes the checksum, breaks the history. Add a new migration instead.
- Two migrations with the same version number on different branches - collision on merge.
- Letting the schema drift between environments - dev has V1-V10, prod has V1-V8 because someone forgot to deploy. Automate migrations in CI/CD.
- Treating the history table as editable - it's not. If a migration failed mid-way, you have to manually clean up the partial state and remove the failed row.

## Further reading

- [[14 - Schema Evolution/05 - Flyway]]
- [[14 - Schema Evolution/06 - Liquibase]]
- [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
