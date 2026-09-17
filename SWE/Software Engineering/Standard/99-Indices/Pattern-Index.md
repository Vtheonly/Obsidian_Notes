# Pattern Index

> All patterns covered in the vault, organized by category. Each entry links to the chapter that teaches it and shows where the Banking case study applies it.

## How to use this index

A pattern is a documented solution to a recurring set of forces (see [[00-Patterns-As-Documented-Forces]]). Use this index to:

1. **Look up a pattern by name** when you encounter it in code or in a review.
2. **Find a pattern for a problem** — scan the categories below.
3. **See the Banking application** of each pattern.

---

## GoF Creational Patterns

> Patterns that abstract object construction. The problem: construction logic scattered across callers; the fix: encapsulate the construction.

| Pattern | Problem | Chapter | Banking application |
|---|---|---|---|
| **Abstract Factory** | Create families of related objects without specifying concrete classes | [[01-Creational-Patterns]] | `PersistenceFactory` returning either JPA or JDBC repositories for tests vs production |
| **Builder** | Construct complex objects step by step; avoid telescoping constructors | [[01-Creational-Patterns]] | `TransferRequest.builder().from(a).to(b).amount(100).idempotencyKey("...").build()` |
| **Factory Method** | Defer instantiation to subclasses | [[01-Creational-Patterns]] | `NotificationService.create(channel)` returning EmailNotification or SmsNotification |
| **Prototype** | Clone existing objects instead of constructing from scratch | [[01-Creational-Patterns]] | Cloning a template account configuration |
| **Singleton** | One instance per JVM | [[01-Creational-Patterns]] | Often an anti-pattern; see [[05-Anti-Patterns]]. Use DI instead. |

## GoF Structural Patterns

> Patterns that compose objects into larger structures. The problem: the structure of objects does not match the structure of the problem; the fix: introduce an adapter or wrapper.

| Pattern | Problem | Chapter | Banking application |
|---|---|---|---|
| **Adapter** | Make incompatible interfaces work together | [[02-Structural-Patterns]] | Adapting a legacy payment gateway to the modern `PaymentProvider` interface |
| **Bridge** | Decouple abstraction from implementation | [[02-Structural-Patterns]] | `Notification` abstraction bridged to `EmailSender` or `SmsSender` implementations |
| **Composite** | Treat individual objects and compositions uniformly | [[02-Structural-Patterns]] | A composite `FraudRule` that combines multiple sub-rules with AND/OR logic |
| **Decorator** | Add behavior without modifying the original | [[02-Structural-Patterns]] | `LoggingTransferService` wrapping `TransferService`; `AuditingAccount` wrapping `Account` |
| **Facade** | Provide a simplified interface to a complex subsystem | [[02-Structural-Patterns]] | `TransferService` as the facade hiding Account + Ledger + Fraud + Notification |
| **Flyweight** | Share state across many objects to save memory | [[02-Structural-Patterns]] | Sharing `Currency` instances; sharing `InterestRate` immutable objects |
| **Proxy** | Control access to another object | [[02-Structural-Patterns]] | Hibernate's lazy-loading proxy for `Account.ledgerEntries`; access-control proxy |

## GoF Behavioral Patterns

> Patterns that assign responsibilities among objects. The problem: who does what, and how do they communicate; the fix: introduce an indirection.

| Pattern | Problem | Chapter | Banking application |
|---|---|---|---|
| **Chain of Responsibility** | Pass a request along a chain of handlers | [[03-Behavioral-Patterns]] | Fraud rules: large-amount rule → new-beneficiary rule → velocity rule → default |
| **Command** | Encapsulate a request as an object | [[03-Behavioral-Patterns]] | `TransferCommand` enabling undo, queueing, and retry |
| **Interpreter** | Define a language and interpret it | [[03-Behavioral-Patterns]] | (out of scope for Banking) |
| **Iterator** | Traverse a collection without exposing its representation | [[03-Behavioral-Patterns]] | Iterating `LedgerEntry` stream without loading all into memory |
| **Mediator** | Centralize complex communication | [[03-Behavioral-Patterns]] | `TransferService` mediating between Account, Fraud, Notification |
| **Memento** | Capture and restore state | [[03-Behavioral-Patterns]] | Snapshot before a multi-step mutation for rollback; `AccountMemento` |
| **Observer** | Notify dependents of state changes | [[03-Behavioral-Patterns]] | `TransferCompleted` event published; NotificationService observes and reacts |
| **State** | Change behavior as state changes | [[03-Behavioral-Patterns]] | Account lifecycle: PENDING / ACTIVE / FROZEN / CLOSED behaviors |
| **Strategy** | Encapsulate interchangeable algorithms | [[03-Behavioral-Patterns]] | `InterestPolicy` (Savings vs Checking vs MoneyMarket) |
| **Template Method** | Define an algorithm skeleton, defer steps to subclasses | [[03-Behavioral-Patterns]] | `StatementGenerator.generate()` calls `computeHeader()`, `computeRows()`, `computeFooter()` |
| **Visitor** | Separate operations from object structure | [[03-Behavioral-Patterns]] | `ReportVisitor` walking the account hierarchy to produce compliance reports |

