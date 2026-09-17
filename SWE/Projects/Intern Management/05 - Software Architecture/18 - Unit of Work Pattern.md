---
tags: [concept, pattern, unit-of-work]
type: concept
status: complete
related:
  - [[05 - Software Architecture/14 - Repository Pattern]]
  - [[10 - Transactions and Concurrency/01 - ACID Properties]]
---

# Unit of Work Pattern

> "Maintains a list of objects affected by a business transaction and coordinates the writing out of changes and the resolution of concurrency problems." — Martin Fowler, P of EAA

## What it is

A **Unit of Work** tracks all changes made to objects during a business transaction. When the transaction commits, the Unit of Work writes all changes to the database in one atomic operation.

```java
UnitOfWork uow = unitOfWorkFactory.create();
Intern intern = uow.interns().findById(123);
intern.accept(chief);
User user = uow.users().findById(chiefId);
user.incrementAcceptCount();
uow.commit();  // writes both changes atomically
```

## Why it exists

- **Atomicity** — multiple changes commit or roll back together.
- **Consistency** — the in-memory state matches the DB state after commit.
- **Efficiency** — batch writes, avoid redundant queries.
- **Concurrency** — the Unit of Work can detect and resolve conflicts (optimistic locking).

## How it works

1. **Begin** — start a transaction, create a Unit of Work.
2. **Track** — every loaded object is tracked. Every modification is recorded.
3. **Commit** — write all changes (inserts, updates, deletes) to the DB in order.
4. **Rollback** — discard all changes, close the transaction.

## JPA EntityManager is a Unit of Work

```java
@Transactional
public void acceptIntern(long internId, long chiefId) {
    Intern intern = entityManager.find(Intern.class, internId);  // tracked
    User chief = entityManager.find(User.class, chiefId);        // tracked
    intern.accept(chief);  // modifies intern
    chief.incrementAcceptCount();  // modifies chief
    // no explicit save — EntityManager tracks changes and writes them at commit
}
```

The `@Transactional` annotation starts a Unit of Work. `entityManager.find` loads objects into the UoW. Modifications to those objects are tracked. At method exit, the UoW commits — both changes are written atomically.

## Spring @Transactional

Spring's `@Transactional` is built on the Unit of Work concept:
- Method entry: start a transaction (and a Hibernate session, which is a UoW).
- Method body: load and modify entities.
- Method exit: commit the transaction (write all changes).
- Exception: rollback the transaction (discard all changes).

## Project Connection

The project has no Unit of Work. Every `oracleConnector` method is an independent operation in auto-commit mode. If `insertIntern` succeeds but `insertInternAssignment` fails, the intern is inserted but the assignment is not — inconsistent state.

The fix: use explicit transactions (`conn.setAutoCommit(false); ...; conn.commit();`) or Spring `@Transactional`. See [[10 - Transactions and Concurrency/01 - ACID Properties]].

## Common pitfalls

- **Long-running UoWs** — holding a transaction open for a long time locks rows. Keep UoWs short.
- **Modifying objects outside the UoW** — changes are lost. Always load within the UoW.
- **Multiple UoWs for one transaction** — splits atomicity. Use one UoW per transaction.

## Further reading

- *Patterns of Enterprise Application Architecture* (Fowler), Unit of Work pattern.
