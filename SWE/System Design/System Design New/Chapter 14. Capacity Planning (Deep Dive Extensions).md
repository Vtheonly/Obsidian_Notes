---
title: Chapter 14. Capacity Planning (Deep Dive Extensions)
course: System Design
chapter: 14
tags: [system-design, capacity-planning, estimation, cost-modeling, traffic-spikes]
---

# Chapter 14. Capacity Planning (Deep Dive Extensions)

> [!abstract] Chapter Goal
> Chapter 1 introduced back-of-the-envelope estimation and the basic latency numbers. This chapter extends those foundations with the techniques used in **real capacity planning**: read/write ratios and their impact on database sizing, multi-region capacity math, cost-per-request modeling, traffic spike planning (Black Friday, viral moments), the 80/20 rule for cache sizing, headroom and N+M redundancy math, and how to translate forecasts into actual procurement decisions.

## 1. Why This Chapter Exists

Chapter 1 gave you the *first-order* estimate: QPS, bandwidth, storage, memory, server count. That's enough for a system design interview. Real capacity planning goes deeper:

- **What's the read/write ratio?** A 100:1 read-heavy system needs different infrastructure than a 1:1 system.
- **What about multi-region?** Replication overhead, cross-region bandwidth.
- **What does it cost?** A design that "works" but costs $100k/month is a failed design.
- **What about traffic spikes?** Black Friday can 10× normal traffic.
- **What about cache sizing?** The 80/20 rule tells you how much to cache.
- **What about redundancy?** N+1, N+2, N+M — how much extra capacity?

This chapter answers all of these.

## 2. The Read/Write Ratio

The single most overlooked factor in capacity planning is the **read/write ratio**. It shapes every architectural decision.

### 2.1. Why It Matters

- **Reads** are easy to scale: add more replicas, cache aggressively.
- **Writes** are hard to scale: most databases have a single primary; replicas don't help with writes.

A 100:1 read-heavy system can be scaled cheaply with read replicas and caching. A 1:1 write-heavy system needs sharding, partitioning, and careful design.

### 2.2. Typical Ratios by Application Type

| Application | Read : Write | Notes |
|-------------|--------------|-------|
| Social media feed (read) | 1000 : 1 | Scrolling feeds is all reads |
| Social media (post) | 1 : 1 | Each post creates a write; reads still dominate overall |
| News site | 10000 : 1 | Few articles published; many readers |
| E-commerce browse | 100 : 1 | Many product views; few add-to-cart |
| E-commerce checkout | 1 : 1 | Cart → order is write-heavy |
| Banking (transaction) | 1 : 10 | Every transfer is two writes (debit + credit) |
| Telemetry / IoT | 1 : 100 | Sensors stream writes constantly |
| Chat (active user) | 1 : 5 | Each message = 1 write + delivery to N recipients |
| Search engine | 1000000 : 1 | Billions of queries; crawlers do the writes |

### 2.3. Sizing Implications

For a 1000 : 1 read-heavy system:
- 1 primary handles all writes.
- 10 read replicas handle reads.
- Cache hit ratio of 95 % reduces DB reads by 20×.
- Effective DB load: writes + reads/(20 × 10) = writes + reads/200 ≈ writes.

For a 1 : 1 write-heavy system:
- 1 primary handles all writes (the bottleneck).
- Read replicas don't help.
- Caching doesn't help (every write is unique).
- You must shard the database to scale writes.

### 2.4. Computing the Ratio for Your System

Walk through your user journeys and count:

```
Journey: User opens app, scrolls feed for 30 seconds, likes 2 posts
- App open: 1 read (user profile)
- Feed load: 1 read (feed items)
- Scroll pagination: 5 reads (additional pages)
- Like post 1: 1 write (like) + 1 read (post existence check)
- Like post 2: 1 write + 1 read

Total per journey: 8 reads + 2 writes = 4:1 ratio
```

Multiply by the number of journeys per user per day to get the system-wide ratio.

## 3. The 80/20 Rule for Cache Sizing

