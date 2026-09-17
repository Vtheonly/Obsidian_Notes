# DKNF — Domain-Key Normal Form

> Domain-Key Normal Form (Fagin, 1981) is the "ultimate" normal form. It says: every constraint on the relation is a logical consequence of domain constraints and key constraints. DKNF is rarely achievable in practice, but it is the *goal* that tells us what "fully normalized" really means. Without it, the normal-form hierarchy lacks a summit.

## What you already know

From [[06-1NF-2NF-3NF]] through [[08-4NF-5NF]]: the normal forms are a sequence of increasingly strict constraints on the FDs, MVDs, and JDs of a relation. Each form removes a class of redundancy.

From [[02-Domain-Check-Constraints]] (forward): a domain constraint restricts the values an attribute may take; a key constraint asserts uniqueness. These are the two *primitive* constraint types in the relational model.

From [[03-Dependency-As-Root-Concept]]: a constraint is a dependency — "this cannot be true unless that is also true." DKNF asks: can all constraints be reduced to the two simplest kinds?

## Why this layer exists

The normal forms from 1NF to 5NF each target a *specific* dependency type (FD, MVD, JD). But real schemas have *other* constraints: arbitrary `CHECK` constraints, complex multi-attribute rules, business invariants that span tables. None of the named normal forms address these.

DKNF is the *general* statement: a relation is "fully normalized" when *every* constraint — including the arbitrary ones — follows from just domain and key constraints. If you can achieve DKNF, you need no triggers, no application-level checks, no complex assertions; the schema itself enforces all invariants.

This is rarely achievable. But as a *goal*, it tells you what to aim for: reduce every constraint to the simplest form the database can enforce natively. The closer you get, the fewer triggers you need and the more invariants the DB guarantees.

## What is genuinely new

- The **definition** of DKNF.
- The recognition that DKNF is *not* a strict superset of the lower normal forms in the usual sense — a DKNF relation is automatically in 5NF (and below), but a 5NF relation is not necessarily in DKNF.
- Why DKNF is rarely achievable: most real schemas have constraints that cannot be reduced to domain + key.
- The *value* of DKNF as a goal: it tells you what to push into the schema vs. what to enforce in code.

This chapter is brief — DKNF is more compass than destination.

## Concepts

### The formal definition

A relation $R$ is in **Domain-Key Normal Form (DKNF)** iff every constraint on $R$ is a logical consequence of:

1. **Domain constraints** — each attribute's value must belong to its declared domain (type + value restrictions).
2. **Key constraints** — certain attribute sets are unique (candidate keys) and certain attributes reference keys in other relations (foreign keys).

That is it. If every constraint you care about — FDs, MVDs, JDs, business rules — can be derived from domain and key constraints alone, the relation is in DKNF.

### What DKNF implies

A DKNF relation:

- Has no insertion, update, or deletion anomalies (those would be constraints not captured by domain/key).
- Has no redundancy that is not implied by the keys.
- Enforces all its invariants declaratively — no triggers, no application checks.

DKNF subsumes 5NF (and thus 4NF, BCNF, 3NF, 2NF, 1NF). Any DKNF relation is automatically in 5NF, because 5NF's constraints (JDs) are constraints, and DKNF requires them to be consequences of domain/key.

The reverse is not true: a 5NF relation may have a `CHECK` constraint that is not a consequence of domain/key, and thus is not DKNF.

### Why DKNF is rarely achievable

Most real schemas have constraints that cannot be reduced to domain + key. Examples:

- **Cross-row constraints**: "the sum of ledger entries for an account must equal the account's balance." This is not a domain or key constraint; it requires a trigger or a periodic check.
- **Temporal constraints**: "an account cannot be closed if it has a non-zero balance." A `CHECK` on `status = 'CLOSED'` would not capture this without referencing other rows.
- **Conditional constraints**: "checking accounts must have an overdraft_limit; savings accounts must not." This is a domain constraint *if* you model `overdraft_limit` as a nullable column with a CHECK, but it is a constraint that crosses columns and is awkward to express as pure domain + key.
- **Cross-table constraints**: "an account's currency must equal the customer's country currency." Foreign keys cannot express this.

