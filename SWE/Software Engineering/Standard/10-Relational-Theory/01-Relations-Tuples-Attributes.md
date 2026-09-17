# Relations, Tuples, Attributes — and Where SQL Deviates

> The vocabulary of the relational model is small: relation, tuple, attribute, domain, degree, cardinality. But each term carries a precise mathematical meaning that SQL quietly violates. Knowing the violations is what separates a working SQL user from a database engineer.

## What you already know

From [[00-Relational-Model]]: a relation is a subset of a Cartesian product of domains. It is a set, not a "table." SQL is an implementation that deviates from the model in specific, documented ways.

From [[05-Identity-State-Lifecycle]]: identity in object land is memory reference; identity in database land is the primary key. Here we look at the *structure* those identities live in.

From [[06-Coupling-and-Cohesion]]: a relation should be cohesive — it should hold one fact type. This note defines what a "fact type" is, structurally.

## Why this layer exists

Every later chapter — algebra, normalization, query optimization — assumes you can reason about relations *as sets* and not be confused by SQL's bag semantics. If you skip this, you will write queries that produce duplicate rows unexpectedly, violate your own constraints unknowingly, and misunderstand why `DISTINCT` exists.

The layer exists to install the *mental model* the rest of the chapter relies on.

## What is genuinely new

The formal definitions of relation, tuple, attribute, and domain — and the **four specific ways SQL deviates** from those definitions. Memorize the deviations; they are the source of most subtle SQL bugs.

## Concepts

### Relation

A **relation** is a set of tuples all sharing the same set of attributes. Formally (from [[00-Relational-Model]]):

$$R \subseteq D_1 \times D_2 \times \ldots \times D_n$$

A relation has:

- A **name** (e.g., `accounts`).
- A fixed set of **attributes** (the columns).
- A **degree** (or **arity**): the number of attributes, $n$.
- A **cardinality**: the number of tuples currently in the relation. Cardinality changes as rows are inserted or deleted; degree is fixed by the schema.

A relation is a *predicate*: each tuple is a true statement of the predicate "this account exists with these attribute values." This is why relations and logic are inseparable — see [[05-Relational-Calculus]].

### Tuple

A **tuple** is one element of the relation. It is an ordered (mathematically) or named (in practice) assignment of values to attributes:

$$(id=1042,\ iban=\text{'GB29...'},\ balance=1500.00,\ status=\text{'ACTIVE'},\ customer\_id=701)$$

