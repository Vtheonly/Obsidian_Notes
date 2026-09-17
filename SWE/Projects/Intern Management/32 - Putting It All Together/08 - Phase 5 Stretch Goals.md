---
tags: [concept, rebuild, phase-5]
type: concept
status: complete
---

# Phase 5 — Stretch Goals (20+ hours, optional)

> Goal: demonstrate breadth of skill. Pick 2-3, not all.

## Options

### 1. REST API (Spring Boot sidecar)
Expose `/api/v1/interns`, `/api/v1/users` etc. with:
- OpenAPI spec.
- JWT auth.
- Rate limiting.
- Pagination.

### 2. Embedded Apache Lucene full-text search
Index intern name, university, theme description. Fuzzy search.

### 3. Quartz scheduler
Nightly "remind chief of pending interns" email. Weekly stats digest.

### 4. Multi-tenant (schema-per-tenant)
In the REST API. Hibernate `@TenantId`.

### 5. Plugin architecture (Java SPI)
`DocumentExporter` interface. PDF, CSV, XLSX, HTML implementations.

### 6. WebSocket notifications
Notify all logged-in chiefs when a new intern is inserted.

### 7. OpenTelemetry distributed tracing
Trace ID propagated from controller → service → repository → DB.

### 8. jpackage native installers
`.deb`, `.rpm`, `.msi`, `.dmg`. GitHub Releases.

## Why these are "stretch"

Each demonstrates a senior-level skill that few candidates have. Pick the ones that align with the jobs you're applying for:
- Backend roles → REST API, multi-tenant, tracing.
- Data roles → Lucene, Quartz.
- DevOps roles → jpackage, CI/CD.

## Don't do all

Doing all 8 stretches the project to 200+ hours. Pick 2-3, do them well. A focused project is more impressive than a sprawling one.

## Further reading

- [[31 - Enterprise Java/00 - MOC - Enterprise Java]].
