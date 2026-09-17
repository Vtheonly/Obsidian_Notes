---
tags: [concept, docker, secrets, security]
type: concept
status: complete
related:
  - [[17 - Application Security/09 - Secrets Management]]
---

# Docker Secrets

## What it is

**Docker Secrets** is Docker's secrets management. Secrets are mounted as files in `/run/secrets/`, readable only by the service.

## Why

- **Not visible in `docker inspect`** — environment variables are.
- **Not in the image** — mounted at runtime.
- **Encrypted at rest** (in swarm mode).
- **Rotatable** — update the secret file, restart the service.

## Usage (docker-compose)

```yaml
services:
  app:
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
    secrets: [db_password]

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

The app reads the file:
```java
String password = Files.readString(Path.of(System.getenv("DB_PASSWORD_FILE")));
```

## The project's fix

Replace `ORACLE_PASSWORD: rootroot` with:
```yaml
environment:
  ORACLE_PASSWORD_FILE: /run/secrets/oracle_password
secrets:
  - oracle_password
secrets:
  oracle_password:
    file: ./secrets/oracle_password.txt
```

`./secrets/` is gitignored. Each developer has their own secrets file.

## Further reading

- Docker Secrets documentation.
