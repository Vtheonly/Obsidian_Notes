---
tags: [concept, observability, health-check]
type: concept
status: complete
related:
  - [[25 - Docker and Deployment/04 - Healthchecks]]
---

# Health Check Endpoints

## What it is

A **health check endpoint** (`/health`) reports whether the app is healthy. Used by:
- Docker `HEALTHCHECK`.
- Kubernetes liveness/readiness probes.
- Load balancers.
- Monitoring systems.

## Implementation

```java
public class HealthCheck {
    private final DataSource dataSource;

    public HealthResponse check() {
        List<HealthCheckResult> checks = List.of(
            checkDatabase(),
            checkDiskSpace(),
            checkMemory()
        );
        boolean allHealthy = checks.stream().allMatch(HealthCheckResult::isHealthy);
        return new HealthResponse(allHealthy ? "UP" : "DOWN", checks);
    }

    private HealthCheckResult checkDatabase() {
        try (Connection conn = dataSource.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery("SELECT 1 FROM DUAL")) {
            rs.next();
            return HealthCheckResult.healthy("database");
        } catch (SQLException e) {
            return HealthCheckResult.unhealthy("database", e.getMessage());
        }
    }
}
```

Expose via HTTP:
```java
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/health", exchange -> {
    HealthResponse response = healthCheck.check();
    int status = "UP".equals(response.status()) ? 200 : 503;
    exchange.sendResponseHeaders(status, 0);
    exchange.getResponseBody().write(toJson(response).getBytes());
});
server.start();
```

## Liveness vs Readiness (Kubernetes)

- **Liveness** — "is the app running?" If false, restart the container.
- **Readiness** — "is the app ready to serve traffic?" If false, remove from load balancer (but don't restart).

For a desktop app, these don't apply. For a server:
- Liveness: `GET /health/live` — checks the JVM is up.
- Readiness: `GET /health/ready` — checks DB connectivity, pool saturation, etc.

## Project Connection

The project has no health check. The fix: `/health` endpoint on localhost:8080 for Docker `HEALTHCHECK` and monitoring.

## Further reading

- Spring Boot Actuator health endpoints.
