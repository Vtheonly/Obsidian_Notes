---
tags: [concept, docker, healthcheck]
type: concept
status: complete
related:
  - [[28 - Observability/03 - Health Check Endpoints]]
---

# Docker Healthchecks

## What it is

A `HEALTHCHECK` tells Docker how to check if a container is healthy.

## Usage

```yaml
services:
  oracle-db:
    healthcheck:
      test: ["CMD", "healthcheck.sh"]
      interval: 15s
      timeout: 10s
      retries: 5
      start_period: 30s
```

- `test` — command to run. Exit 0 = healthy, non-zero = unhealthy.
- `interval` — how often to check.
- `timeout` — how long to wait for the command.
- `retries` — consecutive failures before marking unhealthy.
- `start_period` — grace period at startup.

## Why

- **`depends_on` with `condition: service_healthy`** — the app waits for Oracle to be healthy before starting.
- **Auto-restart** — orchestrators (Docker Swarm, Kubernetes) restart unhealthy containers.
- **Monitoring** — `docker ps` shows health status.

## The project's bug

The project's `docker-compose.yml` has the healthcheck commented out:
```yaml
# healthcheck:
#   test: ["CMD", "sqlplus", "-L", "sys/rootroot@//localhost:1521/XE as sysdba", "exit"]
```

Without a healthcheck, the app may try to connect before Oracle is ready (Oracle takes 30+ seconds to start), fail, and never retry.

## The fix

```yaml
healthcheck:
  test: ["CMD", "healthcheck.sh"]
  interval: 15s
  timeout: 10s
  retries: 5
  start_period: 60s
```

(`healthcheck.sh` is a built-in script in `gvenzl/oracle-xe`.)

## Further reading

- Docker HEALTHCHECK documentation.
