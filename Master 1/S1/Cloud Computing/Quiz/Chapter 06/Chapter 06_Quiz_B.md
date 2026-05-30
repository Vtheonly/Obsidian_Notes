---
sources:
  - "[[Chapter 6 - Virtual and Networked Storage/6.1 Storage Foundations and Access Models.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.2 Networked Storage Architectures - DAS NAS SAN.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.3 Storage Virtualization, Datastores, and High Availability.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.4 Block vs File Access and SAN vs NAS Architectures.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.5 RAID, Datastores, and Advanced Storage Features.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.6 Solving Storage Silos with Virtualization and Pooling.md]]"
---

> [!question] Block storage exposes raw sectors of fixed size to the host operating system.
>> [!success]- Answer
>> True

> [!question] File access model allows clients to access files and directories over the network.
>> [!success]- Answer
>> True

> [!question] DAS (Direct Attached Storage) can be shared across multiple physical servers.
>> [!success]- Answer
>> False

> [!question] NAS provides file-level storage access over a standard TCP/IP network.
>> [!success]- Answer
>> True

> [!question] SAN provides block-level storage access over a dedicated high-speed network.
>> [!success]- Answer
>> True

> [!question] RAID 0 provides data redundancy through mirroring.
>> [!success]- Answer
>> False

> [!question] Storage virtualization aggregates physical storage into a single pool.
>> [!success]- Answer
>> True

> [!question] Datastores are logical containers that hold virtual machine files.
>> [!success]- Answer
>> True

> [!question] NAS uses low-level SCSI commands for communication.
>> [!success]- Answer
>> False

> [!question] Storage thin provisioning allocates physical storage only when data is written.
>> [!success]- Answer
>> True

> [!question] Which storage architecture connects directly to a single host server?
> a) NAS
> b) SAN
> c) DAS
> d) Object storage
>> [!success]- Answer
>> c) DAS

> [!question] What protocol does NAS typically use?
> a) SCSI
> b) NFS or SMB
> c) NVMe
> d) Fibre Channel
>> [!success]- Answer
>> b) NFS or SMB

> [!question] Which storage uses Fibre Channel as a dedicated network?
> a) DAS
> b) NAS
> c) SAN
> d) Object storage
>> [!success]- Answer
>> c) SAN

> [!question] What is a key advantage of NAS over DAS?
> a) Lower latency
> b) Multi-host file sharing over network
> c) Block-level access
> d) Direct hardware access
>> [!success]- Answer
>> b) Multi-host file sharing over network

> [!question] What does RAID stand for?
> a) Redundant Array of Independent Disks
> b) Random Access Integrated Drive
> c) Rapid Automated I/O Device
> d) Remote Attached Internet Drive
>> [!success]- Answer
>> a) Redundant Array of Independent Disks

> [!question] Which RAID level provides mirroring?
> a) RAID 0
> b) RAID 1
> c) RAID 5
> d) RAID 10
>> [!success]- Answer
>> b) RAID 1

> [!question] What is storage virtualization?
> a) Encrypting all stored data
> b) Abstracting physical storage into a unified logical pool
> c) Compressing data
> d) Replicating data across data centers
>> [!success]- Answer
>> b) Abstracting physical storage into a unified logical pool

> [!question] What is a datastore in virtualization?
> a) A physical storage device
> b) A logical container for VM files and templates
> c) A network protocol
> d) A type of hypervisor
>> [!success]- Answer
>> b) A logical container for VM files and templates

> [!question] Which enables high availability through shared storage?
> a) DAS only
> b) NAS and SAN
> c) Local SSDs
> d) USB drives
>> [!success]- Answer
>> b) NAS and SAN

> [!question] What is the main disadvantage of DAS?
> a) High cost
> b) No multi-host sharing leading to poor utilization
> c) Low performance
> d) Complex setup
>> [!success]- Answer
>> b) No multi-host sharing leading to poor utilization

> [!question] Match storage architecture with connection method.
>> [!example] Group A
>> a) DAS
>> b) NAS
>> c) SAN
>> d) Object storage
>
>> [!example] Group B
>> n) Direct cable (SATA SAS NVMe)
>> o) Standard LAN/Ethernet network
>> p) Dedicated Fibre Channel or iSCSI network
>> q) HTTP/HTTPS REST API over internet
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match RAID level with characteristic.
>> [!example] Group A
>> a) RAID 0
>> b) RAID 1
>> c) RAID 5
>> d) RAID 10
>
>> [!example] Group B
>> n) Striping without redundancy
>> o) Mirroring for fault tolerance
>> p) Striping with parity
>> q) Mirroring and striping combined
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match access model with data unit.
>> [!example] Group A
>> a) Block access
>> b) File access
>> c) Object access
>> d) Stream access
>
>> [!example] Group B
>> n) Raw sectors (512 bytes / 4KB blocks)
>> o) Files and directories
>> p) Objects with metadata in flat namespace
>> q) Continuous data flow
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage term with definition.
>> [!example] Group A
>> a) LUN
>> b) Volume
>> c) Datastore
>> d) Snapshot
>
>> [!example] Group B
>> n) Logical Unit Number in SAN storage
>> o) Logical storage unit with filesystem
>> p) Container for VM files in virtualization
>> q) Point-in-time copy of data
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage virtualization benefit.
>> [!example] Group A
>> a) Storage pooling
>> b) Thin provisioning
>> c) Storage migration
>> d) Automated tiering
>
>> [!example] Group B
>> n) Eliminates isolated storage silos
>> o) Improves storage utilization efficiency
>> p) Non-disruptive data movement
>> q) Optimizes cost by moving data between tiers
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage protocol with use.
>> [!example] Group A
>> a) NFS
>> b) iSCSI
>> c) Fibre Channel
>> d) SMB
>
>> [!example] Group B
>> n) File sharing in Linux/Unix environments
>> o) Block access over standard TCP/IP
>> p) High-performance block access over dedicated network
>> q) File sharing in Windows environments
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match performance metric with IO focus.
>> [!example] Group A
>> a) IOPS
>> b) Throughput
>> c) Latency
>> d) Bandwidth
>
>> [!example] Group B
>> n) Input/output operations per second
>> o) Data transfer rate per unit time
>> p) Delay in data access
>> q) Maximum data transfer capacity
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage scenario with best architecture.
>> [!example] Group A
>> a) Virtual machine system disks
>> b) Shared file storage
>> c) High-performance database storage
>> d) Backup and archival
>
>> [!example] Group B
>> n) SAN or block storage
>> o) NAS with NFS/SMB
>> p) SAN with Fibre Channel
>> q) Object storage or tape
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage HA feature.
>> [!example] Group A
>> a) Multipathing
>> b) Replication
>> c) Failover
>> d) Load balancing
>
>> [!example] Group B
>> n) Redundant I/O paths to storage
>> o) Synchronous or async data copy to remote site
>> p) Automatic switch to standby component
>> q) Distributing I/O across multiple paths
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match storage challenge with solution.
>> [!example] Group A
>> a) Storage silos
>> b) Poor utilization
>> c) Complex management
>> d) Downtime during maintenance
>
>> [!example] Group B
>> n) Pool physical storage into shared datastores
>> o) Thin provisioning and overcommitment
>> p) Centralized management console
>> q) Live storage migration (vMotion)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
