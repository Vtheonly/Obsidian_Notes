---
tags: [concept, rebuild, phase-2]
type: concept
status: complete
related:
  - [[]]
---

# Phase 2 — Architectural Refactor (24-36 hours)

> Goal: introduce layered architecture, DI, repository pattern, domain model. The big one.

## Tasks

### 1. Define domain records
```java
public record Intern(Long internId, String name, Integer age, String email, ...) {}
public record WorkerUser(...) {}
public record Theme(...) {}
public record Department(...) {}
public enum Role { USER, SECRETARY, ADMIN, CHIEF; }
public enum DecisionStatus { PENDING, ACCEPTED, REJECTED; }
public record InternSearchCriteria(String name, Long themeId, DecisionStatus status) {}
```

### 2. Define interfaces
```java
public interface Repository<T, ID> { ... }
public interface InternRepository extends Repository<Intern, Long> { ... }
public interface AuthService { ... }
public interface PasswordEncoder { ... }
public interface EmailService { ... }
public interface ReportService { ... }
```

### 3. Implement AbstractJdbcRepository<T, ID>
Template method pattern. Shared `save`, `findById`, `findAll`, `delete`. Subclasses provide `tableName()`, `idColumn()`, `mapRow()`, `setInsertParams()`.

### 4. Implement per-entity repositories
`OracleInternRepository`, `OracleWorkerUserRepository`, `OracleThemeRepository`, `OracleDepartmentRepository`. Each ~80 LOC.

### 5. Introduce HikariCP DataSource
Remove the static `Connection`. Each repository borrows a connection per operation via try-with-resources.

### 6. Introduce service layer
`AuthService`, `InternService`, `WorkerUserService`, `ChiefDecisionService`. Services hold repositories; controllers hold services.

### 7. Replace Swing `JOptionPane` with typed exceptions + JavaFX `Alert`
- DAO throws `SQLException` → repository translates to `DuplicateEmailException`, `NotFoundException`, etc.
- Controller catches and shows JavaFX `Alert`.

### 8. Replace `toolkit.hashIt` with `Argon2PasswordEncoder`
Generate per-password salt. Store in `salt` column.

### 9. Move credentials to env vars
`DB_URL`, `DB_USER`, `DB_PASSWORD`. Read via `System.getenv()`. Fail fast with a clear error if missing.

### 10. Replace `getMaxId+1` with Oracle IDENTITY columns
Migration: `ALTER TABLE intern MODIFY (intern_id GENERATED ALWAYS AS IDENTITY)`.

### 11. Replace static `labelText` with explicit controller injection
```java
FXMLLoader loader = new FXMLLoader(...);
Parent root = loader.load();
UpdateInternController ctrl = loader.getController();
ctrl.setIntern(selectedIntern);
stage.show();
```

### 12. Introduce NavigationController
Single-Stage scene swap. Replace `new Stage()` per view.

## After Phase 2

The project is architecturally sound:
- Layered (UI → Service → Repository → DB).
- DI (constructor injection).
- Typed domain model (no more `Map<String, Object>`).
- Testable (mock repositories in service tests).
- No static mutable state.
- No Swing in the data layer.

Still missing: UI polish (Phase 3), observability/resilience (Phase 4).

## Further reading

- [[05 - Software Architecture/00 - MOC - Architecture]].
- [[13 - JDBC and Data Access/00 - MOC - JDBC]].
