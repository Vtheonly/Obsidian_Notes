---
sources:
  - "[[1. Binary Data and Bits]]"
  - "[[2. Storage Types Disk Drives and Solid State Drives]]"
  - "[[3. Data Volatility and Persistence]]"
  - "[[4. Random Access Memory Capabilities]]"
  - "[[5. Central Processing Unit Execution Cycles]]"
  - "[[6. CPU Cache Hierarchy (L1, L2, L3)]]"
  - "[[7. Motherboard and Data Pathways]]"
---

> [!question] PCIe 4.0 provides approximately 2 GB/s of bandwidth per lane per direction.
>> [!success]- Answer
>> True

> [!question] A single byte consists of 8 bits and can represent up to 512 distinct values.
>> [!success]- Answer
>> False

> [!question] Direct Memory Access (DMA) requires the CPU to manually copy each byte between peripherals and RAM.
>> [!success]- Answer
>> False

> [!question] The x86 processor architecture stores multi-byte values in memory using little-endian byte ordering.
>> [!success]- Answer
>> True

> [!question] A 32-bit processor architecture can directly address up to 16 exabytes of memory.
>> [!success]- Answer
>> False

> [!question] Modern superscalar processors can achieve an Instructions Per Cycle (IPC) value greater than 1.
>> [!success]- Answer
>> True

> [!question] Dynamic Random Access Memory (DRAM) cells must be periodically refreshed, typically every 64 milliseconds.
>> [!success]- Answer
>> True

> [!question] SLC (Single-Level Cell) NAND flash stores one bit per cell and offers higher endurance than QLC flash.
>> [!success]- Answer
>> True

> [!question] Cache lines on modern processors are typically 64 bytes in size.
>> [!success]- Answer
>> True

> [!question] In an exclusive cache hierarchy, the L3 cache always contains an exact duplicate superset of all data in L1 and L2.
>> [!success]- Answer
>> False

> [!question] A 10 Gbps network link can transfer data at a rate of 10 Gigabytes (GB) per second.
>> [!success]- Answer
>> False

> [!question] TCP/IP network protocols utilize big-endian byte order, also known as network byte order.
>> [!success]- Answer
>> True

> [!question] A typical 7,200 RPM hard disk drive delivers between 50,000 and 100,000 random read IOPS.
>> [!success]- Answer
>> False

> [!question] Level 1 (L1) cache typically has an access latency of roughly 1 to 4 CPU clock cycles.
>> [!success]- Answer
>> True

> [!question] Write-ahead logging (WAL) updates in-memory data structures before writing transaction logs to persistent disk.
>> [!success]- Answer
>> False

> [!question] ECC memory adds 8 extra bits for every 64 bits of data to detect and correct single-bit errors.
>> [!success]- Answer
>> True

> [!question] NVLink 4.0 provides up to 300 GB/s bandwidth between CPU and GPU, exceeding standard PCIe 5.0 x16 bandwidth.
>> [!success]- Answer
>> True

> [!question] DRAM uses static flip-flop circuits that never lose electrical charge over time.
>> [!success]- Answer
>> False

> [!question] Modern server processors integrate the memory controller and primary PCIe lanes directly onto the CPU die.
>> [!success]- Answer
>> True

> [!question] A dual-channel DDR4 configuration running at 3,200 MHz can achieve a theoretical maximum bandwidth of about 51.2 GB/s.
>> [!success]- Answer
>> True

> [!question] A branch misprediction in modern CPU pipelines typically costs between 10 and 20 clock cycles.
>> [!success]- Answer
>> True

> [!question] QLC NAND flash stores four bits per cell and offers higher endurance than SLC NAND flash.
>> [!success]- Answer
>> False

> [!question] False sharing occurs when multiple threads modify distinct variables located on the exact same cache line.
>> [!success]- Answer
>> True

