---
tags: [concept, database, schema-evolution, refactoring]
type: concept
status: complete
prerequisites:
  - [[14 - Schema Evolution/05 - Flyway]]
  - [[07 - Refactoring Techniques/12 - What Is Refactoring]]
related:
  - [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
  - [[07 - Refactoring Techniques/03 - Extract Class]]
---

# Database Refactoring

## What it is

**Database refactoring** is the practice of changing a database's structure to improve its design **without changing its behavior** - the same way code refactoring changes internal structure without changing external behavior. The catalog is from Ambler & Sadalage, *Refactoring Databases* (2006).

## The catalog

### Structural refactorings

- **Rename Table** - `intern` -> `student`. Use expand-and-contract (view with old name) to keep old code working.
- **Rename Column** - `name` -> `full_name`. Same pattern.
- **Split Table** - `intern` (with contact info) -> `intern` + `intern_contact`.
- **Merge Tables** - `intern` + `intern_contact` -> `intern`.
- **Drop Column** - remove a column no longer used.
- **Drop Table** - remove a table no longer used.

### Data quality refactorings

- **Introduce Surrogate Key** - replace a natural key with an IDENTITY column.
- **Replace Natural Key with Surrogate Key** - same, explicitly.
- **Introduce Common Format** - normalize phone numbers, dates, etc.
- **Introduce Lookup Table** - replace a CHECK constraint with a lookup table (e.g., `intern_status` table).
- **Introduce Constraint** - add a NOT NULL, UNIQUE, or CHECK.

### Architectural refactorings

- **Introduce View** - wrap a query in a view.
- **Introduce Materialized View** - precompute a join.
- **Introduce Index** - add an index.
- **Introduce Partitioning** - split a table by range/list/hash.

### Method refactorings

- **Introduce Stored Procedure** - move a query into a procedure.
- **Introduce Trigger** - automate a side effect.

## The process

Every database refactoring follows the same five-step process:

1. **Verify the need** - is the current design actually causing pain?
2. **Choose the refactoring** - pick from the catalog.
3. **Deprecate the old** - mark the old structure as "going away" (comments, warnings).
4. **Apply the refactoring** - via migrations, using expand-and-contract.
5. **Clean up** - after a deprecation period, remove the old structure.

The deprecation period (step 3-5) can be weeks (for a small app) or years (for a large organization with many consumers). Don't rush it.

## The "transition period"

For a rename (`intern` -> `student`):

```sql
-- Phase 1: rename, add a synonym with the old name
RENAME intern TO student;
CREATE SYNONYM intern FOR student;   -- old queries still work

-- Phase 2 (after deprecation period): drop the synonym
DROP SYNONYM intern;
```

The synonym is a "transition" structure that keeps old code working while new code migrates.

## Database smells (when to refactor)

- **Multi-purpose column** - `intern.contact` holds email or phone or both. Split it.
- **Multi-purpose table** - `intern` holds interns and applicants. Split it.
- **Repeated data** - `department_name` copied into every `intern` row. Normalize.
- **Missing constraints** - data that should be NOT NULL is nullable. Add the constraint.
- **Magic values** - `is_accepted = 'hold'` (not in the CHECK). Add the value or fix the code.
- **Dead tables** - tables with no rows and no references. Drop them.

## Project Connection

The project is a **catalog of database smells**:

- Two conflicting schemas (`insertion.sql` vs `requstes.sql`) - one should be dropped.
- Dead tables (`profile`, `function_and_menu`, etc.) - should be dropped.
- `theme.responsible` is a string column holding a person's name - should be a FK to `worker_user`.
- `is_accepted = 'hold'` in Java vs. `CHECK (is_accepted IN ('Accepted','Rejected','Pending'))` in schema - the constraint is right, the code is wrong.
- No indexes on FKs - should be added.
- No audit columns - should be added.
- Hard delete - should be soft delete.

The redesign proposes a sequence of database refactorings:

- **Drop the dead tables** (V1.1).
- **Introduce Surrogate Key** on `intern` (already NUMBER - just switch to IDENTITY).
- **Introduce Constraint** (`is_accepted` CHECK - already there).
- **Introduce Index** on every FK.
- **Introduce Column** for audit columns.
- **Introduce View** for the dashboard's pre-joined data (or a materialized view).
- **Drop Table** the dead `requstes.sql` schema.

Each is a migration, applied in order, with expand-and-contract where needed.

## Common pitfalls

- Refactoring without tests - you don't know if you broke the behavior. Use characterization tests (see [[07 - Refactoring Techniques/02 - Characterization Tests]]) before refactoring.
- Refactoring without a deprecation period - consumers break unexpectedly.
- Refactoring and adding features in the same migration - mixes two concerns; one failure rolls back both.
- Big-bang refactorings - "let's redesign the whole schema in one migration." Always split into small, independently-deployable changes.

## Further reading

- Ambler & Sadalage, *Refactoring Databases* (2006).
- [[07 - Refactoring Techniques/12 - What Is Refactoring]]
- [[14 - Schema Evolution/07 - Migration Strategies - Expand and Contract]]
