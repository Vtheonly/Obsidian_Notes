# Relational Algebra — The Procedural Query Language

> Relational algebra is the procedural half of Codd's query foundation. It is a small set of operators, closed over relations, that compose into a *tree* — and that tree is exactly what a query planner manipulates. SQL is sugar over this algebra; the optimizer rewrites the tree; the executor runs the leaves. If you can read the algebra, you can read a query plan.

## What you already know

From [[00-Relational-Model]] and [[01-Relations-Tuples-Attributes]]: a relation is a set of tuples, with no duplicates, no order. Operators that take relations and produce relations are *closed* — the output of one operator can be the input of another, and composition is unlimited.

From [[03-Dependency-As-Root-Concept]]: a query that joins two tables creates a runtime dependency — both must be available. The algebra makes that dependency *visible* in the tree.

From [[04-Abstraction-and-Models]]: the algebra is an abstraction — it hides *how* the join is computed (nested loop? hash? merge?) and exposes only *what* the result is. The physical operator is chosen later by the optimizer.

## Why this layer exists

Two reasons:

1. **It is the formal specification of "what a query means."** SQL is defined in terms of relational algebra (modulo bag semantics). To know what `SELECT … FROM … WHERE … GROUP BY …` *means*, you translate it to algebra.
2. **It is the input to the optimizer.** The query planner parses SQL into an algebra tree, then rewrites that tree using algebraic identities (σ distributes over ⨝; π pushes down; etc.). The rewritten tree becomes the physical plan. See [[06-Query-Processing-Pipeline]] and [[07-Cost-Based-Optimizer]].

If you cannot read the algebra, you cannot read `EXPLAIN` output, and you are at the mercy of the optimizer.

## What is genuinely new

Eight **core operators** (σ, π, ⨝, ∪, ∩, −, ×, ρ), five **derived operators** (semijoin, antijoin, outer joins, division), the **algebra-as-tree** picture, and the **SQL-to-algebra translation** map.

## Concepts

### Core operators

Notation: $R$ and $S$ are relations; $A, B$ are attributes; $\theta$ is a comparison operator ($=, <, >, \le, \ge, \ne$); $p$ is a predicate.

| Operator | Symbol | Reads | Returns |
|---|---|---|---|
| Selection | $\sigma_p(R)$ | "select tuples from R where p" | Tuples of R satisfying predicate p |
| Projection | $\pi_A(R)$ | "project R onto attributes A" | The A-subset of each tuple, deduplicated |
| Cartesian product | $R \times S$ | "R cross S" | Every tuple of R paired with every tuple of S |
| Theta-join | $R \bowtie_\theta S$ | "R join S on θ" | $\sigma_\theta(R \times S)$ — i.e., product then filter |
| Natural join | $R \bowtie S$ | "R join S on common attributes" | Theta-join on equality of all shared attribute names, then dedup the shared columns |
| Union | $R \cup S$ | "R or S" | Tuples in R or in S (union-compatible: same attributes) |
| Intersection | $R \cap S$ | "R and S" | Tuples in both R and S (union-compatible) |
| Difference | $R - S$ | "R minus S" | Tuples in R not in S (union-compatible) |
| Rename | $\rho_{S(a_1, \ldots, a_n)}(R)$ | "rename R to S with attributes a_i" | Same tuples, new names |

**Union-compatible** means: same number of attributes, with corresponding attributes drawn from the same domain. You cannot intersect `accounts` and `customers` — they have different schemas.

### Selection — $\sigma$

$$\sigma_{balance > 1000 \land status = \text{'ACTIVE'}}(accounts)$$

Returns the tuples of `accounts` where balance exceeds 1000 and status is ACTIVE. Selection is *horizontal* — it picks rows.

### Projection — $\pi$

$$\pi_{iban, balance}(accounts)$$

Returns only the `iban` and `balance` columns. Projection is *vertical* — it picks columns. Because the result must be a set, projection *deduplicates*: if two tuples have the same `(iban, balance)`, only one survives. In SQL: `SELECT DISTINCT iban, balance FROM accounts` (the `DISTINCT` is what makes it set-theoretic).

### Cartesian product and theta-join

$$accounts \times customers$$

Pairs every account with every customer — usually a disaster (cardinality = |accounts| × |customers|). The useful form is the theta-join, which keeps only the pairs where a condition holds:

$$accounts \bowtie_{accounts.customer\_id = customers.id} customers$$

This is equivalent to $\sigma_{accounts.customer\_id = customers.id}(accounts \times customers)$ — but the optimizer never computes the product first; it computes only the matching pairs. See [[05-Join-Algorithms]].

### Natural join

$$accounts \bowtie customers$$

Joins on the attributes they share (here: `id` — but `accounts.id` and `customers.id` mean different things, so natural join is dangerous with poor naming). Best practice: use *explicit* theta-joins, not natural joins, in real schemas.

### Derived operators

