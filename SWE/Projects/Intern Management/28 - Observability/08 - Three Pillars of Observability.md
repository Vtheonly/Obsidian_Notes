---
tags: [concept, observability]
type: concept
status: complete
---

# Three Pillars of Observability

## The three pillars

1. **Logs** — discrete events with timestamps. "What happened?"
2. **Metrics** — numeric values over time. "How much / how fast?"
3. **Traces** — request flow across services. "Where did the time go?"

## Logs

- **Structured** — JSON with fields (timestamp, level, message, user, request_id).
- **Searchable** — ELK (Elasticsearch, Logstash, Kibana), Loki, Splunk.
- **Levels** — TRACE, DEBUG, INFO, WARN, ERROR, FATAL.

## Metrics

- **Counters** — monotonically increasing (requests served, errors).
- **Gauges** — instant value (active connections, queue depth).
- **Histograms** — distribution (latency, response size).
- **Summaries** — quantiles (p50, p95, p99 latency).

Tools: Prometheus (collect), Grafana (visualize).

## Traces

- **Span** — one operation (DB query, HTTP call).
- **Trace** — tree of spans for one request.
- **Context propagation** — trace ID passed across services.

Tools: OpenTelemetry, Jaeger, Zipkin.

## Why all three

- **Logs** tell you *what* happened (the error message).
- **Metrics** tell you *how bad* it is (error rate spiked).
- **Traces** tell you *where* (which service, which query).

One pillar alone isn't enough.

## Project Connection

The project has **none** of the three:
- Logs: `System.out.println` (unstructured, no levels).
- Metrics: none.
- Traces: none.

The fix:
- Logs: SLF4J + Logback (structured JSON).
- Metrics: Micrometer + Prometheus.
- Traces: OpenTelemetry (if the app evolves to multi-service).

## Further reading

- *Observability Engineering* (Beyer et al.).
