# Object Model vs Data Model — Where They Correspond, Where They Diverge

> The central tension of persistence. The domain has one model (objects); the database has another (relations). They are not the same model, and pretending they are causes most of the pain in enterprise software.

## What you already know

From [[03-Dependency-As-Root-Concept]]: dependencies are about what changes with what. From [[04-Abstraction-and-Models]]: a model is selective forgetting for a purpose. From [[05-Identity-State-Lifecycle]]: identity comes in three flavors (object, logical, surrogate).

This note brings those forces together to explain why the object model and the data model are *two different abstractions* of the same domain — and why treating them as one causes the impedance mismatch (cross-link [[00-ORM-Impedance-Mismatch]]).

## Why this layer exists

A domain can be modeled in multiple ways for multiple purposes. The two most common:

- **Object model** — for behavior. Objects have identity, state, methods, and collaborations. The model is rich; invariants are enforced by methods.
- **Data model** — for persistence and query. Relations have keys, attributes, and constraints. The model is flat; invariants are enforced by constraints.

These two models describe the *same domain*, but they answer *different questions*. The object model answers "what does this thing do?" The data model answers "what is true about this thing, independent of any process?"

Software that persists state needs both. The mistake is to assume they are the same model — that a class is a table, that an object reference is a foreign key, that inheritance is a subtype table. They are not. They are different abstractions, and the relationship between them is itself a design decision.

## What is genuinely new here

- The claim: **object model and data model are different abstractions of the same domain, not the same model in two notations.**
- The correspondence map: where they align (and can be mapped 1:1).
- The divergence map: where they don't (and require translation).
- The design rule: design each model for its purpose; translate at the boundary.

## The correspondence map — where they align

For many entities, the object model and the data model align closely:

| Object model | Data model | Notes |
|---|---|---|
| `Account` class | `accounts` table | One class = one table |
| `Account.id` field | `accounts.id` column (PK) | Object field = column |
| `Account.iban` field | `accounts.iban` column (UNIQUE) | Logical identity = unique constraint |
| `Account.balance` field | `accounts.balance` column | Mutable state = mutable column |
| `Account.ledgerEntries` list | `ledger_entries` table with FK to `accounts` | Collection = child table |
| `Customer.accounts` list | `accounts.customer_id` FK | Back-reference = FK column |
| `Money` value object (amount + currency) | `amount NUMERIC(18,2)` + `currency CHAR(3)` columns | Value object = embedded columns |
| `AccountStatus` enum | `status TEXT CHECK (status IN (...))` | Enum = constrained string |

In these cases, the translation is mechanical: each class becomes a table, each field becomes a column, each collection becomes a child table with a foreign key. This is what ORMs do well.

## The divergence map — where they don't align

But for many other cases, the two models diverge:

| Object model concept | Relational equivalent | Why they diverge |
|---|---|---|
| Object identity (memory reference) | Primary key | Object identity is ephemeral; PK is durable. Different lifetimes. |
| Object reference (`Account` holds `Customer`) | Foreign key (`accounts.customer_id`) | Reference is navigational; FK is associative. Different access patterns. |
| Bidirectional association | Two FKs or one FK + reverse query | Objects can navigate both ways for free; relations cannot. |
| Inheritance hierarchy | STI / CTI / Concrete (cross-link [[07-Composition-vs-Inheritance]]) | Relations have no native inheritance. Must choose a strategy. |
| Polymorphic association | Discriminator column + multiple FKs, or table-per-type | Relations have no native polymorphism. |
| Composition (lifecycle ownership) | FK with `ON DELETE CASCADE` | Close, but cascade is a blunt instrument; composition in objects is finer-grained. |
| Object graph (lazy/eager loading) | JOINs | Objects load on demand; relations query in sets. Different fetching models. |
| Object methods (behavior) | None | Relations have no behavior. Behavior lives in the object layer only. |
| Class invariants (checked at runtime) | CHECK / NOT NULL / triggers | Both enforce invariants, but at different layers and with different expressiveness. |
| Identity across sessions | None (object identity is per-session) | Relations have global identity (PK). Cross-session object equality must use logical identity. |
| Value object equality (two `Money(100, USD)` are equal) | Row equality (two rows with same data are still two rows) | Value semantics vs row semantics. |
| Navigating a graph (a.b.c.d()) | Multiple JOINs or subqueries | Object navigation is O(1) per hop; SQL JOINs are O(N*M) without indexes. |
| Object lifecycle state (PENDING → ACTIVE → FROZEN → CLOSED) | Status column + CHECK constraint | State pattern in objects vs declarative constraint in schema. |
| Domain events (`TransferCompleted`) | None in the schema; events are an application concept | Events are not persisted unless explicitly stored (event sourcing). |
| Aggregate boundary (consistency boundary) | Transaction boundary | Aggregate is a domain concept; transaction is a technical concept. They often align but are not the same. |

