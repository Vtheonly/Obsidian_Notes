---
sources:
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.1 Cloud Storage Paradigms - Block File Object.md]]"
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.2 Distributed Hash Tables and Consistent Hashing.md]]"
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.3 Data Consistency Models and CAP Theorem.md]]"
---

> [!question] Amazon S3 is an example of object storage.
>> [!success]- Answer
>> True

> [!question] File storage uses a hierarchical directory structure.
>> [!success]- Answer
>> True

> [!question] In the CAP theorem, Partition Tolerance is optional for distributed systems.
>> [!success]- Answer
>> False

> [!question] Object storage is ideal for unstructured data like images and videos.
>> [!success]- Answer
>> True

> [!question] Strong consistency guarantees that all nodes return the most recent write.
>> [!success]- Answer
>> True

> [!question] File storage is organized as:
> a) A flat list of objects
> b) A hierarchical directory tree
> c) A hash table
> d) A relational database
>> [!success]- Answer
>> b) A hierarchical directory tree

> [!question] Which consistency model guarantees all nodes return the latest write?
> a) Eventual consistency
> b) Strong consistency
> c) Weak consistency
> d) Causal consistency
>> [!success]- Answer
>> b) Strong consistency

> [!question] Object storage is ideal for:
> a) Relational databases
> b) Unstructured data like images and videos
> c) Operating system files
> d) Swap partitions
>> [!success]- Answer
>> b) Unstructured data like images and videos

> [!question] When a node is added or removed, consistent hashing requires:
> a) Complete rehashing of all keys
> b) Minimal key redistribution
> c) Database migration
> d) Full system restart
>> [!success]- Answer
>> b) Minimal key redistribution

> [!question] Partition Tolerance in CAP means the system continues to function despite:
> a) Hardware upgrades
> b) Network communication failures between nodes
> c) Software bugs
> d) User errors
>> [!success]- Answer
>> b) Network communication failures between nodes

> [!question] Match the distributed system concept with its use.
>> [!example] Group A
>> a) Replication
>> b) Sharding
>> c) Partitioning
>> d) Load balancing
>
>> [!example] Group B
>> n) Copying data across multiple nodes
>> o) Splitting data across databases
>> p) Dividing the keyspace across nodes
>> q) Distributing requests across servers
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the distributed storage feature with its description.
>> [!example] Group A
>> a) Data durability
>> b) Data availability
>> c) Data consistency
>> d) Data integrity
>
>> [!example] Group B
>> n) Protection against permanent data loss
>> o) Ensuring data is accessible when needed
>> p) All replicas return the same value
>> q) Protection against data corruption
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the hashing type with its property.
>> [!example] Group A
>> a) Traditional hashing
>> b) Consistent hashing
>> c) Rendezvous hashing
>> d) Distributed hashing
>
>> [!example] Group B
>> n) All keys remap when node count changes
>> o) Minimal key movement when nodes change
>> p) Each client independently computes target node
>> q) Hash function spreads keys across nodes
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the replication strategy with its approach.
>> [!example] Group A
>> a) Synchronous replication
>> b) Asynchronous replication
>> c) Quorum-based replication
>> d) Chain replication
>
>> [!example] Group B
>> n) Write completes only after all replicas confirm
>> o) Write completes before all replicas are updated
>> p) Requires majority consensus for reads/writes
>> q) Replicas are organized in a linear chain
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the storage access pattern with its typical workload.
>> [!example] Group A
>> a) Sequential access
>> b) Random access
>> c) Streaming access
>> d) Indexed access
>
>> [!example] Group B
>> n) Reading data in order, typical for logs
>> o) Reading data at arbitrary positions
>> p) Continuous flow of data, typical for video
>> q) Accessing data via lookup indexes
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
