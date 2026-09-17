---
tags: [concept, principles, yagni]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/12 - KISS (Keep It Simple, Stupid)]]
---

# YAGNI (You Aren't Gonna Need It)

> "You aren't gonna need it." — Kent Beck, Extreme Programming

## What it means

Don't build features "for the future." Build what you need now. The future is unpredictable, and speculative code:
- Adds complexity now.
- May never be used.
- May not fit the actual future need.
- Must be maintained and tested.

## The project's YAGNI violations

### Dead schema tables

`insertion.sql` defines 7 tables never referenced by any Java code:
- `profile`
- `function_and_menu`
- `function_and_menu_profile`
- `responsible_theme`
- `department_theme`
- `theme_intern`
- `responsible`

These were designed for a future that never arrived. They add schema noise, confuse new developers, and require maintenance (FK constraints, sample data) for zero benefit.

### Email tab (no implementation)

`intern_insertion.fxml` has an Email tab with `TextField` + `HTMLEditor` + `Button` (no `onAction`). `pom.xml` declares `javax.mail`. `README` documents an `EmailService` class. **None of it works.**

### Report tab using deprecated library

The report tab uses OpenPDF's `HTMLWorker` (deprecated since 2010) — kept around "in case we need it," but never modernized.

### `toolkit.isHashEqual`

Dead method. Never called. Speculatively written for a use case that didn't materialize.

### `DataPreprocessor.java`

Entire class is dead code — a "test harness" that was never converted to a real JUnit test.

### `worker_user_user` case in `getIdByName`

A case for a pseudo-table name (`worker_user_user`) that no controller ever passes. Speculatively written.

### Roles 2 and 3 in `setAccessLevel`

`setAccessLevel` switch handles cases 1, 2, 3, default. But `insertion.sql` only inserts roles 1, 4, 5 — no roles 2 or 3. Dead code paths.

## The fix

- Drop the 7 dead tables in a Flyway migration.
- Either implement the email feature or remove it from FXML, pom.xml, README.
- Replace `HTMLWorker` with OpenHTMLtoPDF.
- Delete `toolkit.isHashEqual`, `DataPreprocessor.java`, the `worker_user_user` case.
- Either insert roles 2 and 3 in the schema, or remove the switch cases.

## When YAGNI is wrong

- **Security** — don't say "YAGNI" to input validation or password hashing. Build it in from day one.
- **Extensibility seams** — defining an interface (even with one implementation) is sometimes worth it for testability.
- **Standards compliance** — don't say "YAGNI" to GDPR, OWASP, or accessibility.

The rule of thumb: if removing the code would clearly break something now or in a predictable future, keep it. If the code is "just in case," delete it.

## Common pitfalls

- **"This might be useful later"** — it won't be. Delete it.
- **"I'll finish this feature next week"** — you won't. Delete the half-finished stub.
- **"Let's keep the dead table in case we revive the feature"** — drop it. If you revive the feature, you'll redesign the table anyway.

## Further reading

- *Extreme Programming Explained* (Beck).
- *Clean Code* (Martin), "Dead Code" smell.
