
## Executive summary

Database heuristics are rule-of-thumb strategies that DBMSs, query optimizers, and database administrators use to produce efficient query execution plans and to manage resources under uncertainty. Heuristics are fast, practical, and typically used either alone (heuristic-based optimizers) or together with cost-based methods to prune the search space and make optimization feasible in real time.

---

## Definitions

> [!DEFINITION] What is a "heuristic" in the database context?
> A heuristic is a practical rule or strategy (not guaranteed optimal) used to reduce search complexity, simplify transformations, or guide decisions (join order, index usage, partitioning, caching, resource allocation) so the system produces good execution plans quickly.

**Related terms**
- **Relational algebra equivalence rules:** Formal transformations (commutativity, associativity, distributivity) that justify many heuristics.
- **Cost-based optimization (CBO):** Uses statistical cost models to select plans.
- **Heuristic-based optimization (HBO):** Uses fixed rules or policies (the focus of this note).

---

## Why heuristics matter

- Exhaustive search for the optimal query plan is combinatorial and expensive.
- Heuristics reduce the plan search space and improve optimizer responsiveness.
- In many practical workloads, heuristics provide near-optimal plans with far lower overhead.
- They are essential when statistics are stale, incomplete, or unavailable.

---

# Heuristic categories (detailed)

Each category below contains: a concise definition, concrete heuristic rules, short examples, and implementation notes / tips.

---

## 1) Query optimization heuristics

**Definition:** Transformations applied to relational expressions to reduce intermediate result sizes or operator costs before physical planning.

**Common rules**
- Push selections (σ) down toward base relations (selection pushdown).
- Push projections (π) down to remove unused attributes early.
- Combine cascaded selections into one conjunctive condition.
- Replace `Cartesian product + selection` with `join` where predicate permits.
- Remove redundant operations (e.g., duplicate projections or identity joins).

