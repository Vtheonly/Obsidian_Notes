---
tags: [concept, rebuild, from-scratch]
type: concept
status: complete
---

# How to Rebuild From Scratch

> If you started over (no legacy code), how would you build it?

## 1. Set up the project

```bash
mkdir intern-management && cd intern-management
git init
mvn archetype:generate -DgroupId=com.example -DartifactId=intern-management -DarchetypeArtifactId=maven-archetype-quickstart
```

Add to `pom.xml`:
- Java 21 LTS.
- JavaFX 21.0.4 (controls, fxml, graphics).
- HikariCP 5.1.0.
- ojdbc11 23.5.
- jbcrypt 0.4 (or argon2-jvm 2.11).
- SLF4J 2.0.9 + Logback 1.4.11.
- Flyway 9.22.
- JUnit 5.10 + Mockito 5.5 + Testcontainers 1.19 + TestFX 4.0.17.
- Maven plugins: javafx-maven-plugin, jacoco, spotbugs, checkstyle, pmd, owasp dependency-check.

## 2. Set up the package structure

See [[32 - Putting It All Together/11 - Target Package Structure]].

## 3. Set up the database

`docker-compose.yml` with `gvenzl/oracle-xe:21-slim`, secrets, healthcheck.

Flyway migrations in `src/main/resources/db/migration/`:
- `V1__create_baseline.sql` — tables, constraints, indexes.
- `V2__add_audit_columns.sql`.
- `V3__add_audit_logs_table.sql`.

## 4. Build the domain model

Records for `Intern`, `WorkerUser`, `Theme`, `Department`. Enums for `Role`, `DecisionStatus`, `Permission`.

## 5. Build the repository layer

`Repository<T, ID>` interface. `AbstractJdbcRepository<T, ID>` template. Per-entity repositories.

## 6. Build the service layer

`AuthService`, `InternService`, `WorkerUserService`, `ChiefDecisionService`. Constructor-injected repositories. `@Transactional` (or manual transaction management).

## 7. Build the UI

FXML views + controllers. `BorderPane` main layout. `TableView` for data. `StatusView` for loading/empty/error. `NavigationController` for single-Stage navigation.

## 8. Add security

`Argon2PasswordEncoder`. `SessionManager`. `Authorizer` with `Permission` checks. `Bucket4j` rate limiting on login.

## 9. Add observability

SLF4J + Logback (JSON, rolling). Micrometer + Prometheus. `AuditService`. Health check endpoint.

## 10. Add resilience

HikariCP with proper config. Resilience4j (retry, circuit breaker, bulkhead). Timeouts on every call.

## 11. Add tests

- Unit tests (70%) — services with mocked repositories.
- Integration tests (20%) — repositories with Testcontainers.
- UI tests (10%) — TestFX for critical flows.

## 12. Add CI/CD

GitHub Actions: build + test + Sonar + dependency-check + jpackage on tag.

## 13. Add Docker

Multi-stage Dockerfile. Extended `docker-compose.yml` with app + oracle + prometheus + grafana.

## 14. Write the README

One-paragraph pitch. Architecture diagram. Prerequisites. Quickstart. Screenshots. License.

## The result

A production-grade JavaFX + Oracle app, built from scratch, using modern best practices. ~60 files, ~3000 LOC. Demonstrably senior-level.

## Why this is faster than refactoring

- No legacy code to understand.
- No characterization tests to write.
- No conflicts between old and new design.
- Clean slate, no compromises.

But: you lose the learning experience of refactoring. Refactoring teaches you *why* the old design was bad, which is the point of this vault.

## Recommendation

Do both:
1. **Refactor** the existing project (Phases 0-4) — learn the "why."
2. **Rebuild** from scratch — apply the "why" cleanly.

The rebuild is faster (no legacy) and produces a cleaner result. The refactor is slower but more educational.

## Further reading

- Every chapter in this vault.
