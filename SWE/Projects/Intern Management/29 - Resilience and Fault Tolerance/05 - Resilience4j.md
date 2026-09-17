---
tags: [concept, resilience, resilience4j]
type: concept
status: complete
related:
  - [[29 - Resilience and Fault Tolerance/06 - Retry with Backoff]]
  - [[29 - Resilience and Fault Tolerance/03 - Circuit Breaker Pattern]]
  - [[29 - Resilience and Fault Tolerance/02 - Bulkhead Pattern]]
---

# Resilience4j

## What it is

**Resilience4j** is a lightweight, functional resilience library for Java. It's the successor to Netflix Hystrix (deprecated).

## Modules

- **Retry** — retry failed operations.
- **CircuitBreaker** — fail fast when a service is down.
- **Bulkhead** — limit concurrent calls.
- **RateLimiter** — throttle calls.
- **TimeLimiter** — timeout for async operations.
- **Cache** — simple caching.

## Maven

```xml
<dependency>
    <groupId>io.github.resilience4j</groupId>
    <artifactId>resilience4j-all</artifactId>
    <version>2.2.0</version>
</dependency>
```

## Combining decorators

```java
Retry retry = Retry.of("db", retryConfig);
CircuitBreaker cb = CircuitBreaker.of("db", cbConfig);
Bulkhead bulkhead = Bulkhead.of("db", bulkheadConfig);
TimeLimiter timeLimiter = TimeLimiter.of("db", Timeout.of(Duration.ofSeconds(5)));

Supplier<Intern> supplier = () -> repository.findById(id);

Supplier<Intern> resilient = Decorators.ofSupplier(supplier)
    .withRetry(retry)
    .withCircuitBreaker(cb)
    .withBulkhead(bulkhead)
    .withFallback(List.of(TimeoutException.class), e -> cachedIntern)
    .decorate();

Intern intern = resilient.get();
```

Order matters: outermost decorator runs first. Retry → CircuitBreaker → Bulkhead → call.

## Spring integration

```java
@CircuitBreaker(name = "db", fallbackMethod = "fallback")
@Retry(name = "db")
@Bulkhead(name = "db")
public Intern findById(long id) { ... }

public Intern fallback(long id, Exception e) {
    return cache.get(id);
}
```

## Project Connection

Wrap every DB call:
```java
Intern intern = resilience4j.decorateSupplier(() -> repository.findById(id)).get();
```

When the DB is down, the circuit opens, and the user sees "Database unavailable" immediately.

## Further reading

- Resilience4j documentation.