Each divergence is a place where translation is required. The translation is what ORMs do — and where ORMs leak (cross-link [[00-ORM-Impedance-Mismatch]]).

## The design rule — design each model for its purpose

The mistake: design the object model, then "persist it" by mapping each class to a table. This produces a data model that is shaped by the object model — which is the wrong shape for queries, for constraints, for normalization.

The right approach:

1. **Design the object model for behavior.** What are the entities? What are their methods? What are the invariants? Don't think about tables yet.
2. **Design the data model for persistence and query.** What are the relations? What are the keys? What are the constraints? What are the normal forms? Don't think about objects yet.
3. **Translate at the boundary.** Map objects to relations using the correspondence map above, and explicitly handle the divergences. Use an ORM, a repository, or hand-written SQL — but recognize that the translation is a design decision, not a mechanical mapping.

This is the "two models" approach. It produces a richer object model (because it is not constrained by relational shape) and a better data model (because it is not constrained by object shape).

## Where they correspond in Banking

For the Banking system:

- `Account` (object) ↔ `accounts` (table) — direct correspondence.
- `LedgerEntry` (object) ↔ `ledger_entries` (table) — direct.
- `Customer` (object) ↔ `customers` (table) — direct.
- `Transfer` (object) ↔ `transfers` (table) — direct.

These are the easy cases. The object model and the data model align closely.

## Where they diverge in Banking