Also known as the **Pareto Principle**: 80 % of traffic comes from 20 % of data. In caching terms, caching the hottest 20 % of items serves 80 % of requests.

### 3.1. Applying It

If you have 100 million items in your database:
- Cache the top 20 million (20 %) — these see 80 % of the traffic.
- For 80 million items (80 %), cache misses are common but they're only 20 % of traffic.

This gives a target cache size: **20 % of your active data set**.

### 3.2. Adjustments

The 80/20 rule is a starting point. Adjust based on your actual skew:

- **More skewed (90/10)**: common for viral content, hot products. Cache less, hit ratio higher.
- **Less skewed (60/40)**: long-tail content (e.g., a marketplace with no dominant sellers). Cache more, hit ratio lower.
- **Uniform**: random access patterns. Cache doesn't help much; consider direct DB access.

### 3.3. Computing Cache Memory

Example: 100M users, each cached profile is 2 KB. The active 20 % is 20M users × 2 KB = 40 GB.

If you use Redis with 70 % utilization (leave headroom), you need 60 GB of RAM. Two 32 GB Redis instances in primary-replica = 64 GB usable.

### 3.4. The Working Set vs the Total Set

The **working set** is the data accessed in a recent window (e.g., the last hour). The total set is everything in the database.

Cache the working set, not the total set. If your working set is 1 % of the total (common for time-series data), your cache is 100× smaller than naive estimation suggests.

## 4. Multi-Region Capacity Math

Running in multiple regions adds overhead that's easy to underestimate.

### 4.1. Replication Overhead

If you replicate from Region A to Region B:
- Each write in A generates network traffic to B.
- B's database must process the replication stream.
- Replication lag accumulates if B can't keep up.

**Bandwidth cost**: for a system with 10k writes/sec at 1 KB each = 10 MB/s = 80 Mbps per region pair. With 3 regions (A→B, A→C, B→A, B→C, C→A, C→B), that's 6× = 480 Mbps total.

### 4.2. Cross-Region Bandwidth Costs

AWS cross-region data transfer is **expensive**:
- $0.02/GB for same-region (us-east-1 to us-east-1).
- $0.02/GB egress + $0.01/GB ingress = $0.03/GB cross-region (us-east-1 to eu-west-1).

For 1 TB/day of replication, that's $30/day × 30 = $900/month per region pair. With 4 regions, ~$5,400/month just for replication traffic.

### 4.3. Multi-Region Active-Active

In active-active, both regions accept writes. This requires:
- **Conflict resolution**: when the same record is updated in both regions, who wins? Last-write-wins? CRDTs? Application logic?
- **Causal consistency**: maintain ordering of causally-related writes across regions.
- **Higher write latency**: each write must be replicated before considering it "safe" (if you want strong consistency).

Capacity implications:
- Each region must handle the **full** write load (since either can become the sole survivor of a failover).
- Network bandwidth doubles (writes flow both ways).

### 4.4. Multi-Region Active-Passive

In active-passive:
- Active region handles all traffic.
- Passive region sits idle but ready.
- Replication is one-way (active → passive).

Capacity: each region must handle the full load. The passive region's capacity is "wasted" until failover, but you need it for disaster recovery.

## 5. Cost Modeling

A design that works technically but is too expensive is a failed design. Always model the cost.

### 5.1. Cost Components

| Component | Cost Driver | AWS Example Pricing (2024) |
|------------|-------------|---------------------------|
| Compute | Instance-hours | $0.05–$5/hour depending on size |
| Memory (cache) | GB-hours | Redis: $0.034/GB-hour |
| Storage (SSD) | GB-month | EBS: $0.10/GB-month |
| Storage (object) | GB-month + requests | S3: $0.023/GB-month, $0.0004 per 1k GETs |
| Network (egress) | GB out | $0.09/GB to internet |
| Network (cross-region) | GB transfer | $0.02/GB |
| Managed services | varies | RDS: ~2× self-managed cost |
| Load balancers | LCU-hours | ALB: $0.0225/hour + $0.008/LCU-hour |

