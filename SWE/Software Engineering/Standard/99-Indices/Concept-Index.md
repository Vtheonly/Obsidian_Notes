# Concept Index

> Alphabetical index of every concept in the vault, with the primary chapter that defines it and the chapters that apply it.

## How to use this index

Look up a term you have encountered. The primary chapter teaches the concept; the application chapters show it in action across the layers.

---

## A

- **Abstraction** — Primary: [[04-Abstraction-and-Models]]. Applications: [[00-UML-As-Modeling-Language]], [[07-Views-Materialized-Views]], [[00-Schema-Design]], [[06-Abstract-Classes-And-Interfaces]].
- **ACID** — Primary: [[00-ACID]]. Applications: [[06-Transactions-In-SQL]], [[09-Banking-Transaction-Walkthrough]], [[02-Aggregates]].
- **Activity diagram** — Primary: [[03-Activity-Diagrams]].
- **Aggregate** — Primary: [[02-Aggregates]]. Applications: [[00-Domain-Modeling]], [[04-Enterprise-Patterns]], [[02-Aggregates]] (Banking).
- **Anemic domain model** — Primary: [[05-Anemic-vs-Rich-Models]].
- **Anomaly (concurrency)** — Primary: [[01-Concurrency-Anomalies]]. Applications: [[02-Isolation-Levels]], [[04-MVCC]], [[05-Serializability]].
- **Anti-pattern** — Primary: [[05-Anti-Patterns]].
- **Anticorruption Layer** — Primary: [[03-Bounded-Contexts]].
- **ARIES** — Primary: [[01-ARIES]]. Applications: [[04-Banking-Recovery-Scenario]].
- **Armstrong's axioms** — Primary: [[03-Functional-Dependencies]].
- **Association** — Primary: [[00-Object-Relationships]]. Applications: [[01-Class-Diagrams]].
- **Asynchronous replication** — Primary: [[02-Replication]]. Applications: [[03-Backup-And-Recovery]].
- **Atomicity** — Primary: [[00-ACID]]. Applications: [[02-DML]], [[06-Transactions-In-SQL]].
- **Attribute closure** — Primary: [[03-Functional-Dependencies]].
- **Attribute (relational)** — Primary: [[01-Relations-Tuples-Attributes]].

## B

- **B-tree index** — Primary: [[03-B-Tree-Indexes]]. Applications: [[01-Indexing-Strategy]], [[09-Banking-Query-Plans]].
- **B+tree** — Primary: [[03-B-Tree-Indexes]].
- **Backup** — Primary: [[03-Backup-And-Recovery]].
- **BCNF** — Primary: [[07-BCNF]]. Applications: [[11-Banking-Normalization-Walkthrough]].
- **Begin/Commit/Rollback** — Primary: [[06-Transactions-In-SQL]].
- **Bounded context** — Primary: [[03-Bounded-Contexts]]. Applications: [[00-Domain-Modeling]], [[05-Banking-NoSQL-Choice]].
- **Buffer pool** — Primary: [[02-Buffer-Pool]]. Applications: [[00-Storage-Hierarchy]], [[01-Pages-And-Files]].
- **Builder pattern** — Primary: [[01-Creational-Patterns]].

## C

