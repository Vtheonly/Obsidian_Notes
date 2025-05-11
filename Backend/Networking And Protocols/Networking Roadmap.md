**Chapter 1: Introduction & Foundational Concepts**
- [ ] **1. Network Architectures**
    - [ ] 1a. Client-Server Architecture
    - [ ] 1b. Peer-to-Peer Architecture
- [ ] **2. Network Scope & Types**
    - [ ] 2a. LAN (Local Area Network)
    - [ ] 2b. MAN (Metropolitan Area Network)
    - [ ] 2c. WAN (Wide Area Network)
- [ ] **3. Network Topologies**
    - [ ] 3a. Bus, Ring, Star, Tree, Mesh, Hybrid
- [ ] **4. Basic Network Devices (Introduction)**
    - [ ] 4a. Modem
    - [ ] 4b. Router
    - [ ] 4c. Switch
    - [ ] 4d. Firewall
- [ ] **5. Physical Infrastructure & Protocols**
    - [ ] 5a. Physical Concepts (e.g., Submarine Optical Fibre Cables)
    - [ ] 5b. Introduction to Network Protocols
    - [ ] 5c. Basic Structure of the Network (How devices connect)

**Chapter 2: Network Models & Data Encapsulation**
- [ ] **6. Network Models**
    - [ ] 6a. The OSI Model (7 Layers, Functions)
    - [ ] 6b. The TCP/IP Model (4/5 Layers, Functions)
    - [ ] 6c. OSI vs. TCP/IP Model Comparison
- [ ] **7. Data Encapsulation**
    - [ ] 7a. How data is packaged through layers
    - [ ] 7b. Understanding Headers (Ethernet, IP, TCP/UDP)
    - [ ] 7c. Packet Structure Example (e.g., HTTP flow)

**Chapter 3: Layer 2 - Data Link Layer Concepts**
- [ ] **8. Ethernet & Switching Basics**
    - [ ] 8a. Ethernet Basics (Wired Networking)
    - [ ] 8b. MAC Addresses (48-bit structure, purpose)
    - [ ] 8c. Switches: Function and Operation (Flooding, Learning, Forwarding)
    - [ ] 8d. MAC Address Table (CAM Table)
- [ ] **9. Address Resolution**
    - [ ] 9a. ARP (Address Resolution Protocol): Resolving IP to MAC
- [ ] **10. VLANs (Virtual LANs)**
    - [ ] 10a. Concept and Purpose
    - [ ] 10b. 802.1Q Tagging
    - [ ] 10c. Access Ports vs. Trunk Ports
- [ ] **11. Layer 2 Loops & Broadcasts**
    - [ ] 11a. Broadcast Frames & Broadcast Domains
    - [ ] 11b. Broadcast Storms
    - [ ] 11c. Loop Prevention: Spanning Tree Protocol (STP)

**Chapter 4: Layer 3 - Network Layer (IP & Routing)**
- [ ] **12. IP Addressing**
    - [ ] 12a. IP (Internet Protocol) - Basic Function
    - [ ] 12b. IPv4 Fundamentals (32-bit, Binary vs. Dotted Decimal, Octets)
    - [ ] 12c. Subnet Mask (Netmask): Purpose, `/` notation (CIDR)
    - [ ] 12d. Network Address Calculation (Logical AND)
    - [ ] 12e. Determining if hosts are on the same network
    - [ ] 12f. IPv6 Addressing: Basics, Comparison to IPv4
    - [ ] 12g. IPv4 Address Classes (Historical Context) & Exhaustion
    - [ ] 12h. Special IP Ranges (Private RFC 1918, Link-Local, Loopback, CGNAT)
    - [ ] 12i. Public IP Addresses
- [ ] **13. Routing Fundamentals**
    - [ ] 13a. Routers: Function (Path Selection, Inter-network communication)
    - [ ] 13b. Routing Table: Structure and Purpose
    - [ ] 13c. Routing Concepts: Directly Connected, Default Route (0.0.0.0/0), Longest Prefix Match
    - [ ] 13d. Static Routing
    - [ ] 13e. Dynamic Routing Protocols: Introduction (e.g., OSPF, BGP)
- [ ] **14. IP Packet Forwarding**
    - [ ] 14a. IP Header: Source/Destination IP Addresses
    - [ ] 14b. MAC Address Rewrite (Router behavior at each hop)
- [ ] **15. ICMP (Internet Control Message Protocol)**
    - [ ] 15a. Purpose and common uses (Ping, Traceroute)

**Chapter 5: Layer 4 - Transport Layer (TCP & UDP)**
- [ ] **16. Transport Layer Basics**
    - [ ] 16a. Port Numbers
    - [ ] 16b. Multiplexing & Demultiplexing
    - [ ] 16c. Sockets (Endpoint concept)
    - [ ] 16d. Checksum (Error detection)
- [ ] **17. TCP (Transmission Control Protocol)**
    - [ ] 17a. Characteristics: Connection-Oriented, Reliable Delivery
    - [ ] 17b. TCP Header: Ports, Sequence/Ack Numbers, Flags
    - [ ] 17c. Connection Establishment: 3-Way Handshake (SYN, SYN-ACK, ACK)
    - [ ] 17d. Reliability Mechanisms: Sequence Numbers & Acknowledgement Numbers
    - [ ] 17e. Flow Control & Congestion Control: MSS, Windowing (cwnd), Slow Start, Congestion Avoidance (AIMD), ssthresh
    - [ ] 17f. Handling Packet Loss: Duplicate ACKs, Fast Retransmit, Timers
    - [ ] 17g. Optimizations: Selective Acknowledgement (SACK)
    - [ ] 17h. TCP Implementations (Tahoe, Reno, Cubic, BBR - awareness)
    - [ ] 17i. Impact of RTT / Latency
    - [ ] 17j. Connection Termination (FIN flag)
