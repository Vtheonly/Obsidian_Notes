---
tags: [case-study, code-walkthrough, sql, schema]
type: case-study
status: complete
---

# SQL Scripts

## Overview

3 SQL files, 455 lines total. Two conflicting schemas; the Java code only matches one.

## insertion.sql (283 lines) — main schema

Defines: `role`, `department`, `worker_user`, `theme`, `intern`, plus dead tables `profile`, `responsible`, `function_and_menu`, `function_and_menu_profile`, `department_theme`, `responsible_theme`, `theme_intern`.

Uses:
- PL/SQL anonymous block with `BEGIN...EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; END IF;` to drop tables idempotently.
- `EXECUTE IMMEDIATE 'DROP TABLE ...'`.
- `NUMBER(10)` for IDs.
- `VARCHAR2(n CHAR)` for strings (character semantics — correct).
- `DATE` for `start_date`.
- `DEFAULT SYSDATE` / `DEFAULT 'Pending'`.
- `CHECK (is_accepted IN ('Accepted','Rejected','Pending'))` — but Java inserts `'hold'` (lowercase, violates constraint).
- `FOREIGN KEY ... ON DELETE SET NULL/CASCADE`.
- `COMMENT ON TABLE`.
- Sample `INSERT`s with `TO_DATE('YYYY-MM-DD','YYYY-MM-DD')`.
- Roles: 1=User, 4=Admin, 5=Chief. **No roles 2 or 3** — so the secretary sub-levels 2/3 in `setAccessLevel` can never occur with sample data.
- **Sample users store plaintext `'rootroot'` as `password_hash`** — so Java-hashed `'rootroot'` won't match, and sample users can't log in.

## requstes.sql (114 lines) — alternative/legacy schema (note: filename typo "requstes" should be "requests")

Defines a *different* schema:
- `department_id VARCHAR2(255)` (vs `NUMBER(10)`).
- Table `worker` (vs `worker_user`) with `id VARCHAR2(255)` and `profile_id` (no `role_id`).
- `intern` with **composite PK `(group_id, id)`**, `end_date`, `inserted_by`, `responsible_id`.
- `theme.theme_id VARCHAR2(255)`, no `responsible` column.
- No `role` table.
- No `CHECK` constraints, no `ON DELETE` rules, no sample data.

**This schema is NOT what the Java code uses.** Java uses `worker_user` with `NUMBER` IDs — matching `insertion.sql`.

## DROP.sql (58 lines)

PL/SQL script that drops all tables. Uses:
- `TYPE table_list_t IS TABLE OF VARCHAR2(128);` (PL/SQL collection).
- `FOR i IN 1..l_tables.COUNT LOOP`.
- `SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = ...`.
- Dynamic `EXECUTE IMMEDIATE 'DROP TABLE "..." CASCADE CONSTRAINTS'`.
- `DBMS_OUTPUT.PUT_LINE`.
- `EXCEPTION WHEN OTHERS` with `SQLERRM`.
- Lists both `WORKER` (legacy) and `ROLE` tables.

## Conflicts between the two schemas

| Aspect | `insertion.sql` | `requstes.sql` |
|---|---|---|
| `department_id` type | `NUMBER(10)` | `VARCHAR2(255)` |
| `theme_id` type | `NUMBER(10)` | `VARCHAR2(255)` |
| User table name | `worker_user` | `worker` |
| User PK | `user_id NUMBER` | `id VARCHAR2` |
| `role_id` column | Yes (FK→role) | No (uses `profile_id`) |
| `profile_id` column | No | Yes |
| `intern` PK | `intern_id NUMBER` | composite `(group_id, id)` |
| `intern.end_date`/`inserted_by`/`responsible_id`/`group_id` | No | Yes |
| `theme.responsible` column | Yes (`VARCHAR2(100)`) | No |
| `is_accepted` column | Yes + `CHECK` constraint | No |
| `role` table | Yes | No |
| `CHECK` constraints | Yes | None |
| `ON DELETE` rules | `CASCADE`/`SET NULL` | None |
| Sample data | Yes | None |

## What's wrong

1. **Two conflicting schemas** — anyone trying to set up the project doesn't know which to apply.
2. **`DROP.sql` drops both `worker` and `worker_user`** — tries to drop a table that may or may not exist.
3. **`docker-compose.yml` mounts `./sql-scripts` (which doesn't exist)** — neither SQL file is ever executed automatically. The schema is created manually, off-script.
4. **README doesn't mention which SQL file to run.**
5. **Java references `intern.end_date` and `intern.inserted_by`** (lines 189–192 of `insertionInternController`) which exist only in `requstes.sql` → SQL errors.
6. **Java's `"IS_ACCEPTED"` (uppercase quoted)** resolves to Oracle's uppercase storage of unquoted `is_accepted` → works.
7. **Java's `worker_user.age`** (referenced in `insertionUserController` field `age`) exists in **neither** schema → SQL error.
8. **Sample data stores plaintext `'rootroot'` as `password_hash`** — Java-hashed `'rootroot'` won't match, so sample users can't log in.
9. **Java inserts `'hold'` for `is_accepted`** — violates the `CHECK` constraint allowing only `'Accepted','Rejected','Pending'` → INSERT fails.
10. **No migration tool** — manual SQL files, no versioning, no rollback. See [[14 - Schema Evolution/05 - Flyway]].

## The fix

- Pick one schema (`insertion.sql` is closer).
- Replace with a versioned migration tool (Flyway or Liquibase).
- Migration files in `src/main/resources/db/migration/`:
  - `V1__create_baseline.sql`
  - `V2__add_audit_columns.sql`
  - `V3__add_indexes.sql`
  - `V4__identity_columns.sql`
  - `V5__soft_delete.sql`
- Flyway applies them in order on app startup and tracks applied versions in `flyway_schema_history`.
- Delete `requstes.sql` and `DROP.sql`.
- Fix the sample data: store Argon2id hashes, not plaintext.
- Fix the Java code: insert `'Pending'` not `'hold'`.

See [[14 - Schema Evolution/00 - MOC - Schema Evolution]].
