# Learning Roadmap — 1 Million RPS

> [!tip] Start Here
> This roadmap guides you through the entire knowledge vault in a recommended learning order. Follow the tiers sequentially, or jump to a quick path below if you already have background knowledge.

---

## Mindmap — All 17 Chapters

```mermaid
mindmap
  root((1M RPS<br/>Knowledge Vault))
    Tier 1 Prerequisites
      Ch2 Computer Architecture
        CPU Cores and Threads
        Core Utilization
        CPU Utilization Methods
        RAM vs Disk vs Network Speeds
        Bits Bytes and Data Units
        Network Cards and Bandwidth
      Ch3 Networking
        TCP Connections
        HTTP Protocol
        HTTP Methods
        HTTP Status Codes
        JSON Data Format
        Network Latency and Bandwidth
      Ch4 OS Concepts
        Processes and Threads
        Multi-Threading
        Race Conditions
        Semaphores and Synchronization
        SSH Secure Shell
        Unix and Linux Terminal Commands
    Tier 2 Core Skills
      Ch5 Benchmarking
        Requests Per Second
        Autocannon
        Benchmarking Methodology
        Connections Pipelining and Workers
        Percentiles in Benchmarking
        Resource Monitoring
      Ch6 Big O Notation
        Big O Notation
        O(n) Linear Time
        O(log n) Logarithmic Time
        O(1) Constant Time
        Database Query Complexity
        Why Algorithms Matter at Scale
      Ch7 Node.js
        What is Node.js
        The Event Loop
        Express Framework
        Fastify Framework
        Custom Framework CP
        Framework Benchmarking Results
    Tier 3 Database
      Ch9 Database Fundamentals
        What is a Database
        SQL Basics
        PostgreSQL
        Redis
        RDBMS vs NoSQL
      Ch10 Database Performance
        IOPS
        Database Indexing
        SELECT with ORDER BY RANDOM
        COUNT Performance
        Connection Pooling
        Maximum Connections
    Tier 4 Scaling
      Ch8 High-Performance Languages
        C++ for High Performance
        Drogon Framework
        RapidJSON
        Language Performance Comparison
        Memory Management
      Ch11 Database Scaling
        Vertical Scaling
        Read Replicas
        Sharding
        Batch Processing
        Caching with Redis
      Ch12 Clustering
        Process Clustering
        PM2 Process Manager
        Ecosystem Configuration Files
        Parent-Child Process Architecture
        Cluster Mode Scaling
    Tier 5 Infrastructure
      Ch13 Cloud Computing
        Amazon Web Services AWS
        EC2 Elastic Compute Cloud
        Instance Types
        AMIs Amazon Machine Images
        RDS and Aurora
        Security Groups
        Cloud Cost Estimation
      Ch14 Load Balancing
        What is Load Balancing
        Geographic Distribution
        CDNs Content Delivery Networks
        DNS-Based Routing
    Tier 6 Advanced
      Ch15 Bottleneck Analysis
        Identifying Bottlenecks
        CPU Bottlenecks
        Network Bottlenecks
        Memory Bottlenecks
        Disk I-O Bottlenecks
      Ch16 Cost Engineering
        Cloud Cost Models
        Reserved Instances vs On-Demand
        Serverless vs Dedicated
        Total Cost of Ownership
      Ch17 Real-World Architecture
        Connection Pooling Deep Dive
        HTTP Pipelining Deep Dive
        Network Interface Cards at Scale
        Private Networks VPC
        Monitoring and Observability
        Real-World Architecture for 1M RPS
```

---

## Ch1 — Introduction (Read First)
| # | Chapter | Topic | Hours | Dependencies |
|---|---------|-------|-------|-------------|
| 0 | Ch1 | [[1.1 What Does 1 Million Requests Per Second Mean]] | 0.3h | None |
|   | Ch1 | [[1.2 Real-World Examples at Million RPS Scale]] | 0.3h | None |
|   | Ch1 | [[1.3 The Engineering Mindset at Scale]] | 0.3h | None |
|   | Ch1 | [[1.4 Cost of Operating at Scale]] | 0.3h | None |

