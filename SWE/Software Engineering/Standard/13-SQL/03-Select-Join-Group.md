# SELECT, JOIN, GROUP BY

> The workhorses of SQL. Eighty percent of queries are a `SELECT` with a `JOIN` and a `GROUP BY`. Understanding the evaluation order, the join types, and the `HAVING` vs `WHERE` distinction is what separates a junior who writes queries that work from a senior who writes queries that are obviously correct.

## What you already know

From [[04-Relational-Algebra]]: selection (σ) is row filtering, projection (π) is column filtering, join (⨝) combines relations on a predicate, and aggregation (γ) groups and reduces. From [[00-SQL-From-Relational-Algebra]]: SQL's `SELECT ... FROM ... WHERE` triple maps directly to π / ⨝ / σ, and SQL deviates from algebra with bags, NULLs, and ordering. From [[06-1NF-2NF-3NF]]: a normalized schema spreads facts across many tables; joins reassemble them.

## Why this layer exists

The schema is normalized; the application needs *answers*, not rows scattered across tables. A query is the bridge: it expresses "I want these columns from these tables, filtered by these conditions, grouped by these dimensions, in this order." Without joins, every query would be a single-table lookup. Without grouping, every aggregate would be computed in application code.

## What is genuinely new here

The new idea is **the logical evaluation order of a SELECT statement** — the order in which the clauses are *logically* evaluated, which is almost the reverse of the order in which they are *written*. This single insight explains why you cannot use a column alias in `WHERE`, why `HAVING` exists at all, and why `LIMIT` is the last clause.

## Concepts

### The logical evaluation order

SQL is written in this order:

```sql
SELECT ...
FROM ...
WHERE ...
GROUP BY ...
HAVING ...
ORDER BY ...
LIMIT ...;
```

But the database *logically* evaluates it in this order:

```
FROM (including JOINs)
WHERE
GROUP BY
HAVING
SELECT (projection, DISTINCT, window functions)
ORDER BY
LIMIT / OFFSET
```

This explains several "why can't I..." questions:

- **Why can't I use a column alias in `WHERE`?** Because `WHERE` runs before `SELECT`. The alias does not exist yet.
- **Why can I use a column alias in `ORDER BY`?** Because `ORDER BY` runs after `SELECT`. The alias exists.
- **Why does `HAVING` exist?** Because `WHERE` filters rows *before* grouping, while `HAVING` filters *groups* after grouping. You cannot put `SUM(amount) > 1000` in `WHERE` because the aggregation has not happened yet.
- **Why does `LIMIT` not affect the result of subqueries?** Because `LIMIT` is the final step; it operates on the already-computed result.

### JOIN types

| Join | What it returns |
|---|---|
| `INNER JOIN` (or just `JOIN`) | Rows that match in both tables |
| `LEFT [OUTER] JOIN` | All rows from the left, plus matches from the right (NULL if no match) |
| `RIGHT [OUTER] JOIN` | All rows from the right, plus matches from the left |
| `FULL [OUTER] JOIN` | All rows from both, with NULLs where there is no match |
| `CROSS JOIN` | Cartesian product — every left row paired with every right row |
| `NATURAL JOIN` | Join on columns with the same name (avoid — fragile) |

The most common by far is `INNER JOIN` and `LEFT JOIN`. `RIGHT JOIN` is rarely used (it is just `LEFT JOIN` with the tables swapped); `FULL JOIN` is used in reconciliation queries ("show me rows in either table that do not match"); `CROSS JOIN` is used for generating combinations.

### SQL:1999 JOIN syntax vs the older comma syntax

The modern (SQL:1999) syntax:

```sql
SELECT a.iban, c.legal_name
FROM accounts a
JOIN customers c ON c.id = a.customer_id
WHERE a.status = 'ACTIVE';
```

The older comma syntax (still supported, but discouraged):

```sql
SELECT a.iban, c.legal_name
FROM accounts a, customers c
WHERE a.customer_id = c.id
  AND a.status = 'ACTIVE';
```

The modern syntax is preferred because:

- It separates the join condition (`ON`) from the filter (`WHERE`), making intent clearer.
- It makes outer joins possible (the comma syntax for outer joins was vendor-specific and ugly — remember `(+)` in Oracle?).
- It is harder to accidentally produce a cross join. (Forget the `WHERE` clause in the comma syntax and you get a cross product; the modern syntax forces you to write `ON`.)

### GROUP BY and aggregates

`GROUP BY` partitions the rows into groups by the listed columns; an aggregate function reduces each group to a single value:

