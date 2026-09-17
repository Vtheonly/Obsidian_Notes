---
tags: [concept, docker, compose]
type: concept
status: complete
related:
  - [[25 - Docker and Deployment/02 - Docker Secrets]]
  - [[25 - Docker and Deployment/04 - Healthchecks]]
---

# Docker Compose

## What it is

`docker-compose.yml` defines multi-service applications. One command (`docker compose up`) starts everything.

## The project's docker-compose

```yaml
services:
  oracle-db:
    image: gvenzl/oracle-xe
    ports: ["1521:1521"]
    environment:
      ORACLE_PASSWORD: rootroot
    volumes:
      - oracle_data:/opt/oracle/oradata
      - ./sql-scripts:/container-entrypoint-initdb.d  # WRONG PATH
    shm_size: 2g
    # healthcheck commented out
volumes:
  oracle_data:
```

Problems:
1. `ORACLE_PASSWORD: rootroot` in plaintext.
2. `./sql-scripts` doesn't exist (SQL is in `src/main/sql/`).
3. No healthcheck.
4. No `restart: unless-stopped`.
5. No app service.
6. No network isolation.

## The fix

```yaml
version: '3.8'
services:
  oracle-db:
    image: gvenzl/oracle-xe:21-slim
    restart: unless-stopped
    ports: ["1521:1521"]
    environment:
      ORACLE_PASSWORD_FILE: /run/secrets/oracle_password
      APP_USER: intern_app
      APP_USER_PASSWORD_FILE: /run/secrets/app_password
    volumes:
      - oracle_data:/opt/oracle/oradata
      - ./src/main/sql:/container-entrypoint-initdb.d:ro
    shm_size: 2g
    secrets: [oracle_password, app_password]
    healthcheck:
      test: ["CMD", "healthcheck.sh"]
      interval: 15s
      timeout: 10s
      retries: 5
    networks: [app-tier]

  app:
    build: .
    depends_on:
      oracle-db: { condition: service_healthy }
    environment:
      DB_URL: jdbc:oracle:thin:@oracle-db:1521/XE
      DB_USER_FILE: /run/secrets/app_user
      DB_PASSWORD_FILE: /run/secrets/app_password
    secrets: [app_user, app_password]
    networks: [app-tier]

secrets:
  oracle_password: { file: ./secrets/oracle_password.txt }
  app_password: { file: ./secrets/app_password.txt }
  app_user: { file: ./secrets/app_user.txt }

volumes:
  oracle_data:

networks:
  app-tier:
    driver: bridge
```

## Further reading

- Docker Compose specification.
