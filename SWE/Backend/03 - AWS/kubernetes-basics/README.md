---
tags: [kubernetes, home, moc]
---

#  Kubernetes Basics

> [!info] Welcome
> This vault is a beginner-friendly guide to Kubernetes. Open any note below or follow the links inside each note to explore.

##  Map of Content

### 1. Introduction
- [[What is Kubernetes]]
- [[Why Kubernetes]]

### 2. Architecture
- [[Core Architecture]]
- [[Clusters]]
- [[Nodes]]

### 3. Workloads
- [[Pods]]
- [[Deployments]]
- [[ReplicaSets]]

### 4. Networking
- [[Services]]
- [[Basic Networking]]

### 5. Configuration
- [[Namespaces]]
- [[ConfigMaps and Secrets]]
- [[Volumes]]

### 6. Operations
- [[Basic Scaling]]
- [[Kubectl Commands]]
- [[Deploy a Simple Application]]

### 7. Reference
- [[Common Terminology]]
- [[Best Practices for Beginners]]

---

##  Suggested Learning Path

```mermaid
flowchart LR
    A[What is Kubernetes?] --> B[Why Kubernetes]
    B --> C[Core Architecture]
    C --> D[Clusters & Nodes]
    D --> E[Pods]
    E --> F[Deployments & ReplicaSets]
    F --> G[Services & Networking]
    G --> H[ConfigMaps/Secrets/Volumes]
    H --> I[kubectl Commands]
    I --> J[Deploy a Simple App]
    J --> K[Best Practices]
```

##  Quick Start

1. Install `kubectl` and a local cluster (kind / minikube / Docker Desktop).
2. Read [[What is Kubernetes]] and [[Why Kubernetes]].
3. Skim [[Core Architecture]] to understand the moving parts.
4. Run your first deployment with [[Deploy a Simple Application]].
