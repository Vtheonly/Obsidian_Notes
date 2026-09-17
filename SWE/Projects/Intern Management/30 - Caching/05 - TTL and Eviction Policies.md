---
tags: [concept, caching, ttl, eviction]
type: concept
status: complete
---

# TTL and Eviction Policies

## TTL (Time-to-Live)

How long an entry stays in the cache:
- `expireAfterWrite` — expires N time after the entry was written.
- `expireAfterAccess` — expires N time after the entry was last accessed.
- `expireVariable` — per-entry TTL (Java 21+).

## Eviction policies (when the cache is full)

### LRU (Least Recently Used)
Evict the entry that hasn't been accessed for the longest time. Simple, effective for most workloads.

### LFU (Least Frequently Used)
Evict the entry with the fewest accesses. Good for skewed access patterns (some entries accessed often, others rarely).

### ARC (Adaptive Replacement Cache)
Adjusts between LRU and LFU based on workload. Complex.

### FIFO (First In First Out)
Evict the oldest entry. Rarely good.

### Caffeine's W-TinyLFU
Caffeine uses W-TinyLFU — a hybrid that tracks frequency with a Count-Min Sketch. Near-optimal hit rate for most workloads.

## Caffeine configuration

```java
Cache<Long, Intern> cache = Caffeine.newBuilder()
    .maximumSize(10_000)                    // evict when size > 10000 (LRU)
    .expireAfterWrite(5, TimeUnit.MINUTES)  // TTL
    .expireAfterAccess(10, TimeUnit.MINUTES)
    .weakKeys()                              // GC can reclaim keys
    .recordStats()                           // for monitoring
    .build();
```

## Monitoring

```java
CacheStats stats = cache.stats();
System.out.println("Hit rate: " + stats.hitRate());
System.out.println("Evictions: " + stats.evictionCount());
System.out.println("Average load time: " + stats.averageLoadPenalty());
```

## Project Connection

For the intern cache:
- `maximumSize(1000)` — enough for active interns.
- `expireAfterWrite(5 min)` — safety net for staleness.
- `recordStats()` — monitor hit rate via Micrometer.

## Further reading

- Caffeine documentation — eviction policies.
