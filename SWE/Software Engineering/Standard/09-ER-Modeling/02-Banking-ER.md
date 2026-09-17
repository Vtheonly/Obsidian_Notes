# Banking ER — The Complete Diagram

> The full ER model for the banking case study: every entity, every relationship, every cardinality. This is the picture you would draw before writing a single `CREATE TABLE` statement. It is the source of truth for the schema in [[04-Banking-Schema]], the ORM mapping in [[07-Banking-ORM-Mapping]], and the SQL in [[09-Banking-SQL]].

## What you already know

From [[00-ER-Modeling]]: the ER model captures entities, attributes, relationships, and cardinalities — without committing to tables, columns, or storage. From [[01-ER-to-Relational]]: the translation rules turn an ER model into a relational schema, with lossy edges at subtypes, multi-valued attributes, and composite attributes. From [[06-Banking-Domain-Model]]: the domain model with entities, value objects, aggregates, and events.

This chapter assembles the complete banking ER model in one diagram and walks through where the translation is straightforward and where it strains.

## Why this layer exists

Previous chapters introduced the building blocks. This chapter exists to:

- Show the complete ER picture in one place, so every later chapter can refer to "the banking ER diagram" and you know what it looks like.
- Make the translation decisions explicit (STI vs CTI, composite keys vs surrogate, multi-valued attributes as child tables).
- Identify the places where ER modeling strains — inheritance, value objects, events — and explain why each strain exists.

If you only read one chapter in the ER-Modeling folder, read this one. The previous two chapters are the theory; this is the application.

## What is genuinely new here

Nothing conceptually. The new thing is the *complete artifact*: every entity, every relationship, every attribute, in one diagram and one set of tables. This is the picture you defend in a design review and the source you consult when the schema needs to change.

## Concepts

### The complete ER diagram

```mermaid
erDiagram
    CUSTOMER ||--o{ ACCOUNT : "owns"
    CUSTOMER ||--o{ NOTIFICATION : "receives"
    CUSTOMER ||--o{ PHONE_NUMBER : "has"
    CUSTOMER ||--o{ STATEMENT : "is sent"

    ACCOUNT ||--o| CHECKING_ACCOUNT : "is a"
    ACCOUNT ||--o| SAVINGS_ACCOUNT : "is a"
    ACCOUNT ||--o{ LEDGER_ENTRY : "records"
    ACCOUNT ||--o{ TRANSFER : "is source of"
    ACCOUNT ||--o{ TRANSFER : "is destination of"
    ACCOUNT ||--o{ STATEMENT : "is covered by"
    ACCOUNT ||--o{ ACCOUNT_FREEZE : "may have"

    TRANSFER ||--o{ TRANSFER_AUDIT : "generates"
    LEDGER_ENTRY }o--|| TRANSFER : "may be correlated with"

    CUSTOMER {
        UUID customer_id PK
        string legal_name "mandatory"
        string tax_id "mandatory, unique"
        string email "mandatory, unique"
        string street "composite: address"
        string city "composite: address"
        string postal_code "composite: address"
        string country "composite: address"
        string kyc_status "enum: PENDING APPROVED REJECTED"
        timestamp created_at
    }
    PHONE_NUMBER {
        UUID customer_id PK_FK
        string phone_number PK
        string label "HOME WORK MOBILE"
    }
    ACCOUNT {
        UUID account_id PK
        string iban "mandatory, unique"
        UUID customer_id FK
        decimal balance_amount "composite: money"
        char balance_currency "composite: money"
        string status "enum: PENDING ACTIVE FROZEN CLOSED"
        string account_type "discriminator: CHECKING SAVINGS"
        timestamp opened_at
    }
    CHECKING_ACCOUNT {
        UUID account_id PK_FK
        decimal overdraft_limit_amount "composite: money"
        char overdraft_limit_currency "composite: money"
    }
    SAVINGS_ACCOUNT {
        UUID account_id PK_FK
        decimal interest_rate
    }
    LEDGER_ENTRY {
        UUID entry_id PK
        UUID account_id FK
        decimal amount "negative=debit, positive=credit"
        char currency
        timestamp occurred_at
        string correlation_id "groups entries of a transfer"
        bigint sequence_in_account
    }
    TRANSFER {
        UUID transfer_id PK
        UUID source_account_id FK
        UUID destination_account_id FK
        decimal amount
        char currency
        string status "enum: PENDING COMPLETED FAILED FRAUD_REVIEW"
        string idempotency_key "unique"
        timestamp created_at
    }
    STATEMENT {
        UUID statement_id PK
        UUID account_id FK
        date period_start
        date period_end
        decimal opening_balance_amount
        char opening_balance_currency
        decimal closing_balance_amount
        char closing_balance_currency
    }
    NOTIFICATION {
        UUID notification_id PK
        UUID customer_id FK
        string channel "EMAIL SMS PUSH"
        string template_id
        json payload
        string status "PENDING SENT FAILED"
        timestamp sent_at
    }
    ACCOUNT_FREEZE {
        UUID freeze_id PK
        UUID account_id FK
        string reason
        timestamp frozen_at
        timestamp thawed_at "null until unfrozen"
        string frozen_by "actor id"
    }
    TRANSFER_AUDIT {
        UUID audit_id PK
        UUID transfer_id FK
        string action "CREATED EXECUTED FAILED FLAGGED"
        string actor_id
        timestamp at
        json before
        json after
    }
```

