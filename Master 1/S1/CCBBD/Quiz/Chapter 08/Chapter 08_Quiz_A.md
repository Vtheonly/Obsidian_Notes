---
sources:
  - "[[Chapter 8 - Big Data Processing Frameworks/8.1 Big Data Foundations and Architecture.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.2 Apache Hadoop Ecosystem and HDFS.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.3 MapReduce Programming Model and Execution Engine.md]]"
  - "[[Chapter 8 - Big Data Processing Frameworks/8.4 Apache Spark In-Memory Computation Engine.md]]"
---

> [!question] Big Data is characterized by the 3 Vs: Volume, Velocity, and Variety.
>> [!success]- Answer
>> True

> [!question] Apache Hadoop includes HDFS as its distributed file system.
>> [!success]- Answer
>> True

> [!question] MapReduce is a programming model for processing large datasets in parallel.
>> [!success]- Answer
>> True

> [!question] In MapReduce, the Reduce phase sorts and groups data before the Map phase.
>> [!success]- Answer
>> False

> [!question] Apache Spark performs in-memory computation for faster processing.
>> [!success]- Answer
>> True

> [!question] The three Vs of Big Data are:
> a) Value, Verification, Visualization
> b) Volume, Velocity, Variety
> c) Viability, Volatility, Validity
> d) Verbosity, Vagueness, Virtue
>> [!success]- Answer
>> b) Volume, Velocity, Variety

> [!question] HDFS stores files by:
> a) Storing entire files on one node
> b) Splitting files into blocks distributed across nodes
> c) Compressing files in memory
> d) Storing everything in RAM
>> [!success]- Answer
>> b) Splitting files into blocks distributed across nodes

> [!question] MapReduce consists of which two main phases?
> a) Read and Write
> b) Map and Reduce
> c) Sort and Search
> d) Split and Merge
>> [!success]- Answer
>> b) Map and Reduce

> [!question] Apache Spark performs computations primarily in:
> a) Disk storage
> b) Memory (RAM)
> c) CPU cache
> d) Network buffers
>> [!success]- Answer
>> b) Memory (RAM)

> [!question] The NameNode in HDFS manages:
> a) User authentication
> b) Filesystem metadata and namespace
> c) Data blocks
> d) Network routing
>> [!success]- Answer
>> a) Filesystem metadata and namespace

> [!question] Match the Big Data characteristic with its description.
>> [!example] Group A
>> a) Volume
>> b) Velocity
>> c) Variety
>> d) Veracity
>
>> [!example] Group B
>> n) Massive quantity of data generated
>> o) Speed at which data is generated and processed
>> p) Different types of data formats and sources
>> q) Quality and trustworthiness of data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Hadoop component with its function.
>> [!example] Group A
>> a) HDFS
>> b) MapReduce
>> c) YARN
>> d) NameNode
>
>> [!example] Group B
>> n) Distributed file system for data storage
>> o) Programming model for parallel data processing
>> p) Resource management and job scheduling
>> q) Metadata management for HDFS
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the MapReduce phase with its activity.
>> [!example] Group A
>> a) Map phase
>> b) Shuffle phase
>> c) Sort phase
>> d) Reduce phase
>
>> [!example] Group B
>> n) Processes input data to produce key-value pairs
>> o) Transfers data from mappers to reducers
>> p) Orders data by key for reduce processing
>> q) Aggregates and combines values by key
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Spark concept with its definition.
>> [!example] Group A
>> a) RDD
>> b) DataFrame
>> c) Dataset
>> d) DAG
>
>> [!example] Group B
>> n) Resilient Distributed Dataset - immutable collection
>> o) Distributed collection organized into named columns
>> p) Strongly typed API with optimization benefits
>> q) Directed Acyclic Graph of computation stages
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Spark component with its role.
>> [!example] Group A
>> a) Driver
>> b) Executor
>> c) Cluster Manager
>> d) SparkContext
>
>> [!example] Group B
>> n) Main program that coordinates Spark application
>> o) Worker process running tasks on nodes
>> p) Manages resource allocation across cluster
>> q) Entry point for connecting to Spark cluster
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