> [!question] Battery-backed RAM (BBRAM) allows systems to retain data in volatile memory during power outages to flush it to disk.
>> [!success]- Answer
>> True

> [!question] In hexadecimal notation, each hex digit directly represents a sequence of 8 binary bits.
>> [!success]- Answer
>> False

> [!question] Remote Direct Memory Access (RDMA) enables direct memory transfer between two machines without CPU involvement.
>> [!success]- Answer
>> True

> [!question] Hard disk drives achieve approximately the same low access latency for random reads as they do for sequential reads.
>> [!success]- Answer
>> False

> [!question] L3 cache is typically shared across all processor cores rather than dedicated to an individual core.
>> [!success]- Answer
>> True

> [!question] DDR5 memory can reduce random access latency down to roughly 30 to 50 nanoseconds.
>> [!success]- Answer
>> True

> [!question] Bit manipulation instructions require software emulation and are significantly slower than arithmetic operations.
>> [!success]- Answer
>> False

> [!question] Wear leveling algorithms in SSDs distribute write operations evenly across cells to prevent premature degradation.
>> [!success]- Answer
>> True

> [!question] The execute stage of the CPU cycle interprets the instruction to determine what operands are needed.
>> [!success]- Answer
>> False

> [!question] Non-volatile RAM (NVRAM) technologies like Intel Optane offer byte-addressable access combined with persistence.
>> [!success]- Answer
>> True

> [!question] Sequential array iteration generally exhibits worse cache performance than linked list traversal.
>> [!success]- Answer
>> False

> [!question] A single DRAM cell consists of one transistor and one capacitor.
>> [!success]- Answer
>> True

> [!question] What is the bandwidth per lane per direction in the PCIe 5.0 standard?
> a) 1 GB/s
> b) 2 GB/s
> c) 4 GB/s
> d) 8 GB/s
>> [!success]- Answer
>> c) 4 GB/s

> [!question] How many distinct values can be represented by a single byte?
> a) 8
> b) 64
> c) 128
> d) 256
>> [!success]- Answer
>> d) 256

> [!question] What is the theoretical maximum addressable memory capacity of a 32-bit processor?
> a) 2 GB
> b) 4 GB
> c) 16 GB
> d) 64 GB
>> [!success]- Answer
>> b) 4 GB

> [!question] Which byte ordering scheme places the most significant byte at the lowest memory address?
> a) Little-endian
> b) Big-endian
> c) Mid-endian
> d) Reverse-endian
>> [!success]- Answer
>> b) Big-endian

> [!question] What is the maximum throughput of a 10 Gbps network link in Gigabytes per second (GB/s)?
> a) 10 GB/s
> b) 5 GB/s
> c) 1.25 GB/s
> d) 0.8 GB/s
>> [!success]- Answer
>> c) 1.25 GB/s

> [!question] What are the three fundamental stages of the basic CPU cycle?
> a) Fetch, Decode, Execute
> b) Read, Write, Erase
> c) Load, Link, Run
> d) Input, Process, Output
>> [!success]- Answer
>> a) Fetch, Decode, Execute

> [!question] What is the duration of a single clock cycle on a processor running at 3 GHz?
> a) 3.0 nanoseconds
> b) 1.0 nanosecond
> c) 0.33 nanoseconds
> d) 0.033 nanoseconds
>> [!success]- Answer
>> c) 0.33 nanoseconds

> [!question] What is the typical latency penalty in CPU clock cycles when a branch misprediction occurs?
> a) 1-2 cycles
> b) 4-8 cycles
> c) 10-20 cycles
> d) 50-100 cycles
>> [!success]- Answer
>> c) 10-20 cycles

> [!question] What is the average seek time of a typical 7,200 RPM hard disk drive?
> a) 0.1 milliseconds
> b) 1.0 millisecond
> c) 8-9 milliseconds
> d) 50-70 milliseconds
>> [!success]- Answer
>> c) 8-9 milliseconds

