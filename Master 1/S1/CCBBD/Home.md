# Cloud Computing, Big Data, and Distributed Systems — Vault Index

A comprehensive, unified knowledge base covering cloud computing from physical infrastructure to distributed architecture patterns, big data processing frameworks, and practical lab exercises. All content from both vaults has been merged, deduplicated, and logically ordered into nine chapters.

---

## Chapter 1 - Introduction to Cloud Computing

Foundational concepts: what the cloud is, how it evolved, its defining characteristics, and the major paradigms it introduces.

| # | File | Topic |
|---|------|-------|
| 1.1 | [[1.1 Cloud Computing Definition and Foundations]] | Cloud definition; Essential characteristics; Service and deployment models |
| 1.2 | [[1.2 Historical Evolution of Computing Paradigms]] | Mainframe, Client-Server, Grid, P2P, Utility, and Cloud computing evolution |
| 1.3 | [[1.3 NIST Characteristics of Cloud Computing]] | NIST SP 800-145; On-Demand Self-Service, Resource Pooling, Measured Service |
| 1.4 | [[1.4 Cloud vs On-Premise Strategic Analysis]] | CAPEX vs OPEX; Scalability comparison; Strategic decision framework |
| 1.5 | [[1.5 Evolution, Elasticity, and Scalability Mechanics]] | From Mainframes to Cloud; Scalability vs Elasticity; Scale-Up vs Scale-Out |
| 1.6 | [[1.6 The Five Essential NIST Characteristics and Financial Models]] | NIST definition; On-Demand Self-Service through Measured Service; CAPEX vs OPEX |
| 1.7 | [[1.7 The Historical Paradigm Shifts Preceding Cloud Computing]] | Mainframe, Client-Server, Grid, P2P, Utility Computing contributions |
| 1.8 | [[1.8 What The Cloud Means]] | Cloud definition; Data Center, VM, Server; Cloud workflow; Simulation context |
| 1.9 | [[1.9 Understanding Cloud Providers, Hosting Services, and VPS]] | Hosting vs Cloud provider; Access levels; VPS explained; Cloud vs VPS hierarchy |
| 1.10 | [[1.10 What is a Workload]] | Workload definition; Deployment process; Hosting levels; Where your website lives |
| 1.11 | [[1.11 What is Serverless]] | Serverless internals; Node.js fit; Platform deep dives (Cloudflare, Vercel, Supabase, Firebase, Atlas); Request lifecycle |

---

## Chapter 2 - Service and Deployment Models

Who manages what, how services are delivered, and where the infrastructure lives.

| # | File | Topic |
|---|------|-------|
| 2.1 | [[2.1 Hierarchical Cloud Infrastructure and Architecture]] | Infrastructure layers; Architectural hierarchy; Component relationships |
| 2.2 | [[2.2 Cloud Service Models - IaaS PaaS SaaS Deep Dive]] | IaaS/PaaS/SaaS detailed analysis; Responsibility boundaries; Use cases |
| 2.3 | [[2.3 The Shared Responsibility Model]] | Security responsibility split; Provider vs Customer; Data classification |
| 2.4 | [[2.4 Cloud Deployment Models - Public Private Hybrid Community]] | Deployment model comparison; Use case selection; Multi-cloud strategy |
| 2.5 | [[2.5 Cloud Architecture Layers and Responsibility Boundaries]] | Frontend vs Backend; Shared Responsibility Model (IaaS, PaaS, SaaS) |
| 2.6 | [[2.6 Cloud Deployment Architectures and Network Trade-offs]] | Public, Private, Hybrid (Cloud Bursting), Community Cloud |
| 2.7 | [[2.7 What is VPS and EC2]] | VPS definition and mechanics; EC2 and Auto Scaling Groups; VPS vs EC2 |
| 2.8 | [[2.8 What is a VPC]] | VPC definition; Key features and components; AWS-specific details; VPC vs Normal Cloud vs Physical Server |

---

## Chapter 3 - Virtualization

The technology that enables cloud computing: hypervisors, VMs, physical infrastructure, security, and migration.

