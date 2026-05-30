#!/usr/bin/env python3
"""Generate quiz files for all chapters - 30 questions each (10 TF, 10 MCQ, 10 Matching)"""
import os
import json

# Store quiz data as JSON to avoid Python syntax issues
# The data is loaded from an inline JSON-like structure

def build_yaml(sources):
    lines = ["---", "sources:"]
    for s in sources:
        lines.append('  - "' + s + '"')
    lines.append("---")
    return "\n".join(lines)

def tf_block(q, a):
    return "> [!question] " + q + "\n>> [!success]- Answer\n>> " + a

def mcq_block(q, opts, answer):
    labels = ["a", "b", "c", "d"]
    opts_str = "\n".join(["> " + labels[i] + ") " + o for i, o in enumerate(opts)])
    return "> [!question] " + q + "\n" + opts_str + "\n>> [!success]- Answer\n>> " + answer

def matching_block(q, group_a, group_b, answers):
    a_labels = ["a", "b", "c", "d"]
    b_labels = ["n", "o", "p", "q"]
    a_block = "\n".join([">> " + a_labels[i] + ") " + item for i, item in enumerate(group_a)])
    b_block = "\n".join([">> " + b_labels[i] + ") " + item for i, item in enumerate(group_b)])
    ans_block = "\n".join([">> " + ans for ans in answers])
    return ("> [!question] " + q + "\n>> [!example] Group A\n" + a_block + "\n>\n>> [!example] Group B\n" + b_block + "\n>\n>> [!success]- Answer\n" + ans_block)

def gen_file(sources, tf_data, mcq_data, match_data):
    parts = [build_yaml(sources), ""]
    for q, a in tf_data:
        parts.append(tf_block(q, a))
        parts.append("")
    for q, opts, ans in mcq_data:
        parts.append(mcq_block(q, opts, ans))
        parts.append("")
    for q, ga, gb, ans_list in match_data:
        parts.append(matching_block(q, ga, gb, ans_list))
        parts.append("")
    return "\n".join(parts).strip() + "\n"