### The entities, in plain English

- **CUSTOMER** — A person or organization that owns one or more Accounts. Identified by `customer_id`. Has a name, tax id, email, address (composite), KYC status, and one or more phone numbers.
- **PHONE_NUMBER** — A weak entity belonging to a Customer. Multi-valued attribute made into a child table. Identified by `(customer_id, phone_number)`.
- **ACCOUNT** — A financial container owned by a Customer. Identified by `account_id`, with logical identity `iban`. Has a Money balance (composite), a status (lifecycle enum), and a discriminator (`account_type`).
- **CHECKING_ACCOUNT** — A subtype of Account. Adds an overdraft limit (Money composite). Permits negative balances up to the limit.
- **SAVINGS_ACCOUNT** — A subtype of Account. Adds an interest rate. Does not permit overdraft.
- **LEDGER_ENTRY** — A weak entity belonging to an Account. An immutable record of a single monetary movement. Identified by `entry_id` (surrogate) with a natural key `(account_id, sequence_in_account)`.
- **TRANSFER** — A request to move Money from one Account (source) to another (destination). Produces two LedgerEntries (one debit, one credit) correlated by `correlation_id`. Has a status and an idempotency key.
- **STATEMENT** — A periodic summary of an Account's activity. Covers one Account for one period (start, end). Records opening and closing balances.
- **NOTIFICATION** — A message to be sent to a Customer. Has a channel (email/SMS/push), template, payload, and status.
- **ACCOUNT_FREEZE** — A record of an Account being frozen. Each freeze has a reason, a frozen-at timestamp, an actor, and (eventually) a thawed-at timestamp. An Account may have many freezes over its lifetime (one-to-many).
- **TRANSFER_AUDIT** — An audit log entry for a Transfer. Each transfer generates multiple audit entries (created, executed, failed, flagged). Append-only.

### The relationships and cardinalities