| # | File | Topic |
|---|------|-------|
| 3.1 | [[3.1 Core Virtualization Concepts and Hypervisors]] | Hypervisor fundamentals; Virtualization types; Hardware abstraction |
| 3.2 | [[3.2 Anatomy and Technical Composition of a Virtual Machine]] | VM components; Resource allocation; Virtual hardware |
| 3.3 | [[3.3 Virtual Machine Migration Techniques]] | Live migration; Cold migration; Storage migration; Migration use cases |
| 3.4 | [[3.4 Advanced Virtualization Paradigms and Security]] | Nested virtualization; Container-VM hybrid; Security implications |
| 3.5 | [[3.5 Hypervisor Internals and Execution Types]] | CPU Rings; Full/Para/Hardware-Assisted virtualization; Type 1 vs Type 2; Core jobs |
| 3.6 | [[3.6 VM Migration Mechanisms and State Transfer]] | Pre-Copy Migration; Post-Copy Migration; Dirty page tracking |
| 3.7 | [[3.7 What is a Virtual Machine]] | VM definition; Where it lives; Physical vs Virtual; Nested virtualization |
| 3.8 | [[3.8 The Physical Machine - Racks, Servers, and Data Centers]] | Rack description; Servers; Data center hierarchy; Inside a server |
| 3.9 | [[3.9 What a Rack Unit Really Means]] | 1U definition; Device types; 42U layout example |
| 3.10 | [[3.10 A Server is Not the Rack]] | Rack vs Server distinction; Physical hierarchy |
| 3.11 | [[3.11 Anatomy of a Virtual Machine and File Structures]] | .vmx, .vmdk, .nvram, .vswp, .log files; Memory overcommitment |
| 3.12 | [[3.12 Virtualization Security Risks and Threat Vectors]] | VM Escape; VM Sprawl; Hyperjacking; VM Hopping |
| 3.13 | [[3.13 Hardware Emulation vs System Virtualization]] | Instruction Set Architectures; Emulation (translation) vs Virtualization (allocation) |

---

## Chapter 4 - Architecture and Communication Patterns

How distributed systems communicate: microservices, message queues, event-driven architecture, and the broker layer.

| # | File | Topic |
|---|------|-------|
| 4.1 | [[4.1 What are Microservices]] | Microservices definition; Core idea; Monolith vs Microservices; Cloud deployment |
| 4.2 | [[4.2 What are Message Queues and Event-driven Patterns]] | Synchronous vs Asynchronous; MQ definition and tools; Event-Driven pattern; MQ vs EDA |
| 4.3 | [[4.3 What is a Broker]] | Broker role; Where it lives; Clusters; Broker responsibilities; Cloud deployment |
| 4.4 | [[4.4 Event-Driven Architecture (EDA)]] | EDA lifecycle; Event patterns; CQRS; Sagas; Event sourcing; Benefits and challenges |
| 4.5 | [[4.5 The Publisher-Subscriber Model]] | Pub/Sub mechanics; Topic-based vs Content-based routing; Hierarchical topics; Relationship to EDA |
| 4.6 | [[4.6 Why Node.js Fits Serverless So Well]] | Serverless runtime requirements; Language-by-language comparison; Modern workarounds |

---

## Chapter 5 - Containerization and Orchestration

Container technology: from Linux kernel primitives to Kubernetes orchestration.

| # | File | Topic |
|---|------|-------|
| 5.1 | [[5.1 Linux Kernel Isolation Mechanics - Namespaces and Cgroups]] | Namespace types (PID, NET, MNT, UTS); Cgroup controllers; Container isolation primitives |
| 5.2 | [[5.2 Docker Engine Architecture and Core Components]] | Docker daemon; containerd; runc; Client-Server architecture; Image management |
| 5.3 | [[5.3 Dockerfile Mechanics and Multi-Container Applications]] | Dockerfile instructions; Layer caching; Multi-stage builds; Docker Compose |
| 5.4 | [[5.4 Container Orchestration and Kubernetes Foundations]] | Orchestration need; Kubernetes architecture; Cluster components |
| 5.5 | [[5.5 Kubernetes Control Plane and Worker Node Architecture]] | API Server, Scheduler, Controller Manager, etcd; Kubelet, kube-proxy, container runtime |
| 5.6 | [[5.6 Pod Scheduling, Resource Management, and Services]] | Pod lifecycle; Scheduling policies; Resource requests/limits; Service types |
| 5.7 | [[5.7 Linux Kernel Internals (Namespaces, Cgroups, UnionFS)]] | Namespaces (PID, NET, MNT, UTS); Cgroups; OverlayFS; Copy-on-Write |
| 5.8 | [[5.8 Kubernetes Architecture and Pod Scheduling Workflow]] | Control Plane; Worker Nodes; Pod concept; Scheduling workflow |
| 5.9 | [[5.9 Docker Engine Architecture and Container Lifecycle]] | Docker Daemon; Client-Server architecture; Container states |
| 5.10 | [[5.10 Dockerfile Layering and Image Build Mechanics]] | Dockerfile instructions; Layer caching; Multi-stage builds; Best practices |
| 5.11 | [[5.11 Microservices, Docker Compose, and Container Networking]] | Docker Compose; Bridge/Overlay/Host networking; Service discovery |
| 5.12 | [[5.12 Kubernetes Networking, Services, and Configuration Management]] | Ephemeral IP problem; ClusterIP/NodePort/LoadBalancer; kube-proxy; ConfigMaps and Secrets |

