---
tags: [concept, pattern, service-layer]
type: concept
status: complete
related:
  - [[05 - Software Architecture/10 - Layered Architecture]]
  - [[05 - Software Architecture/14 - Repository Pattern]]
---

# Service Layer Pattern

> "Defines an application's boundary with a layer of services that establishes a set of available operations and coordinates the application's response in each operation." — Martin Fowler, P of EAA

## What it is

A **service layer** is a set of operations (use cases) that the UI (or API, or CLI) can call. Each operation:
1. Validates input.
2. Loads domain objects.
3. Performs the business logic.
4. Persists changes.
5. Returns the result.

```java
public class InternService {
    private final InternRepository repository;
    private final AuditService auditService;

    public InternService(InternRepository repository, AuditService auditService) { ... }

    @Transactional
    public Intern createIntern(CreateInternCommand cmd) {
        // Validate
        if (cmd.email() == null || cmd.email().isBlank()) {
            throw new ValidationException("Email is required");
        }
        // Check uniqueness
        if (repository.existsByEmail(cmd.email())) {
            throw new DuplicateEmailException(cmd.email());
        }
        // Create
        Intern intern = new Intern(cmd.name(), cmd.age(), cmd.email(), ...);
        // Persist
        repository.save(intern);
        // Audit
        auditService.log("CREATE", "intern", intern.getId());
        return intern;
    }

    @Transactional
    public void acceptIntern(long internId, long chiefId) { ... }

    @Transactional(readOnly = true)
    public List<Intern> searchInterns(InternSearchCriteria criteria) { ... }
}
```

## Why it exists

- **Single entry point** — the UI doesn't call repositories directly. It calls service methods.
- **Business logic centralization** — rules live in the service, not scattered across controllers.
- **Transaction boundaries** — `@Transactional` marks the unit of work.
- **Reusability** — the same service can be called from a desktop UI, a REST API, a CLI, a batch job.

## Service types

### Application Service
Orchestrates use cases. Calls repositories, domain services, other application services. No business rules of its own — just coordination.

### Domain Service
Holds business rules that don't fit on a single entity. Stateless. Pure domain.

The distinction matters in DDD. For simpler apps, one "service" class per entity is fine.

## What belongs in a service

- Use case orchestration (load, validate, modify, persist).
- Transaction boundaries.
- Cross-cutting concerns (audit, logging, security).
- **Coordination** between multiple repositories.

## What does NOT belong in a service

- UI logic (JavaFX, FXML, alerts).
- SQL (belongs in the repository).
- Domain rules that fit on an entity (belongs on the entity).

## The project's (lack of) service layer

Controllers call `oracleConnector` directly. No validation (except the broken `value == ""` check). No transactions. No audit. No reusability — the logic is locked inside JavaFX controllers.

## The fix

```java
public class InternService {
    private final InternRepository repository;
    private final AuditService auditService;

    public InternService(InternRepository repository, AuditService auditService) { ... }

    public Intern createIntern(CreateInternCommand cmd) { ... }
    public void acceptIntern(long internId, long chiefId) { ... }
    public List<Intern> searchInterns(InternSearchCriteria criteria) { ... }
}

public class InternSearchController {
    private final InternService internService;

    public InternSearchController(InternService internService) { ... }

    public void handleSearch() {
        // 1. Read UI
        String name = nameField.getText();
        // 2. Call service
        List<Intern> results = internService.searchInterns(new InternSearchCriteria(name));
        // 3. Update UI
        tableView.getItems().setAll(results);
    }
}
```

## Common pitfalls

- **Anemic service** — a service that just delegates to the repository with no logic. Either add logic or remove the layer.
- **Fat service** — a service with 50 methods. Split by use case.
- **Service depending on UI** — `InternService` should not import `javafx.*`.
- **Business rules in the controller** — move them to the service or domain.

## Further reading

- *Patterns of Enterprise Application Architecture* (Fowler), Service Layer pattern.