### 5.2. Cost Per Request

For any service, compute:

```
cost_per_request = total_monthly_cost / total_monthly_requests
```

If your service costs $10,000/month and serves 100M requests:
```
cost_per_request = $10,000 / 100,000,000 = $0.0001 per request = $0.10 per 1,000 requests
```

Compare this to your revenue per request. If you make $0.01 per request, your 10× margin is healthy. If you make $0.0001 per request, you're break-even — and a traffic spike will lose money.

### 5.3. Total Cost of Ownership (TCO)

TCO includes:
- Infrastructure (compute, storage, network).
- Software licenses (Oracle, commercial DBs).
- Operations team salaries.
- On-call burden (more components = more on-call).
- Compliance and audit costs.

A self-managed PostgreSQL on EC2 looks cheaper than RDS until you add the salary of the DBA who has to manage it. For small teams, managed services are usually the right call.

### 5.4. Right-Sizing

Most production systems are **over-provisioned by 2–3×** because:
- Engineers round up ("let's get the bigger instance, just in case").
- Auto-scaling is feared ("what if it doesn't scale fast enough?").
- The cost is borne by a different team than the engineers.

Right-sizing means picking the instance size that handles **peak load at 60–70 % utilization**, not 30 %. Implement auto-scaling to handle the rare spike.

## 6. Traffic Spike Planning

Some systems see predictable spikes (Black Friday, Super Bowl, tax deadline). Others see unpredictable spikes (viral content, marketing push). Capacity planning must handle both.

### 6.1. Predictable Spikes

For predictable spikes:
- **Pre-warm capacity** before the event. Scale up auto-scaling groups 1 hour before.
- **Cache aggressively**. Pre-warm the cache with hot content.
- **Test at 2× expected spike**. If you expect 5× normal traffic, test at 10×.
- **Have a degradation plan**: if you can't serve everyone, who gets priority? (Existing customers > new signups; checkout > browsing.)

### 6.2. Unpredictable Spikes

For unpredictable spikes:
- **Auto-scale aggressively**: smaller scaling steps, faster cooldowns.
- **Use serverless for burst capacity**: Lambda, Cloud Run, Fargate can absorb spikes that would overwhelm fixed instances.
- **Rate-limit early**: better to reject some users with 429 than to take down the whole system.
- **Queue excess work**: for write-heavy spikes, accept requests into a queue and process them later.

### 6.3. The Spike Multiplier

A common rule: provision for **3× average traffic** at all times. This handles:
- 2× spikes (viral content, marketing).
- 1.5× the remaining capacity for failover (if one instance dies, others absorb its load).
- Combined: 2× × 1.5× = 3× average.

If your average is 1,000 QPS, provision for 3,000 QPS. This costs 3× what the average would, but it's the price of availability.

### 6.4. Thundershadow and Thundering Herd

- **Thundering herd**: a cache expiry causes all clients to hit the database simultaneously. Solved with request coalescing (Chapter 5).
- **Thundershadow**: a deployment or restart causes all instances to come online simultaneously, hammering downstream services with cold-cache requests. Solved with gradual rollouts and warm-up periods.

## 7. Headroom and N+M Redundancy

### 7.1. The Headroom Rule

Always run with **30 % headroom**: if your service can handle 1,000 QPS and you're hitting 700 QPS at peak, you have 30 % headroom. Below 30 %, you're one traffic spike away from an outage.

The math: at 70 % utilization, a 50 % traffic spike takes you to 105 % (overload). At 60 % utilization, a 50 % spike takes you to 90 % (uncomfortable but OK).

### 7.2. N+1 Redundancy

For high availability, you need at least N+1 instances:
- N instances handle peak load.
- 1 spare handles the failure of any single instance.

If peak load is 6 instances, run 7. If one dies, the remaining 6 still handle peak load.

### 7.3. N+2 Redundancy

For maintenance windows, you need N+2:
- N for peak load.
- 1 for failure.
- 1 to take offline for deploys.

