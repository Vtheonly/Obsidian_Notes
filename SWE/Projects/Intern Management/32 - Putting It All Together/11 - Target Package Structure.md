---
tags: [concept, rebuild, package-structure]
type: concept
status: complete
related:
  - [[]]
---

# Target Package Structure

```
com.example.internmanagement
├── InternManagementApp.java          // entry point (composition root)
├── config/
│   ├── AppConfig.java                // manual DI wiring
│   ├── DataSourceConfig.java         // HikariCP
│   ├── SecurityConfig.java           // Argon2 + RBAC
│   └── ObservabilityConfig.java      // Micrometer + Logback
├── domain/
│   ├── Intern.java                   // record
│   ├── WorkerUser.java
│   ├── Theme.java
│   ├── Department.java
│   ├── Role.java                     // enum
│   ├── DecisionStatus.java           // enum
│   └── criteria/
│       └── InternSearchCriteria.java
├── persistence/
│   ├── Repository.java               // interface
│   ├── AbstractJdbcRepository.java   // template
│   ├── InternRepository.java         // interface
│   ├── JdbcInternRepository.java     // impl
│   ├── WorkerUserRepository.java
│   ├── JdbcWorkerUserRepository.java
│   └── ... (one impl per entity)
├── service/
│   ├── AuthService.java
│   ├── InternService.java
│   ├── WorkerUserService.java
│   ├── DecisionService.java          // chief accept/reject
│   ├── EmailService.java
│   ├── ReportService.java
│   └── AuditService.java
├── security/
│   ├── PasswordEncoder.java          // interface
│   ├── Argon2PasswordEncoder.java
│   ├── Session.java
│   ├── SessionManager.java
│   ├── Permission.java               // enum
│   └── Authorizer.java
├── ui/
│   ├── NavigationController.java
│   ├── view/
│   │   ├── LoginView.java + .fxml
│   │   ├── ManageInternsView.java + .fxml
│   │   ├── ManageWorkersView.java + .fxml
│   │   ├── DecisionView.java + .fxml
│   │   └── ReportView.java + .fxml
│   ├── component/
│   │   ├── StatusView.java           // loading/empty/error
│   │   ├── ValidatedTextField.java
│   │   └── AuditLogView.java
│   └── theme/
│       ├── style.css
│       └── modena-dark.css
├── observability/
│   ├── MetricsRegistry.java
│   ├── HealthCheck.java
│   └── CorrelationId.java
├── resilience/
│   └── ResilienceConfig.java         // Resilience4j
├── cache/
│   └── LookupCache.java              // Caffeine
└── exception/
    ├── NotFoundException.java
    ├── AuthenticationException.java
    ├── AuthorizationException.java
    ├── ValidationException.java
    └── DataIntegrityException.java
```

~60 files vs the current 11. But each file is 80-150 LOC with one responsibility, vs the current 940-LOC God class.

## Why so many files

- **Single Responsibility** — each class does one thing.
- **Testability** — each class is independently testable.
- **Findability** — to find intern logic, look in `service/InternService.java`.
- **Extensibility** — add a new entity by adding files, not editing existing ones.

## Project Connection

This is the target. The current project has all logic in `oracleConnector.java` (940 LOC). The refactor splits it across ~60 small files.

## Further reading

- *Clean Architecture* (Martin), package structure.
