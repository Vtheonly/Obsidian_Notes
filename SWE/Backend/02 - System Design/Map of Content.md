---
tags:
  - moc
  - system-design
aliases:
  - MOC
  - Table of Contents
  - Course Index
---
# Map of Content

This is the complete map of content for the System Design Vault. Every topic across all twelve chapters is listed below with direct links to the corresponding notes.

---

## Chapter 1 -- Computer Architecture and Hardware Foundations

Understanding the physical hardware layer is essential before designing any software system. This chapter covers the fundamental building blocks of computation, from binary data representation to the boundaries of vertical scaling on a single machine.

1. [[1. Binary Data and Bits]]
2. [[2. Storage Types Disk Drives and Solid State Drives]]
3. [[3. Data Volatility and Persistence]]
4. [[4. Random Access Memory Capabilities]]
5. [[5. Central Processing Unit Execution Cycles]]
6. [[6. CPU Cache Hierarchy Level 1 Level 2 and Level 3]]
7. [[7. Motherboard and Data Pathways]]
8. [[8. Threads and Multi Threading Concepts]]
9. [[9. CPU Core Utilization and Idle Time Calculation]]
10. [[10. Hardware Limitations and Vertical Scaling Boundaries]]

---

## Chapter 2 -- High Level System Architecture and Scaling Strategies

This chapter transitions from single-machine concerns to system-level thinking. It covers how individual servers are combined into distributed systems, the trade-offs between scaling approaches, and the fundamental theorems that govern distributed system design.

1. [[1. Single Server Architecture Lifecycle]]
2. [[2. Vertical Scaling versus Horizontal Scaling]]
3. [[3. System Availability and Nines of Reliability]]
4. [[4. Service Level Objectives]]
5. [[5. Service Level Agreements]]
6. [[6. System Reliability and Fault Tolerance]]
7. [[7. System Redundancy and Backups]]
8. [[8. Throughput Metrics Requests and Queries per Second]]
9. [[9. Latency and Response Time Optimization]]
10. [[10. Single Point of Failure Identification]]
11. [[11. CAP Theorem Consistency Availability and Partition Tolerance]]
12. [[12. Graceful Degradation in System Failures]]

---

## Chapter 3 -- Networking Basics and Communication Protocols

Distributed systems rely on network communication. This chapter provides a thorough grounding in networking fundamentals, from IP addressing through the OSI model to application-layer protocols that power the internet.

1. [[1. Internet Protocol Addressing IPv4 versus IPv6]]
2. [[2. Public versus Private IP Addresses]]
3. [[3. Static versus Dynamic IP Allocation]]
4. [[4. Ports and Network Services]]
5. [[5. Domain Name System and ICANN]]
6. [[6. DNS Record Types A Records and AAAA Records]]
7. [[7. Network Firewalls and Traffic Control]]
8. [[8. OSI Model Transport Layer]]
9. [[9. Transmission Control Protocol and Three Way Handshake]]
10. [[10. User Datagram Protocol and Loss Tolerance]]
11. [[11. OSI Model Application Layer]]
12. [[12. Hypertext Transfer Protocol HTTP and HTTPS]]
13. [[13. SSL and TLS Encryption Layers]]
14. [[14. WebSockets and Bidirectional Communication]]
15. [[15. Advanced Message Queuing Protocol]]
16. [[16. Remote Procedure Calls and gRPC]]
17. [[17. Specialized Protocols SMTP IMAP POP3 FTP SSH WebRTC and MQTT]]

---

## Chapter 4 -- Application Programming Interfaces Design and Architecture

APIs define the contract between system components and external consumers. This chapter covers the three dominant API paradigms -- REST, GraphQL, and gRPC -- along with essential design principles, versioning strategies, and lifecycle management.

1. [[1. API Fundamentals and System Abstraction]]
2. [[2. RESTful API Architecture and Principles]]
3. [[3. Resource Modeling Nouns versus Verbs]]
4. [[4. HTTP Methods GET POST PUT PATCH and DELETE]]
5. [[5. HTTP Status Codes Success Redirection Client Error and Server Error]]
6. [[6. API Query Parameters Filtering and Sorting]]
7. [[7. API Pagination Limits Offsets and Cursors]]
8. [[8. Idempotency in API Requests]]
9. [[9. GraphQL API Architecture and Single Endpoints]]
10. [[10. GraphQL Schema Design and Type Systems]]
11. [[11. GraphQL Queries Mutations and Subscriptions]]
12. [[12. Over Fetching and Under Fetching Solutions]]
13. [[13. GraphQL Error Handling Paradigms]]
14. [[14. gRPC API Architecture and Protocol Buffers]]
15. [[15. Top Down versus Bottom Up API Design Approaches]]
16. [[16. API Lifecycle Management Design Development Deployment Maintenance and Deprecation]]
17. [[17. API Versioning Strategies and Backward Compatibility]]

---

## Chapter 5 -- Security Authentication and Authorization

