#!/usr/bin/env python3
"""
Quiz Generator for CCBBD Course.
Generates 2 quiz files per chapter (9 chapters = 18 files).
Each file: 10 TF + 10 MC + 10 Matching = 30 questions.
Strictly follows the Obsidian callout format required by the validator.
"""

import os

CHAPTERS = {
    "Chapter 01": [
        "Chapter 1 - Introduction to Cloud Computing",
        ["1.1 Cloud Computing Definition and Foundations.md",
         "1.2 Historical Evolution of Computing Paradigms.md",
         "1.3 NIST Characteristics of Cloud Computing.md",
         "1.4 Cloud vs On-Premise Strategic Analysis.md",
         "1.5 Evolution, Elasticity, and Scalability Mechanics.md",
         "1.6 The Five Essential NIST Characteristics and Financial Models.md"]
    ],
    "Chapter 02": [
        "Chapter 2 - Service and Deployment Models",
        ["2.1 Hierarchical Cloud Infrastructure and Architecture.md",
         "2.2 Cloud Service Models - IaaS PaaS SaaS Deep Dive.md",
         "2.3 The Shared Responsibility Model.md",
         "2.4 Cloud Deployment Models - Public Private Hybrid Community.md",
         "2.7 What is VPS and EC2.md",
         "2.8 What is a VPC.md"]
    ],
    "Chapter 03": [
        "Chapter 3 - Virtualization",
        ["3.1 Core Virtualization Concepts and Hypervisors.md",
         "3.2 Anatomy and Technical Composition of a Virtual Machine.md",
         "3.3 Virtual Machine Migration Techniques.md",
         "3.4 Advanced Virtualization Paradigms and Security.md",
         "3.7 What is a Virtual Machine.md",
         "3.8 The Physical Machine - Racks, Servers, and Data Centers.md"]
    ],
    "Chapter 04": [
        "Chapter 4 - Architecture and Communication Patterns",
        ["4.1 What are Microservices.md",
         "4.2 What are Message Queues and Event-driven Patterns.md",
         "4.3 What is a Broker.md",
         "4.4 Event-Driven Architecture (EDA).md",
         "4.5 The Publisher-Subscriber Model.md",
         "4.6 Why Node.js Fits Serverless So Well.md"]
    ],
    "Chapter 05": [
        "Chapter 5 - Containerization and Orchestration",
        ["5.1 Linux Kernel Isolation Mechanics - Namespaces and Cgroups.md",
         "5.2 Docker Engine Architecture and Core Components.md",
         "5.3 Dockerfile Mechanics and Multi-Container Applications.md",
         "5.4 Container Orchestration and Kubernetes Foundations.md",
         "5.5 Kubernetes Control Plane and Worker Node Architecture.md",
         "5.6 Pod Scheduling, Resource Management, and Services.md"]
    ],
    "Chapter 06": [
        "Chapter 6 - Virtual and Networked Storage",
        ["6.1 Storage Foundations and Access Models.md",
         "6.2 Networked Storage Architectures - DAS NAS SAN.md",
         "6.3 Storage Virtualization, Datastores, and High Availability.md",
         "6.4 Block vs File Access and SAN vs NAS Architectures.md",
         "6.5 RAID, Datastores, and Advanced Storage Features.md",
         "6.6 Solving Storage Silos with Virtualization and Pooling.md"]
    ],
    "Chapter 07": [
        "Chapter 7 - Cloud Storage and Distributed Systems",
        ["7.1 Cloud Storage Paradigms - Block File Object.md",
         "7.2 Distributed Hash Tables and Consistent Hashing.md",
         "7.3 Data Consistency Models and CAP Theorem.md"]
    ],
    "Chapter 08": [
        "Chapter 8 - Big Data Processing Frameworks",
        ["8.1 Big Data Foundations and Architecture.md",
         "8.2 Apache Hadoop Ecosystem and HDFS.md",
         "8.3 MapReduce Programming Model and Execution Engine.md",
         "8.4 Apache Spark In-Memory Computation Engine.md"]
    ],
    "Chapter 09": [
        "Chapter 9 - Practical Labs and Solutions",
        ["9.1 TP 1 - Cloud Provisioning with OpenStack and Taikun.md",
         "9.2 TP 2 - Discrete Event Simulation of Cloud Topologies via YAFS.md",
         "9.3 TP 4 and 5 - Private Cloud Deployment with Nextcloud and Docker.md",
         "9.4 TP 6 - Cloud Storage Automation and Persistance with MinIO.md",
         "9.5 TP 7 - Distributed MapReduce Compilation and Execution on Hadoop.md"]
    ]
}

def make_sources(chapter_dir, files):
    sources = []
    for f in files:
        sources.append(f'  - "[[{chapter_dir}/{f}]]"')
    return "\n".join(sources)

# ----- Question Banks per Chapter -----

