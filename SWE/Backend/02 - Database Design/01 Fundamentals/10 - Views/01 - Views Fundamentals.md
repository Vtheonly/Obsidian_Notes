# Views Fundamentals

A **View** (sometimes called a *virtual table* or *saved query*) is a database object that presents a customized subset or transformation of the data stored in one or more underlying base tables. Unlike a standard table, a view **does not store data physically** (with the exception of Materialized Views, which are not covered here). It is stored in the Data Dictionary essentially as a saved `SELECT` query. When you query a view, the RDBMS executes the underlying query in real-time and returns the current results.

Views serve three main objectives in database design:

1. **Security (Confidentiality):** Restrict access to specific rows (e.g., only employees in Algiers) or specific columns (e.g., hide salaries).
2. **Simplification:** Hide complex joins or calculations. The user queries a simple view instead of writing a 20-line SQL statement.
3. **Data Independence:** If the structure of the base tables changes, you can modify the view definition so the user application doesn't break.

## Syntax

```sql
CREATE VIEW <view_name> [(alias_col1, alias_col2...)]
AS <SELECT_query>
[WITH CHECK OPTION];
```

> [!WARNING] Restrictions on Creation
> The sub-query defining the view generally cannot contain an `ORDER BY` clause (sorting is done when *querying* the view, not creating it). The RDBMS wants to preserve its freedom to return rows in any order that is efficient for the underlying execution plan.

Example:

```sql
CREATE VIEW View_Name AS
SELECT col1, col2
FROM table
WHERE condition;
```

## Views for Security (Access Control)

This is the most critical practical use of views. A view allows you to give a user a "window" into the data without giving them the keys to the whole house. Combined with the `GRANT` statement, views provide fine-grained row-level and column-level access control.

### Column-Level Security (Vertical Filtering)

**Scenario:** You want User U1 to see Employee Names, but **not** their salaries.

**Solution:**

```sql
CREATE VIEW V_Public_Emp AS
SELECT Name, Function, Email -- Salary is omitted
FROM Employees;

GRANT SELECT ON V_Public_Emp TO U1;
```

*Result:* If U1 tries `SELECT * FROM Employees`, access is denied. If U1 does `SELECT * FROM V_Public_Emp`, they see the allowed data.

### Row-Level Security (Horizontal Filtering)

**Scenario:** Restrict access to the table `CLIENT` to only show clients living in 'ALGER'.

```sql
CREATE VIEW CLIENTS_ALGER AS
SELECT *
FROM CLIENT
WHERE Adresse = 'ALGER';
```

### Context-Aware Views

A view can restrict data based on the environment in which it is queried (e.g., the terminal ID, the current user, or the current time). This is a powerful technique for building context-aware security directly into the database.

```sql
-- View that only shows data if accessed from Terminal 'T100'
CREATE VIEW V_Secure AS
SELECT *
FROM T
WHERE userenv('TERMINAL') = 'T100';
```

## Views for Simplification

Views can encapsulate complex joins, calculations, and subqueries so that downstream users can `SELECT * FROM simple_view` instead of writing the underlying query themselves. This is especially useful when:

- A query is reused across many reports or applications.
- The underlying schema is complex (5+ tables joined).
- The query involves business logic that should be defined once and reused.

For example, if a `users` table is restructured to split a `full_name` column into `first_name` and `last_name`, a view can concatenate these columns back into `full_name`, preserving compatibility with existing applications.

## Views for Data Independence

If the structure of the base tables changes, you can modify the view definition so the user application doesn't break. This decouples the logical view of the data that applications rely on from the physical storage layout that DBAs may need to evolve.

For example, if a database administrator decides to split a `full_name` column into `first_name` and `last_name` columns, a view can be created that presents the data in the original format, keeping the frontend unchanged. Server-side scripting languages such as PHP, Python, or Node.js further insulate the frontend from the database layer.

## Aggregation Logic in Views (`GROUP BY`)

When views include aggregation, two clauses work together:

- **`GROUP BY`**: Collapses multiple rows into one based on a column.
- **`HAVING`**: Filters the *groups* after aggregation.

> [!IMPORTANT] WHERE vs HAVING
> You cannot use `WHERE` on an aggregate (e.g., `WHERE COUNT(*) > 5` is illegal). You must use `HAVING COUNT(*) > 5`. The `WHERE` clause filters raw rows *before* grouping; the `HAVING` clause filters groups *after* aggregation.

## Handling NULLs in Views

When views compute derived columns, `NULL` values can propagate. Two standard functions handle them:

> [!NOTE] Handling Nulls
> - `COALESCE(val1, val2)`: Returns the first non-null value. Standard SQL.
> - `IFNULL(val1, default)`: MySQL-specific equivalent.

Example:

```sql
CREATE VIEW V_Employee_Contact AS
SELECT
    first_name,
    last_name,
    COALESCE(work_email, personal_email, 'no_email_on_file') AS contact_email
FROM Employees;
```

## Solved Exercise: Complex Access Control Matrix

**Scenario:**

- Table `T1(a1, a2, a3, a4, a5)`
- Table `T2(b1, b2, b3)`

**Q1. Restrict User U1 to columns a1, a2 of T1 where condition 'COND' is true.**

