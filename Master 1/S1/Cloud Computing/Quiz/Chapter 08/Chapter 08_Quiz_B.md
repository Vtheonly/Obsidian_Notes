---
sources:
  - "[[Chapter 8 - Big Data Processing Frameworks/8.1 Big Data Foundations and Architecture.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.2 Apache Hadoop Ecosystem and HDFS.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.3 MapReduce Programming Model and Execution Engine.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.4 Apache Spark In-Memory Computation Engine.md]]"
---

> [!question] Big Data refers to datasets too large or complex for traditional databases to process.
>> [!success]- Answer
>> True

> [!question] The 5Vs of Big Data are Volume Velocity Variety Veracity and Value.
>> [!success]- Answer
>> True

> [!question] HDFS splits files into fixed-size blocks and replicates them across DataNodes.
>> [!success]- Answer
>> True

> [!question] In HDFS the NameNode stores the actual data blocks.
>> [!success]- Answer
>> False

> [!question] MapReduce consists of three phases: Map Shuffle & Sort and Reduce.
>> [!success]- Answer
>> True

> [!question] Apache Spark processes data in memory making it faster than MapReduce for iterative workloads.
>> [!success]- Answer
>> True

> [!question] YARN is responsible for distributed file storage in Hadoop.
>> [!success]- Answer
>> False

> [!question] MapReduce writes intermediate data to disk after each phase.
>> [!success]- Answer
>> True

> [!question] Spark RDDs are mutable collections of data that can be modified in place.
>> [!success]- Answer
>> False

> [!question] Apache Kafka is commonly used for real-time data ingestion in Big Data pipelines.
>> [!success]- Answer
>> True

> [!question] Which is NOT one of the 5Vs of Big Data?
> a) Volume
> b) Velocity
> c) Vulnerability
> d) Value
>> [!success]- Answer
>> c) Vulnerability

> [!question] What is the default replication factor in HDFS?
> a) 1
> b) 2
> c) 3
> d) 5
>> [!success]- Answer
>> c) 3

> [!question] Which Hadoop component manages resources and job scheduling?
> a) HDFS
> b) YARN
> c) MapReduce
> d) Hive
>> [!success]- Answer
>> b) YARN

> [!question] What is the primary advantage of Spark over MapReduce?
> a) Lower cost
> b) In-memory processing for faster iterative workloads
> c) Easier installation
> d) Better security
>> [!success]- Answer
>> b) In-memory processing for faster iterative workloads

> [!question] What is the role of the NameNode in HDFS?
> a) Store actual data blocks
> b) Manage filesystem namespace and metadata
> c) Execute Map tasks
> d) Provide network routing
>> [!success]- Answer
>> b) Manage filesystem namespace and metadata

> [!question] In MapReduce what does the Shuffle & Sort phase do?
> a) Splits the input data
> b) Groups intermediate key-value pairs by key and routes to reducers
> c) Writes final output to HDFS
> d) Encrypts data during transmission
>> [!success]- Answer
>> b) Groups intermediate key-value pairs by key and routes to reducers

> [!question] What is a DataNode in HDFS?
> a) Master node managing metadata
> b) Worker node that stores and retrieves data blocks
> c) Node that schedules jobs
> d) Node that manages network traffic
>> [!success]- Answer
>> b) Worker node that stores and retrieves data blocks

> [!question] What is a Spark RDD?
> a) A relational database
> b) Resilient Distributed Dataset - fault-tolerant collection of elements processed in parallel
> c) A type of Hadoop configuration
> d) A network protocol
>> [!success]- Answer
>> b) Resilient Distributed Dataset - fault-tolerant collection of elements processed in parallel

> [!question] What does HDFS rack awareness do?
> a) Distributes block replicas across different racks to prevent rack-level failures
> b) Speeds up network connections
> c) Reduces storage costs
> d) Manages user authentication
>> [!success]- Answer
>> a) Distributes block replicas across different racks to prevent rack-level failures

> [!question] Which tool is used for SQL-like querying on Hadoop?
> a) Apache Spark
> b) Apache Hive
> c) Apache Kafka
> d) Apache Sqoop
>> [!success]- Answer
>> b) Apache Hive

> [!question] Match the Big Data V with its description.
>> [!example] Group A
>> a) Volume
>> b) Velocity
>> c) Variety
>> d) Veracity
>
>> [!example] Group B
>> n) Scale of data (terabytes to exabytes)
>> o) Speed of data generation and processing
>> p) Diversity of data formats
>> q) Trustworthiness and quality of data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match Hadoop component with function.
>> [!example] Group A
>> a) HDFS
>> b) YARN
>> c) MapReduce
>> d) Hive
>
>> [!example] Group B
>> n) Distributed file storage
>> o) Resource management and job scheduling
>> p) Parallel processing programming model
>> q) SQL-like query engine on Hadoop
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match MapReduce phase with operation.
>> [!example] Group A
>> a) Map phase
>> b) Shuffle & Sort phase
>> c) Reduce phase
>> d) Input split
>
>> [!example] Group B
>> n) Transforms input into intermediate key-value pairs
>> o) Groups and sorts key-value pairs by key
>> p) Aggregates or summarizes grouped data
>> q) Divides input dataset into independent chunks
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match Spark component with function.
>> [!example] Group A
>> a) Spark Core
>> b) Spark SQL
>> c) Spark Streaming
>> d) MLlib
>
>> [!example] Group B
>> n) Basic RDD and DataFrame API
>> o) Structured data query engine
>> p) Real-time stream processing
>> q) Machine learning library
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match HDFS concept with role.
>> [!example] Group A
>> a) Block
>> b) NameNode
>> c) DataNode
>> d) Secondary NameNode
>
>> [!example] Group B
>> n) Fixed-size data unit (default 128MB)
>> o) Metadata manager
>> p) Block storage worker
>> q) Checkpoints NameNode metadata
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match Big Data pipeline stage with tool.
>> [!example] Group A
>> a) Ingestion
>> b) Storage
>> c) Processing
>> d) Analysis
>
>> [!example] Group B
>> n) Apache Kafka
>> o) HDFS or S3
>> p) MapReduce or Spark
>> q) Hive or Presto
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match data processing pattern with framework.
>> [!example] Group A
>> a) Batch processing
>> b) Stream processing
>> c) Iterative algorithms
>> d) Interactive queries
>
>> [!example] Group B
>> n) MapReduce or Spark batch
>> o) Spark Streaming or Flink
>> p) Spark (in-memory)
>> q) Presto or Impala
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match Spark optimization with benefit.
>> [!example] Group A
>> a) In-memory caching
>> b) Lazy evaluation
>> c) Lineage graph
>> d) Catalyst optimizer
>
>> [!example] Group B
>> n) Avoids recomputing intermediate results
>> o) Defers computation until action is called
>> p) RDD fault tolerance through transformation history
>> q) Query plan optimization for DataFrames
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match Hadoop ecosystem tool with category.
>> [!example] Group A
>> a) Apache Sqoop
>> b) Apache Oozie
>> c) Apache Flume
>> d) Apache HBase
>
>> [!example] Group B
>> n) Data transfer between Hadoop and RDBMS
>> o) Workflow scheduling and orchestration
>> p) Log data collection and aggregation
>> q) NoSQL database on HDFS
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match Big Data challenge with solution.
>> [!example] Group A
>> a) Fault tolerance
>> b) Scalability
>> c) Data locality
>> d) Metadata management
>
>> [!example] Group B
>> n) Data replication and speculative execution
>> o) Horizontal scaling with commodity hardware
>> p) Processing tasks near where data resides
>> q) Catalog services like Hive Metastore
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
