# Concept Relationship Map

> [!abstract] Cross-Chapter Connections
> This diagram shows how the most important concepts in this vault relate to each other across chapters. Follow the arrows to understand dependencies and causal chains.

---

## Relationship Graph

```mermaid
graph LR
    subgraph Networking [Ch3: Networking]
        TCP["TCP Connections"]
        HTTP["HTTP Protocol"]
        JSON["JSON Format"]
        Latency["Network Latency"]
        Bandwidth["Network Bandwidth"]
    end

    subgraph Architecture [Ch2: Computer Architecture]
        CPU["CPU Cores"]
        RAM["RAM Speed"]
        Disk["Disk Speed"]
        NIC["Network Card"]
        DataUnits["Bits & Bytes"]
    end

    subgraph OS [Ch4: OS Concepts]
        Processes["Processes"]
        Threads["Threads"]
        RaceCond["Race Conditions"]
        Sync["Semaphores"]
    end

    subgraph Bench [Ch5: Benchmarking]
        RPS["RPS Metric"]
        Autocannon["Autocannon"]
        Percentiles["Percentiles"]
        Mon["Resource Monitoring"]
    end

    subgraph BigO [Ch6: Big O]
        BigO["Big O Notation"]
        On["O(n) Linear"]
        Ologn["O(log n)"]
        O1["O(1) Constant"]
        DBComplex["DB Query Complexity"]
    end

    subgraph NodeJS [Ch7: Node.js]
        Node["Node.js"]
        EventLoop["Event Loop"]
        Express["Express"]
        Fastify["Fastify"]
        CP["CP Framework"]
    end

    subgraph DB [Ch9-10: Database]
        SQL["SQL"]
        PG["PostgreSQL"]
        Redis["Redis"]
        IOPS["IOPS"]
        Indexing["DB Indexing"]
        BTree["B-tree"]
        ConnPool["Connection Pool"]
    end

    subgraph Scaling [Ch11-12: Scaling]
        VertScale["Vertical Scaling"]
        Replicas["Read Replicas"]
        Sharding["Sharding"]
        Caching["Redis Cache"]
        Clustering["Process Clustering"]
        PM2["PM2"]
    end

    subgraph Cloud [Ch13-14: Infrastructure]
        AWS["AWS"]
        EC2["EC2"]
        InstanceType["Instance Types"]
        LB["Load Balancing"]
        CDN["CDN"]
        VPC["VPC"]
    end

    subgraph PerfLang [Ch8: High-Perf Languages]
        CPP["C++"]
        Drogon["Drogon"]
        RapidJSON["RapidJSON"]
        MemMgmt["Memory Mgmt"]
    end

    subgraph Bottleneck [Ch15: Bottlenecks]
        CPUBott["CPU Bottleneck"]
        NetBott["Network Bottleneck"]
        MemBott["Memory Bottleneck"]
        DiskBott["Disk I/O Bottleneck"]
    end

    subgraph Cost [Ch16: Cost]
        CostModel["Cloud Cost"]
        TCO["Total Cost of Ownership"]
    end

    %% Networking chains
    HTTP --> TCP
    TCP --> NIC
    TCP --> Latency
    NIC --> Bandwidth
    JSON --> HTTP
    Latency --> Bandwidth

    %% Architecture chains
    CPU --> CoreUtil["Core Utilization"]
    RAM --> Disk
    Disk --> IOPS
    DataUnits --> Bandwidth
    DataUnits --> RAM

    %% OS chains
    Processes --> Threads
    Threads --> RaceCond
    RaceCond --> Sync
    CPU --> Processes

    %% Benchmarking chains
    TCP --> RPS
    RPS --> Autocannon
    RPS --> Percentiles
    CPU --> Mon
    RAM --> Mon
    Bandwidth --> Mon

    %% Big O chains
    BigO --> On
    BigO --> Ologn
    BigO --> O1
    Ologn --> BTree
    BTree --> Indexing
    Indexing --> DBComplex
    BigO --> DBComplex

    %% Node.js chains
    Node --> EventLoop
    EventLoop --> SingleThread["Single-Threaded"]
    Express --> Node
    Fastify --> Node
    CP --> EventLoop
    SingleThread --> Clustering
    Clustering --> PM2

    %% Database chains
    SQL --> PG
    PG --> Indexing
    Indexing --> Ologn
    PG --> IOPS
    Redis --> Caching
    PG --> ConnPool
    IOPS --> DiskBott
    ConnPool --> MemBott

    %% Scaling chains
    VertScale --> Replicas
    Replicas --> Sharding
    PG --> VertScale
    PG --> Replicas
    Redis --> Caching
    Caching --> O1
    Clustering --> CPU
    Sharding --> LB

    %% Cloud chains
    AWS --> EC2
    EC2 --> InstanceType
    InstanceType --> CPU
    InstanceType --> CostModel
    EC2 --> VPC
    LB --> EC2
    CDN --> LB

    %% High-perf language chains
    CPP --> Drogon
    Drogon --> RapidJSON
    CPP --> MemMgmt
    Express --> Drogon
    Fastify --> Drogon

    %% Bottleneck chains
    CPU --> CPUBott
    Bandwidth --> NetBott
    RAM --> MemBott
    IOPS --> DiskBott
    BigO --> CPUBott
    EventLoop --> CPUBott
    Clustering --> CPUBott

    %% Cost chains
    EC2 --> CostModel
    InstanceType --> CostModel
    CostModel --> TCO
    Sharding --> CostModel
    Caching --> CostModel

    %% Cross-cutting
    RPS --> NetBott
    RPS --> CPUBott
```

---

## Key Relationship Chains

### The RPS Pipeline
```
HTTP Request → TCP Connection → Event Loop / Thread → Business Logic → Database Query → HTTP Response
     ↓              ↓                ↓                        ↓                ↓
  Network IO    Connection Mgmt   CPU Processing         IOPS + Big O      Serialization
     ↓              ↓                ↓                        ↓                ↓
NetBottleneck  ConnPool           CPUBottleneck         DiskBottleneck    JSON Parse Cost
```

### The Scaling Decision Tree
```
Need more RPS?
├── CPU at 100%? → Clustering (Ch12) or Better Language (Ch8)
├── Network saturated? → Bigger NIC (Ch2) or CDN (Ch14)
├── DB too slow? → Indexing (Ch10) → Read Replicas (Ch11) → Sharding (Ch11) → Cache (Ch11)
└── None of the above? → Add more instances behind Load Balancer (Ch14)
```

### The Algorithm Impact Chain
```
Algorithm Choice (Ch6) → Big O Complexity → CPU Cycles per Request → Max RPS
                                                           ↓
                                              O(n) vs O(log n) vs O(1)
                                              35K vs 400K vs 1M+ RPS
```

---

## Related MOCs

- [[MOCs/Main Map of Content]] — Full index of every note
- [[MOCs/Learning Roadmap]] — Recommended learning order
- [[MOCs/Bottleneck Identification Guide]] — Decision tree for diagnosing bottlenecks