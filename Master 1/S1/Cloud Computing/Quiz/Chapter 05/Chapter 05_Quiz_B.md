---
sources:
  - "[[Chapter 5 - Containerization and Orchestration/5.1 Linux Kernel Isolation Mechanics - Namespaces and Cgroups.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.2 Docker Engine Architecture and Core Components.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.3 Dockerfile Mechanics and Multi-Container Applications.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.4 Container Orchestration and Kubernetes Foundations.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.5 Kubernetes Control Plane and Worker Node Architecture.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.6 Pod Scheduling, Resource Management, and Services.md]]"
---

> [!question] A Kubernetes cluster consists of a control plane and worker nodes.
>> [!success]- Answer
>> True

> [!question] A Pod in Kubernetes is the smallest deployable unit.
>> [!success]- Answer
>> True

> [!question] Docker Compose is used for managing single-container applications.
>> [!success]- Answer
>> False

> [!question] UnionFS allows filesystem layers to be stacked and shared.
>> [!success]- Answer
>> True

> [!question] Kubernetes Services provide stable network endpoints for Pods.
>> [!success]- Answer
>> True

> [!question] Docker Compose is used to:
> a) Deploy to Kubernetes
> b) Define and run multi-container Docker applications
> c) Build Linux kernels
> d) Manage databases
>> [!success]- Answer
>> b) Define and run multi-container Docker applications

> [!question] UnionFS enables:
> a) Network bonding
> b) Filesystem layering and sharing of common layers
> c) Memory overcommitment
> d) CPU pinning
>> [!success]- Answer
>> b) Filesystem layering and sharing of common layers

> [!question] A Kubernetes Service provides:
> a) Storage persistence
> b) Stable network endpoint for a set of Pods
> c) Container runtime
> d) Load balancer only for HTTP
>> [!success]- Answer
>> b) Stable network endpoint for a set of Pods

> [!question] kubelet is responsible for:
> a) Managing the control plane
> b) Running containers on each worker node
> c) Routing external traffic
> d) Storing secrets
>> [!success]- Answer
>> b) Running containers on each worker node

> [!question] Container orchestration automates:
> a) Only build processes
> b) Deployment, scaling, and management of containers
> c) Hardware provisioning
> d) Network cable installation
>> [!success]- Answer
>> b) Deployment, scaling, and management of containers

> [!question] Match the scaling concept with its description.
>> [!example] Group A
>> a) Horizontal scaling
>> b) Vertical scaling
>> c) Auto-scaling
>> d) Manual scaling
>
>> [!example] Group B
>> n) Adding more instances of a resource
>> o) Increasing capacity of existing instance
>> p) Automatic adjustment based on metrics
>> q) Administrator-initiated resource changes
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the network type with its Docker scope.
>> [!example] Group A
>> a) Bridge network
>> b) Host network
>> c) Overlay network
>> d) Macvlan network
>
>> [!example] Group B
>> n) Default isolated network for containers on same host
>> o) Container shares host network stack
>> p) Multi-host container communication across nodes
>> q) Assigns MAC addresses to containers
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Kubernetes workload resource with its use case.
>> [!example] Group A
>> a) DaemonSet
>> b) StatefulSet
>> c) Job
>> d) CronJob
>
>> [!example] Group B
>> n) Runs one Pod per node for system services
>> o) Manages stateful applications with stable identity
>> p) Runs a batch task to completion
>> q) Runs jobs on a scheduled basis
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the container storage option with its characteristic.
>> [!example] Group A
>> a) Volume
>> b) Bind mount
>> c) tmpfs mount
>> d) Ephemeral storage
>
>> [!example] Group B
>> n) Persistent storage managed by Docker
>> o) Maps host directory into container
>> p) In-memory storage for sensitive data
>> q) Storage tied to container lifecycle
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the orchestration benefit with its description.
>> [!example] Group A
>> a) Service discovery
>> b) Load balancing
>> c) Self-healing
>> d) Rolling updates
>
>> [!example] Group B
>> n) Automatic detection of available services
>> o) Distributing traffic across instances
>> p) Restarting failed containers automatically
>> q) Updating applications with zero downtime
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