- **Caching** — Primary: [[03-Caching]]. Applications: [[05-Banking-Performance-Tuning]].
- **CAP theorem** — Primary: [[00-CAP-PACELC]]. Applications: [[04-Eventual-Consistency]], [[05-Banking-Distributed-Design]].
- **Candidate key** — Primary: [[02-Keys-Superkeys-Candidate-Keys]].
- **CHECK constraint** — Primary: [[02-Domain-Check-Constraints]]. Applications: [[04-Banking-Schema]], [[03-Triggers-As-Constraints]].
- **Checkpoint** — Primary: [[02-Checkpoints]]. Applications: [[01-ARIES]], [[04-Banking-Recovery-Scenario]].
- **Class** — Primary: [[01-Objects-And-Classes]]. Applications: [[02-Encapsulation]], [[01-Class-Diagrams]].
- **Class diagram** — Primary: [[01-Class-Diagrams]].
- **Class Table Inheritance (CTI)** — Primary: [[07-Composition-vs-Inheritance]], [[00-ORM-Impedance-Mismatch]].
- **Clean Architecture** — Primary: [[04-Clean-Architecture]].
- **Codd, E.F.** — Primary: [[00-Relational-Model]].
- **Cohesion** — Primary: [[06-Coupling-and-Cohesion]]. Applications: [[01-SRP]], [[02-Aggregates]].
- **Command pattern** — Primary: [[03-Behavioral-Patterns]].
- **Commit** — Primary: [[06-Transactions-In-SQL]]. Applications: [[00-ACID]], [[00-WAL-Logging]].
- **Communication diagram** — mentioned in [[00-UML-As-Modeling-Language]].
- **Composite pattern** — Primary: [[02-Structural-Patterns]].
- **Composition** — Primary: [[07-Composition-vs-Inheritance]]. Applications: [[05-Composition-Over-Inheritance]], [[00-Object-Relationships]].
- **Concurrency anomaly** — Primary: [[01-Concurrency-Anomalies]].
- **Consistency (ACID)** — Primary: [[00-ACID]]. Applications: [[02-Domain-Check-Constraints]], [[02-Aggregates]].
- **Constraint** — Primary: [[02-Domain-Check-Constraints]]. Applications: [[03-Triggers-As-Constraints]], [[04-Banking-Schema]].
- **Concrete Table Inheritance** — Primary: [[07-Composition-vs-Inheritance]], [[00-ORM-Impedance-Mismatch]].
- **Conway's Law** — Primary: [[01-Design-Forces]].
- **Cost-Based Optimizer (CBO)** — Primary: [[07-Cost-Based-Optimizer]]. Applications: [[08-Reading-EXPLAIN]], [[09-Banking-Query-Plans]].
- **Coupling** — Primary: [[06-Coupling-and-Cohesion]]. Applications: [[00-SOLID-as-Dependency-Management]], [[03-Law-of-Demeter]].
- **CRC cards** — Primary: [[02-CRC-Cards]]. Applications: [[04-Responsibilities]].
- **CQRS** — Primary: [[04-Enterprise-Patterns]]. Applications: [[05-Repository-Pattern]], [[03-N-plus-1-Problem]].
- **CRDT** — Primary: [[04-Eventual-Consistency]].

## D

- **Database normalization** — Primary: [[06-1NF-2NF-3NF]] through [[09-DKNF]].
- **Deadlock** — Primary: [[06-Deadlocks]]. Applications: [[03-Two-Phase-Locking]], [[09-Banking-Transaction-Walkthrough]].
- **Decorator pattern** — Primary: [[02-Structural-Patterns]].
- **Denormalization** — Primary: [[02-Denormalization-For-Reads]]. Applications: [[10-Normalization-Trade-offs]], [[07-Views-Materialized-Views]].
- **Dependency** — Primary: [[03-Dependency-As-Root-Concept]]. Applications: every chapter.
- **Dependency Injection (DI)** — Primary: [[05-DIP]].
- **Dependency Inversion Principle (DIP)** — Primary: [[05-DIP]].
- **Deployment diagram** — Primary: [[05-Component-And-Deployment]].
- **DKNF** — Primary: [[09-DKNF]].
- **Document store** — Primary: [[01-Document-Stores]].
- **Domain event** — Primary: [[04-Domain-Events]]. Applications: [[04-Enterprise-Patterns]].
- **Domain model** — Primary: [[00-Domain-Modeling]]. Applications: [[06-Banking-Domain-Model]].
- **Domain-Driven Design (DDD)** — Primary: [[00-Domain-Modeling]].
- **Double-entry bookkeeping** — Primary: [[00-Banking-Case-Study]].
- **Dirty read** — Primary: [[01-Concurrency-Anomalies]].
- **Durability** — Primary: [[00-ACID]]. Applications: [[00-WAL-Logging]], [[03-Backup-And-Recovery]].
- **Dynamic dispatch** — Primary: [[04-Polymorphism]].

## E

