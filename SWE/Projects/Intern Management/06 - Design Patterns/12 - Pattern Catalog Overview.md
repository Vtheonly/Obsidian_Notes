---
tags: [concept, design-patterns, catalog]
type: concept
status: complete
related:
  - [[06 - Design Patterns/19 - What Are Design Patterns]]
---

# Pattern Catalog Overview

## The 23 GoF patterns

### Creational (5)
| Pattern | What it does | Project relevance |
|---|---|---|
| **Abstract Factory** | Create families of related objects | Low (could be used for theming) |
| **Builder** | Construct complex objects step by step | High (`InternSearchQuery` builder) |
| **Factory Method** | Define an interface for creation, defer to subclasses | High (`ConnectionFactory`, `AlertFactory`) |
| **Prototype** | Clone existing objects | Low |
| **Singleton** | One instance per class | High (justified: `DataSource`; misused: `oracleConnector`) |

### Structural (7)
| Pattern | What it does | Project relevance |
|---|---|---|
| **Adapter** | Convert one interface to another | High (`MailSender`, `PDFRenderer`) |
| **Bridge** | Decouple abstraction from implementation | Low |
| **Composite** | Treat individual and composite uniformly | Medium (JavaFX scene graph) |
| **Decorator** | Add behavior without subclassing | High (`CachingRepository`, `LoggingDataSource`) |
| **Facade** | Simplify a complex subsystem | High (service layer) |
| **Flyweight** | Share fine-grained objects | Medium (TableView cell recycling) |
| **Proxy** | Placeholder for another object | Medium (lazy loading, access control) |

### Behavioral (11)
| Pattern | What it does | Project relevance |
|---|---|---|
| **Chain of Responsibility** | Pass request along a chain | High (validation chain) |
| **Command** | Encapsulate a request as an object | High (undoable operations, batch accept/reject) |
| **Interpreter** | Define a grammar and interpret | Low |
| **Iterator** | Sequential access to a collection | Medium (Java `Iterator`, enhanced for) |
| **Mediator** | Centralize communication between objects | High (`NavigationController`) |
| **Memento** | Capture and restore state | Low (could be used for undo) |
| **Observer** | Notify dependents of state changes | High (JavaFX properties, event bus) |
| **State** | Behavior changes with state | High (`DecisionStatus`, `ConnectionState`) |
| **Strategy** | Interchangeable algorithms | High (`PasswordEncoder`, `ReportExporter`) |
| **Template Method** | Algorithm skeleton, defer steps to subclasses | High (`AbstractJdbcRepository`) |
| **Visitor** | Separate operations from object structure | Low |

## Enterprise patterns (Fowler, P of EAA)

- **Repository** — collection-like interface for persistence.
- **Unit of Work** — transactional tracking.
- **Service Layer** — use-case orchestration.
- **Specification** — composable query criteria.
- **Plugin** — runtime-discovered extensions (Java SPI).

## Which patterns the project should adopt

Per the reviews:
- **Repository** (Fowler) — replace `oracleConnector` static methods.
- **Strategy** — `PasswordEncoder` (Argon2id/BCrypt), `ReportExporter` (PDF/CSV/XLSX).
- **Factory** — `ConnectionFactory` (HikariCP-backed), `AlertFactory`.
- **Builder** — `InternSearchQuery`, `ReportDocument`.
- **Observer** — selection events on TableView, EventBus.
- **Command** — undoable operations (delete intern → reversible).
- **State** — `DecisionStatus` (currently a string literal).
- **Decorator** — `CachingRepository` wraps `JdbcRepository`; `LoggingDataSource` wraps `DataSource`.
- **Adapter** — `MailSender` (javax.mail → jakarta.mail migration); `PDFRenderer` (OpenPDF / Flying Saucer).
- **Facade** — `InternManagementFacade`.
- **Template Method** — `AbstractJdbcRepository` implements save/findById/delete; subclasses provide RowMapper + table metadata.
- **Singleton** (justified) — `DataSource`, `ObjectMapper`, `Configuration`. Scoped to a DI container, not as static utility.
- **Chain of Responsibility** — validation chain.
- **Mediator** — `NavigationController`.

## Further reading

- *Design Patterns* (GoF).
- *Patterns of Enterprise Application Architecture* (Fowler).
