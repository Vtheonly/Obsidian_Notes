# Primary and Foreign Keys

> The schema's most consequential decisions. The primary key answers *who are you?*; the foreign key answers *who do you depend on?* Both are applications of the five forces — identity and dependency — at the schema layer.

## What you already know

From [[05-Identity-State-Lifecycle]]: every entity has three flavors of identity — object, logical, surrogate. The primary key is the schema's choice of identity. From [[03-Dependency-As-Root-Concept]]: a dependency is "a change in one place can force a change in another." A foreign key is a dependency *the database will enforce*. From [[06-Coupling-and-Cohesion]]: dependencies should point toward stability. In schemas, that means foreign keys should point toward the most stable tables. From [[02-Keys-Superkeys-Candidate-Keys]]: a candidate key is a minimal unique attribute set; the primary key is the candidate key we picked.

## Why this layer exists

Without primary keys, rows have no identity: two identical rows are indistinguishable, and `UPDATE` cannot target one without targeting both. Without foreign keys, references are unenforced: any row can claim to belong to a parent that does not exist. The two together turn a pile of tables into a *connected, integrity-checked graph*.

## What is genuinely new here

The genuinely new idea is **referential integrity as a runtime guarantee enforced by the DBMS**. The application does not have to check "does this customer exist before inserting this account?" The database refuses the insert if the customer does not exist. No bug in any client can produce a dangling reference. This is constraint-as-encapsulation (see [[02-Encapsulation]]), at the strongest layer.

## Concepts

### Primary key

A primary key is:

- **Unique** — no two rows share the same value.
- **Non-null** — every row has one.
- **Minimal** — no column can be removed while preserving uniqueness (it is a candidate key, not just a superkey).
- **Stable** — the value does not change over the row's lifetime (this is a *design* property, not enforced by SQL).

There can be only one primary key per table, but there can be many `UNIQUE NOT NULL` constraints serving the same role.

### Surrogate vs natural keys

| Aspect | Surrogate | Natural |
|---|---|---|
| Example | `BIGINT GENERATED ALWAYS AS IDENTITY` | `iban`, `tax_id`, `isbn` |
| Meaning | None — generated token | Domain-meaningful |
| Stability | Never changes | Can change (rarely) |
| Size | Small, fixed | Variable |
| Index performance | Excellent (monotonic) | Depends on shape |
| Coupling | Loose — internal to DB | Tight — external systems depend on it |
| Updates | Never cascades | Cascades to all FK references |

The vault's standard pattern: **surrogate PK + natural UNIQUE constraint**. Foreign keys use the surrogate; humans and external systems use the natural key. The two are bridged by the unique constraint.

### Foreign key

A foreign key declares: *this column's values must match the primary key (or any unique column) of that other table*. The declaration has two halves:

