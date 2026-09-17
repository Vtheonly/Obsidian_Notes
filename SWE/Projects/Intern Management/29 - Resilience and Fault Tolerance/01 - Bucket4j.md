---
tags: [concept, resilience, rate-limiting, bucket4j]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/03 - Brute Force Protection]]
---

# Bucket4j

## What it is

**Bucket4j** is a Java rate-limiting library based on the token bucket algorithm.

## Token bucket

- A bucket holds N tokens.
- Each request consumes 1 token.
- Tokens are refilled at rate R per second.
- If no tokens, the request is rejected (or waits).

## Usage

```java
Bucket bucket = Bucket.builder()
    .addLimit(limit -> limit.capacity(10).refillGreedy(10, Duration.ofMinutes(1)))
    .build();

if (bucket.tryConsume(1)) {
    // allow the request
} else {
    // rate limit exceeded
    throw new RateLimitExceededException();
}
```

## Per-user limiting

```java
Map<String, Bucket> buckets = new ConcurrentHashMap<>();

public Bucket getBucket(String username) {
    return buckets.computeIfAbsent(username, k ->
        Bucket.builder()
            .addLimit(limit -> limit.capacity(5).refillGreedy(5, Duration.ofMinutes(1)))
            .build()
    );
}

public AuthResult authenticate(String username, String password) {
    if (!getBucket(username).tryConsume(1)) {
        throw new RateLimitExceededException("Too many attempts. Try again in 1 minute.");
    }
    // ... authenticate
}
```

5 login attempts per minute per username. After 5, the user is rate-limited.

## Distributed rate limiting

For multi-instance apps, use Bucket4j with Redis or Hazelcast:
```java
Bucket bucket = bucketProxyManager.builder()
    .withImplicitConfigurationReplacement(key, supplier)
    .build();
```

## Why

- **Brute-force protection** — limit login attempts.
- **API rate limiting** — protect against abuse.
- **Fairness** — one user can't monopolize the API.

## Project Connection

The project has no rate limiting. The fix: Bucket4j on login (5 attempts/min/username), on search (60/min/user), on PDF generation (10/min/user).

## Further reading

- Bucket4j documentation.
