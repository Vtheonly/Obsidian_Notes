# Updatable Views and Check Options

A View is a saved query that acts like a virtual table. While reading from views (`SELECT`) is straightforward, writing to them (`INSERT`, `UPDATE`, `DELETE`) involves strict rules. This note covers when a view is updatable, what can go wrong, and how the `WITH CHECK OPTION` clause prevents one of the most confusing bugs in view-based access control.

## When is a View Updatable?

A view is only considered "Updatable" (meaning you can manipulate data through it, and the DBMS will pass those changes down to the underlying physical table) if it maintains a **1-to-1 relationship** with the rows of the base table. If each row of the view maps to exactly one row of the base table, the DBMS can unambiguously translate any `INSERT`, `UPDATE`, or `DELETE` on the view into the corresponding operation on the base table.

A view is **STRICTLY NOT UPDATABLE** if its defining query contains any of the following:

- **`GROUP BY` or `HAVING`** — The virtual row represents multiple physical rows. The DB doesn't know which physical row to update.
- **Aggregate functions** like `SUM()`, `MAX()`, `COUNT()`, `AVG()` — Same problem: changing `SUM(Salary)` to 5000 is ambiguous.
- **`DISTINCT`** — Removes duplicates, breaking the 1-to-1 mapping.
- **`UNION` or `UNION ALL`** — Combines multiple row sources; ambiguous which underlying row to update.
- **Most `JOIN`s** — Some DBMSs allow updates on certain join views if the modification only affects one side of the join, but generally, complex joins block updates.

**Reasoning:** If a view shows `SUM(Salary)`, and you try to change that sum to 5000, the database doesn't know which specific employee rows to update to achieve that total. Therefore, it is ambiguous and forbidden.

| Defining query contains... | Updatable? | Why |
|----------------------------|------------|-----|
| Single table, simple `WHERE` | ✅ YES | 1-to-1 mapping preserved |
| `GROUP BY` / `HAVING` | ❌ NO | One virtual row ↔ many physical rows |
| Aggregates (`SUM`, `COUNT`, etc.) | ❌ NO | Aggregate is not reversible |
| `DISTINCT` | ❌ NO | Duplicate rows collapsed; mapping lost |
| `UNION` / `UNION ALL` | ❌ NO | Row source ambiguous |
| Single-table computed column (`a + b AS c`) | ⚠️ Partial | Can `UPDATE` non-computed columns; not `c` |
| Simple join (one-to-one) | ⚠️ DBMS-dependent | Some allow updates to one side |

## The `WITH CHECK OPTION` Clause

If you create an updatable view that filters data, a dangerous loophole exists.

### The Problem: Phantom Inserts

Imagine a view for the Paris office:

```sql
CREATE VIEW Paris_Employees AS
SELECT id, name, city FROM Employees WHERE city = 'Paris';
```

By default, you could run this query:

```sql
INSERT INTO Paris_Employees (id, name, city) VALUES (99, 'John', 'London');
```

The database would successfully insert John into the underlying `Employees` table with the city 'London'. However, if you immediately `SELECT * FROM Paris_Employees`, John will not be there! He vanished from the perspective of the view, because his `city` value does not match the view's `WHERE` clause.

The same applies to an age-based view:

```sql
CREATE VIEW Adults AS SELECT * FROM Users WHERE age > 18;
```

Inserting a row with `age = 10` through this view would succeed without `CHECK OPTION`: the row goes into the underlying `Users` table, but immediately disappears from the view (phantom insert). This is confusing and potentially dangerous.

### The Solution

To prevent users from inserting or updating data that immediately falls outside the scope of the view, use the `WITH CHECK OPTION`:

```sql
CREATE VIEW Paris_Employees AS
SELECT id, name, city FROM Employees WHERE city = 'Paris'
WITH CHECK OPTION;
```

```sql
CREATE VIEW CLIENTS_ALGER AS
SELECT * FROM CLIENT WHERE Adresse = 'ALGER'
WITH CHECK OPTION;
```

Now, if you attempt to insert 'London' (or 'ORAN') into `Paris_Employees`, the DBMS will block it with an error: *"CHECK OPTION failed"*. The view acts as a strict security and integrity boundary.

### Effect of `WITH CHECK OPTION`

- **Effect:** The SGBD checks every `INSERT` or `UPDATE` made through the view.
- **Result:** If you try to insert `Adresse = 'ORAN'` into `CLIENTS_ALGER`, the database throws an error and rejects the operation. It enforces the view's integrity.
- **Scope:** Only applies to operations issued through the view. Direct `INSERT`/`UPDATE` on the underlying base table bypasses the check (because the view's `WHERE` clause is not in scope).

## `CHECK OPTION` vs. `CHECK` Constraint

These two are easy to confuse but are conceptually different:

| Feature | `CHECK` Constraint | `WITH CHECK OPTION` |
|---------|--------------------|--------------------|
| Defined on | A column or table | A view |
| Enforces | Domain integrity on the underlying table | That inserts/updates through the view stay visible in the view |
| Applies to | All writes to the table (direct or through any view) | Only writes issued through the view |
| Syntax | `CHECK (age >= 18)` | `... WITH CHECK OPTION` |
| Failure message | "CHECK constraint violated" | "CHECK OPTION failed" |

Use a `CHECK` constraint to enforce a business rule on a column regardless of how the data enters. Use `WITH CHECK OPTION` to keep a view's contents self-consistent when users write through the view.

## See Also

- [[01 - Views Fundamentals]] — View definition, security, simplification, and data independence
- [[08 - Data Integrity]] — The three integrity types (entity, referential, domain) that views complement
- [[03 - SQL Syntax Rules and Best Practices]] — The `CHECK` constraint (different from `CHECK OPTION`)
