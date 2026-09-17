# The Relational Model — Codd's Mathematical Foundation

> The whole of relational theory, normalization, SQL semantics, and query optimization rests on one 1970 paper by E. F. Codd. This note establishes what that foundation actually *is*, why it matters, and where SQL departs from it.

## What you already know

From [[02-The-Continuous-Chain]]: every layer refines the one above. The relational model is the layer that turns *persistent data* into something with a mathematical foundation — sets, predicates, and a query algebra.

From [[03-Dependency-As-Root-Concept]]: dependencies are the root force. The relational model gives us a vocabulary for them — **foreign keys**, **functional dependencies**, **join dependencies** — that we will use for the rest of the vault.

From [[04-Abstraction-and-Models]]: a good abstraction hides irrelevant detail for a purpose. The relational model is exactly that — it hides physical storage (files, indexes, pages) and exposes only the *logical* shape of data.

## Why this layer exists

Before 1970, databases were *navigational*. To find a customer's accounts you literally walked a linked list or followed a pointer from one record to the next. The application code had to know the physical layout of the data. Change the layout, change every program.

Codd's insight: data should be presented as **relations**, and queries should be expressed as **logical predicates** over those relations — independent of how the data is stored on disk. The database is then free to choose *any* physical execution strategy (index lookup, sequential scan, hash join) that produces the same answer.

That separation of *logical model* from *physical implementation* is the same separation as **interface from implementation** in OOP — see [[04-Abstraction-and-Models]] and [[02-Encapsulation]]. The relational model is encapsulation, applied to data.

## What is genuinely new

Three things, all formal:

1. **A relation is a subset of a Cartesian product of domains** — a *set*, not a "table." This is the mathematical core.
2. **The model is set-theoretic**: no duplicates, no ordering, no hidden pointers.
3. **SQL is an implementation that deviates** from the model. Knowing where and why is half of being a good database engineer.

## Concepts

### The three layers — model, language, database

Engineers conflate these. They are not the same.

| Layer | What it is | Who defined it |
|---|---|---|
| **The Relational Model** | The mathematical theory: relations, tuples, attributes, domains, constraints, algebra | E. F. Codd (1970) and successors |
| **SQL** | A query language that approximates the model, with deviations (bags, NULLs, ordering) | ANSI/ISO SQL standard |
| **A specific database (PostgreSQL, Oracle, MySQL)** | An implementation of SQL (each with further deviations and extensions) | The vendor |

A `SELECT` in PostgreSQL is *not* the relational model. It is *PostgreSQL's interpretation of SQL's approximation of the relational model.* Three layers of indirection. Knowing which layer a property belongs to is essential — it tells you whether a behavior is mathematical law, language standard, or vendor quirk.

### Relation — the formal definition

Let $D_1, D_2, \ldots, D_n$ be sets (called **domains**). The Cartesian product $D_1 \times D_2 \times \ldots \times D_n$ is the set of all possible tuples $(v_1, v_2, \ldots, v_n)$ with $v_i \in D_i$.

A **relation** $R$ over those domains is any subset of that Cartesian product:

$$R \subseteq D_1 \times D_2 \times \ldots \times D_n$$

That is the entire definition. A relation is just a set of tuples, where each tuple is a value drawn from the specified domains. The number $n$ is the **degree** (or **arity**) of the relation. The number of tuples in $R$ is its **cardinality**.

Two consequences that follow immediately from "it is a set":

1. **No duplicate tuples.** Sets cannot have duplicates. (SQL violates this — see [[01-Relations-Tuples-Attributes]].)
2. **No ordering of tuples.** Sets have no intrinsic order. (SQL violates this with `ORDER BY`, but only at output time — the table itself has no order.)

### Attribute, tuple, domain — the formal vocabulary

- A **domain** $D_i$ is a set of *atomic* values of one type (e.g., the set of all valid IBAN strings, the set of all `NUMERIC(18,2)` values). A domain has an associated type and may have a constraint (e.g., "balance ≥ 0").
- An **attribute** is a named role played by a domain in a relation (e.g., `iban`, `balance`). The name is for human convenience; the underlying domain is what matters.
- A **tuple** is one element of the relation — a single assignment of values to attributes.
- A **relation schema** is the structure: the name plus the ordered list of attribute-domain pairs: `accounts(id: BIGINT, iban: TEXT, balance: NUMERIC(18,2), ...)`.

### Why formalism matters

This is not pedantry. The formal definition is what gives us:

- **Relational algebra** — a set of operators (σ, π, ⨝, ∪, …) closed over relations. Because relations are sets, the algebra has clean algebraic laws (e.g., σ-selection distributes over ⨝-join). Those laws are what a query optimizer uses to rewrite your SQL into a faster plan. See [[04-Relational-Algebra]] and [[07-Cost-Based-Optimizer]].
- **Relational calculus** — a declarative logical notation equivalent in power to the algebra (Codd's theorem). This is the ancestor of SQL. See [[05-Relational-Calculus]].
- **Normalization theory** — functional dependencies, BCNF, 4NF — all defined in terms of relations and constraints. Without the formal model, "normalize until 3NF" is folklore; with it, "BCNF" is a theorem. See [[06-1NF-2NF-3NF]] through [[09-DKNF]].
- **Data independence** — the freedom to change physical storage without changing the logical model. This is the *whole point* of Codd's proposal, and it is why the optimizer exists.

If the model were "a table is a list of rows," none of these would exist. The algebra would not have laws. The optimizer would have nothing to rewrite. Normalization would be opinion.

### The Informal Design Principles (Codd)

Codd also gave informal principles that remain the practical compass for schema design:

1. **Each fact in exactly one place** (no redundancy except where deliberate).
2. **Each relation represents one entity or one relationship** (no "god tables").
3. **NULLs are avoided where possible** (they break two-valued logic — see [[02-Domain-Check-Constraints]]).
4. **The schema should be lossless**: any decomposition can be rejoined to reconstruct the original (see [[07-BCNF]] — lossless join property).

These map directly onto the cohesion/invariant ideas from [[06-Coupling-and-Cohesion]]: a relation should be cohesive (one invariant), and normalization is the algorithm that gets you there.

## Banking application

In our banking system ([[00-Banking-Case-Study]]), the relation `accounts` is, formally:

- Domain $D_{id}$ = the set of all valid `BIGINT` surrogate keys.
- Domain $D_{iban}$ = the set of all valid IBAN strings (conforming to the ISO 13616 format).
- Domain $D_{balance}$ = the set of all `NUMERIC(18,2)` values where `balance >= -overdraft_limit` and (for savings) `balance >= 0`.
- Domain $D_{status}$ = $\{$ `PENDING`, `ACTIVE`, `FROZEN`, `CLOSED` $\}$.
- Domain $D_{customer\_id}$ = the set of all valid customer surrogate keys.

The relation `accounts` is then *any* subset of $D_{id} \times D_{iban} \times D_{balance} \times D_{status} \times D_{customer\_id}$ that satisfies the constraints we declare (PK on `id`, UNIQUE on `iban`, FK on `customer_id`, CHECK on `status`).

The set-theoretic framing matters because it tells us, for example, that two `accounts` rows with the same `id` cannot both exist — by the definition of a set, a tuple either is or is not a member of the relation. The PRIMARY KEY constraint is the schema-level enforcement of that mathematical fact.

## Code

The relational model itself is not SQL. But every schema is an attempt to express it in SQL:

```sql
-- ANSI SQL: an attempt to express a relation
CREATE TABLE accounts (
    id          BIGINT       NOT NULL,
    iban        CHAR(34)     NOT NULL,
    balance     NUMERIC(18,2) NOT NULL,
    status      VARCHAR(16)  NOT NULL,
    customer_id BIGINT       NOT NULL,
    CONSTRAINT accounts_pk PRIMARY KEY (id),
    CONSTRAINT accounts_iban_uk UNIQUE (iban),
    CONSTRAINT accounts_status_ck CHECK (status IN ('PENDING','ACTIVE','FROZEN','CLOSED')),
    CONSTRAINT accounts_balance_ck CHECK (balance >= 0)  -- savings; relaxed for checking
);
```

Already here, the SQL deviates from the model in three ways:

1. `id` is `BIGINT`, but the model only requires that the domain be a set. SQL forces a concrete type.
2. `NULL` is allowed by default unless we write `NOT NULL`. The model has no NULL — Codd's model has a separate "mark" concept that SQL mangled. See [[02-Domain-Check-Constraints]].
3. SQL allows duplicate rows *unless* we declare keys. The model forbids them by definition.

These deviations are not bugs in SQL — they are deliberate compromises (storage efficiency, pragmatic querying). But they are why we must *think* in relations and *write* in SQL with care.

## What can go wrong

- **Treating tables as relations** — leads to duplicate rows that break algebraic identities; e.g., `SELECT customer_id FROM accounts` may return a customer twice, and a `JOIN` against it doubles the result. The fix is `DISTINCT` — a way to claw back set semantics.
- **Treating SQL NULL as a value** — `NULL = NULL` evaluates to UNKNOWN, not TRUE. Three-valued logic infects every query that touches a nullable column. The model has no NULL.
- **Assuming row order** — `SELECT * FROM accounts` has no guaranteed order. The model says so. Yet engineers ship code that depends on it, and it breaks the day the planner changes.
- **Confusing the model with the database** — "PostgreSQL doesn't support CHECK constraints the way I expected" is a *vendor* fact, not a *model* fact. The model is unchanged.

## Trade-offs

- **Formal purity vs. pragmatism.** A truly relational engine (e.g., **Tutorial D**, **Rel**) enforces sets and forbids NULL. SQL chose bags and NULLs because real-world data is messy and queries are cheaper to express that way. The cost is decades of subtle bugs.
- **Data independence vs. physical control.** The model says "you don't get to control the access path." That is the optimizer's job. The trade-off: when the optimizer is wrong, you need escape hatches (hints, materialized views, denormalization). See [[07-Cost-Based-Optimizer]] and [[02-Denormalization-For-Reads]].
- **Simplicity vs. expressiveness.** The model has six core operators. Real SQL has hundreds of features (window functions, CTEs, JSON, arrays). Each adds expressiveness at the cost of deviating further from the clean theory. See [[05-Window-Functions]] and [[04-Subqueries-CTEs]].

## Forward links

- [[01-Relations-Tuples-Attributes]] — the building blocks in detail, and where SQL deviates.
- [[02-Keys-Superkeys-Candidate-Keys]] — identity inside a relation (cross-link [[05-Identity-State-Lifecycle]]).
- [[03-Functional-Dependencies]] — the engine that drives normalization.
- [[04-Relational-Algebra]] and [[05-Relational-Calculus]] — the two formal query languages.
- [[06-1NF-2NF-3NF]] → [[09-DKNF]] — the normal forms, taught in full.
- [[00-Schema-Design]] and [[04-Banking-Schema]] — the SQL realization of the model.
- [[06-Query-Processing-Pipeline]] — where the algebra becomes a plan.
- [[00-ER-Modeling]] and [[01-ER-to-Relational]] — how ER diagrams map onto relations.
