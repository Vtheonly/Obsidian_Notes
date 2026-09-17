---
tags: [concept, observability, tracing, opentelemetry]
type: concept
status: complete
---

# Distributed Tracing (OpenTelemetry)

## What it is

**Distributed tracing** tracks a request as it flows through multiple services. Each step is a **span**; all spans for one request form a **trace**.

## OpenTelemetry

**OpenTelemetry** (OTel) is the standard for instrumenting code. Vendor-neutral — exports to Jaeger, Zipkin, Datadog, etc.

## Usage

```java
import io.opentelemetry.api.trace.*;

Tracer tracer = openTelemetry.getTracer("intern-management");

public Intern createIntern(CreateInternCommand cmd) {
    Span span = tracer.spanBuilder("createIntern").startSpan();
    try (Scope scope = span.makeCurrent()) {
        span.setAttribute("intern.name", cmd.name());
        Intern intern = repository.save(...);
        span.setAttribute("intern.id", intern.getId());
        return intern;
    } catch (Exception e) {
        span.recordException(e);
        span.setStatus(StatusCode.ERROR);
        throw e;
    } finally {
        span.end();
    }
}
```

## Context propagation

The trace ID is propagated across service calls (HTTP headers, message queue metadata). Each service adds its span to the trace.

## When to use

- **Microservices** — essential for debugging cross-service issues.
- **Monoliths** — useful for tracing request flow through layers (controller → service → repository).

For a desktop app, tracing is overkill (single process, single user).

## Project Connection

Not needed for the desktop app. If it evolves to a server with REST API + DB + email service, OpenTelemetry traces help debug "why is creating an intern slow?"

## Further reading

- OpenTelemetry documentation.