## Enterprise Patterns (Fowler / DDD)

> Patterns for the application and domain layers. The problem: where does business logic live, and how does it persist; the fix: introduce named layers and abstractions.

| Pattern | Problem | Chapter | Banking application |
|---|---|---|---|
| **Repository** | Mediate between domain and data layer with a collection-like interface | [[05-Repository-Pattern]], [[04-Enterprise-Patterns]] | `AccountRepository.findById(id)`, `findByIban(iban)` |
| **Unit of Work** | Track changes and write them out as a unit | [[04-Unit-of-Work]], [[04-Enterprise-Patterns]] | Hibernate `EntityManager`; the transfer flow debits + credits + ledger entries committed atomically |
| **Identity Map** | Ensure one in-memory object per row per session | [[01-Identity-Map]], [[04-Enterprise-Patterns]] | Hibernate `PersistenceContext` |
| **Service Layer** | Coordinate use cases; thin layer above the domain | [[04-Enterprise-Patterns]] | `TransferService`, `StatementService`, `InterestService` |
| **Domain Events** | Decouple producers from consumers via past-tense events | [[04-Domain-Events]], [[04-Enterprise-Patterns]] | `TransferCompleted`, `AccountFrozen`, `BalanceLowThresholdReached` |
| **CQRS** | Separate read models from write models | [[04-Enterprise-Patterns]] | Write model = entities + repository; read model = DTOs + optimized queries + materialized views |
| **Event Sourcing** | Store events as the source of truth; derive state by replay | [[04-Enterprise-Patterns]] | The `ledger_entries` table IS an event log; account balance is derived by `SUM(amount)` |
| **Aggregate** | Consistency boundary around a cluster of objects | [[02-Aggregates]] | Account + its LedgerEntry children = one aggregate |
| **Bounded Context** | Boundary within which a model is consistent | [[03-Bounded-Contexts]] | Account Management, Identity & Access, Audit, Reporting |
| **Anticorruption Layer** | Translate between contexts to prevent model pollution | [[03-Bounded-Contexts]] | Translating the legacy CRM's `customer_record` to the modern `Customer` entity |
| **Outbox Pattern** | Reliably publish events after a transaction commits | [[04-Domain-Events]] | Writing `TransferCompleted` to an outbox table in the same transaction as the transfer |
| **Saga** | Coordinate a multi-step transaction across services | [[07-Distributed-Transactions]] | Cross-bank transfer: debit at Bank A → credit at Bank B → compensate on failure |
| **Specification** | Encapsulate a business rule as a composable predicate | [[05-Repository-Pattern]] | `OverdueAccountSpec`, `HighValueTransferSpec` composable with AND/OR |

## Concurrency Patterns

| Pattern | Problem | Chapter | Banking application |
|---|---|---|---|
| **Optimistic Locking** | Detect conflicts at commit time using a version field | [[04-Unit-of-Work]] | `@Version` on Account for transfer conflicts |
| **Pessimistic Locking** | Lock rows to prevent conflicts | [[02-DML]], [[03-Two-Phase-Locking]] | `SELECT ... FOR UPDATE` on the source account |
| **Lock Ordering** | Acquire locks in a canonical order to prevent deadlocks | [[06-Deadlocks]] | Always lock the lower account ID first in transfers |
| **Retry on Conflict** | Retry transactions aborted by serializability conflicts | [[05-Serializability]] | Retry on `SQLSTATE 40001` |
| **Idempotency Key** | Make operations safe to retry | [[02-DML]], [[00-Banking-Case-Study]] | `idempotency_key` column with `ON CONFLICT DO NOTHING` |

