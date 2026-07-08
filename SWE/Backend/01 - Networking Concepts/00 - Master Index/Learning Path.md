---
title: Recommended Learning Path
type: guide
tags: [learning-path, study-guide]
---

#  Recommended Learning Path

> [!tip] How to Use This Path
> This is a **6-week study plan** that takes you from zero to confident in advanced networking. Each week pairs reading with active recall (quizzes) and a hands-on lab suggestion. Adjust pace based on your prior exposure.

---

## Week 1 — Foundations & Models

**Goal:** Build a rock-solid vocabulary and understand *why* we layer.

### Reading
1. [[01 - Network Fundamentals/01.00 Chapter Overview|01.00 Network Fundamentals — Overview]]
2. [[01 - Network Fundamentals/01.01 What is a Computer Network|01.01 What is a Computer Network]]
3. [[01 - Network Fundamentals/01.06 Network Topologies|01.06 Topologies]] ← study the diagrams carefully
4. [[02 - Reference Models (OSI & TCP-IP)/02.00 Chapter Overview|02.00 Reference Models — Overview]]
5. [[02 - Reference Models (OSI & TCP-IP)/02.02 The OSI 7-Layer Model|02.02 OSI 7-Layer Model]]
6. [[02 - Reference Models (OSI & TCP-IP)/02.04 Encapsulation & PDUs|02.04 Encapsulation & PDUs]]

### Active Recall
- Without looking, list all 7 OSI layers and one protocol per layer.
- Explain to a rubber duck: "Why do we need encapsulation?"

### Hands-on Lab
- Install Wireshark. Capture 60 seconds of traffic on your Wi-Fi interface. Identify ARP, DNS, and TCP handshake packets in the capture.

---

## Week 2 — Physical, Data Link & IPv4 Addressing

**Goal:** Master L2 frame structure and IPv4 subnet math.

### Reading
1. [[03 - Physical & Data Link Layer/03.00 Chapter Overview|03 — Physical & Data Link Overview]]
2. [[03 - Physical & Data Link Layer/03.02 MAC Addressing|03.02 MAC Addressing]]
3. [[03 - Physical & Data Link Layer/03.03 Ethernet II Frame Structure|03.03 Ethernet II Frame Structure]]
4. [[03 - Physical & Data Link Layer/03.04 Hubs vs Switches|03.04 Hubs vs Switches]]
5. [[04 - IPv4 Network Layer/04.00 Chapter Overview|04 — IPv4 Overview]]
6. [[04 - IPv4 Network Layer/04.02 Classful Addressing|04.02 Classful Addressing]]
7. [[04 - IPv4 Network Layer/04.05 FLSM|04.05 FLSM]]
8. [[04 - IPv4 Network Layer/04.06 VLSM|04.06 VLSM]]
9. [[14 - Memory Aids & Mnemonics/14.01 IPv4 Subnetting Memory Tricks|14.01 Subnetting Mnemonics]]

### Active Recall
- Given `172.19.155.42/18`, calculate: network address, broadcast, usable range, number of hosts.
- Decode the first octet `0x4A` in binary — is it unicast or multicast at L2?

### Hands-on Lab
- In Cisco Packet Tracer, design a network with three subnets (60, 30, 14 hosts) from `192.168.50.0/24` using VLSM. Document each allocation.

---

## Week 3 — IP Packets, Fragmentation & ARP

**Goal:** Understand what's actually inside an IP packet and how L3 talks to L2.

### Reading
1. [[05 - IP Datagram & Fragmentation/05.00 Chapter Overview|05 — Fragmentation Overview]]
2. [[05 - IP Datagram & Fragmentation/05.01 IP Header Fields|05.01 IP Header Fields]]
3. [[05 - IP Datagram & Fragmentation/05.02 Fragmentation Mathematics|05.02 Fragmentation Math]]
4. [[05 - IP Datagram & Fragmentation/05.03 Practical Walkthroughs|05.03 Walkthroughs]]
5. [[06 - ARP & Address Resolution/06.00 Chapter Overview|06 — ARP Overview]]
6. [[06 - ARP & Address Resolution/06.02 ARP Operation Lifecycle|06.02 ARP Operation Lifecycle]]
7. [[06 - ARP & Address Resolution/06.03 ARP Packet Format|06.03 ARP Packet Format]]
8. [[06 - ARP & Address Resolution/06.04 Advanced ARP|06.04 Advanced ARP]]

### Active Recall
- Fragment a 3000-byte payload over a 1000-byte MTU. Build the fragment table (length, offset, MF).
- Trace an ARP request from origin to destination — which fields are zero? Why?

### Hands-on Lab
- On Linux, run `arp -a` before and after pinging a new host. Run `tcpdump -i any arp` in another terminal while pinging a fresh host to watch the request/reply exchange.

---

## Week 4 — Routing & Routing Protocols

**Goal:** Predict how a packet will be forwarded in any topology.