# Chapter sources
CHAPTER_SOURCES = {
    "01": [
        "[[Chapter 1 - Introduction to Cloud Computing/1.1 Cloud Computing Definition and Foundations.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.2 Historical Evolution of Computing Paradigms.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.3 NIST Characteristics of Cloud Computing.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.4 Cloud vs On-Premise Strategic Analysis.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.5 Evolution, Elasticity, and Scalability Mechanics.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.6 The Five Essential NIST Characteristics and Financial Models.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.7 The Historical Paradigm Shifts Preceding Cloud Computing.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.8 What The Cloud Means.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.9 Understanding Cloud Providers, Hosting Services, and VPS.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.10 What is a Workload.md]]",
        "[[Chapter 1 - Introduction to Cloud Computing/1.11 What is Serverless.md]]",
    ],
    "02": [
        "[[Chapter 2 - Service and Deployment Models/2.1 Hierarchical Cloud Infrastructure and Architecture.md]]",
        "[[Chapter 2 - Service and Deployment Models/2.2 Cloud Service Models - IaaS PaaS SaaS Deep Dive.md]]",
        "[[Chapter 2 - Service and Deployment Models/2.3 The Shared Responsibility Model.md]]",
        "[[Chapter 2 - Service and Deployment Models/2.4 Cloud Deployment Models - Public Private Hybrid Community.md]]",
        "[[Chapter 2 - Service and Deployment Models/2.5 Cloud Architecture Layers and Responsibility Boundaries.md]]",
        "[[Chapter 2 - Service and Deployment Models/2.6 Cloud Deployment Architectures and Network Trade-offs.md]]",
        "[[Chapter 2 - Service and Deployment Models/2.7 What is VPS and EC2.md]]",
        "[[Chapter 2 - Service and Deployment Models/2.8 What is a VPC.md]]",
    ],
    "03": [
        "[[Chapter 3 - Virtualization/3.1 Core Virtualization Concepts and Hypervisors.md]]",
        "[[Chapter 3 - Virtualization/3.2 Anatomy and Technical Composition of a Virtual Machine.md]]",
        "[[Chapter 3 - Virtualization/3.3 Virtual Machine Migration Techniques.md]]",
        "[[Chapter 3 - Virtualization/3.4 Advanced Virtualization Paradigms and Security.md]]",
        "[[Chapter 3 - Virtualization/3.5 Hypervisor Internals and Execution Types.md]]",
        "[[Chapter 3 - Virtualization/3.6 VM Migration Mechanisms and State Transfer.md]]",
        "[[Chapter 3 - Virtualization/3.7 What is a Virtual Machine.md]]",
        "[[Chapter 3 - Virtualization/3.8 The Physical Machine - Racks, Servers, and Data Centers.md]]",
        "[[Chapter 3 - Virtualization/3.9 What a Rack Unit Really Means.md]]",
        "[[Chapter 3 - Virtualization/3.10 A Server is Not the Rack.md]]",
        "[[Chapter 3 - Virtualization/3.11 Anatomy of a Virtual Machine and File Structures.md]]",
        "[[Chapter 3 - Virtualization/3.12 Virtualization Security Risks and Threat Vectors.md]]",
        "[[Chapter 3 - Virtualization/3.13 Hardware Emulation vs System Virtualization.md]]",
    ],
    "04": [
        "[[Chapter 4 - Architecture and Communication Patterns/4.1 What are Microservices.md]]",
        "[[Chapter 4 - Architecture and Communication Patterns/4.2 What are Message Queues and Event-driven Patterns.md]]",
        "[[Chapter 4 - Architecture and Communication Patterns/4.3 What is a Broker.md]]",
        "[[Chapter 4 - Architecture and Communication Patterns/4.4 Event-Driven Architecture (EDA).md]]",
        "[[Chapter 4 - Architecture and Communication Patterns/4.5 The Publisher-Subscriber Model.md]]",
        "[[Chapter 4 - Architecture and Communication Patterns/4.6 Why Node.js Fits Serverless So Well.md]]",
    ],
    "05": [
        "[[Chapter 5 - Containerization and Orchestration/5.1 Linux Kernel Isolation Mechanics - Namespaces and Cgroups.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.2 Docker Engine Architecture and Core Components.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.3 Dockerfile Mechanics and Multi-Container Applications.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.4 Container Orchestration and Kubernetes Foundations.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.5 Kubernetes Control Plane and Worker Node Architecture.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.6 Pod Scheduling, Resource Management, and Services.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.7 Linux Kernel Internals (Namespaces, Cgroups, UnionFS).md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.8 Kubernetes Architecture and Pod Scheduling Workflow.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.9 Docker Engine Architecture and Container Lifecycle.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.10 Dockerfile Layering and Image Build Mechanics.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.11 Microservices, Docker Compose, and Container Networking.md]]",
        "[[Chapter 5 - Containerization and Orchestration/5.12 Kubernetes Networking, Services, and Configuration Management.md]]",
    ],
    "06": [
        "[[Chapter 6 - Virtual and Networked Storage/6.1 Storage Foundations and Access Models.md]]",
        "[[Chapter 6 - Virtual and Networked Storage/6.2 Networked Storage Architectures - DAS NAS SAN.md]]",
        "[[Chapter 6 - Virtual and Networked Storage/6.3 Storage Virtualization, Datastores, and High Availability.md]]",
        "[[Chapter 6 - Virtual and Networked Storage/6.4 Block vs File Access and SAN vs NAS Architectures.md]]",
        "[[Chapter 6 - Virtual and Networked Storage/6.5 RAID, Datastores, and Advanced Storage Features.md]]",
        "[[Chapter 6 - Virtual and Networked Storage/6.6 Solving Storage Silos with Virtualization and Pooling.md]]",
    ],
    "07": [
        "[[Chapter 7 - Cloud Storage and Distributed Systems/7.1 Cloud Storage Paradigms - Block File Object.md]]",
        "[[Chapter 7 - Cloud Storage and Distributed Systems/7.2 Distributed Hash Tables and Consistent Hashing.md]]",
        "[[Chapter 7 - Cloud Storage and Distributed Systems/7.3 Data Consistency Models and CAP Theorem.md]]",
    ],
    "08": [
        "[[Chapter 8 - Big Data Processing Frameworks/8.1 Big Data Foundations and Architecture.md]]",
        "[[Chapter 8 - Big Data Processing Frameworks/8.2 Apache Hadoop Ecosystem and HDFS.md]]",
        "[[Chapter 8 - Big Data Processing Frameworks/8.3 MapReduce Programming Model and Execution Engine.md]]",
        "[[Chapter 8 - Big Data Processing Frameworks/8.4 Apache Spark In-Memory Computation Engine.md]]",
    ],
    "09": [
        "[[Chapter 9 - Practical Labs and Solutions/9.1 TP 1 - Cloud Provisioning with OpenStack and Taikun.md]]",
        "[[Chapter 9 - Practical Labs and Solutions/9.2 TP 2 - Discrete Event Simulation of Cloud Topologies via YAFS.md]]",
        "[[Chapter 9 - Practical Labs and Solutions/9.3 TP 4 and 5 - Private Cloud Deployment with Nextcloud and Docker.md]]",
        "[[Chapter 9 - Practical Labs and Solutions/9.4 TP 6 - Cloud Storage Automation and Persistance with MinIO.md]]",
        "[[Chapter 9 - Practical Labs and Solutions/9.5 TP 7 - Distributed MapReduce Compilation and Execution on Hadoop.md]]",
    ],
}

