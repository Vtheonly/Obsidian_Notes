# Welcome and Start Here

> [!quote] Welcome to the 1 Million RPS Knowledge Vault
> This Obsidian vault contains **85 detailed notes** extracted from a deep-dive video on building systems that handle 1 million requests per second. It covers everything from first principles (CPU cores, TCP connections) to advanced architecture (sharding, VPCs, real-world 1M RPS systems).

---

## What Is This Vault?

This vault decomposes a comprehensive technical video about achieving million-RPS throughput into organized, interconnected notes. It covers:

- **Computer architecture** — CPUs, memory, network cards, and why hardware matters
- **Networking** — TCP, HTTP, JSON, latency, and bandwidth
- **Operating systems** — Processes, threads, race conditions, and Linux
- **Benchmarking** — How to measure RPS reliably with Autocannon
- **Algorithms** — Big O notation and why O(log n) vs O(n) matters at scale
- **Node.js development** — Express, Fastify, and custom frameworks
- **High-performance languages** — C++, Drogon, RapidJSON
- **Databases** — PostgreSQL, Redis, indexing, IOPS, and connection pooling
- **Scaling** — Vertical scaling, read replicas, sharding, caching, clustering
- **Cloud & infrastructure** — AWS, EC2, load balancing, CDNs, VPCs
- **Bottleneck analysis** — Systematic diagnosis of CPU, network, memory, and disk limits
- **Cost engineering** — Cloud pricing, TCO, reserved vs on-demand
- **Real-world architecture** — Putting it all together for production systems

---

## Where to Start

> [!tip] Recommended Starting Point
> **[[MOCs/Learning Roadmap]]** — This is your main guide. It contains a tiered learning order, a mindmap of all chapters, estimated study hours, and quick-start paths based on your background.

### Quick Navigation

| If you want to... | Go to... |
|-------------------|----------|
| Follow a structured learning path | [[MOCs/Learning Roadmap]] |
| Browse all notes by chapter | [[MOCs/Main Map of Content]] |
| Understand how concepts connect | [[MOCs/Concept Relationship Map]] |
| Compare web frameworks | [[MOCs/Comparison - Frameworks]] |
| Compare programming languages | [[MOCs/Comparison - Languages]] |
| Choose a database scaling strategy | [[MOCs/Comparison - Database Strategies]] |
| Diagnose a performance problem | [[MOCs/Bottleneck Identification Guide]] |
| Follow the video's story from 18K to 6M RPS | [[MOCs/Video Journey - From 18K to 6M RPS]] |

---

## Folder Structure

