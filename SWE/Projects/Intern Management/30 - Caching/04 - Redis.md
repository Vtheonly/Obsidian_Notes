---
tags: [concept, caching, redis, distributed]
type: concept
status: complete
related:
  - [[11 - DB Performance and Indexing/06 - Caffeine Cache]]
---

# Redis

## What it is

**Redis** (Remote Dictionary Server) is an in-memory key-value store. Used as a distributed cache, session store, message queue, and more.

## Why Redis (vs Caffeine)

- **Distributed** — multiple app instances share the cache.
- **Persistent** — data survives restarts (with AOF/RDB).
- **Rich data types** — strings, lists, sets, sorted sets, hashes, streams.
- **Pub/Sub** — real-time messaging.

For a single-instance desktop app, Caffeine is sufficient. For a multi-instance server, Redis.

## Usage (Java with Lettuce)

```java
RedisClient client = RedisClient.create("redis://localhost:6379");
StatefulRedisConnection<String, String> conn = client.connect();
RedisCommands<String, String> sync = conn.sync();

sync.set("intern:123", "Alice");
String name = sync.get("intern:123");

sync.expire("intern:123", 300);  // TTL 5 min
```

## Spring Cache with Redis

```java
@Cacheable(value = "interns", key = "#id")
public Intern findById(long id) { ... }
```

Spring auto-configures Redis as the cache provider.

## Use cases

- **Session storage** — share sessions across instances.
- **Rate limiting** — Bucket4j with Redis for distributed rate limiting.
- **Leaderboards** — sorted sets.
- **Real-time analytics** — counters, hyperloglog.
- **Message queue** — Redis Streams, List, Pub/Sub.

## Project Connection

For the desktop app, Redis is overkill. If the app evolves to a server, Redis for sessions and shared cache.

## Further reading

- Redis documentation (redis.io).
