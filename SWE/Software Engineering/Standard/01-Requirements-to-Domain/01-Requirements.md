# Requirements — Where the Chain Begins

> The first link in the continuous chain. Requirements are not "what the system does" — they are *what the system must be true about itself*.

## What you already know

From [[02-The-Continuous-Chain]]: every layer adds something. Requirements are the start; they add nothing technical. They are a problem statement.

From [[00-Banking-Case-Study]]: the anchor problem is a retail banking system with ten invariants.

## Why this layer exists

Software exists to solve a problem. If we do not know what problem we are solving, every later decision is unmoored. A class design without requirements is decoration; a schema without requirements is data hoarding; a query plan without requirements is micro-optimization for an unknown workload.

Requirements exist to *constrain the design space*. They tell us what is in scope, what is out of scope, what success looks like, and what failure looks like. Without them, "good design" is undefined — good for what?

## What is genuinely new here

Two things, neither technical:

1. **The notion of a stakeholder.** Someone cares about the outcome. Their cares are the requirements.
2. **The notion of a constraint vs a preference.** A constraint must hold; a preference is nice to have. Confusing them leads to over-engineering or under-engineering.

That is it. Everything else in this chapter is method, not concept.

## Types of requirements

| Type | Question it answers | Example |
|---|---|---|
| **Functional** | What must the system do? | "A customer can transfer money between accounts." |
| **Non-functional** | How well must it do it? | "Transfers complete in under 2 seconds at p99." |
| **Constraint** | What is fixed about the environment? | "Must run on PostgreSQL 15." |
| **Quality attribute** | What -ilities matter? | "Available 99.99% of the time." |
| **Invariant** | What must always be true? | "Balance equals the sum of ledger entries." |
| **Compliance** | What external rules apply? | "Audit trail retained for 7 years (regulatory)." |

The categories overlap. The point is not the taxonomy but the discipline of asking, for each requirement: *which kind is this, and how will we know if we have satisfied it?*

## Functional vs non-functional — the false divide

A common mistake: treating functional requirements as "the real requirements" and non-functional ones as "soft" or "later." This is wrong.

- A transfer system that is functionally correct but takes 30 seconds per transfer has not satisfied the requirement.
- A transfer system that is fast but loses money under concurrency has not satisfied the requirement.
- A transfer system that is fast and correct but cannot recover from a crash has not satisfied the requirement.

Functional requirements describe *behavior*; non-functional requirements describe *qualities of behavior*. Both are requirements. Both must be designed for from the start. Retrofitting non-functional requirements is far more expensive than designing for them.

## Invariants — the most important kind of requirement

Invariants are requirements of the form "*X must always be true.*" They are the most important kind because:

- They are testable (assert X after every operation).
- They are enforceable (in code, in schema, in constraints).
- They survive refactorings (the invariant stays even when implementation changes).
- They are the contract every layer must respect.

The Banking case study lists ten invariants. Every one of them will be enforced in multiple layers:

- **Code**: class invariants, method pre/post-conditions.
- **Schema**: `CHECK`, `NOT NULL`, `UNIQUE`, foreign keys.
- **Transactions**: serializable isolation for balance-changing operations.
- **Application**: idempotency keys, audit logging.

When a new requirement comes in, ask: *is this an invariant?* If yes, it deserves multi-layer enforcement. If no, it is a feature, not a constraint.

## The problem of unstated requirements

Most failures in software come from requirements nobody wrote down. Examples in banking:

- "Transfers must be idempotent" — assumed but not stated, until a retry caused a double-debit.
- "The ledger is append-only" — assumed but not stated, until someone wrote a "correction" that deleted a row.
- "Closed accounts cannot transact" — assumed but not stated, until a closed account received a deposit six months later.
- "Balance must equal the sum of ledger entries" — assumed but not stated, until a denormalized column drifted out of sync.

The discipline of requirements is not only to write down what was asked. It is to *interrogate the assumed invariants* — the ones every stakeholder takes for granted but no one has named. These are the requirements that, when violated, cause outages.

## Banking application — the requirements document

A condensed requirements document for the banking system:

**Functional**:
- A customer can register and submit KYC documents.
- A customer can open a checking or savings account.
- A customer can deposit money into an active or frozen account.
- A customer can withdraw money from an active account, subject to balance and overdraft rules.
- A customer can transfer money between their own accounts and to external accounts.
- A customer can request a statement for any account they own.
- Interest accrues daily on savings accounts and is credited monthly.
- Fraud detection flags suspicious transfers for review.

**Non-functional**:
- Transfer latency: p99 < 2 seconds for internal transfers.
- Availability: 99.99% monthly (≈ 4.4 minutes downtime).
- Throughput: 1,000 transfers/second sustained.
- Durability: no committed transaction is ever lost.
- Auditability: every state change has a tamper-evident audit trail.

**Constraints**:
- Single currency (USD).
- Single region (us-east-1) initially, multi-region later.
- PostgreSQL 15+ as primary database.
- Java 21 LTS.
- Synchronous fraud check initially; async later.

**Invariants** (the ten from [[00-Banking-Case-Study]], repeated here as first-class requirements).

## What can go wrong

- **Vague requirements** ("the system should be fast") — untestable, lead to arguments later.
- **Missing requirements** — the assumed invariants that no one wrote down.
- **Conflicting requirements** ("fast" and "serializable") — must be reconciled explicitly, not silently.
- **Over-specified requirements** ("must use Redis for caching") — these are constraints masquerading as requirements; they limit design space without need.
- **Under-specified requirements** ("must be secure") — security is not a single requirement; it is a set of specific properties.

## Trade-offs

- **How much to specify?** Too little: design drifts. Too much: no room for the engineer to choose well. The right amount: invariants and quality attributes fully specified; implementation choices left open.
- **How formal?** Formal specs (TLA+, Alloy) catch more bugs but cost more to write. Use them for the most critical invariants (e.g., transfer atomicity).
- **When to freeze?** Freezing too early locks in wrong assumptions. Freezing too late means the team builds without a target. Iterate, but mark invariants as frozen early — they are the contract.

## Forward links

- [[02-Use-Cases]] — structuring the behavior requirements into named interactions.
- [[03-Domain-Concepts]] — extracting the nouns and verbs from requirements.
- [[04-Responsibilities]] — assigning the verbs to nouns.
- [[00-ACID]] — the four properties that turn "durability" and "atomicity" requirements into formal guarantees.