| Relationship | Cardinality | Optionality | Notes |
|---|---|---|---|
| Customer → Account | 1:N | Customer side: optional (a customer may have no accounts); Account side: mandatory (every account has a customer) | FK on Account |
| Customer → PhoneNumber | 1:N | Both: a customer must have at least one phone (mandatory); each phone belongs to one customer | Child table |
| Customer → Notification | 1:N | Mandatory on Notification side | FK on Notification |
| Customer → Statement | 1:N | Mandatory on Statement side | FK on Statement (via account) |
| Account → CheckingAccount | 1:0..1 | Optional subtype | CTI: shared PK |
| Account → SavingsAccount | 1:0..1 | Optional subtype | CTI: shared PK |
| Account → LedgerEntry | 1:N | Mandatory on LedgerEntry side | FK on LedgerEntry |
| Account → Transfer (source) | 1:N | Mandatory on Transfer side | FK on Transfer |
| Account → Transfer (destination) | 1:N | Mandatory on Transfer side | FK on Transfer |
| Account → Statement | 1:N | Mandatory on Statement side | FK on Statement |
| Account → AccountFreeze | 1:N | Mandatory on AccountFreeze side; optional on Account side | FK on AccountFreeze |
| Transfer → TransferAudit | 1:N | Mandatory on TransferAudit side | FK on TransferAudit |
| LedgerEntry ↔ Transfer | N:0..1 | Optional correlation — a LedgerEntry may belong to a Transfer (and a Transfer has 2 LedgerEntries) | FK `correlation_id` on LedgerEntry, nullable |

### Where ER is straightforward

The following translations are mechanical, with no design decisions:

- **Strong entity → table**: `customers`, `accounts`, `transfers`, `statements`, `notifications`.
- **Simple attribute → column**: `legal_name`, `tax_id`, `email`, `iban`, `status`, `account_type`, `interest_rate`.
- **Composite attribute → columns**: `address` becomes `street, city, postal_code, country`; `Money` becomes `amount, currency` (repeated for each money-typed attribute).
- **Many-to-one → foreign key**: `accounts.customer_id`, `ledger_entries.account_id`, `transfers.source_account_id`, `transfers.destination_account_id`, `statements.account_id`, `notifications.customer_id`, `account_freezes.account_id`, `transfer_audits.transfer_id`.
- **Multi-valued attribute → child table**: `phone_numbers` with composite PK `(customer_id, phone_number)`.
- **Weak entity → table with parent FK**: `ledger_entries` with `account_id` FK and a natural key `(account_id, sequence_in_account)`.

### Where ER strains

ER modeling has limits, and the banking domain hits several of them. Each strain is a place where the translation to relational requires a deliberate design choice.

#### 1. Inheritance (subtypes)

The `Account → CheckingAccount / SavingsAccount` subtype relationship has no single relational translation. We chose CTI (class table inheritance) here, with `accounts` as the supertype table and `checking_accounts` / `savings_accounts` as subtype tables sharing the primary key. The alternative (STI) would put all columns in one table with sparse NULLs.

The strain: ER's subtype is a clean "is-a" relationship; the relational model has three lossy translations (STI, CTI, Concrete). The choice depends on query patterns, the differences between subtypes, and the importance of `NOT NULL` constraints. See [[07-Composition-vs-Inheritance]] for the full trade-off.

#### 2. Value objects (composite attributes)

The domain model has `Money`, `IBAN`, `Address`, `OverdraftPolicy`, `InterestRate`, `DateRange` as first-class value objects. ER demotes most of them to composite or simple attributes:

- `Money` → composite attribute `(amount, currency)`. Each occurrence is two columns: `balance_amount, balance_currency`, `overdraft_limit_amount, overdraft_limit_currency`, etc. Verbose but normalizable.
- `IBAN` → simple attribute. The validation logic that lives in the value object (see [[01-Entities-Value-Objects]]) is lost at the ER layer — it must be re-expressed as a `CHECK` constraint at the schema layer.
- `Address` → composite attribute `(street, city, postal_code, country)`. The immutability and equality semantics of the value object are lost.
- `OverdraftPolicy` → composite attribute on `checking_accounts`. The behavior `ensureAllowed(newBalance)` is lost — it must be re-expressed as a `CHECK` constraint `balance_amount >= -overdraft_limit_amount`.
- `InterestRate` → simple attribute. The `dailyAccrual(principal)` method is lost.

