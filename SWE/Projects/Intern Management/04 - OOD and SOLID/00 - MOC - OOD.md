---
tags: [moc, ood, solid]
type: moc
status: complete
---

# MOC — Object-Oriented Design and SOLID

> Every architectural critique in the reviews is grounded in SOLID. Without
> SRP, OCP, DIP, "God Class" is just an insult, not a diagnosis.

## Notes (read in order)

### Foundations
1. [[04 - OOD and SOLID/24 - The Four Pillars of OOP]] — encapsulation, abstraction, inheritance, polymorphism.
2. [[04 - OOD and SOLID/08 - Encapsulation]] — information hiding, why `public` fields are bad.
3. [[04 - OOD and SOLID/05 - Composition over Inheritance]] — favor object composition over class inheritance.
4. [[04 - OOD and SOLID/17 - Programming to Interfaces]] — "program to an interface, not an implementation" (GoF).

### SOLID
5. [[04 - OOD and SOLID/19 - Single Responsibility Principle (SRP)]] — a class should have one reason to change.
6. [[04 - OOD and SOLID/15 - Open-Closed Principle (OCP)]] — open for extension, closed for modification.
7. [[04 - OOD and SOLID/14 - Liskov Substitution Principle (LSP)]] — subtypes must be substitutable for base types.
8. [[04 - OOD and SOLID/11 - Interface Segregation Principle (ISP)]] — no client should be forced to depend on methods it doesn't use.
9. [[04 - OOD and SOLID/07 - Dependency Inversion Principle (DIP)]] — depend on abstractions, not concretions.

### Other Principles
10. [[04 - OOD and SOLID/06 - DRY (Don't Repeat Yourself)]] — every piece of knowledge has a single, authoritative representation.
11. [[04 - OOD and SOLID/12 - KISS (Keep It Simple, Stupid)]] — simplicity is a virtue.
12. [[04 - OOD and SOLID/25 - YAGNI (You Aren't Gonna Need It)]] — don't build for speculative futures.
13. [[04 - OOD and SOLID/13 - Law of Demeter]] — don't talk to strangers; only talk to immediate friends.
14. [[04 - OOD and SOLID/23 - Tell-Dont-Ask]] — tell objects what to do, don't ask them for data.
15. [[04 - OOD and SOLID/04 - Composition Root]] — where you wire up dependencies.

### Anti-Patterns
16. [[04 - OOD and SOLID/01 - Anemic Domain Model]] — domain objects with no behavior.
17. [[04 - OOD and SOLID/21 - Static Utility Anti-Pattern]] — `static` mutable state is a code smell.
18. [[04 - OOD and SOLID/10 - God Class (God Object)]] — a class that knows too much.
19. [[04 - OOD and SOLID/20 - Smart UI Anti-Pattern]] — UI classes doing business logic and data access.
20. [[04 - OOD and SOLID/09 - Feature Envy]] — a method more interested in another class than its own.
21. [[04 - OOD and SOLID/16 - Primitive Obsession]] — using primitives instead of small objects.
22. [[04 - OOD and SOLID/18 - Replace Magic Strings with Enums]] — type-safe constants.

### Code Quality
23. [[04 - OOD and SOLID/02 - Clean Code Principles]] — meaningful names, small functions, single level of abstraction.
24. [[04 - OOD and SOLID/03 - Code Smells Catalog]] — the full catalog (Fowler).
25. [[04 - OOD and SOLID/22 - Technical Debt]] — what it is, how to measure, how to pay down.
