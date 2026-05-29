---
sources:
  - "[[Chapter 8 - Big Data Processing Frameworks/8.1 Big Data Foundations and Architecture.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.2 Apache Hadoop Ecosystem and HDFS.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.3 MapReduce Programming Model and Execution Engine.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.4 Apache Spark In-Memory Computation Engine.md]]"
---

> [!question] HDFS stores data in fixed-size blocks distributed across a cluster.
>> [!success]- Answer
>> True

> [!question] Spark can run workloads 100x faster than Hadoop MapReduce for some tasks.
>> [!success]- Answer
>> True

> [!question] The NameNode manages metadata in a Hadoop cluster.
>> [!success]- Answer
>> True

> [!question] Data locality means moving computation to where the data resides.
>> [!success]- Answer
>> True

> [!question] MapReduce jobs always require a cluster of at least three nodes.
>> [!success]- Answer
>> False

> [!question] Data locality in Hadoop means:
> a) Moving data to the computation
> b) Moving computation to where data resides
> c) Storing data in a local database
> d) Using only local disks
>> [!success]- Answer
>> b) Moving computation to where data resides

> [!question] Spark RDD stands for:
> a) Rapid Data Distribution
> b) Resilient Distributed Dataset
> c) Random Data Duplication
> d) Reduced Data Delay
>> [!success]- Answer
>> b) Resilient Distributed Dataset

> [!question] Which framework performs in-memory processing for faster analytics?
> a) Apache Hadoop MapReduce
> b) Apache Spark
> c) Apache Hadoop only
> d) Apache Hive
>> [!success]- Answer
>> b) Apache Spark

> [!question] MapReduce is best suited for:
> a) Real-time streaming
> b) Batch processing of large datasets
> c) Interactive queries
> d) Transaction processing
>> [!success]- Answer
>> b) Batch processing of large datasets

> [!question] HDFS data blocks are replicated across:
> a) Single node for speed
> b) Multiple nodes for fault tolerance
> c) Only the NameNode
> d) External storage
>> [!success]- Answer
>> b) Multiple nodes for fault tolerance

> [!question] Match the Big Data processing model with its description.
>> [!example] Group A
>> a) Batch processing
>> b) Stream processing
>> c) Real-time processing
>> d) Interactive processing
>
>> [!example] Group B
>> n) Processing large datasets at scheduled intervals
>> o) Continuous processing of data in motion
>> p) Immediate processing with low latency
>> q) Ad-hoc queries and exploration of data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the HDFS concept with its description.
>> [!example] Group A
>> a) Block size
>> b) Replication factor
>> c) DataNode
>> d) Secondary NameNode
>
>> [!example] Group B
>> n) Default 128 MB in modern Hadoop
>> o) Number of copies of each data block
>> p) Worker node that stores actual data blocks
>> q) Checkpoints NameNode metadata for recovery
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the optimization technique with its benefit.
>> [!example] Group A
>> a) Data locality
>> b) In-memory computing
>> c) Partitioning
>> d) Caching
>
>> [!example] Group B
>> n) Reduces network transfer by processing near data
>> o) Eliminates disk I/O bottlenecks
>> p) Enables parallel processing of subsets
>> q) Stores intermediate results for reuse
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Big Data tool with its category.
>> [!example] Group A
>> a) Apache Hive
>> b) Apache HBase
>> c) Apache Pig
>> d) Apache Flume
>
>> [!example] Group B
>> n) Data warehouse and SQL-like queries
>> o) NoSQL columnar database
>> p) Data flow scripting language
>> q) Log data collection and aggregation
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the processing framework with its characteristic.
>> [!example] Group A
>> a) Hadoop MapReduce
>> b) Apache Spark
>> c) Apache Flink
>> d) Apache Storm
>
>> [!example] Group B
>> n) Disk-based batch processing
>> o) In-memory batch and stream processing
>> p) True stream processing with event time
>> q) Real-time stream processing system
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