The strain: value objects in DDD combine *data + behavior*. ER captures only the data; the behavior must be re-expressed in `CHECK` constraints, triggers, or application logic. This is one of the canonical impedance mismatches — see [[00-ORM-Impedance-Mismatch]].

#### 3. Domain events

The domain model has events: `TransferCompleted`, `AccountFrozen`, `BalanceLowThresholdReached`. ER has no concept of events. To persist them, we model them as entities:

- `AccountFrozen` becomes `ACCOUNT_FREEZE` — an entity recording each freeze event with its reason, timestamp, and actor.
- `TransferCompleted` is *not* modeled directly — it is represented by the `Transfer` row reaching `status = COMPLETED` and the two `LedgerEntry` rows being created. The event is implicit in the state change.
- `BalanceLowThresholdReached` is *not* modeled — it is a derived fact, computed when the balance crosses a threshold.

The strain: events are facts about things that happened; ER is a model of things that exist. To capture events, we either model them as entities (verbose but explicit) or compute them from state changes (compact but lossy). The transactional outbox pattern (see [[04-Domain-Events]]) bridges this gap by storing events in a separate `outbox` table — but that table is not part of the ER model; it is infrastructure.

#### 4. Aggregate boundaries

The domain model has explicit aggregate boundaries: the `Account` aggregate (root + LedgerEntries), the `Transfer` aggregate, the `Customer` aggregate. ER has no aggregate concept — every entity is a table, and the boundaries are expressed only through foreign keys and transactional discipline.

The strain: a query that joins `accounts` and `ledger_entries` does not know it is crossing an aggregate boundary. The application layer must enforce "only the `Account` aggregate may mutate its `LedgerEntries`" — the schema cannot. This is why ORMs have concepts like "cascade" and "orphan removal" — they are attempts to express aggregate boundaries at the persistence layer.

#### 5. Immutability

`LedgerEntry` is immutable in the domain model — once written, never modified or deleted. ER has no immutability concept; a row is a row, and any `UPDATE` or `DELETE` is allowed at the relational layer.

The strain: immutability must be enforced at the schema layer via triggers (reject `UPDATE` and `DELETE` on `ledger_entries`) or at the application layer via repository discipline. See [[03-Triggers-As-Constraints]] for the trigger approach.

#### 6. Lifecycle state machines

`AccountStatus` is a state machine: `PENDING → ACTIVE → FROZEN → CLOSED`, with rules about which transitions are legal. ER captures only the current status as an attribute. The state machine is lost.

The strain: the transition rules must be enforced via triggers (rejecting illegal transitions), application logic, or a separate `account_status_transitions` audit table. The ER diagram itself cannot express "you cannot go from CLOSED back to ACTIVE."

#### 7. Double-entry invariant

The domain model has the invariant: "every Transfer produces exactly two LedgerEntries (one debit, one credit) summing to zero." ER has no way to express this. It is a multi-table invariant.

The strain: this invariant must be enforced at the application layer (the `Transfer.execute` method writes both entries atomically) and reinforced at the schema layer via a `correlation_id` that groups the two entries. The schema cannot enforce "exactly two entries per transfer, summing to zero" — that requires a trigger or a materialized view with a check.

## Banking application

### The transfer flow, viewed through the ER lens

When a transfer executes:

1. A `TRANSFER` row is created with `status = PENDING`, source and destination account IDs, amount, and idempotency key.
2. The source `ACCOUNT` row is updated (balance decreases).
3. The destination `ACCOUNT` row is updated (balance increases).
4. Two `LEDGER_ENTRY` rows are inserted: one for the source (negative amount), one for the destination (positive amount), both with the same `correlation_id` (the transfer ID).
5. The `TRANSFER` row is updated to `status = COMPLETED`.
6. A `TRANSFER_AUDIT` row is inserted recording the execution.
7. (If the account crosses a threshold, an `ACCOUNT_FREEZE` may be created — but this is a separate flow.)

