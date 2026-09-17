# 04 Subqueries and Correlated Subqueries

A subquery is a query nested inside another SQL statement.

## Scalar subquery

Returns one value.

Example: employees whose salary is above the company average.

```sql
SELECT name, salary
FROM employee
WHERE salary > (SELECT AVG(salary) FROM employee);
```

## Multi-row subquery

A subquery can return several values and can be used with operators such as `IN`, `ANY`, or `ALL` where appropriate.

## Correlated subquery

A correlated subquery refers to a value from the outer query, so it is evaluated in relation to the current outer row.

Conceptually:

```sql
SELECT c.name
FROM customer c
WHERE EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.id
);
```

The inner query depends on `c.id` from the outer query.

## Optimization note

Do not assume that a subquery is inherently slower or faster than a join. Modern optimizers can transform equivalent formulations. Inspect the actual execution plan when performance matters.
