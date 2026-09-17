# BCNF — Boyce-Codd Normal Form

> BCNF is the strict refinement of 3NF that catches one specific anomaly 3NF misses: when a relation has multiple overlapping candidate keys, a non-key attribute can determine part of a candidate key. The fix is to require that *every* determinant be a candidate key — full stop. The cost is that BCNF decomposition is not always dependency-preserving, which forces a real trade-off.

## What you already know

From [[06-1NF-2NF-3NF]]: 3NF says "every non-key attribute depends on the key, the whole key, and nothing but the key." 3NF allows an FD $X \to A$ when $A$ is a prime attribute (i.e., $A$ is part of *some* candidate key), even if $X$ is not a superkey. That exception is the loophole BCNF closes.

From [[03-Functional-Dependencies]]: a determinant is the left-hand side of an FD. A superkey is a determinant of all attributes. A candidate key is a minimal superkey.

From [[02-Keys-Superkeys-Candidate-Keys]]: a relation can have multiple candidate keys, and they may overlap (share attributes).

## Why this layer exists

3NF was Codd's original "good enough" normal form. In 1974, Codd and Boyce discovered a class of 3NF relations that still had anomalies: those with multiple overlapping candidate keys. BCNF was introduced to close that gap.

BCNF is the strongest normal form based purely on functional dependencies. Beyond BCNF, you need multi-valued dependencies (4NF) and join dependencies (5NF) — see [[08-4NF-5NF]]. For most practical schemas, BCNF is the target.

## What is genuinely new

- The formal definition of BCNF: every non-trivial FD has a superkey as its determinant.
- The class of cases where 3NF is not enough: multiple overlapping candidate keys.
- The decomposition algorithm and its two guarantees (lossless join, dependency preservation *not always*).
- The trade-off between BCNF and dependency preservation.

## Concepts

### The formal definition

A relation $R$ is in **Boyce-Codd Normal Form (BCNF)** iff for every non-trivial functional dependency $X \to Y$ in $R$, $X$ is a superkey of $R$.

Equivalently: **every determinant is a candidate key** (or a superkey, which is the same up to minimality).

Compare with 3NF: 3NF allows $X \to A$ when $A$ is prime. BCNF removes that exception. BCNF is strictly stronger than 3NF: every BCNF relation is in 3NF, but not every 3NF relation is in BCNF.

### When 3NF is not enough — the overlapping candidate keys case

The classic example: a relation `advisor(course, student, instructor)` with FDs:

- `{student, course} → {instructor}` (each student takes each course from one instructor)
- `{instructor, student} → {course}` (each instructor teaches each student at most one course)

Candidate keys: `{student, course}` and `{instructor, student}`. They overlap on `student`.

All attributes are prime (each appears in some candidate key). So the relation is in 3NF: every FD's right-hand side is a prime attribute.

But it is **not in BCNF**, because `{instructor} → {course}` is implied: if you know the instructor and student, you know the course — and the determinant `{instructor}` is not a superkey.

The anomalies:

- **Insertion**: you cannot record that an instructor teaches a course until a student is assigned.
- **Update**: changing the course an instructor teaches a student requires updating potentially many rows (if a student has multiple courses with the same instructor — but actually they cannot, by the second FD; the anomaly is subtle).
- **Deletion**: deleting the last enrollment for an instructor deletes the fact that the instructor teaches that course.

### The BCNF decomposition algorithm

Given a relation $R$ not in BCNF:

1. Find a non-trivial FD $X \to Y$ where $X$ is not a superkey of $R$.
2. Decompose $R$ into:
   - $R_1 = X \cup Y$ (the FD and its determinant)
   - $R_2 = X \cup (R - Y)$ (the determinant and everything except the dependent)
3. Repeat on each resulting relation until all are in BCNF.

### Lossless join property

The decomposition is **lossless**: $R = R_1 \bowtie R_2$ (you can reconstruct $R$ by joining $R_1$ and $R_2$ on $X$). This is guaranteed because $X$ is a candidate key of at least one of the two resulting relations (it follows from the FD structure).

Losslessness is *essential*. A decomposition that loses information is useless. The BCNF algorithm preserves it automatically.

### Dependency preservation — the catch

A decomposition is **dependency-preserving** if every FD in the original relation can be checked in one of the decomposed relations without computing a join. BCNF decomposition is **not always** dependency-preserving.

In the advisor example, decomposing by `{instructor} → {course}` yields:

- $R_1$ = `teaches(instructor, course)`
- $R_2$ = `enrolls(student, course, instructor)` — but now the FD `{student, course} → {instructor}` *crosses* the two relations (it requires joining $R_1$ and $R_2$ to verify). The FD is not preserved.

The consequence: enforcing the FD requires either a trigger, a deferred check, or application code. None of these is as cheap as a `UNIQUE` constraint.

### The trade-off

When BCNF decomposition is not dependency-preserving, you have three options:

1. **Decompose to BCNF and accept the FD-checking cost** (trigger or application check).
2. **Stay at 3NF and accept the residual anomalies** (manage them with triggers or careful code).
3. **Denormalize selectively** — pick a different decomposition that preserves dependencies but is not fully BCNF.

For most OLTP systems, option 1 is preferred: BCNF for cleanliness, triggers only for the few FDs that cannot be checked locally. For systems where triggers are expensive or forbidden (e.g., some managed databases), option 2 is realistic.

## Banking application

### A subtle BCNF violation

Consider a banking schema where each customer can have multiple accounts, and accounts have an "account type" that determines a per-customer overdraft limit:

```
customer_account_type(
    customer_id,        -- FK to customers
    account_type,       -- 'CHECKING' | 'SAVINGS' | 'LOAN'
    overdraft_limit,    -- per (customer, account_type)
    account_id          -- FK to accounts (the specific account)
)
```

FDs:

- `{account_id} → {customer_id, account_type, overdraft_limit}` (each account has one customer and one type)
- `{customer_id, account_type} → {overdraft_limit}` (per customer, the overdraft limit is set per type, not per account)

Candidate keys: `{account_id}` only.

Is `{customer_id, account_type}` a superkey? No — multiple accounts of the same customer and type could exist (a customer with two checking accounts). So the FD `{customer_id, account_type} → {overdraft_limit}` has a non-superkey determinant.

This relation is in **3NF** (every non-prime attribute depends on a superkey — `overdraft_limit` is non-prime; its determinant in the offending FD is `{customer_id, account_type}`, but `{customer_id, account_type}` is not a candidate key, so 3NF... wait).

Let me redo this carefully. The FDs are:

1. `{account_id} → {customer_id, account_type, overdraft_limit}` — determinant is a superkey, fine.
2. `{customer_id, account_type} → {overdraft_limit}` — determinant is *not* a superkey.

3NF test: for FD 2, is the right-hand side (`overdraft_limit`) a prime attribute? `overdraft_limit` does not appear in the only candidate key (`{account_id}`), so it is non-prime. Therefore 3NF is **violated**. (And so BCNF is also violated.)

So this example is actually a 3NF violation, not a "3NF-only" violation. Let me construct a real BCNF-only violation in banking.

### A real BCNF-only violation in banking

Consider `account_signatories(account_id, iban, customer_id)` where:

- An account has exactly one IBAN; one account can have multiple signatories (customers).
- Each signatory is associated with the account via the account_id; the IBAN is denormalized for convenience.

FDs:

- `{account_id} → {iban}` (account determines IBAN)
- `{iban} → {account_id}` (IBAN determines account — IBAN is also a candidate key)
- `{account_id, customer_id} → {iban}` (a signatory row determines the account's IBAN)
- `{iban, customer_id} → {account_id}` (a signatory row determines the account)

Candidate keys: `{account_id, customer_id}` and `{iban, customer_id}`. They overlap on `customer_id`.

Every attribute is prime (each appears in some candidate key). So the relation is in 3NF. But:

- The FD `{account_id} → {iban}` has a non-superkey determinant (`{account_id}` alone is not a superkey — you also need `customer_id`). The relation is **not in BCNF**.

The anomaly: the IBAN is repeated for every signatory of the same account. Updating the IBAN means updating every signatory row — but IBANs do not change, so this is rarely a problem; still, the redundancy is real.

### Decomposition

Extract the FD `{account_id} → {iban}` into its own relation:

- $R_1$ = `accounts(account_id, iban)` (with `account_id` as PK and `iban` as UNIQUE)
- $R_2$ = `account_signatories(account_id, customer_id)` (composite PK)

Both are in BCNF. The join `accounts ⋈ account_signatories` on `account_id` reconstructs the original.

Dependency preservation: the FDs `{account_id} → {iban}` and `{iban} → {account_id}` are now in `accounts` (enforced by PK and UNIQUE). The composite-key FDs `{account_id, customer_id} → {iban}` and `{iban, customer_id} → {account_id}` are now trivial consequences of joining. Decomposition is dependency-preserving in this case.

## Code

```sql
-- The BCNF-compliant banking schema (relevant fragment)

CREATE TABLE accounts (
    id          BIGINT   NOT NULL,
    iban        CHAR(34) NOT NULL,
    balance     NUMERIC(18,2) NOT NULL,
    status      VARCHAR(16) NOT NULL,
    customer_id BIGINT   NOT NULL,
    CONSTRAINT accounts_pk PRIMARY KEY (id),
    CONSTRAINT accounts_iban_uk UNIQUE (iban)
    -- other constraints omitted for brevity
);

CREATE TABLE account_signatories (
    account_id  BIGINT NOT NULL,
    customer_id BIGINT NOT NULL,
    role         VARCHAR(16) NOT NULL,
    CONSTRAINT account_signatories_pk PRIMARY KEY (account_id, customer_id),
    CONSTRAINT account_signatories_account_fk FOREIGN KEY (account_id) REFERENCES accounts(id),
    CONSTRAINT account_signatories_customer_fk FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

### Enforcing a non-preserved FD with a trigger (rare case)

If a BCNF decomposition left an FD unchecked, you can enforce it with a trigger:

```sql
-- PostgreSQL: trigger to enforce an FD that crosses tables
CREATE OR REPLACE FUNCTION check_overdraft_fd() RETURNS TRIGGER AS $$
BEGIN
    -- For the (customer_id, account_type) -> overdraft_limit FD
    PERFORM 1 FROM customer_account_type
    WHERE customer_id = NEW.customer_id
      AND account_type = NEW.account_type
      AND overdraft_limit <> NEW.overdraft_limit;
    IF FOUND THEN
        RAISE EXCEPTION 'Overdraft limit for (%,%) is inconsistent',
            NEW.customer_id, NEW.account_type;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_overdraft_fd
BEFORE INSERT OR UPDATE ON customer_account_type
FOR EACH ROW EXECUTE FUNCTION check_overdraft_fd();
```

Triggers are a last resort. They are hard to reason about, easy to get wrong, and invisible to the optimizer. Always prefer a `UNIQUE` or `CHECK` constraint when possible. See [[03-Triggers-As-Constraints]].

## What can go wrong

- **Confusing 3NF with BCNF.** They differ only when candidate keys overlap. If your relation has a single candidate key, 3NF and BCNF are the same.
- **Forgetting to verify losslessness.** A *random* decomposition can lose information. The BCNF algorithm guarantees losslessness; ad-hoc splits do not. Always check that the join attribute is a candidate key of one of the resulting relations.
- **Losing an FD silently.** After decomposition, list the original FDs and verify each one is enforceable in the new schema. If any cannot be enforced with a constraint, document the trigger or application check that handles it.
- **Over-decomposing into BCNF when 3NF is good enough.** If the residual anomalies in 3NF are negligible (e.g., IBANs never change), staying at 3NF may be cheaper than paying for extra joins and triggers.
- **Ignoring NULL semantics.** BCNF assumes set semantics with no NULLs. Nullable columns that participate in FDs lead to subtle violations. See [[01-Relations-Tuples-Attributes]].

## Trade-offs

- **BCNF vs. dependency preservation.** Sometimes you must choose: full BCNF (cleaner, lossless, but FDs need triggers) or 3NF (slight redundancy, FDs preserved declaratively). The right answer depends on how expensive triggers are and how often the redundant data changes.
- **BCNF vs. join cost.** More decomposition = more joins. For OLTP queries that touch one tuple at a time, the cost is small. For reporting queries that aggregate, the cost can be large — and you may denormalize via materialized views. See [[10-Normalization-Trade-offs]] and [[07-Views-Materialized-Views]].
- **Theory vs. practice.** Real-world schemas often stop at 3NF because the BCNF-only violations are rare and the cost of fully decomposing (more joins, possible triggers) is not worth it. This is a legitimate trade-off, not laziness — as long as it is *deliberate*.

## Forward links

- [[08-4NF-5NF]] — beyond BCNF: multi-valued and join dependencies.
- [[09-DKNF]] — the "ultimate" normal form, mostly aspirational.
- [[10-Normalization-Trade-offs]] — when to stop.
- [[11-Banking-Normalization-Walkthrough]] — full end-to-end decomposition including BCNF.
- [[03-Triggers-As-Constraints]] — enforcing non-preserved FDs.
- [[04-Banking-Schema]] — the concrete SQL DDL.
- [[06-Coupling-and-Cohesion]] — BCNF is the formal version of "each table, one fact type."
