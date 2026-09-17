---
tags: [concept, rebuild, architecture]
type: concept
status: complete
related:
  - [[]]
---

# Target Architecture

## The end state

After the refactor, the project looks like this:

```
+--------------------------------------------------------------+
|                       JavaFX UI Layer                        |
|  LoginView  ManageView  SearchView  InsertView  ReportView   |
|  (FXML + Controllers, no business logic, no JDBC)            |
+-----------------------+--------------------------------------+
                        |  via NavigationController + DI
                        v
+--------------------------------------------------------------+
|                       Service Layer                          |
|  AuthService  InternService  WorkerService  DecisionService  |
|  (business rules, @Transactional, orchestration)             |
+-----------------------+--------------------------------------+
                        |  via Repository
                        v
+--------------------------------------------------------------+
|                     Repository Layer                         |
|  InternRepo  WorkerRepo  ThemeRepo  DeptRepo  (interfaces)   |
|  AbstractJdbcRepository (template)                           |
+-----------------------+--------------------------------------+
                        |  via DataSource (HikariCP)
                        v
+--------------------------------------------------------------+
|                          Oracle XE                           |
+--------------------------------------------------------------+

Cross-cutting (horizontal):
  + Security: Argon2id + Session + RBAC + RateLimiter
  + Observability: SLF4J/Logback + Micrometer + AuditLog
  + Resilience: Resilience4j (retry / circuit breaker / bulkhead)
  + Caching: Caffeine (lookup tables)
  + Validation: Bean Validation (JSR-380)
  + Migration: Flyway (src/main/resources/db/migration/)

Configuration:
  + application.yml per profile (dev / test / prod)
  + secrets in env vars / Docker secrets / Vault
```

## The dependency rule

Dependencies point inward:
- UI → Service → Repository → DataSource → Oracle.
- Oracle knows about nothing above it.
- Repository knows nothing about UI.
- Service knows nothing about FXML.

Every seam is an interface. Every cross-cutting concern is a decorator.

## Why this architecture

- **Testable** — mock the repository to test the service in isolation.
- **Portable** — swap Oracle for PostgreSQL by writing a new repository.
- **Reusable** — the service layer can be exposed via REST API, CLI, batch job.
- **Maintainable** — a schema change touches only the repository layer.
- **Extensible** — add a new entity by writing one repository + one service.

## Project Connection

This is the target. The refactoring roadmap (Phases 0-4) gets you there incrementally.

## Further reading

- *Clean Architecture* (Martin).
