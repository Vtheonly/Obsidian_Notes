# Subqueries and CTEs

> When a single `SELECT` is not enough. Subqueries nest one query inside another; CTEs (Common Table Expressions, the `WITH` clause) name them and let you compose them. Recursive CTEs unlock hierarchies and graphs — the things SQL was not originally designed to do.

## What you already know

From [[03-Select-Join-Group]]: a SELECT returns a table; that table can be the input to another SELECT. From [[00-SQL-From-Relational-Algebra]]: relational algebra is *closed* — every operator's output is a relation, ready to be the next operator's input. Subqueries and CTEs are SQL's way of expressing that closure. From [[04-Relational-Algebra]]: the algebra has a selection (σ), a projection (π), and a join (⨝) — and it has *derivations* built by composition.

## Why this layer exists

Real queries are rarely flat. "Find customers whose total balance is above average" requires computing the average first, then comparing each customer to it. "Find accounts whose owner has at least one closed account" requires a lookup against accounts grouped by customer. "Compute a hierarchy" requires walking a tree. SQL needs a way to compose queries — and a way to make that composition readable.

## What is genuinely new here

The new idea is **named composition**. A CTE gives a name to a sub-result, so the main query reads top-to-bottom like a recipe. A recursive CTE adds the ability to express iteration declaratively — something the relational model was not designed for, but SQL:1999 added.

## Concepts

### Scalar subqueries

A subquery that returns one row, one column. Used where a scalar value is expected:

```sql
SELECT iban, balance
FROM accounts
WHERE balance > (SELECT AVG(balance) FROM accounts);
```

The subquery `SELECT AVG(balance) FROM accounts` is evaluated once (the optimizer may cache it) and its result is used in the outer `WHERE`. If the subquery returns no rows, the value is NULL; if it returns more than one row, it is an error.

### Correlated subqueries

A subquery that references a column from the outer query. Evaluated once per outer row:

```sql
SELECT a.iban, a.balance,
       (SELECT SUM(amount) FROM ledger_entries le
        WHERE le.account_id = a.id) AS ledger_sum
FROM accounts a;
```

The inner query references `a.id` from the outer query. Conceptually, the database runs the inner query once per row of `accounts`. In practice, the optimizer may transform this into a join (see [[07-Cost-Based-Optimizer]]).

Correlated subqueries are expressive but can be slow if the optimizer cannot transform them. A `LEFT JOIN` with `GROUP BY` is often equivalent and faster.

### EXISTS / NOT EXISTS

Tests whether a subquery returns any rows. Used for "has at least one" or "has no":

```sql
-- Customers who have at least one ACTIVE account
SELECT c.id, c.legal_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM accounts a
    WHERE a.customer_id = c.id AND a.status = 'ACTIVE'
);

-- Customers who have NEVER had a CLOSED account
SELECT c.id, c.legal_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a
    WHERE a.customer_id = c.id AND a.status = 'CLOSED'
);
```

`EXISTS` is often clearer than a `JOIN` with `DISTINCT`, and can be faster — the database stops scanning as soon as it finds one matching row.

### IN / NOT IN

Tests membership in a list. `IN` with a subquery is similar to `EXISTS`, but with a subtle NULL trap:

```sql
-- WRONG: if any account.status is NULL, NOT IN returns no rows at all
SELECT c.legal_name FROM customers c
WHERE c.id NOT IN (SELECT customer_id FROM accounts WHERE status = 'CLOSED');

-- CORRECT: use NOT EXISTS instead
SELECT c.legal_name FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a
    WHERE a.customer_id = c.id AND a.status = 'CLOSED'
);
```

The NULL trap: `x NOT IN (a, b, NULL)` evaluates to `x <> a AND x <> b AND x <> NULL`, which is `unknown` if x is not equal to a or b. The whole `WHERE` becomes unknown, and the row is excluded. **Use `NOT EXISTS` for negation; reserve `NOT IN` for known-non-NULL lists.**

### CTEs (WITH clause)

A CTE names a subquery so the main query can reference it:

```sql
WITH active_accounts AS (
    SELECT id, customer_id, balance
    FROM accounts
    WHERE status = 'ACTIVE'
),
customer_totals AS (
    SELECT customer_id, SUM(balance) AS total
    FROM active_accounts
    GROUP BY customer_id
)
SELECT c.legal_name, ct.total
FROM customers c
JOIN customer_totals ct ON ct.customer_id = c.id
WHERE ct.total > 100000;
```

Benefits:

- **Readability.** The query reads top-to-bottom like a recipe.
- **Reuse.** A CTE can be referenced multiple times in the main query without re-typing.
- **Recursion.** A CTE can reference itself (see below).

Pre-PostgreSQL-12, CTEs were *optimization fences* — the optimizer treated each CTE as a materialized intermediate. This meant CTEs could be slower than equivalent subqueries. PostgreSQL 12+ inlines non-recursive CTEs by default, removing this penalty. Use `MATERIALIZED` to force materialization when you want the fence.

