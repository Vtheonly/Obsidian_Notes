---
tags: [concept, observability, micrometer, metrics]
type: concept
status: complete
related:
  - [[28 - Observability/06 - Prometheus and Grafana]]
---

# Micrometer

## What it is

**Micrometer** is a metrics facade (like SLF4J for logs). You write metrics once; Micrometer exports to Prometheus, Datadog, New Relic, etc.

## Usage

```java
import io.micrometer.core.instrument.*;

public class InternService {
    private final MeterRegistry registry;
    private final Counter internsCreated;
    private final Timer searchTimer;

    public InternService(MeterRegistry registry, InternRepository repo) {
        this.registry = registry;
        this.internsCreated = registry.counter("interns.created");
        this.searchTimer = registry.timer("interns.search");
    }

    public Intern create(...) {
        internsCreated.increment();
        // ...
    }

    public List<Intern> search(String name) {
        return searchTimer.record(() -> repository.findByName(name));
    }

    public void initGauges() {
        Gauge.builder("interns.pending", () -> repository.countByStatus("Pending"))
             .register(registry);
    }
}
```

## Meter types

| Type | What it measures | Example |
|---|---|---|
| Counter | Monotonically increasing | Requests served, errors |
| Gauge | Instant value | Active connections, queue depth |
| Timer | Duration + count | Query latency |
| DistributionSummary | Distribution | Response size |
| LongTaskTimer | Long-running operations | Batch job duration |

## Annotations (Spring)

```java
@Timed(value = "interns.search", percentiles = {0.5, 0.95, 0.99})
public List<Intern> search(String name) { ... }
```

## Why

- **Spot bottlenecks** — "the search endpoint p95 latency is 2 sec; let's add an index."
- **Capacity planning** — "we're at 80% of max connections; time to scale."
- **Anomaly detection** — "login failures spiked 10x — possible attack."

## Project Connection

The project has no metrics. The fix: Micrometer with:
- Counter: `interns.created`, `interns.accepted`, `interns.rejected`, `login.attempts`, `login.failures`.
- Timer: `interns.search.duration`, `db.query.duration`.
- Gauge: `db.pool.active`, `db.pool.idle`, `jvm.memory.heap.used`.

## Further reading

- Micrometer documentation.
