# 02 COUNT and Other Aggregate Functions

## COUNT(*)

`COUNT(*)` counts rows. It does not discard a row merely because one of its columns is `NULL`.

## COUNT(column)

`COUNT(column)` counts non-NULL values in that column.

For rows containing:

`10, 20, NULL, 30`

- `COUNT(*)` = 4;
- `COUNT(price)` = 3.

## Other aggregates

- `SUM(column)` aggregates non-NULL values;
- `AVG(column)` averages non-NULL values;
- `MIN(column)` and `MAX(column)` consider non-NULL values.

If all values supplied to an aggregate are `NULL`, the result is generally `NULL` rather than zero.

## Exam trap

Never replace `COUNT(*)` with `COUNT(id)` without checking whether `id` can be `NULL` and whether the intended question is "how many rows" or "how many non-NULL values".