- The *reference* (this column → that table's PK).
- The *policy* for what happens when the referenced row is deleted or updated.

### ON DELETE / ON UPDATE behaviors

| Behavior | Meaning |
|---|---|
| `RESTRICT` | Disallow the delete/update if any referencing row exists. Error. |
| `NO ACTION` | Same as `RESTRICT` in effect, but checked at end of statement (allows intermediate violations within a transaction). Default in PostgreSQL. |
| `CASCADE` | Propagate: delete the referencing rows automatically. |
| `SET NULL` | Set the FK column to NULL on the referencing row (requires the column to be nullable). |
| `SET DEFAULT` | Set the FK column to its declared default on the referencing row. |

`CASCADE` is the most dangerous — it can erase a tree of data with one `DELETE`. Use it only when the referencing rows are truly owned by the parent (a composition relationship in UML terms — see [[00-Object-Relationships]]). For most relationships, `RESTRICT` is the safer default; the application must explicitly delete dependents first, in the order it chooses.

### Direction follows stability

From [[03-Dependency-As-Root-Concept]]: dependencies should point toward stability. In schema terms, the foreign key points from the *less stable* table to the *more stable* table. `accounts.customer_id → customers.id` because accounts come and go but customers (mostly) stay. `ledger_entries.account_id → accounts.id` because ledger entries are immutable append-only (see [[04-Domain-Events]]); accounts can be closed but ledger entries never change. The dependency arrow points toward the most stable, most appended-to, least-deleted table.

### Cycles and how to break them

A cyclic foreign-key graph (A → B → A) means neither row can be inserted first without temporarily violating referential integrity. SQL handles this by deferring constraint checks to commit time (`DEFERRABLE INITIALLY DEFERRED` in PostgreSQL), but the underlying design smell is real. The cure is the same as in code (see [[06-Coupling-and-Cohesion]]): introduce an intermediary table that both originals reference, breaking the cycle.

In the Banking case study, the most common cycle temptation is `accounts.default_counterparty_id → accounts.id` (an account that names its default transfer partner). The right fix: extract the relationship into a `counterparties` table that both accounts reference.

## Banking application

```sql
-- PostgreSQL DDL, focusing on keys

CREATE TABLE customers (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tax_id      TEXT NOT NULL UNIQUE,
    legal_name  TEXT NOT NULL
);

CREATE TABLE accounts (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id   BIGINT NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    iban          TEXT NOT NULL UNIQUE,
    status        TEXT NOT NULL CHECK (status IN ('PENDING','ACTIVE','FROZEN','CLOSED')),
    balance       NUMERIC(18,2) NOT NULL DEFAULT 0
);

CREATE TABLE ledger_entries (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_id    BIGINT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    amount        NUMERIC(18,2) NOT NULL CHECK (amount <> 0),
    occurred_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE transfers (
    id                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    from_account_id   BIGINT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    to_account_id     BIGINT NOT NULL REFERENCES accounts(id) ON DELETE RESTRICT,
    amount            NUMERIC(18,2) NOT NULL CHECK (amount > 0),
    status            TEXT NOT NULL CHECK (status IN ('PENDING','COMPLETED','FAILED','FRAUD_REVIEW')),
    idempotency_key   TEXT NOT NULL UNIQUE,
    CHECK (from_account_id <> to_account_id)
);
```

Notice the rules expressed purely by keys:

- `customers.id` is a surrogate PK; `tax_id` is the natural identity exposed to the world.
- `accounts.customer_id` is `ON DELETE RESTRICT` — you cannot delete a customer who still owns accounts.
- `ledger_entries.account_id` is `ON DELETE RESTRICT` — you cannot delete an account that still has ledger entries (which is correct: ledger entries are immutable history; see [[04-Domain-Events]]).
- `transfers.idempotency_key` is `UNIQUE` — enforces invariant 7 of [[00-Banking-Case-Study]].
- The `CHECK (from_account_id <> to_account_id)` prevents a self-transfer at the schema level — no application code needed.
- `transfers.from_account_id` and `to_account_id` both reference `accounts.id` — the same table can be referenced by multiple FKs from the same child.

## Code — breaking a cycle with an intermediary

Suppose accounts can name a "default transfer counterparty" for convenience. The naive version creates a cycle:

```sql
-- BAD: self-referential cycle through accounts
ALTER TABLE accounts ADD COLUMN default_counterparty_id BIGINT REFERENCES accounts(id);
-- This works in SQL, but the design is fragile: deleting the counterparty
-- account forces a SET NULL or RESTRICT, and the relationship is implicit.
```

The clean version extracts the relationship:

```sql
-- GOOD: explicit relationship table
CREATE TABLE account_counterparties (
    account_id        BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    counterparty_id   BIGINT NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    label             TEXT,
    PRIMARY KEY (account_id, counterparty_id),
    CHECK (account_id <> counterparty_id)
);
```

Now the relationship is first-class: it can carry attributes (a label, a created-at, a fraud score), and the cycle is gone.

## What can go wrong

- **Natural keys that change.** Using `email` as a primary key breaks the moment a user changes their email. Every foreign key must cascade, or the update fails.
- **Surrogate keys that leak.** Auto-increment integers reveal insertion order and rough volume. UUID v7 or ULID avoids this if it matters.
- **`ON DELETE CASCADE` as a default.** A single `DELETE FROM customers WHERE id = 42` can wipe out accounts, ledger entries, transfers, statements, and notifications in one statement. Use cascade only on true composition relationships.
- **Foreign keys that point the wrong way.** If `customers` references `accounts` (instead of the other way around), a customer cannot exist without an account, and deleting an account deletes the customer. The dependency direction was inverted.
- **Missing foreign keys.** A schema with column names like `customer_id` but no `REFERENCES` clause is a schema that trusts the application. It will eventually be wrong.
- **UUID v4 in a B-tree primary key.** Random inserts cause page splits and fragmentation. Prefer UUID v7, ULID, or sequential BIGINT.
- **Forgetting that primary keys imply an index.** Every PK creates a unique B-tree (see [[03-B-Tree-Indexes]]). Adding a second unique index on the natural key gives you two indexes to maintain.

## Trade-offs

- **Surrogate vs natural** — already discussed. The default is surrogate + natural UNIQUE.
- **`RESTRICT` vs `CASCADE`** — RESTRICT is safer; CASCADE is convenient. Default to RESTRICT; promote to CASCADE only when the child is genuinely owned by the parent.
- **Single-column vs composite primary keys.** Single-column surrogate keys are easier for ORMs (see [[00-ORM-Impedance-Mismatch]]) and smaller in indexes. Composite natural keys express the domain more directly but make every foreign key wider. Choose per table.
- **`DEFERRABLE` vs immediate checks.** Deferred constraints allow temporary violations within a transaction. Useful for cycles and for bulk loads; dangerous because it delays error reporting.
- **Foreign keys vs application-level integrity.** FKs are stronger (no client can bypass them) but slower on writes (the DB must check the parent row). High-throughput systems sometimes drop FKs and enforce integrity in the app — trading safety for speed. This is almost always a mistake in OLTP systems; sometimes acceptable in OLAP.

## Forward links

- [[02-Domain-Check-Constraints]] — the other half of declarative integrity.
- [[04-Banking-Schema]] — the full schema with all keys in place.
- [[02-Keys-Superkeys-Candidate-Keys]] — the formal background.
- [[00-ORM-Impedance-Mismatch]] — how ORMs map (and sometimes fight) primary keys.
- [[02-Aggregates]] — aggregate boundaries in DDD often align with cascade boundaries in schema.
- [[01-Indexing-Strategy]] — primary keys and unique constraints are indexes; choose their shape carefully.