Security is a cross-cutting concern that every system must address. This chapter covers the full spectrum of security topics, from authentication and authorization models to attack prevention and infrastructure security.

1. [[1. Authentication versus Authorization Concepts]]
2. [[2. Basic and Digest Authentication Methods]]
3. [[3. API Key Generation and Validation]]
4. [[4. Session Based Authentication and Stateful Servers]]
5. [[5. Token Based Authentication and Stateless Servers]]
6. [[6. JSON Web Tokens Structure and Claims]]
7. [[7. Access Tokens versus Refresh Tokens Lifecycles]]
8. [[8. Single Sign On User Experience]]
9. [[9. Security Assertion Markup Language Identity Protocol]]
10. [[10. OpenID Connect Identity Protocol]]
11. [[11. OAuth 2 Framework and Delegated Authorization]]
12. [[12. Role Based Access Control Models]]
13. [[13. Attribute Based Access Control Models]]
14. [[14. Access Control Lists and Resource Specific Permissions]]
15. [[15. Rate Limiting Strategies Per IP Per User and Global]]
16. [[16. Cross Origin Resource Sharing Policies]]
17. [[17. SQL and NoSQL Injection Attack Prevention]]
18. [[18. Web Application Firewalls]]
19. [[19. Virtual Private Networks for Internal APIs]]
20. [[20. Cross Site Request Forgery Prevention]]
21. [[21. Cross Site Scripting Vulnerability Mitigation]]

---

## Chapter 6 -- Proxies Load Balancing and NGINX

Traffic management is critical for any system serving more than a handful of users. This chapter covers proxy architectures, load balancing algorithms, and the practical configuration of NGINX and Traefik as production-grade reverse proxies and load balancers.

1. [[1. Proxy Server Fundamentals]]
2. [[2. Forward Proxies Anonymization and Access Control]]
3. [[3. Reverse Proxies Security and Traffic Management]]
4. [[4. Specialized Proxies Open Transparent Anonymous and Distorting]]
5. [[5. Load Balancing Core Concepts]]
6. [[6. Round Robin and Weighted Round Robin Algorithms]]
7. [[7. Least Connections and Weighted Least Connections Algorithms]]
8. [[8. Least Response Time Algorithm]]
9. [[9. IP Hashing and Session Persistence]]
10. [[10. Geographical Routing Algorithms]]
11. [[11. Consistent Hashing and Hash Rings]]
12. [[12. Load Balancer Health Checks and Self Healing]]
13. [[13. Hardware Software and Cloud Load Balancers]]
14. [[14. NGINX Installation and Configuration Structure]]
15. [[15. Serving Static Content with NGINX]]
16. [[16. NGINX Reverse Proxy Setup]]
17. [[17. NGINX SSL Termination and HTTP to HTTPS Redirection]]
18. [[18. NGINX Upstream Blocks and Load Balancing]]
19. [[19. Traefik Reverse Proxy and Microservices Routing]]

---

## Chapter 7 -- Caching and Content Delivery Networks

Caching is one of the most impactful optimization techniques in system design. This chapter covers caching at every layer of the stack, from browser caches to CDNs, and explains the write strategies and eviction policies that determine cache behavior.

1. [[1. Caching Fundamentals and Latency Reduction]]
2. [[2. Browser Caching and Cache Control Headers]]
3. [[3. Server Side Caching In Memory Storage]]
4. [[4. Database Query Caching]]
5. [[5. Write Around Cache Strategy]]
6. [[6. Write Through Cache Strategy]]
7. [[7. Write Back Cache Strategy]]
8. [[8. Cache Eviction Policies Least Recently Used and First In First Out]]
9. [[9. Content Delivery Networks Architectural Overview]]
10. [[10. Push Based versus Pull Based Content Delivery Networks]]
11. [[11. Serving Static Assets versus Dynamic Content Routing]]
12. [[12. NGINX Caching Configuration and Temporary Storage]]

---

## Chapter 8 -- Databases and Data Storage

Data storage is the backbone of nearly every application. This chapter covers the full landscape of database technologies, from relational SQL databases to the diverse NoSQL family, along with critical operational concerns like replication, sharding, and indexing.

1. [[1. Relational Databases SQL Structured Data]]
2. [[2. Tables Columns Rows and Join Operations]]
3. [[3. ACID Properties Atomicity Consistency Isolation Durability]]
4. [[4. Non Relational Databases NoSQL Unstructured Data]]
5. [[5. Document Stores MongoDB]]
6. [[6. Wide Column Stores Cassandra]]
7. [[7. Graph Databases Neo4j]]
8. [[8. Key Value Stores Redis and Memcached]]
9. [[9. SQL versus NoSQL Decision Framework]]
10. [[10. Master Slave and Master Master Database Replication]]
11. [[11. Database Sharding Range Based Directory Based and Geographical]]
12. [[12. Database Indexing for Rapid Retrieval]]
13. [[13. Query Optimization and Execution Planning]]

---

## Chapter 9 -- Message Queues and Event Streaming with Apache Kafka