- **Eager loading** — Primary: [[02-Lazy-Eager-Loading]].
- **Entity** — Primary: [[01-Entities-Value-Objects]]. Applications: [[05-Identity-State-Lifecycle]].
- **Entity graph (JPA)** — Primary: [[02-Lazy-Eager-Loading]], [[03-N-plus-1-Problem]].
- **ER model** — Primary: [[00-ER-Modeling]]. Applications: [[02-Banking-ER]].
- **Event sourcing** — Primary: [[04-Enterprise-Patterns]]. Applications: [[04-Domain-Events]], [[00-Banking-Case-Study]] (ledger as event log).
- **Eventual consistency** — Primary: [[04-Eventual-Consistency]]. Applications: [[02-Replication]], [[05-Banking-Distributed-Design]].
- **EXPLAIN** — Primary: [[08-Reading-EXPLAIN]]. Applications: [[09-Banking-Query-Plans]], [[00-Query-Optimization-Strategy]].
- **Extension (use case)** — Primary: [[02-Use-Cases]].

## F

- **Facade pattern** — Primary: [[02-Structural-Patterns]].
- **Factory Method** — Primary: [[01-Creational-Patterns]].
- **Foreign key** — Primary: [[01-Primary-Foreign-Keys]]. Applications: [[04-Banking-Schema]], [[01-ER-to-Relational]].
- **4NF** — Primary: [[08-4NF-5NF]].
- **Fragment (sequence diagram)** — Primary: [[02-Sequence-Diagrams]].
- **Functional dependency (FD)** — Primary: [[03-Functional-Dependencies]]. Applications: [[06-1NF-2NF-3NF]], [[07-BCNF]], [[11-Banking-Normalization-Walkthrough]].

## G

- **GEQO** — Primary: [[07-Cost-Based-Optimizer]].
- **God Object** — Primary: [[05-Anti-Patterns]]. Applications: [[01-SRP]], [[04-Responsibilities]].

## H

- **Hash index** — Primary: [[04-Hash-Indexes]]. Applications: [[01-Indexing-Strategy]].
- **Hash join** — Primary: [[05-Join-Algorithms]]. Applications: [[09-Banking-Query-Plans]].
- **Hibernate** — Primary: [[06-Hibernate-JPA]]. Applications: [[07-Banking-ORM-Mapping]], [[01-Identity-Map]].
- **Hexagonal architecture** — Primary: [[03-Hexagonal-Architecture]].

## I

- **Idempotency** — Primary: [[00-Banking-Case-Study]] (invariant 7). Applications: [[02-DML]], [[06-Transactions-In-SQL]], [[04-Domain-Events]].
- **Identity** — Primary: [[05-Identity-State-Lifecycle]]. Applications: [[01-Identity-Map]], [[02-Keys-Superkeys-Candidate-Keys]].
- **Identity Map** — Primary: [[01-Identity-Map]]. Applications: [[04-Enterprise-Patterns]], [[06-Hibernate-JPA]].
- **Impedance mismatch** — Primary: [[00-ORM-Impedance-Mismatch]].
- **Index** — Primary: [[03-B-Tree-Indexes]], [[04-Hash-Indexes]]. Applications: [[01-Indexing-Strategy]], [[05-Join-Algorithms]].
- **Inheritance** — Primary: [[03-Inheritance]], [[07-Composition-vs-Inheritance]]. Applications: [[00-ORM-Impedance-Mismatch]].
- **Interface** — Primary: [[06-Abstract-Classes-And-Interfaces]]. Applications: [[04-ISP]], [[05-DIP]].
- **Interface Segregation Principle (ISP)** — Primary: [[04-ISP]].
- **Invariant** — Primary: [[01-Requirements]]. Applications: [[02-Encapsulation]], [[02-Aggregates]], [[02-Domain-Check-Constraints]].
- **Isolation** — Primary: [[00-ACID]]. Applications: [[02-Isolation-Levels]], [[04-MVCC]], [[05-Serializability]].
- **Isolation level** — Primary: [[02-Isolation-Levels]]. Applications: [[09-Banking-Transaction-Walkthrough]].

## J

- **Join (relational algebra)** — Primary: [[04-Relational-Algebra]].
- **Join algorithm** — Primary: [[05-Join-Algorithms]]. Applications: [[09-Banking-Query-Plans]].
- **JSONB** — Primary: [[01-Document-Stores]]. Applications: [[04-Banking-Schema]].

## K

- **Key (relational)** — Primary: [[02-Keys-Superkeys-Candidate-Keys]].
- **Kyoto Counter / Snowflake ID** — Primary: [[05-Identity-State-Lifecycle]].