All of this happens in one transaction (see [[00-ACID]] and [[09-Banking-Transaction-Walkthrough]]). The ER diagram shows *what* tables are touched; it does not show *how* they are coordinated.

### Why the ER diagram is necessary but not sufficient

The ER diagram is necessary because:

- It captures the entities and relationships in a form domain experts can validate.
- It is the source of truth for the schema. Every table in [[04-Banking-Schema]] traces back to an entity here.
- It is the source of truth for the ORM mapping. Every entity in [[07-Banking-ORM-Mapping]] traces back to an entity here.

The ER diagram is not sufficient because:

- It does not capture behavior (invariants, lifecycle, immutability). Those live in the domain model and the schema constraints.
- It does not capture transactions. Those live in the application layer and the database's transaction manager.
- It does not capture events. Those live in the domain model and the outbox.
- It does not capture aggregate boundaries. Those live in the domain model.

ER is the picture of *what exists*. The full design needs ER *plus* the domain model *plus* the schema constraints *plus* the transaction policy. Each layer adds what the layer above could not express.

## Code/diagrams

A compact version of the ER diagram, suitable for a design review slide:

```mermaid
erDiagram
    CUSTOMER ||--o{ ACCOUNT : owns
    CUSTOMER ||--o{ NOTIFICATION : receives
    ACCOUNT ||--o{ LEDGER_ENTRY : records
    ACCOUNT ||--o{ TRANSFER : "source of"
    ACCOUNT ||--o{ TRANSFER : "destination of"
    ACCOUNT ||--o{ STATEMENT : "covered by"
    ACCOUNT ||--o| CHECKING_ACCOUNT : "is a"
    ACCOUNT ||--o| SAVINGS_ACCOUNT : "is a"
    TRANSFER ||--o{ TRANSFER_AUDIT : generates

    CUSTOMER {
        UUID customer_id PK
        string legal_name
        string tax_id UK
        string email UK
        string kyc_status
    }
    ACCOUNT {
        UUID account_id PK
        string iban UK
        UUID customer_id FK
        decimal balance_amount
        char balance_currency
        string status
        string account_type
    }
    LEDGER_ENTRY {
        UUID entry_id PK
        UUID account_id FK
        decimal amount
        timestamp occurred_at
        string correlation_id
    }
    TRANSFER {
        UUID transfer_id PK
        UUID source_account_id FK
        UUID destination_account_id FK
        decimal amount
        string status
        string idempotency_key UK
    }
    STATEMENT {
        UUID statement_id PK
        UUID account_id FK
        date period_start
        date period_end
    }
    CHECKING_ACCOUNT {
        UUID account_id PK_FK
        decimal overdraft_limit_amount
    }
    SAVINGS_ACCOUNT {
        UUID account_id PK_FK
        decimal interest_rate
    }
    NOTIFICATION {
        UUID notification_id PK
        UUID customer_id FK
        string channel
        string status
    }
    TRANSFER_AUDIT {
        UUID audit_id PK
        UUID transfer_id FK
        string action
        timestamp at
    }
```

## What can go wrong

