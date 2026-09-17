---
tags: [concept, caching, caffeine, performance]
type: concept
status: complete
prerequisites:
  - [[11 - DB Performance and Indexing/09 - Connection Pooling]]
related:
  - [[30 - Caching/00 - MOC - Caching]]
---

# Caffeine Cache

## What it is

**Caffeine** is a high-performance Java caching library. It's the spiritual successor to Guava Cache, with better performance and more features.

## Maven dependency

```xml
<dependency>
    <groupId>com.github.ben-manes.caffeine</groupId>
    <artifactId>caffeine</artifactId>
    <version>3.1.8</version>
</dependency>
```

## Basic usage

```java
Cache<String, List<String>> cache = Caffeine.newBuilder()
    .maximumSize(1000)
    .expireAfterWrite(5, TimeUnit.MINUTES)
    .recordStats()
    .build();

// Put
cache.put("departments", departmentRepository.findAllNames());

// Get (returns null if absent)
List<String> depts = cache.getIfPresent("departments");

// Get with loader (computes if absent)
List<String> depts = cache.get("departments", k -> departmentRepository.findAllNames());
```

## Features

- **Size-based eviction** (`maximumSize`) — LRU when full.
- **Time-based eviction** (`expireAfterWrite`, `expireAfterAccess`).
- **Weak/soft keys/values** — allow GC to reclaim.
- **Statistics** (`recordStats`) — hit rate, miss rate, load time.
- **Async loading** (`AsyncCache`) — `CompletableFuture`-based.
- **Refresh** (`refreshAfterWrite`) — reload in background before expiry.
- **Listenable** — `RemovalListener` for eviction events.

## When to cache

- **Lookup tables** — departments, roles, themes. Rarely change, frequently queried.
- **Computed results** — dashboard metrics (cache for 5 minutes).
- **External API responses** — cache third-party data.

## When NOT to cache

- **Frequently changing data** — cache invalidation is hard.
- **Per-user data** — cache size explodes.
- **Data that must be fresh** — financial balances, inventory counts.

## Spring Cache abstraction

```java
@Service
public class DepartmentService {
    @Cacheable("departments")  // cache the result
    public List<Department> findAll() {
        return repository.findAll();
    }

    @CacheEvict("departments")  // invalidate on change
    public void save(Department dept) {
        repository.save(dept);
    }
}
```

Spring abstracts the cache provider — Caffeine, Redis, Ehcache.

## Project Connection

The project calls `getSelectableOptions("department", "department_name")` on every form open. With 10 forms × 5 lookups per form, that's 50 unnecessary DB queries per session.

The fix:
```java
Cache<String, List<String>> lookupCache = Caffeine.newBuilder()
    .expireAfterWrite(5, TimeUnit.MINUTES)
    .build();

public List<String> getDepartments() {
    return lookupCache.get("departments", k -> repository.findAllDepartmentNames());
}
```

Invalidate on insert/update/delete.

## Common pitfalls

- **Stale data** — cache returns old data after a DB update. Always invalidate on writes.
- **Cache stampede** — on expiry, 1000 requests hit the DB simultaneously. Use `refreshAfterWrite` or a lock.
- **Memory pressure** — unbounded cache causes OOM. Always set `maximumSize`.

## Further reading

- Caffeine GitHub — wiki and benchmarks.
- Spring Cache documentation.
