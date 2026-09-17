---
tags: [concept, caching, invalidation]
type: concept
status: complete
related:
  - [[30 - Caching/03 - Cache-Aside Pattern]]
---

# Cache Invalidation

> "There are only two hard things in Computer Science: cache invalidation and naming things." — Phil Karlton

## The problem

When the underlying data changes, the cache becomes stale. You must invalidate (or update) the cache.

## Strategies

### 1. TTL (Time-to-Live)
```java
Cache<Long, Intern> cache = Caffeine.newBuilder()
    .expireAfterWrite(5, TimeUnit.MINUTES)
    .build();
```
Entries expire after 5 minutes. Simple, but data can be stale for up to 5 min.

### 2. Explicit invalidation
```java
public void save(Intern intern) {
    repository.save(intern);
    cache.put(intern.getId(), intern);  // update cache
}

public void delete(long id) {
    repository.delete(id);
    cache.invalidate(id);  // remove from cache
}
```
Always up-to-date, but requires discipline (every write must invalidate).

### 3. Write-through
Updates go to cache and DB simultaneously. No stale data, but adds latency to writes.

### 4. Event-driven
Subscribe to DB change events (Oracle CDC, Debezium). On change, invalidate the cache. Complex but automatic.

## The trade-off

- **TTL only** — simple, but stale data.
- **Explicit only** — always fresh, but easy to forget.
- **Both** — explicit for writes, TTL as a safety net.

## Common pitfalls

- **Forgetting to invalidate** — stale data leads to bugs.
- **Invalidating too much** — cache hit rate drops.
- **Cascade invalidation** — invalidating `intern:123` should also invalidate `interns:by-department:5`.

## Project Connection

The fix: Caffeine with 5-min TTL + explicit invalidation on insert/update/delete. For lookup tables (departments, roles), TTL is enough (they rarely change). For interns, invalidate on every mutation.

## Further reading

- *Designing Data-Intensive Applications* (Kleppmann).