```
1-Million-RPS-Knowledge-Vault/
├── 00 - Welcome and Start Here.md        ← You are here
├── MOCs/
│   ├── Learning Roadmap.md               ← Recommended learning order
│   ├── Main Map of Content.md            ← Index of all 85 notes
│   ├── Concept Relationship Map.md       ← How concepts connect (Mermaid graph)
│   ├── Comparison - Frameworks.md        ← Express vs Fastify vs CP vs Drogon
│   ├── Comparison - Languages.md         ← Node.js vs C++ vs Go vs Rust...
│   ├── Comparison - Database Strategies.md ← Vertical vs Sharding vs Caching
│   ├── Bottleneck Identification Guide.md ← Decision tree for diagnosis
│   └── Video Journey - From 18K to 6M RPS.md ← The narrative journey
├── Chapter 1. Introduction to High-Scale Systems/
│   ├── 1.1 What Does 1 Million Requests Per Second Mean.md
│   ├── 1.2 Real-World Examples at Million RPS Scale.md
│   ├── 1.3 The Engineering Mindset at Scale.md
│   └── 1.4 Cost of Operating at Scale.md
├── Chapter 2. Computer Architecture Fundamentals/
│   ├── 2.1 CPU Cores and Threads.md
│   ├── 2.2 Core Utilization.md
│   ├── 2.3 CPU Utilization Methods.md
│   ├── 2.4 RAM vs Disk vs Network Speeds.md
│   ├── 2.5 Bits, Bytes, and Data Units.md
│   └── 2.6 Network Cards and Bandwidth.md
├── Chapter 3. Networking Fundamentals/
│   ├── 3.1 TCP Connections.md
│   ├── 3.2 HTTP Protocol.md
│   ├── 3.3 HTTP Methods.md
│   ├── 3.4 HTTP Status Codes.md
│   ├── 3.5 JSON Data Format.md
│   └── 3.6 Network Latency and Bandwidth.md
├── Chapter 4. Operating System Concepts/
│   ├── 4.1 Processes and Threads.md
│   ├── 4.2 Multi-Threading.md
│   ├── 4.3 Race Conditions.md
│   ├── 4.4 Semaphores and Synchronization.md
│   ├── 4.5 SSH (Secure Shell).md
│   └── 4.6 Unix and Linux Terminal Commands.md
├── Chapter 5. Performance and Benchmarking/
│   ├── 5.1 Requests Per Second (RPS).md
│   ├── 5.2 Autocannon.md
│   ├── 5.3 Benchmarking Methodology.md
│   ├── 5.4 Connections, Pipelining, and Workers.md
│   ├── 5.5 Percentiles in Benchmarking.md
│   └── 5.6 Resource Monitoring.md
├── Chapter 6. Big O Notation and Algorithms/
│   ├── 6.1 Big O Notation.md
│   ├── 6.2 O(n) Linear Time.md
│   ├── 6.3 O(log n) Logarithmic Time.md
│   ├── 6.4 O(1) Constant Time.md
│   ├── 6.5 Database Query Complexity.md
│   └── 6.6 Why Algorithms Matter at Scale.md
├── Chapter 7. Backend Development with Node.js/
│   ├── 7.1 What is Node.js.md
│   ├── 7.2 The Event Loop.md
│   ├── 7.3 Express Framework.md
│   ├── 7.4 Fastify Framework.md
│   ├── 7.5 Custom Framework (CP).md
│   └── 7.6 Framework Benchmarking Results.md
├── Chapter 8. High-Performance Languages/
│   ├── 8.1 C++ for High Performance.md
│   ├── 8.2 Drogon Framework.md
│   ├── 8.3 RapidJSON.md
│   ├── 8.4 Language Performance Comparison.md
│   └── 8.5 Memory Management.md
├── Chapter 9. Database Fundamentals/
│   ├── 9.1 What is a Database.md
│   ├── 9.2 SQL Basics.md
│   ├── 9.3 PostgreSQL.md
│   ├── 9.4 Redis.md
│   └── 9.5 RDBMS vs NoSQL.md
├── Chapter 10. Database Performance/
│   ├── 10.1 IOPS (Input-Output Operations Per Second).md
│   ├── 10.2 Database Indexing.md
│   ├── 10.3 SELECT with ORDER BY RANDOM.md
│   ├── 10.4 COUNT Performance.md
│   ├── 10.5 Connection Pooling.md
│   └── 10.6 Maximum Connections.md
├── Chapter 11. Database Scaling Strategies/
│   ├── 11.1 Vertical Scaling.md
│   ├── 11.2 Read Replicas.md
│   ├── 11.3 Sharding.md
│   ├── 11.4 Batch Processing.md
│   └── 11.5 Caching with Redis.md
├── Chapter 12. Clustering and Multi-Process/
│   ├── 12.1 Process Clustering.md
│   ├── 12.2 PM2 Process Manager.md
│   ├── 12.3 Ecosystem Configuration Files.md
│   ├── 12.4 Parent-Child Process Architecture.md
│   └── 12.5 Cluster Mode Scaling.md
├── Chapter 13. Cloud Computing/
│   ├── 13.1 Amazon Web Services (AWS).md
│   ├── 13.2 EC2 (Elastic Compute Cloud).md
│   ├── 13.3 Instance Types.md
│   ├── 13.4 AMIs (Amazon Machine Images).md
│   ├── 13.5 RDS and Aurora.md
│   ├── 13.6 Security Groups.md
│   └── 13.7 Cloud Cost Estimation.md
├── Chapter 14. Load Balancing and Distribution/
│   ├── 14.1 What is Load Balancing.md
│   ├── 14.2 Geographic Distribution.md
│   ├── 14.3 CDNs (Content Delivery Networks).md
│   └── 14.4 DNS-Based Routing.md
├── Chapter 15. Bottleneck Analysis/
│   ├── 15.1 Identifying Bottlenecks.md
│   ├── 15.2 CPU Bottlenecks.md
│   ├── 15.3 Network Bottlenecks.md
│   ├── 15.4 Memory Bottlenecks.md
│   └── 15.5 Disk I-O Bottlenecks.md
├── Chapter 16. Cost Engineering/
│   ├── 16.1 Cloud Cost Models.md
│   ├── 16.2 Reserved Instances vs On-Demand.md
│   ├── 16.3 Serverless vs Dedicated.md
│   └── 16.4 Total Cost of Ownership.md
└── Chapter 17. Advanced Topics and Real-World Architecture/
    ├── 17.1 Connection Pooling Deep Dive.md
    ├── 17.2 HTTP Pipelining Deep Dive.md
    ├── 17.3 Network Interface Cards at Scale.md
    ├── 17.4 Private Networks (VPC).md
    ├── 17.5 Monitoring and Observability.md
    └── 17.6 Real-World Architecture for 1M RPS.md
```

