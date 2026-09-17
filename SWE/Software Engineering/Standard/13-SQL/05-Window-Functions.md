# Window Functions

> The most powerful analytical feature added to SQL since SQL:1999. Window functions compute aggregates *without collapsing rows* — they let you say "give me every transfer and, on the same row, the running total of that account's balance." What used to require self-joins, procedural code, or post-processing in the application is now one clause.

## What you already know

From [[03-Select-Join-Group]]: `GROUP BY` collapses rows — each group becomes one row in the output. From [[04-Relational-Algebra]]: the algebra has aggregation (γ) but it always collapses. From [[00-SQL-From-Relational-Algebra]]: SQL deviates from the algebra where useful; window functions are the biggest such deviation, adding a non-collapsing form of aggregation. From [[08-Trade-offs-Everywhere]]: window functions trade some query complexity for huge gains in expressiveness and performance.

## Why this layer exists

Before window functions, computing a running total required a correlated subquery or a self-join — both O(N²) without an index. Computing "the rank of each row within its partition" required procedural code in the application. Window functions move these computations into the database, where the data already lives, and let the optimizer choose an efficient algorithm (often a single sorted scan).

## What is genuinely new here

The new idea is **aggregation without collapse**. A window function computes a value *per row*, based on a *window* of related rows, and returns that value alongside the original row's data. The output has the same number of rows as the input.

## Concepts

### The OVER clause

Every window function is followed by `OVER (...)`, which defines the window:

```sql
SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY occurred_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

The three components:

- **`PARTITION BY`** — divides rows into groups (like `GROUP BY`, but rows are not collapsed).
- **`ORDER BY`** — orders rows within each partition (required for running aggregates and rank functions).
- **`FRAME`** — the subset of the partition used for each row's computation (`ROWS BETWEEN ... AND ...`).

If you omit `PARTITION BY`, the window is the whole result set. If you omit `ORDER BY`, the window is unordered (and rank functions are undefined). If you omit the frame, the default depends on the function.

### Aggregate vs window functions

The same name (`SUM`, `COUNT`, `AVG`, `MIN`, `MAX`) is used both as an aggregate (with `GROUP BY`) and as a window function (with `OVER`). The difference:

| Aggregate (with GROUP BY) | Window function (with OVER) |
|---|---|
| One row per group | One row per input row |
| Collapses the result | Preserves the result |
| Cannot reference non-grouped columns | Can reference any column |

### The ranking functions

| Function | Behavior |
|---|---|
| `ROW_NUMBER()` | Unique sequential integer (1, 2, 3, ...). Ties are broken arbitrarily. |
| `RANK()` | Same rank for ties, then skips (1, 2, 2, 4). |
| `DENSE_RANK()` | Same rank for ties, no skip (1, 2, 2, 3). |
| `NTILE(n)` | Divides the partition into n buckets; returns the bucket number. |
| `PERCENT_RANK()` | Rank as a fraction between 0 and 1. |
| `CUME_DIST()` | Cumulative distribution: fraction of rows with value ≤ current. |

### The value functions

| Function | Behavior |
|---|---|
| `LAG(col, n)` | Value of `col` in the row n positions before the current. |
| `LEAD(col, n)` | Value of `col` in the row n positions after. |
| `FIRST_VALUE(col)` | First value in the window frame. |
| `LAST_VALUE(col)` | Last value in the window frame. |
| `NTH_VALUE(col, n)` | Nth value in the frame. |

### Running totals and moving averages

The frame clause determines the window:

```sql
-- Running total: from the start of the partition to the current row
SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY occurred_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)

-- Moving average: last 7 rows including current
AVG(amount) OVER (
    PARTITION BY account_id
    ORDER BY occurred_at
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)