### Reading
1. [[07 - IP Routing/07.00 Chapter Overview|07 — IP Routing Overview]]
2. [[07 - IP Routing/07.02 Administrative Distance & Metrics|07.02 Administrative Distance]]
3. [[07 - IP Routing/07.03 Longest Prefix Match|07.03 Longest Prefix Match]]
4. [[07 - IP Routing/07.05 Router Operations & Packet Processing|07.05 Router Packet Processing]]
5. [[08 - Routing Protocols/08.00 Chapter Overview|08 — Routing Protocols Overview]]
6. [[08 - Routing Protocols/08.01 Distance-Vector - RIP|08.01 RIP]]
7. [[08 - Routing Protocols/08.04 Link-State - OSPF|08.04 OSPF]]
8. [[08 - Routing Protocols/08.07 Dijkstra Algorithm Walkthrough|08.07 Dijkstra Walkthrough]]
9. [[08 - Routing Protocols/08.08 Path-Vector - BGP|08.08 BGP]]

### Active Recall
- Take the [[Quizzes/Quiz 05 - IP Routing|Chapter 5 quiz]] and the [[Quizzes/Quiz 07 - Routing Protocols|Chapter 7 quiz]].
- Re-run the Dijkstra walkthrough from node F without looking.

### Hands-on Lab
- Build a 4-router topology in Packet Tracer. Configure RIPv2 between R1–R2–R3 and OSPF area 0 between R3–R4. Verify the routing tables converge correctly. Then break a link and watch convergence.

---

## Week 5 — Edge, Transport & Application

**Goal:** Understand how traffic crosses the perimeter and reaches applications.

### Reading
1. [[09 - NAT & Perimeter Security/09.00 Chapter Overview|09 — NAT Overview]]
2. [[09 - NAT & Perimeter Security/09.04 PAT NAT Overload|09.04 PAT]]
3. [[10 - Transport Layer/10.00 Chapter Overview|10 — Transport Overview]]
4. [[10 - Transport Layer/10.06 TCP|10.06 TCP]]
5. [[10 - Transport Layer/10.08 TCP Connection Lifecycle|10.08 TCP Connection Lifecycle]]
6. [[10 - Transport Layer/10.09 TCP Flow Control & Windowing|10.09 Flow Control]]
7. [[11 - Application Layer/11.00 Chapter Overview|11 — Application Overview]]
8. [[11 - Application Layer/11.01 DNS & Domain Resolution|11.01 DNS]]
9. [[11 - Application Layer/11.02 HTTP & HTTPS|11.02 HTTP/HTTPS]]
10. [[11 - Application Layer/11.03 SSL & TLS|11.03 TLS]]

### Active Recall
- Take the [[Quizzes/Quiz 06 - ARP & NAT|Chapter 6 quiz]] and [[Quizzes/Quiz 08 - Transport Layer|Chapter 8 quiz]].
- Draw a sequence diagram of a TCP connection opening, transferring data, and closing.

### Hands-on Lab
- Spin up an `nginx` container. Use `curl -v http://localhost` and capture the exchange with Wireshark. Identify the 3-way handshake, the HTTP request, and the FIN close.

---

## Week 6 — Tunnels, Operations & Memory Aids

**Goal:** Round out operational knowledge and lock in mnemonics for the exam.

### Reading
1. [[12 - Tunnels & Remote Access/12.00 Chapter Overview|12 — Tunnels Overview]]
2. [[12 - Tunnels & Remote Access/12.02 Ngrok|12.02 Ngrok]]
3. [[12 - Tunnels & Remote Access/12.03 Cloudflare Tunnels|12.03 Cloudflare Tunnels]]
4. [[13 - Cisco IOS CLI/13.00 Chapter Overview|13 — Cisco IOS Overview]]
5. [[13 - Cisco IOS CLI/13.02 Essential Configuration|13.02 Essential Configuration]]
6. [[13 - Cisco IOS CLI/13.04 RIP & OSPF Configuration|13.04 RIP & OSPF Configuration]]
7. [[14 - Memory Aids & Mnemonics/14.00 Chapter Overview|14 — Mnemonics Overview]] ← entire chapter

### Active Recall
- Re-take all four quizzes in one sitting. Aim for >90%.
- From memory, write the Cisco IOS commands to: change hostname, set an IP on Fa0/0, configure RIPv2 with no auto-summary, and verify the routing table.

### Hands-on Lab
- Expose a local web server with both `ngrok http 80` and `cloudflared tunnel --url http://localhost:80`. Compare latency, headers, and behavior on disconnect.

---

##  Capstone Project

Once you complete the 6 weeks, validate your knowledge with this capstone:

> Design a small enterprise network with 3 branches (each with 2 LANs + 1 WAN link), an edge router doing PAT, a DMZ with a web server reachable via static NAT, an OSPF backbone, and a default route learned via BGP to the ISP. Document the addressing plan, the routing configuration, and the NAT rules. Implement it in Packet Tracer or GNS3.

This capstone touches every chapter except Chapter 1 and Chapter 11's upper-layer protocols — a true integration test.

---

##  Daily Habit

Regardless of where you are in the path, do this **every day** for 5 minutes:

1. Open a random chapter overview.
2. Read one topic note.
3. Try to explain it out loud without looking.
4. If you stumble, re-read and try again tomorrow.

Consistency beats intensity in networking — the field rewards repeated exposure.