With N+1, taking one instance offline for a deploy leaves you with N — exactly enough for peak, no room for failure. N+2 lets you deploy safely.

### 7.4. N+M for Rolling Deploys

For larger fleets, define M = the number of instances you take offline simultaneously during a rolling deploy. If you do "one at a time" deploys, M=1. If you do "10 % at a time" canary deploys on a 100-instance fleet, M=10. Provision N+M.

### 7.5. Cross-AZ Headroom

If you run across 3 AZs and one AZ fails, you lose 1/3 of capacity. To survive an AZ failure, each AZ must be able to handle 50 % of traffic (because 2 AZs share 100 %). This means **each AZ is provisioned for 50 % of peak** — total provisioned = 150 % of peak, a 50 % overhead just for AZ redundancy.

## 8. Forecasting Demand

Capacity planning is fundamentally about predicting the future. Techniques:

### 8.1. Linear Extrapolation

If traffic grows 5 % per month, next year = 1.05^12 = 1.80× = 80 % growth. Plan for 2× to be safe.

### 8.2. Seasonal Decomposition

Some businesses have strong seasonality:
- E-commerce peaks in November-December.
- Tax software peaks in April.
- Travel peaks in summer.

Decompose historical data into trend + seasonality + noise. Forecast each separately, then combine.

### 8.3. Scenario Planning

Define multiple scenarios:
- **Conservative**: 20 % growth next year.
- **Base**: 50 % growth.
- **Aggressive**: 2× growth (successful product launch).
- **Black swan**: 5× growth (viral adoption).

Plan capacity for the **aggressive** scenario, but pay-as-you-go so you only pay for what you use.

### 8.4. Lead Times

Procurement has lead times:
- AWS EC2 instances: minutes (instant).
- Reserved Instances: hours (commitment).
- Physical hardware: weeks to months.
- Cross-region capacity reservations: days.

If you provision on-demand cloud, lead time is short. If you use physical hardware or reserved capacity, plan 3–6 months ahead.

## 9. Worked Example: Full Capacity Plan

Let's design a capacity plan for a hypothetical "social media app" with 10 million DAU.

### 9.1. Assumptions

- 10M DAU.
- Average session: 5 minutes, 50 API calls.
- Read:write ratio = 100:1.
- Payload: 2 KB average.
- 80/20 caching rule.
- Multi-region (2 regions, active-passive).
- 99.9 % availability target (8.76 hours downtime/year).

### 9.2. QPS Calculation

- Daily requests = 10M × 50 = 500M.
- Average QPS = 500M / 86400 ≈ 5,800 QPS.
- Peak QPS (3× average) = 17,400 QPS.
- Writes (1 %) = 174 writes/sec peak.
- Reads (99 %) = 17,226 reads/sec peak.

### 9.3. Cache Sizing

- Active users in last hour = ~2M (rolling).
- Average user profile + recent posts = 10 KB cached.
- Working set = 2M × 10 KB = 20 GB.
- With 80/20 cache ratio: cache 20 % = 4 GB.
- Add 70 % headroom + Redis overhead = ~10 GB RAM.
- 2× 16 GB Redis instances (primary + replica) = 32 GB total, 16 GB usable per node.

Expected hit ratio: 90 % (since we cache the working set).
DB read load after cache: 17,226 × 10 % = 1,723 reads/sec.

### 9.4. Database Sizing

- Writes: 174/sec → 1 primary handles this easily.
- Reads: 1,723/sec → 5 read replicas (350 reads/sec each).
- Storage: 174 writes/sec × 1 KB × 86,400 sec/day × 365 days × 5 years = 27 TB.
- With replication (3×) and indexes (1.5×) = 120 TB total storage.

### 9.5. App Server Sizing

- Each app server handles 2,000 QPS.
- Peak QPS = 17,400.
- Base = 9 instances.
- N+2 redundancy = 11 instances.
- 30 % headroom = 14 instances.
- Cross-AZ overhead (50 %) = 21 instances per region.
- 2 regions (active-passive) = 42 instances total.

