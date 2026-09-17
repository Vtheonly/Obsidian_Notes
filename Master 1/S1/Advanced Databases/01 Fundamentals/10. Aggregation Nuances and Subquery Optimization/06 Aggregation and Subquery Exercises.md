# 06 Aggregation and Subquery Exercises

## Exercise 1 — NULL

A table contains prices `10, 20, NULL, 30`.

**Question:** compare `COUNT(*)`, `COUNT(price)`, and `AVG(price)`.

**Answer:** `COUNT(*)` counts four rows, `COUNT(price)` counts three non-NULL values, and `AVG(price)` is calculated from the three known prices.

## Exercise 2 — filtering

Find customers whose total active-order amount exceeds 1000.

**Question:** should the status condition be in `WHERE` and the total condition in `HAVING`?

**Answer:** yes. Status filters rows before grouping; the total filters groups after aggregation.

## Exercise 3 — existence

Find customers who have at least one order without returning one row per order.

**Task:** write the query using `EXISTS`.

```sql
SELECT c.name
FROM customer c
WHERE EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.id
);
```

## Exam checklist

- check `NULL` behavior;
- distinguish row filters from group filters;
- identify what the subquery returns;
- use `EXISTS` when the requirement is existence;
- never claim a query is faster without considering the execution plan and DBMS.
