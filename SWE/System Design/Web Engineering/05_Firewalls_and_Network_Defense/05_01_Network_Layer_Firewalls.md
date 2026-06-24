## 5.1. Network Layer Firewalls (IP and Port Filtering)

A Network Layer Firewall operates primarily at **OSI Layers 3 and 4 (Network and Transport)**. It is responsible for policing traffic coming into and going out of a network based purely on packet header addresses.

---

### 1. Packet Filtering Firewalls

A basic packet-filtering firewall inspects packets on the fly. It compares each packet against a static rule matrix containing specific conditions:

```
[ Incoming Packet ]
       │
       ├──► Source IP: 198.51.100.42
       ├──► Destination Port: 80
       └──► TCP Flag: SYN
       │
[ Firewall Rule Evaluation ]
       │
       ├── Rule 1: ALLOW Source 197.112.0.0/16 ──► No Match
       └── Rule 2: DROP Source 198.51.100.0/24  ──► MATCH! Packet Dropped
```

The firewall evaluates rules sequentially. If a packet matches a rule's conditions, the defined action is executed:
* **ACCEPT/ALLOW:** The packet is allowed to pass through the interface.
* **DROP:** The packet is silently discarded. The client's connection attempt hangs and eventually times out.
* **REJECT:** The packet is discarded, and a rejection response (typically a TCP RST packet for TCP, or an ICMP Port Unreachable packet for UDP) is returned to the sender.

---

### 2. Stateful Packet Inspection (SPI)

Early firewalls were **stateless**—they evaluated each packet as a completely independent unit. This meant developers had to open a wide range of incoming ephemeral ports so that returning traffic from established outgoing connections could pass back into the network.

Modern firewalls use **Stateful Packet Inspection (SPI)**. An stateful firewall maintains an in-memory **state table** tracking all active, established connections:

```
State Table Example:
| Source IP:Port | Destination IP:Port | State |
| :--- | :--- | :--- |
| 192.168.1.50:51224 | 93.184.216.34:443 | ESTABLISHED |
```

When a packet arrives, the SPI firewall checks this state table first. If the packet belongs to an already active, valid outbound connection, it is allowed through automatically without needing to be validated against the static rule matrix again. This significantly increases performance and improves network security.

---

###  Common Student Pitfalls & Pro-Tips
* **The "Hang" vs. "Refuse" Indicator:** If your web automation script returns a connection timeout error, the target network layer firewall is likely set to **DROP** your packets. If your script returns a connection refused error, either the host port is closed or the firewall is configured to **REJECT** your connection.

---