---

## Tags Used in This Vault

| Tag | Meaning | Example Notes |
|-----|---------|---------------|
| `#concept` | Foundational concept or definition | CPU Cores, TCP, Big O |
| `#benchmark` | Performance measurement or result | Framework Benchmarking Results, RPS |
| `#tool` | Specific software tool | Autocannon, PM2, Redis |
| `#architecture` | System design or infrastructure | Load Balancing, Sharding, VPC |
| `#bottleneck` | Performance constraint | CPU Bottlenecks, Network Bottlenecks |
| `#cost` | Financial or pricing topic | Cloud Cost Models, TCO |
| `#database` | Database-related | PostgreSQL, Indexing, IOPS |
| `#nodejs` | Node.js specific | Event Loop, Express, Fastify |
| `#cpp` | C++ specific | Drogon, RapidJSON, Memory Management |
| `#aws` | AWS specific | EC2, RDS, Security Groups |
| `#algorithm` | Algorithm or complexity | O(n), O(log n), O(1) |
| `#scaling` | Scaling strategy | Vertical Scaling, Read Replicas, Sharding |

---

## Quick-Start Guide

### New to Systems Performance?
1. Read [[1.1 What Does 1 Million Requests Per Second Mean]] for context
2. Follow [[MOCs/Learning Roadmap]] from Tier 1

### Already Know the Basics?
1. Skim [[MOCs/Main Map of Content]] to find gaps
2. Jump to [[MOCs/Video Journey - From 18K to 6M RPS]] for the narrative
3. Use [[MOCs/Comparison - Frameworks]] and [[MOCs/Comparison - Languages]] for quick reference

### Preparing for System Design Interviews?
1. Focus on [[MOCs/Comparison - Database Strategies]] and [[MOCs/Bottleneck Identification Guide]]
2. Study [[MOCs/Concept Relationship Map]] to articulate trade-offs
3. Read [[17.6 Real-World Architecture for 1M RPS]] for the capstone

### Troubleshooting a Slow System?
1. Use [[MOCs/Bottleneck Identification Guide]] flowchart
2. Check the relevant chapter notes for solutions
3. Reference [[MOCs/Comparison - Database Strategies]] if the database is the issue

---

## MOC Index

- [[MOCs/Learning Roadmap]]
- [[MOCs/Main Map of Content]]
- [[MOCs/Concept Relationship Map]]
- [[MOCs/Comparison - Frameworks]]
- [[MOCs/Comparison - Languages]]
- [[MOCs/Comparison - Database Strategies]]
- [[MOCs/Bottleneck Identification Guide]]
- [[MOCs/Video Journey - From 18K to 6M RPS]]