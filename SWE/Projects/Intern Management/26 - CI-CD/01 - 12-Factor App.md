---
tags: [concept, devops, 12-factor, methodology]
type: concept
status: complete
---

# 12-Factor App

> "Twelve-Factor App" (Heroku, 2011) is a methodology for building SaaS apps that are portable, scalable, and deployable on modern cloud platforms.

## The 12 factors

1. **Codebase** — one codebase per app, many deploys.
2. **Dependencies** — explicitly declare and isolate (Maven, pip, npm).
3. **Config** — store config in environment variables, not code.
4. **Backing services** — treat DBs, caches, email as attached resources (via URLs).
5. **Build, release, run** — separate build and run stages.
6. **Processes** — stateless processes; state in DB/cache.
7. **Port binding** — self-contained apps (bind to a port).
8. **Concurrency** — scale via processes (horizontal).
9. **Disposability** — fast startup and graceful shutdown.
10. **Dev/prod parity** — similar tools across environments.
11. **Logs** — write to stdout (let the platform route them).
12. **Admin processes** — one-off tasks (migrations, scripts) use the same environment.

## Project violations

1. **Config** — hardcoded `system/rootroot` in code. Fix: env vars.
2. **Backing services** — JDBC URL hardcoded. Fix: `DB_URL` env var.
3. **Processes** — desktop app, not a server process. (Less relevant.)
4. **Logs** — `System.out.println`. Fix: SLF4J + Logback.
5. **Dev/prod parity** — one config for all environments. Fix: profiles.
6. **Admin processes** — manual SQL scripts. Fix: Flyway migrations.

## Further reading

- 12factor.net.