## L

- **Lazy loading** — Primary: [[02-Lazy-Eager-Loading]]. Applications: [[03-N-plus-1-Problem]].
- **Law of Demeter** — Primary: [[03-Law-of-Demeter]].
- **Layered architecture** — Primary: [[02-Layered-Architecture]].
- **Ledger (immutable log)** — Primary: [[00-Banking-Case-Study]].
- **Lock** — Primary: [[03-Two-Phase-Locking]]. Applications: [[06-Deadlocks]], [[04-MVCC]].
- **Lost update** — Primary: [[01-Concurrency-Anomalies]]. Applications: [[04-MVCC]], [[09-Banking-Transaction-Walkthrough]].
- **LSN (Log Sequence Number)** — Primary: [[00-WAL-Logging]]. Applications: [[01-ARIES]], [[02-Checkpoints]].

## M

- **Many-to-many relationship** — Primary: [[00-ER-Modeling]]. Applications: [[01-ER-to-Relational]].
- **Materialized view** — Primary: [[07-Views-Materialized-Views]]. Applications: [[02-Denormalization-For-Reads]].
- **Mediator pattern** — Primary: [[03-Behavioral-Patterns]].
- **Memento pattern** — Primary: [[03-Behavioral-Patterns]].
- **MERGE (UPSERT)** — Primary: [[02-DML]].
- **Microservices** — Primary: [[05-Architecture-Trade-offs]]. Applications: [[03-Bounded-Contexts]], [[07-Distributed-Transactions]].
- **MVD (Multi-valued dependency)** — Primary: [[08-4NF-5NF]].
- **MVCC** — Primary: [[04-MVCC]]. Applications: [[02-Isolation-Levels]], [[05-Serializability]].

## N

- **N+1 problem** — Primary: [[03-N-plus-1-Problem]]. Applications: [[02-Lazy-Eager-Loading]], [[05-Repository-Pattern]].
- **Natural key** — Primary: [[02-Keys-Superkeys-Candidate-Keys]]. Applications: [[05-Identity-State-Lifecycle]].
- **Nested loop join** — Primary: [[05-Join-Algorithms]].
- **NoSQL** — Primary: [[00-When-Relational-Strains]]. Applications: [[05-Banking-NoSQL-Choice]].
- **NOT NULL** — Primary: [[02-Domain-Check-Constraints]].
- **Normalization** — Primary: [[06-1NF-2NF-3NF]] through [[09-DKNF]]. Trade-offs: [[10-Normalization-Trade-offs]].

## O

- **Object identity** — Primary: [[05-Identity-State-Lifecycle]]. Applications: [[01-Identity-Map]].
- **Object model** — Primary: [[01-Objects-And-Classes]]. Applications: [[09-Object-Model-vs-Data-Model]] (mentioned in foundations).
- **Observer pattern** — Primary: [[03-Behavioral-Patterns]]. Applications: [[04-Domain-Events]].
- **OLTP vs OLAP** — Primary: [[00-Storage-Hierarchy]], [[02-Denormalization-For-Reads]].
- **ON CONFLICT (UPSERT)** — Primary: [[02-DML]]. Applications: [[09-Banking-SQL]].
- **Open/Closed Principle (OCP)** — Primary: [[02-OCP]].
- **Optimistic locking** — Primary: [[04-Unit-of-Work]]. Applications: [[07-Banking-ORM-Mapping]].
- **Optimization (query)** — Primary: [[00-Query-Optimization-Strategy]]. Applications: [[05-Banking-Performance-Tuning]].
- **Overdraft** — Primary: [[00-Banking-Case-Study]].

## P

