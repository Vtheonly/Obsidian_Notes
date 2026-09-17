# Relational Calculus — The Declarative Counterpart

> Relational calculus is the other half of Codd's query foundation: a *declarative* notation in which you describe the result you want, not the procedure to compute it. Codd's theorem proves calculus and algebra are equivalent in expressive power. SQL is roughly tuple relational calculus with bag semantics and three-valued logic. Understanding this lineage explains why SQL looks the way it does.

## What you already know

From [[04-Relational-Algebra]]: relational algebra is *procedural* — you compose operators into a tree that specifies *how* to compute the result. The optimizer rewrites that tree.

From [[04-Abstraction-and-Models]]: declarative and procedural are two abstractions of the same thing. A declarative spec says *what*; a procedural spec says *how*. Both compute the same answer; the choice is about which layer you commit to.

From [[03-Dependency-As-Root-Concept]]: SQL `WHERE` clauses are predicates — logical formulas. Predicates are the building block of calculus.

## Why this layer exists

Two reasons:

1. **It is the theoretical ancestor of SQL.** SQL's `SELECT-FROM-WHERE` is syntactic sugar for a tuple relational calculus expression. Knowing the calculus explains why SQL is the shape it is.
2. **It establishes the equivalence of declarative and procedural query languages.** Codd's theorem says: anything you can express in algebra, you can express in calculus, and vice versa. That equivalence is what justifies having a query *optimizer* at all — the optimizer can rewrite your declarative SQL into any equivalent procedural plan, because the two are provably the same.

## What is genuinely new

Two formal languages:

1. **Tuple Relational Calculus (TRC)**: $\{t \mid P(t)\}$ — "the set of tuples $t$ such that predicate $P$ holds."
2. **Domain Relational Calculus (DRC)**: $\{\langle x_1, \ldots, x_n \rangle \mid P(x_1, \ldots, x_n)\}$ — "the set of value-tuples where predicate $P$ holds."

And **Codd's theorem**: TRC, DRC, and relational algebra are equivalent in expressive power (for *safe* formulas).

This chapter is shorter than the algebra chapter — the calculus is conceptually simpler; the heavy lifting was in [[04-Relational-Algebra]].

## Concepts

### Tuple Relational Calculus (TRC)

A TRC expression has the form:

$$\{t \mid P(t)\}$$

where $t$ is a tuple variable (ranging over tuples of some relation) and $P$ is a predicate built from:

- Atomic formulas: $t \in R$ ("t is in relation R"), $t.a \theta s.b$ (compare attribute $a$ of $t$ to attribute $b$ of $s$).
- Logical connectives: $\land$ (and), $\lor$ (or), $\lnot$ (not).
- Quantifiers: $\exists s \, (P(s))$ ("there exists a tuple s such that..."), $\forall s \, (P(s))$ ("for all tuples s...").

Example: "The IBAN and balance of all active accounts."

$$\{t \mid t \in accounts \land t.status = \text{'ACTIVE'}\}$$

Read: "the set of tuples $t$ such that $t$ is an account and $t$'s status is ACTIVE." The result is a set of full account tuples; you then project onto `(iban, balance)` if needed (TRC allows attribute selection in the result shape).

### Domain Relational Calculus (DRC)

In DRC, the variables range over *domains* (values), not tuples. An expression has the form:

$$\{\langle x_1, x_2, \ldots, x_n \rangle \mid P(x_1, x_2, \ldots, x_n)\}$$

The same query in DRC:

$$\{\langle i, b \rangle \mid \exists s, c \, (\langle id, i, b, s, c \rangle \in accounts \land s = \text{'ACTIVE'})\}$$

Read: "the set of pairs $\langle i, b \rangle$ such that there exist $s, c$ making $\langle id, i, b, s, c \rangle$ an account with status ACTIVE." DRC is more verbose but more "atomic" — it reasons about values, not tuples.

