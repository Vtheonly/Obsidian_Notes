---
sources:
  - "[[Chapter 3 - Virtualization/3.1 Core Virtualization Concepts and Hypervisors.md]]"
  - "[[Chapter 3 - Virtualization/3.2 Anatomy and Technical Composition of a Virtual Machine.md]]"
  - "[[Chapter 3 - Virtualization/3.3 Virtual Machine Migration Techniques.md]]"
  - "[[Chapter 3 - Virtualization/3.4 Advanced Virtualization Paradigms and Security.md]]"
  - "[[Chapter 3 - Virtualization/3.5 Hypervisor Internals and Execution Types.md]]"
  - "[[Chapter 3 - Virtualization/3.6 VM Migration Mechanisms and State Transfer.md]]"
  - "[[Chapter 3 - Virtualization/3.7 What is a Virtual Machine.md]]"
  - "[[Chapter 3 - Virtualization/3.8 The Physical Machine - Racks, Servers, and Data Centers.md]]"
  - "[[Chapter 3 - Virtualization/3.9 What a Rack Unit Really Means.md]]"
  - "[[Chapter 3 - Virtualization/3.10 A Server is Not the Rack.md]]"
  - "[[Chapter 3 - Virtualization/3.11 Anatomy of a Virtual Machine and File Structures.md]]"
  - "[[Chapter 3 - Virtualization/3.12 Virtualization Security Risks and Threat Vectors.md]]"
  - "[[Chapter 3 - Virtualization/3.13 Hardware Emulation vs System Virtualization.md]]"
---

> [!question] Paravirtualization requires modifying the guest operating system.
>> [!success]- Answer
>> True

> [!question] Hardware-assisted virtualization uses CPU extensions like Intel VT-x.
>> [!success]- Answer
>> True

> [!question] A single physical machine can host only one virtual machine.
>> [!success]- Answer
>> False

> [!question] VM snapshots capture the entire state of a virtual machine at a point in time.
>> [!success]- Answer
>> True

> [!question] Type 1 hypervisors have a larger attack surface than Type 2.
>> [!success]- Answer
>> False

> [!question] Virtualization enables better resource utilization by consolidating workloads.
>> [!success]- Answer
>> True

> [!question] Cold migration requires the VM to be powered off before moving.
>> [!success]- Answer
>> True

> [!question] Network isolation is automatically guaranteed in all virtualized environments.
>> [!success]- Answer
>> False

> [!question] The host OS manages hardware directly in Type 2 hypervisor setups.
>> [!success]- Answer
>> True

> [!question] Overcommitment of resources can lead to performance degradation.
>> [!success]- Answer
>> True

> [!question] Which CPU feature enables hardware-assisted virtualization?
> a) SSE
> b) Intel VT-x / AMD-V
> c) AVX
> d) MMX
>> [!success]- Answer
>> b) Intel VT-x / AMD-V

> [!question] What is the primary disadvantage of Type 2 hypervisors?
> a) Difficult to install
> b) Limited hardware support
> c) Performance overhead from double scheduling
> d) Cannot run multiple VMs
>> [!success]- Answer
>> c) Performance overhead from double scheduling

> [!question] Which virtualization technique requires guest OS modifications?
> a) Full virtualization
> b) Paravirtualization
> c) Hardware emulation
> d) Containerization
>> [!success]- Answer
>> b) Paravirtualization

> [!question] What is VM sprawl?
> a) Rapid growth of VMs leading to management challenges
> b) A type of VM escape attack
> c) The process of migrating VMs
> d) A feature for automatic scaling
>> [!success]- Answer
>> a) Rapid growth of VMs leading to management challenges

> [!question] In a Type 2 hypervisor what happens if the host OS crashes?
> a) VMs continue running unaffected
> b) All VMs running on it crash as well
> c) VMs failover to another host automatically
> d) Only the hypervisor crashes
>> [!success]- Answer
>> b) All VMs running on it crash as well

> [!question] What is the purpose of a virtual disk file (.vmdk)?
> a) Stores the VM configuration
> b) Stores the guest OS and application data
> c) Manages network connections
> d) Logs VM operations
>> [!success]- Answer
>> b) Stores the guest OS and application data

> [!question] Which technology provides process-level isolation without full virtualization?
> a) Hypervisors
> b) Containers
> c) Hardware emulators
> d) Virtual appliances
>> [!success]- Answer
>> b) Containers