**Example**
```text
σ_age>30 (Employee ⨝ Department)
→ (σ_age>30 Employee) ⨝ Department
````

**Implementation tips**

- Apply selection and projection pushdown as early passes in the logical optimizer.
    
- Maintain attribute lineage so projections do not remove columns needed later.
    
- Use syntactic checks to detect redundant operators.
    

---

## 2) Join order and join method heuristics

**Definition:** Heuristics to determine join ordering and which join algorithm to use (nested-loop, hash, merge).

**Common rules**

- Join the most selective or smallest relations first to reduce intermediate sizes.
    
- Use associative and commutative laws to reorder joins.
    
- Choose nested-loop join if one input is very small or indexed; choose hash join for large, unsorted equi-joins; choose merge join if inputs are already sorted on join keys.
    

**Example**

```text
If |A| << |B| << |C|, compute (A ⨝ B) first, then join with C.
```

**Implementation tips**

- Use heuristics to produce a small candidate set of join orders; apply cost model only to that set.
    
- Track estimated cardinalities to compare relative sizes; fall back to heuristics (e.g., assume uniform distribution) if stats are missing.
    
- For multiway joins consider greedy heuristics (pick best local join repeatedly) or dynamic programming within a bounded search size.
    

---

## 3) Index selection and usage heuristics

**Definition:** Rules that guide which indexes to create or use for queries given query patterns and update costs.

**Common rules**

- Prefer indexes on columns used in highly selective WHERE predicates.
    
- Use composite indexes when common query patterns filter or sort on the same column sequence.
    
- Avoid indexes on columns that are frequently updated if update overhead is high.
    
- Consider covering indexes for frequently-run queries to avoid lookups.
    

**Example**

- Create an index on `(user_id, created_at)` if many queries use `WHERE user_id = ? AND created_at > ?` and need ordered results.
    

**Implementation tips**

- Use workload profiling to identify candidate index columns.
    
- Estimate index maintenance cost vs query benefit; automate recommendations when possible.
    
- Consider partial indexes or filtered indexes for skewed data.
    

---

## 4) Data caching and buffer management heuristics

**Definition:** Strategies to keep frequently used pages, tuples, or intermediate results in memory to reduce I/O.

**Common rules**

- Use LRU, LFU, or adaptive replacement policies to evict less useful pages.
    
- Cache results of expensive subqueries or materialize intermediate results when reuse is likely.
    
- Pin hot pages or indices during high-intensity operations.
    

**Example**

- Cache aggregation results for the last 24 hours for repeated analytical queries.
    

**Implementation tips**

- Track access frequencies and recency metrics per page or result.
    
- Provide administrative knobs for cache size and eviction policy.
    
- Combine blocking vs non-blocking eviction policies depending on read/write mix.
    

---

## 5) Data partitioning heuristics

**Definition:** Rules for horizontal/vertical partitioning to improve locality, parallelism, and pruning.

**Common rules**

- Partition large tables by a frequently-filtered column (range, list, or hash partitioning).
    
- Use partition pruning to avoid scanning irrelevant partitions.
    
- Balance partition sizes to avoid hotspots; co-locate related partitions for multi-table queries.
    

**Example**

- Partition a `transactions` table by `transaction_date` (range) so queries for a date range touch fewer partitions.
    

**Implementation tips**

- Evaluate partitioning key selectivity and query patterns before applying partitioning.
    
- Monitor partition growth and rebalance if skew appears.
    
- For distributed DBs, align partitioning with placement (shard) strategy.
    

---

## 6) Concurrency control heuristics

**Definition:** Heuristics to choose locking, MVCC, or timestamp ordering strategies that minimize contention and maintain consistency.

**Common rules**

- Favor fine-grained locking for high concurrency reads; favor coarser locks if contention is low and overhead matters.
    
- Use MVCC to allow readers to proceed without blocking writers; tune retention of older versions.
    
- Prioritize short transactions or partitioned transactions to reduce lock hold times.
    
- Apply deadlock prevention heuristics (wait-die, wound-wait) or detection with timely resolution.
    

**Example**

- Apply optimistic concurrency for read-mostly workloads and pessimistic locking for high-write contention.
    

**Implementation tips**

- Track lock acquisition patterns and escalate or split locks adaptively.
    
- Tune MVCC garbage collection thresholds to balance storage vs concurrency.
    
- Use heuristics to time out or abort long-running transactions that block critical paths.
    

---

## 7) Resource allocation and scheduling heuristics

**Definition:** Rules to assign CPU, memory, and I/O bandwidth across queries and background tasks.

**Common rules**

- Allocate more memory to queries that sort or hash large inputs.
    
- Throttle or deprioritize heavy background jobs during peak hours.
    
- Batch small writes to amortize I/O overhead.
    

**Example**

- Reserve a memory pool for sorts and hashes; if demand exceeds pool size, spill by heuristic thresholds.
    

**Implementation tips**

- Instrument queries to estimate resource needs up-front (e.g., based on estimated cardinality).
    
- Implement workload classes (interactive, batch, ad-hoc) with separate resource quotas.
    
- Use admission control heuristics to deny or queue very expensive queries under heavy load.
    

---

## 8) Cost estimation heuristics

**Definition:** Fallback rules and approximations used when statistics are incomplete or stale.

**Common rules**

- Assume uniform distribution of values when no histograms are available.
    
- Use default selectivity constants for common predicates (e.g., equality ~1/10, inequality ~1/3) with configurable overrides.
    
- Use table cardinality hints or sampling-based estimates when full stats are absent.
    

**Example**

- If no histogram exists for column `status`, assume `selectivity(status = 'X') = 0.1` unless hinted otherwise.
    

**Implementation tips**

- Prefer lightweight sampling to obtain approximate histograms instead of relying solely on defaults.
    
- Make default heuristics configurable to reflect domain-specific distributions.
    
- Recompute or refresh statistics proactively for fast-changing tables.
    

---

## 9) Query rewriting and materialization heuristics

**Definition:** Heuristics that choose when to rewrite queries for equivalence or when to materialize subexpressions (materialized views / caches).

**Common rules**

- Rewrite correlated subqueries into joins when it results in more efficient plans.
    
- Materialize subexpressions expected to be reused multiple times.
    
- Use view merging and substitution heuristics to leverage existing materialized views.
    

**Example**

- Replace `EXISTS (SELECT 1 FROM B WHERE B.a = A.a)` with a semi-join when beneficial.
    

**Implementation tips**

- Track reuse frequency and materialization cost vs benefit.
    
- Use automatic materialized view selection heuristics based on query workload analysis.
    

---

## Algebraic equivalence rules (concise reference)

These formal rules justify many heuristics and are safe transformations if applied correctly:

- **Commutativity of join:** `A ⨝ B = B ⨝ A`
    
- **Associativity of join:** `(A ⨝ B) ⨝ C = A ⨝ (B ⨝ C)`
    
- **Selection pushdown:** `σ_p(A ⨝ B) = (σ_p(A) ⨝ B)` if predicate p references only A
    
- **Projection pushdown:** `π_L(A ⨝ B) = (π_{L_A}(A) ⨝ π_{L_B}(B))` when L_A and L_B are disjoint projections needed for join
    
- **Selection combination:** `σ_p(σ_q(R)) = σ_{p AND q}(R)`
    
- **Product-to-join rewrite:** `σ_joinCond(A × B) = A ⨝ B` when joinCond references both relations
    

---

## Heuristic checklist (for DBAs / optimizer engineers)

-  Push selections and projections down as early as possible.
    
-  Identify and remove redundant operators.
    
-  Reorder joins based on selectivity & sizes (join small, selective relations early).
    
-  Choose join algorithm by input size and data distribution.
    
-  Cache frequently used pages / results; use adaptive eviction policies.
    
-  Partition large tables by high-cardinality or common filter columns.
    
-  Use MVCC or appropriate concurrency heuristics for read-heavy workloads.
    
-  Tune resource pools and schedule background work for off-peak times.
    
-  Use sampling and light-weight stats when full statistics are expensive to compute.
    
-  Consider materialization for repeated subexpressions.
    

---

## Practical examples and patterns

- **Online transactional systems (OLTP):** Favor MVCC, fine-grained locks, indexes on foreign keys, and short transaction heuristics.
    
- **Analytical workloads (OLAP):** Favor partitioning by time, caching aggregated results, wide scans with vectorized execution, and hash/merge joins.
    
- **Mixed workloads:** Use workload classes, admission control, and dynamic resource allocation heuristics.
    

---

## Limitations and pitfalls

- Heuristics can be suboptimal for corner cases and skewed distributions.
    
- Over-aggressive indexing increases write overhead.
    
- Poorly chosen partition keys create hotspots instead of improvements.
    
- Stale statistics undermine cost-model and heuristic decisions; maintain statistics pipelines.
    

---