---

## Tier 1 — Prerequisites (~9 hours)

| # | Chapter | Topic | Hours | Dependencies |
|---|---------|-------|-------|-------------|
| 1 | Ch2 | [[2.1 CPU Cores and Threads]] | 0.5h | None |
|   | Ch2 | [[2.2 Core Utilization]] | 0.5h | 2.1 |
|   | Ch2 | [[2.3 CPU Utilization Methods]] | 0.5h | 2.1, 2.2 |
|   | Ch2 | [[2.4 RAM vs Disk vs Network Speeds]] | 0.5h | None |
|   | Ch2 | [[2.5 Bits, Bytes, and Data Units]] | 0.5h | None |
|   | Ch2 | [[2.6 Network Cards and Bandwidth]] | 0.5h | 2.5 |
| 2 | Ch3 | [[3.1 TCP Connections]] | 0.5h | None |
|   | Ch3 | [[3.2 HTTP Protocol]] | 0.5h | 3.1 |
|   | Ch3 | [[3.3 HTTP Methods]] | 0.3h | 3.2 |
|   | Ch3 | [[3.4 HTTP Status Codes]] | 0.3h | 3.2 |
|   | Ch3 | [[3.5 JSON Data Format]] | 0.3h | 3.2 |
|   | Ch3 | [[3.6 Network Latency and Bandwidth]] | 0.5h | 2.6, 3.1 |
| 3 | Ch4 | [[4.1 Processes and Threads]] | 0.5h | 2.1 |
|   | Ch4 | [[4.2 Multi-Threading]] | 0.5h | 4.1 |
|   | Ch4 | [[4.3 Race Conditions]] | 0.5h | 4.2 |
|   | Ch4 | [[4.4 Semaphores and Synchronization]] | 0.5h | 4.3 |
|   | Ch4 | [[4.5 SSH (Secure Shell)]] | 0.3h | None |
|   | Ch4 | [[4.6 Unix and Linux Terminal Commands]] | 0.5h | 4.5 |

---

## Tier 2 — Core Skills (~9 hours)

| # | Chapter | Topic | Hours | Dependencies |
|---|---------|-------|-------|-------------|
| 4 | Ch5 | [[5.1 Requests Per Second (RPS)]] | 0.5h | Ch3 |
|   | Ch5 | [[5.2 Autocannon]] | 0.5h | 5.1 |
|   | Ch5 | [[5.3 Benchmarking Methodology]] | 1h | 5.1, 5.2 |
|   | Ch5 | [[5.4 Connections, Pipelining, and Workers]] | 0.5h | 3.1, 5.1 |
|   | Ch5 | [[5.5 Percentiles in Benchmarking]] | 0.5h | 5.1 |
|   | Ch5 | [[5.6 Resource Monitoring]] | 0.5h | 2.2, 2.4 |
| 5 | Ch6 | [[6.1 Big O Notation]] | 0.5h | None |
|   | Ch6 | [[6.2 O(n) Linear Time]] | 0.3h | 6.1 |
|   | Ch6 | [[6.3 O(log n) Logarithmic Time]] | 0.5h | 6.1 |
|   | Ch6 | [[6.4 O(1) Constant Time]] | 0.3h | 6.1 |
|   | Ch6 | [[6.5 Database Query Complexity]] | 0.5h | 6.1–6.4 |
|   | Ch6 | [[6.6 Why Algorithms Matter at Scale]] | 0.3h | 6.5 |
| 6 | Ch7 | [[7.1 What is Node.js]] | 0.5h | Ch4 |
|   | Ch7 | [[7.2 The Event Loop]] | 0.5h | 7.1, 4.1 |
|   | Ch7 | [[7.3 Express Framework]] | 0.5h | 7.1 |
|   | Ch7 | [[7.4 Fastify Framework]] | 0.5h | 7.3 |
|   | Ch7 | [[7.5 Custom Framework (CP)]] | 0.5h | 7.2, 7.4 |
|   | Ch7 | [[7.6 Framework Benchmarking Results]] | 1h | 7.3–7.5, Ch5 |

