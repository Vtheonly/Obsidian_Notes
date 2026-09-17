---
tags: [concept, observability, prometheus, grafana]
type: concept
status: complete
related:
  - [[28 - Observability/05 - Micrometer]]
---

# Prometheus and Grafana

## Prometheus

**Prometheus** is a metrics collection and storage system. It scrapes metrics from instrumented apps via HTTP (`/metrics`).

### Micrometer + Prometheus

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

Spring Boot Actuator exposes `/actuator/prometheus` automatically. For a desktop app, run a small HTTP server:

```java
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/metrics", exchange -> {
    String body = prometheusRegistry.scrape();
    exchange.sendResponseHeaders(200, body.length());
    exchange.getResponseBody().write(body.getBytes());
});
server.start();
```

### PromQL

Query language:
- `rate(interns_created_total[5m])` — creations per second.
- `histogram_quantile(0.95, rate(interns_search_duration_seconds_bucket[5m]))` — p95 latency.
- `sum by (status) (interns_status)` — count by status.

## Grafana

**Grafana** is a dashboarding tool. Connects to Prometheus (and many other sources).

### Dashboards
- JVM metrics (heap, GC, threads).
- DB pool (active, idle, wait time).
- App metrics (requests, errors, latency).
- Custom (interns by status, login attempts).

### Alerts
- "p95 latency > 1 sec for 5 min."
- "Error rate > 1% for 5 min."
- "DB pool utilization > 80%."

## Docker Compose

```yaml
services:
  prometheus:
    image: prom/prometheus:v2.45.0
    ports: ["9090:9090"]
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  grafana:
    image: grafana/grafana:10.1.0
    ports: ["3000:3000"]
```

## Project Connection

For a desktop app, Prometheus + Grafana is overkill. But you can expose `/metrics` on localhost for debugging:

```java
// In the app:
PerformanceDiagnosticsEngine engine = new PerformanceDiagnosticsEngine(dataSource);
// Expose via small HTTP server on localhost:8080/metrics
```

The diagnostics dashboard (in-app) shows the same info.

## Further reading

- Prometheus documentation.
- Grafana documentation.
