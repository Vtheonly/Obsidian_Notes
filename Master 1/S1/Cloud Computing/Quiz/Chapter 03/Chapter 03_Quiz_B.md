---
sources:
  - "[[Chapter 3 - Virtualization/3.1 Core Virtualization Concepts and Hypervisors.md]]"
  - "[[Chapter 3 - Virtualization/3.2 Anatomy and Technical Composition of a Virtual Machine.md]]"
  - "[[Chapter 3 - Virtualization/3.3 Virtual Machine Migration Techniques.md]]"
  - "[[Chapter 3 - Virtualization/3.4 Advanced Virtualization Paradigms and Security.md]]"
  - "[[Chapter 3 - Virtualization/3.7 What is a Virtual Machine.md]]"
  - "[[Chapter 3 - Virtualization/3.8 The Physical Machine - Racks, Servers, and Data Centers.md]]"
---

> [!question] Hardware emulation simulates entire hardware components in software.
>> [!success]- Answer
>> True

> [!question] A virtual machine includes virtual CPU, memory, storage, and network interfaces.
>> [!success]- Answer
>> True

> [!question] Containers use less overhead than full virtual machines.
>> [!success]- Answer
>> True

> [!question] Virtualization security risks include VM escape attacks.
>> [!success]- Answer
>> True

> [!question] A rack unit (U) is a standard measurement equal to 1.75 inches.
>> [!success]- Answer
>> True

> [!question] A rack unit (1U) equals how many inches in height?
> a) 1.00
> b) 1.75
> c) 2.00
> d) 3.50
>> [!success]- Answer
>> b) 1.75

> [!question] Which storage format is commonly used for virtual machine disk images?
> a) MP4
> b) VMDK
> c) PDF
> d) EXE
>> [!success]- Answer
>> b) VMDK

> [!question] Hardware emulation differs from system virtualization because:
> a) It is faster
> b) It simulates specific hardware components entirely in software
> c) It requires no hypervisor
> d) It uses only physical hardware
>> [!success]- Answer
>> b) It simulates specific hardware components entirely in software

> [!question] Memory overcommitment allows:
> a) Allocating more memory to VMs than physically available
> b) Reducing physical memory
> c) Eliminating swap space
> d) Disabling memory entirely
>> [!success]- Answer
>> a) Allocating more memory to VMs than physically available

> [!question] Which hypervisor type is typically used in enterprise data centers?
> a) Type 2
> b) Type 1
> c) Type 3
> d) Type 0
>> [!success]- Answer
>> b) Type 1

> [!question] Match the virtualization benefit with its effect.
>> [!example] Group A
>> a) Server consolidation
>> b) Isolation
>> c) Hardware independence
>> d) Snapshot capability
>
>> [!example] Group B
>> n) Running multiple VMs on fewer physical hosts
>> o) Faults in one VM do not affect others
>> p) VMs can run on different hardware platforms
>> q) Ability to capture VM state for backup
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the virtualization concept with its definition.
>> [!example] Group A
>> a) Hardware emulation
>> b) Full virtualization
>> c) Paravirtualization
>> d) OS-level virtualization
>
>> [!example] Group B
>> n) Simulating entire hardware architecture in software
>> o) Complete hardware abstraction with no OS modification
>> p) Guest OS is modified to improve performance
>> q) Sharing host kernel among multiple user spaces
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the VM file type with its purpose.
>> [!example] Group A
>> a) .vmdk or .vhd
>> b) .vmx or .config
>> c) .nvram
>> d) .log
>
>> [!example] Group B
>> n) Virtual disk data storage file
>> o) VM configuration and settings file
>> p) BIOS/UEFI firmware state file
>> q) Virtual machine log file
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the resource metric with its meaning in virtualization.
>> [!example] Group A
>> a) CPU ready time
>> b) Ballooning
>> c) Swap space
>> d) Overcommit ratio
>
>> [!example] Group B
>> n) Time VM is ready but waiting for CPU scheduling
>> o) Memory reclaim technique by hypervisor
>> p) Disk-based extension of physical memory
>> q) Ratio of allocated to physical resources
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the hardware feature with its virtualization support.
>> [!example] Group A
>> a) Intel VT-x
>> b) AMD-V
>> c) SR-IOV
>> d) NUMA
>
>> [!example] Group B
>> n) Intel hardware virtualization extensions
>> o) AMD hardware virtualization extensions
>> p) Single root I/O virtualization for direct device access
>> q) Non-uniform memory access architecture
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
