# Standard Views, Updatability & Materialized Views

This note integrates **Chapter 2 Part I (Slides 4–15)**, **TP 2 (Exercises 1–3, Ex 12 Task 4, Part IV Q10–11)**, **TD 2 (Exercises 1* & 2*)**, and access-control / simplification patterns from the course (`GRANT`/`REVOKE`, "Max of Sums", and Relational Division views).

---

## 1. Standard Views (Virtual Relations)

A **standard view** is a **virtual relation defined from a named SQL `SELECT` query** stored in the database catalog. Unlike a base table (or a materialized view), a standard view **does not store a physical copy of its rows**. Whenever you query the view, the DBMS runs its defining `SELECT` query in real time against the current state of the underlying base tables.

### Five Core Purposes of Views (Ch 2 Slide 6)
1. **Hide certain columns / Confidentiality:** For example, an academic coordinator needs to consult teachers without seeing their `salary` (Ch 2 Slide 5).
2. **Simplify queries:** Encapsulate repeated multi-table joins (`teacher_department_view`) or nested aggregates behind a single virtual table.
3. **Present data in an appropriate form:** Rename, concatenate, format, or handle `NULL`s (`COALESCE(work_email, personal_email, 'none')`).
4. **Reuse and layer query logic:** Build nested views on top of existing views (TD 2 Ex 1.3).
5. **Provide logical data independence:** If underlying tables are restructured (e.g., splitting `full_name` into `first_name` and `last_name`), updating the view keeps client applications working unchanged.

### General Syntax & Management (TP 2 Part II.1 & Ch 2 Slides 7–10)
```sql
CREATE OR REPLACE VIEW view_name [(alias_col1, alias_col2, ...)] AS
SELECT column1, column2
FROM table_name
WHERE condition;

DROP VIEW view_name;
```
- **`CREATE OR REPLACE VIEW`** updates an existing view definition in place without dropping its `GRANT` permissions (if column types/order stay compatible).
- **`DROP VIEW`** removes **only the view definition** from the data dictionary—never the underlying base-table data.
- **Restriction on `ORDER BY`:** Standard SQL generally forbids `ORDER BY` inside `CREATE VIEW` definitions because a relation is conceptually unordered; apply `ORDER BY` when *querying* the view (`SELECT * FROM teacher_view ORDER BY teacher_id;`).

---

## 2. Worked View Exercises: Chapter 2, TP 2 (Ex 1) & TD 2 (Ex 1*)