> [!question] How many bits of data are stored in a single Triple-Level Cell (TLC) NAND flash cell?
> a) 1 bit
> b) 2 bits
> c) 3 bits
> d) 4 bits
>> [!success]- Answer
>> c) 3 bits

> [!question] How many random read IOPS does a standard 7,200 RPM hard disk drive typically achieve?
> a) 75-100 IOPS
> b) 500-1,000 IOPS
> c) 10,000-20,000 IOPS
> d) 50,000-100,000 IOPS
>> [!success]- Answer
>> a) 75-100 IOPS

> [!question] What is the typical random read access latency for a solid state drive (SSD)?
> a) 1 nanosecond
> b) 50-100 nanoseconds
> c) 0.1 milliseconds (100 microseconds)
> d) 10 milliseconds
>> [!success]- Answer
>> c) 0.1 milliseconds (100 microseconds)

> [!question] What is the standard size of a cache line transferred between modern CPU caches and RAM?
> a) 16 bytes
> b) 32 bytes
> c) 64 bytes
> d) 128 bytes
>> [!success]- Answer
>> c) 64 bytes

> [!question] What is the typical access latency of Level 1 (L1) CPU cache?
> a) 1-4 cycles
> b) 10-20 cycles
> c) 50-100 cycles
> d) 100-200 cycles
>> [!success]- Answer
>> a) 1-4 cycles

> [!question] What is the typical capacity of L1 cache per core on contemporary processors?
> a) 4-8 KB
> b) 32-64 KB
> c) 256-512 KB
> d) 4-8 MB
>> [!success]- Answer
>> b) 32-64 KB

> [!question] Which level of CPU cache is typically shared across all processor cores?
> a) L1 Instruction Cache
> b) L1 Data Cache
> c) L2 Cache
> d) L3 Cache
>> [!success]- Answer
>> d) L3 Cache

> [!question] Which physical components comprise a single Dynamic RAM (DRAM) memory cell?
> a) Two transistors and two capacitors
> b) One transistor and one capacitor
> c) Four floating-gate transistors
> d) Six static logic gates
>> [!success]- Answer
>> b) One transistor and one capacitor

> [!question] How often must DRAM cells typically be refreshed to avoid data corruption?
> a) Every 64 microseconds
> b) Every 64 milliseconds
> c) Every 64 seconds
> d) Only upon reboot
>> [!success]- Answer
>> b) Every 64 milliseconds

> [!question] What is the typical random access latency range for DDR4 RAM?
> a) 1-4 nanoseconds
> b) 10-20 nanoseconds
> c) 50-70 nanoseconds
> d) 100-200 microseconds
>> [!success]- Answer
>> c) 50-70 nanoseconds

> [!question] In a standard ECC memory module, how many total bits are stored for every 64 bits of data?
> a) 66 bits
> b) 68 bits
> c) 72 bits
> d) 80 bits
>> [!success]- Answer
>> c) 72 bits

> [!question] How many PCIe lanes are typically dedicated to a discrete high-performance graphics card (GPU)?
> a) 2 lanes
> b) 4 lanes
> c) 8 lanes
> d) 16 lanes
>> [!success]- Answer
>> d) 16 lanes

> [!question] Which technology enables direct memory transfers between two machines across a network without CPU overhead?
> a) DMA
> b) RDMA
> c) NVLink
> d) UPI
>> [!success]- Answer
>> b) RDMA

> [!question] What is the modern chipset component that replaced the traditional southbridge for handling system I/O?
> a) Northbridge Hub
> b) Memory Controller Hub (MCH)
> c) Platform Controller Hub (PCH)
> d) Direct Memory Controller (DMC)
>> [!success]- Answer
>> c) Platform Controller Hub (PCH)

> [!question] What is the approximate interconnect bandwidth delivered by NVIDIA NVLink 4.0?
> a) 32 GB/s
> b) 64 GB/s
> c) 128 GB/s
> d) 300 GB/s
>> [!success]- Answer
>> d) 300 GB/s