Two tuples are equal iff they agree on every attribute value. A tuple is *atomic* in the sense that you do not partially update a tuple — you replace it (SQL's `UPDATE` is logically a `DELETE` + `INSERT` of the changed tuple; the model has no half-updated tuple).

### Attribute

An **attribute** is a (name, domain) pair. The name is what humans use; the domain is what the model cares about. Two relations can have attributes with the same name but different domains (e.g., `accounts.id : BIGINT` vs. `transfers.id : UUID`). The model cares about the domain, not the name.

### Domain

A **domain** is the set of allowed values for an attribute, plus the operations defined on them. Domains are more than types:

- `iban`'s domain is not just "text" — it is "strings matching ISO 13616 IBAN format, with valid checksum."
- `balance`'s domain is not just "numeric" — it is "NUMERIC(18,2) values ≥ -overdraft_limit."
- `status`'s domain is the enumerated set $\{$ `PENDING`, `ACTIVE`, `FROZEN`, `CLOSED` $\}$.

A good schema declares the domain as tightly as possible. SQL's `CHECK` constraints are the schema's way of expressing domain restrictions — see [[02-Domain-Check-Constraints]].

### Degree and cardinality — easy to confuse

- **Degree / arity**: number of *attributes* (columns). Fixed by the schema. A relation with 5 columns has degree 5, forever.
- **Cardinality**: number of *tuples* (rows). Changes over time. A relation with 5 million rows has cardinality 5,000,000 today and 5,000,001 tomorrow.

These matter because they have very different effects on query cost. Degree affects row width (and thus I/O per row). Cardinality affects the number of rows the optimizer must estimate — see [[07-Cost-Based-Optimizer]].

### Relation variable (relvar) vs. relation value

This is a subtle but important distinction from Date and Darwen:

- A **relation value** (or "relval") is a particular set of tuples at a particular moment.
- A **relation variable** (or "relvar") is a *named container* whose value is a relval; `UPDATE`, `INSERT`, `DELETE` change the relval inside the relvar.

When we say "the `accounts` relation," we usually mean the relvar. The value changes constantly; the variable is the schema-level thing. SQL has no explicit term for this — it just calls both "the table." That ambiguity causes confusion when we discuss "the schema" vs. "the data."

## The four SQL deviations

SQL deviates from the relational model in four documented ways. Each one is a deliberate engineering compromise, and each one creates bugs if you forget it.

### 1. SQL tables are *bags*, not sets

The model says: a relation is a set; duplicate tuples cannot exist. SQL says: a table may contain duplicate rows unless you explicitly forbid them with `UNIQUE` or `PRIMARY KEY`.

```sql
-- Without a UNIQUE constraint, this is legal:
INSERT INTO t (x) VALUES (1), (1), (1);
-- Now SELECT x FROM t returns three rows of 1.
```

Consequence: algebraic identities break. In the model, $R \cup R = R$ (idempotence of union). In SQL, `SELECT x FROM t UNION SELECT x FROM t` returns distinct rows; `SELECT x FROM t UNION ALL SELECT x FROM t` returns duplicates. `UNION` and `UNION ALL` are *different operators* because of bag semantics.

Practical rule: when you care about correctness of cardinality (e.g., counting customers), use `DISTINCT`. When you want set semantics across a join's output, also use `DISTINCT`. But not always — sometimes the duplicates *are* the answer (e.g., "show me every order line, even if two products are identical").

### 2. SQL allows NULL — the model has no NULL

The model has no concept of "missing." A tuple is an assignment of values to all attributes. If an attribute has no value, the tuple does not belong to the relation.

SQL introduced `NULL` as a placeholder for "unknown," "missing," or "not applicable" — three different concepts collapsed into one symbol. Worse, SQL uses **three-valued logic**: any comparison involving `NULL` evaluates to `UNKNOWN`, not `TRUE` or `FALSE`.

```sql
SELECT * FROM accounts WHERE balance > 0;
-- Does NOT return rows where balance IS NULL.
-- Because (NULL > 0) is UNKNOWN, and only TRUE qualifies.
```

Consequence: `NOT IN` is dangerous with nullable subqueries; `NOT EXISTS` is safer. `COUNT(*)` counts rows including NULLs; `COUNT(col)` skips NULLs. Every aggregate has its own NULL semantics. See [[02-Domain-Check-Constraints]] and [[03-Select-Join-Group]].

The fix is to make every column `NOT NULL` unless you have a specific reason not to. Defaults, sentinels, and separate child tables (`overdraft_limit` in a `checking_accounts` table only) are often better than NULL.

### 3. SQL permits ordering — the model forbids it

A set has no intrinsic order. A relation's tuples have no "first" or "last." But SQL lets you write `ORDER BY` and the result has an order.

That order is a property of the *output cursor*, not of the *table*. The table itself remains unordered — `SELECT * FROM accounts` without `ORDER BY` can return rows in any order, and that order can change between executions (the planner may pick a different access path; vacuum may compact the table; etc.).

Practical rule: any query whose *correctness* depends on row order must have an `ORDER BY`. Pagination without `ORDER BY` is a bug. "It worked in dev" is not a guarantee — see [[06-Query-Processing-Pipeline]].

### 4. SQL has columns, not (named) attributes

In the model, an attribute is identified by name within the relation. SQL adds two confusions:

- **Anonymous columns**: `SELECT 1+1` produces a column with no name. The model requires named attributes.
- **Duplicate column names**: `SELECT a.id, b.id FROM a JOIN b ON ...` produces two columns both called `id`. SQL allows this (some dialects auto-rename, some do not). The model does not.

Practical rule: always alias your columns in production SQL, especially across joins. `AS account_id` and `AS customer_id` make the output unambiguous and the application code that consumes it stable.

## Banking application

The `accounts` relation in our banking system ([[00-Banking-Case-Study]]) has degree 5 and cardinality (say) 2.4 million:

| id | iban | balance | status | customer_id |
|---|---|---|---|---|
| 1042 | GB29NWBK60161331926819 | 1500.00 | ACTIVE | 701 |
| 1043 | GB29NWBK60161331926820 | -200.00 | ACTIVE | 702 |
| 1044 | GB29NWBK60161331926821 | 9050.00 | FROZEN | 703 |

Formally:

- Degree 5: `{id, iban, balance, status, customer_id}`.
- Cardinality 3 (in this toy example).
- Each tuple is a statement of the predicate: "Account `id` with IBAN `iban` has balance `balance`, status `status`, and is owned by customer `customer_id`."
- The domain of `status` is the enumerated set; the domain of `balance` excludes values that would violate the CHECK constraint.

In SQL, the relation is approximated by the `accounts` table, with the deviations noted: technically duplicate rows *could* exist if we forgot `PRIMARY KEY (id)` (we did not), `NULL`s *could* appear in `status` if we forgot `NOT NULL` (we did not), and `ORDER BY` is needed whenever the application code depends on order.

## Code

```sql
-- A relation expressed in SQL (with all the deviations made explicit)
CREATE TABLE accounts (
    id          BIGINT        NOT NULL,                 -- attribute, domain BIGINT, NOT NULL (no NULLs)
    iban        CHAR(34)      NOT NULL,                 -- attribute, domain: ISO 13616 IBAN
    balance     NUMERIC(18,2) NOT NULL,                 -- attribute, domain: NUMERIC(18,2)
    status      VARCHAR(16)   NOT NULL,                 -- attribute, domain: 4-value enum
    customer_id BIGINT        NOT NULL,
    CONSTRAINT accounts_pk      PRIMARY KEY (id),        -- enforces set semantics on (id)
    CONSTRAINT accounts_iban_uk UNIQUE (iban),           -- enforces set semantics on (iban)
    CONSTRAINT accounts_status_ck CHECK (status IN ('PENDING','ACTIVE','FROZEN','CLOSED')),
    CONSTRAINT accounts_balance_ck CHECK (
        (status = 'SAVINGS' AND balance >= 0)
        OR status IN ('CHECKING','FROZEN','CLOSED','PENDING','ACTIVE')
    )
);

-- A relation-valued expression in SQL
SELECT iban, balance
FROM accounts
WHERE status = 'ACTIVE'
ORDER BY balance DESC;   -- ORDER BY at output only; the table itself is unordered
```

PostgreSQL-specific: PostgreSQL enforces `PRIMARY KEY` and `UNIQUE` via B-tree indexes by default and treats `NULL` as distinct in `UNIQUE` constraints (so multiple `NULL`s are allowed — a deviation from the standard). See [[03-B-Tree-Indexes]].

## What can go wrong

- **Duplicate rows silently appearing** in a `JOIN` because of bag semantics, doubling your count. Add `DISTINCT` or restructure the join.
- **`NOT IN` with NULLs** returning zero rows because `(x NOT IN (1, 2, NULL))` is `UNKNOWN` for any `x` not in `{1, 2}`. Use `NOT EXISTS` instead.
- **Assuming insertion order** = `SELECT` order. It is not. Even without an `ORDER BY`, the planner may use an index that returns rows in index order — which can change after a `VACUUM` or an index rebuild.
- **Two columns named `id`** in a join result, breaking the consuming code when the driver picks one arbitrarily. Alias everything.
- **NULLs in a UNIQUE column** silently allowing duplicates you did not expect. In standard SQL, `UNIQUE` ignores NULLs; in PostgreSQL, multiple NULLs are allowed.

## Trade-offs

- **Set purity vs. storage cost.** Forcing sets everywhere would require an implicit deduplication on every `SELECT`, which is expensive. SQL leaves deduplication to the programmer (`DISTINCT`). The cost is that you must remember to use it.
- **No NULL vs. real-world missing data.** Some attributes genuinely do not apply to every tuple (e.g., `overdraft_limit` only applies to checking accounts). The model's answer is decomposition (a separate `checking_accounts` table); SQL's answer is NULL. Both have costs — decomposition requires an extra join, NULL requires three-valued logic. See [[07-BCNF]].
- **Strict typing vs. flexibility.** Declaring a tight domain (e.g., `status IN ('PENDING','ACTIVE','FROZEN','CLOSED')`) catches bugs but makes schema evolution harder (adding `'SUSPENDED'` requires a migration). The trade-off is data integrity vs. changeability.

## Forward links

- [[02-Keys-Superkeys-Candidate-Keys]] — identity inside a relation.
- [[03-Functional-Dependencies]] — the constraints that drive normalization.
- [[04-Relational-Algebra]] — operators on relations, and where SQL's bag semantics change the math.
- [[00-Schema-Design]] and [[01-Primary-Foreign-Keys]] — schema realization.
- [[02-Domain-Check-Constraints]] — enforcing domains.
- [[05-Identity-State-Lifecycle]] — the identity concept that ties this to OOP.
- [[00-Banking-Case-Study]] — the anchor.