```sql
-- PostgreSQL 12+: force materialization (optimization fence)
WITH expensive_filter AS MATERIALIZED (
    SELECT ... FROM big_table WHERE ...
)
SELECT ... FROM expensive_filter WHERE ...;
```

### Recursive CTEs

A recursive CTE has two parts: a *base case* (non-recursive) and a *recursive case* (which references the CTE itself):

```sql
WITH RECURSIVE countdown(n) AS (
    SELECT 10              -- base case
    UNION ALL
    SELECT n - 1 FROM countdown WHERE n > 1   -- recursive case
)
SELECT n FROM countdown;
```

The database evaluates the base case, then repeatedly applies the recursive case to the previous result, until no new rows are produced. The result is the union of all iterations.

Recursive CTEs are how SQL handles:

- **Hierarchies** — employee → manager, category → parent category, account → parent account.
- **Graphs** — find all accounts reachable from a starting account through a chain of transfers.
- **Fixed-point computations** — compound interest, PageRank-style iterations.

### Recursive CTE — anatomy

```sql
WITH RECURSIVE name(columns) AS (
    -- Anchor: non-recursive seed
    SELECT ... FROM ... WHERE ...
    UNION [ALL]
    -- Recursive: references name
    SELECT ... FROM name JOIN ... WHERE ...
)
SELECT ... FROM name;
```

- The anchor produces the initial set.
- The recursive step produces the next set from the previous one.
- `UNION ALL` allows duplicates (faster); `UNION` deduplicates (slower).
- Termination is guaranteed when the recursive step produces no new rows.

### When to use a CTE vs a subquery vs a view

- **Subquery**: used once, simple. Inline; no name.
- **CTE**: used once but complex, or used multiple times in the same query. Named; scoped to the query.
- **View** (see [[07-Views-Materialized-Views]]): used across many queries. Named; persisted in the schema.

## Banking application

### Query 1: accounts whose balance disagrees with the ledger (reconciliation)

```sql
WITH ledger_sums AS (
    SELECT account_id, SUM(amount) AS ledger_total
    FROM ledger_entries
    GROUP BY account_id
)
SELECT a.id, a.iban, a.balance, COALESCE(ls.ledger_total, 0) AS ledger_total,
       a.balance - COALESCE(ls.ledger_total, 0) AS discrepancy
FROM accounts a
LEFT JOIN ledger_sums ls ON ls.account_id = a.id
WHERE a.balance - COALESCE(ls.ledger_total, 0) <> 0;
```

The CTE makes the query readable: first compute ledger sums, then compare. Without the CTE, the same query is a correlated subquery or a nested `FROM (SELECT ...)`.

### Query 2: compound interest via recursive CTE

```sql
-- PostgreSQL: compute 30 days of daily compound interest on savings
WITH RECURSIVE daily_balance(day, account_id, balance) AS (
    -- Anchor: today's balance for each savings account
    SELECT 0, a.id, a.balance
    FROM accounts a
    JOIN savings_accounts sa ON sa.account_id = a.id
    WHERE a.status = 'ACTIVE'

    UNION ALL

    -- Recursive: previous day's balance plus daily interest
    SELECT db.day + 1, db.account_id,
           db.balance * (1 + (SELECT interest_rate FROM savings_accounts
                              WHERE account_id = db.account_id) / 365.0)
    FROM daily_balance db
    WHERE db.day < 30
)
SELECT account_id, day, ROUND(balance, 2) AS projected_balance
FROM daily_balance
ORDER BY account_id, day;
```

The CTE iterates 30 times, projecting the balance forward by one day each time. This is the kind of computation that would otherwise require procedural code.

### Query 3: transfer chains (find a cycle)

```sql
-- PostgreSQL: find transfer chains up to 5 hops deep from a starting account
WITH RECURSIVE transfer_chain(hop, from_acct, to_acct, transfer_id, amount) AS (
    -- Anchor: transfers from the starting account
    SELECT 1, t.from_account_id, t.to_account_id, t.id, t.amount
    FROM transfers t
    WHERE t.from_account_id = $1 AND t.status = 'COMPLETED'

    UNION ALL

    -- Recursive: transfers from the destination of the previous hop
    SELECT tc.hop + 1, t.from_account_id, t.to_account_id, t.id, t.amount
    FROM transfers t
    JOIN transfer_chain tc ON tc.to_acct = t.from_account_id
    WHERE tc.hop < 5 AND t.status = 'COMPLETED'
)
SELECT * FROM transfer_chain ORDER BY hop;
```

This walks the graph of completed transfers up to 5 hops from a starting account. Useful for fraud detection: "where did the money go?"

### Query 4: top-N per group (without window functions)

