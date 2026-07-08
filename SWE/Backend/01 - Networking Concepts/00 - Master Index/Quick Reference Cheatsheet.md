---
title: Quick Reference Cheatsheet
type: reference
tags: [cheatsheet, reference]
---

#  Quick Reference Cheatsheet

> [!summary] One-Page Condensed Reference
> Use this page as a fast lookup during labs, troubleshooting, or exam practice. Each row points to the full note for deeper context.

---

##  OSI vs TCP/IP Layers

| OSI # | OSI Layer | TCP/IP Layer | PDU | Example Protocols |
| :-: | :--- | :--- | :--- | :--- |
| 7 | Application | Application | Data | HTTP, DNS, SMTP, FTP |
| 6 | Presentation | Application | Data | JPEG, MP3, TLS |
| 5 | Session | Application | Data | RPC, NetBIOS |
| 4 | Transport | Transport | Segment (TCP) / Datagram (UDP) | TCP, UDP |
| 3 | Network | Internet | Packet / Datagram | IP, ICMP, ARP |
| 2 | Data Link | Network Access | Frame | Ethernet, Wi-Fi |
| 1 | Physical | Network Access | Bit | Cables, fiber, radio |

→ See [[02 - Reference Models (OSI & TCP-IP)/02.05 OSI vs TCP-IP Comparison|OSI vs TCP/IP Comparison]].

---

##  IPv4 Classful Addressing

| Class | 1st Octet Range | Default Mask | Default Prefix | Use |
| :-: | :--- | :--- | :-: | :--- |
| A | 1–126 | 255.0.0.0 | /8 | Very large networks |
| B | 128–191 | 255.255.0.0 | /16 | Medium networks |
| C | 192–223 | 255.255.255.0 | /24 | Small networks |
| D | 224–239 | N/A | N/A | Multicast |
| E | 240–255 | N/A | N/A | Experimental |

**RFC 1918 Private Ranges:**
- `10.0.0.0/8`
- `172.16.0.0/12` (i.e., `172.16.0.0` – `172.31.255.255`)
- `192.168.0.0/16`

→ See [[04 - IPv4 Network Layer/04.02 Classful Addressing|Classful Addressing]].

---

##  Subnet Math Cheat Sheet

| Prefix | Mask | Usable Hosts | Block Size |
| :-: | :--- | :---: | :---: |
| /24 | 255.255.255.0 | 254 | 256 |
| /25 | 255.255.255.128 | 126 | 128 |
| /26 | 255.255.255.192 | 62 | 64 |
| /27 | 255.255.255.224 | 30 | 32 |
| /28 | 255.255.255.240 | 14 | 16 |
| /29 | 255.255.255.248 | 6 | 8 |
| /30 | 255.255.255.252 | 2 | 4 |

**Formulas:**
- Borrowed subnet bits: $2^n \ge$ required subnets
- Usable hosts per subnet: $2^h - 2$
- Subnet ID: `IP AND Mask`
- Broadcast: `Subnet ID OR (NOT Mask)`

→ See [[04 - IPv4 Network Layer/04.05 FLSM|FLSM]] and [[04 - IPv4 Network Layer/04.06 VLSM|VLSM]].

---

##  MAC Address Quick Facts

- 48 bits / 6 octets, written in hex (`00:1A:2B:3C:4D:5E`).
- OUI = first 3 octets (vendor).
- **I/G bit** (LSB of first octet): `0` = Unicast, `1` = Multicast.
- **U/L bit** (next bit): `0` = Globally unique, `1` = Locally administered.
- Broadcast = `FF:FF:FF:FF:FF:FF`.
- Multicast IPv4 maps to OUI `01:00:5E:...`.
- **Source MAC must always be unicast.**

→ See [[03 - Physical & Data Link Layer/03.02 MAC Addressing|MAC Addressing]].

---

##  Ethernet II Frame

| Field | Bytes |
| :--- | :-: |
| Preamble | 8 |
| Destination MAC | 6 |
| Source MAC | 6 |
| EtherType | 2 |
| Payload | 46–1500 |
| FCS (CRC) | 4 |

- **Min frame (excl. preamble & FCS):** 64 bytes
- **Max frame (excl. preamble & FCS):** 1518 bytes
- EtherType values: `0x0800` IPv4, `0x0806` ARP, `0x86DD` IPv6, `0x8100` 802.1Q tag.

→ See [[03 - Physical & Data Link Layer/03.03 Ethernet II Frame Structure|Ethernet II Frame]].

---

##  Administrative Distance Defaults (Cisco)

| Source | AD |
| :--- | :-: |
| Directly Connected | 0 |
| Static Route | 1 |
| EIGRP (internal) | 90 |
| IGRP | 100 |
| OSPF | 110 |
| RIP | 120 |
| External EIGRP | 170 |
| Unreachable | 255 |

→ See [[07 - IP Routing/07.02 Administrative Distance & Metrics|Administrative Distance]].

---

