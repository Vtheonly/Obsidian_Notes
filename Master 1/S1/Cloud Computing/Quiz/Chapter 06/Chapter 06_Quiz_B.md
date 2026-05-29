---
sources:
  - "[[Chapter 6 - Virtual and Networked Storage/6.1 Storage Foundations and Access Models.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.2 Networked Storage Architectures - DAS NAS SAN.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.3 Storage Virtualization, Datastores, and High Availability.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.4 Block vs File Access and SAN vs NAS Architectures.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.5 RAID, Datastores, and Advanced Storage Features.md]]"
  - "[[Chapter 6 - Virtual and Networked Storage/6.6 Solving Storage Silos with Virtualization and Pooling.md]]"
---

> [!question] Storage virtualization pools physical storage from multiple devices.
>> [!success]- Answer
>> True

> [!question] A datastore is a logical container for virtual machine files.
>> [!success]- Answer
>> True

> [!question] Block access is typically slower than file access for database workloads.
>> [!success]- Answer
>> False

> [!question] High availability in storage implies no single point of failure.
>> [!success]- Answer
>> True

> [!question] iSCSI is a protocol used to transport SCSI commands over IP networks.
>> [!success]- Answer
>> True

> [!question] Storage virtualization pools:
> a) Only RAM
> b) Physical storage from multiple devices into a single logical unit
> c) Network bandwidth
> d) CPU cores
>> [!success]- Answer
>> b) Physical storage from multiple devices into a single logical unit

> [!question] A datastore in virtualization is:
> a) A database management system
> b) A logical container for VM files
> c) A network protocol
> d) A physical hard drive
>> [!success]- Answer
>> b) A logical container for VM files

> [!question] iSCSI transports SCSI commands over:
> a) Serial cables
> b) IP networks
> c) USB
> d) HDMI
>> [!success]- Answer
>> b) IP networks

> [!question] High availability storage eliminates:
> a) All data
> b) Single points of failure
> c) Network redundancy
> d) Power usage
>> [!success]- Answer
>> b) Single points of failure

> [!question] Block storage is most suitable for:
> a) Unstructured data
> b) High-performance databases and VMs
> c) Email attachments
> d) Log files
>> [!success]- Answer
>> b) High-performance databases and VMs

> [!question] Match the storage optimization with its benefit.
>> [!example] Group A
>> a) Deduplication
>> b) Compression
>> c) Tiering
>> d) Caching
>
>> [!example] Group B
>> n) Eliminating duplicate data blocks
>> o) Reducing data size through algorithms
>> p) Moving data between performance tiers
>> q) Storing frequently accessed data in faster media
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the SAN component with its function.
>> [!example] Group A
>> a) HBA
>> b) Fibre Channel switch
>> c) Storage array
>> d) LUN
>
>> [!example] Group B
>> n) Host Bus Adapter to connect server to SAN
>> o) Network switch dedicated to storage traffic
>> p) Disk enclosure with controllers and disks
>> q) Logical Unit Number representing storage volume
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the storage metric with its meaning.
>> [!example] Group A
>> a) IOPS
>> b) Throughput
>> c) Latency
>> d) Capacity
>
>> [!example] Group B
>> n) Input/Output operations per second
>> o) Data transfer rate (MB/s or GB/s)
>> p) Time delay in data access
>> q) Total storage space available
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the DAS limitation vs network storage benefit.
>> [!example] Group A
>> a) DAS scalability
>> b) NAS file sharing
>> c) SAN performance
>> d) Storage pooling benefit
>
>> [!example] Group B
>> n) Limited to local machine expansion
>> o) Multiple clients can access same files
>> p) High-speed block access for databases
>> q) Flexible capacity allocation across systems
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)

> [!question] Match the data protection technique with its description.
>> [!example] Group A
>> a) Backup
>> b) Replication
>> c) Erasure coding
>> d) Snapshots
>
>> [!example] Group B
>> n) Copying data to separate media for recovery
>> o) Continuous copying to remote site
>> p) Data fragmentation with parity for fault tolerance
>> q) Instant point-in-time copy for quick recovery
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
>> d) -> q)
