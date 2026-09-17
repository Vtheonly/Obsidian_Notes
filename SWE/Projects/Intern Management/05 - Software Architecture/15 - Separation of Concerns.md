---
tags: [concept, architecture, soc]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/19 - Single Responsibility Principle (SRP)]]
  - [[05 - Software Architecture/10 - Layered Architecture]]
---

# Separation of Concerns (SoC)

> "Parsifal: So, in a way, you're saying that computer science is the study of how to keep different ideas separate." — Edsger Dijkstra, 1974

## What it is

Separation of Concerns is the principle that a system should be divided into distinct sections, each addressing a separate concern. A **concern** is anything that matters to the system — data persistence, user interaction, authentication, logging, validation, etc.

## The canonical layers

1. **Presentation** — UI rendering, event handling, user input.
2. **Business logic** — domain rules, use-case orchestration.
3. **Data access** — SQL, persistence.

Each layer depends only on the layer below (or, in Clean Architecture, on abstractions in the same layer).

## The project's violation

```java
// insertionInternController.java
public void insertInternController() {
    // Presentation: read UI fields
    String name = insert_intern_Name.getText();
    // Validation: parse age (badly)
    int age = Integer.parseInt(insert_intern_Age.getText());
    // Business logic: generate ID (race condition)
    int newId = oracleConnector.getMaxId("intern", "intern_id") + 1;
    // Data construction: build a Map
    HashMap<String, Object> internData = new HashMap<>();
    // ...
    // Data access: insert
    oracleConnector.insertIntern(internData);
    // Presentation: show dialog
    JOptionPane.showMessageDialog(null, "Intern inserted successfully");
}
```

Six concerns in one method: presentation, validation, business logic, data construction, data access, UI feedback.

## Why it matters

- **Reuse** — business logic should be reusable across UIs (desktop, web, CLI). With SoC, you can.
- **Testability** — test the business logic without launching JavaFX or hitting Oracle.
- **Maintainability** — a schema change touches only the data access layer.
- **Teamwork** — UI designers work on presentation; DBAs work on data access. They don't conflict.

## The fix: layered architecture

```
[Controller]     → [Service]    → [Repository]   → [DB]
  Presentation       Business       Data Access
```

- Controller: reads UI fields, calls service, shows alert.
- Service: validates, orchestrates, calls repository.
- Repository: executes SQL, maps rows to objects.

No SQL in the controller. No `JOptionPane` in the repository. No business rules in either.

See [[05 - Software Architecture/10 - Layered Architecture]].

## Common pitfalls

- **"It's just a small app"** — SoC is more important in small apps because they grow.
- **Anemic service layer** — a service that just delegates to the repository adds a layer with no value. Either put real logic in the service, or skip it.
- **Cross-cutting concerns everywhere** — logging, security, transactions are cross-cutting. Use AOP or decorators, not sprinkled calls.

## Project Connection

The project has zero SoC. The fix is the layered architecture introduced in Phase 2 of the refactoring roadmap.

## Further reading

- Dijkstra, "On the role of scientific thought" (1974).
- *Clean Architecture* (Martin), Chapter 2.
