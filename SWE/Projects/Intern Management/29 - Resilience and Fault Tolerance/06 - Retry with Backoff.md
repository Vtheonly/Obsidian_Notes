---
tags: [concept, resilience, retry, backoff]
type: concept
status: complete
related:
  - [[29 - Resilience and Fault Tolerance/04 - Idempotency]]
---

# Retry with Backoff

## What it is

When an operation fails transiently (network blip, DB restart), retry it after a delay.

## Exponential backoff

Each retry waits longer:
```
Attempt 1: immediate
Attempt 2: wait 1 sec
Attempt 3: wait 2 sec
Attempt 4: wait 4 sec
Attempt 5: wait 8 sec
```

Gives the failing service time to recover.

## Jitter

Add randomness to prevent the **thundering herd** problem (all clients retrying at the same time):
```java
long backoff = baseDelay * (1L << attempt);
long jitter = ThreadLocalRandom.current().nextLong(0, backoff / 10);
long delay = backoff + jitter;
Thread.sleep(delay);
```

## When to retry

- **Transient failures** — network timeout, connection reset, 503.
- **NOT for** — 400 Bad Request, 404 Not Found, validation errors. Retrying won't help.

## When NOT to retry

- **Non-idempotent operations** — retrying a non-idempotent insert could create duplicates. See [[29 - Resilience and Fault Tolerance/04 - Idempotency]].
- **After max attempts** — give up, report failure.
- **For business errors** — duplicate email, invalid input.

## Implementation

```java
public <T> T retryWithBackoff(Supplier<T> operation, int maxAttempts) {
    int attempt = 0;
    while (true) {
        try {
            return operation.get();
        } catch (SQLException e) {
            attempt++;
            if (attempt >= maxAttempts || !isTransient(e)) {
                throw new RuntimeException(e);
            }
            long backoff = calculateExponentialBackoff(attempt);
            try {
                Thread.sleep(backoff);
            } catch (InterruptedException ie) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(ie);
            }
        }
    }
}
```

Or use Resilience4j:
```java
RetryConfig config = RetryConfig.custom()
    .maxAttempts(3)
    .intervalFunction(IntervalFunction.ofExponentialBackoff(1000, 2.0))
    .retryOnException(e -> e instanceof SQLException)
    .build();
Retry retry = Retry.of("dbQuery", config);

T result = retry.executeSupplier(() -> repository.findById(id));
```

## Project Connection

The project has no retry — one failed DB call = failed operation. The fix: Resilience4j Retry on repository operations, with exponential backoff + jitter.

## Further reading

- *Release It!* (Nygard).
- Resilience4j Retry documentation.