The standard pattern is:

- Domain and key constraints in the schema (NOT NULL, CHECK, UNIQUE, FK).
- Anything beyond that in triggers or application code.
- Periodic reconciliation jobs for constraints that span rows or tables (e.g., balance vs. sum of ledger entries).

DKNF is achievable only for relations whose *only* constraints are domain and key. Most real relations have more.

### The value of DKNF as a goal

Even though you cannot always reach DKNF, aiming for it tells you where to put each constraint:

- **Push into domain/key constraints** whenever possible. `NOT NULL`, `CHECK (status IN (...))`, `UNIQUE`, `FOREIGN KEY` are cheap, declarative, and always-on.
- **Push into triggers** only when the constraint cannot be expressed as domain/key. Triggers are expensive to reason about and invisible to the optimizer.
- **Push into application code** only when the constraint spans multiple systems or requires external state (e.g., "this IBAN exists in the SWIFT registry").
- **Run as a reconciliation job** when the constraint is too expensive to check synchronously (e.g., "sum of ledger entries equals balance" — checked nightly, with discrepancies logged).

The closer to DKNF, the more invariants the database guarantees on its own. The further from DKNF, the more invariants depend on application discipline — which is fragile.

## Banking application

The banking system ([[00-Banking-Case-Study]]) has many constraints. Let's classify them:

| Constraint | Type | Where enforced |
|---|---|---|
| `accounts.id` is unique | Key | Schema (PK) — DKNF-compatible |
| `accounts.iban` is unique | Key | Schema (UNIQUE) — DKNF-compatible |
| `accounts.status ∈ {PENDING, ACTIVE, FROZEN, CLOSED}` | Domain | Schema (CHECK) — DKNF-compatible |
| `accounts.balance` is `NUMERIC(18,2)` | Domain | Schema (type) — DKNF-compatible |
| `accounts.customer_id` references `customers.id` | Key (FK) | Schema (FK) — DKNF-compatible |
| Savings balance ≥ 0 | Domain (conditional) | Schema (CHECK) — DKNF-compatible |
| Account cannot be CLOSED if balance ≠ 0 | Cross-row | Trigger or app — *not* DKNF-compatible |
| Sum of ledger entries = balance | Cross-row | Trigger or reconciliation — *not* DKNF-compatible |
| A transfer's debit and credit must sum to zero | Cross-row | Trigger or app — *not* DKNF-compatible |
| Frozen accounts cannot withdraw | Cross-row + state | Trigger or app — *not* DKNF-compatible |

The first six constraints are domain/key — they fit DKNF. The last four are not — they require triggers or application checks.

A DKNF-compliant design would *try* to push the cross-row constraints into the schema. Some can be:

- "Frozen accounts cannot withdraw" can be partially enforced by a trigger on `ledger_entries` that rejects negative entries for frozen accounts.
- "Sum of ledger entries = balance" can be enforced by *not storing* balance at all — compute it on read. That is DKNF-pure but slow; the trade-off is normalization vs. read performance (see [[10-Normalization-Trade-offs]]).

The realistic banking schema accepts partial DKNF: domain/key constraints where possible, triggers for cross-row invariants, reconciliation for performance-critical denormalizations.

## Code

