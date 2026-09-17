# Main Map of Content — 1 Million RPS Knowledge Vault

> [!abstract] Vault Overview
> This vault contains **85 notes** organized across **17 chapters**, covering the complete journey from first principles to building systems that handle 1 million requests per second. Each link below leads to a detailed note.

---

## Chapter 1. Introduction to High-Scale Systems
- [[1.1 What Does 1 Million Requests Per Second Mean]] — Defining the scale and what it truly means
- [[1.2 Real-World Examples at Million RPS Scale]] — AWS IAM, Uber, Netflix, and others operating at massive scale
- [[1.3 The Engineering Mindset at Scale]] — How to think about systems that serve millions
- [[1.4 Cost of Operating at Scale]] — Financial implications of high-throughput systems

## Chapter 2. Computer Architecture Fundamentals
- [[2.1 CPU Cores and Threads]] — How processors work and what cores/threads mean
- [[2.2 Core Utilization]] — Measuring how much of the CPU is actually being used
- [[2.3 CPU Utilization Methods]] — Techniques for maximizing CPU usage
- [[2.4 RAM vs Disk vs Network Speeds]] — Speed hierarchy of storage and communication
- [[2.5 Bits, Bytes, and Data Units]] — Foundational data measurement units
- [[2.6 Network Cards and Bandwidth]] — Network interface hardware and throughput limits

## Chapter 3. Networking Fundamentals
- [[3.1 TCP Connections]] — The foundation of reliable network communication
- [[3.2 HTTP Protocol]] — How web requests and responses work
- [[3.3 HTTP Methods]] — GET, POST, PUT, DELETE and when to use each
- [[3.4 HTTP Status Codes]] — Understanding 200, 404, 500 and the full spectrum
- [[3.5 JSON Data Format]] — The dominant data interchange format for APIs
- [[3.6 Network Latency and Bandwidth]] — The two key metrics of network performance

## Chapter 4. Operating System Concepts
- [[4.1 Processes and Threads]] — How operating systems manage execution units
- [[4.2 Multi-Threading]] — Running multiple threads for concurrent work
- [[4.3 Race Conditions]] — When concurrent access causes unpredictable bugs
- [[4.4 Semaphores and Synchronization]] — Primitives for coordinating concurrent access
- [[4.5 SSH (Secure Shell)]] — Secure remote access to servers
- [[4.6 Unix and Linux Terminal Commands]] — Essential commands for working with servers

## Chapter 5. Performance and Benchmarking
- [[5.1 Requests Per Second (RPS)]] — The primary metric for measuring throughput
- [[5.2 Autocannon]] — The benchmarking tool used throughout the project
- [[5.3 Benchmarking Methodology]] — How to run reliable and meaningful benchmarks
- [[5.4 Connections, Pipelining, and Workers]] — HTTP connection strategies that affect performance
- [[5.5 Percentiles in Benchmarking]] — Why p50, p95, p99 matter more than averages
- [[5.6 Resource Monitoring]] — Tracking CPU, memory, and network during benchmarks

## Chapter 6. Big O Notation and Algorithms
- [[6.1 Big O Notation]] — The language for describing algorithm efficiency
- [[6.2 O(n) Linear Time]] — Algorithms that scale proportionally with input size
- [[6.3 O(log n) Logarithmic Time]] — Efficient algorithms like binary search and B-trees
- [[6.4 O(1) Constant Time]] — The gold standard: operations that don't slow down with scale
- [[6.5 Database Query Complexity]] — How Big O applies to database operations
- [[6.6 Why Algorithms Matter at Scale]] — The dramatic impact of algorithmic efficiency at 1M RPS

## Chapter 7. Backend Development with Node.js
- [[7.1 What is Node.js]] — JavaScript runtime built on V8 for server-side development
- [[7.2 The Event Loop]] — Node.js's non-blocking I/O execution model
- [[7.3 Express Framework]] — The most popular Node.js web framework
- [[7.4 Fastify Framework]] — A high-performance alternative to Express
- [[7.5 Custom Framework (CP)]] — Building a minimal framework for maximum performance
- [[7.6 Framework Benchmarking Results]] — Head-to-head performance comparison of all frameworks

## Chapter 8. High-Performance Languages
- [[8.1 C++ for High Performance]] — Why C++ is the choice for extreme throughput
- [[8.2 Drogon Framework]] — High-performance C++ web framework that reached 1M RPS
- [[8.3 RapidJSON]] — Fast JSON parsing library for C++ applications
- [[8.4 Language Performance Comparison]] — Benchmarks across Node.js, Python, Java, Go, Rust, and C++
- [[8.5 Memory Management]] — Manual memory control in C++ vs garbage collection

## Chapter 9. Database Fundamentals
- [[9.1 What is a Database]] — The role of databases in web applications
- [[9.2 SQL Basics]] — Foundations of structured query language
- [[9.3 PostgreSQL]] — The advanced open-source relational database
- [[9.4 Redis]] — In-memory data store for caching and fast access
- [[9.5 RDBMS vs NoSQL]] — Trade-offs between relational and non-relational databases

