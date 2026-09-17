# Comparison — Web Frameworks

> [!abstract] Framework Head-to-Head
> A comparison of the four web frameworks benchmarked in the 1M RPS project, from the simplest Node.js framework to a high-performance C++ framework.

---

## Frameworks Compared

- [[7.3 Express Framework]] — The industry-standard Node.js web framework
- [[7.4 Fastify Framework]] — A modern, schema-based Node.js framework focused on speed
- [[7.5 Custom Framework (CP)]] — A minimal custom Node.js framework built for performance
- [[8.2 Drogon Framework]] — A high-performance C++ web framework

---

## Performance Comparison

| Metric | Express | Fastify | CP (Custom) | Drogon (C++) |
|--------|---------|---------|-------------|--------------|
| **Simple Route RPS** | ~18,000 | ~66,000 | ~73,000 | ~1,000,000+ |
| **Complex Route RPS** | Lower | Moderate | Moderate | Very High |
| **Relative to Express** | 1x | ~3.7x | ~4x | ~55x |
| **Language** | JavaScript (Node.js) | JavaScript (Node.js) | JavaScript (Node.js) | C++ |
| **Runtime** | V8 | V8 | V8 | Native compiled |
| **Memory per Request** | Higher | Moderate | Lower | Lowest |
| **Startup Time** | Fast | Fast | Fast | Slower (compilation) |
| **JSON Parsing** | Built-in (slow) | Built-in (faster) | Custom (optimized) | RapidJSON (fastest) |

---

## Feature Comparison

| Feature | Express | Fastify | CP (Custom) | Drogon (C++) |
|---------|---------|---------|-------------|--------------|
| **Routing** | Full-featured | Full-featured | Minimal | Full-featured |
| **Middleware Ecosystem** | Massive | Large | None | Growing |
| **Schema Validation** | Via plugins | Built-in | None | Built-in |
| **TypeScript Support** | Excellent | Excellent | Manual | C++ native |
| **Database ORM Support** | Extensive | Good | None | Limited |
| **Community & Docs** | Largest | Large | N/A | Moderate |
| **Learning Curve** | Low | Low | N/A (custom) | High |
| **Production Readiness** | Battle-tested | Battle-tested | Experimental | Production-ready |
| **Debugging** | Easy | Easy | Hard | Harder (C++ tools) |

---

## When to Use Each

### Express — [[7.3 Express Framework]]
> [!success] Best for: Rapid development, maximum ecosystem, teams with JS experience

- You need to ship quickly with minimum risk
- Your RPS requirements are under 50K
- You rely heavily on npm middleware packages
- Your team is primarily JavaScript/TypeScript developers
- Ecosystem support and community answers matter more than raw speed

### Fastify — [[7.4 Fastify Framework]]
> [!success] Best for: Performance-conscious Node.js projects needing balance of speed and features

- You want 3-4x the RPS of Express with minimal code changes
- You value built-in schema validation and type safety
- You need a modern async/await-first framework
- Your RPS target is 50K–200K per instance
- You want a production-ready framework with good plugin ecosystem

### CP (Custom Framework) — [[7.5 Custom Framework (CP)]]
> [!success] Best for: Learning how frameworks work, squeezing every drop from Node.js

- You want to understand what makes frameworks slow
- You're building a highly specialized API with minimal features
- Every millisecond of overhead matters
- You don't need middleware, validation, or plugins
- Educational purposes — understanding the cost of abstractions

### Drogon (C++) — [[8.2 Drogon Framework]]
> [!success] Best for: Extreme performance requirements, 1M+ RPS targets

- You need 500K–1M+ RPS per instance
- You can afford the development time and C++ expertise
- Memory efficiency is critical
- You're building infrastructure-level services
- The cost of developer time is justified by reduced infrastructure costs
- You need to maximize hardware utilization (see [[13.3 Instance Types]])

---

## Key Takeaways

1. **Framework choice matters less than language choice.** Moving from Express to Drogon is a ~55x improvement, while Express → Fastify is only ~3.7x.
2. **Abstractions have a cost.** Express's middleware chain, routing, and convenience features come at a 4x performance penalty vs. a minimal custom framework.
3. **JSON parsing is a major bottleneck.** Switching from Node's built-in `JSON.parse` to RapidJSON in C++ is a significant factor in Drogon's performance.
4. **See [[7.6 Framework Benchmarking Results]]** for the full benchmark data and methodology.
5. **See [[8.4 Language Performance Comparison]]** for how different languages compare beyond just frameworks.

---

## Related

- [[MOCs/Comparison - Languages]] — Language-level comparison
- [[MOCs/Video Journey - From 18K to 6M RPS]] — How benchmarks evolved through the video
- [[MOCs/Comparison - Database Strategies]] — Database scaling comparisons