### 9.6. Bandwidth

- 17,400 QPS × 2 KB = 35 MB/s = 280 Mbps at peak.
- Cross-region replication: 174 writes/sec × 1 KB = 0.17 MB/s = 1.4 Mbps. Negligible.

### 9.7. Cost Estimate (Monthly)

| Component | Quantity | Unit Cost | Monthly |
|-----------|----------|-----------|---------|
| App servers (m5.large) | 42 | $70 | $2,940 |
| DB primary (r5.2xlarge) | 2 (regions) | $1,000 | $2,000 |
| DB read replicas | 10 (5 per region) | $500 | $5,000 |
| Redis (cache.r6.large) | 4 (2 per region) | $250 | $1,000 |
| Storage (EBS + S3) | 120 TB | $0.10/GB | $12,000 |
| Network egress | 10 TB | $0.09/GB | $900 |
| Load balancers (ALB) | 2 | $200 | $400 |
| **Total** | | | **~$24,240/month** |

Cost per DAU: $24,240 / 10M = $0.0024 per user per month. Very healthy.

### 9.8. Validation

- QPS: 17,400 peak. App capacity: 42 × 2,000 = 84,000 QPS. 5× headroom. ✅
- Storage: 27 TB/year × 5 years = 135 TB provisioned. ✅
- Availability: Multi-AZ + multi-region, automated failover. Target 99.9 %. ✅

## 10. Tips, Tricks, and Common Pitfalls

> [!tip] Track Cost Per User
> Normalize cost by active users. If cost/user is rising over time, your efficiency is degrading. If it's falling, you're scaling well.

> [!warning] Don't Forget Cross-Region Bandwidth
> Cross-region data transfer is one of the biggest surprises on cloud bills. Replication, backups, and CDN origin fetches all add up. Model it explicitly.

> [!tip] Use Reserved Instances for Steady-State
> If you know you'll need 20 instances for the next year, buy Reserved Instances (or Savings Plans). They're 30–70 % cheaper than on-demand. Use on-demand only for spikes.

> [!warning] Don't Scale on Average Utilization
> Auto-scaling on average CPU causes flapping. Scale on a 5-minute rolling average, with a cooldown period, and scale on multiple metrics (CPU + latency + queue depth).

> [!tip] Pre-Warm Before Predictable Spikes
> For Black Friday, product launches, or marketing pushes, pre-warm capacity at least 1 hour before. Auto-scaling takes minutes; pre-warming takes seconds.

> [!warning] Don't Forget Connection Limits
> A database might handle 10k QPS but only allow 1,000 concurrent connections. Each app server opens 10 connections, so 100 app servers max out the DB connection pool even though CPU is fine. Use connection pooling (PgBouncer, RDS Proxy).

> [!tip] Model Failure Scenarios
> Capacity isn't just about normal traffic. Model: what happens if one AZ dies? If the cache fails? If a downstream dependency is slow? Each scenario should be survivable.

## 11. Chapter Summary

- The read/write ratio shapes architecture: read-heavy systems scale with replicas and caching; write-heavy systems need sharding.
- The 80/20 rule: cache 20 % of data to serve 80 % of traffic. Adjust based on actual skew.
- Multi-region adds 50–100 % overhead: cross-region replication bandwidth, idle standby capacity.
- Always compute cost per request and compare to revenue per request.
- Provision for 3× average traffic to handle spikes and failover.
- Run with 30 % headroom; use N+1 for HA, N+2 for maintenance, N+M for rolling deploys.
- Cross-AZ redundancy requires 50 % extra capacity (each AZ must handle 50 % of traffic).
- Forecast demand with linear extrapolation, seasonal decomposition, and scenario planning.
- Use Reserved Instances for steady-state, on-demand for spikes.

The next four chapters (15–18) are case studies that apply all the patterns from this book to specific domains: geospatial systems, news feeds, real-time chat, and video processing.
