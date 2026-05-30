---
sources:
  - "[[Chapter 5 - Containerization and Orchestration/5.1 Linux Kernel Isolation Mechanics - Namespaces and Cgroups.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.2 Docker Engine Architecture and Core Components.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.3 Dockerfile Mechanics and Multi-Container Applications.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.4 Container Orchestration and Kubernetes Foundations.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.5 Kubernetes Control Plane and Worker Node Architecture.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.6 Pod Scheduling, Resource Management, and Services.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.7 Linux Kernel Internals (Namespaces, Cgroups, UnionFS).md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.8 Kubernetes Architecture and Pod Scheduling Workflow.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.9 Docker Engine Architecture and Container Lifecycle.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.10 Dockerfile Layering and Image Build Mechanics.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.11 Microservices, Docker Compose, and Container Networking.md]]"
  - "[[Chapter 5 - Containerization and Orchestration/5.12 Kubernetes Networking, Services, and Configuration Management.md]]"
---

> [!question] Containers share the host operating system kernel for resource efficiency.
>> [!success]- Answer
>> True

> [!question] Docker uses a hypervisor to run containers.
>> [!success]- Answer
>> False

> [!question] Namespaces in Linux provide resource isolation for containers.
>> [!success]- Answer
>> True

> [!question] Cgroups control groups limit and monitor resource usage.
>> [!success]- Answer
>> True

> [!question] The Docker Daemon (dockerd) is the client interface for Docker commands.
>> [!success]- Answer
>> False

> [!question] Kubernetes uses a master-worker architecture.
>> [!success]- Answer
>> True

> [!question] The kube-scheduler assigns pods to worker nodes based on resource requirements.
>> [!success]- Answer
>> True

> [!question] etcd is Kubernetes backing store for all cluster data.
>> [!success]- Answer
>> True

> [!question] Docker images are built in layers each representing a change.
>> [!success]- Answer
>> True

> [!question] Kube-proxy runs on the control plane node only.
>> [!success]- Answer
>> False

> [!question] Which Linux feature provides process isolation for containers?
> a) Cgroups
> b) Namespaces
> c) Systemd
> d) System calls
>> [!success]- Answer
>> b) Namespaces

> [!question] What is the role of the Docker Daemon?
> a) CLI interface
> b) Background service managing Docker objects
> c) Container registry
> d) Image build tool
>> [!success]- Answer
>> b) Background service managing Docker objects

> [!question] Which Kubernetes component stores cluster state?
> a) kube-apiserver
> b) kube-scheduler
> c) etcd
> d) kubelet
>> [!success]- Answer
>> c) etcd

> [!question] What does a container runtime do?
> a) Manages Docker images
> b) Runs containers using Linux kernel features
> c) Provides network routing
> d) Stores container logs
>> [!success]- Answer
>> b) Runs containers using Linux kernel features

> [!question] Which namespace type isolates network interfaces?
> a) PID namespace
> b) NET namespace
> c) MNT namespace
> d) UTS namespace
>> [!success]- Answer
>> b) NET namespace

> [!question] What is the purpose of a Dockerfile?
> a) Configure Docker Daemon
> b) Define the steps to build a Docker image
> c) Manage Docker networks
> d) Start Docker containers
>> [!success]- Answer
>> b) Define the steps to build a Docker image

> [!question] Which component maintains pod replicas?
> a) kube-apiserver
> b) kube-controller-manager
> c) kube-scheduler
> d) kube-proxy
>> [!success]- Answer
>> b) kube-controller-manager

> [!question] What is the function of kubelet?
> a) Schedule pods on nodes
> b) Agent on each worker node ensuring containers are running
> c) Store cluster configuration
> d) Route network traffic
>> [!success]- Answer
>> b) Agent on each worker node ensuring containers are running

> [!question] What does UnionFS enable in Docker?
> a) Union of multiple filesystems into one
> b) Network isolation
> c) Process isolation
> d) Resource limiting
>> [!success]- Answer
>> a) Union of multiple filesystems into one

> [!question] A Kubernetes Pod is:
> a) A single container
> b) The smallest deployable unit with one or more containers
> c) A cluster of machines
> d) A type of service
>> [!success]- Answer
>> b) The smallest deployable unit with one or more containers

> [!question] Match the Kubernetes component with function.
>> [!example] Group A
>> a) kube-apiserver
>> b) kube-scheduler
>> c) kube-controller-manager
>> d) etcd
>
>> [!example] Group B
>> n) Front-end for the Kubernetes API
>> o) Selects best node for new pods
>> p) Runs background control loops for cluster state
>> q) Distributed key-value store for cluster data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Linux namespace with what it isolates.
>> [!example] Group A
>> a) PID namespace
>> b) NET namespace
>> c) MNT namespace
>> d) USER namespace
>
>> [!example] Group B
>> n) Process ID tree isolation
>> o) Network interfaces and routing
>> p) Filesystem mount points
>> q) User and group ID mapping
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Docker component with its role.
>> [!example] Group A
>> a) Docker client (CLI)
>> b) Docker Daemon (dockerd)
>> c) Docker registry
>> d) containerd
>
>> [!example] Group B
>> n) Sends commands to the Docker Daemon
>> o) Background service managing containers and images
>> p) Stores and distributes container images
>> q) Industry-standard container runtime
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Cgroup controller with resource limits.
>> [!example] Group A
>> a) cpu cgroup
>> b) memory cgroup
>> c) blkio cgroup
>> d) pids cgroup
>
>> [!example] Group B
>> n) CPU cycles and core usage
>> o) Memory consumption limits
>> p) Disk I/O bandwidth
>> q) Number of processes a container can create
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
>> n) Smallest deployable unit with containers
>> o) Stable network endpoint for pods
>> p) Declarative updates for pods and ReplicaSets
>> q) Stores configuration data separately from pods
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Docker layer concept.
>> [!example] Group A
>> a) Base image
>> b) Intermediate layer
>> c) Container layer
>> d) Cache layer
>
>> [!example] Group B
>> n) Starting point for Docker images
>> o) Read-only layer from each Dockerfile instruction
>> p) Writable layer added when container runs
>> q) Reused layer to speed up builds
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match orchestration concept with Kubernetes.
>> [!example] Group A
>> a) Desired state
>> b) Self-healing
>> c) Scaling
>> d) Rolling update
>
>> [!example] Group B
>> n) Declared in Deployment spec
>> o) Replaces failed pods automatically
>> p) Changes replica count based on load
>> q) Gradually updates pod versions without downtime
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match Docker network driver with isolation.
>> [!example] Group A
>> a) bridge
>> b) host
>> c) overlay
>> d) none
>
>> [!example] Group B
>> n) Default isolated network for containers on one host
>> o) Container uses hosts network stack directly
>> p) Multi-host container networking across nodes
>> q) Container has no network access
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the Dockerfile instruction with purpose.
>> [!example] Group A
>> a) FROM
>> b) RUN
>> c) CMD
>> d) EXPOSE
>
>> [!example] Group B
>> n) Sets the base image for the build
>> o) Executes a command during build
>> p) Defines default command when container starts
>> q) Informs Docker of containers listening port
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the observability concept with Kubernetes tool.
>> [!example] Group A
>> a) Metrics collection
>> b) Logging
>> c) Distributed tracing
>> d) Health probes
>
>> [!example] Group B
>> n) Prometheus and Metrics Server
>> o) Fluentd and Elasticsearch
>> p) Jaeger or Zipkin
>> q) Liveness and readiness probes
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
