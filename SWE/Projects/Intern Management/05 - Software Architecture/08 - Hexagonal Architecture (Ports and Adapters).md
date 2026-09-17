---
tags: [concept, architecture, hexagonal, ports-adapters]
type: concept
status: complete
related:
  - [[05 - Software Architecture/02 - Clean Architecture (Uncle Bob)]]
  - [[05 - Software Architecture/04 - Dependency Injection]]
---

# Hexagonal Architecture (Ports and Adapters)

> "The application is at the center. The UI, database, and other external interfaces are all on the outside. They communicate with the application through ports, which are interfaces." — Alistair Cockburn, 2005

## What it is

Hexagonal Architecture (Cockburn, 2005) — also called Ports and Adapters — puts the **application core** at the center. The core defines **ports** (interfaces). External systems (UI, DB, email) connect via **adapters** that implement the ports.

```
                ┌─────────────┐
                │  Web UI     │  (driving adapter)
                └──────┬──────┘
                       │
                       ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Console   │──│ Application │──│   Oracle    │
│   (driver)  │  │    Core     │  │   (driven)  │
└─────────────┘  └─────────────┘  └─────────────┘
                       │
                       ▼
                ┌─────────────┐
                │  Email      │  (driven adapter)
                └─────────────┘
```

## Ports

A **port** is an interface defined by the application core. There are two kinds:

### Driving ports (primary)
Interfaces that the outside world calls *into* the application. E.g., `AcceptInternUseCase` — the UI calls this to accept an intern.

```java
public interface AcceptInternUseCase {
    void execute(long internId, long chiefUserId);
}
```

### Driven ports (secondary)
Interfaces that the application core calls *out to* the outside world. E.g., `InternRepository` — the application calls this to persist an intern.

```java
public interface InternRepository {
    void save(Intern intern);
    Optional<Intern> findById(long id);
}
```

## Adapters

An **adapter** is the implementation of a port for a specific technology.

### Driving adapters
- `RestAcceptInternController` (Spring MVC, calls `AcceptInternUseCase`).
- `JavaFxAcceptInternController` (JavaFX, calls `AcceptInternUseCase`).
- `CliAcceptInternCommand` (CLI, calls `AcceptInternUseCase`).

### Driven adapters
- `OracleInternRepository` (JDBC, implements `InternRepository`).
- `PostgresInternRepository` (JDBC, implements `InternRepository`).
- `InMemoryInternRepository` (for tests, implements `InternRepository`).

## Why it's powerful

- **Swap any external system without touching the core.** Replace Oracle with Postgres, replace JavaFX with a web UI, replace SMTP with a mail API — the core never changes.
- **Test the core in complete isolation.** Use `InMemoryInternRepository` and a fake `EmailSender` in tests.
- **The core has no framework dependencies.** No `@Entity`, no `@FXML`, no `@RestController`. Pure Java.

## Project Connection

The project's `oracleConnector` is a driving adapter (UI calls it) and a driven adapter (it calls the DB) all in one — and it has no port (interface). The fix: define `InternRepository` (port), implement `OracleInternRepository` (adapter), inject the port into the service (core).

## Common pitfalls

- **Putting the port in the wrong layer** — the port must live in the application core, not in the adapter.
- **Too many ports** — every use case becomes a port. Some ports can be grouped (e.g., `InternUseCases` with `accept`, `reject`, `search` methods).
- **Confusing ports with repositories** — repositories are driven ports, but not all ports are repositories. Email, SMS, file storage are also driven ports.

## Further reading

- Cockburn, "Hexagonal Architecture" (alistair.cockburn.us).
- *Get Your Hands Dirty on Clean Architecture* (Tom Hombergs).