- **Semijoin** $R \ltimes S$: "tuples of R that match some tuple of S." Equivalent to $\pi_R(R \bowtie S)$. Used in distributed queries to avoid shipping whole relations across the network.
- **Antijoin** $R \rhd S$: "tuples of R that match no tuple of S." Equivalent to $R - \pi_R(R \bowtie S)$. SQL's `NOT IN` or `NOT EXISTS`.
- **Left outer join** $R \LOJ S$: all tuples of R, with matching S tuples or NULLs where no match. SQL: `LEFT JOIN`.
- **Right outer join** $R \ROJ S$: symmetric to the above.
- **Full outer join** $R \FOJ S$: all tuples of both, with NULLs where no match. SQL: `FULL OUTER JOIN`.
- **Division** $R \div S$: "tuples of R whose related S-values cover all of S." Used for "find customers who have *all* account types." Rare in practice; usually rewritten with `GROUP BY ... HAVING COUNT(DISTINCT ...) = (SELECT COUNT(*) ...)`.

### The algebra as a tree

Every relational algebra expression is a tree. The leaves are base relations; internal nodes are operators; the root is the result.

Example: "Find the IBANs of ACTIVE accounts owned by customers whose tax_id starts with 'GB'."

$$\pi_{iban}\big(\sigma_{status=\text{'ACTIVE'}}(accounts) \bowtie_{customer\_id=id} \sigma_{tax\_id \text{ LIKE } \text{'GB\%'}}(customers)\big)$$

Tree (read bottom-up):

```
                π (iban)
                   |
                 ⨝ (accounts.customer_id = customers.id)
                /                                  \
        σ (status='ACTIVE')                 σ (tax_id LIKE 'GB%')
               |                                     |
            accounts                               customers
```

This tree is exactly what the planner starts with. The optimizer then *rewrites* it: it might push the σ down, swap the join order, replace ⨝ with a hash join, push π below σ, etc. — all using algebraic identities. The result is the physical plan you see in `EXPLAIN`. See [[06-Query-Processing-Pipeline]] and [[08-Reading-EXPLAIN]].

### SQL-to-algebra translation

| SQL clause | Algebra operator |
|---|---|
| `FROM a, b` (cross) | $a \times b$ |
| `FROM a JOIN b ON p` | $a \bowtie_p b$ |
| `WHERE p` | $\sigma_p$ applied to the FROM-result |
| `SELECT col1, col2` | $\pi_{col1, col2}$ applied to the WHERE-result |
| `GROUP BY col` | (extension: $\gamma_{col, agg}$) — algebra has an aggregation operator |
| `HAVING p` | $\sigma_p$ applied after $\gamma$ |
| `DISTINCT` | explicit deduplication (set semantics) |
| `UNION` / `INTERSECT` / `EXCEPT` | $\cup$ / $\cap$ / $-$ |
| `ORDER BY` | not algebraic — output-only |
| `LIMIT n` | not algebraic — top-k operator |

A complete SQL query maps to one algebra tree. `SELECT DISTINCT iban FROM accounts WHERE status='ACTIVE'` becomes $\pi_{iban}(\sigma_{status=\text{'ACTIVE'}}(accounts))$.

### Bag semantics — the SQL deviation

The algebra is set-based. SQL is bag-based. The translation above is *approximate*:

- $\pi$ in the algebra deduplicates; `SELECT` in SQL does not (unless `DISTINCT`).
- $\cup$ in the algebra deduplicates; `UNION` in SQL does; `UNION ALL` does not.
- $\cap$ and $-$ are similarly affected.

This matters because the optimizer's algebraic identities are *set-theoretic*. When SQL runs in bag mode, some rewrites are not valid (e.g., pushing $\pi$ below $\sigma$ may change the duplicate count). The planner is careful — but understanding *why* it is careful requires knowing the algebra-to-bag gap.

## Banking application

"Find the IBAN and current balance of every ACTIVE account owned by a customer whose status is VERIFIED, ordered by balance descending."

In relational algebra:

$$\pi_{iban, balance}\Big(\sigma_{status=\text{'ACTIVE'}}(accounts) \bowtie_{accounts.customer\_id = customers.id} \sigma_{customer\_status=\text{'VERIFIED'}}(customers)\Big)$$

Tree:

```
              π (iban, balance)
                    |
              ⨝ (accounts.customer_id = customers.id)
             /                                    \
    σ (status='ACTIVE')                   σ (customer_status='VERIFIED')
           |                                          |
        accounts                                  customers
```

In SQL:

```sql
SELECT a.iban, a.balance
FROM accounts a
JOIN customers c ON a.customer_id = c.id
WHERE a.status = 'ACTIVE'
  AND c.customer_status = 'VERIFIED'
ORDER BY a.balance DESC;
```

PostgreSQL parses the SQL into an algebra tree equivalent to the one above, then rewrites it. Two common rewrites the planner might apply:

1. **Predicate pushdown**: move $\sigma_{status=\text{'ACTIVE'}}$ below the join so it filters `accounts` before joining. This reduces the join's input size.
2. **Join reordering**: if `customers` is small and indexed on `customer_status`, the planner may join in the opposite order (filter customers first, then join to accounts via the `customer_id` index).

The final physical plan might look like:

```
Sort (by balance DESC)
  ↳ Hash Join (accounts.customer_id = customers.id)
       ↳ Seq Scan on accounts  (filter: status='ACTIVE')
       ↳ Hash
         ↳ Index Scan on customers (customer_status='VERIFIED')
```

That plan *is* the algebra tree, annotated with physical choices. Read [[08-Reading-EXPLAIN]] for the vocabulary.

## Code

### A more complex query — algebra and SQL side by side

Question: "For each customer with at least one ACTIVE account, find the total balance across their ACTIVE accounts, but only for customers whose total exceeds 10,000."

Algebra (with aggregation operator $\gamma$):

$$\pi_{customer\_id, total}\Big(\sigma_{total > 10000}\big(\gamma_{customer\_id, \text{SUM}(balance) \to total}(\sigma_{status=\text{'ACTIVE'}}(accounts))\big)\Big)$$

SQL:

```sql
SELECT customer_id, SUM(balance) AS total
FROM accounts
WHERE status = 'ACTIVE'
GROUP BY customer_id
HAVING SUM(balance) > 10000;
```

The `WHERE` is the inner σ; the `GROUP BY` is the γ; the `HAVING` is the outer σ; the `SELECT` is the outer π. SQL is the algebra wearing syntax.

### Set operators

```sql
-- Customers who own at least one ACTIVE account AND have a verified status.
-- (intersection)
SELECT customer_id FROM accounts WHERE status = 'ACTIVE'
INTERSECT
SELECT id FROM customers WHERE customer_status = 'VERIFIED';

-- Customers who own NO account. (difference / antijoin)
SELECT id FROM customers
WHERE id NOT IN (SELECT customer_id FROM accounts WHERE customer_id IS NOT NULL);

-- Equivalent using NOT EXISTS (preferred — NULL-safe):
SELECT c.id FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a WHERE a.customer_id = c.id
);
```

PostgreSQL-specific: PostgreSQL's `EXPLAIN` output uses the algebra's vocabulary directly — `Seq Scan`, `Index Scan`, `Hash Join`, `Nested Loop`, `Sort`, `Aggregate`, `HashAggregate`. Learn to read these — they are the algebra in textual form.

## What can go wrong

- **Cartesian product by accident.** `FROM a, b` without a join condition produces $a \times b$. SQL accepts it; the result is usually wrong and very slow. Always use explicit `JOIN ... ON`.
- **Projection that drops a column you need.** $\pi$ is lossy. If you project away `customer_id` then try to join, you cannot. The optimizer is smart but cannot recover information that has been projected away.
- **Treating `LEFT JOIN` as `INNER JOIN`.** The outer-join preserves unmatched rows with NULLs; downstream predicates on the right side then eliminate them again (because `NULL = anything` is UNKNOWN). The result is silently equivalent to an inner join — but slower.
- **`NOT IN` with NULLs.** As discussed in [[01-Relations-Tuples-Attributes]], `NOT IN (subquery)` returns no rows if the subquery produces any NULL. Use `NOT EXISTS` — it is the antijoin, correctly.
- **Natural join on misnamed columns.** Two tables that both have an `id` column will natural-join on `id` — almost always wrong. Always specify the join condition explicitly.

## Trade-offs

- **Algebraic purity vs. SQL's pragmatism.** The algebra has no `NULL`, no `ORDER BY`, no bag semantics. SQL added all three because real queries need them. The cost is that the optimizer must track three-valued logic and bag cardinalities.
- **Join order freedom vs. optimizer trust.** The algebra is associative and commutative for inner joins ($\bowtie$), so the planner is free to reorder. But for outer joins, reordering changes the result. The planner is conservative; sometimes you can help by restructuring the SQL.
- **Declarative vs. procedural.** The algebra is *procedural* — it specifies an order. SQL is *declarative* — it specifies a result. The optimizer's job is to find the best procedure for the declaration. If you write procedural SQL (forcing join order, using subqueries as if they were loops), you fight the optimizer. See [[07-Cost-Based-Optimizer]].

## Forward links

- [[05-Relational-Calculus]] — the declarative counterpart; Codd's theorem proves equivalence.
- [[00-SQL-From-Relational-Algebra]] — the algebra-to-SQL translation in detail.
- [[03-Select-Join-Group]] — SQL `SELECT`, `JOIN`, `GROUP BY` in practice.
- [[05-Join-Algorithms]] — the physical realizations of $\bowtie$.
- [[06-Query-Processing-Pipeline]] — how SQL becomes a plan.
- [[07-Cost-Based-Optimizer]] — algebraic rewriting for performance.
- [[08-Reading-EXPLAIN]] — reading the algebra in PostgreSQL output.
- [[00-Banking-Case-Study]] — the queries above run on this system.
