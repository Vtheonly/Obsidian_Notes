---
tags: [concept, resilience]
type: concept
status: complete
---

# What Is Resilience?

## The definition

**Resilience** is the ability of a system to keep functioning when things go wrong — network failures, dependency outages, traffic spikes, partial failures.

## The assumption

> "Networks are unreliable. Databases restart. Services fail. Plan for it."

The project assumes the DB is always up and the network is always fast. Real systems can't make these assumptions.

## Resilience patterns

1. **Retry** — try again on transient failure.
2. **Circuit Breaker** — stop calling a failing service.
3. **Bulkhead** — limit concurrent calls to a service.
4. **Timeout** — don't wait forever.
5. **Rate Limiting** — protect against overload.
6. **Fallback** — return a default when the real service fails.
7. **Idempotency** — safe retries.

## The project's resilience status

Zero resilience:
- Static `Connection` — if it dies, the app is dead until restart.
- No retry — one network blip = failed operation.
- No timeout — a slow query blocks forever.
- No circuit breaker — the app keeps trying a dead DB.
- No bulkhead — one slow operation blocks the pool.

## The fix

Wrap every external call (DB, email, PDF) in resilience patterns. Use Resilience4j (the modern Hystrix successor).

## Further reading

- *Release It!* (Nygard) — the book on resilience.
- *Chaos Engineering* (Rosenthal et al.).