DRC is the conceptual ancestor of **Query-by-Example (QBE)**, the visual query language. TRC is the conceptual ancestor of SQL.

### Safety

Both TRC and DRC admit expressions that define *infinite* sets — e.g., $\{t \mid \lnot (t \in accounts)\}$ "all tuples that are NOT accounts" is infinite (it ranges over the universe of possible tuples). Such expressions are **unsafe**.

A calculus expression is **safe** if every variable in it is *range-restricted* — bound to a finite relation or to equality with such a bound variable. Codd's theorem applies only to safe expressions.

SQL is implicitly safe: every column referenced in `SELECT` or `WHERE` must come from a table in `FROM`. You cannot write `SELECT * WHERE NOT EXISTS (SELECT 1 FROM accounts)` in standard SQL — there is no `FROM`, hence no range restriction.

### Codd's theorem

> **For every safe TRC expression, there is an equivalent relational algebra expression, and vice versa.**

This is the *relational completeness* theorem. It says the procedural and declarative styles are equivalent in power. SQL is *relationally complete* (it can express anything the algebra can), plus it adds a few extras (aggregation, bag semantics, recursion via CTEs in modern SQL).

The practical consequence: a query optimizer is free to translate your SQL into any equivalent algebra tree, because the equivalence is mathematically guaranteed. The optimizer's job is to find the *cheapest* equivalent tree, not to discover one — there always is one.

## Banking application

Query: "Find the IBANs of accounts whose customer is VERIFIED."

In **TRC**:

$$\{t.iban \mid t \in accounts \land \exists c \, (c \in customers \land c.id = t.customer\_id \land c.customer\_status = \text{'VERIFIED'})\}$$

In **relational algebra** (for comparison):

$$\pi_{iban}\big(accounts \bowtie_{accounts.customer\_id = customers.id \land customers.customer\_status = \text{'VERIFIED'}} customers\big)$$

In **SQL**:

```sql
SELECT a.iban
FROM accounts a
WHERE EXISTS (
    SELECT 1 FROM customers c
    WHERE c.id = a.customer_id
      AND c.customer_status = 'VERIFIED'
);

-- Or equivalently, using a join:
SELECT a.iban
FROM accounts a
JOIN customers c ON c.id = a.customer_id
WHERE c.customer_status = 'VERIFIED';
```

Notice that SQL is a near-verbatim translation of the TRC formula. The `EXISTS` form mirrors TRC's $\exists c$; the `JOIN` form mirrors the algebra's $\bowtie$. Both compute the same set.

A query with universal quantification ("customers who hold accounts of *all* types"):

In **TRC**:

$$\{c \mid c \in customers \land \forall t \, (t \in account\_types \Rightarrow \exists a \, (a \in accounts \land a.customer\_id = c.id \land a.type = t.name))\}$$

In **SQL** (using `NOT EXISTS` to express universal quantification — a standard idiom):

```sql
SELECT c.*
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM account_types t
    WHERE NOT EXISTS (
        SELECT 1 FROM accounts a
        WHERE a.customer_id = c.id
          AND a.type = t.name
    )
);
```

`∀x P(x)` is equivalent to `¬∃x ¬P(x)`. SQL has no `FORALL` keyword; the `NOT EXISTS ... NOT EXISTS` double negation is how SQL expresses universal quantification. This is a direct inheritance from TRC.

## Code

```sql
-- TRC: { t | t ∈ accounts ∧ t.balance > 1000 ∧ t.status = 'ACTIVE' }
-- SQL:
SELECT * FROM accounts
WHERE balance > 1000 AND status = 'ACTIVE';

-- TRC with existential: "accounts whose customer is verified"
-- { a | a ∈ accounts ∧ ∃c (c ∈ customers ∧ c.id = a.customer_id ∧ c.verified = TRUE) }
SELECT a.*
FROM accounts a
WHERE EXISTS (
    SELECT 1 FROM customers c
    WHERE c.id = a.customer_id AND c.verified = TRUE
);

-- TRC with universal: "customers who have ALL account types"
-- { c | c ∈ customers ∧ ∀t (t ∈ account_types ⇒ ∃a (a ∈ accounts ∧ a.customer_id = c.id ∧ a.type = t.name)) }
SELECT c.*
FROM customers c
WHERE NOT EXISTS (
    SELECT 1 FROM account_types t
    WHERE NOT EXISTS (
        SELECT 1 FROM accounts a
        WHERE a.customer_id = c.id AND a.type = t.name
    )
);
```

