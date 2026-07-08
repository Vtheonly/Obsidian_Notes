---
tags: [kubernetes, architecture]
---

# Core Architecture

> [!summary] TL;DR
> A Kubernetes cluster has two main parts: the **Control Plane** (the "brain") and **Worker Nodes** (the "muscle"). They communicate via the API Server.

## High-Level Architecture

```mermaid
flowchart TB
    User([User / kubectl / CI]) -->|HTTPS| API[API Server]

    subgraph CP[Control Plane]
        API[API Server]
        ETCD[(etcd)]
        SCHED[Scheduler]
        CM[Controller Manager]
        API <--> ETCD
        API --> SCHED
        API --> CM
    end

    subgraph Node1[Worker Node 1]
        KUBELET1[kubelet]
        PROXY1[kube-proxy]
        CRI1[Container Runtime<br/>containerd]
        POD1[Pod A]
        POD2[Pod B]
        KUBELET1 --> CRI1 --> POD1
        KUBELET1 --> CRI1 --> POD2
        PROXY1 -.-> POD1
    end

    API <-->|watch/watch| KUBELET1
    API <--> KUBELET1
```

## Control Plane Components

| Component                  | Role                                                                         |
| -------------------------- | ----------------------------------------------------------------------------- |
| **API Server** (`kube-apiserver`) | The front door. All components and users talk to it over REST/HTTPS.    |
| **etcd**                   | Strongly-consistent key-value store. Source of truth for cluster state.      |
| **Scheduler** (`kube-scheduler`) | Decides which node a new Pod runs on based on resources, taints, etc.   |
| **Controller Manager**     | Runs control loops (replica set, node, deployment, endpoint controllers).    |
| **Cloud Controller Manager** | Optional; integrates with cloud provider APIs (load balancers, volumes).    |

> [!note] Source of truth
> `etcd` is the **only** place cluster state lives. If you lose etcd without a backup, you lose the cluster.

## Worker Node Components

| Component                | Role                                                                            |
| ------------------------ | -------------------------------------------------------------------------------- |
| **kubelet**              | Agent on each node. Talks to API server, ensures pods are running & healthy.    |
| **kube-proxy**           | Maintains network rules for [[Services]] (iptables / IPVS).                     |
| **Container Runtime**    | Runs containers. Usually **containerd** (formerly Docker). CRI-compatible.      |
| **Pods**                 | The smallest deployable unit. See [[Pods]].                                     |

## How a Request Flows (Deployment example)

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant API as API Server
    participant ETCD as etcd
    participant SCHED as Scheduler
    participant CM as Controller Manager
    participant K as kubelet (Node X)
    participant CRI as Container Runtime

    U->>API: kubectl apply -f deployment.yaml
    API->>ETCD: persist Deployment object
    CM->>API: watch detects new Deployment
    CM->>API: create ReplicaSet
    CM->>API: (ReplicaSet controller) create Pods (pending)
    SCHED->>API: watch detects pending Pods
    SCHED->>API: bind Pod to Node X
    K->>API: watch detects Pod bound to its node
    K->>CRI: pull image, start containers
    K->>API: report Pod status = Running
```

## Concepts Recap

- [[Clusters]] — the whole thing (control plane + nodes).
- [[Nodes]] — individual machines (or VMs).
- [[Pods]] — what actually runs your containers.

## Related Notes
- [[Clusters]] · [[Nodes]] · [[Pods]] · [[Common Terminology]]
