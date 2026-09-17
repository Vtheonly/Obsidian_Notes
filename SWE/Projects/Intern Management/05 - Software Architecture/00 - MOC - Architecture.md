---
tags: [moc, architecture]
type: moc
status: complete
---

# MOC — Software Architecture

> The #1 critical issue in the project is "no architecture." Layered, Repository,
> DI, and the Smart UI anti-pattern all live here.

## Notes (read in order)

### Foundations
1. [[05 - Software Architecture/15 - Separation of Concerns]] — the foundational principle.
2. [[05 - Software Architecture/10 - Layered Architecture]] — presentation / service / data.
3. [[05 - Software Architecture/02 - Clean Architecture (Uncle Bob)]] — the dependency rule.
4. [[05 - Software Architecture/08 - Hexagonal Architecture (Ports and Adapters)]] — Cockburn.
5. [[05 - Software Architecture/12 - Onion Architecture]] — Jeffrey Palermo.
6. [[05 - Software Architecture/05 - Domain-Driven Design]] — Evans, bounded contexts.
7. [[05 - Software Architecture/11 - MVC MVP MVVM]] — UI architectural patterns.

### Patterns
8. [[05 - Software Architecture/14 - Repository Pattern]] — Fowler P of EAA.
9. [[05 - Software Architecture/18 - Unit of Work Pattern]] — transactional consistency.
10. [[05 - Software Architecture/16 - Service Layer Pattern]] — use-case orchestration.
11. [[05 - Software Architecture/07 - Facade Pattern]] — simplified API.
12. [[05 - Software Architecture/04 - Dependency Injection]] — constructor, setter, field, container.
13. [[05 - Software Architecture/09 - Inversion of Control]] — the broader principle.

### Anti-Patterns
14. [[05 - Software Architecture/17 - Smart UI Anti-Pattern]] — UI classes doing business logic.
15. [[05 - Software Architecture/01 - Big Ball of Mud]] — no architecture at all.

### Cross-Cutting
16. [[05 - Software Architecture/06 - Exception Translation]] — turning SQLException into NotFoundException.
17. [[05 - Software Architecture/03 - Cross-Cutting Concerns]] — logging, security, transactions.
18. [[05 - Software Architecture/13 - Package by Feature vs Package by Layer]] — how to organize code.