| Aggregate | What it returns |
|---|---|
| `COUNT(*)` | Number of rows in the group (including NULLs) |
| `COUNT(col)` | Number of non-NULL values of `col` |
| `SUM(col)` | Sum of `col` (ignores NULLs) |
| `AVG(col)` | Average of `col` (ignores NULLs) |
| `MIN(col)`, `MAX(col)` | Extreme values |
| `BOOL_AND(col)`, `BOOL_OR(col)` (PostgreSQL) | Logical reduction |
| `STRING_AGG(col, sep)` (PostgreSQL) | Concatenate strings |
| `ARRAY_AGG(col)` (PostgreSQL) | Collect into an array |

The fundamental rule: every column in `SELECT` that is not inside an aggregate must appear in `GROUP BY`. Otherwise, the database does not know which value to pick from the group.

PostgreSQL is strict about this (some databases, like MySQL in non-strict mode, pick an arbitrary value — a footgun).

### HAVING vs WHERE

- `WHERE` filters rows *before* grouping. It cannot reference aggregates.
- `HAVING` filters groups *after* grouping. It can reference aggregates.

```sql
-- Find customers whose total ACTIVE balance exceeds $100,000
SELECT c.id, c.legal_name, SUM(a.balance) AS total
FROM customers c
JOIN accounts a ON a.customer_id = c.id
WHERE a.status = 'ACTIVE'    -- filter rows before grouping
GROUP BY c.id, c.legal_name
HAVING SUM(a.balance) > 100000;  -- filter groups after aggregation
```

Both filters are necessary and serve different purposes. Removing `WHERE` would include closed/frozen accounts in the sum; removing `HAVING` would return every customer, not just the high-balance ones.

### DISTINCT

`DISTINCT` removes duplicate rows from the result. It is a set operator in a bag world. Use it when:

- A join produces duplicates that the application does not want.
- You want a list of unique values of a column.

Avoid it as a band-aid for a poorly-thought-out join. If you need `DISTINCT`, ask: *why are there duplicates?* Sometimes the answer is "the join is one-to-many and I only wanted the one side" — in which case the join should be an `EXISTS` subquery.

## Banking application

### Query 1: customer with their account count and total balance

```sql
SELECT c.id, c.legal_name,
       COUNT(a.id) AS account_count,
       COALESCE(SUM(a.balance), 0) AS total_balance
FROM customers c
LEFT JOIN accounts a ON a.customer_id = c.id  -- LEFT JOIN: include customers with no accounts
WHERE c.status = 'VERIFIED'
GROUP BY c.id, c.legal_name
ORDER BY total_balance DESC;
```

The `LEFT JOIN` ensures customers with no accounts still appear (with `account_count = 0` and `total_balance = 0` thanks to `COALESCE`). An `INNER JOIN` would silently drop them.

### Query 2: high-balance customers

```sql
-- Find customers with total ACTIVE balance > $100,000
SELECT c.id, c.legal_name, SUM(a.balance) AS total_balance
FROM customers c
JOIN accounts a ON a.customer_id = c.id
WHERE a.status = 'ACTIVE'
GROUP BY c.id, c.legal_name
HAVING SUM(a.balance) > 100000
ORDER BY total_balance DESC;
```

The vault's anchor query, from [[00-SQL-From-Relational-Algebra]]. It exercises five algebraic operators: σ (`WHERE`), ⨝ (`JOIN`), γ (`GROUP BY` + `SUM`), σ again (`HAVING`), and sort (`ORDER BY`).

### Query 3: recent transfers per account, with customer names

```sql
SELECT t.id, t.amount, t.created_at,
       fa.iban AS from_iban, fc.legal_name AS from_customer,
       ta.iban AS to_iban,   tc.legal_name AS to_customer
FROM transfers t
JOIN accounts fa ON fa.id = t.from_account_id
JOIN accounts ta ON ta.id = t.to_account_id
JOIN customers fc ON fc.id = fa.customer_id
JOIN customers tc ON tc.id = ta.customer_id
WHERE t.created_at > now() - interval '7 days'
ORDER BY t.created_at DESC
LIMIT 100;
```

Note that `accounts` and `customers` each appear *twice* with different aliases. The same table can be joined multiple times in one query; each appearance needs its own alias.

### Query 4: per-day transfer volume

```sql
SELECT DATE(t.created_at) AS day,
       COUNT(*) AS transfer_count,
       SUM(t.amount) AS total_volume,
       AVG(t.amount) AS avg_amount,
       MAX(t.amount) AS largest_transfer
FROM transfers t
WHERE t.status = 'COMPLETED'
GROUP BY DATE(t.created_at)
ORDER BY day DESC;
```

A typical reporting query: group by a date dimension, aggregate over a fact table. This is the bread-and-butter of OLAP.

