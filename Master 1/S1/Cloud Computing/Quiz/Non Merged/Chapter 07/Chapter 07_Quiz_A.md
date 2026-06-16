---
sources:
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.1 Cloud Storage Paradigms - Block File Object.md]]"
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.2 Distributed Hash Tables and Consistent Hashing.md]]"
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.3 Data Consistency Models and CAP Theorem.md]]"
---

> [!question] Object storage uses a flat namespace with independent objects.
>> [!success]- Answer
>> True

> [!question] Block storage supports partial updates without rewriting the entire file.
>> [!success]- Answer
>> True

> [!question] Object storage is best suited for low-latency database workloads.
>> [!success]- Answer
>> False

> [!question] The CAP Theorem states a distributed system can guarantee all three properties simultaneously.
>> [!success]- Answer
>> False

> [!question] Strong consistency guarantees every read returns the most recent write.
>> [!success]- Answer
>> True

> [!question] Eventual consistency means updates propagate over time and all copies converge.
>> [!success]- Answer
>> True

> [!question] Consistent hashing minimizes remapping when nodes are added or removed.
>> [!success]- Answer
>> True

> [!question] Amazon S3 is an example of block storage.
>> [!success]- Answer
>> False

> [!question] A distributed hash table (DHT) maps keys to nodes across a distributed system.
>> [!success]- Answer
>> True

> [!question] In a CP system availability is sacrificed when a network partition occurs.
>> [!success]- Answer
>> True

> [!question] Which cloud storage type provides virtually unlimited scalability?
> a) Block storage
> b) File storage
> c) Object storage
> d) Local storage
>> [!success]- Answer
>> c) Object storage

> [!question] Which storage type supports the lowest latency for databases?
> a) Object storage
> b) File storage
> c) Block storage
> d) Archive storage
>> [!success]- Answer
>> c) Block storage

> [!question] According to CAP theorem which property is sacrificed in AP systems?
> a) Availability
> b) Partition tolerance
> c) Consistency
> d) Performance
>> [!success]- Answer
>> c) Consistency

> [!question] What does consistent hashing solve?
> a) Data encryption
> b) The remapping problem when nodes join or leave
> c) Network routing
> d) Resource allocation in Kubernetes
>> [!success]- Answer
>> b) The remapping problem when nodes join or leave

> [!question] In cloud object storage how is an object updated?
> a) Partially overwritten
> b) The entire object must be rewritten (immutable)
> c) Appended to
> d) Only metadata changed
>> [!success]- Answer
>> b) The entire object must be rewritten (immutable)

> [!question] Which represents a CP system?
> a) DNS
> b) Traditional RDBMS with replication
> c) Amazon DynamoDB default
> d) CDN cache
>> [!success]- Answer
>> b) Traditional RDBMS with replication

> [!question] What does a Distributed Hash Table provide?
> a) Centralized database storage
> b) Key-based lookup across distributed nodes
> c) File system hierarchy
> d) Network routing
>> [!success]- Answer
>> b) Key-based lookup across distributed nodes

> [!question] Which consistency model is typical for Cassandra?
> a) Strong consistency
> b) Eventual consistency
> c) Strict consistency
> d) Linearizable consistency
>> [!success]- Answer
>> b) Eventual consistency

> [!question] What is a key advantage of object storage metadata?
> a) Minimal and fixed-size
> b) Highly customizable with unlimited key-value tags
> c) Cannot be modified
> d) Stored separately from object
>> [!success]- Answer
>> b) Highly customizable with unlimited key-value tags

> [!question] Which is most suitable for backup and archival?
> a) Block storage
> b) File storage
> c) Object storage
> d) In-memory storage
>> [!success]- Answer
>> c) Object storage

> [!question] Match storage paradigm with data structure.
>> [!example] Group A
>> a) Block storage
>> b) File storage
>> c) Object storage
>> d) In-memory storage
>
>> [!example] Group B
>> n) Raw sectors of fixed size
>> o) Hierarchical folder tree
>> p) Flat namespace with independent objects
>> q) RAM-based data structures
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match CAP property with definition.
>> [!example] Group A
>> a) Consistency
>> b) Availability
>> c) Partition tolerance
>> d) Durability
>
>> [!example] Group B
>> n) Every read receives most recent write
>> o) Every non-failing node returns response
>> p) System continues despite network failures
>> q) Data persists after writes confirmed
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match distributed systems concept with purpose.
>> [!example] Group A
>> a) Distributed Hash Table
>> b) Consistent hashing
>> c) Replication
>> d) Partitioning
>
>> [!example] Group B
>> n) Key-value lookup across distributed nodes
>> o) Minimizes key remapping on node changes
>> p) Data copying for fault tolerance
>> q) Splitting data across multiple nodes
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match cloud storage example with type.
>> [!example] Group A
>> a) AWS EBS
>> b) AWS EFS
>> c) AWS S3
>> d) AWS Glacier
>
>> [!example] Group B
>> n) Block storage for EC2 instances
>> o) File storage for shared filesystems
>> p) Object storage for scalable data
>> q) Archive storage for long-term retention
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match consistency model with characteristic.
>> [!example] Group A
>> a) Strong consistency
>> b) Eventual consistency
>> c) Read-your-writes
>> d) Monotonic reads
>
>> [!example] Group B
>> n) Guarantees latest data on every read
>> o) Data converges over time
>> p) User always sees their own writes
>> q) Reads never return older values
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage access method with protocol.
>> [!example] Group A
>> a) Block access
>> b) File access
>> c) Object access
>> d) Stream access
>
>> [!example] Group B
>> n) SCSI NVMe iSCSI
>> o) NFS SMB/CIFS
>> p) HTTP/S REST API (GET PUT POST)
>> q) Kafka Kinesis Pulsar
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match DHT concept with role.
>> [!example] Group A
>> a) Key
>> b) Node
>> c) Virtual node
>> d) Ring topology
>
>> [!example] Group B
>> n) Identifier used for data lookup
>> o) Physical or logical server in the DHT
>> p) Multiple virtual positions per physical node
>> q) Circular arrangement of nodes for routing
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage scenario with paradigm.
>> [!example] Group A
>> a) VM boot volume
>> b) Shared team documents
>> c) Media assets for website
>> d) IoT sensor data archive
>
>> [!example] Group B
>> n) Block storage (high performance)
>> o) File storage (multi-user access)
>> p) Object storage (scalable assets)
>> q) Object storage (large volume low cost)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match replication strategy with consistency.
>> [!example] Group A
>> a) Synchronous replication
>> b) Asynchronous replication
>> c) Quorum-based replication
>> d) Gossip protocol
>
>> [!example] Group B
>> n) Strong consistency (all nodes must confirm)
>> o) Eventual consistency (data syncs over time)
>> p) Configurable consistency (R+W > N)
>> q) Eventual consistency (epidemic-style propagation)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match CAP system classification.
>> [!example] Group A
>> a) CP (Consistency + Partition)
>> b) AP (Availability + Partition)
>> c) CA (Consistency + Availability)
>> d) Eventual Consistency system
>
>> [!example] Group B
>> n) Traditional RDBMS with primary-secondary
>> o) Cassandra or DynamoDB default
>> p) Not achievable during partitions
>> q) DNS system
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
