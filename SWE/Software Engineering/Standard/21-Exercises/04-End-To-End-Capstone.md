# End-to-End Capstone — The Library System

> The integration test. Carry a single problem (different from Banking, to prevent copying) through every layer of the vault.

## Why a different domain

The Banking case study is solved throughout the vault. If the capstone used Banking, you could copy the answer. The capstone uses a **Library Management System** — a different domain that exercises the same concepts, forcing you to apply (not recall) what you have learned.

## The problem

Design and implement a library management system with the following capabilities:

- **Catalog management** — books, authors, categories; a book may have multiple copies.
- **Member management** — registration, membership renewal, suspension for overdue items.
- **Loans** — a member borrows a copy; due date is computed by loan policy (e.g., 14 days for regular, 7 days for high-demand, 21 days for faculty).
- **Returns** — a member returns a copy; if late, a fine is computed.
- **Reservations** — a member can reserve a book that is currently loaned out; when a copy becomes available, the next reservation is notified.
- **Fines** — overdue items accrue daily fines; fines must be paid before new loans.
- **Notifications** — email/SMS for due-soon, overdue, reservation-available.
- **Reporting** — most-borrowed books, overdue members, daily fine collection.

## The ten invariants

1. **Copy state invariant**: a copy's state (`AVAILABLE`, `ON_LOAN`, `RESERVED`, `LOST`) matches the latest loan/reservation event.
2. **No double-loan**: a copy cannot be loaned to two members simultaneously.
3. **Loan due date**: computed by the loan policy in effect at loan time; does not change.
4. **Fine invariant**: `fine.amount = days_overdue × daily_rate` for the member's category at the time of overdue.
5. **Fine payment before loan**: a member with unpaid fines cannot borrow.
6. **Reservation FIFO**: reservations are fulfilled in the order they were made.
7. **Membership active**: only active members can borrow.
8. **Auditability**: every state change has an audit trail.
9. **Idempotency**: a return request with the same idempotency key produces the same result.
10. **Concurrent loan safety**: two members attempting to loan the same copy at the same time must not both succeed.

## Your task — every layer

For each layer below, produce the artifact. Show your reasoning, not just the final answer.

### Layer 1 — Requirements

Write a one-page requirements document covering functional, non-functional, constraints, and invariants. Identify at least two *unstated* requirements that the stakeholders probably assume but did not write down.

*Back-link: [[01-Requirements]].*

### Layer 2 — Use cases

Write the use case for "borrow a copy" in Cockburn's full template: trigger, preconditions, main success scenario, extensions, postconditions. Include at least five extensions.

*Back-link: [[02-Use-Cases]].*

### Layer 3 — Domain concepts

Extract the nouns and verbs from the use case. Build a domain glossary with at least 12 terms. Identify at least one homonym (same word, different meaning in different contexts).

*Back-link: [[03-Domain-Concepts]].*

### Layer 4 — Responsibilities

Use CRC cards to assign responsibilities. Show the card for `Copy`, `Loan`, `Member`, and `LoanPolicy`. Each card should have 3-5 responsibilities and 2-4 collaborators.

*Back-link: [[04-Responsibilities]], [[02-CRC-Cards]].*

### Layer 5 — Classes and objects

Design the class structure. Show the `Copy`, `Loan`, `Member`, `LoanPolicy` classes as Java code with fields, constructors, and the key methods. Apply the "tell, don't ask" principle.

*Back-link: [[01-Objects-And-Classes]], [[02-Encapsulation]], [[04-Tell-Dont-Ask]].*

### Layer 6 — Relationships

Draw a class diagram (Mermaid `classDiagram`) showing the relationships among `Member`, `Copy`, `Book`, `Loan`, `Reservation`, `Fine`. Specify multiplicities.

*Back-link: [[00-Object-Relationships]], [[01-Class-Diagrams]].*

### Layer 7 — SOLID

Apply each SOLID principle to the design. Show one concrete refactor for each principle (e.g., for OCP, show how to add a new loan policy without modifying existing code).

*Back-link: [[00-SOLID-as-Dependency-Management]] through [[06-SOLID-in-Banking]].*

### Layer 8 — Patterns

Identify where each of these patterns fits: Strategy (loan policy), State (copy state), Observer (reservation notification), Repository (persistence), Factory (notification creation). Show one in Java.

*Back-link: [[00-Patterns-As-Documented-Forces]] through [[06-Patterns-in-Banking]].*

### Layer 9 — UML

Draw:
- A class diagram of the full domain.
- A sequence diagram of the borrow use case.
- A state diagram of the `Copy` lifecycle.
- An activity diagram of the return-and-fine flow.

*Back-link: [[00-UML-As-Modeling-Language]] through [[06-UML-For-Banking]].*

### Layer 10 — LLD

Apply the LLD method to the "borrow a copy" flow: naive design → failure mode → forces → better design → UML → code → trade-offs. Identify at least two failure modes of the naive design.

