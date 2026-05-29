---
sources:
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.1 Cloud Storage Paradigms - Block File Object.md]]"
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.2 Distributed Hash Tables and Consistent Hashing.md]]"
  - "[[Chapter 7 - Cloud Storage and Distributed Systems/7.3 Data Consistency Models and CAP Theorem.md]]"
---

> [!question] Object storage uses a flat namespace with unique identifiers.
>> [!success]- Answer
>> True

> [!question] Block storage stores data as objects with metadata.
>> [!success]- Answer
>> False

> [!question] Consistent hashing minimizes remapping when nodes are added or removed.
>> [!success]- Answer
>> True

> [!question] The CAP theorem states that a distributed system can guarantee all three of Consistency, Availability, and Partition Tolerance simultaneously.
>> [!success]- Answer
>> False

> [!question] A Distributed Hash Table (DHT) provides a lookup service across distributed nodes.
>> [!success]- Answer
>> True

> [!question] Object storage uses a:
> a) Hierarchical directory structure
> b) Flat namespace with unique identifiers
> c) Relational schema
> d) Block-based addressing
>> [!success]- Answer
>> b) Flat namespace with unique identifiers

> [!question] Consistent hashing helps with:
> a) Encrypting data
> b) Minimizing key remapping when nodes change
> c) Indexing databases
> d) Compressing files
>> [!success]- Answer
>> b) Minimizing key remapping when nodes change

> [!question] The CAP theorem states a system cannot guarantee all three of:
> a) Cost, Availability, Performance
> b) Consistency, Availability, Partition Tolerance
> c) Capacity, Access, Privacy
> d) Compliance, Audit, Portability
>> [!success]- Answer
>> b) Consistency, Availability, Partition Tolerance

> [!question] A Distributed Hash Table (DHT) provides:
> a) SQL querying
> b) Decentralized key-value storage and lookup
> c) File compression
> d) Network routing only
>> [!success]- Answer
>> b) Decentralized key-value storage and lookup

> [!question] Amazon S3 is an example of:
> a) Block storage
> b) Object storage
> c) File storage
> d) Cache storage
>> [!success]- Answer
>> b) Object storage

> [!question] Match the storage paradigm with its data organization.
>> [!example] Group A
>> a) Block storage
>> b) File storage
>> c) Object storage
>> d) Key-value storage
>
>> [!example] Group B
>> n) Data divided into fixed-size blocks with addresses
>> o) Organized in hierarchical directories and files
>> p) Data stored as objects with unique IDs and metadata
>> q) Data stored as key-value pairs
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the CAP theorem property with its meaning.
>> [!example] Group A
>> a) Consistency
>> b) Availability
>> c) Partition Tolerance
>> d) Trade-off
>
>> [!example] Group B
>> n) All nodes see the same data at the same time
>> o) Every request receives a response
>> p) System continues despite network failures
>> q) Must sacrifice one property in distributed systems
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the DHT concept with its description.
>> [!example] Group A
>> a) Key
>> b) Value
>> c) Node
>> d) Ring
>
>> [!example] Group B
>> n) Unique identifier for stored data
>> o) Data associated with the key
>> p) Participant storing a portion of the data
>> q) Circular keyspace topology in consistent hashing
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the consistency model with its guarantee.
>> [!example] Group A
>> a) Strong consistency
>> b) Eventual consistency
>> c) Causal consistency
>> d) Read-your-writes consistency
>
>> [!example] Group B
>> n) All nodes return the most recent write
>> o) System will converge over time
>> p) Related events are seen in correct order
>> q) User always sees their own updates
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the cloud storage product with its type.
>> [!example] Group A
>> a) Amazon S3
>> b) Amazon EBS
>> c) Amazon EFS
>> d) Amazon Glacier
>
>> [!example] Group B
>> n) Object storage with unlimited scalability
>> o) Block storage for EC2 instances
>> p) File storage with shared access
>> q) Archival storage at low cost
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