```sql
-- A DKNF-adjacent banking schema fragment
-- Every constraint here is domain or key.

CREATE TABLE customers (
    id         BIGINT       NOT NULL,
    legal_name VARCHAR(255) NOT NULL,
    tax_id     VARCHAR(32)  NOT NULL,
    country    CHAR(2)      NOT NULL,    -- ISO 3166-1 alpha-2
    CONSTRAINT customers_pk PRIMARY KEY (id),
    CONSTRAINT customers_tax_id_uk UNIQUE (tax_id),
    CONSTRAINT customers_country_ck CHECK (country ~ '^[A-Z]{2}$')
);

CREATE TABLE accounts (
    id          BIGINT       NOT NULL,
    iban        CHAR(34)     NOT NULL,
    balance     NUMERIC(18,2) NOT NULL,
    status      VARCHAR(16)  NOT NULL,
    customer_id BIGINT       NOT NULL,
    CONSTRAINT accounts_pk PRIMARY KEY (id),
    CONSTRAINT accounts_iban_uk UNIQUE (iban),
    CONSTRAINT accounts_customer_fk FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT accounts_status_ck CHECK (status IN ('PENDING','ACTIVE','FROZEN','CLOSED')),
    CONSTRAINT accounts_balance_ck CHECK (balance >= 0)  -- savings-style; see CHECK for conditional logic
);
```

### A constraint that cannot be DKNF

```sql
-- "An account cannot be CLOSED if its balance is non-zero."
-- This is a transition constraint — it depends on the *previous* status.
-- No domain or key constraint can express it. Use a trigger.

CREATE OR REPLACE FUNCTION prevent_close_nonzero_balance() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'CLOSED' AND OLD.status <> 'CLOSED' AND NEW.balance <> 0 THEN
        RAISE EXCEPTION 'Cannot close account %: balance is non-zero', NEW.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_close_only_when_zero
BEFORE UPDATE OF status ON accounts
FOR EACH ROW EXECUTE FUNCTION prevent_close_nonzero_balance();
```

This trigger exists *because* the constraint cannot be reduced to domain/key — i.e., because the schema is not DKNF for this constraint. See [[03-Triggers-As-Constraints]].

## What can go wrong

- **Assuming DKNF is achievable.** It almost never is, fully. Aim for it; accept partial achievement.
- **Treating DKNF as a binary "achieved or not."** DKNF is a *spectrum*: the more constraints you push into domain/key, the closer you are. Track which constraints are DKNF-compatible and which are not.
- **Pushing complex logic into triggers to "achieve" DKNF.** A trigger does not make a constraint DKNF — DKNF requires the constraint to be a *consequence* of domain/key, not an additional enforcement. Triggers are the *opposite* of DKNF for the constraint they enforce.
- **Forgetting that DKNF subsumes 5NF.** A schema in DKNF is automatically in 5NF/4NF/BCNF. The reverse is not true.
- **Ignoring the read-cost trade-off.** Computing `balance` from `ledger_entries` (DKNF-pure) is expensive. Storing `balance` as a column (denormalization) is faster but breaks the "sum = balance" invariant — which must then be enforced by a trigger or reconciliation. This is the canonical normalization-vs-performance trade-off. See [[10-Normalization-Trade-offs]].

## Trade-offs

- **DKNF purity vs. read performance.** The closer to DKNF, the more constraints are declarative — and the more reads require joins or computations. The further from DKNF, the more denormalization (faster reads) but the more triggers (slower writes, more failure modes).
- **DKNF purity vs. developer velocity.** Triggers and application checks are easier to add incrementally than DKNF-compliant schema redesign. The trade-off is short-term speed vs. long-term maintainability.
- **DKNF purity vs. distributed systems.** Cross-table constraints in a distributed database (where tables live on different nodes) cannot be enforced by triggers in one node. DKNF becomes essentially unachievable, and the constraints move to application-level sagas or eventual reconciliation. See [[04-Eventual-Consistency]] and [[07-Distributed-Transactions]].

## Forward links

- [[10-Normalization-Trade-offs]] — when to stop chasing DKNF.
- [[11-Banking-Normalization-Walkthrough]] — practical decomposition, stopping at BCNF.
- [[02-Domain-Check-Constraints]] — domain and key constraints in SQL.
- [[03-Triggers-As-Constraints]] — what you do when DKNF is impossible.
- [[00-ACID]] — the consistency property that DKNF aspires to make automatic.
- [[02-Aggregates]] — aggregate boundaries as the design-time approximation of DKNF.
- [[04-Eventual-Consistency]] — what happens to DKNF-style constraints in distributed systems.
