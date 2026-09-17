# 05 EXISTS versus JOIN

Use `EXISTS` when the question is fundamentally whether at least one related row exists.

## EXISTS

```sql
SELECT c.name
FROM customer c
WHERE EXISTS (
  SELECT 1
  FROM orders o
  WHERE o.customer_id = c.id
);
```

This asks: "Does this customer have at least one order?"

The database can stop considering the existence condition once a qualifying match is established, depending on the execution strategy.

## JOIN

A join is appropriate when the query needs columns from both relations or needs to construct a combined row set.

A plain join can produce multiple rows for one customer when that customer has multiple orders.

## Avoid accidental duplicates

If the question is only existence, `EXISTS` often expresses the intent more directly than a join followed by `DISTINCT`.

## Performance principle

There is no universal rule that `EXISTS` is faster. Query optimizer behavior depends on the DBMS, indexes, statistics, data distribution, and query shape.