- **PACELC** — Primary: [[00-CAP-PACELC]].
- **Page (database)** — Primary: [[01-Pages-And-Files]]. Applications: [[02-Buffer-Pool]], [[03-B-Tree-Indexes]].
- **Partitioning** — Primary: [[04-Partitioning-And-Sharding]]. Applications: [[05-Banking-Performance-Tuning]].
- **Pattern (design)** — Primary: [[00-Patterns-As-Documented-Forces]]. Catalog: [[Pattern-Index]].
- **Phantom read** — Primary: [[01-Concurrency-Anomalies]]. Applications: [[02-Isolation-Levels]].
- **PITR (Point-In-Time Recovery)** — Primary: [[03-Backup-And-Recovery]].
- **PL/pgSQL** — Primary: [[08-Stored-Procedures]].
- **Polymorphism** — Primary: [[04-Polymorphism]]. Applications: [[02-OCP]], [[03-LSP]].
- **PostgreSQL** — used throughout; internals chapters are PG-focused.
- **Pre/post-condition** — Primary: [[03-LSP]]. Applications: [[02-Encapsulation]].
- **Primary key** — Primary: [[02-Keys-Superkeys-Candidate-Keys]]. Applications: [[01-Primary-Foreign-Keys]].
- **Prototype pattern** — Primary: [[01-Creational-Patterns]].
- **Proxy pattern** — Primary: [[02-Structural-Patterns]]. Applications: [[02-Lazy-Eager-Loading]].

## Q

- **Query plan** — Primary: [[06-Query-Processing-Pipeline]]. Applications: [[08-Reading-EXPLAIN]], [[09-Banking-Query-Plans]].
- **Query Processing Pipeline** — Primary: [[06-Query-Processing-Pipeline]].

## R

- **Raft** — Primary: [[01-Consensus-Raft-Paxos]].
- **Read skew** — Primary: [[01-Concurrency-Anomalies]].
- **Read-your-writes consistency** — Primary: [[04-Eventual-Consistency]].
- **Recovery** — Primary: [[00-WAL-Logging]] through [[04-Banking-Recovery-Scenario]].
- **Recursive CTE** — Primary: [[04-Subqueries-CTEs]].
- **Redo log** — Primary: [[00-WAL-Logging]]. Applications: [[01-ARIES]].
- **Refactor** — Primary: [[05-Composition-Over-Inheritance]]. Applications: [[06-SOLID-in-Banking]].
- **Relation** — Primary: [[01-Relations-Tuples-Attributes]].
- **Relational algebra** — Primary: [[04-Relational-Algebra]]. Applications: [[00-SQL-From-Relational-Algebra]], [[06-Query-Processing-Pipeline]].
- **Relational calculus** — Primary: [[05-Relational-Calculus]].
- **Relational model** — Primary: [[00-Relational-Model]].
- **Replication** — Primary: [[02-Replication]]. Applications: [[03-Backup-And-Recovery]], [[05-Banking-Distributed-Design]].
- **Repository pattern** — Primary: [[05-Repository-Pattern]]. Applications: [[04-Enterprise-Patterns]], [[07-Banking-ORM-Mapping]].
- **Responsibility** — Primary: [[04-Responsibilities]]. Applications: [[02-CRC-Cards]].
- **RETURNING clause** — Primary: [[02-DML]].
- **Rollback** — Primary: [[06-Transactions-In-SQL]]. Applications: [[00-ACID]], [[01-ARIES]].
- **RPO / RTO** — Primary: [[03-Backup-And-Recovery]]. Applications: [[04-Banking-Recovery-Scenario]].

## S