## Code — common patterns

```sql
-- Pattern 1: self-join (find accounts whose owner has another account with higher balance)
SELECT a.iban, a.balance, b.iban AS bigger_sibling_iban
FROM accounts a
JOIN accounts b ON b.customer_id = a.customer_id AND b.balance > a.balance;

-- Pattern 2: LEFT JOIN with filter on the right side
-- WARNING: putting right-side filters in WHERE converts the LEFT JOIN to INNER JOIN
-- WRONG:
SELECT * FROM customers c
LEFT JOIN accounts a ON a.customer_id = c.id
WHERE a.status = 'ACTIVE';   -- this filters out customers with no ACTIVE account
-- CORRECT:
SELECT * FROM customers c
LEFT JOIN accounts a ON a.customer_id = c.id AND a.status = 'ACTIVE';

-- Pattern 3: FULL JOIN for reconciliation
SELECT a.iban AS accounts_iban, s.account_id AS statements_account_id
FROM accounts a
FULL JOIN statements s ON s.account_id = a.id
WHERE a.id IS NULL OR s.account_id IS NULL;
-- Returns rows that exist in only one table — useful for finding missing statements.

-- Pattern 4: COUNT with CASE for conditional aggregation
SELECT customer_id,
       COUNT(*) AS total_accounts,
       COUNT(CASE WHEN status = 'ACTIVE' THEN 1 END) AS active_accounts,
       COUNT(CASE WHEN status = 'CLOSED' THEN 1 END) AS closed_accounts
FROM accounts
GROUP BY customer_id;
```

## What can go wrong

- **Forgetting that `WHERE` filters before grouping.** Putting `SUM(balance) > 1000` in `WHERE` is a syntax error in strict databases and a silent failure in lenient ones.
- **`LEFT JOIN` plus right-side filter in `WHERE`.** Converts the outer join to an inner join silently. Move the filter to the `ON` clause.
- **Counting the wrong thing.** `COUNT(*)` counts rows; `COUNT(column)` counts non-NULL values. They differ when `column` is nullable.
- **Aggregating across a one-to-many join.** `SUM(a.balance)` where `a` is joined to a one-to-many parent can double-count if the parent has multiple children that match the join.
- **Relying on `GROUP BY` order.** The order of groups in the output is unspecified without `ORDER BY`. Some databases (older MySQL) happened to sort by the GROUP BY columns; PostgreSQL does not.
- **`SELECT *` in production.** Returns every column, including ones added later. Schema changes silently break callers. Always list columns explicitly.
- **Forgetting `LIMIT` on exploratory queries.** A `SELECT` on a 100M-row table without `LIMIT` can saturate the network and the client.
- **Joining on the wrong column.** `JOIN accounts a ON a.id = c.id` (instead of `a.customer_id = c.id`) is a typo that produces results — wrong results.
- **NATURAL JOIN.** Joins on all columns with matching names. Adding a column to one table silently changes the join semantics. Avoid.

## Trade-offs

- **Joins vs denormalization.** A query that joins six tables is correct but slow. Denormalizing (storing the joined data in one table) is faster but harder to keep consistent. See [[02-Denormalization-For-Reads]].
- **`INNER JOIN` vs `LEFT JOIN`.** `INNER JOIN` is simpler and usually faster. `LEFT JOIN` preserves all left rows, including those with no match. Choose deliberately; do not default to one.
- **`GROUP BY` vs window functions.** `GROUP BY` collapses rows; window functions (see [[05-Window-Functions]]) compute aggregates without collapsing. Use `GROUP BY` when you want one row per group; use window functions when you want every row plus an aggregate.
- **`DISTINCT` vs `EXISTS`.** `DISTINCT` removes duplicates; `EXISTS` prevents them. `EXISTS` is usually clearer and sometimes faster.
- **Subquery vs JOIN.** Often equivalent; the optimizer may produce the same plan. Use whichever is clearer.
- **`LIMIT` vs pagination.** `LIMIT n` returns the first n rows; pagination needs `OFFSET` or a keyset. `OFFSET` is O(n); keyset pagination is O(log n). See [[00-Query-Optimization-Strategy]].

## Forward links

- [[04-Subqueries-CTEs]] — composition when joins are not enough.
- [[05-Window-Functions]] — aggregates without collapsing rows.
- [[07-Views-Materialized-Views]] — saving useful SELECTs.
- [[05-Join-Algorithms]] — how the database actually executes a JOIN.
- [[07-Cost-Based-Optimizer]] — how the optimizer chooses a join order.
- [[08-Reading-EXPLAIN]] — seeing the join order in a plan.
- [[09-Banking-SQL]] — the anchor queries in context.
