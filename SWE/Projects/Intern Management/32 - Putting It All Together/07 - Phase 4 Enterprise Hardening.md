---
tags: [concept, rebuild, phase-4]
type: concept
status: complete
---

# Phase 4 — Enterprise Hardening (16-24 hours)

> Goal: add observability, security, and resilience features that distinguish a portfolio project.

## Tasks

### 1. SLF4J + Logback
Replace every `System.out` / `printStackTrace` with parameterized logging. Configure rolling file appender (30 days, JSON encoded).

### 2. Micrometer + Prometheus
Instrument service methods with `@Timed`. Counters for logins/failures. Gauges for active sessions. Expose `localhost:8080/metrics`.

### 3. Audit log table + AuditService
Every mutation writes an audit entry in the same transaction. 'Audit Log' tab for admins.

### 4. Resilience4j
Retry (3 attempts, exp backoff). Circuit breaker (50% failure, 30s open). Bulkhead (10 concurrent DB calls).

### 5. Rate limiting on login (Bucket4j)
5 attempts per minute per username. Lock for 5 min after 5 failures.

### 6. Flyway migrations
`V1__baseline.sql`, `V2__add_audit_columns.sql`, `V3__add_indexes.sql`, `V4__identity_columns.sql`, `V5__soft_delete.sql`.

### 7. Caffeine cache for lookup tables
5-minute TTL, invalidate on mutation.

### 8. Password reset flow
Email a one-time token. User enters new password. Argon2id hash.

### 9. Dockerfile (multi-stage)
Builder + runtime. Extend docker-compose: app + oracle + (optional) prometheus + grafana.

### 10. GitHub Actions CI
Build + test + Sonar + dependency-check + SpotBugs + jpackage artifact on tag.

### 11. OpenHTMLtoPDF
Replace deprecated HTMLWorker. FileChooser for save path.

### 12. Jakarta Mail email tab
Async send via background executor. Template-based emails.

## After Phase 4

The project is production-grade:
- Observable (logs, metrics, audit).
- Resilient (retry, circuit breaker, rate limiting).
- Secure (Argon2id, RBAC, rate limiting, audit).
- Containerized (Docker, Compose).
- CI/CD (GitHub Actions).
- Tested (unit, integration, UI).

## Further reading

- [[28 - Observability/00 - MOC - Observability]].
- [[29 - Resilience and Fault Tolerance/00 - MOC - Resilience]].