---

## Tier 3 — Database (~7 hours)

| # | Chapter | Topic | Hours | Dependencies |
|---|---------|-------|-------|-------------|
| 7 | Ch9 | [[9.1 What is a Database]] | 0.5h | None |
|   | Ch9 | [[9.2 SQL Basics]] | 0.5h | 9.1 |
|   | Ch9 | [[9.3 PostgreSQL]] | 0.5h | 9.2 |
|   | Ch9 | [[9.4 Redis]] | 0.5h | 9.1 |
|   | Ch9 | [[9.5 RDBMS vs NoSQL]] | 0.5h | 9.3, 9.4 |
| 8 | Ch10 | [[10.1 IOPS (Input-Output Operations Per Second)]] | 0.5h | 9.1, 2.4 |
|   | Ch10 | [[10.2 Database Indexing]] | 1h | 9.2, 6.3 |
|   | Ch10 | [[10.3 SELECT with ORDER BY RANDOM]] | 0.5h | 10.2, 6.2 |
|   | Ch10 | [[10.4 COUNT Performance]] | 0.3h | 10.2 |
|   | Ch10 | [[10.5 Connection Pooling]] | 0.5h | 10.1, 3.1 |
|   | Ch10 | [[10.6 Maximum Connections]] | 0.3h | 10.5 |

---

## Tier 4 — Scaling (~10 hours)

| # | Chapter | Topic | Hours | Dependencies |
|---|---------|-------|-------|-------------|
| 9 | Ch8 | [[8.1 C++ for High Performance]] | 1h | Ch4 |
|   | Ch8 | [[8.2 Drogon Framework]] | 0.5h | 8.1 |
|   | Ch8 | [[8.3 RapidJSON]] | 0.5h | 8.1 |
|   | Ch8 | [[8.4 Language Performance Comparison]] | 0.5h | 8.1, 7.6 |
|   | Ch8 | [[8.5 Memory Management]] | 0.5h | 8.1 |
| 10 | Ch11 | [[11.1 Vertical Scaling]] | 0.5h | Ch10 |
|   | Ch11 | [[11.2 Read Replicas]] | 0.5h | 11.1, 9.3 |
|   | Ch11 | [[11.3 Sharding]] | 1h | 11.2 |
|   | Ch11 | [[11.4 Batch Processing]] | 0.5h | 10.1, 11.1 |
|   | Ch11 | [[11.5 Caching with Redis]] | 0.5h | 9.4, 11.1 |
| 11 | Ch12 | [[12.1 Process Clustering]] | 0.5h | 7.2, 4.1 |
|   | Ch12 | [[12.2 PM2 Process Manager]] | 0.5h | 12.1 |
|   | Ch12 | [[12.3 Ecosystem Configuration Files]] | 0.3h | 12.2 |
|   | Ch12 | [[12.4 Parent-Child Process Architecture]] | 0.5h | 12.1, 4.1 |
|   | Ch12 | [[12.5 Cluster Mode Scaling]] | 0.5h | 12.1–12.4 |

---

## Tier 5 — Infrastructure (~6 hours)

| # | Chapter | Topic | Hours | Dependencies |
|---|---------|-------|-------|-------------|
| 12 | Ch13 | [[13.1 Amazon Web Services (AWS)]] | 0.5h | None |
|   | Ch13 | [[13.2 EC2 (Elastic Compute Cloud)]] | 0.5h | 13.1, 2.1 |
|   | Ch13 | [[13.3 Instance Types]] | 0.5h | 13.2 |
|   | Ch13 | [[13.4 AMIs (Amazon Machine Images)]] | 0.3h | 13.2 |
|   | Ch13 | [[13.5 RDS and Aurora]] | 0.5h | 13.1, 9.3 |
|   | Ch13 | [[13.6 Security Groups]] | 0.3h | 13.1 |
|   | Ch13 | [[13.7 Cloud Cost Estimation]] | 0.5h | 13.2, 13.3 |
| 13 | Ch14 | [[14.1 What is Load Balancing]] | 0.5h | Ch13 |
|   | Ch14 | [[14.2 Geographic Distribution]] | 0.5h | 14.1, 3.6 |
|   | Ch14 | [[14.3 CDNs (Content Delivery Networks)]] | 0.5h | 14.2 |
|   | Ch14 | [[14.4 DNS-Based Routing]] | 0.5h | 14.1 |