TF_BANKS = {
    "Chapter 01": [
        ("Cloud Computing enables on-demand network access to a shared pool of configurable computing resources.", True),
        ("Cloud Computing requires users to purchase physical hardware assets before using services.", False),
        ("The NIST definition of Cloud Computing includes five essential characteristics.", True),
        ("Elasticity in cloud computing means resources can be automatically scaled up or down based on demand.", True),
        ("On-premise infrastructure typically has lower upfront costs compared to cloud solutions.", False),
        ("Serverless computing still requires the user to manage virtual machines.", False),
        ("A workload is a specific application or service that runs on cloud resources.", True),
        ("Scalability refers only to increasing resources, never decreasing them.", False),
        ("Cloud providers follow a pay-as-you-go financial model.", True),
        ("The evolution of cloud computing began with the invention of the internet in the 1990s.", False),
    ],
    "Chapter 02": [
        ("IaaS provides virtualized computing resources over the internet.", True),
        ("In PaaS, the consumer manages the operating system and middleware.", False),
        ("SaaS applications are accessed via a web browser without local installation.", True),
        ("In the Shared Responsibility Model, the cloud provider is always responsible for everything.", False),
        ("Public cloud deployment means resources are shared across multiple unrelated organizations.", True),
        ("Private cloud is only deployable on-premise.", False),
        ("A hybrid cloud combines public and private cloud infrastructure.", True),
        ("Community cloud is shared by several organizations with common concerns.", True),
        ("VPS stands for Virtual Private Server and is an example of IaaS.", True),
        ("VPC stands for Virtual Public Cloud.", False),
    ],
    "Chapter 03": [
        ("A hypervisor is software that creates and manages virtual machines.", True),
        ("Type 1 hypervisors run directly on the host hardware.", True),
        ("Type 2 hypervisors run on top of an existing operating system.", True),
        ("VM migration can transfer a running virtual machine between physical hosts.", True),
        ("Memory overcommitment is not possible in virtualized environments.", False),
        ("Hardware emulation simulates entire hardware components in software.", True),
        ("A virtual machine includes virtual CPU, memory, storage, and network interfaces.", True),
        ("Containers use less overhead than full virtual machines.", True),
        ("Virtualization security risks include VM escape attacks.", True),
        ("A rack unit (U) is a standard measurement equal to 1.75 inches.", True),
    ],
    "Chapter 04": [
        ("Microservices architecture splits an application into small, independent services.", True),
        ("Message queues enable asynchronous communication between services.", True),
        ("A broker is a component that routes messages between producers and consumers.", True),
        ("Event-Driven Architecture (EDA) relies on the production and consumption of events.", True),
        ("In the Publisher-Subscriber model, publishers send messages directly to specific subscribers.", False),
        ("Node.js is well-suited for serverless computing due to its event-driven nature.", True),
        ("Microservices always require a message broker to communicate.", False),
        ("Event-driven architectures are always synchronous by nature.", False),
        ("A broker can provide message persistence and delivery guarantees.", True),
        ("Tight coupling is a goal of microservices architecture.", False),
    ],
    "Chapter 05": [
        ("Namespaces provide process isolation in the Linux kernel.", True),
        ("Cgroups control and limit resource usage of processes.", True),
        ("Docker uses a client-server architecture.", True),
        ("Docker images are built in read-only layers.", True),
        ("Kubernetes is a container orchestration platform.", True),
        ("A Kubernetes cluster consists of a control plane and worker nodes.", True),
        ("A Pod in Kubernetes is the smallest deployable unit.", True),
        ("Docker Compose is used for managing single-container applications.", False),
        ("UnionFS allows filesystem layers to be stacked and shared.", True),
        ("Kubernetes Services provide stable network endpoints for Pods.", True),
    ],
    "Chapter 06": [
        ("DAS stands for Directly Attached Storage.", True),
        ("NAS provides file-level data access over a network.", True),
        ("SAN provides block-level data access over a dedicated network.", True),
        ("RAID 0 provides redundancy through data mirroring.", False),
        ("RAID 5 uses striping with distributed parity.", True),
        ("Storage virtualization pools physical storage from multiple devices.", True),
        ("A datastore is a logical container for virtual machine files.", True),
        ("Block access is typically slower than file access for database workloads.", False),
        ("High availability in storage implies no single point of failure.", True),
        ("iSCSI is a protocol used to transport SCSI commands over IP networks.", True),
    ],
    "Chapter 07": [
        ("Object storage uses a flat namespace with unique identifiers.", True),
        ("Block storage stores data as objects with metadata.", False),
        ("Consistent hashing minimizes remapping when nodes are added or removed.", True),
        ("The CAP theorem states that a distributed system can guarantee all three of Consistency, Availability, and Partition Tolerance simultaneously.", False),
        ("A Distributed Hash Table (DHT) provides a lookup service across distributed nodes.", True),
        ("Amazon S3 is an example of object storage.", True),
        ("File storage uses a hierarchical directory structure.", True),
        ("In the CAP theorem, Partition Tolerance is optional for distributed systems.", False),
        ("Object storage is ideal for unstructured data like images and videos.", True),
        ("Strong consistency guarantees that all nodes return the most recent write.", True),
    ],
    "Chapter 08": [
        ("Big Data is characterized by the 3 Vs: Volume, Velocity, and Variety.", True),
        ("Apache Hadoop includes HDFS as its distributed file system.", True),
        ("MapReduce is a programming model for processing large datasets in parallel.", True),
        ("In MapReduce, the Reduce phase sorts and groups data before the Map phase.", False),
        ("Apache Spark performs in-memory computation for faster processing.", True),
        ("HDFS stores data in fixed-size blocks distributed across a cluster.", True),
        ("Spark can run workloads 100x faster than Hadoop MapReduce for some tasks.", True),
        ("The NameNode manages metadata in a Hadoop cluster.", True),
        ("Data locality means moving computation to where the data resides.", True),
        ("MapReduce jobs always require a cluster of at least three nodes.", False),
    ],
    "Chapter 09": [
        ("OpenStack is an open-source cloud computing platform.", True),
        ("Taikun is a cloud management tool for provisioning resources.", True),
        ("YAFS is a simulator for cloud network topologies.", True),
        ("Nextcloud provides a self-hosted file sync and share platform.", True),
        ("Docker is required to deploy Nextcloud in a private cloud setup.", False),
        ("MinIO is an S3-compatible object storage server.", True),
        ("Hadoop requires compilation of MapReduce jobs written in Java.", True),
        ("Discrete event simulation models system behavior over continuous time.", False),
        ("Private cloud deployment can be fully automated with infrastructure-as-code tools.", True),
        ("Storage automation in MinIO can use lifecycle policies and bucket replication.", True),
    ],
}

