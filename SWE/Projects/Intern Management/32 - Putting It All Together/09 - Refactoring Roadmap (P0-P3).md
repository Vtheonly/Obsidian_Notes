---
tags: [concept, rebuild, roadmap]
type: concept
status: complete
---

# Refactoring Roadmap (P0 → P3)

## Priority levels

| Priority | Items | Impact |
|---|---|---|
| **P0 — must-do** (20-30 hrs) | Hygiene + critical security | Defensible on résumé |
| **P1 — should-do** (30-40 hrs) | Architecture + testing | Genuinely impressive |
| **P2 — nice-to-have** (20-30 hrs) | Observability + resilience | Production-grade |
| **P3 — stretch** (20+ hrs) | REST API, Lucene, multi-tenant | Stand out |

Total: 80-120 hours.

## P0 (must-do)

1. Purge JavaFX SDK from git history.
2. Fix package/module typo.
3. Delete hardcoded `system/rootroot`; create least-privilege user.
4. Replace SHA-256 with Argon2id + per-password salt.
5. Replace static Connection with HikariCP pool.
6. Remove all `JOptionPane` from DAO; throw typed exceptions.
7. Fix the two real bugs (`==`, `HashMap` iteration order).
8. Bump Java 20→21 LTS, JavaFX 21.0.4, ojdbc11 23.x.
9. Write README + LICENSE.

## P1 (should-do)

1. Introduce Repository + AbstractJdbcRepository.
2. Introduce domain records.
3. Introduce service layer.
4. Replace TitledPane list with TableView.
5. Add StatusView (loading/empty/error).
6. Move DB calls off FX thread (Task + ExecutorService).
7. Add Flyway migrations; consolidate SQL files.
8. Add JUnit 5 + Mockito + Testcontainers + TestFX.
9. Add CI (GitHub Actions) + SpotBugs + Checkstyle + JaCoCo.
10. Replace HTMLWorker with OpenHTMLtoPDF.

## P2 (nice-to-have)

1. SLF4J + Logback JSON logging.
2. Micrometer + Prometheus metrics.
3. Audit log table + service.
4. Resilience4j (retry / circuit breaker).
5. Caffeine cache for lookup tables.
6. Rate limiting on login (Bucket4j).
7. Dockerfile (multi-stage) + extended docker-compose.
8. Soft delete + audit columns.
9. Bean Validation (JSR-380).
10. i18n (English + French).

## P3 (stretch)

1. Spring Boot REST API sidecar + OpenAPI.
2. Embedded Lucene full-text search.
3. Quartz scheduler for nightly reminders.
4. WebSocket notifications.
5. Multi-tenant (schema-per-tenant) in REST API.
6. OpenTelemetry distributed tracing.
7. jpackage native installers.
8. Plugin architecture (ServiceProvider).

## Why this order

- **P0 first** — removes the most damning issues. The project no longer screams "beginner."
- **P1 next** — architectural soundness. Reviewers see real engineering.
- **P2** — enterprise awareness. Differentiates from 95% of student projects.
- **P3** — standout. Demonstrates senior-level breadth.

## How to execute

- **One phase at a time.** Don't skip ahead.
- **Tests before refactor.** (Phase 1 before Phase 2.)
- **Small commits.** Each commit is one refactoring step, tests green.
- **Boy Scout Rule.** Every PR leaves the code a little better.

## The gap

> "The gap between 'student project' and 'portfolio project' is not talent — it is iteration. Iterate."

— *Production Code Review*

See the next notes for phase-by-phase details.