## Architecture Patterns

| Pattern | Problem | Chapter | Banking application |
|---|---|---|---|
| **Layered Architecture** | Separate concerns into stacked layers | [[02-Layered-Architecture]] | Presentation → Application → Domain → Infrastructure |
| **Hexagonal (Ports & Adapters)** | Isolate the domain from technology | [[03-Hexagonal-Architecture]] | Domain exposes `TransferPort`; REST controller and JPA repository are adapters |
| **Clean Architecture** | Concentric circles with the Dependency Rule | [[04-Clean-Architecture]] | Entities → Use Cases → Interface Adapters → Frameworks |
| **Microservices** | Decompose by bounded context | [[05-Architecture-Trade-offs]] | One service per bounded context for the global bank |
| **Event-Driven Architecture** | Communicate via events rather than RPCs | [[04-Domain-Events]] | TransferService publishes `TransferRequested`; FraudService consumes |
| **CQRS** | Split read and write models | [[04-Enterprise-Patterns]] | Write to `accounts` / `ledger_entries`; read from `daily_balances` materialized view |

## Database Patterns

| Pattern | Problem | Chapter | Banking application |
|---|---|---|---|
| **Single Table Inheritance (STI)** | Persist a class hierarchy in one table | [[07-Composition-vs-Inheritance]], [[00-ORM-Impedance-Mismatch]] | All account types in `accounts` with a discriminator column |
| **Class Table Inheritance (CTI)** | Persist a class hierarchy across linked tables | [[07-Composition-vs-Inheritance]] | `accounts` + `checking_accounts` + `savings_accounts` |
| **Concrete Table Inheritance** | One table per concrete subclass | [[07-Composition-vs-Inheritance]] | Avoided in Banking due to shared invariants |
| **Materialized View** | Pre-compute a query result for fast reads | [[07-Views-Materialized-Views]] | `daily_balances` materialized view refreshed nightly |
| **Partitioning** | Split a logical table into physical pieces | [[04-Partitioning-And-Sharding]] | `ledger_entries` partitioned by month |
| **Sharding** | Distribute data across databases | [[03-Sharding-Revisited]] | Accounts sharded by `customer_id` hash for global scale |
| **Outbox Table** | Publish events reliably from within a transaction | [[04-Domain-Events]] | `outbox_events` table written in same transaction as the transfer |
| **Polyglot Persistence** | Different stores for different needs | [[05-Banking-NoSQL-Choice]] | PostgreSQL (truth), Cassandra (event log), Redis (cache), Neo4j (fraud), ES (search) |

## Anti-Patterns

> Catalogued in [[05-Anti-Patterns]]. Each is a violation of foundational principles.

| Anti-pattern | Symptom | Cure |
|---|---|---|
| **God Object** | One class does everything | Split by responsibility |
| **Spaghetti Code** | No structure, hard to follow | Introduce layers |
| **Golden Hammer** | One tool/pattern used everywhere | Learn alternatives |
| **Magic Numbers** | Unexplained constants in code | Named constants |
| **Poltergeist** | Short-lived objects that just pass data through | Remove them; let callers talk directly |
| **Boat Anchor** | Unused code kept "just in case" | Delete; version control remembers |
| **Input Kludge** | Ad hoc input validation scattered around | Centralize at boundaries |
| **Zero Means Null** | Using 0 / empty string to mean absence | Use `Optional` or `null` explicitly |
| **Anemic Domain Model** | Entities are data bags; services hold behavior | Move behavior to the entity that owns the invariant |
| **Singleton Abuse** | Singletons used as global variables | Use DI; if one instance is needed, enforce it via container |
| **Open Session In View** | Holding a Hibernate session open for the whole HTTP request | Close the session in the service layer; use DTOs for the view |
| **Premature Optimization** | Optimizing without measurement | Measure first ([[00-Query-Optimization-Strategy]]) |

## Cross-references

- [[Concept-Index]] — alphabetical index of all concepts.
- [[Cross-Reference-Map]] — how the five forces map across layers.
- [[00-Map-of-Content]] — the master navigation.