Asynchronous communication is fundamental to building resilient, decoupled distributed systems. This chapter covers the paradigm shift from synchronous to asynchronous communication, the distinction between message brokers and event streaming platforms, and a deep dive into Apache Kafka's architecture and operations.

1. [[1. Synchronous versus Asynchronous Microservice Communication]]
2. [[2. Message Brokers versus Event Streaming Platforms]]
3. [[3. Apache Kafka Architectural Overview]]
4. [[4. Kafka Producers and Event Generation]]
5. [[5. Kafka Consumers and Event Processing]]
6. [[6. Kafka Topics and Logical Organization]]
7. [[7. Kafka Partitions and Parallel Processing]]
8. [[8. Consumer Groups and Automatic Load Distribution]]
9. [[9. Kafka Brokers and Cluster Management]]
10. [[10. Zookeeper Dependency versus KRaft Mode]]
11. [[11. Metadata Tracking and Consumer Offsets]]
12. [[12. Event Persistence on Disk versus Traditional Transient Queues]]
13. [[13. Kafka Listeners Client versus Controller Endpoints]]
14. [[14. Kafka Graceful Shutdown and Resource Cleanup]]
15. [[15. Troubleshooting with Kafka Command Line Interface]]

---

## Chapter 10 -- Big Data Processing with Apache Spark

When data volumes exceed what a single machine can process, distributed data processing frameworks become essential. This chapter covers Apache Spark's architecture, programming model, and optimization techniques for processing massive datasets efficiently.

1. [[1. Apache Spark Ecosystem and Capabilities]]
2. [[2. Resilient Distributed Datasets Fundamentals]]
3. [[3. Data Partitions and Cluster Distribution]]
4. [[4. In Memory Computation versus Disk Spillage]]
5. [[5. Spark Context versus Spark Session Initialization]]
6. [[6. Lazy Evaluation and Execution Flow Optimization]]
7. [[7. Spark Transformations versus Spark Actions]]
8. [[8. Narrow Transformations Map FlatMap and Filter]]
9. [[9. Wide Transformations GroupByKey ReduceByKey SortByKey and AggregateByKey]]
10. [[10. MapPartitions for Heavy Initialization Optimization]]
11. [[11. Combiners and Mini Reducers Network Input Output Reduction]]
12. [[12. Partition Management Repartition versus Coalesce]]
13. [[13. Spark Storage Levels and Persistence Cache Memory Only and Memory And Disk]]
14. [[14. Spark Web User Interface and Data Lineage Tracking]]

---

## Chapter 11 -- Containerization Orchestration and DevOps Engineering

Modern software deployment relies on containerization and orchestration to achieve reproducibility, scalability, and operational efficiency. This chapter covers the evolution from monoliths to microservices, Docker and Kubernetes, and the DevOps practices that tie development to operations.

1. [[1. Monolithic versus Microservices Architectural Paradigms]]
2. [[2. Docker Containerization Portability and Isolation]]
3. [[3. Docker Compose for Multi Container Applications]]
4. [[4. Orchestration Systems Kubernetes and Docker Swarm]]
5. [[5. Kubernetes Pods and Services Configuration]]
6. [[6. Kubernetes Ingress and Traffic Routing]]
7. [[7. DevOps Culture and Development Velocity]]
8. [[8. Continuous Integration and Merge Conflict Prevention]]
9. [[9. Continuous Deployment and Automated Delivery]]
10. [[10. GitHub Actions Workflows and CI CD Pipelines]]
11. [[11. Production Logging Monitoring and Alerting Systems]]
12. [[12. Safe Debugging Strategies Staging versus Production]]
13. [[13. Hotfixes and Incident Response]]

---

## Chapter 12 -- High Performance System Design Case Study

This capstone chapter brings together concepts from every preceding chapter in a practical case study: scaling a system to handle one million HTTP requests per second. It demonstrates how theoretical knowledge translates into real-world engineering decisions under extreme pressure.

1. [[1. Single Server Benchmarking Basics and AutoCannon Setup]]
2. [[2. Web Framework Performance Express versus Fastify versus Cpeak]]
3. [[3. Node Cluster Mode and Multi Threading CPU Utilization]]
4. [[4. Identifying Physical Hardware Bottlenecks CPU RAM and Network Interface Cards]]
5. [[5. Cloud Infrastructure Sizing AWS EC2 Compute and Network Optimized Instances]]
6. [[6. Analyzing Database Write Operation Limitations and High Cost Scaling]]
7. [[7. Transitioning from Disk Based SQL to In Memory Redis Queues]]
8. [[8. Handling UUID Collisions at High Scale using Birthday Paradox Mathematics]]
9. [[9. Redis Clustering Strategies Masters Replicas and Slot Hashing]]
10. [[10. Bypassing Language Limitations Transitioning from Node to C++ Drogon Framework]]
11. [[11. Network Load Balancer Capacity Limits and Pre Warming Requests]]
12. [[12. Massive Traffic Simulation Architecture Master and Worker Tester Nodes]]