MC_BANKS = {
    "Chapter 01": [
        ("Which organization published the standard definition of Cloud Computing?",
         ["NIST", "ISO", "IEEE", "W3C"], "NIST", "a"),
        ("Which of the following is NOT a NIST essential characteristic of Cloud Computing?",
         ["On-demand self-service", "Broad network access", "Fixed pricing", "Resource pooling"], "Fixed pricing", "c"),
        ("What does the pay-as-you-go model in cloud computing refer to?",
         ["Annual subscription", "Usage-based billing", "One-time payment", "Freemium model"], "Usage-based billing", "b"),
        ("Which term describes automatically scaling resources based on demand?",
         ["Elasticity", "Durability", "Latency", "Throughput"], "Elasticity", "a"),
        ("What is a workload in cloud computing?",
         ["A measure of CPU speed", "An application or service running on resources", "The physical server capacity", "The network bandwidth"], "An application or service running on resources", "b"),
        ("Serverless computing means:",
         ["No servers exist at all", "Servers are abstracted away from developers", "Only physical servers are used", "Servers are eliminated permanently"], "Servers are abstracted away from developers", "b"),
        ("Which computing paradigm preceded cloud computing historically?",
         ["Quantum computing", "Edge computing", "Mainframe and client-server computing", "Neural computing"], "Mainframe and client-server computing", "c"),
        ("On-premise vs Cloud: Which statement is correct?",
         ["Cloud requires higher upfront CAPEX", "On-premise has lower long-term OPEX", "Cloud shifts CAPEX to OPEX", "On-premise eliminates maintenance costs"], "Cloud shifts CAPEX to OPEX", "c"),
        ("Broad network access means cloud resources are:",
         ["Only accessible via Ethernet", "Accessible over standard network protocols", "Limited to VPN only", "Restricted to local LAN"], "Accessible over standard network protocols", "b"),
        ("Rapid elasticity in cloud computing refers to:",
         ["Physical hardware replacement", "Quick provisioning and release of resources", "Network cable upgrades", "Database optimization"], "Quick provisioning and release of resources", "b"),
    ],
    "Chapter 02": [
        ("IaaS provides which of the following to consumers?",
         ["Complete software applications", "Virtualized computing resources", "Development frameworks only", "Database schemas"], "Virtualized computing resources", "b"),
        ("Which service model gives consumers the most control?",
         ["SaaS", "PaaS", "IaaS", "FaaS"], "IaaS", "c"),
        ("In the Shared Responsibility Model, who is responsible for physical security?",
         ["The consumer", "The cloud provider", "Both equally", "A third party"], "The cloud provider", "b"),
        ("Public cloud characteristics include:",
         ["Single-tenant", "Located on consumer premises", "Multi-tenant shared infrastructure", "Government-only access"], "Multi-tenant shared infrastructure", "c"),
        ("What distinguishes hybrid cloud from multi-cloud?",
         ["Hybrid uses multiple providers independently", "Hybrid connects public and private clouds", "Multi-cloud requires VPN", "Hybrid is always on-premise"], "Hybrid connects public and private clouds", "b"),
        ("VPS is an example of which service model?",
         ["SaaS", "PaaS", "IaaS", "FaaS"], "IaaS", "c"),
        ("A VPC provides:",
         ["Public internet access only", "Isolated virtual network in the cloud", "Physical server rental", "Email hosting"], "Isolated virtual network in the cloud", "b"),
        ("Community cloud is shared by:",
         ["The general public", "Single organization", "Organizations with common goals", "Only government entities"], "Organizations with common goals", "c"),
        ("PaaS primarily enables developers to:",
         ["Manage physical servers", "Build and deploy applications without managing infrastructure", "Replace network cables", "Install operating systems"], "Build and deploy applications without managing infrastructure", "b"),
        ("Which deployment model is most cost-effective for startups?",
         ["Private cloud", "Community cloud", "Public cloud", "Hybrid cloud"], "Public cloud", "c"),
    ],
    "Chapter 03": [
        ("What is the primary function of a hypervisor?",
         ["To manage physical network cables", "To create and manage virtual machines", "To compile source code", "To encrypt data"], "To create and manage virtual machines", "b"),
        ("Type 1 hypervisors run:",
         ["On top of an operating system", "Directly on host hardware", "Inside a virtual machine", "As a user application"], "Directly on host hardware", "b"),
        ("VM migration that transfers a running VM with no downtime is called:",
         ["Cold migration", "Hot migration / Live migration", "Snapshot migration", "Template migration"], "Hot migration / Live migration", "b"),
        ("Which component represents a virtual CPU in a VM?",
         ["VHDX", "vCPU", "VMDK", "VNC"], "vCPU", "b"),
        ("What is a VM escape attack?",
         ["Deleting a VM accidentally", "An attacker breaking out of a VM to access the hypervisor", "Migrating a VM to another host", "Backing up a VM snapshot"], "An attacker breaking out of a VM to access the hypervisor", "b"),
        ("A rack unit (1U) equals how many inches in height?",
         ["1.00", "1.75", "2.00", "3.50"], "1.75", "b"),
        ("Which storage format is commonly used for virtual machine disk images?",
         ["MP4", "VMDK", "PDF", "EXE"], "VMDK", "b"),
        ("Hardware emulation differs from system virtualization because:",
         ["It is faster", "It simulates specific hardware components entirely in software", "It requires no hypervisor", "It uses only physical hardware"], "It simulates specific hardware components entirely in software", "b"),
        ("Memory overcommitment allows:",
         ["Allocating more memory to VMs than physically available", "Reducing physical memory", "Eliminating swap space", "Disabling memory entirely"], "Allocating more memory to VMs than physically available", "a"),
        ("Which hypervisor type is typically used in enterprise data centers?",
         ["Type 2", "Type 1", "Type 3", "Type 0"], "Type 1", "b"),
    ],
    "Chapter 04": [
        ("Microservices architecture is characterized by:",
         ["Single monolithic deployment", "Small independent services communicating via APIs", "All code in one repository", "Shared database for all services"], "Small independent services communicating via APIs", "b"),
        ("A message queue provides:",
         ["Direct synchronous communication", "Asynchronous decoupling of services", "Permanent data storage", "CPU scheduling"], "Asynchronous decoupling of services", "b"),
        ("In Event-Driven Architecture, events are:",
         ["Error messages only", "Significant changes in state", "Database backups", "Network pings"], "Significant changes in state", "b"),
        ("A broker in messaging systems typically:",
         ["Routes messages between producers and consumers", "Replaces the database", "Manages physical servers", "Compiles application code"], "Routes messages between producers and consumers", "a"),
        ("In the Publisher-Subscriber model:",
         ["Publishers send to specific subscribers", "Publishers send messages without knowing subscribers", "Subscribers send messages to publishers", "Messages are always deleted after reading"], "Publishers send messages without knowing subscribers", "b"),
        ("Why does Node.js fit serverless well?",
         ["It is compiled", "It uses an event-driven, non-blocking I/O model", "It requires a heavy runtime", "It only runs on Windows"], "It uses an event-driven, non-blocking I/O model", "b"),
        ("What decouples producers from consumers in a messaging system?",
         ["Direct API calls", "The broker/message queue", "Shared memory", "Environment variables"], "The broker/message queue", "b"),
        ("Event-driven architectures are typically:",
         ["Synchronous and blocking", "Asynchronous and non-blocking", "Sequential", "Batch-oriented"], "Asynchronous and non-blocking", "b"),
        ("Which pattern allows multiple services to react to the same event?",
         ["Request-Response", "Publish-Subscribe", "Point-to-Point", "Polling"], "Publish-Subscribe", "b"),
        ("A key benefit of microservices is:",
         ["Larger codebase per service", "Independent deployability and scalability", "Single point of failure", "Tight coupling"], "Independent deployability and scalability", "b"),
    ],
    "Chapter 05": [
        ("Linux Namespaces provide:",
         ["Resource limits", "Process isolation", "Network routing", "File compression"], "Process isolation", "b"),
        ("Cgroups (Control Groups) are used for:",
         ["Creating users", "Limiting and accounting resource usage", "Managing DNS", "Compiling code"], "Limiting and accounting resource usage", "b"),
        ("Docker images are built using:",
         ["A single flat file", "Read-only layers stacked on each other", "A database dump", "A compiled binary"], "Read-only layers stacked on each other", "b"),
        ("Kubernetes Pods are:",
         ["Physical servers", "The smallest deployable units containing one or more containers", "Network switches", "Storage volumes"], "The smallest deployable units containing one or more containers", "b"),
        ("The Kubernetes control plane component that maintains desired state is:",
         ["kubelet", "API Server", "etcd", "Controller Manager"], "etcd", "b"),
        ("Docker Compose is used to:",
         ["Deploy to Kubernetes", "Define and run multi-container Docker applications", "Build Linux kernels", "Manage databases"], "Define and run multi-container Docker applications", "b"),
        ("UnionFS enables:",
         ["Network bonding", "Filesystem layering and sharing of common layers", "Memory overcommitment", "CPU pinning"], "Filesystem layering and sharing of common layers", "b"),
        ("A Kubernetes Service provides:",
         ["Storage persistence", "Stable network endpoint for a set of Pods", "Container runtime", "Load balancer only for HTTP"], "Stable network endpoint for a set of Pods", "b"),
        ("kubelet is responsible for:",
         ["Managing the control plane", "Running containers on each worker node", "Routing external traffic", "Storing secrets"], "Running containers on each worker node", "b"),
        ("Container orchestration automates:",
         ["Only build processes", "Deployment, scaling, and management of containers", "Hardware provisioning", "Network cable installation"], "Deployment, scaling, and management of containers", "b"),
    ],
    "Chapter 06": [
        ("DAS provides storage:",
         ["Over a network", "Directly attached to a computer system", "Via fiber channel only", "As object storage"], "Directly attached to a computer system", "b"),
        ("NAS provides access at which level?",
         ["Block level", "File level", "Object level", "Sector level"], "File level", "b"),
        ("SAN uses which protocol typically?",
         ["HTTP", "Fibre Channel or iSCSI", "FTP", "SMTP"], "Fibre Channel or iSCSI", "b"),
        ("RAID 0 provides:",
         ["Redundancy through mirroring", "Striping without redundancy", "Parity protection", "Hot spares"], "Striping without redundancy", "b"),
        ("RAID 5 uses:",
         ["Striping with distributed parity", "Full mirroring of all data", "No striping", "Double parity"], "Striping with distributed parity", "a"),
        ("Storage virtualization pools:",
         ["Only RAM", "Physical storage from multiple devices into a single logical unit", "Network bandwidth", "CPU cores"], "Physical storage from multiple devices into a single logical unit", "b"),
        ("A datastore in virtualization is:",
         ["A database management system", "A logical container for VM files", "A network protocol", "A physical hard drive"], "A logical container for VM files", "b"),
        ("iSCSI transports SCSI commands over:",
         ["Serial cables", "IP networks", "USB", "HDMI"], "IP networks", "b"),
        ("High availability storage eliminates:",
         ["All data", "Single points of failure", "Network redundancy", "Power usage"], "Single points of failure", "b"),
        ("Block storage is most suitable for:",
         ["Unstructured data", "High-performance databases and VMs", "Email attachments", "Log files"], "High-performance databases and VMs", "b"),
    ],
    "Chapter 07": [
        ("Object storage uses a:",
         ["Hierarchical directory structure", "Flat namespace with unique identifiers", "Relational schema", "Block-based addressing"], "Flat namespace with unique identifiers", "b"),
        ("Consistent hashing helps with:",
         ["Encrypting data", "Minimizing key remapping when nodes change", "Indexing databases", "Compressing files"], "Minimizing key remapping when nodes change", "b"),
        ("The CAP theorem states a system cannot guarantee all three of:",
         ["Cost, Availability, Performance", "Consistency, Availability, Partition Tolerance", "Capacity, Access, Privacy", "Compliance, Audit, Portability"], "Consistency, Availability, Partition Tolerance", "b"),
        ("A Distributed Hash Table (DHT) provides:",
         ["SQL querying", "Decentralized key-value storage and lookup", "File compression", "Network routing only"], "Decentralized key-value storage and lookup", "b"),
        ("Amazon S3 is an example of:",
         ["Block storage", "Object storage", "File storage", "Cache storage"], "Object storage", "b"),
        ("File storage is organized as:",
         ["A flat list of objects", "A hierarchical directory tree", "A hash table", "A relational database"], "A hierarchical directory tree", "b"),
        ("Which consistency model guarantees all nodes return the latest write?",
         ["Eventual consistency", "Strong consistency", "Weak consistency", "Causal consistency"], "Strong consistency", "b"),
        ("Object storage is ideal for:",
         ["Relational databases", "Unstructured data like images and videos", "Operating system files", "Swap partitions"], "Unstructured data like images and videos", "b"),
        ("When a node is added or removed, consistent hashing requires:",
         ["Complete rehashing of all keys", "Minimal key redistribution", "Database migration", "Full system restart"], "Minimal key redistribution", "b"),
        ("Partition Tolerance in CAP means the system continues to function despite:",
         ["Hardware upgrades", "Network communication failures between nodes", "Software bugs", "User errors"], "Network communication failures between nodes", "b"),
    ],
    "Chapter 08": [
        ("The three Vs of Big Data are:",
         ["Value, Verification, Visualization", "Volume, Velocity, Variety", "Viability, Volatility, Validity", "Verbosity, Vagueness, Virtue"], "Volume, Velocity, Variety", "b"),
        ("HDFS stores files by:",
         ["Storing entire files on one node", "Splitting files into blocks distributed across nodes", "Compressing files in memory", "Storing everything in RAM"], "Splitting files into blocks distributed across nodes", "b"),
        ("MapReduce consists of which two main phases?",
         ["Read and Write", "Map and Reduce", "Sort and Search", "Split and Merge"], "Map and Reduce", "b"),
        ("Apache Spark performs computations primarily in:",
         ["Disk storage", "Memory (RAM)", "CPU cache", "Network buffers"], "Memory (RAM)", "b"),
        ("The NameNode in HDFS manages:",
         ["User authentication", "Filesystem metadata and namespace", "Data blocks", "Network routing"], "Filesystem metadata and namespace", "a"),
        ("Data locality in Hadoop means:",
         ["Moving data to the computation", "Moving computation to where data resides", "Storing data in a local database", "Using only local disks"], "Moving computation to where data resides", "b"),
        ("Spark RDD stands for:",
         ["Rapid Data Distribution", "Resilient Distributed Dataset", "Random Data Duplication", "Reduced Data Delay"], "Resilient Distributed Dataset", "b"),
        ("Which framework performs in-memory processing for faster analytics?",
         ["Apache Hadoop MapReduce", "Apache Spark", "Apache Hadoop only", "Apache Hive"], "Apache Spark", "b"),
        ("MapReduce is best suited for:",
         ["Real-time streaming", "Batch processing of large datasets", "Interactive queries", "Transaction processing"], "Batch processing of large datasets", "b"),
        ("HDFS data blocks are replicated across:",
         ["Single node for speed", "Multiple nodes for fault tolerance", "Only the NameNode", "External storage"], "Multiple nodes for fault tolerance", "b"),
    ],
    "Chapter 09": [
        ("OpenStack is primarily used for:",
         ["Web development", "Building and managing public/private cloud infrastructure", "Database management", "Graphic design"], "Building and managing public/private cloud infrastructure", "b"),
        ("YAFS is used to simulate:",
         ["Network traffic of video games", "Cloud topologies and network architectures", "Weather patterns", "Stock market"], "Cloud topologies and network architectures", "b"),
        ("Nextcloud provides:",
         ["Email hosting", "Self-hosted file sync and share platform", "Virtual machine creation", "Container orchestration"], "Self-hosted file sync and share platform", "b"),
        ("MinIO is compatible with which storage API?",
         ["S3", "EBS", "EFS", "Glacier"], "S3", "a"),
        ("Hadoop MapReduce jobs are typically written in:",
         ["Python", "Java", "JavaScript", "Ruby"], "Java", "b"),
        ("Discrete event simulation models events at:",
         ["Continuous time intervals", "Specific points in time", "Random intervals", "No specific times"], "Specific points in time", "b"),
        ("Taikun is used to:",
         ["Compile code", "Provision and manage cloud resources", "Edit text files", "Design logos"], "Provision and manage cloud resources", "b"),
        ("Docker Compose can be used in conjunction with Nextcloud to:",
         ["Build web pages", "Define multi-container services for the deployment", "Manage databases only", "Replace Kubernetes"], "Define multi-container services for the deployment", "b"),
        ("Infrastructure-as-code tools allow:",
         ["Manual server management", "Automated provisioning and configuration", "Only network configuration", "User training"], "Automated provisioning and configuration", "b"),
        ("MinIO bucket replication provides:",
         ["Faster network", "Data redundancy across locations", "Automatic scaling of compute", "Database indexing"], "Data redundancy across locations", "b"),
    ],
}

