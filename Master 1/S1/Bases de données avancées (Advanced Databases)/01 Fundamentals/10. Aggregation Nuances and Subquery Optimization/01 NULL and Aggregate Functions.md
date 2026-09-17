# 01 NULL and Aggregate Functions

`NULL` means that a value is unknown or not present. It is not the same as zero or an empty string.

## Aggregate behavior

For standard SQL aggregate functions such as `SUM`, `AVG`, `MIN`, and `MAX`, `NULL` input values are generally ignored.

Example values:

`10, 20, NULL, 30`

`AVG(price)` uses the three non-NULL values, so the result is `20`.

## Important consequence

Replacing `NULL` with zero changes the meaning of the data and can change the aggregate result. Use `COALESCE` only when zero is genuinely the intended business interpretation.

Example:

```sql
AVG(COALESCE(price, 0))
```

This calculates an average over all rows after replacing missing prices with zero; it is not equivalent to the default `AVG(price)` behavior.
