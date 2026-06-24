# 4. Aggregation Nuances and Subquery Optimization

While basic `JOIN`s and `GROUP BY`s are standard, mastering how the database handles `NULL` values and choosing between subqueries vs joins separates beginners from advanced SQL developers.

## 1. The Perils of NULL in Aggregations
Aggregation functions (`SUM`, `AVG`, `MIN`, `MAX`, `COUNT`) have very specific, often misunderstood behaviors regarding `NULL` values.

*   **Rule 1: Aggregations Ignore NULLs.**
    If you have a `price` column with values `[10, 20, NULL, 30]`, executing `AVG(price)` will return `20` (Calculated as $60 \div 3$). It entirely skips the row with the `NULL`.
*   **Rule 2: The Exception of `COUNT(*)`**
    *   `COUNT(price)` counts how many non-null prices exist (returns 3).
    *   `COUNT(*)` counts the physical rows in the table, regardless of what they contain (returns 4).
*   **Fixing NULL Math:** If you want the `NULL` to be treated as a zero in your average, you must force it using `COALESCE` or `IFNULL`:
    `AVG(IFNULL(price, 0))` will return `15` (Calculated as $60 \div 4$).

## 2. WHERE vs HAVING
A common point of confusion is when to filter data during an aggregation.

*   **`WHERE`** applies to raw rows **before** they are grouped together.
    *   *Example:* `WHERE status = 'Active'` removes inactive users before the database even starts calculating totals.
*   **`HAVING`** applies to the grouped summary rows **after** aggregation.
    *   *Example:* `HAVING SUM(amount) > 1000` looks at the final groups and discards any group that didn't generate enough revenue.

## 3. Subqueries vs Joins: Optimization Strategies
You can often write the exact same logic using either a Subquery or a `JOIN`. Which should you choose?

### When to use a JOIN:
*   When retrieving data from multiple tables simultaneously.
*   When dealing with massive datasets. The query optimizer is highly tuned to process `JOIN` operations efficiently using Hash algorithms.

### When to use a Subquery:
*   When you need an intermediate calculated value (e.g., finding all employees who earn more than the company average). You *cannot* do this with a simple join.
*   **Using `EXISTS`:** If you just want to know if a record exists in another table (e.g., "Show me clients who have placed at least one order"), using `WHERE EXISTS (SELECT 1 FROM Orders WHERE...)` is drastically faster than a `JOIN`. `EXISTS` stops searching the instant it finds the first match, whereas a `JOIN` will map out every single order before filtering.