> [!question] What does VM consolidation mean?
> a) Deleting unused VMs
> b) Running multiple VMs on fewer physical hosts
> c) Merging two VMs into one
> d) Compressing VM disk files
>> [!success]- Answer
>> b) Running multiple VMs on fewer physical hosts

> [!question] Which is NOT a benefit of virtualization?
> a) Hardware independence
> b) Improved disaster recovery
> c) Elimination of all security risks
> d) Legacy system support
>> [!success]- Answer
>> c) Elimination of all security risks

> [!question] What does a hypervisor use to allocate CPU time to VMs?
> a) Time-sharing scheduling
> b) Dedicated processor per VM
> c) Sequential execution
> d) Manual assignment
>> [!success]- Answer
>> a) Time-sharing scheduling

> [!question] Match the virtualization layer with its role.
>> [!example] Group A
>> a) Physical hardware
>> b) Hypervisor
>> c) Guest OS
>> d) Application
>
>> [!example] Group B
>> n) CPU memory storage network interfaces
>> o) Abstraction and resource management layer
>> p) Operating system running inside a VM
>> q) Software running on the guest OS
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the resource type with its virtualization approach.
>> [!example] Group A
>> a) CPU virtualization
>> b) Memory virtualization
>> c) Storage virtualization
>> d) Network virtualization
>
>> [!example] Group B
>> n) Time-slicing and hardware-assisted execution
>> o) Shadow page tables and NUMA awareness
>> p) Abstraction of physical storage into pools
>> q) Virtual switches and software-defined networking
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the VM operation with its description.
>> [!example] Group A
>> a) Provisioning
>> b) Snapshotting
>> c) Cloning
>> d) Template creation
>
>> [!example] Group B
>> n) Creating and configuring a new virtual machine
>> o) Capturing a point-in-time state of a VM
>> p) Creating a copy of an existing VM
>> q) Creating a reusable master VM image
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the data center term with its definition.
>> [!example] Group A
>> a) Rack
>> b) Blade server
>> c) SAN
>> d) PDU
>
>> [!example] Group B
>> n) Standard frame for mounting server equipment
>> o) Compact server module fitting in a chassis
>> p) Storage Area Network for block-level storage
>> q) Power Distribution Unit for rack power management
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the migration technique with downtime impact.
>> [!example] Group A
>> a) Cold migration
>> b) Live migration (vMotion)
>> c) Storage vMotion
>> d) Cross-vCenter migration
>
>> [!example] Group B
>> n) Full downtime during migration
>> o) Zero to minimal downtime
>> p) Zero downtime for storage moves
>> q) Minimal downtime across vCenter instances
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the security concern with its layer.
>> [!example] Group A
>> a) VM escape
>> b) Guest OS compromise
>> c) Hypervisor vulnerability
>> d) Management plane breach
>
>> [!example] Group B
>> n) Virtualization layer boundary
>> o) Individual virtual machine
>> p) Hypervisor software itself
>> q) Administrative console or API
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the container term with its Linux kernel mechanism.
>> [!example] Group A
>> a) Process isolation
>> b) Resource limits
>> c) Filesystem isolation
>> d) Network isolation
>
>> [!example] Group B
>> n) PID namespaces
>> o) Cgroups (control groups)
>> p) Mount namespaces
>> q) Network namespaces
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the virtualization type with overhead level.
>> [!example] Group A
>> a) Full virtualization (software)
>> b) Paravirtualization
>> c) Hardware-assisted virtualization
>> d) Containerization
>
>> [!example] Group B
>> n) High overhead (binary translation)
>> o) Moderate overhead (modified guest)
>> p) Low overhead (CPU extensions)
>> q) Minimal overhead (kernel sharing)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the resource allocation term.
>> [!example] Group A
>> a) Reservation
>> b) Limit
>> c) Share
>> d) Overcommitment
>
>> [!example] Group B
>> n) Guaranteed minimum resource for a VM
>> o) Maximum resource a VM can consume
>> p) Relative priority weight for resources
>> q) Allocating more resources than physically available
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the hypervisor challenge with mitigation.
>> [!example] Group A
>> a) Performance overhead
>> b) Security isolation
>> c) Resource contention
>> d) Management complexity
>
>> [!example] Group B
>> n) Hardware-assisted virtualization extensions
>> o) Strong isolation boundaries and patching
>> p) Resource pools and reserved allocations
>> q) Centralized management platforms
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
