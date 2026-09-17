---
tags: [concept, database, migration, compatibility]
type: concept
status: complete
related:
  - [[14 - Schema Evolution/05 - Flyway]]
---

# Backward and Forward Compatibility

## The problem

In a zero-downtime deployment, the new version of the app must work with the old DB, and the old version must work with the new DB (during rollout).

## Backward compatible (new app, old DB)

The new app must handle the old schema. Techniques:
- **Don't remove columns the old version uses.**
- **Don't add NOT NULL columns without a default.**
- **Don't rename columns** (use a view with the old name).

## Forward compatible (old app, new DB)

The old app must handle the new schema. Techniques:
- **New columns must be nullable or have a default.**
- **New tables must not break old queries.**
- **Old code must ignore unknown columns** (it usually does — `SELECT *` includes them, typed queries ignore them).

## Multi-step migrations

For breaking changes, do them in stages:

### Stage 1: Add the new column (nullable)
```sql
ALTER TABLE interns ADD COLUMN email_normalized VARCHAR2(100);
```
Both old and new app work. New app populates `email_normalized`; old app ignores it.

### Stage 2: Backfill
```sql
UPDATE interns SET email_normalized = LOWER(email) WHERE email_normalized IS NULL;
```
Run in the background. No app changes.

### Stage 3: Add NOT NULL constraint
```sql
ALTER TABLE interns MODIFY email_normalized NOT NULL;
```
Now the column is guaranteed populated. New app can rely on it.

### Stage 4: Deploy new app code that uses `email_normalized`
Old app is retired.

### Stage 5: Drop the old column (optional, later)
```sql
ALTER TABLE interns DROP COLUMN email;
```
Only after confirming no code uses it.

## Project Connection

The project isn't deployed (it's a desktop app), so zero-downtime migrations are less critical. But the principle applies: if you ever need to migrate the schema without breaking the app, do it in stages.

## Further reading

- *Refactoring Databases* (Ambler & Sadalage).
- Stripe's "Expanded" migration pattern (stripe.com blog).
