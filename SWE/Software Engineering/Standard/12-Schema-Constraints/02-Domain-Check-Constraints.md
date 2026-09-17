# Domain and Check Constraints

> Constraints that the database will enforce on every row, every transaction, every client, forever. `NOT NULL`, `CHECK`, `UNIQUE`, and (PostgreSQL) `EXCLUDE` are the declarative tools that turn a schema from a pile of typed columns into a *domain contract*.

## What you already know

From [[02-Encapsulation]]: encapsulation is protecting invariants by hiding state behind an interface. The schema version of encapsulation is *declaring invariants the database will refuse to violate*. From [[00-Banking-Case-Study]]: the system has ten domain invariants. Each one must be enforced somewhere; the cheapest place is the schema. From [[06-1NF-2NF-3NF]] and [[07-BCNF]]: a well-designed relation has every non-key attribute depend on the whole key and nothing else. Constraints make the *allowed values* of those attributes explicit. From [[08-Trade-offs-Everywhere]]: declarative constraints are cheap at runtime and hard to change; triggers are flexible at runtime and expensive to debug. The trade-off is real.

## Why this layer exists

An application can check `balance >= -overdraft_limit` before writing. But:

- A different application (a migration script, a maintenance console, a future microservice) might not.
- The check might be skipped under a code path the original author forgot.
- The check might race with a concurrent transaction and see a stale balance.

A `CHECK` constraint removes all three failure modes by moving the check into the database itself. The database is the *only* layer that sees every write from every client. Declaring a constraint there is the only way to make it universal.

## What is genuinely new here

The new idea is **declarative integrity enforced by the DBMS, independent of any client**. A CHECK is not "a hint to the application"; it is a hard refusal. The constraint and the data live together; you cannot have one without the other.

## Concepts

### NOT NULL

The simplest constraint, and the most underused. `NOT NULL` says: every row must have a value for this column. The presence of NULL is not "no value" in a clean sense — it is *unknown*, and unknown propagates through arithmetic and comparisons in surprising ways (see [[01-Relations-Tuples-Attributes]] for the three-valued logic that results).

A schema with many nullable columns is a schema with many "we don't know" states. Each nullable column is a code path the application must handle. The rule: if a value is required for the row to be meaningful, make it `NOT NULL`. Default to non-null; allow null only when the absence is genuinely meaningful (e.g., `closed_at` is NULL until the account is closed).

### CHECK

A CHECK constraint is a boolean expression that must evaluate to true (or unknown — which is treated as passing) for every row. Examples:

```sql
balance >= 0
status IN ('PENDING','ACTIVE','FROZEN','CLOSED')
amount > 0
start_date <= end_date
email ~ '^[^@]+@[^@]+$'    -- PostgreSQL: ~ is regex match
```

CHECK constraints are:

- **Per-row** — evaluated on INSERT and UPDATE.
- **Cheap** — no locking beyond the row itself, no cross-table lookups.
- **Composable** — multiple CHECKs on the same column are AND-ed together.
- **Limited** — they cannot reference other rows, other tables, or subqueries. (They can call immutable functions in PostgreSQL, which is a useful escape hatch but should be used sparingly.)

### UNIQUE

A UNIQUE constraint says: no two rows can share the same value(s) for this column set. In SQL, UNIQUE allows multiple NULLs (a long-standing debate; the SQL standard treats NULLs as distinct for UNIQUE). PostgreSQL follows this rule.

UNIQUE can be:

- **Single-column** — `iban TEXT UNIQUE`.
- **Composite** — `UNIQUE (customer_id, label)` — two counterparties can have the same label only if they belong to different customers.
- **Partial** (PostgreSQL) — `UNIQUE (iban) WHERE status <> 'CLOSED'` — only non-closed accounts must have unique IBANs (allows reusing an IBAN after closure if your regulator permits).

Every UNIQUE constraint creates a B-tree index (see [[03-B-Tree-Indexes]]).

### EXCLUDE (PostgreSQL)

`EXCLUDE` generalizes UNIQUE. Where UNIQUE says "no two rows have equal values," EXCLUDE says "no two rows satisfy this operator." The classic use is range overlap:

```sql
-- PostgreSQL: prevent overlapping interest-rate periods for the same account
CREATE TABLE savings_rates (
    account_id   BIGINT REFERENCES accounts(id),
    rate         NUMERIC(5,4) NOT NULL,
    valid_during DATERANGE NOT NULL,
    EXCLUDE USING gist (account_id WITH =, valid_during WITH &&)
);
```

This says: no two rows for the same account can have overlapping `valid_during` ranges. UNIQUE cannot express this. EXCLUDE with the GiST index on ranges is the right tool. Outside of range/schedule problems, EXCLUDE is rare.

### Domain constraints as the schema's invariant enforcement

From [[02-Encapsulation]]: an invariant is a property that must always hold. The schema layer enforces invariants declaratively:

| Domain invariant (Banking) | Schema constraint |
|---|---|
| Balance never goes below `-overdraft_limit` | `CHECK (balance >= -overdraft_limit)` on accounts (or per subtype) |
| IBAN is unique | `UNIQUE (iban)` |
| Account status is one of four values | `CHECK (status IN (...))` |
| Ledger entry amount is non-zero | `CHECK (amount <> 0)` |
| Transfer amount is positive | `CHECK (amount > 0)` |
| No self-transfers | `CHECK (from_account_id <> to_account_id)` |
| Idempotency keys are unique | `UNIQUE (idempotency_key)` |

Each of these is a single line of SQL. None require triggers. None require application code. They are enforced at every write, by every client, forever.

### CHECK vs trigger

| Aspect | CHECK | Trigger |
|---|---|---|
| Scope | One row | One row, a statement, or a transaction |
| Cross-table | No | Yes |
| Cross-row | No (mostly) | Yes |
| Time-dependent | No | Yes |
| Performance | Cheap (per-row, no lookups) | Expensive (can run arbitrary SQL) |
| Discoverability | Inline with table definition | Separate object, easy to miss |
| Debugging | Easy — error names the constraint | Hard — trigger fires invisibly |
| Test surface | Schema introspection | Application behavior |

The rule: **prefer CHECK; use triggers only when CHECK cannot express the rule** (cross-row, cross-table, time-dependent). See [[03-Triggers-As-Constraints]] for the escape hatch.

## Banking application

```sql
-- PostgreSQL DDL with rich declarative constraints

CREATE TABLE accounts (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id     BIGINT NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    iban            TEXT NOT NULL,
    account_type    TEXT NOT NULL CHECK (account_type IN ('CHECKING','SAVINGS')),
    status          TEXT NOT NULL CHECK (status IN ('PENDING','ACTIVE','FROZEN','CLOSED')),
    balance         NUMERIC(18,2) NOT NULL DEFAULT 0,
    overdraft_limit NUMERIC(18,2) NOT NULL DEFAULT 0,
    opened_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at       TIMESTAMPTZ,
    -- Invariant: balance respects the overdraft limit
    CONSTRAINT balance_within_limit CHECK (balance >= -overdraft_limit),
    -- Invariant: closed_at is null until the account is closed
    CONSTRAINT closed_at_consistency CHECK (
        (status = 'CLOSED' AND closed_at IS NOT NULL)
        OR (status <> 'CLOSED' AND closed_at IS NULL)
    ),
    -- IBAN uniqueness only for non-closed accounts (regulator permits reuse)
    CONSTRAINT unique_active_iban UNIQUE (iban) DEFERRABLE INITIALLY IMMEDIATE
);

-- Partial unique index: only one active account per IBAN at a time
-- PostgreSQL: partial index
CREATE UNIQUE INDEX idx_accounts_unique_iban_active
    ON accounts (iban)
    WHERE status <> 'CLOSED';

CREATE TABLE ledger_entries (
    id             BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id     BIGINT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    amount         NUMERIC(18,2) NOT NULL,
    occurred_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- Amount cannot be zero (a zero entry is meaningless)
    CONSTRAINT amount_nonzero CHECK (amount <> 0),
    -- Precision: amounts must be whole cents
    CONSTRAINT amount_whole_cents CHECK (amount * 100 = floor(amount * 100))
);

CREATE TABLE transfers (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    from_account_id BIGINT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    to_account_id   BIGINT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    amount          NUMERIC(18,2) NOT NULL,
    status          TEXT NOT NULL CHECK (status IN ('PENDING','COMPLETED','FAILED','FRAUD_REVIEW')),
    idempotency_key TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    -- Invariant: amount is strictly positive
    CONSTRAINT amount_positive CHECK (amount > 0),
    -- Invariant: no self-transfers
    CONSTRAINT no_self_transfer CHECK (from_account_id <> to_account_id),
    -- Invariant: idempotency keys are unique
    CONSTRAINT unique_idempotency UNIQUE (idempotency_key)
);
```

