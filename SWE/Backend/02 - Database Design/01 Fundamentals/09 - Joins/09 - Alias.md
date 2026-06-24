# Alias

An alias in SQL is a temporary name assigned to a table or column within a query. Aliases do not modify the underlying database schema or data; they exist only for the duration of the query in which they are defined. The primary purposes of aliases are to improve readability, shorten lengthy table or column names, and resolve ambiguity when multiple tables have columns with the same name.

Aliases are especially important in join queries, where you frequently reference multiple tables and need to distinguish between columns that share names across tables. They are also essential for self joins, where a single table is referenced multiple times in the same query and must be given different names to avoid confusion. See [[08 - Auto-Join, Self-Reference, and Self Join]] for that specific use case.

## Table Aliases

A table alias assigns a short, temporary name to a table within a query. The alias is defined using the `AS` keyword (which is optional in most database systems) immediately after the table name in the `FROM` or `JOIN` clause. Once defined, the alias must be used throughout the rest of the query in place of the original table name.

```sql
SELECT c.first_name, c.last_name, o.order_date
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id;
```

In this query, `customers` is aliased as `c` and `orders` is aliased as `o`. Every subsequent reference to these tables uses the alias rather than the full name. The `AS` keyword can be omitted without changing the meaning:

```sql
SELECT c.first_name, c.last_name, o.order_date
FROM customers c
INNER JOIN orders o
    ON c.customer_id = o.customer_id;
```

Both forms are valid and produce identical results. The explicit `AS` keyword is generally preferred for clarity, especially in complex queries where it helps distinguish aliases from other keywords.

## Why Table Aliases Improve Readability

Without aliases, a join query with multiple tables becomes verbose and difficult to read. Consider the difference:

```sql
-- Without aliases (verbose)
SELECT customers.first_name, customers.last_name, orders.order_date, products.product_name
FROM customers
INNER JOIN orders
    ON customers.customer_id = orders.customer_id
INNER JOIN order_items
    ON orders.order_id = order_items.order_id
INNER JOIN products
    ON order_items.product_id = products.product_id;

-- With aliases (concise)
SELECT c.first_name, c.last_name, o.order_date, p.product_name
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
INNER JOIN order_items AS oi
    ON o.order_id = oi.order_id
INNER JOIN products AS p
    ON oi.product_id = p.product_id;
```

The aliased version is shorter, easier to scan, and less prone to typing errors. In queries with many tables, the benefit of aliases becomes even more pronounced.

## Column Aliases

A column alias assigns a temporary name to a column in the query result. This is most commonly used to rename computed columns, remove underscores from column names, or provide more descriptive headers in the output. Column aliases are defined using the `AS` keyword after the column expression.

```sql
SELECT
    first_name AS "First Name",
    last_name AS "Last Name",
    salary * 12 AS "Annual Salary"
FROM employees;
```

When the alias contains spaces or special characters, it must be enclosed in quotes. Single quotes, double quotes, or square brackets may be used depending on the database system. Without quotes, the alias must follow standard identifier naming rules (no spaces, no special characters).

```sql
-- Different quoting styles (database-dependent)
SELECT
    first_name AS FirstName,           -- no quotes needed
    last_name AS "Last Name",         -- double quotes (standard SQL)
    salary * 12 AS 'Annual Salary'    -- single quotes (MySQL)
FROM employees;
```

The column alias affects only the output header of the result set. It does not change the column name in the underlying table, and it cannot be referenced in the `WHERE` clause of the same query (because the `WHERE` clause is evaluated before the `SELECT` clause in the logical query processing order).

## Aliases in Joins

In join queries, aliases serve two critical functions: shortening table references and disambiguating column names. When two tables have columns with the same name (such as `customer_id` in both a `customer` table and an `orders` table), the table alias provides a concise way to specify which column you mean.

```sql
SELECT
    c.first_name,
    c.last_name,
    ca.card_type,
    ca.max_amount
FROM customer AS c
INNER JOIN card AS ca
    ON c.customer_id = ca.customer_id;
```

Without aliases, you would need to write `customer.customer_id` and `card.customer_id` every time you reference these columns. With aliases, `c.customer_id` and `ca.customer_id` achieve the same result with less visual noise.

## Aliases in Subqueries

Aliases are also used to name derived tables (subqueries in the `FROM` clause). Most database systems require that every subquery in the `FROM` clause be given an alias, even if you do not reference the alias elsewhere in the query. This is because the subquery produces a temporary result set that the database treats as a virtual table, and every table must have a name.

```sql
SELECT
    dept_summary.department_name,
    dept_summary.employee_count
FROM (
    SELECT
        department_name,
        COUNT(*) AS employee_count
    FROM employees
    GROUP BY department_name
) AS dept_summary
ORDER BY dept_summary.employee_count DESC;
```

In this query, the subquery is aliased as `dept_summary`. The outer query references `dept_summary.department_name` and `dept_summary.employee_count` as if `dept_summary` were a real table.

## Combining Table and Column Aliases

In practice, you will frequently combine table and column aliases in the same query. This is particularly useful in join queries where you want both concise table references and descriptive column headers:

```sql
SELECT
    c.first_name AS "First Name",
    c.last_name AS "Last Name",
    ct.name AS "Card Type",
    ca.max_amount AS "Credit Limit"
FROM customer AS c
INNER JOIN card AS ca
    ON c.customer_id = ca.customer_id
INNER JOIN card_type AS ct
    ON ca.card_type_id = ct.card_type_id;
```

This query uses table aliases (`c`, `ca`, `ct`) for concise column references and column aliases for user-friendly output headers. The result is a query that is both easy to write and easy to read when reviewing the output.

## Summary

Aliases are a fundamental tool for writing clear, maintainable SQL. Table aliases shorten references and disambiguate column names in joins. Column aliases improve the presentation of query results. Subquery aliases are required for derived tables. While the `AS` keyword is optional in most contexts, using it explicitly is a best practice that improves code readability and reduces the chance of misinterpretation. These concepts become even more important when working with [[03 - Inner Join]] queries and [[08 - Auto-Join, Self-Reference, and Self Join]] scenarios where table aliases are not just convenient but necessary.
