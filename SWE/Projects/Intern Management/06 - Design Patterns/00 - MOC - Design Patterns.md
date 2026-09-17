---
tags: [moc, design-patterns, gof]
type: moc
status: complete
---

# MOC — Design Patterns

> The review identifies 13+ patterns that should be applied. Learn what they are,
> when to use them, and when they're overkill.

## Notes (read in order)

### Foundations
1. [[06 - Design Patterns/19 - What Are Design Patterns]] — GoF, the catalog, why patterns exist.
2. [[06 - Design Patterns/12 - Pattern Catalog Overview]] — all 23 GoF patterns at a glance.

### Creational
3. [[06 - Design Patterns/08 - Factory Pattern]] — `ConnectionFactory`, `AlertFactory`.
4. [[06 - Design Patterns/01 - Abstract Factory Pattern]] — families of related objects.
5. [[06 - Design Patterns/03 - Builder Pattern]] — `InternSearchQuery`, `ReportDocument`.
6. [[06 - Design Patterns/14 - Singleton Pattern]] — `DataSource`, `ObjectMapper` (justified vs misused).

### Structural
7. [[06 - Design Patterns/02 - Adapter Pattern]] — `MailSender`, `PDFRenderer`, `ExceptionTranslator`.
8. [[05 - Software Architecture/07 - Facade Pattern]] — see [[05 - Software Architecture/07 - Facade Pattern]].
9. [[06 - Design Patterns/07 - Decorator Pattern]] — `CachingRepository`, `LoggingDataSource`.
10. [[06 - Design Patterns/06 - Composite Pattern]] — JavaFX scene graph.

### Behavioral
11. [[06 - Design Patterns/17 - Strategy Pattern]] — `PasswordEncoder`, `ReportExporter`.
12. [[06 - Design Patterns/18 - Template Method Pattern]] — `AbstractJdbcRepository`.
13. [[06 - Design Patterns/11 - Observer Pattern]] — JavaFX properties, event bus.
14. [[06 - Design Patterns/05 - Command Pattern]] — undoable operations.
15. [[06 - Design Patterns/16 - State Pattern]] — `DecisionStatus`, `ConnectionState`.
16. [[06 - Design Patterns/04 - Chain of Responsibility Pattern]] — validation chain.
17. [[06 - Design Patterns/09 - Iterator Pattern]] — `Iterator`, enhanced for-loop.
18. [[06 - Design Patterns/10 - Mediator Pattern]] — `NavigationController`.

### Enterprise
19. [[05 - Software Architecture/14 - Repository Pattern]] — see [[05 - Software Architecture/14 - Repository Pattern]].
20. [[05 - Software Architecture/18 - Unit of Work Pattern]] — see [[05 - Software Architecture/18 - Unit of Work Pattern]].
21. [[06 - Design Patterns/15 - Specification Pattern]] — composable query criteria.
22. [[06 - Design Patterns/13 - Plugin Pattern]] — Java SPI `ServiceLoader`.
