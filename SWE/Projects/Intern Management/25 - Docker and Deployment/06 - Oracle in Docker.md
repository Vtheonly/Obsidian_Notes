---
tags: [concept, docker, oracle, gvenzl]
type: concept
status: complete
---

# Oracle in Docker

## The image

`gvenzl/oracle-xe` is the standard community Oracle XE Docker image. (Oracle has an official image too, but gvenzl's is more popular.)

## Tags

- `gvenzl/oracle-xe:21-slim` — Oracle 21c XE, slim variant (~1.5 GB).
- `gvenzl/oracle-xe:21-full` — full variant (~6 GB).
- `gvenzl/oracle-xe:18-slim` — Oracle 18c XE.
- `gvenzl/oracle-xe:11-slim` — Oracle 11g XE.

Use `21-slim` for development.

## Environment variables

| Variable | Purpose |
|---|---|
| `ORACLE_PASSWORD` | SYS/SYSTEM password. |
| `ORACLE_PASSWORD_FILE` | Same, from a file (secrets). |
| `APP_USER` | Create a low-privilege app user. |
| `APP_USER_PASSWORD` | App user's password. |

## Init scripts

Mount SQL scripts to `/container-entrypoint-initdb.d/`:
```yaml
volumes:
  - ./src/main/sql:/container-entrypoint-initdb.d:ro
```

Scripts run in alphabetical order on first start (when the data volume is empty).

## Persistence

```yaml
volumes:
  - oracle_data:/opt/oracle/oradata
```

Named volume — data survives container recreation.

## `shm_size`

Oracle needs shared memory. Set `shm_size: 2g` (or at least 1g):
```yaml
shm_size: 2g
```

Without it, Oracle may fail to start or run slowly.

## Project Connection

The project uses `gvenzl/oracle-xe` (unversioned) with hardcoded `rootroot`, wrong mount path, no healthcheck. The fix: pin `21-slim`, use secrets, correct mount, add healthcheck.

## Further reading

- `gvenzl/oracle-xe` GitHub README.
