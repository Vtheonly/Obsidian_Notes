---
tags: [concept, caching, stampede]
type: concept
status: complete
related:
  - [[30 - Caching/03 - Cache-Aside Pattern]]
  - [[29 - Resilience and Fault Tolerance/06 - Retry with Backoff]]
---

# Cache Stampede and Thundering Herd

## The problem

When a cache entry expires, N concurrent requests all see a miss and all hit the DB:
```
[Request 1] miss → query DB
[Request 2] miss → query DB
[Request 3] miss → query DB
...
[Request 1000] miss → query DB
```
The DB is overwhelmed.

## Solutions

### 1. Locking
Only one request queries the DB; others wait:
```java
Intern intern = cache.get(id, key -> {
    // Only one thread executes this; others wait
    return repository.findById(key).orElseThrow();
});
```
Caffeine's `get(key, loader)` does this automatically (the loader is called once per key).

### 2. Refresh-ahead
Refresh the cache *before* it expires:
```java
Cache<Long, Intern> cache = Caffeine.newBuilder()
    .refreshAfterWrite(4, TimeUnit.MINUTES)  // refresh at 4 min
    .expireAfterWrite(5, TimeUnit.MINUTES)   // expire at 5 min
    .build(key -> repository.findById(key).orElseThrow());
```
At 4 min, the cache refreshes in the background. The 5-min TTL is the fallback.

### 3. Early expiration with jitter
Add randomness to the TTL so entries don't all expire at once:
```java
long ttl = baseTtl + ThreadLocalRandom.current().nextLong(0, 60);  // 0-60 sec jitter
```

## Project Connection

The fix uses Caffeine's `get(key, loader)` (locking) + `refreshAfterWrite` (refresh-ahead). Stampede is prevented.

## Further reading

- *Designing Data-Intensive Applications* (Kleppmann).
