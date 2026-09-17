# 5. Updatable Views and Check Options

A View is a saved query that acts like a virtual table. While reading from views (`SELECT`) is straightforward, writing to them (`INSERT`, `UPDATE`, `DELETE`) involves strict rules.

## 1. When is a View Updatable?
A view is considered updatable only when the DBMS can unambiguously map the modification back to the underlying base table(s). The exact rules are DBMS-specific, but many complex query constructs make a view non-updatable.

A view is commonly **not updatable** when its defining query contains constructs such as:
* `GROUP BY` or `HAVING`;
* aggregation functions like `SUM()` or `MAX()`;
* `DISTINCT`;
* `UNION` or `UNION ALL`;
* complex `JOIN`s, although some DBMSs support limited updates for specific join views.

## 2. The `WITH CHECK OPTION` Clause
If you create an updatable view that filters data, a loophole can occur when a user inserts or updates a row so that it no longer satisfies the view predicate.

```sql
CREATE VIEW Paris_Employees AS
SELECT id, name, city
FROM Employees
WHERE city = 'Paris';
```

Without a check option, a DBMS may allow an update performed through the view to make a row leave the view's result set.

### Fixing the Loophole

```sql
CREATE VIEW Paris_Employees AS
SELECT id, name, city
FROM Employees
WHERE city = 'Paris'
WITH CHECK OPTION;
```

Now inserts/updates performed through the view must satisfy the view predicate after the modification. The exact updatability and check-option semantics are DBMS-specific.

## 3. Views as Security Boundaries

A view can expose only selected columns (vertical restriction) or selected rows (horizontal restriction), reducing the base-table data that a particular user needs to access.

Example:

```sql
CREATE VIEW V_Service_A003 AS
SELECT EMP_Num, EMP_Nom, EMP_Titre, SRV_Num
FROM EMPLOYE
WHERE SRV_Num = 'A003'
WITH CHECK OPTION;
```

Here the view both limits what rows are visible and, where the view is updatable, prevents modifications that would move an employee outside service `A003` through that view.