*Back-link: [[00-LLD-Method]], [[06-Banking-LLD]].*

### Layer 11 — Architecture

Pick an architecture (Layered / Hexagonal / Clean / Microservices) and justify. Draw the component diagram. Specify the bounded contexts.

*Back-link: [[02-Layered-Architecture]] through [[05-Architecture-Trade-offs]].*

### Layer 12 — Domain model (DDD)

Identify: entities, value objects (e.g., `Money` for fines, `ISBN`, `DueDate`), aggregates (what is the consistency boundary for a loan?), bounded contexts (Catalog, Membership, Circulation, Billing), domain events (`BookBorrowed`, `BookReturned`, `FinePaid`).

*Back-link: [[00-Domain-Modeling]] through [[06-Banking-Domain-Model]].*

### Layer 13 — ER model

Draw the ER diagram (Mermaid `erDiagram`). Show all entities and relationships with cardinalities. Handle the inheritance: `Book` has subtypes (e.g., `PrintBook`, `EBook`, `AudioBook`) — pick a strategy and justify.

*Back-link: [[00-ER-Modeling]] through [[02-Banking-ER]].*

### Layer 14 — Relational schema

Translate the ER model to a relational schema. Write the SQL DDL with all constraints: primary keys, foreign keys, unique, check, not null. Identify the functional dependencies and verify BCNF.

*Back-link: [[00-Schema-Design]] through [[04-Banking-Schema]], [[03-Functional-Dependencies]], [[07-BCNF]].*

### Layer 15 — SQL

Write the SQL for:
- Borrow a copy (one transaction).
- Return a copy and compute the fine.
- Find members with overdue items.
- Find the most-borrowed book of the last month.
- Compute daily fine collection (window function).

*Back-link: [[00-SQL-From-Relational-Algebra]] through [[09-Banking-SQL]].*

### Layer 16 — Indexes

Propose indexes for the schema. For each, justify: what query does it speed up? What is the write cost? Are there any composite indexes?

*Back-link: [[01-Indexing-Strategy]], [[03-B-Tree-Indexes]].*

### Layer 17 — Transactions

For the borrow flow, specify:
- Isolation level (justify).
- Locking strategy (which rows are locked, in what order).
- The idempotency mechanism.

*Back-link: [[00-ACID]], [[02-Isolation-Levels]], [[03-Two-Phase-Locking]], [[06-Deadlocks]].*

### Layer 18 — Concurrency

Identify at least three concurrency hazards in the system and the fix for each:
- Two members borrowing the same copy simultaneously.
- A member returning a copy while a fine is being computed.
- A reservation being fulfilled while the copy is being marked lost.

*Back-link: [[01-Concurrency-Anomalies]], [[04-MVCC]], [[05-Serializability]].*

### Layer 19 — Query optimization

Take the "most-borrowed book of the last month" query. Write it, run `EXPLAIN ANALYZE` (mentally or for real on a test database), identify the bottleneck, and propose a fix.

*Back-link: [[00-Query-Optimization-Strategy]], [[08-Reading-EXPLAIN]].*

### Layer 20 — Recovery

The library's database crashes at 14:32 with active loans in progress. Walk through the recovery. What is committed? What is rolled back? What does the user see when the system comes back up?

*Back-link: [[00-WAL-Logging]] through [[04-Banking-Recovery-Scenario]].*

### Layer 21 — Distributed (stretch)

If the library expands to 50 branches, each with its own database, how would you handle:
- A member borrowing at branch A and returning at branch B?
- The aggregated "most-borrowed" report across all branches?

*Back-link: [[03-Sharding-Revisited]], [[07-Distributed-Transactions]], [[04-Eventual-Consistency]].*

## How to attempt the capstone

1. **Do not try to do all 21 layers in one sitting.** Budget at least a week.
2. **Do them in order.** Each layer depends on the previous.
3. **Write your answers down.** Thinking is not enough; the act of writing forces precision.
4. **Compare to the Banking solution in the vault.** Not to copy — to check your reasoning. The domains are different, but the *patterns* of reasoning are the same.
5. **Find a reviewer.** If possible, have another engineer review your design at each layer. The act of explaining exposes gaps.

## What success looks like

If you can complete all 21 layers, you have demonstrated that you can:

- Take a real software problem and reason about it from requirements to physical storage.
- Apply each layer's concepts in context, not just recite them.
- Make trade-offs explicit.
- Connect the layers into one coherent design.

This is the goal of the vault: not to know *about* software design and database engineering, but to *do* them.

## Where to look when stuck

Each layer above links back to the chapter that teaches it. If you cannot complete a layer, go back, re-read the chapter, and try again. The vault is designed for this loop — that is why it is structured as a continuous chain rather than isolated topics.

## The final question

When you finish the capstone, ask yourself:

> *What did I learn that I did not know before?*

If the answer is "nothing," you have mastered the vault. If the answer is "X, Y, and Z," go back and study those. The capstone is the test; the gaps it reveals are the curriculum.