-- Cumulative total: every row up to and including current (same as running total in most cases)
SUM(amount) OVER (
    PARTITION BY account_id
    ORDER BY occurred_at
    RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
)
```

`ROWS` counts rows; `RANGE` counts peer values (rows with the same `ORDER BY` value). For most uses, `ROWS` is what you want. `RANGE` matters when there are ties in the `ORDER BY` column.

### The default frame

If you omit the frame, the default depends on whether `ORDER BY` is present:

- With `ORDER BY`: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` (a running total).
- Without `ORDER BY`: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` (the whole partition).

This is a common source of bugs: `SUM(amount) OVER (PARTITION BY account_id)` returns the partition total on every row (because there is no `ORDER BY`), while `SUM(amount) OVER (PARTITION BY account_id ORDER BY occurred_at)` returns a running total.

### Where window functions fit in the evaluation order

From [[03-Select-Join-Group]]: the logical evaluation order is `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`. Window functions run *after* `SELECT` is computed but *before* `ORDER BY` and `LIMIT`. This means:

- Window functions can reference column aliases defined in `SELECT`.
- Window functions cannot appear in `WHERE` or `HAVING` (those run before the window).
- To filter on a window function's result, wrap the query in a CTE or subquery and filter the outer query.

```sql
-- WRONG: cannot use window function in WHERE
SELECT * FROM accounts
WHERE ROW_NUMBER() OVER (ORDER BY balance DESC) <= 3;

-- CORRECT: wrap in a CTE
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (ORDER BY balance DESC) AS rn
    FROM accounts
)
SELECT * FROM ranked WHERE rn <= 3;
```

## Banking application

### Query 1: running balance per account over time

```sql
-- PostgreSQL: running balance for account 42 over the last 30 days
SELECT le.occurred_at, le.amount,
       SUM(le.amount) OVER (
           PARTITION BY le.account_id
           ORDER BY le.occurred_at
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_balance
FROM ledger_entries le
WHERE le.account_id = 42
  AND le.occurred_at > now() - interval '30 days'
ORDER BY le.occurred_at;
```

Without window functions, this query required a self-join (`SELECT SUM(amount) FROM ledger_entries WHERE account_id = 42 AND occurred_at <= le.occurred_at`) — O(N²) without an index. With a window function, the database sorts once and computes the running total in a single pass.

### Query 2: top-3 transfers per customer

```sql
-- Find the three largest transfers per customer
SELECT * FROM (
    SELECT t.id, t.amount, t.created_at,
           c.legal_name,
           ROW_NUMBER() OVER (PARTITION BY c.id ORDER BY t.amount DESC) AS rn
    FROM transfers t
    JOIN accounts a ON a.id = t.from_account_id
    JOIN customers c ON c.id = a.customer_id
    WHERE t.status = 'COMPLETED'
) ranked
WHERE rn <= 3
ORDER BY legal_name, rn;
```

This is the canonical "top-N per group" pattern. It is one of the most common uses of window functions and is dramatically cleaner than the alternatives.

### Query 3: day-over-day balance change

```sql
-- PostgreSQL: daily balance with day-over-day delta
WITH daily AS (
    SELECT DATE(occurred_at) AS day,
           account_id,
           SUM(amount) AS daily_change
    FROM ledger_entries
    WHERE occurred_at > now() - interval '30 days'
    GROUP BY DATE(occurred_at), account_id
)
SELECT day, account_id, daily_change,
       LAG(daily_change) OVER (PARTITION BY account_id ORDER BY day) AS prev_day_change,
       daily_change - LAG(daily_change) OVER (PARTITION BY account_id ORDER BY day) AS delta
FROM daily
ORDER BY account_id, day;
```

`LAG` accesses the previous row's value, making day-over-day comparisons trivial.

### Query 4: ranking accounts by balance within each customer

```sql
SELECT a.id, a.iban, a.balance, c.legal_name,
       RANK() OVER (PARTITION BY a.customer_id ORDER BY a.balance DESC) AS balance_rank,
       DENSE_RANK() OVER (PARTITION BY a.customer_id ORDER BY a.balance DESC) AS dense_rank
FROM accounts a
JOIN customers c ON c.id = a.customer_id
WHERE a.status = 'ACTIVE';
```

`RANK` and `DENSE_RANK` differ on ties: if two accounts have the same balance, `RANK` gives them both rank 1 and the next gets rank 3; `DENSE_RANK` gives them both rank 1 and the next gets rank 2.

### Query 5: percentile of each transfer

```sql
SELECT t.id, t.amount,
       NTILE(100) OVER (ORDER BY t.amount) AS percentile_bucket,
       PERCENT_RANK() OVER (ORDER BY t.amount) AS percent_rank,
       CUME_DIST() OVER (ORDER BY t.amount) AS cumulative_dist
FROM transfers t
WHERE t.status = 'COMPLETED'
  AND t.created_at > now() - interval '7 days';
```

`NTILE(100)` divides the transfers into 100 buckets, ranked by amount. `PERCENT_RANK` gives the rank as a fraction. `CUME_DIST` gives the fraction of transfers with amount ≤ the current row's amount.

## Code — common patterns

```sql
-- Pattern 1: deduplicate (keep the latest row per key)
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY occurred_at DESC) AS rn
    FROM ledger_entries
)
SELECT * FROM ranked WHERE rn = 1;

