---
tags: [concept, docker, dockerfile]
type: concept
status: complete
---

# Dockerfile

## What it is

A `Dockerfile` is a script that builds a Docker image.

## Basic structure

```dockerfile
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY target/intern-management-1.0.0.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Commands

| Command | Purpose |
|---|---|
| `FROM` | Base image. |
| `RUN` | Execute a command (build step). |
| `COPY` | Copy files from host to image. |
| `ADD` | Like COPY + URL extraction + tar extraction. |
| `WORKDIR` | Set working directory. |
| `ENV` | Set environment variable. |
| `ARG` | Build-time variable. |
| `EXPOSE` | Document a port (doesn't actually publish). |
| `VOLUME` | Declare a mount point. |
| `USER` | Run as a non-root user. |
| `CMD` | Default command (overridable). |
| `ENTRYPOINT` | Fixed command (CMD becomes args). |
| `HEALTHCHECK` | How to check if the container is healthy. |

## Best practices

- **Use specific tags** — `eclipse-temurin:21-jre`, not `latest`.
- **Multi-stage** — see [[25 - Docker and Deployment/05 - Multi-Stage Builds]].
- **Layer caching** — put rarely-changing layers first (dependencies), frequently-changing last (code).
- **Non-root user** — `USER 1000:1000` for security.
- **Small images** — use `jlink` for custom runtimes, or `alpine`/`distroless` base.
- **`.dockerignore`** — exclude `target/`, `.git/`, `*.md`.

## Project Connection

The project has no Dockerfile for the app (only `docker-compose.yml` for Oracle). The fix:

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/target/intern-management-1.0.0.jar app.jar
USER 1000:1000
ENTRYPOINT ["java", "-jar", "app.jar"]
```

## Further reading

- Dockerfile reference (docs.docker.com).
