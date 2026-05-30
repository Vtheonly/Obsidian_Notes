#!/usr/bin/env python3
"""Convert quiz_data.json to markdown quiz files."""
import os, json

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

def matching_block(q, ga, gb, ans):
    al = ["a", "b", "c", "d"]
    bl = ["n", "o", "p", "q"]
    ab = "\n".join([">> " + al[i] + ") " + x for i, x in enumerate(ga)])
    bb = "\n".join([">> " + bl[i] + ") " + x for i, x in enumerate(gb)])
    anb = "\n".join([">> " + a for a in ans])
    return "> [!question] " + q + "\n>> [!example] Group A\n" + ab + "\n>\n>> [!example] Group B\n" + bb + "\n>\n>> [!success]- Answer\n" + anb

def gen_md(sources, tf, mcq, match):
    parts = [build_yaml(sources), ""]
    for q, a in tf:
        parts.append(tf_block(q, a))
        parts.append("")
    for q, opts, ans in mcq:
        parts.append(mcq_block(q, opts, ans))
        parts.append("")
    for q, ga, gb, al in match:
        parts.append(matching_block(q, ga, gb, al))
        parts.append("")
    return "\n".join(parts).strip() + "\n"

if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Quiz")
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz_data.json")
    with open(json_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
    
    count = 0
    for ch in sorted(CHAPTER_SOURCES.keys()):
        d = os.path.join(base, "Chapter " + ch)
        os.makedirs(d, exist_ok=True)
        for v in ["A", "B"]:
            key = ch + "_" + v
            if key not in all_data:
                continue
            data = all_data[key]
            content = gen_md(CHAPTER_SOURCES[ch], data["tf"], data["mcq"], data["matching"])
            fn = "Chapter " + ch + "_Quiz_" + v + ".md"
            with open(os.path.join(d, fn), "w", encoding="utf-8") as f:
                f.write(content)
            tc = len(data["tf"])
            mc = len(data["mcq"])
            mtc = len(data["matching"])
            print("OK " + fn + ": " + str(tc) + " TF + " + str(mc) + " MCQ + " + str(mtc) + " Matching = " + str(tc+mc+mtc))
            count += 1
    print("Done: " + str(count) + " files, " + str(count*30) + " questions")