---

## Tier 6 — Advanced (~8 hours)

| # | Chapter | Topic | Hours | Dependencies |
|---|---------|-------|-------|-------------|
| 14 | Ch15 | [[15.1 Identifying Bottlenecks]] | 0.5h | Ch5, Ch6 |
|   | Ch15 | [[15.2 CPU Bottlenecks]] | 1h | 15.1, Ch2 |
|   | Ch15 | [[15.3 Network Bottlenecks]] | 1h | 15.1, Ch3, 2.6 |
|   | Ch15 | [[15.4 Memory Bottlenecks]] | 0.5h | 15.1, 2.4 |
|   | Ch15 | [[15.5 Disk I-O Bottlenecks]] | 0.5h | 15.1, 10.1 |
| 15 | Ch16 | [[16.1 Cloud Cost Models]] | 0.5h | Ch13 |
|   | Ch16 | [[16.2 Reserved Instances vs On-Demand]] | 0.5h | 16.1 |
|   | Ch16 | [[16.3 Serverless vs Dedicated]] | 0.5h | 16.1 |
|   | Ch16 | [[16.4 Total Cost of Ownership]] | 0.5h | 16.1–16.3 |
| 16 | Ch17 | [[17.1 Connection Pooling Deep Dive]] | 0.5h | 10.5, 15.1 |
|   | Ch17 | [[17.2 HTTP Pipelining Deep Dive]] | 0.5h | 5.4, 3.2 |
|   | Ch17 | [[17.3 Network Interface Cards at Scale]] | 0.5h | 2.6, 15.3 |
|   | Ch17 | [[17.4 Private Networks (VPC)]] | 0.5h | 13.6, 14.1 |
|   | Ch17 | [[17.5 Monitoring and Observability]] | 0.5h | 5.6, Ch13 |
|   | Ch17 | [[17.6 Real-World Architecture for 1M RPS]] | 1h | All prior chapters |

**Estimated total: ~49 hours**

---

## Quick-Start Paths

> [!info] Jump to the right starting point based on your background

### "I already know networking"
Skip Ch3. Start at Ch2 → Ch4 → Ch5 → Ch6 → Ch7 ...

### "I'm a backend developer"
Skip Ch4 (OS basics) and Ch9 (DB basics). Start at Ch5 → Ch6 → Ch7 → Ch10 → Ch11 ...

### "I just want the benchmarks"
Jump to [[7.6 Framework Benchmarking Results]] → [[8.4 Language Performance Comparison]] → [[MOCs/Video Journey - From 18K to 6M RPS]]

### "I'm studying for system design interviews"
Focus on: Ch5, Ch6, Ch10, Ch11, Ch12, Ch13, Ch14, Ch17

### "I'm ops/SRE focused"
Focus on: Ch2, Ch5, Ch12, Ch13, Ch14, Ch15, Ch16, Ch17

### "I want to go from 18K to 1M RPS"
Follow the full video journey: [[MOCs/Video Journey - From 18K to 6M RPS]]

---

## Related MOCs

- [[MOCs/Main Map of Content]] — Full index of every note
- [[MOCs/Concept Relationship Map]] — How concepts connect across chapters
- [[MOCs/Comparison - Frameworks]] — Express vs Fastify vs CP vs Drogon
- [[MOCs/Comparison - Languages]] — Node.js vs C++ vs Go vs Rust...
- [[MOCs/Comparison - Database Strategies]] — Vertical vs Sharding vs Caching
- [[MOCs/Bottleneck Identification Guide]] — Decision tree for diagnosing bottlenecks