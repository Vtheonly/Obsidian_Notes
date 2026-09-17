---
tags: [concept, docker, multi-stage]
type: concept
status: complete
prerequisites:
  - [[25 - Docker and Deployment/03 - Dockerfile]]
---

# Multi-Stage Builds

## What it is

A multi-stage build has multiple `FROM` lines. Each stage produces an intermediate image; the final stage copies only what's needed.

## Why

- **Smaller final image** — no Maven, no source, no test deps.
- **Separation** — build tools don't leak into runtime.
- **Security** — fewer tools in the runtime image = smaller attack surface.

## Example

```dockerfile
# Stage 1: Build
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline  # cache deps
COPY src ./src
RUN mvn package -DskipTests

# Stage 2: Runtime
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=builder /app/target/intern-management-1.0.0.jar app.jar
USER 1000:1000
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Final image: ~200 MB (JRE + JAR). Without multi-stage: ~800 MB (Maven + JDK + source + JAR).

## Project Connection

The project has no Dockerfile. The fix: multi-stage build as above.

## Further reading

- Docker multi-stage builds documentation.
