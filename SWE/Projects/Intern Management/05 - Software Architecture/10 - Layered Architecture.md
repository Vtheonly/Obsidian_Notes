---
tags: [concept, architecture, layered]
type: concept
status: complete
related:
  - [[05 - Software Architecture/15 - Separation of Concerns]]
  - [[05 - Software Architecture/02 - Clean Architecture (Uncle Bob)]]
  - [[05 - Software Architecture/17 - Smart UI Anti-Pattern]]
---

# Layered Architecture

## What it is

A **layered architecture** organizes a system into horizontal layers, each with a specific responsibility. Each layer depends only on the layer directly below it.

```
┌─────────────────────────────────┐
│   Presentation Layer            │  Controllers, FXML, UI
├─────────────────────────────────┤
│   Service / Business Layer      │  Business rules, use cases
├─────────────────────────────────┤
│   Data Access Layer             │  Repositories, DAOs
├─────────────────────────────────┤
│   Database                      │  Oracle
└─────────────────────────────────┘
```

The dependency direction is **downward**: presentation depends on service, service depends on data access, data access depends on the DB driver. The DB knows about nothing above it.

## The layers in detail

### Presentation
- Renders the UI (JavaFX FXML, controllers).
- Handles user input (button clicks, form submission).
- Calls the service layer.
- Catches exceptions and shows user-friendly messages.
- **Does NOT** contain business rules, SQL, or direct DB access.

### Service (Business)
- Implements use cases ("create intern", "accept intern", "search interns").
- Validates input (calling domain objects or validators).
- Orchestrates multiple repositories if needed.
- Manages transactions (`@Transactional`).
- **Does NOT** know about FXML, Alert, or JOptionPane.

### Data Access (Repository)
- Executes SQL via JDBC, JPA, or another ORM.
- Maps rows to domain objects (RowMapper).
- **Does NOT** know about UI or business rules.

## Why it matters

- **Reuse** — business logic can be exposed via REST API, CLI, or batch job without rewriting.
- **Testability** — test the service layer with mocked repositories (no DB needed).
- **Maintainability** — a schema change touches only the repository layer.
- **Clarity** — new developers can find where things are.

## The project's (lack of) layers

The project has no layers. `oracleConnector` is presentation + business + data access all in one. Controllers call `oracleConnector` directly, bypassing any service layer.

## The fix

```
[ LoginController ]        [ InternSearchController ]    [ ChiefDecisionController ]
       │                              │                              │
       ▼                              ▼                              ▼
[ AuthService ]            [ InternService ]              [ ChiefDecisionService ]
       │                              │                              │
       ▼                              ▼                              ▼
[ WorkerUserRepository ]  [ InternRepository ]           [ InternRepository ]
       │                              │                              │
       ▼                              ▼                              ▼
[ HikariDataSource ]      [ HikariDataSource ]           [ HikariDataSource ]
       │                              │                              │
       ▼                              ▼                              ▼
[ Oracle XE ]              [ Oracle XE ]                  [ Oracle XE ]
```

## Variations

- **3-layer** (presentation / business / data) — the classic.
- **4-layer** (add a "domain" layer for rich domain objects, separate from services) — DDD style.
- **5-layer** (add "infrastructure" for cross-cutting concerns) — enterprise style.

## Common pitfalls

- **"Lateral" calls** — `InternService` calling `WorkerUserService` directly. Use a higher-level orchestration service, or events.
- **"Upward" dependencies** — repository knowing about service. Violates the dependency rule.
- **Anemic layers** — a service that just delegates to the repository. Either add logic or remove the layer.
- **Layer leakage** — `SQLException` thrown from the repository, caught in the controller. Translate to a domain exception at the service boundary. See [[05 - Software Architecture/06 - Exception Translation]].

## Project Connection

The project has no layers. The refactoring roadmap (Phase 2) introduces them.

## Further reading

- *Patterns of Enterprise Application Architecture* (Fowler), Layered Architecture.
- *Clean Architecture* (Martin).