-- Pattern 2: running total and moving average side by side
SELECT occurred_at, amount,
       SUM(amount) OVER (ORDER BY occurred_at
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running,
       AVG(amount) OVER (ORDER BY occurred_at
                         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_7
FROM ledger_entries WHERE account_id = 42;

-- Pattern 3: first and last value per partition
SELECT account_id,
       FIRST_VALUE(amount) OVER (PARTITION BY account_id ORDER BY occurred_at) AS first_amount,
       LAST_VALUE(amount)  OVER (PARTITION BY account_id ORDER BY occurred_at
                                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_amount
FROM ledger_entries;
-- Note: LAST_VALUE requires the explicit frame; the default frame ends at CURRENT ROW,
-- which would always be the current row's value.

-- Pattern 4: percent of total
SELECT account_id, SUM(amount) AS total,
       SUM(amount) / SUM(SUM(amount)) OVER () * 100 AS pct_of_grand_total
FROM ledger_entries
GROUP BY account_id;
```

## What can go wrong

- **Using a window function in `WHERE`.** Not allowed — wrap in a CTE and filter outside.
- **Forgetting the frame for `LAST_VALUE`.** The default frame ends at `CURRENT ROW`, so `LAST_VALUE` returns the current row's value. Always specify `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` for `LAST_VALUE`.
- **Surprising default frames.** `SUM(x) OVER (PARTITION BY y)` returns the partition total on every row (no `ORDER BY`, so the frame is the whole partition). Adding `ORDER BY` silently changes the semantics to "running total."
- **Performance on large windows.** A window function with `PARTITION BY` and `ORDER BY` requires sorting. On a large table, this can be the dominant cost. Index the partition + order columns.
- **Sorting mismatches.** If the `OVER (ORDER BY ...)` differs from the query's `ORDER BY`, the output rows are in the query's order, but the window was computed in a different order. Confusing.
- **NULL handling.** `LAG` and `LEAD` return NULL at partition boundaries. Some functions ignore NULLs; some include them. Check the docs for each function.
- **Using `RANGE` when you meant `ROWS`.** `RANGE` includes peer rows (rows with the same `ORDER BY` value). For running totals with unique `ORDER BY` values, they are equivalent. With duplicates, they differ.
- **Window functions on top of `GROUP BY`.** The window function operates on the post-`GROUP BY` rows. This is sometimes what you want; sometimes a surprise.

## Trade-offs

- **Window function vs self-join.** The window function is almost always faster (single sort vs O(N²) joins) and clearer. Use it.
- **Window function vs procedural code.** The window function runs in the database, avoiding data transfer. Use it for computations that fit the window model; switch to procedural code for complex business logic.
- **`ROW_NUMBER` vs `RANK` vs `DENSE_RANK`.** Choose based on how you want ties handled. `ROW_NUMBER` for unique ranks; `RANK` for "Olympic" ranking (1, 2, 2, 4); `DENSE_RANK` for "no gaps" (1, 2, 2, 3).
- **`ROWS` vs `RANGE`.** `ROWS` counts rows; `RANGE` counts peer values. `ROWS` is usually what you want for running totals.
- **Sort cost vs expressiveness.** Every window function with `ORDER BY` requires a sort. On large partitions, this is the dominant cost. Sometimes a separate pre-aggregated table is cheaper — see [[02-Denormalization-For-Reads]].

## Forward links

- [[03-Select-Join-Group]] — the foundation these build on.
- [[04-Subqueries-CTEs]] — wrap a window function in a CTE to filter on its result.
- [[07-Views-Materialized-Views]] — save useful windowed queries.
- [[06-Query-Processing-Pipeline]] — how window functions are executed.
- [[07-Cost-Based-Optimizer]] — how the optimizer chooses a sort or an index for the window.
- [[09-Banking-SQL]] — running balances and top-N queries in the Banking case study.
