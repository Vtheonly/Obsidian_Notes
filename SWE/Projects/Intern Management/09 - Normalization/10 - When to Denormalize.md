---
tags: [concept, database, normalization, denormalization, pattern]
type: concept
status: complete
prerequisites:
  - [[09 - Normalization/03 - Denormalization]]
related:
  - [[12 - Advanced Database Features/06 - Materialized Views]]
  - [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]]
---

# When to Denormalize

## What it is

A **decision framework** for introducing redundancy. Denormalization is the exception, not the rule. The default is 3NF/BCNF; denormalize only when you can show a measurable benefit and a plan to keep the redundant data consistent.

## The decision tree

```
1. Is the schema in 3NF? If no, normalize first. Denormalizing a
   poorly-normalized schema just adds more bugs.

2. Have you measured the slow query with EXPLAIN PLAN? If no, measure
   before optimizing. See [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]].

3. Have you tried indexing? Often the right index fixes the query
   without any denormalization. See [[11 - DB Performance and Indexing/02 - B-tree Indexes]].

4. Have you tried a covering index? A composite index that includes
   all the query's columns can avoid the table lookup entirely.

5. Have you tried query rewriting? Sometimes the JOIN can be re-ordered
   or rewritten to be cheap.

6. Have you tried a materialized view? MVs give you denormalization
   without application-level maintenance.

7. If all the above failed: denormalize. Pick the smallest, most stable
   column to copy. Add a trigger or application-level hook to keep it
   in sync. Document the invariant.
```

## When to denormalize

- **Read-to-write ratio is 100:1 or higher**. A dashboard queried 10k times/sec with 1 write/sec - denormalize the aggregates.
- **The denormalized column is stable**. Copying `country_name` next to `country_code` is safe because country names change once a decade. Copying `user_email` is dangerous because emails change weekly.
- **The query is on the critical path** and a join adds measurable latency (say, >50ms) that you cannot eliminate any other way.
- **The denormalization enables a covering index**. Storing `department_name` on `intern` lets a single index satisfy the entire list query.

## When NOT to denormalize

- **OLTP workloads with frequent updates** - the maintenance cost exceeds the read savings.
- **Columns that change often** - you'll spend more time keeping the copy in sync than you save on reads.
- **Before measuring** - premature denormalization is a tax you pay forever.
- **When a materialized view would work** - MVs are denormalization with built-in maintenance.
- **When the schema is not yet normalized** - denormalizing a 1NF schema just adds more redundancy on top of redundancy.

## Maintenance strategies

If you do denormalize, pick one and stick to it:

1. **Application-level maintenance** - every code path that changes the source also updates the copy. Brittle; one missed path and the data drifts.
2. **Trigger-based maintenance** - a `BEFORE INSERT OR UPDATE` trigger keeps the copy in sync. Centralized, but triggers are invisible to application developers and can surprise them.
3. **Materialized view** - Oracle maintains the copy. Safest; costs a slightly slower commit. See [[12 - Advanced Database Features/06 - Materialized Views]].
4. **Async refresh** - a job (DBMS_SCHEDULER) refreshes the copy every N minutes. Acceptable for dashboards where "stale by 5 minutes" is fine.

## Project Connection

The project has **no denormalization at all** and **no joins to compensate**. The result is the N+1 query: every intern row triggers a separate `getNameById` call to fetch the department name. The reviews propose either:

- A JOIN (no denormalization, single round-trip) - preferred.
- A materialized view with `FAST REFRESH ON COMMIT` - if the read load justifies it.

Neither is implemented; the N+1 stays. See [[11 - DB Performance and Indexing/20 - The N+1 Query Problem]].

## Common pitfalls

- Denormalizing the wrong column - one that changes often, costing more in maintenance than it saves in reads.
- Denormalizing without a maintenance plan - the copy drifts, and you find out months later when a report doesn't reconcile.
- Denormalizing before checking that an index would have fixed the query.
- Skipping the UNIQUE constraint on the natural key when you add a surrogate - you lose the ability to detect duplicate inserts.

## Trade-offs

- Read speed vs write cost - denormalization shifts cost from reads to writes.
- Simplicity vs consistency - denormalized data is easier to query but harder to keep correct.
- Storage vs compute - denormalization uses more disk to save CPU.

## Further reading

- [[09 - Normalization/03 - Denormalization]]
- [[12 - Advanced Database Features/06 - Materialized Views]]
- [[11 - DB Performance and Indexing/11 - EXPLAIN Plan]]
