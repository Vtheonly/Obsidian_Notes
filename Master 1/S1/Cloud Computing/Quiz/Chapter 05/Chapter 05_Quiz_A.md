---
sources:
  - "[[Chapter 5 - Containerization and Orchestration/5.1 Linux Kernel Isolation Mechanics - Namespaces and Cgroups.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.2 Docker Engine Architecture and Core Components.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.3 Dockerfile Mechanics and Multi-Container Applications.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.4 Container Orchestration and Kubernetes Foundations.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.5 Kubernetes Control Plane and Worker Node Architecture.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.6 Pod Scheduling, Resource Management, and Services.md]]"
---

> [!question] Namespaces provide process isolation in the Linux kernel.
>> [!success]- Answer
>> True

> [!question] Cgroups control and limit resource usage of processes.
>> [!success]- Answer
>> True

> [!question] Docker uses a client-server architecture.
>> [!success]- Answer
>> True

> [!question] Docker images are built in read-only layers.
>> [!success]- Answer
>> True

> [!question] Kubernetes is a container orchestration platform.
>> [!success]- Answer
>> True

> [!question] Linux Namespaces provide:
> a) Resource limits
> b) Process isolation
> c) Network routing
> d) File compression
>> [!success]- Answer
>> b) Process isolation

> [!question] Cgroups (Control Groups) are used for:
> a) Creating users
> b) Limiting and accounting resource usage
> c) Managing DNS
> d) Compiling code
>> [!success]- Answer
>> b) Limiting and accounting resource usage

> [!question] Docker images are built using:
> a) A single flat file
> b) Read-only layers stacked on each other
> c) A database dump
> d) A compiled binary
>> [!success]- Answer
>> b) Read-only layers stacked on each other

> [!question] Kubernetes Pods are:
> a) Physical servers
> b) The smallest deployable units containing one or more containers
> c) Network switches
> d) Storage volumes
>> [!success]- Answer
>> b) The smallest deployable units containing one or more containers

> [!question] The Kubernetes control plane component that maintains desired state is:
> a) kubelet
> b) API Server
> c) etcd
> d) Controller Manager
>> [!success]- Answer
>> b) etcd

> [!question] Match the container concept with its description.
>> [!example] Group A
>> a) Docker image
>> b) Docker container
>> c) Dockerfile
>> d) Docker registry
>
>> [!example] Group B
>> n) Read-only template with instructions for creating a container
>> o) Runnable instance of an image
>> p) Script with commands to build an image
>> q) Repository for storing and distributing images
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Kubernetes component with its role.
>> [!example] Group A
>> a) API Server
>> b) etcd
>> c) Scheduler
>> d) Controller Manager
>
>> [!example] Group B
>> n) Entry point for all Kubernetes API requests
>> o) Distributed key-value store for cluster state
>> p) Assigns Pods to worker nodes
>> q) Runs controllers that maintain desired state
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Linux kernel feature with its function.
>> [!example] Group A
>> a) Namespaces
>> b) Cgroups
>> c) UnionFS
>> d) Capabilities
>
>> [!example] Group B
>> n) Provides process isolation
>> o) Limits and accounts resource usage
>> p) Enables filesystem layering
>> q) Grants fine-grained privileges
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Docker component with its description.
>> [!example] Group A
>> a) Docker daemon
>> b) Docker client
>> c) Docker Hub
>> d) Docker Compose
>
>> [!example] Group B
>> n) Background service managing containers
>> o) CLI tool that sends commands to daemon
>> p) Default public registry for images
>> q) Tool for defining multi-container applications
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Kubernetes object with its purpose.
>> [!example] Group A
>> a) Pod
>> b) Service
>> c) Deployment
>> d) ConfigMap
>
>> [!example] Group B
>> n) Smallest deployable unit with one or more containers
>> o) Stable network endpoint for Pods
>> p) Declarative update for Pods and ReplicaSets
>> q) Stores non-sensitive configuration data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