- [ ] **18. UDP (User Datagram Protocol)**
    - [ ] 18a. Characteristics: Connectionless, Unreliable, Lightweight
    - [ ] 18b. UDP Header Structure

**Chapter 6: Application Layer & Core Network Services**
- [ ] **19. DNS (Domain Name System)**
    - [ ] 19a. Purpose: Resolving Domain Names to IP Addresses
    - [ ] 19b. Resolution Process: Client -> Resolver -> Root -> TLD -> Authoritative
    - [ ] 19c. Common Record Types (A, AAAA, CNAME, MX, NS)
    - [ ] 19d. Configuration & Troubleshooting Tools (`nslookup`, `dig`)
- [ ] **20. DHCP (Dynamic Host Configuration Protocol)**
    - [ ] 20a. Purpose: Automatic IP Configuration
    - [ ] 20b. DORA Process: Discover, Offer, Request, Acknowledge
    - [ ] 20c. Configuration & Troubleshooting
- [ ] **21. HTTP (Hypertext Transfer Protocol)**
    - [ ] 21a. Fundamentals of Web Communication
    - [ ] 21b. HTTP Methods (GET, POST, PUT, DELETE, etc.)
    - [ ] 21c. HTTP Status Codes (2xx, 3xx, 4xx, 5xx)
    - [ ] 21d. HTTP Versions: 1.0, 1.1 (Persistent Connections, HoL Blocking), HTTP/2 (Multiplexing), QUIC/HTTP/3 (UDP-based)
    - [ ] 21e. HTTPS: Secure HTTP using TLS/SSL
    - [ ] 21f. Cookies: State Management
- [ ] **22. Email Protocols**
    - [ ] 22a. How Email Works (SMTP, POP3, IMAP)
- [ ] **23. File Transfer Protocols**
    - [ ] 23a. FTP, SFTP, TFTP: Use Cases

**Chapter 7: Advanced Routing & Network Technologies**
- [ ] **24. NAT (Network Address Translation)**
    - [ ] 24a. Purpose (IP Conservation) & How it Works
    - [ ] 24b. Types: Many-to-One/PAT (Stateful), One-to-One (Stateless)
- [ ] **25. Middleboxes**
    - [ ] 25a. Concept and Examples (Firewalls, NAT, Load Balancers)
- [ ] **26. BGP (Border Gateway Protocol)**
    - [ ] 26a. Role as the Internet Routing Protocol
    - [ ] 26b. Autonomous System (AS) & ASN
    - [ ] 26c. BGP Attributes & Path Selection (AS_PATH, Local Pref, MED, Communities)
    - [ ] 26d. Traffic Engineering Concepts (AS_PATH Prepending, Local Preference)
- [ ] **27. Wireless Networking**
    - [ ] 27a. Wi-Fi Basics (802.11 standards overview)

**Chapter 8: Network Security**
- [ ] **28. Firewalls**
    - [ ] 28a. Purpose and Basic Configuration
    - [ ] 28b. Types: Stateless, Stateful, Next-Generation (NGFW)
- [ ] **29. VPN (Virtual Private Network)**
    - [ ] 29a. Concept: Creating Secure Overlay Networks
    - [ ] 29b. Types: Site-to-Site, Remote Access
    - [ ] 29c. Common Protocols: IPsec, SSL/TLS (OpenVPN)
    - [ ] 29d. IPsec Details: IKE (v1/v2, UDP 500), ESP (Protocol 50), NAT Traversal (NAT-T, UDP 4500)
- [ ] **30. Intrusion Detection & Prevention**
    - [ ] 30a. IDS (Intrusion Detection System) vs. IPS (Intrusion Prevention System)
- [ ] **31. Encryption & Secure Communication**
    - [ ] 31a. Encryption Fundamentals (Symmetric vs. Asymmetric)
    - [ ] 31b. TLS/SSL: Securing Application Data (Handshake latency 1.2 vs 1.3)
    - [ ] 31c. PKI (Public Key Infrastructure): Certificates, CAs, Trust
- [ ] **32. Access Control**
    - [ ] 32a. Models: MAC (Mandatory), DAC (Discretionary), RBAC (Role-Based)
- [ ] **33. Security Practices**
    - [ ] 33a. Network Hardening Best Practices
    - [ ] 33b. DoS/DDoS Attack Awareness & Mitigation Concepts

**Chapter 9: Practical Skills & Tools**
- [ ] **34. Command-Line Network Tools**
    - [ ] 34a. Connectivity Testing: `ping`, `traceroute`/`tracert`
    - [ ] 34b. Interface Configuration: `ipconfig`/`ifconfig`
    - [ ] 34c. Connection Information: `netstat`
    - [ ] 34d. DNS Queries: `nslookup`, `dig` (including `+trace`)
- [ ] **35. Network Traffic Analysis**
    - [ ] 35a. Packet Capture Tools: Wireshark, tcpdump
    - [ ] 35b. Basic Packet Analysis Techniques
- [ ] **36. Network Simulation**
    - [ ] 36a. Using Simulators: Cisco Packet Tracer, GNS3, EVE-NG
    - [ ] 36b. Benefits: Design, Testing, Practice without hardware