##  Routing Protocols at a Glance

| Protocol | Type | Algorithm | Metric | Update | AD |
| :--- | :--- | :--- | :--- | :--- | :-: |
| RIPv1 | Distance-Vector | Bellman-Ford | Hop count | Broadcast 30s | 120 |
| RIPv2 | Distance-Vector | Bellman-Ford | Hop count | Multicast 224.0.0.9 30s | 120 |
| OSPF | Link-State | Dijkstra (SPF) | Cost (ref BW / link BW) | LSU event-driven + LSA refresh | 110 |
| EIGRP | Hybrid (advanced DV) | DUAL | Composite (BW + delay) | Event-driven, partial | 90 |
| BGP | Path-Vector | Best-path selection | Path attributes | TCP 179 | 20 (eBGP) / 200 (iBGP) |

**RIP loop prevention:** Split Horizon, Poison Reverse, Hold-Down (60s), Invalid Timer (180s), Flush Timer (240s).
**BGP loop prevention:** discard any update whose `AS_PATH` contains the local ASN.

→ See [[08 - Routing Protocols/08.00 Chapter Overview|Chapter 8 Overview]].

---

##  TCP vs UDP

| Property | TCP | UDP |
| :--- | :-: | :-: |
| Connection | Oriented (3-way handshake) | Connectionless |
| Reliability | Reliable (ACKs, retransmit) | Best-effort |
| Ordering | Ordered (sequence numbers) | Unordered |
| Header | 20–60 bytes | 8 bytes (fixed) |
| Flow control | Sliding window | None |
| Congestion control | Slow start, AIMD | None |
| Use cases | Web, mail, file transfer | DNS, VoIP, gaming, DHCP |

→ See [[10 - Transport Layer/10.11 TCP vs UDP Comparison|TCP vs UDP]].

---

##  Well-Known Ports You Must Memorize

| Port | Proto | Service |
| :-: | :-: | :--- |
| 20/21 | TCP | FTP (data/control) |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | UDP/TCP | DNS |
| 67/68 | UDP | DHCP (server/client) |
| 69 | UDP | TFTP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 161 | UDP | SNMP |
| 179 | TCP | BGP |
| 443 | TCP | HTTPS |

→ Full table: [[10 - Transport Layer/10.03 Well-Known Ports Reference|Ports Reference]].

---

##  TCP 3-Way Handshake

```
Client                Server
  |--- SYN (seq=x) --->|
  |<- SYN-ACK (seq=y, ack=x+1) -|
  |--- ACK (ack=y+1) -->|
```

**4-step close:** `FIN → ACK → FIN → ACK`.

→ See [[10 - Transport Layer/10.08 TCP Connection Lifecycle|TCP Connection Lifecycle]].

---

##  Fragmentation Quick Recipe

1. `Data = OriginalPacket − Header`
2. `MaxPayload = floor((MTU − Header) / 8) × 8`
3. `N = ceil(Data / MaxPayload)`
4. For each fragment: `Length = Payload + Header`, `Offset = (BytesBeforeMe) / 8`, `MF = 1` except last.

→ See [[05 - IP Datagram & Fragmentation/05.02 Fragmentation Mathematics|Fragmentation Math]].

---

##  NAT Type Matrix

| Type | Mapping | Use | Pool Demand |
| :--- | :--- | :--- | :--- |
| Static | 1:1 permanent | Public servers (DMZ) | High |
| Dynamic | m:n pool | Outbound bursts | Medium |
| PAT (Overload) | n:1 + ports | Home/SMB internet | Low (1 IP) |

→ See [[09 - NAT & Perimeter Security/09.00 Chapter Overview|Chapter 9 Overview]].

---

##  Cisco IOS Mode Prompts

| Mode | Prompt | Enter via |
| :--- | :--- | :--- |
| User EXEC | `Router>` | (default) |
| Privileged EXEC | `Router#` | `enable` |
| Global Config | `Router(config)#` | `configure terminal` |
| Interface Config | `Router(config-if)#` | `interface fa0/0` |
| Line Config | `Router(config-line)#` | `line vty 0 4` |
| Router Config | `Router(config-router)#` | `router rip` |

→ See [[13 - Cisco IOS CLI/13.01 CLI Modes & Prompts|CLI Modes]].

---

##  Top Mnemonics

- **OSI layers (bottom-up):** "Please Do Not Throw Sausage Pizza Away" — Physical, Data Link, Network, Transport, Session, Presentation, Application.
- **Subnetting flow:** "Classy Friends Visit Small Gateways" → C→F→V→S→G.
- **Fragmentation steps:** "Don't Make Networking Terrifying" → D→M→N→T (Data → Max → Number → Table).
- **TCP flags:** UAPRSF → "U Are Prepared, Restart Server Fast" (Urgent, Ack, Psh, Rst, Syn, Fin).

→ More in [[14 - Memory Aids & Mnemonics/14.00 Chapter Overview|Memory Aids]].