> [!question] How many binary bits does a single hexadecimal digit represent?
> a) 2 bits
> b) 4 bits
> c) 8 bits
> d) 16 bits
>> [!success]- Answer
>> b) 4 bits

> [!question] What allows a superscalar CPU core to execute multiple independent instructions during the same clock cycle?
> a) Multiple parallel execution units
> b) Slower bus frequencies
> c) Exclusive L1 cache structure
> d) Flash translation layer
>> [!success]- Answer
>> a) Multiple parallel execution units

> [!question] What is the approximate write cycle endurance of Single-Level Cell (SLC) NAND flash memory?
> a) 1,000 cycles
> b) 3,000 to 10,000 cycles
> c) 100,000 cycles
> d) Unlimited cycles
>> [!success]- Answer
>> c) 100,000 cycles

> [!question] What causes the severe multi-threaded performance degradation known as false sharing?
> a) Exceeding the maximum capacity of the L3 cache
> b) Cores constantly invalidating the same shared cache line for independent variables
> c) Incorrect branch predictions in parallel loop structures
> d) DRAM capacitors leaking charge faster than the 64ms refresh interval
>> [!success]- Answer
>> b) Cores constantly invalidating the same shared cache line for independent variables

> [!question] Why do database engines implement Write-Ahead Logging (WAL)?
> a) To improve CPU instruction cache hit rates
> b) To guarantee data durability before updating volatile in-memory state
> c) To convert big-endian data into little-endian format
> d) To avoid wear leveling on solid state drives
>> [!success]- Answer
>> b) To guarantee data durability before updating volatile in-memory state

> [!question] What is the theoretical peak bandwidth of a dual-channel DDR4 memory system clocked at 3,200 MHz?
> a) 25.6 GB/s
> b) 51.2 GB/s
> c) 102.4 GB/s
> d) 128.0 GB/s
>> [!success]- Answer
>> b) 51.2 GB/s

> [!question] What term describes a cache design where higher-level caches contain a complete copy of all data in lower caches?
> a) Exclusive cache
> b) Inclusive cache
> c) Paged cache
> d) Over-provisioned cache
>> [!success]- Answer
>> b) Inclusive cache

> [!question] Which component physically positions the read/write heads over the tracks of a hard disk platter?
> a) Actuator arm
> b) Platform controller hub
> c) Floating-gate transistor
> d) DMA controller
>> [!success]- Answer
>> a) Actuator arm

> [!question] What principle states that memory locations close to recently accessed data are likely to be accessed soon?
> a) Temporal locality
> b) Spatial locality
> c) Superscalar locality
> d) Endian locality
>> [!success]- Answer
>> b) Spatial locality

> [!question] How many PCIe lanes does a standard NVMe SSD typically use?
> a) 1 lane
> b) 2 lanes
> c) 4 lanes
> d) 16 lanes
>> [!success]- Answer
>> c) 4 lanes

> [!question] What is the maximum theoretical memory address space of a 64-bit processor architecture?
> a) 4 Gigabytes
> b) 1 Terabyte
> c) 512 Terabytes
> d) 16 Exabytes
>> [!success]- Answer
>> d) 16 Exabytes