```sql
-- 1. Create the Window
CREATE VIEW V1 AS
SELECT a1, a2
FROM T1
WHERE COND; -- e.g., a1 > 100

-- 2. Give the Key
GRANT SELECT ON V1 TO U1;
```

**Q2. Restrict User U2 to columns a4, a5 of T1 (No condition).**

```sql
CREATE VIEW V2 AS
SELECT a4, a5
FROM T1;

GRANT SELECT ON V2 TO U2;
```

**Q3. Complex Chain: User U3 needs a join between V2 and T2.**

*Requirement:* U3 needs columns `a4, a5` (from V2) and `b1, b2` (from T2), joined where `a4 = b1`. You can build a view on top of another view.

```sql
CREATE VIEW V3 AS
SELECT V2.a4, V2.a5, T2.b1, T2.b2
FROM V2, T2
WHERE V2.a4 = T2.b1;

GRANT SELECT ON V3 TO U3;
```

> [!TIP] Diagram of Dependency
> User U3 → Query V3 → (Queries V2 + Queries T2) → (Queries T1).

Views can be layered on top of other views. This is a powerful composition technique, but be aware that deeply nested views can hurt query optimization because the database must expand every layer at query time.

## Solved Exercise: Simplification & Aggregation ("Max of Sums")

Views are commonly used to solve SQL problems that are impossible or very hard to do in a single nested query — specifically regarding aggregates. SQL standard forbids nested aggregates like `MAX(SUM(km))`. The view solution breaks the problem into steps.

**Question:** Who is the "Chef de Service" who has traveled the most kilometers?

*The Difficulty:* We need to calculate the sum of kilometers for *each* chef (`SUM`), and then find the *maximum* of those sums (`MAX`).

**Step 1: Create a View to calculate totals per Chef.**

```sql
CREATE VIEW R11 AS
SELECT
    chef.SRV_Libelle,
    chef.EMP_Num,
    chef.EMP_Nom,
    SUM(m.MIS_KlmRetour - m.MIS_KlmDepart) AS NbKil
FROM chef, MISSION m
WHERE chef.EMP_Num = m.EMP_Num
GROUP BY chef.SRV_Libelle, chef.EMP_Num, chef.EMP_Nom;
```

*Note:* The view `chef` was created in a previous question to isolate managers.

**Step 2: Query the View.**

```sql
SELECT *
FROM R11
WHERE NbKil = (SELECT MAX(NbKil) FROM R11);
```

*Reasoning:* The view acts as a temporary storage of the "Sum" results. We can then easily find the "Max" from that storage.

## Solved Exercise: Views for Intermediate Sets (Relational Division)

**Question:** Select articles sold by ALL shops.

This is a classic "Relational Division" problem (see [[10 - The Division Operator]]). Writing this in one block is messy. Views make it clean.

**Step 1: Create a View of distinct (Article, Shop) pairs.**

```sql
CREATE VIEW V20 AS
SELECT DISTINCT art_num, mag_num
FROM VENTES;
```

**Step 2: Count shops per article vs Total shops.**

```sql
SELECT V.art_num, A.art_nom
FROM V20 V, ARTICLES A
WHERE V.art_num = A.art_num
GROUP BY V.art_num, A.art_nom
HAVING COUNT(*) = (SELECT COUNT(*) FROM MAGASINS);
```

*Reasoning:* If an article is found in the `V20` view associated with 5 different shops, and the total number of shops in the database is 5, then that article was sold by all shops.

**Question:** Shops with the highest turnover (Chiffre d'affaire) last month.

Similar to the "Chef" example, we need to compare a Sum against a Max of Sums.

**Step 1: View for Turnover per Store.**

```sql
CREATE VIEW V21 AS
SELECT mag_num, SUM(vnt_montant) AS Chiffre_Affaire
FROM VENTES
WHERE to_char(vnt_date, 'MM') = to_char(add_months(sysdate, -1), 'MM') -- Last Month logic (Oracle)
GROUP BY mag_num;
```

**Step 2: Select the Max.**

```sql
SELECT mag_loc, mag_ger, Chiffre_Affaire
FROM V21 V, MAGASINS M
WHERE V.mag_num = M.mag_num
  AND Chiffre_Affaire = (SELECT MAX(Chiffre_Affaire) FROM V21);
```

## Managing Views (DDL)

### Modification

Standard SQL doesn't have an easy "ALTER VIEW" to change the definition logic (in older versions). You usually use:

```sql
CREATE OR REPLACE VIEW nom_vue AS ...
```

This overwrites the old definition with the new one without dropping permissions.

### Dropping

```sql
DROP VIEW nom_vue;
```

*Impact:* This deletes the definition from the dictionary. It does **not** delete the data in the underlying tables.

## See Also

- [[02 - Updatable Views and Check Options]] — When you can INSERT/UPDATE through a view, and the `WITH CHECK OPTION` clause
- [[04 - RDBMS]] — Views as a core RDBMS feature
- [[10 - The Division Operator]] — The division pattern that views make tractable
- [[13 - Aggregation Nuances and Subquery Optimization]] — "Max of Sums" pattern and WHERE vs HAVING