MATCH_BANKS = {
    "Chapter 01": [
        ("Match the NIST characteristic with its description.",
         ["a) On-demand self-service", "b) Broad network access", "c) Resource pooling", "d) Rapid elasticity"],
         ["n) User can provision resources without human interaction",
          "o) Resources accessible over standard network protocols",
          "p) Multi-tenant model serving multiple consumers",
          "q) Resources can scale quickly up or down"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the computing paradigm with its era.",
         ["a) Mainframe computing", "b) Client-Server computing", "c) Cloud computing", "d) Edge computing"],
         ["n) 1960s-1970s: Centralized computing",
          "o) 1980s-1990s: Distributed personal computing",
          "p) 2000s-present: On-demand utility computing",
          "q) Modern: Processing near data sources"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the financial model with its description.",
         ["a) CAPEX", "b) OPEX", "c) Pay-as-you-go", "d) Reserved instance"],
         ["n) Upfront capital expenditure",
          "o) Ongoing operational expenditure",
          "p) Usage-based billing model",
          "q) Pre-paid discounted commitment"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the cloud benefit with its explanation.",
         ["a) Elasticity", "b) Scalability", "c) High availability", "d) Fault tolerance"],
         ["n) Automatic resource adjustment based on load",
          "o) Ability to handle growing workloads",
          "p) Minimal downtime through redundancy",
          "q) System continues functioning despite component failures"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the workload type with its example.",
         ["a) Compute-intensive", "b) Memory-intensive", "c) Storage-intensive", "d) Network-intensive"],
         ["n) Video rendering and scientific simulations",
          "o) In-memory databases and caching",
          "p) Data lakes and backup archives",
          "q) Streaming services and real-time communications"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the cloud service category with its focus.",
         ["a) Compute services", "b) Storage services", "c) Database services", "d) Networking services"],
         ["n) Virtual machines and containers",
          "o) Object and block storage solutions",
          "p) Managed relational and NoSQL databases",
          "q) VPCs, load balancers, DNS"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the deployment concern with its meaning.",
         ["a) Latency", "b) Throughput", "c) Availability", "d) Durability"],
         ["n) Delay in data transmission",
          "o) Data processing rate per unit time",
          "p) Percentage of uptime",
          "q) Long-term data preservation"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the historical development with its contribution.",
         ["a) Virtualization technology", "b) Utility computing concept", "c) Web services", "d) Grid computing"],
         ["n) Enabled resource abstraction and VM management",
          "o) Metered service delivery like electricity",
          "p) Standardized API communication",
          "q) Distributed computing across multiple sites"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the cloud characteristic with its requirement.",
         ["a) Measured service", "b) Resource pooling", "c) On-demand self-service", "d) Broad network access"],
         ["n) Metering and billing capabilities",
          "o) Multi-tenant architecture support",
          "p) Self-service portal or API",
          "q) Internet connectivity"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the economic factor with its cloud impact.",
         ["a) Total Cost of Ownership (TCO)", "b) Return on Investment (ROI)", "c) Capital efficiency", "d) Operational agility"],
         ["n) Overall cost including all direct and indirect expenses",
          "o) Measure of profitability relative to investment",
          "p) Reducing upfront spending while increasing flexibility",
          "q) Speed of adapting to changing business needs"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 02": [
        ("Match the service model with its description.",
         ["a) IaaS", "b) PaaS", "c) SaaS", "d) FaaS"],
         ["n) Provides virtualized computing resources",
          "o) Provides platform for application development and deployment",
          "p) Provides ready-to-use software applications",
          "q) Provides serverless function execution environment"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the deployment model with its access scope.",
         ["a) Public cloud", "b) Private cloud", "c) Hybrid cloud", "d) Community cloud"],
         ["n) Open to general public over the internet",
          "o) Exclusive use by a single organization",
          "p) Combination of public and private environments",
          "q) Shared by organizations with common concerns"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the responsibility with the accountable party.",
         ["a) Physical security of data center", "b) Customer data encryption", "c) Operating system patching in IaaS", "d) Application security in SaaS"],
         ["n) Cloud provider", "o) Customer", "p) Customer", "q) Cloud provider"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the network concept with its definition.",
         ["a) VPC", "b) Subnet", "c) VPN", "d) VPS"],
         ["n) Isolated virtual network in the cloud",
          "o) Logical subdivision of a VPC network",
          "p) Encrypted tunnel over public internet",
          "q) Virtual machine instance for hosting"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the architecture layer with its service model.",
         ["a) Hardware layer", "b) Operating system layer", "c) Application layer", "d) Middleware layer"],
         ["n) IaaS manages this", "o) Both IaaS and PaaS manage this differently", "p) SaaS manages this", "q) PaaS provides this often"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the shared responsibility with its level.",
         ["a) Network infrastructure", "b) Virtual network configuration", "c) Data classification", "d) Access management"],
         ["n) Always provider responsibility",
          "o) Customer responsibility in IaaS",
          "p) Always customer responsibility",
          "q) Customer responsibility"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the deployment trade-off with its factor.",
         ["a) Security control", "b) Cost efficiency", "c) Compliance", "d) Scalability"],
         ["n) Private cloud offers more but at higher cost",
          "o) Public cloud maximizes resource sharing",
          "p) Regulatory requirements may mandate private deployment",
          "q) Hybrid cloud can burst to public during peaks"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the acronym with its full form.",
         ["a) EC2", "b) VPC", "c) VPN", "d) VPS"],
         ["n) Elastic Compute Cloud",
          "o) Virtual Private Cloud",
          "p) Virtual Private Network",
          "q) Virtual Private Server"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the cloud storage type with its cloud model relevance.",
         ["a) Ephemeral storage", "b) Persistent block storage", "c) Object storage", "d) File storage"],
         ["n) Temporary instance storage in IaaS",
          "o) EBS volumes attached to EC2 (IaaS)",
          "p) S3 buckets for scalable storage (IaaS)",
          "q) EFS for shared file access (IaaS)"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the service model with the level of control.",
         ["a) IaaS control level", "b) PaaS control level", "c) SaaS control level", "d) On-premise control level"],
         ["n) Most user control over infrastructure",
          "o) User controls application and data only",
          "p) Least user control, only configuration",
          "q) Full control including hardware"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 03": [
        ("Match the hypervisor type with its description.",
         ["a) Type 1 hypervisor", "b) Type 2 hypervisor", "c) Bare-metal hypervisor", "d) Hosted hypervisor"],
         ["n) Runs directly on hardware without host OS",
          "o) Runs on top of an existing operating system",
          "p) Another name for Type 1",
          "q) Another name for Type 2"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the VM component with its function.",
         ["a) vCPU", "b) vRAM", "c) VMDK", "d) Virtual NIC"],
         ["n) Virtual processor for computation",
          "o) Virtual memory for running processes",
          "p) Virtual disk file for persistent storage",
          "q) Virtual network interface for connectivity"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the migration type with its characteristic.",
         ["a) Cold migration", "b) Live migration", "c) Storage migration", "d) Cross-host migration"],
         ["n) VM is powered off during transfer",
          "o) VM remains running with zero downtime",
          "p) Moving virtual disk files between datastores",
          "q) Moving VM to a different physical server"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the security risk with its description.",
         ["a) VM escape", "b) Hypervisor compromise", "c) VM sprawl", "d) Resource starvation"],
         ["n) Breaking out of VM to access other systems",
          "o) Attacking the virtualization layer directly",
          "p) Uncontrolled proliferation of VMs",
          "q) Denial of resource access to legitimate VMs"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the data center component with its unit.",
         ["a) Rack", "b) Server", "c) Rack Unit (1U)", "d) Chassis"],
         ["n) Frame housing multiple servers",
          "o) Individual computing node",
          "p) Standard height of 1.75 inches",
          "q) Enclosure for multiple blades"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the virtualization benefit with its effect.",
         ["a) Server consolidation", "b) Isolation", "c) Hardware independence", "d) Snapshot capability"],
         ["n) Running multiple VMs on fewer physical hosts",
          "o) Faults in one VM do not affect others",
          "p) VMs can run on different hardware platforms",
          "q) Ability to capture VM state for backup"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the virtualization concept with its definition.",
         ["a) Hardware emulation", "b) Full virtualization", "c) Paravirtualization", "d) OS-level virtualization"],
         ["n) Simulating entire hardware architecture in software",
          "o) Complete hardware abstraction with no OS modification",
          "p) Guest OS is modified to improve performance",
          "q) Sharing host kernel among multiple user spaces"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the VM file type with its purpose.",
         ["a) .vmdk or .vhd", "b) .vmx or .config", "c) .nvram", "d) .log"],
         ["n) Virtual disk data storage file",
          "o) VM configuration and settings file",
          "p) BIOS/UEFI firmware state file",
          "q) Virtual machine log file"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the resource metric with its meaning in virtualization.",
         ["a) CPU ready time", "b) Ballooning", "c) Swap space", "d) Overcommit ratio"],
         ["n) Time VM is ready but waiting for CPU scheduling",
          "o) Memory reclaim technique by hypervisor",
          "p) Disk-based extension of physical memory",
          "q) Ratio of allocated to physical resources"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the hardware feature with its virtualization support.",
         ["a) Intel VT-x", "b) AMD-V", "c) SR-IOV", "d) NUMA"],
         ["n) Intel hardware virtualization extensions",
          "o) AMD hardware virtualization extensions",
          "p) Single root I/O virtualization for direct device access",
          "q) Non-uniform memory access architecture"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 04": [
        ("Match the architecture style with its description.",
         ["a) Monolithic", "b) Microservices", "c) Event-Driven", "d) Layered"],
         ["n) Single unified codebase for entire application",
          "o) Small independent services communicating via APIs",
          "p) Components react to events asynchronously",
          "q) Organized in tiers with specific responsibilities"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the messaging concept with its role.",
         ["a) Producer", "b) Consumer", "c) Broker", "d) Queue"],
         ["n) Creates and sends messages",
          "o) Receives and processes messages",
          "p) Routes messages between producers and consumers",
          "q) Temporary storage for pending messages"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the communication pattern with its behavior.",
         ["a) Synchronous", "b) Asynchronous", "c) Publish-Subscribe", "d) Point-to-Point"],
         ["n) Sender blocks until response is received",
          "o) Sender continues without waiting for response",
          "p) One-to-many message distribution",
          "q) One-to-one message delivery"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the EDA component with its function.",
         ["a) Event", "b) Event source", "c) Event handler", "d) Event bus"],
         ["n) A significant change in state",
          "o) Component that generates events",
          "p) Component that processes events",
          "q) Channel that transports events"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the microservice benefit with its description.",
         ["a) Scalability", "b) Resilience", "c) Autonomy", "d) Technology diversity"],
         ["n) Each service can be scaled independently",
          "o) Failure in one service does not cascade",
          "p) Teams can develop and deploy independently",
          "q) Different tech stacks can be used per service"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the pattern with its messaging model.",
         ["a) Request-Reply", "b) Fire-and-Forget", "c) Competing Consumers", "d) Dead Letter Channel"],
         ["n) Synchronous request followed by response",
          "o) Async message without expectation of reply",
          "p) Multiple consumers compete for same messages",
          "q) Storage for messages that cannot be processed"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the broker type with its specialty.",
         ["a) Apache Kafka", "b) RabbitMQ", "c) Amazon SQS", "d) Redis Pub/Sub"],
         ["n) Distributed streaming platform for event logs",
          "o) Message broker supporting AMQP protocol",
          "p) Fully managed message queuing service",
          "q) In-memory publish-subscribe messaging"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the deployment characteristic with serverless.",
         ["a) Scaling", "b) Billing", "c) Management", "d) Cold start"],
         ["n) Automatic from zero to any scale",
          "o) Pay per execution, not per resource",
          "p) Provider manages infrastructure fully",
          "q) Initial latency when invoking idle function"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the coupling type with its description.",
         ["a) Tight coupling", "b) Loose coupling", "c) Temporal coupling", "d) Spatial coupling"],
         ["n) Components heavily depend on each other",
          "o) Components have minimal dependencies",
          "p) Sender and receiver must be available simultaneously",
          "q) Components must know each other's location"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the ESB concept with its function.",
         ["a) Service registry", "b) Protocol transformation", "c) Message routing", "d) Orchestration"],
         ["n) Directory of available services",
          "o) Converting between different communication protocols",
          "p) Directing messages based on content",
          "q) Coordinating multiple service executions"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 05": [
        ("Match the container concept with its description.",
         ["a) Docker image", "b) Docker container", "c) Dockerfile", "d) Docker registry"],
         ["n) Read-only template with instructions for creating a container",
          "o) Runnable instance of an image",
          "p) Script with commands to build an image",
          "q) Repository for storing and distributing images"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Kubernetes component with its role.",
         ["a) API Server", "b) etcd", "c) Scheduler", "d) Controller Manager"],
         ["n) Entry point for all Kubernetes API requests",
          "o) Distributed key-value store for cluster state",
          "p) Assigns Pods to worker nodes",
          "q) Runs controllers that maintain desired state"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Linux kernel feature with its function.",
         ["a) Namespaces", "b) Cgroups", "c) UnionFS", "d) Capabilities"],
         ["n) Provides process isolation",
          "o) Limits and accounts resource usage",
          "p) Enables filesystem layering",
          "q) Grants fine-grained privileges"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Docker component with its description.",
         ["a) Docker daemon", "b) Docker client", "c) Docker Hub", "d) Docker Compose"],
         ["n) Background service managing containers",
          "o) CLI tool that sends commands to daemon",
          "p) Default public registry for images",
          "q) Tool for defining multi-container applications"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Kubernetes object with its purpose.",
         ["a) Pod", "b) Service", "c) Deployment", "d) ConfigMap"],
         ["n) Smallest deployable unit with one or more containers",
          "o) Stable network endpoint for Pods",
          "p) Declarative update for Pods and ReplicaSets",
          "q) Stores non-sensitive configuration data"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the scaling concept with its description.",
         ["a) Horizontal scaling", "b) Vertical scaling", "c) Auto-scaling", "d) Manual scaling"],
         ["n) Adding more instances of a resource",
          "o) Increasing capacity of existing instance",
          "p) Automatic adjustment based on metrics",
          "q) Administrator-initiated resource changes"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the network type with its Docker scope.",
         ["a) Bridge network", "b) Host network", "c) Overlay network", "d) Macvlan network"],
         ["n) Default isolated network for containers on same host",
          "o) Container shares host network stack",
          "p) Multi-host container communication across nodes",
          "q) Assigns MAC addresses to containers"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Kubernetes workload resource with its use case.",
         ["a) DaemonSet", "b) StatefulSet", "c) Job", "d) CronJob"],
         ["n) Runs one Pod per node for system services",
          "o) Manages stateful applications with stable identity",
          "p) Runs a batch task to completion",
          "q) Runs jobs on a scheduled basis"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the container storage option with its characteristic.",
         ["a) Volume", "b) Bind mount", "c) tmpfs mount", "d) Ephemeral storage"],
         ["n) Persistent storage managed by Docker",
          "o) Maps host directory into container",
          "p) In-memory storage for sensitive data",
          "q) Storage tied to container lifecycle"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the orchestration benefit with its description.",
         ["a) Service discovery", "b) Load balancing", "c) Self-healing", "d) Rolling updates"],
         ["n) Automatic detection of available services",
          "o) Distributing traffic across instances",
          "p) Restarting failed containers automatically",
          "q) Updating applications with zero downtime"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 06": [
        ("Match the storage type with its access method.",
         ["a) DAS", "b) NAS", "c) SAN", "d) Object storage"],
         ["n) Directly attached via SATA/SAS",
          "o) File-level access over network (NFS/SMB)",
          "p) Block-level access over Fibre Channel/iSCSI",
          "q) HTTP-based access with REST APIs"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the RAID level with its description.",
         ["a) RAID 0", "b) RAID 1", "c) RAID 5", "d) RAID 10"],
         ["n) Striping without redundancy",
          "o) Mirroring without striping",
          "p) Striping with distributed parity",
          "q) Striping with mirroring (combination)"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the storage virtualization concept with its definition.",
         ["a) Storage pool", "b) Datastore", "c) Thin provisioning", "d) Thick provisioning"],
         ["n) Aggregated logical unit from multiple physical devices",
          "o) Logical container for VM files in hypervisor",
          "p) Allocates storage on-demand as data is written",
          "q) Pre-allocates full storage capacity upfront"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the storage protocol with its transport.",
         ["a) Fibre Channel", "b) iSCSI", "c) NFS", "d) SMB"],
         ["n) Dedicated fiber optic network",
          "o) SCSI commands over TCP/IP",
          "p) Network File System for Unix/Linux",
          "q) Server Message Block for Windows"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the high availability feature with its purpose.",
         ["a) Multipathing", "b) Replication", "c) Snapshot", "d) Clustering"],
         ["n) Multiple I/O paths for redundancy",
          "o) Copying data to secondary storage",
          "p) Point-in-time copy for backup",
          "q) Grouping servers for failover"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the storage optimization with its benefit.",
         ["a) Deduplication", "b) Compression", "c) Tiering", "d) Caching"],
         ["n) Eliminating duplicate data blocks",
          "o) Reducing data size through algorithms",
          "p) Moving data between performance tiers",
          "q) Storing frequently accessed data in faster media"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the SAN component with its function.",
         ["a) HBA", "b) Fibre Channel switch", "c) Storage array", "d) LUN"],
         ["n) Host Bus Adapter to connect server to SAN",
          "o) Network switch dedicated to storage traffic",
          "p) Disk enclosure with controllers and disks",
          "q) Logical Unit Number representing storage volume"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the storage metric with its meaning.",
         ["a) IOPS", "b) Throughput", "c) Latency", "d) Capacity"],
         ["n) Input/Output operations per second",
          "o) Data transfer rate (MB/s or GB/s)",
          "p) Time delay in data access",
          "q) Total storage space available"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the DAS limitation vs network storage benefit.",
         ["a) DAS scalability", "b) NAS file sharing", "c) SAN performance", "d) Storage pooling benefit"],
         ["n) Limited to local machine expansion",
          "o) Multiple clients can access same files",
          "p) High-speed block access for databases",
          "q) Flexible capacity allocation across systems"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the data protection technique with its description.",
         ["a) Backup", "b) Replication", "c) Erasure coding", "d) Snapshots"],
         ["n) Copying data to separate media for recovery",
          "o) Continuous copying to remote site",
          "p) Data fragmentation with parity for fault tolerance",
          "q) Instant point-in-time copy for quick recovery"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 07": [
        ("Match the storage paradigm with its data organization.",
         ["a) Block storage", "b) File storage", "c) Object storage", "d) Key-value storage"],
         ["n) Data divided into fixed-size blocks with addresses",
          "o) Organized in hierarchical directories and files",
          "p) Data stored as objects with unique IDs and metadata",
          "q) Data stored as key-value pairs"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the CAP theorem property with its meaning.",
         ["a) Consistency", "b) Availability", "c) Partition Tolerance", "d) Trade-off"],
         ["n) All nodes see the same data at the same time",
          "o) Every request receives a response",
          "p) System continues despite network failures",
          "q) Must sacrifice one property in distributed systems"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the DHT concept with its description.",
         ["a) Key", "b) Value", "c) Node", "d) Ring"],
         ["n) Unique identifier for stored data",
          "o) Data associated with the key",
          "p) Participant storing a portion of the data",
          "q) Circular keyspace topology in consistent hashing"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the consistency model with its guarantee.",
         ["a) Strong consistency", "b) Eventual consistency", "c) Causal consistency", "d) Read-your-writes consistency"],
         ["n) All nodes return the most recent write",
          "o) System will converge over time",
          "p) Related events are seen in correct order",
          "q) User always sees their own updates"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the cloud storage product with its type.",
         ["a) Amazon S3", "b) Amazon EBS", "c) Amazon EFS", "d) Amazon Glacier"],
         ["n) Object storage with unlimited scalability",
          "o) Block storage for EC2 instances",
          "p) File storage with shared access",
          "q) Archival storage at low cost"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the distributed system concept with its use.",
         ["a) Replication", "b) Sharding", "c) Partitioning", "d) Load balancing"],
         ["n) Copying data across multiple nodes",
          "o) Splitting data across databases",
          "p) Dividing the keyspace across nodes",
          "q) Distributing requests across servers"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the distributed storage feature with its description.",
         ["a) Data durability", "b) Data availability", "c) Data consistency", "d) Data integrity"],
         ["n) Protection against permanent data loss",
          "o) Ensuring data is accessible when needed",
          "p) All replicas return the same value",
          "q) Protection against data corruption"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the hashing type with its property.",
         ["a) Traditional hashing", "b) Consistent hashing", "c) Rendezvous hashing", "d) Distributed hashing"],
         ["n) All keys remap when node count changes",
          "o) Minimal key movement when nodes change",
          "p) Each client independently computes target node",
          "q) Hash function spreads keys across nodes"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the replication strategy with its approach.",
         ["a) Synchronous replication", "b) Asynchronous replication", "c) Quorum-based replication", "d) Chain replication"],
         ["n) Write completes only after all replicas confirm",
          "o) Write completes before all replicas are updated",
          "p) Requires majority consensus for reads/writes",
          "q) Replicas are organized in a linear chain"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the storage access pattern with its typical workload.",
         ["a) Sequential access", "b) Random access", "c) Streaming access", "d) Indexed access"],
         ["n) Reading data in order, typical for logs",
          "o) Reading data at arbitrary positions",
          "p) Continuous flow of data, typical for video",
          "q) Accessing data via lookup indexes"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 08": [
        ("Match the Big Data characteristic with its description.",
         ["a) Volume", "b) Velocity", "c) Variety", "d) Veracity"],
         ["n) Massive quantity of data generated",
          "o) Speed at which data is generated and processed",
          "p) Different types of data formats and sources",
          "q) Quality and trustworthiness of data"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Hadoop component with its function.",
         ["a) HDFS", "b) MapReduce", "c) YARN", "d) NameNode"],
         ["n) Distributed file system for data storage",
          "o) Programming model for parallel data processing",
          "p) Resource management and job scheduling",
          "q) Metadata management for HDFS"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the MapReduce phase with its activity.",
         ["a) Map phase", "b) Shuffle phase", "c) Sort phase", "d) Reduce phase"],
         ["n) Processes input data to produce key-value pairs",
          "o) Transfers data from mappers to reducers",
          "p) Orders data by key for reduce processing",
          "q) Aggregates and combines values by key"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Spark concept with its definition.",
         ["a) RDD", "b) DataFrame", "c) Dataset", "d) DAG"],
         ["n) Resilient Distributed Dataset - immutable collection",
          "o) Distributed collection organized into named columns",
          "p) Strongly typed API with optimization benefits",
          "q) Directed Acyclic Graph of computation stages"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Spark component with its role.",
         ["a) Driver", "b) Executor", "c) Cluster Manager", "d) SparkContext"],
         ["n) Main program that coordinates Spark application",
          "o) Worker process running tasks on nodes",
          "p) Manages resource allocation across cluster",
          "q) Entry point for connecting to Spark cluster"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Big Data processing model with its description.",
         ["a) Batch processing", "b) Stream processing", "c) Real-time processing", "d) Interactive processing"],
         ["n) Processing large datasets at scheduled intervals",
          "o) Continuous processing of data in motion",
          "p) Immediate processing with low latency",
          "q) Ad-hoc queries and exploration of data"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the HDFS concept with its description.",
         ["a) Block size", "b) Replication factor", "c) DataNode", "d) Secondary NameNode"],
         ["n) Default 128 MB in modern Hadoop",
          "o) Number of copies of each data block",
          "p) Worker node that stores actual data blocks",
          "q) Checkpoints NameNode metadata for recovery"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the optimization technique with its benefit.",
         ["a) Data locality", "b) In-memory computing", "c) Partitioning", "d) Caching"],
         ["n) Reduces network transfer by processing near data",
          "o) Eliminates disk I/O bottlenecks",
          "p) Enables parallel processing of subsets",
          "q) Stores intermediate results for reuse"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Big Data tool with its category.",
         ["a) Apache Hive", "b) Apache HBase", "c) Apache Pig", "d) Apache Flume"],
         ["n) Data warehouse and SQL-like queries",
          "o) NoSQL columnar database",
          "p) Data flow scripting language",
          "q) Log data collection and aggregation"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the processing framework with its characteristic.",
         ["a) Hadoop MapReduce", "b) Apache Spark", "c) Apache Flink", "d) Apache Storm"],
         ["n) Disk-based batch processing",
          "o) In-memory batch and stream processing",
          "p) True stream processing with event time",
          "q) Real-time stream processing system"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
    "Chapter 09": [
        ("Match the lab tool with its purpose.",
         ["a) OpenStack", "b) Taikun", "c) YAFS", "d) MinIO"],
         ["n) Open-source cloud infrastructure management",
          "o) Cloud provisioning and resource management",
          "p) Discrete event simulation of cloud topologies",
          "q) S3-compatible object storage server"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the deployment technology with its use case.",
         ["a) Docker Compose", "b) Kubernetes", "c) Ansible", "d) Terraform"],
         ["n) Multi-container local application definition",
          "o) Container orchestration at scale",
          "p) Configuration management and automation",
          "q) Infrastructure-as-code provisioning"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the storage concept with its implementation in MinIO.",
         ["a) Bucket", "b) Object", "c) Access key", "d) Bucket policy"],
         ["n) Container for storing objects",
          "o) A file with its metadata stored in a bucket",
          "p) Credential for API authentication",
          "q) Rules governing bucket access permissions"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the simulation concept with YAFS meaning.",
         ["a) Topology", "b) Workload", "c) Orchestrator", "d) Simulator engine"],
         ["n) Network structure of cloud nodes",
          "o) Pattern of user requests and tasks",
          "p) Coordinates simulation components",
          "q) Core simulation runtime"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Nextcloud component with its role.",
         ["a) Web server", "b) Database", "c) Data directory", "d) Redis cache"],
         ["n) Serves the Nextcloud web interface",
          "o) Stores application metadata",
          "p) Stores user files and uploaded content",
          "q) Provides session locking and caching"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the MapReduce step with its operation.",
         ["a) Input split", "b) Mapping", "c) Shuffling", "d) Reducing"],
         ["n) Divides input data into manageable chunks",
          "o) Applies transformation to each record",
          "p) Rearranges data by key across nodes",
          "q) Aggregates values per key to produce output"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the cloud security concept with its implementation.",
         ["a) Firewall rules", "b) IAM roles", "c) Encryption at rest", "d) Audit logging"],
         ["n) Network traffic filtering",
          "o) Identity and access management",
          "p) Data encryption on storage media",
          "q) Recording all API activities"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the Docker compose directive with its purpose.",
         ["a) services", "b) volumes", "c) networks", "d) environment"],
         ["n) Defines application containers",
          "o) Defines persistent data storage",
          "p) Defines container communication channels",
          "q) Defines configuration variables"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the lab automation tool with its description.",
         ["a) Shell scripts", "b) Docker Compose", "c) Ansible playbooks", "d) Kubernetes manifests"],
         ["n) Sequential command execution automation",
          "o) YAML-defined multi-container deployments",
          "p) Declarative configuration management automation",
          "q) YAML-defined Kubernetes resource specifications"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
        ("Match the cloud lab category with its focus.",
         ["a) Provisioning lab", "b) Simulation lab", "c) Storage lab", "d) Processing lab"],
         ["n) Deploying virtual machines and networks",
          "o) Modeling cloud topologies and workloads",
          "p) Setting up object storage and backups",
          "q) Running distributed data processing jobs"],
         ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]
        ),
    ],
}


def generate_quiz_file(chapter_num_padded, chapter_dir, sources, variant, tfs, mcs, matches):
    lines = []
    lines.append("---")
    lines.append("sources:")
    for s in sources:
        lines.append(s)
    lines.append("---")
    lines.append("")

    # True/False questions
    for q_text, answer in tfs:
        ans_str = "True" if answer else "False"
        lines.append(f"> [!question] {q_text}")
        lines.append(">> [!success]- Answer")
        lines.append(f">> {ans_str}")
        lines.append("")

    # Multiple Choice questions
    for q_data in mcs:
        q_text = q_data[0]
        options = q_data[1]
        correct_text = q_data[2]
        correct_letter = q_data[3]
        lines.append(f"> [!question] {q_text}")
        letters = ["a", "b", "c", "d"]
        for i, opt in enumerate(options):
            lines.append(f"> {letters[i]}) {opt}")
        lines.append(">> [!success]- Answer")
        lines.append(f">> {correct_letter}) {correct_text}")
        lines.append("")

    # Matching questions
    for m_data in matches:
        q_text = m_data[0]
        group_a = m_data[1]
        group_b = m_data[2]
        answers = m_data[3]
        lines.append(f"> [!question] {q_text}")
        lines.append(">> [!example] Group A")
        for item in group_a:
            lines.append(f">> {item}")
        lines.append(">")
        lines.append(">> [!example] Group B")
        for item in group_b:
            lines.append(f">> {item}")
        lines.append(">")
        lines.append(">> [!success]- Answer")
        for ans in answers:
            lines.append(f">> {ans}")
        lines.append("")

    return "\n".join(lines)


def main():
    base = "Quiz"
    for ch_key, (ch_dir, source_files) in CHAPTERS.items():
        folder = f"{base}/{ch_key}"
        os.makedirs(folder, exist_ok=True)

        # Build sources for frontmatter
        sources = [f'  - "[[{ch_dir}/{f}]]"' for f in source_files]

        # Get the question banks for this chapter
        tfs = TF_BANKS[ch_key]
        mcs = MC_BANKS[ch_key]
        matches = MATCH_BANKS[ch_key]

        # Split each bank into two halves
        half_tf = len(tfs) // 2
        half_mc = len(mcs) // 2
        half_match = len(matches) // 2

        # File 1 variant (odd-numbered questions)
        tfs_v1 = tfs[:half_tf]
        mcs_v1 = mcs[:half_mc]
        matches_v1 = matches[:half_match]

        # File 2 variant (even-numbered questions)
        tfs_v2 = tfs[half_tf:]
        mcs_v2 = mcs[half_mc:]
        matches_v2 = matches[half_match:]

        content1 = generate_quiz_file(ch_key, ch_dir, sources, "A", tfs_v1, mcs_v1, matches_v1)
        content2 = generate_quiz_file(ch_key, ch_dir, sources, "B", tfs_v2, mcs_v2, matches_v2)

        # Filenames
        file1 = f"{folder}/{ch_key}_Quiz_A.md"
        file2 = f"{folder}/{ch_key}_Quiz_B.md"

        with open(file1, "w") as f:
            f.write(content1)
        with open(file2, "w") as f:
            f.write(content2)

        print(f"Created: {file1}")
        print(f"Created: {file2}")

    print("\nAll quiz files generated successfully.")


if __name__ == "__main__":
    main()