## Chapter 10. Database Performance
- [[10.1 IOPS (Input-Output Operations Per Second)]] — The fundamental limit of disk-based storage
- [[10.2 Database Indexing]] — How indexes dramatically speed up queries via B-trees
- [[10.3 SELECT with ORDER BY RANDOM]] — A case study in catastrophic query performance
- [[10.4 COUNT Performance]] — Why counting rows can be surprisingly expensive
- [[10.5 Connection Pooling]] — Managing database connections efficiently at scale
- [[10.6 Maximum Connections]] — Understanding and configuring connection limits

## Chapter 11. Database Scaling Strategies
- [[11.1 Vertical Scaling]] — Scaling up: bigger machines, faster disks, more RAM
- [[11.2 Read Replicas]] — Distributing read queries across copied databases
- [[11.3 Sharding]] — Distributing data across multiple database instances
- [[11.4 Batch Processing]] — Grouping operations to reduce overhead
- [[11.5 Caching with Redis]] — Reducing database load with in-memory caching

## Chapter 12. Clustering and Multi-Process
- [[12.1 Process Clustering]] — Running multiple server processes to utilize all CPU cores
- [[12.2 PM2 Process Manager]] — Production-grade Node.js process management
- [[12.3 Ecosystem Configuration Files]] — Configuring PM2 with ecosystem files
- [[12.4 Parent-Child Process Architecture]] — How clustered processes communicate and coordinate
- [[12.5 Cluster Mode Scaling]] — Scaling from single-process to multi-process deployments

## Chapter 13. Cloud Computing
- [[13.1 Amazon Web Services (AWS)]] — Overview of the leading cloud platform
- [[13.2 EC2 (Elastic Compute Cloud)]] — Virtual servers in the cloud
- [[13.3 Instance Types]] — Choosing the right EC2 instance for your workload
- [[13.4 AMIs (Amazon Machine Images)]] — Pre-configured machine images for deployment
- [[13.5 RDS and Aurora]] — Managed database services on AWS
- [[13.6 Security Groups]] — Virtual firewalls for controlling network access
- [[13.7 Cloud Cost Estimation]] — Predicting and managing cloud infrastructure costs

## Chapter 14. Load Balancing and Distribution
- [[14.1 What is Load Balancing]] — Distributing traffic across multiple servers
- [[14.2 Geographic Distribution]] — Placing servers close to users for lower latency
- [[14.3 CDNs (Content Delivery Networks)]] — Caching content at the edge for global performance
- [[14.4 DNS-Based Routing]] — Using DNS to direct users to the nearest or best server

## Chapter 15. Bottleneck Analysis
- [[15.1 Identifying Bottlenecks]] — Systematic approach to finding what limits your system
- [[15.2 CPU Bottlenecks]] — When the processor is the limiting factor
- [[15.3 Network Bottlenecks]] — When bandwidth or latency constrains throughput
- [[15.4 Memory Bottlenecks]] — When RAM limitations degrade performance
- [[15.5 Disk I-O Bottlenecks]] — When storage speed becomes the constraint

## Chapter 16. Cost Engineering
- [[16.1 Cloud Cost Models]] — Understanding pricing structures in the cloud
- [[16.2 Reserved Instances vs On-Demand]] — Trading commitment for lower prices
- [[16.3 Serverless vs Dedicated]] — Cost comparison of different compute models
- [[16.4 Total Cost of Ownership]] — The full picture of running systems at scale

## Chapter 17. Advanced Topics and Real-World Architecture
- [[17.1 Connection Pooling Deep Dive]] — Advanced patterns for managing connections at scale
- [[17.2 HTTP Pipelining Deep Dive]] — Sending multiple requests without waiting for responses
- [[17.3 Network Interface Cards at Scale]] — Understanding NIC capabilities in cloud environments
- [[17.4 Private Networks (VPC)]] — Isolating infrastructure within virtual private clouds
- [[17.5 Monitoring and Observability]] — Tools and practices for understanding system behavior
- [[17.6 Real-World Architecture for 1M RPS]] — Putting it all together: architecture for million-RPS systems

---

## Navigation

- [[MOCs/Learning Roadmap]] — Recommended learning order
- [[MOCs/Concept Relationship Map]] — How concepts connect across chapters
- [[MOCs/Bottleneck Identification Guide]] — Decision tree for diagnosing performance issues
- [[MOCs/Comparison - Frameworks]] — Express vs Fastify vs CP vs Drogon
- [[MOCs/Comparison - Languages]] — Language performance head-to-head
- [[MOCs/Comparison - Database Strategies]] — Database scaling decision matrix
- [[MOCs/Video Journey - From 18K to 6M RPS]] — The video's narrative journey