PostgreSQL-specific: PostgreSQL also supports the `ALL` subquery operator, which can express some universal queries more directly:

```sql
SELECT c.*
FROM customers c
WHERE c.id = ALL (
    SELECT a.customer_id FROM accounts a WHERE a.type = ANY (SELECT name FROM account_types)
);
-- But the NOT EXISTS form is more readable and more general.
```

Modern PostgreSQL also supports recursive CTEs, which extend SQL beyond relational completeness into computationally complete queries (e.g., transitive closure). See [[04-Subqueries-CTEs]].

## What can go wrong

- **Unsafe expressions** in TRC produce infinite sets. SQL avoids this by requiring `FROM` — but you can still write queries with subtle scoping bugs (e.g., correlated subqueries that reference columns from outer queries unexpectedly).
- **Universal quantification via `NOT IN`** is unsafe in the presence of NULLs. `WHERE x NOT IN (subquery)` returns no rows if the subquery yields any NULL. Use `NOT EXISTS` instead — it is the correct translation of $\lnot\exists$.
- **Three-valued logic** in SQL means predicates evaluate to TRUE, FALSE, or UNKNOWN. The calculus uses two-valued logic. SQL `WHERE` keeps only TRUE; `CHECK` keeps TRUE and UNKNOWN. The mismatch causes bugs — see [[02-Domain-Check-Constraints]].
- **Correlated subqueries** that look like calculus are often slow if the planner fails to decorrelate them. Modern planners can rewrite `EXISTS` into a semi-join; older planners may not. See [[07-Cost-Based-Optimizer]].
- **Bag semantics** break the equivalence theorem. The theorem is for *sets*; SQL is for *bags*. SQL with `DISTINCT` everywhere is closer to calculus; without `DISTINCT`, the algebra of bags has fewer identities (e.g., $\sigma$ no longer distributes cleanly across $\cup$).

## Trade-offs

- **Declarative vs. procedural.** Calculus is declarative (what); algebra is procedural (how). SQL chose declarative because it is more user-friendly and lets the optimizer choose the how. The trade-off: when the optimizer is wrong, you need escape hatches (hints, materialized views, denormalization).
- **Calculus purity vs. SQL's extensions.** SQL added aggregation, sorting, NULL, bag semantics, and recursion. Each addition breaks some algebraic identity. The trade-off is expressive power vs. clean theory.
- **Universal quantification idioms.** `NOT EXISTS ... NOT EXISTS` is correct but cryptic. `GROUP BY ... HAVING COUNT(DISTINCT ...) = (SELECT COUNT(*) ...)` is more readable but expresses the same idea procedurally. Pick the form your team can maintain.

## Forward links

- [[04-Relational-Algebra]] — the procedural counterpart; this chapter is its mirror.
- [[00-SQL-From-Relational-Algebra]] — how SQL translates into algebra and calculus.
- [[03-Select-Join-Group]] — SQL `SELECT`, `JOIN`, and `GROUP BY` in practice.
- [[04-Subqueries-CTEs]] — subqueries (correlated `EXISTS`) and CTEs as the modern SQL expression of TRC.
- [[06-Query-Processing-Pipeline]] — how SQL is parsed, validated, and optimized.
- [[07-Cost-Based-Optimizer]] — how equivalent algebra trees are explored.
- [[00-Banking-Case-Study]] — the queries above run on this system.
