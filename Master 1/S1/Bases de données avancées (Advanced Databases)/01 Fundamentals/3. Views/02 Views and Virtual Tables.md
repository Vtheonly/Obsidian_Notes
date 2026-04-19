###  Sources
*   *Based on Images: 5, 11 (Top Right)*

### 1. Definition and Usage
A **View (Vue)** is a virtual table. It is a saved SQL query, not a physical store of data.

**Syntax:**
```sql
CREATE VIEW View_Name AS
SELECT col1, col2 
FROM table 
WHERE condition;
```

**Benefits:**
1.  **Security:** Restrict user access to specific columns (hide passwords/salaries).
2.  **Simplicity:** encapsulate complex Joins so users just do `SELECT * FROM simple_view`.

### 2. Updating Views (Crucial Concept)
Can you `INSERT` or `UPDATE` a view?
*   **YES:** If the view is a direct window onto a single table (1:1 mapping).
*   **NO:** If the view contains:
    *   Aggregates (`SUM`, `COUNT`).
    *   `GROUP BY` or `HAVING`.
    *   `DISTINCT`.
    *   `UNION`.
    *   Joins (in most cases, depending on DBMS strictness).

#### `WITH CHECK OPTION`
If you create a view that filters data (e.g., `WHERE age > 18`), and you insert a user with `age = 10` through that view:
*   **Without Option:** The insertion succeeds, but the row immediately disappears from the view (phantom insert).
*   **`WITH CHECK OPTION`:** The DBMS rejects the insert because the data violates the view's `WHERE` clause.

### 3. Aggregation Logic (`GROUP BY`)
*   **`GROUP BY`:** Collapses multiple rows into one based on a column.
*   **`HAVING`:** Filters the *groups* after aggregation.
    *   *Rule:* You cannot use `WHERE` on an aggregate (e.g., `WHERE COUNT(*) > 5` is illegal). You must use `HAVING COUNT(*) > 5`.

> [!NOTE] Handling Nulls
> *   `COALESCE(val1, val2)`: Returns the first non-null value. Standard SQL.
> *   `IFNULL(val1, default)`: MySQL specific.

---