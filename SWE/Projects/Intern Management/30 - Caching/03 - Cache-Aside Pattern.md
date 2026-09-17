---
tags: [concept, caching, cache-aside]
type: concept
status: complete
related:
  - [[30 - Caching/01 - Cache Invalidation]]
---

# Cache-Aside Pattern

## What it is

The **cache-aside** (lazy loading) pattern: the application checks the cache first; on miss, loads from the DB and populates the cache.

```java
public Intern findById(long id) {
    Intern cached = cache.getIfPresent(id);
    if (cached != null) return cached;

    Intern fromDb = repository.findById(id).orElseThrow();
    cache.put(id, fromDb);
    return fromDb;
}
```

## Why

- **Fast reads** — cache hit is O(1).
- **Lazy** — only caches what's accessed.
- **Simple** — no DB triggers or cache loaders.

## Variations

### Read-through
The cache provider handles the DB read on miss:
```java
Intern intern = cache.get(id, key -> repository.findById(key).orElseThrow());
```
(Caffeine's `get(key, loader)` does this.)

### Write-through
Writes update both cache and DB:
```java
public void save(Intern intern) {
    repository.save(intern);
    cache.put(intern.getId(), intern);
}
```

### Write-behind
Writes update the cache immediately, async-write to DB:
```java
public void save(Intern intern) {
    cache.put(intern.getId(), intern);
    asyncWriteQueue.add(intern);  // written to DB later
}
```
Fast writes, but risk of data loss on crash.

## Project Connection

The project calls `getSelectableOptions("department", "department_name")` on every form open — 50 DB queries per session for static data. The fix: cache-aside with Caffeine, 5-min TTL, invalidate on insert/update/delete.

## Further reading

- *Designing Data-Intensive Applications* (Kleppmann).
