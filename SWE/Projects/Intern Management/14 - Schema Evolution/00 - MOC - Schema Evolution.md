---
tags: [moc, database, schema, migration]
type: moc
status: complete
---

# MOC — Schema Evolution

## Notes (read in order)

1. [[14 - Schema Evolution/13 - The Schema Evolution Problem]] — why schemas change.
2. [[14 - Schema Evolution/09 - Soft Delete Pattern]] — `deleted_at` instead of DELETE.
3. [[14 - Schema Evolution/01 - Audit Columns]] — `created_at`, `updated_at`, `created_by`, `updated_by`.
4. [[14 - Schema Evolution/11 - Temporal Tables (SCD Type 2)]] — tracking history.
5. [[14 - Schema Evolution/05 - Flyway]] — versioned SQL migrations.
6. [[14 - Schema Evolution/06 - Liquibase]] — XML/YAML/JSON changesets.
7. [[14 - Schema Evolution/03 - Backward and Forward Compatibility]] — zero-downtime migrations.