- **Account subtypes** — `CheckingAccount` and `SavingsAccount` are distinct classes in the object model (with different behavior: overdraft rules, interest policies). In the data model, we choose Class Table Inheritance (CTI): `accounts` (base) + `checking_accounts` (subtype table) + `savings_accounts` (subtype table). The translation is explicit; the ORM handles it.
- **Money** — a value object in the object model (with currency). In the data model, it is two columns (`amount`, `currency`) on each table that holds money. The translation is mechanical but explicit.
- **Account status** — a State pattern in the object model (different behavior per state). In the data model, it is a `status` column with a CHECK constraint. The behavior is in the object; the constraint is in the schema. Both enforce the same invariant (status must be one of the allowed values), but at different layers.
- **Transfer → Account reference** — the `Transfer` object holds references to two `Account` objects (source, destination). In the data model, the `transfers` table has two FK columns (`source_account_id`, `destination_account_id`). The translation is mechanical.
- **Account → LedgerEntry collection** — the `Account` object holds a `List<LedgerEntry>`. In the data model, `ledger_entries` has an FK to `accounts`. The collection is a query, not a stored reference. This is where the N+1 problem lives (cross-link [[03-N-plus-1-Problem]]).
- **TransferCompleted event** — a domain event in the object model. Not in the data model unless we use event sourcing (we don't, in Banking; the ledger entries serve as the event log). The event is published in-process or via an outbox table (cross-link [[04-Domain-Events]]).
- **Aggregate boundary** — the `Account` aggregate includes its `LedgerEntry` children. In the data model, this means `accounts` and `ledger_entries` are modified in the same transaction. The aggregate boundary is enforced at the application layer (one transaction per aggregate modification), not at the schema layer.

## The implications for design

The "two models" approach has implications:

1. **You write the object model and the data model separately.** They start aligned (one class = one table) but evolve independently. A change to the object model may not require a schema change, and vice versa.
2. **The translation layer (ORM, repository) is a real layer, not a detail.** It deserves design attention. Leaky abstractions here cost real money (cross-link [[04-Abstraction-and-Models]]).
3. **Queries are written against the data model, not the object model.** A SQL query joins tables; it does not navigate objects. Trying to query through the object model (e.g., Hibernate HQL that mimics SQL) is a category error.
4. **Reporting often uses a third model** — a denormalized read model (cross-link [[02-Denormalization-For-Reads]]) optimized for queries. This is the CQRS insight (cross-link [[04-Enterprise-Patterns]]): write model = object model + OLTP schema; read model = denormalized tables or materialized views.
5. **The schema outlives the application.** The object model changes with every refactor; the schema changes rarely (because migrations are expensive). Design the schema for stability; design the objects for flexibility.

## The CQRS resolution

The cleanest resolution to the "two models" tension is CQRS (Command Query Responsibility Segregation):

- **Write side**: the object model is rich; the schema is normalized; invariants are enforced in both. The ORM maps between them.
- **Read side**: a separate set of read models (denormalized tables, materialized views, search indexes) optimized for queries. No ORM; just SQL or a thin query layer.

This separates the two concerns completely. The write side honors the object model; the read side honors the data model. The translation between them is an asynchronous projection (event handler that updates read models when the write model changes).

Banking uses a mild form of CQRS: the write model is `accounts` + `ledger_entries` (normalized); the read model is `account_balances` (materialized view) and `daily_balances` (denormalized table refreshed nightly). The object model is used for the write side; raw SQL is used for the read side.

## What can go wrong

- **Treating them as the same model** — produces a data model shaped by the object model (bad for queries) or an object model shaped by the data model (anemic, behavior-less).
- **Letting the ORM dictate the schema** — Hibernate's default mapping produces a schema that is convenient for the ORM but suboptimal for queries. Design the schema first; map the ORM to it.
- **Letting the schema dictate the object model** — generating entities from the schema (e.g., JPA reverse engineering) produces anemic data bags. Design the object model first; map the schema to it.
- **Ignoring the divergence** — pretending that object references are foreign keys, that inheritance is subtyping, that collections are JOINs. The mismatches leak as bugs (N+1, lost updates, lazy initialization exceptions).

## Trade-offs

- **Two models vs one** — two models are more work to maintain but produce better software. One model is easier to start with but degenerates as the system grows.
- **ORM vs hand-written SQL** — ORM reduces boilerplate but hides the translation. Hand-written SQL makes the translation explicit but is verbose. Banking uses ORM for the write side (where the object model is rich) and hand-written SQL for the read side (where the data model is optimized for queries).
- **CQRS vs single model** — CQRS gives the cleanest separation but adds complexity (projections, eventual consistency between read and write). Banking uses a mild CQRS (read models are projections, not separate services); a full CQRS would be overkill.

## What is genuinely new here

- The object model and the data model are *different abstractions of the same domain*, not the same model in two notations.
- They correspond in the easy cases (class ↔ table) and diverge in the hard cases (identity, inheritance, collections, behavior).
- The right design approach: design each model for its purpose, translate at the boundary, and consider CQRS for read-heavy systems.

## Where this goes next

- [[00-ORM-Impedance-Mismatch]] — the divergence map, in depth.
- [[01-Identity-Map]] — how ORMs reconcile object identity with primary key.
- [[02-Aggregates]] — aggregate boundaries as a bridge between the two models.
- [[04-Enterprise-Patterns]] — Repository, Unit of Work, CQRS as translation patterns.
- [[02-Denormalization-For-Reads]] — the read model as a third abstraction.
- [[04-Banking-Schema]] — the data model side of Banking.
- [[06-Banking-Domain-Model]] — the object model side of Banking.