```sql
-- Find the three largest transfers per customer
WITH ranked_transfers AS (
    SELECT t.id, t.amount, t.from_account_id,
           c.id AS customer_id, c.legal_name,
           ROW_NUMBER() OVER (PARTITION BY c.id ORDER BY t.amount DESC) AS rn
    FROM transfers t
    JOIN accounts a ON a.id = t.from_account_id
    JOIN customers c ON c.id = a.customer_id
    WHERE t.status = 'COMPLETED'
)
SELECT customer_id, legal_name, id AS transfer_id, amount
FROM ranked_transfers
WHERE rn <= 3
ORDER BY customer_id, rn;
```

This combines a CTE with a window function (see [[05-Window-Functions]]). The CTE makes the structure readable; the window function does the ranking.

## Code — common CTE patterns

```sql
-- Pattern 1: split a complex query into named stages
WITH active_customers AS (
    SELECT id, legal_name FROM customers WHERE status = 'VERIFIED'
),
their_active_accounts AS (
    SELECT a.* FROM accounts a
    JOIN active_customers c ON c.id = a.customer_id
    WHERE a.status = 'ACTIVE'
)
SELECT * FROM their_active_accounts;

-- Pattern 2: CTE referenced multiple times
WITH period_totals AS (
    SELECT account_id, SUM(amount) AS total
    FROM ledger_entries
    WHERE occurred_at >= date_trunc('month', now()) - interval '1 month'
      AND occurred_at <  date_trunc('month', now())
    GROUP BY account_id
)
SELECT a.iban, pt.total AS last_month,
       (SELECT total FROM period_totals pt2
        WHERE pt2.account_id = a.id
        -- previous month referenced again
       ) AS two_months_ago
FROM accounts a
JOIN period_totals pt ON pt.account_id = a.id;

-- Pattern 3: recursive CTE for hierarchy
WITH RECURSIVE category_tree(id, name, depth, path) AS (
    SELECT id, name, 0, name::TEXT
    FROM categories WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.name, ct.depth + 1, ct.path || ' > ' || c.name
    FROM categories c
    JOIN category_tree ct ON ct.id = c.parent_id
)
SELECT * FROM category_tree ORDER BY path;
```

## What can go wrong

- **`NOT IN` with NULLs.** As described above — silently returns no rows. Use `NOT EXISTS`.
- **Correlated subquery performance.** If the optimizer cannot transform it, it runs per-row. Check the plan (see [[08-Reading-EXPLAIN]]).
- **Recursive CTE without a termination condition.** The recursion runs forever. Always include a `WHERE` in the recursive step that eventually excludes all rows.
- **`UNION` vs `UNION ALL` in recursive CTEs.** `UNION` deduplicates; for graph traversal, you usually want `UNION ALL` plus a visited-set check, or `UNION` plus a depth limit.
- **CTE materialization surprises (pre-PG-12).** A CTE that was an optimization fence becomes inline in PG-12+. If you depended on the fence, add `MATERIALIZED`.
- **Recursive CTEs that exceed memory.** Each iteration's rows are kept. Deep or wide recursions can blow up. Use `LIMIT` or a depth bound.
- **Subqueries returning more than one row.** A scalar subquery that returns multiple rows is an error. Use `IN`, `EXISTS`, or aggregate to one row.
- **Column aliases referenced too early.** You cannot reference a CTE's column alias inside the CTE that defines it. Define aliases in the CTE header.

## Trade-offs

- **CTE vs subquery vs view.** CTEs are scoped to a query; subqueries are inline; views are persisted. Choose based on reuse: once → subquery; once-but-complex → CTE; many queries → view.
- **Recursive CTE vs procedural code.** The CTE is declarative and runs in the database; procedural code is more flexible but requires a round-trip. Use the CTE for traversal; switch to procedural code for complex business logic.
- **`UNION ALL` vs `UNION`.** `UNION ALL` is faster (no dedup); `UNION` is correct when duplicates would be wrong. Default to `ALL` and add dedup only when needed.
- **`MATERIALIZED` vs inlined CTE.** Materialized is a fence (predictable, possibly slower); inlined is optimizer-friendly (possibly faster, possibly re-evaluated). Force materialization when you want to control the plan.
- **Correlated subquery vs JOIN.** The JOIN is usually faster (the optimizer can choose join order); the correlated subquery is sometimes clearer. Try both; check the plan.

## Forward links

- [[05-Window-Functions]] — another way to express "top-N per group" and "running totals."
- [[07-Views-Materialized-Views]] — CTEs that persist across queries.
- [[06-Query-Processing-Pipeline]] — how the database plans a CTE.
- [[07-Cost-Based-Optimizer]] — how CTEs are inlined or materialized.
- [[08-Reading-EXPLAIN]] — seeing CTEs in a plan.
- [[09-Banking-SQL]] — recursive CTEs for interest accrual and transfer chains.