> [!question] Match the PCIe generation with its per-lane unidirectional bandwidth.
>> [!example] Group A
>> a) PCIe 3.0
>> b) PCIe 4.0
>> c) PCIe 5.0
>
>> [!example] Group B
>> n) ~1 GB/s per lane
>> o) ~2 GB/s per lane
>> p) ~4 GB/s per lane
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the NAND flash type with its stored bits per cell.
>> [!example] Group A
>> a) SLC (Single-Level Cell)
>> b) MLC (Multi-Level Cell)
>> c) TLC (Triple-Level Cell)
>
>> [!example] Group B
>> n) 3 bits per cell
>> o) 1 bit per cell
>> p) 2 bits per cell
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the flash memory type with its approximate write cycle endurance.
>> [!example] Group A
>> a) SLC NAND
>> b) MLC NAND
>> c) TLC NAND
>
>> [!example] Group B
>> n) ~1,000 - 3,000 write cycles
>> o) ~100,000 write cycles
>> p) ~3,000 - 10,000 write cycles
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the CPU cache level with its typical access latency.
>> [!example] Group A
>> a) L1 Cache
>> b) L2 Cache
>> c) L3 Cache
>
>> [!example] Group B
>> n) 4-10 CPU cycles
>> o) 1-4 CPU cycles
>> p) 10-50 CPU cycles
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the CPU cache level with its typical capacity size.
>> [!example] Group A
>> a) L1 Cache per core
>> b) L2 Cache per core
>> c) L3 Cache shared
>
>> [!example] Group B
>> n) 4-64 MB
>> o) 32-64 KB
>> p) 256 KB - 1 MB
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the storage medium with its typical random read access latency.
>> [!example] Group A
>> a) System RAM (DRAM)
>> b) Solid State Drive (SSD)
>> c) Hard Disk Drive (HDD)
>
>> [!example] Group B
>> n) ~10 milliseconds
>> o) ~50-100 nanoseconds
>> p) ~100 microseconds (0.1 ms)
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the storage technology with its typical random read IOPS.
>> [!example] Group A
>> a) 7,200 RPM HDD
>> b) 15,000 RPM HDD
>> c) Enterprise NVMe SSD
>
>> [!example] Group B
>> n) > 500,000 IOPS
>> o) 75-100 IOPS
>> p) 180-210 IOPS
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the CPU instruction execution stage with its primary task.
>> [!example] Group A
>> a) Fetch
>> b) Decode
>> c) Execute
>
>> [!example] Group B
>> n) Interprets instruction opcode and identifies required operands
>> o) Retrieves the next instruction from instruction cache or memory
>> p) Performs the computation or logical operation on hardware units
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the memory type with its defining characteristic.
>> [!example] Group A
>> a) DRAM
>> b) SRAM
>> c) NVRAM
>
>> [!example] Group B
>> n) High-speed static circuit used in caches without refresh cycles
>> o) Single-transistor dynamic cell requiring periodic refresh
>> p) Byte-addressable memory that retains state without continuous power
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the bitwise operator with its logical behavior.
>> [!example] Group A
>> a) Bitwise AND
>> b) Bitwise OR
>> c) Bitwise XOR
>
>> [!example] Group B
>> n) Produces 1 if either bit or both bits are 1
>> o) Produces 1 only when the two input bits differ
>> p) Produces 1 only if both input bits are 1
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the endianness terminology with its byte-ordering rule.
>> [!example] Group A
>> a) Little-endian
>> b) Big-endian
>> c) Network byte order
>
>> [!example] Group B
>> n) Standardized big-endian representation for network protocols
>> o) Most significant byte stored at the lowest memory address
>> p) Least significant byte stored at the lowest memory address
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the number system base with its radix value.
>> [!example] Group A
>> a) Binary
>> b) Hexadecimal
>> c) Decimal
>
>> [!example] Group B
>> n) Base 16
>> o) Base 2
>> p) Base 10
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the system interconnect with its primary communication role.
>> [!example] Group A
>> a) Memory bus
>> b) PCIe bus
>> c) Inter-socket interconnect (UPI / Infinity Fabric)
>
>> [!example] Group B
>> n) Links peripheral expansion devices and NVMe drives to the system
>> o) Connects CPU dies and processor sockets with dedicated links
>> p) Connects integrated memory controllers directly to system RAM
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the motherboard chipset architecture term with its description.
>> [!example] Group A
>> a) Northbridge
>> b) Southbridge
>> c) Platform Controller Hub (PCH)
>
>> [!example] Group B
>> n) Modern consolidated chipset handling remaining system I/O
>> o) Legacy controller handling slower peripherals like USB and SATA
>> p) Legacy hub for high-speed CPU, RAM, and primary graphics bus
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the cache locality concept with its definition.
>> [!example] Group A
>> a) Temporal locality
>> b) Spatial locality
>> c) False sharing
>
>> [!example] Group B
>> n) Accessing memory physically adjacent to recently read addresses
>> o) Performance penalty from invalidating shared lines with distinct vars
>> p) Re-accessing data that was referenced in the recent past
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the hardware component with its operational role.
>> [!example] Group A
>> a) DMA controller
>> b) DRAM capacitor
>> c) Branch predictor
>
>> [!example] Group B
>> n) Guesses the outcome of conditional instructions to keep pipeline fed
>> o) Offloads block data transfers between peripherals and memory
>> p) Stores an electrical charge representing a single binary bit
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the processor word size with its maximum addressable memory.
>> [!example] Group A
>> a) 8-bit byte value
>> b) 32-bit architecture
>> c) 64-bit architecture
>
>> [!example] Group B
>> n) Up to 16 exabytes
>> o) 256 distinct addressable states
>> p) Up to 4 gigabytes
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the DDR4-3200 memory configuration with its theoretical bandwidth.
>> [!example] Group A
>> a) Single-channel
>> b) Dual-channel
>> c) Quad-channel
>
>> [!example] Group B
>> n) 102.4 GB/s
>> o) 25.6 GB/s
>> p) 51.2 GB/s
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the storage persistence mechanism with its operational behavior.
>> [!example] Group A
>> a) Volatile RAM
>> b) Non-volatile Flash/Disk
>> c) Battery-Backed RAM
>
>> [!example] Group B
>> n) Retains data indefinitely after power removal
>> o) Uses auxiliary energy to flush volatile contents during power loss
>> p) Loses all stored state immediately upon loss of power
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the hard drive latency component with its definition.
>> [!example] Group A
>> a) Seek time
>> b) Rotational latency
>> c) Transfer time
>
>> [!example] Group B
>> n) Time for the target sector on the platter to rotate under the head
>> o) Time required to read or write the actual stream of data bits
>> p) Time for the actuator arm to physically move across disk tracks
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the cache organization concept with its design property.
>> [!example] Group A
>> a) Cache line
>> b) Inclusive cache
>> c) Exclusive cache
>
>> [!example] Group B
>> n) L3 cache stores strictly data not present in L1 or L2 caches
>> o) Fixed 64-byte block used for cache-to-RAM transfers
>> p) L3 cache maintains a duplicate superset of all lower cache contents
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the data throughput specification with its byte-equivalent rate.
>> [!example] Group A
>> a) 10 Gbps network link
>> b) 64-bit memory word per clock
>> c) 1 Byte transfer
>
>> [!example] Group B
>> n) Exactly 8 bits
>> o) 8 bytes transferred simultaneously
>> p) 1.25 Gigabytes per second
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the hardware peripheral with its typical PCIe lane allocation.
>> [!example] Group A
>> a) NVMe SSD
>> b) Enterprise Network Card
>> c) High-end Discrete GPU
>
>> [!example] Group B
>> n) 8 to 16 PCIe lanes
>> o) 4 PCIe lanes
>> p) 16 PCIe lanes
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the CPU architectural concept with its performance metric.
>> [!example] Group A
>> a) Clock speed
>> b) Instructions Per Cycle (IPC)
>> c) Pipelining
>
>> [!example] Group B
>> n) Division of instruction execution into overlapping assembly stages
>> o) Average number of instructions executed per individual clock cycle
>> p) Frequency measured in GHz indicating total cycle iterations per second
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the GPU/accelerator interconnect with its bandwidth rating.
>> [!example] Group A
>> a) PCIe 4.0 x16
>> b) PCIe 5.0 x16
>> c) NVIDIA NVLink 4.0
>
>> [!example] Group B
>> n) Up to 300 GB/s
>> o) ~32 GB/s bidirectional
>> p) ~64 GB/s bidirectional
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the SSD reliability feature with its function.
>> [!example] Group A
>> a) Wear leveling
>> b) Over-provisioning
>> c) Floating-gate transistor
>
>> [!example] Group B
>> n) Extra physical cell capacity reserved to replace worn blocks
>> o) Traps electrical charge to non-volatilely store binary bits
>> p) Distributes write operations evenly across all memory blocks
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the fault-tolerance mechanism with its primary target.
>> [!example] Group A
>> a) ECC Memory
>> b) Write-Ahead Logging
>> c) Multi-node Replication
>
>> [!example] Group B
>> n) Crash recovery ensuring in-memory updates are durable on disk
>> o) Protects against simultaneous power/hardware loss across machines
>> p) Detects and corrects single-bit DRAM corruption errors
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the hardware timing metric with its typical duration.
>> [!example] Group A
>> a) 3 GHz CPU cycle
>> b) DDR5 RAM latency
>> c) DDR4 RAM latency
>
>> [!example] Group B
>> n) 50-70 nanoseconds
>> o) 0.33 nanoseconds
>> p) 30-50 nanoseconds
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the memory access pattern with its cache behavior.
>> [!example] Group A
>> a) Contiguous array iteration
>> b) Linked list node traversal
>> c) Branchless calculation
>
>> [!example] Group B
>> n) Eliminates pipeline stalls caused by branch mispredictions
>> o) High cache hit rate due to strong spatial locality and prefetching
>> p) High cache miss rate due to scattered pointer-chasing patterns
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the CPU pipeline event with its definition.
>> [!example] Group A
>> a) Pipeline stall
>> b) Pipeline flush
>> c) Out-of-order dispatch
>
>> [!example] Group B
>> n) Issuing independent instructions to parallel execution units
>> o) Delay introduced when an instruction waits for an incomplete dependency
>> p) Discarding fetched instructions after an incorrect branch prediction
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the storage tier with its optimal system use case.
>> [!example] Group A
>> a) NVMe SSD tier
>> b) HDD tier
>> c) In-memory cache tier
>
>> [!example] Group B
>> n) Sub-millisecond session caching and real-time state lookup
>> o) Cold data archival and large bulk sequential backup files
>> p) High-throughput random read/write primary database storage
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the multi-bit NAND flash type with its cell capacity.
>> [!example] Group A
>> a) MLC
>> b) TLC
>> c) QLC
>
>> [!example] Group B
>> n) 4 bits per cell
>> o) 2 bits per cell
>> p) 3 bits per cell
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the cache metric with its expected hit/miss rate.
>> [!example] Group A
>> a) L1 Cache hit rate
>> b) L2 hit rate for L1 misses
>> c) Overall miss rate to RAM
>
>> [!example] Group B
>> n) 80-90%
>> o) Typically below 5% for localized workloads
>> p) 90-95% for well-optimized code
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the architectural feature with its primary performance benefit.
>> [!example] Group A
>> a) Hardware prefetcher
>> b) Superscalar execution
>> c) RDMA network protocol
>
>> [!example] Group B
>> n) Executes multiple independent instructions per clock cycle
>> o) Transfers remote memory directly without CPU context switches
>> p) Loads sequential cache lines into cache prior to CPU execution
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the historical/modern bus type with its connected components.
>> [!example] Group A
>> a) Memory bus
>> b) Legacy Front-Side Bus (FSB)
>> c) PCIe bus
>
>> [!example] Group B
>> n) Historical bus connecting CPU directly to external northbridge
>> o) Connects modern expansion peripherals (NVMe, NICs, GPUs)
>> p) Directly links the CPU integrated memory controller to DRAM channels
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)