---

## Chapter 6 - Virtual and Networked Storage

How storage works in cloud environments: from physical disks to software-defined storage pools.

| # | File | Topic |
|---|------|-------|
| 6.1 | [[6.1 Storage Foundations and Access Models]] | Storage hierarchy; Access methods; Performance characteristics |
| 6.2 | [[6.2 Networked Storage Architectures - DAS NAS SAN]] | DAS, NAS, SAN comparison; Block vs File access; HCI evolution |
| 6.3 | [[6.3 Storage Virtualization, Datastores, and High Availability]] | Storage pooling; Datastore types; HA strategies; Replication |
| 6.4 | [[6.4 Block vs File Access and SAN vs NAS Architectures]] | Block vs File access; DAS, NAS, SAN; HCI evolution |
| 6.5 | [[6.5 RAID, Datastores, and Advanced Storage Features]] | RAID levels (0, 1, 5, 6, 10); Thin vs Thick provisioning; Snapshots; Deduplication |
| 6.6 | [[6.6 Solving Storage Silos with Virtualization and Pooling]] | Storage silo problem; Storage virtualization; HCI revolution |

---

## Chapter 7 - Cloud Storage and Distributed Systems

Distributed storage paradigms, data partitioning strategies, and consistency models in large-scale systems.

| # | File | Topic |
|---|------|-------|
| 7.1 | [[7.1 Cloud Storage Paradigms - Block File Object]] | Block, File, and Object storage comparison; Access patterns; Use cases |
| 7.2 | [[7.2 Distributed Hash Tables and Consistent Hashing]] | DHT fundamentals; Consistent hashing; Ring topology; Data distribution |
| 7.3 | [[7.3 Data Consistency Models and CAP Theorem]] | Strong vs Eventual consistency; CAP theorem; PACELC; Trade-off analysis |

---

## Chapter 8 - Big Data Processing Frameworks

Big data infrastructure: Hadoop ecosystem, HDFS, MapReduce, and Spark for large-scale distributed computation.

| # | File | Topic |
|---|------|-------|
| 8.1 | [[8.1 Big Data Foundations and Architecture]] | Big Data definition (3Vs); Lambda architecture; Batch vs Stream processing |
| 8.2 | [[8.2 Apache Hadoop Ecosystem and HDFS]] | HDFS architecture; NameNode/DataNode; Block replication; Rack awareness |
| 8.3 | [[8.3 MapReduce Programming Model and Execution Engine]] | Map/Reduce phases; Shuffle and Sort; YARN resource management; WordCount example |
| 8.4 | [[8.4 Apache Spark In-Memory Computation Engine]] | RDD concept; DAG execution; Transformations vs Actions; Spark vs MapReduce comparison |

---

## Chapter 9 - Practical Labs and Solutions

Hands-on exercises: OpenStack provisioning, YAFS simulation, Nextcloud deployment, MinIO automation, and MapReduce compilation.

| # | File | Topic |
|---|------|-------|
| 9.1 | [[9.1 TP 1 - Cloud Provisioning with OpenStack and Taikun]] | OpenStack setup; Taikun CLI; Instance provisioning; Cloud resource management |
| 9.2 | [[9.2 TP 2 - Discrete Event Simulation of Cloud Topologies via YAFS]] | YAFS framework; Cloud topology simulation; Discrete event modeling |
| 9.3 | [[9.3 TP 4 and 5 - Private Cloud Deployment with Nextcloud and Docker]] | Nextcloud deployment; Docker Compose setup; Private cloud configuration |
| 9.4 | [[9.4 TP 6 - Cloud Storage Automation and Persistance with MinIO]] | MinIO object storage; S3-compatible API; Automation scripts; Persistence configuration |
| 9.5 | [[9.5 TP 7 - Distributed MapReduce Compilation and Execution on Hadoop]] | Java MapReduce compilation; Hadoop job submission; Distributed execution |

---

## Reading Order

For a complete top-to-bottom understanding, read the chapters in order:

1. **Chapter 1** — What the cloud is, why it exists, and its fundamental characteristics
2. **Chapter 2** — How services are delivered and where infrastructure lives
3. **Chapter 3** — The virtualization technology that makes cloud computing possible
4. **Chapter 4** — How distributed systems communicate and coordinate
5. **Chapter 5** — Containerization technology from kernel primitives to orchestration
6. **Chapter 6** — How storage works in virtualized and cloud environments
7. **Chapter 7** — Distributed storage paradigms, DHTs, and consistency models
8. **Chapter 8** — Big data processing frameworks for large-scale computation
9. **Chapter 9** — Practical hands-on labs applying the concepts

Each chapter's files are numbered sequentially and build on each other.