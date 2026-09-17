# 5. Updatable Views and Check Options

A View is a saved query that acts like a virtual table. While reading from views (`SELECT`) is straightforward, writing to them (`INSERT`, `UPDATE`, `DELETE`) involves strict rules.

## 1. When is a View Updatable?
A view is only considered "Updatable" (meaning you can manipulate data through it, and the DBMS will pass those changes down to the underlying physical table) if it maintains a **1-to-1 relationship** with the rows of the base table.

A view is **STRICTLY NOT UPDATABLE** if its defining query contains any of the following:
*   `GROUP BY` or `HAVING` (The virtual row represents multiple physical rows. The DB doesn't know which physical row to update).
*   Aggregation functions like `SUM()`, `MAX()`.
*   `DISTINCT` (Removes duplicates, breaking the 1-to-1 mapping).
*   `UNION` or `UNION ALL`.
*   Most `JOIN`s (Some DBMSs allow updates on certain join views if the modification only affects one side of the join, but generally, complex joins block updates).

## 2. The WITH CHECK OPTION Clause
If you create an updatable view that filters data, a dangerous loophole exists. 

Imagine a view for the Paris office:
```sql
CREATE VIEW Paris_Employees AS 
SELECT id, name, city FROM Employees WHERE city = 'Paris';
```
By default, you could run this query:
```sql
INSERT INTO Paris_Employees (id, name, city) VALUES (99, 'John', 'London');
```
The database would successfully insert John into the underlying `Employees` table with the city 'London'. However, if you immediately `SELECT * FROM Paris_Employees`, John will not be there! He vanished from the perspective of the view.

### Fixing the Loophole
To prevent users from inserting or updating data that immediately falls outside the scope of the view, use the `WITH CHECK OPTION`.

```sql
CREATE VIEW Paris_Employees AS 
SELECT id, name, city FROM Employees WHERE city = 'Paris'
WITH CHECK OPTION;
```
Now, if you attempt to insert 'London', the DBMS will block it with an error: *"CHECK OPTION failed"*. The view acts as a strict security and integrity boundary.
