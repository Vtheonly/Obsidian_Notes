---
tags: [concept, resilience, circuit-breaker]
type: concept
status: complete
related:
  - [[29 - Resilience and Fault Tolerance/06 - Retry with Backoff]]
---

# Circuit Breaker Pattern

## What it is

A **circuit breaker** stops calling a failing service. After N failures, the circuit "opens" — calls fail fast (no network wait). After a cooldown, it "half-opens" — one test call. If it succeeds, the circuit "closes" (normal operation).

## States

```
       CLOSED (normal)
          │
          │ failures ≥ threshold
          ▼
       OPEN (fail fast)
          │
          │ after cooldown
          ▼
     HALF_OPEN (test)
       │       │
   success   failure
       │       │
       ▼       ▼
    CLOSED   OPEN
```

- **CLOSED** — normal operation. Track failures.
- **OPEN** — calls fail immediately (no network). Wait for cooldown.
- **HALF_OPEN** — allow one test call. Success → CLOSED. Failure → OPEN.

## Why

- **Fail fast** — don't make the user wait 30 seconds for a timeout when the DB is down.
- **Let the failing service recover** — stop hammering it.
- **Cascade prevention** — one service's failure doesn't bring down everything.

## Implementation (Resilience4j)

```java
CircuitBreakerConfig config = CircuitBreakerConfig.custom()
    .failureRateThreshold(50)            // 50% failures → open
    .slowCallRateThreshold(80)           // 80% slow calls → open
    .slowCallDurationThreshold(Duration.ofSeconds(2))
    .waitDurationInOpenState(Duration.ofSeconds(30))
    .permittedNumberOfCallsInHalfOpenState(3)
    .slidingWindowSize(10)               // last 10 calls
    .build();
CircuitBreaker cb = CircuitBreaker.of("db", config);

T result = cb.executeSupplier(() -> repository.findById(id));
```

## Fallback

When the circuit is open, return a fallback:
```java
T result = CircuitBreaker.decorateSupplier(cb, () -> repository.findById(id))
    .recover(throwable -> cache.get(id))
    .get();
```

## Project Connection

The project's static `Connection` is the anti-pattern: if the DB is down, every call waits for a timeout. The fix: circuit breaker around DB calls. When open, show "Database unavailable" immediately instead of hanging.

## Further reading

- *Release It!* (Nygard) — Circuit Breaker.
- Resilience4j CircuitBreaker documentation.
