# DBMS Architectures, Specialized Models & NoSQL Internals

*(Supplementary Advanced Database Systems module consolidated cleanly from the prior vault and separated from Views.)*

---

## 1. System Architectures, Data Independence & Legacy Flaws

### Client-Server vs. Distributed Architectures
- **Client-Server (2-Tier):** Clients submit SQL queries to one centralized DBMS server. Simple security and administration, but creates a Single Point of Failure (SPOF) and scales mostly **vertically** (bigger hardware).
- **Distributed Architecture:** Spreads storage/processing across multiple nodes for fault tolerance, load balancing, and geographic proximity:
  1. **Replication:** Full dataset copied across nodes $\to$ high availability and fast reads; write synchronization is harder.
  2. **Fragmentation (Sharding):** Table split across servers (rows `A–M` on Node 1, `N–Z` on Node 2) $\to$ parallelizes writes; cross-node joins become expensive.
  3. **Hybrid:** Combines fragmentation and replication.

### ANSI/SPARC Data Independence & Legacy Model Failures
- **Physical Data Independence:** Changing physical storage (HDD $\to$ SSD, adding a B+ tree index on `LastName`) does **not** require rewriting application SQL queries.
- **Logical Data Independence:** Splitting `EMPLOYEE(EmpID, Name, Department)` into normalized `EMPLOYEE` + `DEPARTMENT` tables does **not** break legacy apps if an External **View** exposes the original layout.
- **Why Legacy Models (Hierarchical & Network) Failed:** (1) Required brittle manual pointer traversal in code; (2) suffered the **Orphan Problem** (in strict hierarchies, deleting a `Department` destroyed child `Employee`s and children couldn't exist without parents; M:N failed); (3) extreme **path rigidity** (querying outside the physical tree order forced full scans).

---

## 2. Specialized Database Models

| Model | Core Problem Solved & Mechanics | Ideal Use Cases & Examples |
| :--- | :--- | :--- |
| **Object-Oriented (OODBMS)** | Solves the **Object-Relational Impedance Mismatch** (like parking a whole car in a garage rather than disassembling it into drawers like SQL, eliminating ORMs such as **Hibernate**). Stores objects directly with **attributes + methods**, inheritance (`Person` $\leftarrow$ `Student`), and polymorphism. | CAD/CAM, engineering simulations, complex nested objects (`ObjectDB`, `db4o`). |
| **Multimedia DB** | Handles large **BLOBs** (audio, video, images) with automatic metadata extraction (GPS, date, resolution), **Content-Based Retrieval (CBR)** (searching by color/features instead of filename), and streaming I/O. | Digital Asset Management (`Oracle Multimedia`). |
| **Time-Series DB (TSDB)** | Write-optimized ingestion indexed by **timestamp** (handling millions of IoT readings/sec without choking B-trees), automatic **downsampling** (rolling millisecond data into minute/day averages), and retention expiration. | IoT sensors, stock tickers, CPU telemetry (`InfluxDB`, `Prometheus`, `TimescaleDB`). |

---

## 3. NoSQL Paradigms, CAP Theorem & Physical Internals

### The CAP Theorem
In a distributed database, you can guarantee at most **two of three** properties simultaneously:
- **C — Consistency:** Every read returns the most recent write or an error.
- **A — Availability:** Every request receives a non-error response (even if slightly stale).
- **P — Partition Tolerance:** System keeps operating when network links drop between nodes.
Because network partitions ($P$) inevitably occur in real clusters, distributed systems must choose **CP** (consistency over availability) or **AP** (availability / eventual consistency).

### The Four NoSQL Families & Storage Mechanics

#### 1. Key-Value Stores (`Redis`, `DynamoDB`, `Riak`)
A distributed hash map (`PUT`, `GET`, `DELETE`) achieving $\mathcal{O}(1)$ lookups on opaque value blobs (cannot query inside values like `WHERE age > 18`). Ideal for caching, login sessions, and shopping carts.

#### 2. Document Stores (`MongoDB`, `CouchDB`, `Couchbase`)
Schema-flexible JSON documents grouped into **Collections** (equivalent to tables), allowing nested lists/sub-objects without joins.
- **BSON (Binary JSON):** MongoDB encodes JSON into binary BSON containing **field lengths and type byte-offsets**, allowing instant memory-offset jumps to fields without parsing the entire text string; every document has an immutable clustered `_id`.
- **JSONiq:** Declarative query language built for nested semi-structured JSON (`for $user in collection("users") where $user.profile.age > 30 return { "name": $user.name };`).

#### 3. Wide-Column / Column-Oriented Stores (`Cassandra`, `HBase`, `BigTable`)
- **Row-Oriented (OLTP) vs. Column-Oriented (OLAP):** Row stores read entire rows (`SELECT AVG(salary)` wastes I/O reading names/emails); column stores pack each column contiguously, cutting disk I/O and enabling heavy compression (e.g., Run-Length Encoding), at the cost of slower single-row writes.
- **4D Sparse Nested Map:** `[RowKey] -> [ColumnFamily] -> [Column] -> [Timestamp] = Value`. If `user_123` has `email` and `user_456` only has `city`, missing columns consume **0 bytes** (no `NULL` padding!).
- **Write Path & Conflict Resolution:** Writes hit RAM **MemTable + WAL** $\to$ flush to immutable disk **SSTables** $\to$ background **Compaction** merges SSTables. Cell microsecond timestamps implement **Last Write Wins (LWW)**.
- **Tombstones (Preventing Zombie Deletes):** `DELETE` writes a timestamped **Tombstone** marker rather than erasing immediately, so an offline replica returning online sees the newer Tombstone instead of resurrecting the deleted record before Compaction removes it.

#### 4. Graph Databases (`Neo4j`, `OrientDB`)
Models **Nodes** (entities), directed **Edges** (relationships), and **Properties** on both (`since: 2015`), queried with `Cypher`/`Gremlin`.
- **Index-Free Adjacency:** Each node physically stores direct memory pointers to neighbor nodes, traversing multi-hop "friends-of-friends" or fraud rings in **$\mathcal{O}(1)$ per hop** instead of $\mathcal{O}(\log n)$ SQL index joins.

*(Multi-model engines like **ArangoDB** and **CosmosDB** combine Key-Value, Document, and Graph models in one server; **DBaaS** platforms like RDS/Firestore offload ops. Always remember: NoSQL is not universally "faster than SQL"—choose SQL for complex joins and strict ACID, and NoSQL for schema flexibility or massive horizontal throughput.)*
