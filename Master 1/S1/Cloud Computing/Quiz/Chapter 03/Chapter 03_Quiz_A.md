---
sources:
  - "[[Chapter 3 - Virtualization/3.1 Core Virtualization Concepts and Hypervisors.md]]"
  - "[[Chapter 3 - Virtualization/3.2 Anatomy and Technical Composition of a Virtual Machine.md]]"
  - "[[Chapter 3 - Virtualization/3.3 Virtual Machine Migration Techniques.md]]"
  - "[[Chapter 3 - Virtualization/3.4 Advanced Virtualization Paradigms and Security.md]]"
  - "[[Chapter 3 - Virtualization/3.7 What is a Virtual Machine.md]]"
  - "[[Chapter 3 - Virtualization/3.8 The Physical Machine - Racks, Servers, and Data Centers.md]]"
---

> [!question] A hypervisor is software that creates and manages virtual machines.
>> [!success]- Answer
>> True

> [!question] Type 1 hypervisors run directly on the host hardware.
>> [!success]- Answer
>> True

> [!question] Type 2 hypervisors run on top of an existing operating system.
>> [!success]- Answer
>> True

> [!question] VM migration can transfer a running virtual machine between physical hosts.
>> [!success]- Answer
>> True

> [!question] Memory overcommitment is not possible in virtualized environments.
>> [!success]- Answer
>> False

> [!question] What is the primary function of a hypervisor?
> a) To manage physical network cables
> b) To create and manage virtual machines
> c) To compile source code
> d) To encrypt data
>> [!success]- Answer
>> b) To create and manage virtual machines

> [!question] Type 1 hypervisors run:
> a) On top of an operating system
> b) Directly on host hardware
> c) Inside a virtual machine
> d) As a user application
>> [!success]- Answer
>> b) Directly on host hardware

> [!question] VM migration that transfers a running VM with no downtime is called:
> a) Cold migration
> b) Hot migration / Live migration
> c) Snapshot migration
> d) Template migration
>> [!success]- Answer
>> b) Hot migration / Live migration

> [!question] Which component represents a virtual CPU in a VM?
> a) VHDX
> b) vCPU
> c) VMDK
> d) VNC
>> [!success]- Answer
>> b) vCPU

> [!question] What is a VM escape attack?
> a) Deleting a VM accidentally
> b) An attacker breaking out of a VM to access the hypervisor
> c) Migrating a VM to another host
> d) Backing up a VM snapshot
>> [!success]- Answer
>> b) An attacker breaking out of a VM to access the hypervisor

> [!question] Match the hypervisor type with its description.
>> [!example] Group A
>> a) Type 1 hypervisor
>> b) Type 2 hypervisor
>> c) Bare-metal hypervisor
>> d) Hosted hypervisor
>
>> [!example] Group B
>> n) Runs directly on hardware without host OS
>> o) Runs on top of an existing operating system
>> p) Another name for Type 1
>> q) Another name for Type 2
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the VM component with its function.
>> [!example] Group A
>> a) vCPU
>> b) vRAM
>> c) VMDK
>> d) Virtual NIC
>
>> [!example] Group B
>> n) Virtual processor for computation
>> o) Virtual memory for running processes
>> p) Virtual disk file for persistent storage
>> q) Virtual network interface for connectivity
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the migration type with its characteristic.
>> [!example] Group A
>> a) Cold migration
>> b) Live migration
>> c) Storage migration
>> d) Cross-host migration
>
>> [!example] Group B
>> n) VM is powered off during transfer
>> o) VM remains running with zero downtime
>> p) Moving virtual disk files between datastores
>> q) Moving VM to a different physical server
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the security risk with its description.
>> [!example] Group A
>> a) VM escape
>> b) Hypervisor compromise
>> c) VM sprawl
>> d) Resource starvation
>
>> [!example] Group B
>> n) Breaking out of VM to access other systems
>> o) Attacking the virtualization layer directly
>> p) Uncontrolled proliferation of VMs
>> q) Denial of resource access to legitimate VMs
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the data center component with its unit.
>> [!example] Group A
>> a) Rack
>> b) Server
>> c) Rack Unit (1U)
>> d) Chassis
>
>> [!example] Group B
>> n) Frame housing multiple servers
>> o) Individual computing node
>> p) Standard height of 1.75 inches
>> q) Enclosure for multiple blades
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
