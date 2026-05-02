# Cloud Computing - Vault Index

A comprehensive, unified knowledge base covering cloud computing from physical infrastructure to distributed architecture patterns. All content has been merged, deduplicated, and logically ordered into six chapters.

---

## Chapter 1 - Introduction to Cloud Computing

Foundational concepts: what the cloud is, how it evolved, its defining characteristics, and the major paradigms it introduces.

| File | Topic |
|------|-------|
| [[1.1 Evolution, Elasticity, and Scalability Mechanics]] | From Mainframes to Cloud; Scalability vs Elasticity; Scale-Up vs Scale-Out |
| [[1.2 The Five Essential NIST Characteristics and Financial Models]] | NIST definition; On-Demand Self-Service through Measured Service; CAPEX vs OPEX |
| [[1.3 The Historical Paradigm Shifts Preceding Cloud Computing]] | Mainframe, Client-Server, Grid, P2P, Utility Computing contributions |
| [[1.4 What The Cloud Means]] | Cloud definition; Data Center, VM, Server; Cloud workflow; Simulation context |
| [[1.5 Understanding Cloud Providers, Hosting Services, and VPS]] | Hosting vs Cloud provider; Access levels; VPS explained; Cloud vs VPS hierarchy |
| [[1.6 What is a Workload]] | Workload definition; Deployment process; Hosting levels; Where your website lives |
| [[1.7 What is Serverless]] | Serverless internals; Node.js fit; Platform deep dives (Cloudflare, Vercel, Supabase, Firebase, Atlas); Request lifecycle |

---

## Chapter 2 - Service and Deployment Models

Who manages what, how services are delivered, and where the infrastructure lives.

| File | Topic |
|------|-------|
| [[2.1 Cloud Architecture Layers and Responsibility Boundaries]] | Frontend vs Backend; Shared Responsibility Model (IaaS, PaaS, SaaS) |
| [[2.2 Cloud Deployment Architectures and Network Trade-offs]] | Public, Private, Hybrid (Cloud Bursting), Community Cloud |
| [[2.3 What is VPS and EC2]] | VPS definition and mechanics; EC2 and Auto Scaling Groups; VPS vs EC2 |
| [[2.4 What is a VPC]] | VPC definition; Key features and components; AWS-specific details; VPC vs Normal Cloud vs Physical Server |

---

## Chapter 3 - Virtualization

The technology that enables cloud computing: hypervisors, VMs, physical infrastructure, security, and migration.

| File | Topic |
|------|-------|
| [[3.1 Hypervisor Internals and Execution Types]] | CPU Rings; Full/Para/Hardware-Assisted virtualization; Type 1 vs Type 2; Core jobs |
| [[3.2 VM Migration Mechanisms and State Transfer]] | Pre-Copy Migration; Post-Copy Migration; Dirty page tracking |
| [[3.3 What is a Virtual Machine]] | VM definition; Where it lives; Physical vs Virtual; Nested virtualization |
| [[3.4 The Physical Machine - Racks, Servers, and Data Centers]] | Rack description; Servers; Data center hierarchy; Inside a server |
| [[3.5 What a Rack Unit Really Means]] | 1U definition; Device types; 42U layout example |
| [[3.6 A Server is Not the Rack]] | Rack vs Server distinction; Physical hierarchy |
| [[3.7 Anatomy of a Virtual Machine and File Structures]] | .vmx, .vmdk, .nvram, .vswp, .log files; Memory overcommitment |
| [[3.8 Virtualization Security Risks and Threat Vectors]] | VM Escape; VM Sprawl; Hyperjacking; VM Hopping |
| [[3.9 Hardware Emulation vs System Virtualization]] | Instruction Set Architectures; Emulation (translation) vs Virtualization (allocation) |

---

## Chapter 4 - Architecture and Communication Patterns

How distributed systems communicate: microservices, message queues, event-driven architecture, and the broker layer.

| File | Topic |
|------|-------|
| [[4.1 What are Microservices]] | Microservices definition; Core idea; Monolith vs Microservices; Cloud deployment |
| [[4.2 What are Message Queues and Event-driven Patterns]] | Synchronous vs Asynchronous; MQ definition and tools; Event-Driven pattern; MQ vs EDA |
| [[4.3 What is a Broker]] | Broker role; Where it lives; Clusters; Broker responsibilities; Cloud deployment |
| [[4.4 Event-Driven Architecture (EDA)]] | EDA lifecycle; Event patterns; CQRS; Sagas; Event sourcing; Benefits and challenges |
| [[4.5 The Publisher-Subscriber Model]] | Pub/Sub mechanics; Topic-based vs Content-based routing; Hierarchical topics; Relationship to EDA |
| [[4.6 Why Node.js Fits Serverless So Well]] | Serverless runtime requirements; Language-by-language comparison; Modern workarounds |

---

## Chapter 5 - Docker Engine and Containerization

Container technology: from Linux kernel primitives to Kubernetes orchestration.

| File | Topic |
|------|-------|
| [[5.1 Linux Kernel Internals (Namespaces, Cgroups, UnionFS)]] | Namespaces (PID, NET, MNT, UTS); Cgroups; OverlayFS; Copy-on-Write |
| [[5.2 Kubernetes Architecture and Pod Scheduling Workflow]] | Control Plane; Worker Nodes; Pod concept; Scheduling workflow |
| [[5.3 Docker Engine Architecture and Container Lifecycle]] | Docker Daemon; Client-Server architecture; Container states |
| [[5.4 Dockerfile Layering and Image Build Mechanics]] | Dockerfile instructions; Layer caching; Multi-stage builds; Best practices |
| [[5.5 Microservices, Docker Compose, and Container Networking]] | Docker Compose; Bridge/Overlay/Host networking; Service discovery |
| [[5.6 Kubernetes Networking, Services, and Configuration Management]] | Ephemeral IP problem; ClusterIP/NodePort/LoadBalancer; kube-proxy; ConfigMaps and Secrets |

---

## Chapter 6 - Virtual Storage

How storage works in cloud environments: from physical disks to software-defined storage pools.

| File | Topic |
|------|-------|
| [[6.1 Block vs File Access and SAN vs NAS Architectures]] | Block vs File access; DAS, NAS, SAN; HCI evolution |
| [[6.2 RAID, Datastores, and Advanced Storage Features]] | RAID levels (0, 1, 5, 6, 10); Thin vs Thick provisioning; Snapshots; Deduplication |
| [[6.3 Solving Storage Silos with Virtualization and Pooling]] | Storage silo problem; Storage virtualization; HCI revolution |

---

## Reading Order

For a complete top-to-bottom understanding, read the chapters in order:

1. Start with **Chapter 1** to understand what the cloud is and why it exists
2. Move to **Chapter 2** to learn how services are delivered and deployed
3. Proceed to **Chapter 3** for the virtualization technology that makes it all possible
4. Continue to **Chapter 4** for how distributed systems communicate and coordinate
5. Then **Chapter 5** for containerization and orchestration
6. Finish with **Chapter 6** for how storage works in virtualized environments

Each chapter's files are numbered sequentially and build on each other.