### A. Column-Hiding & Live Reflection (Ch 2 Slide 7 & 10, TP 2 Ex 1 Tasks 1 & 3, TD 2 Ex 1.1)
```sql
-- TP 2 Ex 1 Task 1 / Ch 2 Slide 7: teacher_view (TD 2 Ex 1.1 names it teacher_public_view)
CREATE OR REPLACE VIEW teacher_public_view AS
SELECT teacher_id, last_name, first_name, department_id
FROM teacher;

-- TD 2 Ex 1.1: Retrieve teachers whose first name is Ahmed
SELECT * FROM teacher_public_view WHERE first_name = 'Ahmed';
```
**Key conceptual answers (TP 2 Ex 1 Tasks 1 & 3):**
- *Which columns are hidden?* `salary` (and any column omitted from the view's `SELECT` list).
- *Is `salary` still stored in `teacher`?* Yes—the base table is untouched.
- *Does the view store an independent copy of rows?* No—it stores only the query definition.
- *What happens if a teacher's `first_name` changes in `teacher`?* Subsequent queries against the view show the updated `first_name` immediately.
- *Reversible transaction test (TP 2 Ex 1 Task 3):*
  ```sql
  BEGIN;
  UPDATE teacher SET salary = 80000 WHERE teacher_id = 101;
  SELECT * FROM teacher WHERE teacher_id = 101;       -- shows salary = 80000
  SELECT * FROM teacher_view WHERE teacher_id = 101;  -- columns remain unchanged (no salary column)
  ROLLBACK;
  ```
  Updating `salary` changes the base row, not the view's column schema!

### B. Multi-Table & Nested Views (Ch 2 Slides 8–9, TP 2 Ex 1 Task 2 & Ex 12, TD 2 Ex 1.2–1.3, 1.5)
> [!NOTE] Source Naming Difference
> In **TP 2 Ex 1 Task 2** (and Ch 2 Slide 8), `teacher_department_view` omits `salary`. In **TD 2 Ex 1.2–1.3**, `teacher_department_view` **includes `salary`** so that the nested `computer_science_high_salary_view` can filter `salary >= 70000`! Also note Ch 2 Slide 9 defines `computer_science_teacher_view` over `teacher_department_view`, whereas Slide 11 reuses the same name directly on `teacher` with `WITH CHECK OPTION`. TP 2 resolves that collision by naming the updatable view `department_1_teachers`.

```sql
-- TD 2 Ex 1.2: Multi-table join view (includes salary)
CREATE OR REPLACE VIEW teacher_department_view AS
SELECT t.teacher_id, t.last_name, t.first_name, t.salary, d.department_name
FROM teacher t
INNER JOIN department d ON t.department_id = d.department_id;

-- TD 2 Ex 1.3: Nested View 1 (reuse & layer query logic)
CREATE OR REPLACE VIEW computer_science_teacher_view AS
SELECT teacher_id, last_name, first_name, salary
FROM teacher_department_view
WHERE department_name = 'Informatique';

-- TD 2 Ex 1.3: Nested View 2 built on the first view
CREATE OR REPLACE VIEW computer_science_high_salary_view AS
SELECT teacher_id, last_name, first_name, salary
FROM computer_science_teacher_view
WHERE salary >= 70000;

-- TD 2 Ex 1.5: Drop the high-salary view
DROP VIEW computer_science_high_salary_view;

-- TP 2 Ex 12 (Task 4): View showing teacher IDs, names, and department names without salaries
CREATE OR REPLACE VIEW teacher_department_no_salary AS
SELECT t.teacher_id, t.last_name, t.first_name, d.department_name
FROM teacher AS t
JOIN department AS d ON d.department_id = t.department_id;
```
*(Deeply nested views promote modularity and reuse, though excessive nesting can make query plans harder to inspect.)*

---

## 3. Views for Access Control (DCL) & Query Simplification (Archived BDA Patterns)

### A. Security Matrix with `GRANT` / `REVOKE`
Views combined with DCL (`GRANT`, `REVOKE`) enforce **column-level**, **row-level**, and **context-aware** security without copying tables:
- **Column-level:** `CREATE VIEW V_Public_Emp AS SELECT Name, Function, Email FROM Employees; GRANT SELECT ON V_Public_Emp TO U1;` (U1 cannot access salaries).
- **Row-level:** `CREATE VIEW CLIENTS_ALGER AS SELECT * FROM CLIENT WHERE Adresse = 'ALGER';`.
- **Context-aware (Oracle legacy example):** `CREATE VIEW V_Secure AS SELECT * FROM T WHERE userenv('TERMINAL') = 'T100';`.
- **Solved Multi-Table Access Matrix:** Given `T1(a1..a5)` and `T2(b1..b3)`:
  - User U1 sees `(a1, a2)` where `COND`: `CREATE VIEW V1 AS SELECT a1, a2 FROM T1 WHERE COND; GRANT SELECT ON V1 TO U1;`
  - User U2 sees `(a4, a5)`: `CREATE VIEW V2 AS SELECT a4, a5 FROM T1; GRANT SELECT ON V2 TO U2;`
  - User U3 needs `(a4, a5, b1, b2)` joined on `a4 = b1`: build `V3` directly on top of `V2` and `T2` (`CREATE VIEW V3 AS SELECT V2.a4, V2.a5, T2.b1, T2.b2 FROM V2, T2 WHERE V2.a4 = T2.b1; GRANT SELECT ON V3 TO U3;`).

### B. Simplification Patterns: "Max of Sums" & Relational Division
Standard SQL forbids nested aggregates like `MAX(SUM(km))`. Views solve this cleanly in two steps:
1. **"Max of Sums" (`Chef de Service` Mission Mileage):**
   ```sql
   CREATE VIEW R11 AS
   SELECT chef.SRV_Libelle, chef.EMP_Num, chef.EMP_Nom,
          SUM(m.MIS_KlmRetour - m.MIS_KlmDepart) AS NbKil
   FROM chef, MISSION m WHERE chef.EMP_Num = m.EMP_Num
   GROUP BY chef.SRV_Libelle, chef.EMP_Num, chef.EMP_Nom;

   SELECT * FROM R11 WHERE NbKil = (SELECT MAX(NbKil) FROM R11);
   ```
   *(Same pattern for top turnover store last month using view `V21(mag_num, Chiffre_Affaire)`.)*
2. **Relational Division via Intermediate View (`V20`):** Articles sold by ALL shops:
   ```sql
   CREATE VIEW V20 AS SELECT DISTINCT art_num, mag_num FROM VENTES;
   SELECT V.art_num, A.art_nom FROM V20 V, ARTICLES A
   WHERE V.art_num = A.art_num
   GROUP BY V.art_num, A.art_nom
   HAVING COUNT(*) = (SELECT COUNT(*) FROM MAGASINS);
   ```

---

## 4. Updatable Views & `WITH CHECK OPTION` (Ch 2 Slides 11–12, TP 2 Ex 3, TD 2 Ex 1.4)

### When Is a View Automatically Updatable?
A view allows `INSERT`, `UPDATE`, and `DELETE` through it **only when every row in the view maps 1-to-1 to a single row in one base table**. A view is **NOT automatically updatable** if its query uses:
- `GROUP BY` or `HAVING` (1 virtual row maps to many physical rows).
- Aggregate functions (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`).
- `DISTINCT` (collapses duplicates, destroying 1-to-1 identity).
- Set operations (`UNION`, `UNION ALL`, `INTERSECT`, `EXCEPT`).
- Multi-table `JOIN`s (generally not automatically updatable in PostgreSQL—to make a join view writable, attach an **`INSTEAD OF` trigger**; see [[01 - Triggers, Automatic Auditing & Constraints vs Triggers]]).

### The Phantom Write Problem & `WITH [LOCAL] CHECK OPTION`
Suppose you create a filtered view without `CHECK OPTION`:
`CREATE VIEW Paris_Employees AS SELECT id, name, city FROM Employees WHERE city = 'Paris';` (or `CREATE VIEW Adults AS SELECT * FROM Users WHERE age > 18;`).
Inserting `(99, 'John', 'London')` through `Paris_Employees` (or `age = 10` through `Adults`) succeeds on the base table, yet John **immediately vanishes** from the view!

Adding **`WITH CHECK OPTION`** (or PostgreSQL's **`WITH LOCAL CHECK OPTION`**) blocks any `INSERT` or `UPDATE` *made through the view* whose resulting row would fail the view's `WHERE` condition:

```sql
-- TP 2 Ex 3 / Ch 2 Slide 11 / TD 2 Ex 1.4
CREATE OR REPLACE VIEW department_1_teachers AS
SELECT teacher_id, last_name, first_name, salary, department_id
FROM teacher
WHERE department_id = 1
WITH LOCAL CHECK OPTION;

-- SUCCEEDS: teacher 101 stays in department 1
UPDATE department_1_teachers SET salary = 79000 WHERE teacher_id = 101;

-- REJECTED ("new row violates check option for view"): moves row outside department_id = 1
UPDATE department_1_teachers SET department_id = 2 WHERE teacher_id = 101;
```

> [!WARNING] What `WITH CHECK OPTION` Does and Does NOT Guarantee (TP 2 Part IV Q11)
> - **Guarantees:** Any `INSERT` or `UPDATE` executed **through the view** must leave the row satisfying the view's `WHERE` condition (`department_id = 1`).
> - **Does NOT guarantee:** It **never blocks** direct `INSERT`/`UPDATE` statements executed on the underlying `teacher` base table (`UPDATE teacher SET department_id = 2 WHERE teacher_id = 101;` succeeds!).
> - **`LOCAL` vs. `CASCADED`:** `WITH LOCAL CHECK OPTION` validates only the current view's `WHERE` condition; `WITH CASCADED CHECK OPTION` (standard default for `WITH CHECK OPTION` in PostgreSQL) also checks conditions of any underlying nested views.
> - **Different from `CHECK` constraint:** A table `CHECK` constraint enforces domain integrity on *all* writes to the table regardless of path; `WITH CHECK OPTION` enforces scope consistency *only* for writes issued through the view.

---

## 5. Materialized Views (Ch 2 Slides 13–15, TP 2 Ex 2, TD 2 Ex 2*)

A **materialized view** executes its query upon creation and **physically stores the resulting rows on disk**. It is designed for expensive analytical or aggregation reports executed frequently where slightly stale data is acceptable.

```sql
-- TP 2 Ex 2 (mv_department_salary) / TD 2 Ex 2* (department_average_salary)
CREATE MATERIALIZED VIEW department_average_salary AS
SELECT department_id, AVG(salary) AS average_salary
FROM teacher
GROUP BY department_id;

-- Query stored snapshot (fast—no re-aggregation of teacher!)
SELECT * FROM department_average_salary ORDER BY department_id;

-- Observe staleness & manual refresh workflow (TP 2 Ex 2)
UPDATE teacher SET salary = 78000 WHERE teacher_id = 101;
SELECT * FROM department_average_salary ORDER BY department_id; -- STILL shows old average!

REFRESH MATERIALIZED VIEW department_average_salary;
SELECT * FROM department_average_salary ORDER BY department_id; -- Now shows updated average

-- Restore original salary and refresh again so stored snapshot matches restored data
UPDATE teacher SET salary = 75000 WHERE teacher_id = 101;
REFRESH MATERIALIZED VIEW department_average_salary;

-- Drop if starting fresh
DROP MATERIALIZED VIEW department_average_salary;
```
*(Note: Grouping directly on `teacher` omits department 5 `Chimie` because it has 0 rows in `teacher`; join from `department LEFT JOIN teacher` if all departments should be materialized.)*

### Regular View vs. Materialized View Comparison (Ch 2 Slide 15, TP 2 Part IV Q10, TD 2 Ex 2.5–2.6)

| Dimension | Regular (Standard) View | Materialized View |
| :--- | :--- | :--- |
| **Data Storage** | Stores **only the SQL query definition** (logical result; 0 data storage) | **Physically stores query result rows** on disk (can be indexed) |
| **Query Execution** | Re-runs its defining query against base tables on every `SELECT` | Reads precomputed rows directly from disk (very fast for heavy reports) |
| **Result Freshness** | **Always up-to-date** (current data) | **May become outdated/stale** after source tables change |
| **Refresh Required?** | **No `REFRESH` required** | **`REFRESH MATERIALIZED VIEW` required** to recompute stored data |
| **Advantage / Limitation** | Advantage: zero redundancy & always live; Limitation: slow for repeated heavy aggregations | **Advantage (TD 2 Ex 2.6):** Dramatic speedup on expensive salary statistics/reports; **Limitation:** consumes storage and serves stale results until explicitly refreshed |