- **Missing subtype strategy.** Drawing `Account → CheckingAccount / SavingsAccount` without choosing STI, CTI, or Concrete. The ER diagram is incomplete; the schema cannot be generated.
- **Missing cardinalities.** "Customer has Accounts" — but how many? Mandatory or optional? Without cardinalities, the FK constraints cannot be written.
- **Modeling events as entities when they should be derived.** A `TransferCompletedEvent` table that duplicates the `transfers` table. Either model the event as an entity (and accept duplication) or derive it (and accept loss). Don't do both.
- **Modeling value objects as entities.** A `moneys` table with `id, amount, currency` and foreign keys from everywhere. Bloats the schema with joins. Use composite columns.
- **Missing natural identity constraints.** `ledger_entries` with a surrogate `entry_id` but no `UNIQUE (account_id, sequence_in_account)`. Allows duplicate sequence numbers.
- **Forgetting the audit table.** No `transfer_audits` table; the system cannot reconstruct what happened. Audit is an entity, not an afterthought.
- **Inheritance modeled as two separate entities.** `CheckingAccount` and `SavingsAccount` as unrelated tables, with `accounts` not existing. IBAN uniqueness cannot be enforced across both. Use a supertype.
- **Composite attribute as a single string column.** `address TEXT` containing "123 Main St, Springfield, IL 62701". Cannot query by city, cannot index by postal code. Flatten.
- **Missing `CHECK` constraints.** ER shows `status` as an enum, but the schema doesn't have `CHECK (status IN (...))`. The constraint is lost in translation.

## Trade-offs

- **STI vs CTI for Account subtypes.** STI: one table, sparse columns, polymorphic queries fast. CTI: separate tables, `NOT NULL` on subtype fields, polymorphic queries need `JOIN`. We chose CTI for the banking schema because subtype-specific `NOT NULL` matters (overdraft limit must be set for checking; interest rate must be set for savings). See [[04-Banking-Schema]] for the actual choice.
- **Composite vs surrogate key for LedgerEntry.** Composite `(account_id, sequence)`: meaningful, enforces natural identity. Surrogate `entry_id`: easy to reference. We chose surrogate + `UNIQUE` because the entries are referenced by `correlation_id` and by audit tables.
- **Model events as entities or derive from state.** Entities: explicit, queryable, but duplicate data. Derived: compact, but require computation. We model `AccountFreeze` as an entity (because freezes have their own attributes) and derive `TransferCompleted` from the `Transfer` status (because the event is fully captured by the state change).
- **One `notifications` table or per-channel tables.** One table: simpler, polymorphic. Per-channel: cleaner per-channel schema, but unions for "all notifications." We chose one table with a `channel` discriminator.
- **Audit table per entity or one global audit table.** Per-entity: clean, queryable, but many tables. Global: one table, JSON `before`/`after`, but harder to query. We chose per-entity for critical flows (`transfer_audits`) and a global audit log for cross-cutting concerns.
- **Store `Money` as `amount + currency` or as a single composite type.** Two columns: standard SQL, queryable, indexable. Composite type: compact, but PostgreSQL-specific and harder to query. We chose two columns for portability.
- **Phone numbers as child table or JSONB array.** Child table: normalizable, queryable. JSONB: compact, but loses constraints. We chose child table because phone numbers have a `label` and may be queried ("find all customers with a mobile number").

## Forward links

- [[04-Banking-Schema]] — the actual schema, with every trade-off resolved.
- [[07-Banking-ORM-Mapping]] — how the entities map to Hibernate.
- [[09-Banking-SQL]] — the SQL that operates on this schema.
- [[11-Banking-Normalization-Walkthrough]] — normalizing this schema to BCNF.
- [[00-ER-Modeling]] — the theory behind this diagram.
- [[01-ER-to-Relational]] — the rules used to translate it.
- [[06-Banking-Domain-Model]] — the domain model this ER diagram captures.
- [[00-Banking-Case-Study]] — the invariants this schema must enforce.
- [[01-Primary-Foreign-Keys]] — how the FKs in this diagram are enforced.
- [[02-Domain-Check-Constraints]] — how the enums and value-object invariants are enforced.
- [[03-Triggers-As-Constraints]] — how immutability and lifecycle transitions are enforced.
- [[00-ORM-Impedance-Mismatch]] — where this ER diagram and the domain model disagree.
- [[00-Relational-Model]] — the layer this diagram translates to.
- [[00-SQL-From-Relational-Algebra]] — the SQL that operates on the translated schema.