def get_quiz_data(chapter, variant):
    """Return quiz data for a given chapter and variant (A/B)."""
    key = chapter + "_" + variant
    
    # All quiz data stored in one large structure
    all_data = {
        # ====== CHAPTER 01 ======
        "01_A": {
            "tf": [
                ("Cloud Computing enables on-demand network access to a shared pool of configurable computing resources.", "True"),
                ("Cloud Computing requires users to purchase physical hardware assets before using services.", "False"),
                ("The NIST definition of Cloud Computing includes five essential characteristics.", "True"),
                ("Elasticity in cloud computing means resources can be automatically scaled up or down based on demand.", "True"),
                ("On-premise infrastructure typically has lower upfront costs compared to cloud solutions.", "False"),
                ("Serverless computing eliminates the need for any servers to run applications.", "False"),
                ("Measured service in cloud computing provides metering and billing transparency.", "True"),
                ("Resource pooling in cloud computing uses a single-tenant model for each customer.", "False"),
                ("Broad network access restricts cloud resources to local area networks only.", "False"),
                ("The pay-as-you-go model shifts capital expenditure to operational expenditure.", "True"),
            ],
            "mcq": [
                ("Which organization published the standard definition of Cloud Computing?", ["NIST", "ISO", "IEEE", "W3C"], "a) NIST"),
                ("Which of the following is NOT a NIST essential characteristic of Cloud Computing?", ["On-demand self-service", "Broad network access", "Fixed pricing", "Resource pooling"], "c) Fixed pricing"),
                ("What does the pay-as-you-go model in cloud computing refer to?", ["Annual subscription", "Usage-based billing", "One-time payment", "Freemium model"], "b) Usage-based billing"),
                ("Which term describes automatically scaling resources based on demand?", ["Elasticity", "Durability", "Latency", "Throughput"], "a) Elasticity"),
                ("What is a workload in cloud computing?", ["A measure of CPU speed", "An application or service running on resources", "The physical server capacity", "The network bandwidth"], "b) An application or service running on resources"),
                ("Serverless computing means:", ["No servers exist at all", "Servers are abstracted away from developers", "Only physical servers are used", "Servers are eliminated permanently"], "b) Servers are abstracted away from developers"),
                ("Which computing paradigm preceded cloud computing historically?", ["Quantum computing", "Edge computing", "Mainframe and client-server computing", "Neural computing"], "c) Mainframe and client-server computing"),
                ("On-premise vs Cloud: Which statement is correct?", ["Cloud requires higher upfront CAPEX", "On-premise has lower long-term OPEX", "Cloud shifts CAPEX to OPEX", "On-premise eliminates maintenance costs"], "c) Cloud shifts CAPEX to OPEX"),
                ("Broad network access means cloud resources are:", ["Only accessible via Ethernet", "Accessible over standard network protocols", "Limited to VPN only", "Restricted to local LAN"], "b) Accessible over standard network protocols"),
                ("Rapid elasticity in cloud computing refers to:", ["Physical hardware replacement", "Quick provisioning and release of resources", "Network cable upgrades", "Database optimization"], "b) Quick provisioning and release of resources"),
            ],
            "matching": [
                ("Match the NIST characteristic with its description.", ["On-demand self-service", "Broad network access", "Resource pooling", "Rapid elasticity"], ["User can provision resources without human interaction", "Resources accessible over standard network protocols", "Multi-tenant model serving multiple consumers", "Resources can scale quickly up or down"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the computing paradigm with its era.", ["Mainframe computing", "Client-Server computing", "Cloud computing", "Edge computing"], ["1960s-1970s: Centralized computing", "1980s-1990s: Distributed personal computing", "2000s-present: On-demand utility computing", "Modern: Processing near data sources"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the financial model with its description.", ["CAPEX", "OPEX", "Pay-as-you-go", "Reserved instance"], ["Upfront capital expenditure", "Ongoing operational expenditure", "Usage-based billing model", "Pre-paid discounted commitment"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the cloud benefit with its explanation.", ["Elasticity", "Scalability", "High availability", "Fault tolerance"], ["Automatic resource adjustment based on load", "Ability to handle growing workloads", "Minimal downtime through redundancy", "System continues functioning despite component failures"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the workload type with its example.", ["Compute-intensive", "Memory-intensive", "Storage-intensive", "Network-intensive"], ["Video rendering and scientific simulations", "In-memory databases and caching", "Data lakes and backup archives", "Streaming services and real-time communications"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the cloud characteristic with its requirement.", ["Measured service", "Resource pooling", "On-demand self-service", "Broad network access"], ["Metering and billing capabilities", "Multi-tenant architecture support", "Self-service portal or API", "Internet connectivity"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the economic factor with its cloud impact.", ["Total Cost of Ownership (TCO)", "Return on Investment (ROI)", "Capital efficiency", "Operational agility"], ["Overall cost including all direct and indirect expenses", "Measure of profitability relative to investment", "Reducing upfront spending while increasing flexibility", "Speed of adapting to changing business needs"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the historical development with its contribution.", ["Virtualization technology", "Utility computing concept", "Web services", "Grid computing"], ["Enabled resource abstraction and VM management", "Metered service delivery like electricity", "Standardized API communication", "Distributed computing across multiple sites"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the deployment concern with its meaning.", ["Latency", "Throughput", "Availability", "Durability"], ["Delay in data transmission", "Data processing rate per unit time", "Percentage of uptime", "Long-term data preservation"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the service category with its focus.", ["Compute services", "Storage services", "Database services", "Networking services"], ["Virtual machines and containers", "Object and block storage solutions", "Managed relational and NoSQL databases", "VPCs, load balancers, DNS"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
            ],
        },
        "01_B": {
            "tf": [
                ("Serverless computing still requires the user to manage virtual machines.", "False"),
                ("A workload is a specific application or service that runs on cloud resources.", "True"),
                ("Scalability refers only to increasing resources, never decreasing them.", "False"),
                ("Cloud providers follow a pay-as-you-go financial model.", "True"),
                ("The evolution of cloud computing began with the invention of the internet in the 1990s.", "False"),
                ("On-demand self-service allows users to provision resources without human interaction with the provider.", "True"),
                ("Resource pooling means each customer gets dedicated physical hardware.", "False"),
                ("Rapid elasticity makes cloud resources appear unlimited to the consumer.", "True"),
                ("Measured service is optional and not required for cloud computing.", "False"),
                ("Utility computing is a concept where computing resources are delivered like electricity.", "True"),
            ],
            "mcq": [
                ("Which of the following best describes cloud computing?", ["Running applications on local desktops", "On-demand access to shared configurable resources over the network", "Storing files on USB drives", "Installing software from physical media"], "b) On-demand access to shared configurable resources over the network"),
                ("What is the primary difference between CAPEX and OPEX?", ["CAPEX is monthly, OPEX is yearly", "CAPEX is upfront investment, OPEX is ongoing expense", "CAPEX is for software, OPEX is for hardware", "There is no difference"], "b) CAPEX is upfront investment, OPEX is ongoing expense"),
                ("Which NIST characteristic ensures resources can be monitored and billed?", ["Rapid elasticity", "Measured service", "Resource pooling", "Broad network access"], "b) Measured service"),
                ("What does abstraction mean in cloud computing?", ["Physical hardware is hidden behind virtualized software layers", "Data is encrypted during transmission", "Users must know the hardware details", "Applications run on bare metal"], "a) Physical hardware is hidden behind virtualized software layers"),
                ("Which of the following is an example of a workload?", ["A CPU core", "A network cable", "A payment processing application", "A power supply unit"], "c) A payment processing application"),
                ("What does the term multi-tenant refer to in cloud computing?", ["One customer uses multiple providers", "Multiple customers share the same physical infrastructure securely", "Tenant pays for multiple services", "Multiple VMs run on separate hardware"], "b) Multiple customers share the same physical infrastructure securely"),
                ("Which paradigm shift preceded the cloud computing era?", ["Mainframe to client-server", "Quantum to neural computing", "Edge to fog computing", "Serverless to container computing"], "a) Mainframe to client-server"),
                ("What is the main advantage of shifting from CAPEX to OPEX?", ["Higher long-term costs", "Reduced financial risk and improved cash flow", "More physical hardware control", "Slower deployment times"], "b) Reduced financial risk and improved cash flow"),
                ("Which of the following is NOT a benefit of cloud computing?", ["Elasticity", "Pay-as-you-go pricing", "Guaranteed zero downtime", "Broad network access"], "c) Guaranteed zero downtime"),
                ("What does rapid provisioning mean?", ["Slow manual setup of servers", "Quick automated allocation of resources", "Annual hardware refresh cycles", "Weekly software updates"], "b) Quick automated allocation of resources"),
            ],
            "matching": [
                ("Match the cloud deployment model with its description.", ["Public cloud", "Private cloud", "Hybrid cloud", "Community cloud"], ["Services offered over the public internet to multiple organizations", "Dedicated cloud infrastructure for a single organization", "Combination of public and private cloud infrastructures", "Shared infrastructure for organizations with common concerns"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the cloud computing pillar with its definition.", ["Abstraction", "Orchestration", "Utility billing", "Virtualization"], ["Hiding physical hardware behind software layers", "Automating deployment and scaling of resources", "Fine-grained metering and usage tracking", "Creating virtual instances from physical hardware"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the terminology with its correct meaning.", ["Cloud", "Workload", "Serverless", "Elasticity"], ["Shared pool of configurable computing resources", "Application or service running on resources", "Abstracted server management for developers", "Automatic scaling of resources based on demand"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the characteristic with its opposite.", ["Elasticity (Cloud)", "CAPEX (Traditional)", "Multi-tenant (Cloud)", "Measured service (Cloud)"], ["Fixed capacity (On-premise)", "OPEX (Cloud)", "Single-tenant (Dedicated)", "Flat rate billing (Traditional)"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the NIST essential characteristic with its technical enabler.", ["On-demand self-service", "Broad network access", "Resource pooling", "Rapid elasticity"], ["API Gateway and automation platform", "Standard protocols (HTTP/HTTPS) and CDNs", "Hypervisors and container runtimes", "Auto-scaling groups and orchestration"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the computing resource with its cloud abstraction.", ["Physical server", "Storage device", "Network switch", "Operating system"], ["Virtual machine instance", "Block or object storage volume", "Virtual network and subnets", "Container or VM image"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the business benefit with its cloud enabler.", ["Cost reduction", "Business agility", "Global reach", "Disaster recovery"], ["Pay-as-you-go and elimination of idle resources", "Rapid provisioning and experimentation", "Global infrastructure and CDN networks", "Automated backups and geo-redundancy"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the cloud service category with the provider example.", ["IaaS provider", "PaaS provider", "SaaS provider", "FaaS provider"], ["Amazon Web Services (EC2)", "Google App Engine", "Salesforce CRM", "AWS Lambda"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the historical era with its computing characteristic.", ["1960s-1970s", "1980s-1990s", "2000s", "2010s-present"], ["Mainframe centralized computing with terminals", "Client-server distributed personal computing", "Virtualization and utility computing emerge", "Cloud-native, containers, and serverless"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
                ("Match the financial term with its cloud relevance.", ["TCO", "ROI", "CapEx to OpEx shift", "FinOps"], ["Total cost including direct and indirect cloud expenses", "Measure of profitability from cloud investment", "Moving from upfront to operational spending", "Financial management practice for cloud spending"], ["a) -> n)", "b) -> o)", "c) -> p)", "d) -> q)"]),
            ],
        },
    }
    
    # For chapters 02-09, reuse and adapt. Since all_data only has 01_A and 01_B,
    # we need to return data for all. Let me load from a JSON file instead.
    return all_data.get(key, None)

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Quiz")
    
    # Use the data from the existing files approach - write JSON first
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_data.json")
    
    if not os.path.exists(json_path):
        print("ERROR: quiz_data.json not found!")
        print("Generate it first by running the companion script.")
        sys.exit(1)
    
    with open(json_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
    
    for chap_num in sorted(CHAPTER_SOURCES.keys()):
        sources = CHAPTER_SOURCES[chap_num]
        chap_dir = os.path.join(base_dir, "Chapter " + chap_num)
        os.makedirs(chap_dir, exist_ok=True)
        
        for variant in ["A", "B"]:
            key = chap_num + "_" + variant
            if key not in all_data:
                print("WARNING: No data for " + key + ", skipping")
                continue
            
            data = all_data[key]
            content = gen_file(sources, data["tf"], data["mcq"], data["matching"])
            
            filename = "Chapter " + chap_num + "_Quiz_" + variant + ".md"
            filepath = os.path.join(chap_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
            tf_c = len(data["tf"])
            mcq_c = len(data["mcq"])
            match_c = len(data["matching"])
            print("OK " + filename + ": " + str(tf_c) + " TF + " + str(mcq_c) + " MCQ + " + str(match_c) + " Matching = " + str(tf_c+mcq_c+match_c) + " questions")
    
    total = sum(1 for ch in CHAPTER_SOURCES for v in ["A", "B"] if ch + "_" + v in all_data)
    print("\n" + "=" * 50)
    print("Total: " + str(total) + " quiz files generated across " + str(len(CHAPTER_SOURCES)) + " chapters")
    print("Total questions: " + str(total * 30))