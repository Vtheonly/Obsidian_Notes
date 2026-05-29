---
sources:
  - "[[Chapter 6 - Virtual and Networked Storage/6.1 Storage Foundations and Access Models.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.2 Networked Storage Architectures - DAS NAS SAN.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.3 Storage Virtualization, Datastores, and High Availability.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.4 Block vs File Access and SAN vs NAS Architectures.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.5 RAID, Datastores, and Advanced Storage Features.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.6 Solving Storage Silos with Virtualization and Pooling.md]]"
---

> [!question] DAS stands for Directly Attached Storage.
>> [!success]- Answer
>> True

> [!question] NAS provides file-level data access over a network.
>> [!success]- Answer
>> True

> [!question] SAN provides block-level data access over a dedicated network.
>> [!success]- Answer
>> True

> [!question] RAID 0 provides redundancy through data mirroring.
>> [!success]- Answer
>> False

> [!question] RAID 5 uses striping with distributed parity.
>> [!success]- Answer
>> True

> [!question] DAS provides storage:
> a) Over a network
> b) Directly attached to a computer system
> c) Via fiber channel only
> d) As object storage
>> [!success]- Answer
>> b) Directly attached to a computer system

> [!question] NAS provides access at which level?
> a) Block level
> b) File level
> c) Object level
> d) Sector level
>> [!success]- Answer
>> b) File level

> [!question] SAN uses which protocol typically?
> a) HTTP
> b) Fibre Channel or iSCSI
> c) FTP
> d) SMTP
>> [!success]- Answer
>> b) Fibre Channel or iSCSI

> [!question] RAID 0 provides:
> a) Redundancy through mirroring
> b) Striping without redundancy
> c) Parity protection
> d) Hot spares
>> [!success]- Answer
>> b) Striping without redundancy

> [!question] RAID 5 uses:
> a) Striping with distributed parity
> b) Full mirroring of all data
> c) No striping
> d) Double parity
>> [!success]- Answer
>> a) Striping with distributed parity

> [!question] Match the storage type with its access method.
>> [!example] Group A
>> a) DAS
>> b) NAS
>> c) SAN
>> d) Object storage
>
>> [!example] Group B
>> n) Directly attached via SATA/SAS
>> o) File-level access over network (NFS/SMB)
>> p) Block-level access over Fibre Channel/iSCSI
>> q) HTTP-based access with REST APIs
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the RAID level with its description.
>> [!example] Group A
>> a) RAID 0
>> b) RAID 1
>> c) RAID 5
>> d) RAID 10
>
>> [!example] Group B
>> n) Striping without redundancy
>> o) Mirroring without striping
>> p) Striping with distributed parity
>> q) Striping with mirroring (combination)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the storage virtualization concept with its definition.
>> [!example] Group A
>> a) Storage pool
>> b) Datastore
>> c) Thin provisioning
>> d) Thick provisioning
>
>> [!example] Group B
>> n) Aggregated logical unit from multiple physical devices
>> o) Logical container for VM files in hypervisor
>> p) Allocates storage on-demand as data is written
>> q) Pre-allocates full storage capacity upfront
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the storage protocol with its transport.
>> [!example] Group A
>> a) Fibre Channel
>> b) iSCSI
>> c) NFS
>> d) SMB
>
>> [!example] Group B
>> n) Dedicated fiber optic network
>> o) SCSI commands over TCP/IP
>> p) Network File System for Unix/Linux
>> q) Server Message Block for Windows
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the high availability feature with its purpose.
>> [!example] Group A
>> a) Multipathing
>> b) Replication
>> c) Snapshot
>> d) Clustering
>
>> [!example] Group B
>> n) Multiple I/O paths for redundancy
>> o) Copying data to secondary storage
>> p) Point-in-time copy for backup
>> q) Grouping servers for failover
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