Each constraint encodes one of the ten invariants from [[00-Banking-Case-Study]]. The application can still check them (for friendly error messages), but the database is the final authority.

## Code — when CHECK is not enough

The `closed_at_consistency` CHECK above is the *most* CHECK can do: a row-level condition between two columns of the same row. But it cannot express:

- "Closed accounts cannot receive new ledger entries." (Cross-row, cross-table.)
- "A transfer's two ledger entries must sum to zero." (Cross-row.)
- "An account cannot be frozen for longer than 90 days without review." (Time-dependent.)

These need triggers (see [[03-Triggers-As-Constraints]]) or application-level enforcement. The trade-off: triggers are flexible but invisible; application checks are visible but bypassable. Defense in depth uses both.

## What can go wrong

- **`NOT NULL` added late.** Adding `NOT NULL` to an existing column requires backfilling every existing row. Migrations that forget this fail mid-deploy.
- **CHECK that references a function.** A CHECK like `CHECK (validate_iban(iban))` works, but if `validate_iban` is later changed, existing rows may suddenly violate the constraint. Mark such functions `IMMUTABLE` and never change them.
- **CHECK that depends on time.** `CHECK (created_at <= now())` is invalid in PostgreSQL because `now()` is not immutable. Time-dependent rules need triggers.
- **NULL semantics in UNIQUE.** Two rows with `iban = NULL` are allowed by UNIQUE. If NULL is not a meaningful state, the column should be `NOT NULL`.
- **CHECK that depends on another row.** SQL CHECK cannot say "this account's balance equals the sum of its ledger entries." That invariant is enforced by the application, by triggers, or by a materialized view that audits it.
- **Performance cliffs.** Complex CHECKs on hot tables slow every insert and update. Keep CHECKs simple and deterministic.
- **Constraints that conflict.** A CHECK that says `balance >= 0` and another that says `balance >= -overdraft_limit` are fine together. But a CHECK that says `status = 'CLOSED'` while a trigger is trying to set `status = 'ACTIVE'` will fire errors that look mysterious.

## Trade-offs

- **Strictness vs flexibility.** A schema that enforces every invariant declaratively is safer but harder to evolve. A schema that defers everything to the application is flexible but eventually inconsistent. Default to strict; relax only with documented justification.
- **Inline vs out-of-band.** Inline CHECK constraints are part of the table definition and discoverable. Triggers (see [[03-Triggers-As-Constraints]]) are out-of-band and easy to miss. Inline when possible.
- **Partial vs full UNIQUE.** Partial unique indexes (PostgreSQL) allow rules like "only active accounts need unique IBANs." They are more expressive but harder for ORM tools to introspect.
- **DEFERRABLE vs immediate.** Deferred constraints allow temporary violations within a transaction. Useful for cycles and bulk loads; costs you early error detection.
- **Speed vs safety.** Every constraint slows writes slightly. In a high-throughput OLTP system, this adds up. The right answer is almost never "remove the constraint"; it is "make the constraint cheaper" (simpler expression, indexed lookup, or partial constraint).

## Forward links

- [[03-Triggers-As-Constraints]] — when CHECK cannot express the rule.
- [[04-Banking-Schema]] — full Banking DDL with all constraints inline.
- [[02-Encapsulation]] — the same force at the code layer.
- [[00-ACID]] — constraints are part of the C (consistency) in ACID.
- [[08-Reading-EXPLAIN]] — constraint checks appear in query plans.
- [[01-DDL]] — the SQL syntax for declaring these constraints.