- **Saga pattern** — Primary: [[07-Distributed-Transactions]]. Applications: [[05-Banking-Distributed-Design]].
- **SAVEPOINT** — Primary: [[06-Transactions-In-SQL]].
- **Schema** — Primary: [[00-Schema-Design]]. Applications: [[04-Banking-Schema]].
- **Search (full-text)** — mentioned in [[05-Banking-NoSQL-Choice]].
- **SELECT FOR UPDATE** — Primary: [[02-DML]]. Applications: [[09-Banking-Transaction-Walkthrough]].
- **Sequence diagram** — Primary: [[02-Sequence-Diagrams]].
- **Serializable** — Primary: [[05-Serializability]]. Applications: [[02-Isolation-Levels]].
- **Serializability** — Primary: [[05-Serializability]].
- **Service Layer** — Primary: [[04-Enterprise-Patterns]].
- **Sharding** — Primary: [[04-Partitioning-And-Sharding]]. Applications: [[03-Sharding-Revisited]], [[05-Banking-Distributed-Design]].
- **Singleton** — Primary: [[01-Creational-Patterns]]. Anti-pattern warning: [[05-Anti-Patterns]].
- **Slotted page** — Primary: [[01-Pages-And-Files]].
- **Snapshot isolation** — Primary: [[04-MVCC]]. Applications: [[02-Isolation-Levels]], [[05-Serializability]].
- **SOR (System of Record)** — Primary: [[00-Schema-Design]]. Applications: [[02-Denormalization-For-Reads]].
- **SP (Stored Procedure)** — Primary: [[08-Stored-Procedures]].
- **SRP** — Primary: [[01-SRP]].
- **SSI (Serializable Snapshot Isolation)** — Primary: [[05-Serializability]]. Applications: [[02-Isolation-Levels]].
- **State diagram** — Primary: [[04-State-Diagrams]].
- **State pattern** — Primary: [[03-Behavioral-Patterns]]. Applications: [[04-State-Diagrams]].
- **Statement (use case)** — Primary: [[02-Use-Cases]].
- **Statistics (optimizer)** — Primary: [[07-Cost-Based-Optimizer]]. Applications: [[08-Reading-EXPLAIN]].
- **Strategy pattern** — Primary: [[03-Behavioral-Patterns]]. Applications: [[02-OCP]], [[05-Composition-Over-Inheritance]].
- **Strong consistency** — Primary: [[00-CAP-PACELC]]. Applications: [[04-Eventual-Consistency]].
- **Superkey** — Primary: [[02-Keys-Superkeys-Candidate-Keys]].
- **Surrogate key** — Primary: [[02-Keys-Superkeys-Candidate-Keys]]. Applications: [[05-Identity-State-Lifecycle]].
- **Synchronous replication** — Primary: [[02-Replication]].

## T

- **Tell, Don't Ask** — Primary: [[04-Tell-Dont-Ask]].
- **Template Method** — Primary: [[03-Behavioral-Patterns]].
- **3NF** — Primary: [[06-1NF-2NF-3NF]].
- **Throughput vs latency** — Primary: [[08-Trade-offs-Everywhere]].
- **TOAST** — Primary: [[01-Pages-And-Files]].
- **Trade-off** — Primary: [[08-Trade-offs-Everywhere]]. Applications: every chapter.
- **Transaction** — Primary: [[00-ACID]]. Applications: [[06-Transactions-In-SQL]], [[09-Banking-Transaction-Walkthrough]].
- **Trigger** — Primary: [[03-Triggers-As-Constraints]]. Applications: [[04-Banking-Schema]].
- **Tuple** — Primary: [[01-Relations-Tuples-Attributes]].
- **2NF** — Primary: [[06-1NF-2NF-3NF]].
- **2PC (Two-Phase Commit)** — Primary: [[08-Two-Phase-Commit]]. Applications: [[07-Distributed-Transactions]].
- **2PL (Two-Phase Locking)** — Primary: [[03-Two-Phase-Locking]].

## U

- **Ubiquitous language** — Primary: [[00-Domain-Modeling]]. Applications: [[03-Domain-Concepts]].
- **Undo log** — Primary: [[00-WAL-Logging]]. Applications: [[01-ARIES]].
- **UNIQUE constraint** — Primary: [[02-Domain-Check-Constraints]].
- **Use case** — Primary: [[02-Use-Cases]].

## V

- **Value object** — Primary: [[01-Entities-Value-Objects]]. Applications: [[06-Banking-Domain-Model]].
- **View** — Primary: [[07-Views-Materialized-Views]].
- **Volcano model** — Primary: [[06-Query-Processing-Pipeline]].

## W

- **WAL (Write-Ahead Log)** — Primary: [[00-WAL-Logging]]. Applications: [[01-ARIES]], [[02-Checkpoints]].
- **Window function** — Primary: [[05-Window-Functions]]. Applications: [[09-Banking-SQL]].
- **Write skew** — Primary: [[01-Concurrency-Anomalies]]. Applications: [[05-Serializability]].

## X-Y-Z

- **XML** — not covered in depth.
- **XPath / XQuery** — out of scope.
- **Zero means null** — Primary: [[05-Anti-Patterns]].

## Cross-references

- [[Pattern-Index]] — patterns by category.
- [[Cross-Reference-Map]] — how the five forces map across layers.
- [[00-Map-of-Content]] — the master navigation.
