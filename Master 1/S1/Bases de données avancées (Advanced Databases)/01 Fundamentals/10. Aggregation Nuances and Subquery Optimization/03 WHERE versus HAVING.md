# 03 WHERE versus HAVING

The difference is the stage at which rows are filtered.

## WHERE

`WHERE` filters individual rows before grouping and aggregation.

```sql
SELECT customer_id, SUM(amount)
FROM orders
WHERE status = 'Active'
GROUP BY customer_id;
```

Inactive rows are removed before the groups are calculated.

## HAVING

`HAVING` filters groups after grouping and aggregation.

```sql
SELECT customer_id, SUM(amount) AS total
FROM orders
GROUP BY customer_id
HAVING SUM(amount) > 1000;
```

The condition depends on the grouped result.

## Memory rule

- **WHERE:** filter rows.
- **GROUP BY:** build groups.
- **HAVING:** filter groups.

A condition that does not depend on aggregation often belongs in `WHERE`, which can reduce the rows that need to be grouped.
