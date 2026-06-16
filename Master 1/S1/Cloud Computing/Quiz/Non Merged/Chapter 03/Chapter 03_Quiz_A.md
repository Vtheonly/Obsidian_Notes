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

> [!question] Virtualization is the foundational technology that enables cloud computing.
>> [!success]- Answer
>> True

> [!question] A Type 1 hypervisor runs on top of a host operating system.
>> [!success]- Answer
>> False

> [!question] A hypervisor is also known as a Virtual Machine Monitor (VMM).
>> [!success]- Answer
>> True

> [!question] Type 2 hypervisors provide near-native performance compared to Type 1.
>> [!success]- Answer
>> False

> [!question] VMware ESXi is an example of a Type 1 hypervisor.
>> [!success]- Answer
>> True

> [!question] A guest system refers to the physical machine running the hypervisor.
>> [!success]- Answer
>> False

> [!question] Live migration allows a running VM to be moved between hosts without downtime.
>> [!success]- Answer
>> True

> [!question] Hardware emulation virtualizes the CPU at the instruction level which is very fast.
>> [!success]- Answer
>> False

> [!question] Containers share the host operating system kernel.
>> [!success]- Answer
>> True

> [!question] Virtualization security risks include VM escape attacks.
>> [!success]- Answer
>> True

> [!question] Which type of hypervisor installs directly on physical hardware?
> a) Type 1 (Bare-metal)
> b) Type 2 (Hosted)
> c) Type 3 (Embedded)
> d) Type 0 (Native)
>> [!success]- Answer
>> a) Type 1 (Bare-metal)

> [!question] What is the main advantage of a Type 1 hypervisor over Type 2?
> a) Easier installation
> b) Near-native performance
> c) Broader hardware support
> d) Lower cost
>> [!success]- Answer
>> b) Near-native performance

> [!question] Which of the following is a Type 2 hypervisor?
> a) VMware ESXi
> b) Microsoft Hyper-V
> c) Oracle VM VirtualBox
> d) Xen
>> [!success]- Answer
>> c) Oracle VM VirtualBox

> [!question] What is a host system in virtualization?
> a) The guest operating system
> b) The physical machine providing resources
> c) The hypervisor management console
> d) The virtual network switch
>> [!success]- Answer
>> b) The physical machine providing resources

> [!question] What does live migration enable?
> a) Moving a VM while powered off
> b) Moving a running VM to another host with minimal disruption
> c) Creating a snapshot
> d) Deleting a VM from storage
>> [!success]- Answer
>> b) Moving a running VM to another host with minimal disruption

> [!question] Which virtualization risk involves a guest OS accessing the hypervisor?
> a) Resource exhaustion
> b) VM escape
> c) Snapshot sprawl
> d) Network isolation failure
>> [!success]- Answer
>> b) VM escape

> [!question] What is the function of a hypervisor?
> a) Compile application code
> b) Manage and isolate virtual machines on physical hardware
> c) Encrypt network traffic
> d) Provide internet connectivity
>> [!success]- Answer
>> b) Manage and isolate virtual machines on physical hardware

> [!question] Which statement about containers vs VMs is correct?
> a) Containers have their own kernel
> b) VMs share the host kernel
> c) Containers share the host kernel
> d) VMs are lighter than containers
>> [!success]- Answer
>> c) Containers share the host kernel

> [!question] What is hardware emulation?
> a) Running code natively on CPU
> b) Simulating hardware components entirely in software
> c) Using physical devices directly
> d) Overclocking the processor
>> [!success]- Answer
>> b) Simulating hardware components entirely in software

> [!question] Which characteristic is unique to Type 2 hypervisors?
> a) Direct hardware access
> b) Requires a host operating system
> c) Enterprise-grade scalability
> d) Used in data centers exclusively
>> [!success]- Answer
>> b) Requires a host operating system

> [!question] Match the virtualization term with its definition.
>> [!example] Group A
>> a) Hypervisor
>> b) Guest OS
>> c) Host system
>> d) VM snapshot
>
>> [!example] Group B
>> n) Software layer managing VMs on physical hardware
>> o) Operating system running inside a virtual machine
>> p) Physical machine providing CPU memory and storage
>> q) Point-in-time state of a virtual machine
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the hypervisor type with its characteristic.
>> [!example] Group A
>> a) Type 1 hypervisor
>> b) Type 2 hypervisor
>> c) Bare-metal hypervisor
>> d) Hosted hypervisor
>
>> [!example] Group B
>> n) Installs directly on physical hardware
>> o) Runs as application on host OS
>> p) Used in enterprise data centers
>> q) Used for local development and testing
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the virtualization concept with its benefit.
>> [!example] Group A
>> a) VM isolation
>> b) Live migration
>> c) Snapshot and restore
>> d) Resource overcommitment
>
>> [!example] Group B
>> n) Fault containment between VMs
>> o) Zero-downtime maintenance
>> p) Quick recovery from failures
>> q) Higher physical resource utilization
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the virtualization technology with its use case.
>> [!example] Group A
>> a) Full virtualization
>> b) Paravirtualization
>> c) Hardware-assisted virtualization
>> d) Containerization
>
>> [!example] Group B
>> n) Running unmodified guest OS with software emulation
>> o) Modified guest OS with hypervisor calls
>> p) Using CPU extensions (Intel VT-x / AMD-V)
>> q) Lightweight process isolation sharing host kernel
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the security risk with its virtualization context.
>> [!example] Group A
>> a) VM escape
>> b) Hyperjack
>> c) Snap theft
>> d) Resource starvation
>
>> [!example] Group B
>> n) Guest breaks out to access hypervisor
>> o) Attacker gains control of hypervisor layer
>> p) Unauthorized access to VM snapshot files
>> q) One VM consumes all resources starving others
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the VM component with its purpose.
>> [!example] Group A
>> a) vCPU
>> b) vRAM
>> c) Virtual disk
>> d) Virtual NIC
>
>> [!example] Group B
>> n) Virtual processor allocated to a VM
>> o) Virtual memory allocated to a VM
>> p) Virtual storage device for the VM
>> q) Virtual network interface for the VM
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the hardware term with its data center significance.
>> [!example] Group A
>> a) Rack unit (U)
>> b) Server chassis
>> c) Power distribution unit
>> d) Top-of-rack switch
>
>> [!example] Group B
>> n) Standardized height measurement for equipment (1.75 inches)
>> o) Enclosure holding multiple server blades
>> p) Distributes electrical power to rack equipment
>> q) Network switch at the top of a server rack
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the migration type with its behavior.
>> [!example] Group A
>> a) Cold migration
>> b) Live migration
>> c) Storage migration
>> d) Cross-platform migration
>
>> [!example] Group B
>> n) Migrating a powered-off VM
>> o) Migrating a running VM with no downtime
>> p) Moving VM storage between datastores
>> q) Moving VM between different hypervisor types
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the VM file type with its extension.
>> [!example] Group A
>> a) VM configuration file
>> b) Virtual disk file
>> c) Snapshot file
>> d) VM log file
>
>> [!example] Group B
>> n) .vmx or .xml
>> o) .vmdk or .vhdx
>> p) .vmsn or .snap
>> q) .log
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the industry product with its hypervisor type.
>> [!example] Group A
>> a) VMware ESXi
>> b) Oracle VirtualBox
>> c) Microsoft Hyper-V
>> d) Xen
>
>> [!example] Group B
>> n) Type 1 bare-metal hypervisor
>> o) Type 2 hosted hypervisor
>> p) Type 1 bare-metal hypervisor
>> q) Type 1 bare-metal hypervisor
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
