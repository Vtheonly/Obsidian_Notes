---
title: "Quiz 06 — ARP & NAT"
type: quiz
chapter: 06
sources:
  - "[[06 - ARP & Address Resolution/06.01 ARP Concepts]]"
  - "[[06 - ARP & Address Resolution/06.02 ARP Operation Lifecycle]]"
  - "[[06 - ARP & Address Resolution/06.03 ARP Packet Format]]"
  - "[[06 - ARP & Address Resolution/06.04 Advanced ARP]]"
  - "[[09 - NAT & Perimeter Security/09.01 NAT Principles]]"
  - "[[09 - NAT & Perimeter Security/09.02 Static NAT]]"
  - "[[09 - NAT & Perimeter Security/09.03 Dynamic NAT]]"
  - "[[09 - NAT & Perimeter Security/09.04 PAT NAT Overload]]"
tags: [quiz, arp, nat]
---

#  Quiz 06 — ARP & NAT

> [!abstract] Test Your Knowledge
> This quiz covers ARP (request/reply, packet format, gratuitous ARP, security) and NAT (static, dynamic, PAT, port forwarding).

---

## Part 1 — True / False

> [!question] The IP address block 172.16.0.0/12 is reserved for private network use.
>> [!success]- Answer
>> **True.** RFC 1918 private range — covers 172.16.0.0 to 172.31.255.255.

> [!question] Static NAT provides a one-to-one permanent mapping between private and public IP addresses.
>> [!success]- Answer
>> **True.**

> [!question] Class A private IP address range is 10.0.0.0/8.
>> [!success]- Answer
>> **True.**

> [!question] NAT was primarily developed to improve routing latency on WAN boundaries.
>> [!success]- Answer
>> **False.** NAT was developed to mitigate IPv4 address exhaustion.

> [!question] The EtherType value for an ARP frame in Ethernet II is 0x0806.
>> [!success]- Answer
>> **True.**

> [!question] ARP is used to resolve IPv6 addresses to MAC addresses.
>> [!success]- Answer
>> **False.** IPv6 uses NDP (Neighbor Discovery Protocol, ICMPv6 types 135/136) instead of ARP.

> [!question] An ARP Request packet has the target hardware address set to the sender's MAC address.
>> [!success]- Answer
>> **False.** It's set to all zeros (`00:00:00:00:00:00`) — the sender doesn't know the target MAC, that's why it's asking.

> [!question] Inbound packets entering a PAT router are translated by matching the destination port against the translation table.
>> [!success]- Answer
>> **True.** PAT tracks (public IP, public port) → (private IP, private port).

> [!question] Dynamic NAT maps private IP addresses to public IP addresses from a pool of registered public addresses.
>> [!success]- Answer
>> **True.**

> [!question] The destination MAC address in an Ethernet header for an ARP Request is FF:FF:FF:FF:FF:FF.
>> [!success]- Answer
>> **True.** ARP Requests are broadcasts.

> [!question] Port Address Translation has higher router CPU and memory overhead than Static NAT.
>> [!success]- Answer
>> **True.** PAT must maintain a state table for thousands of port mappings.

> [!question] An ARP Reply is flooded out of all ports by a switch.
>> [!success]- Answer
>> **False.** The ARP Reply is unicast — the switch forwards it only to the destination port.

> [!question] A router decapsulates the Layer 2 header of an incoming frame to expose the Layer 3 IP packet.
>> [!success]- Answer
>> **True.**

> [!question] Static NAT is more efficient in public IP space consumption than PAT.
>> [!success]- Answer
>> **False.** PAT is far more efficient — one public IP serves thousands of hosts.

> [!question] Static NAT is typically used for internal servers that must be accessible from the public Internet.
>> [!success]- Answer
>> **True.** DMZ web/mail servers commonly use static NAT.

> [!question] An ARP Request is sent as a unicast frame to the target host.
>> [!success]- Answer
>> **False.** It's a broadcast (`FF:FF:FF:FF:FF:FF`).

> [!question] Private IP addresses defined in RFC 1918 are routable across the public Internet.
>> [!success]- Answer
>> **False.** ISPs filter them at borders (BCP 38).

> [!question] A Layer 2 switch dynamically populates its CAM table by inspecting the source MAC addresses of incoming frames.
>> [!success]- Answer
>> **True.**

> [!question] An ARP packet is directly encapsulated inside an IP packet.
>> [!success]- Answer
>> **False.** ARP rides directly inside Ethernet (EtherType 0x0806), not inside IP.

> [!question] Under PAT, the router tracks connections by using unique source port numbers.
>> [!success]- Answer
>> **True.**

---

## Part 2 — Multiple Choice

> [!question] What security advantage does PAT provide?
> a) Automatically filters malware downloads
> b) Encrypts all payload data passing through the router
> c) Conceals internal network topology and blocks unsolicited inbound traffic
> d) Protects against all Layer 7 application exploits
>> [!success]- Answer
>> **c) Conceals internal network topology and blocks unsolicited inbound traffic**

> [!question] What is the maximum number of concurrent translation sessions theoretically possible per public IP under PAT?
> a) Dependent on the IP pool size
> b) Unlimited
> c) Exactly 254
> d) Up to 65,536 (limited by port range)
>> [!success]- Answer
>> **d) Up to 65,536 (limited by port range)**

> [!question] What is the default value of the target hardware address field inside an ARP Request payload?
> a) FF:FF:FF:FF:FF:FF
> b) Randomly generated
> c) The sender's MAC address
> d) 00:00:00:00:00:00
>> [!success]- Answer
>> **d) 00:00:00:00:00:00** — it's unknown, that's why we're asking.

> [!question] What CLI command displays the ARP cache on Cisco IOS devices?
> a) show arp
> b) arp -a
> c) show mac-address-table
> d) show ip route
>> [!success]- Answer
>> **a) show arp** (Note: `arp -a` works on Windows/Linux/macOS, not Cisco IOS.)

> [!question] What NAT type establishes a permanent one-to-one mapping between internal and external IP addresses?
> a) Dynamic NAT
> b) Static NAT
> c) Port Address Translation
> d) NAT Overload
>> [!success]- Answer
>> **b) Static NAT**

> [!question] Which IP address block represents the Class A RFC 1918 private range?
> a) 172.16.0.0/12
> b) 10.0.0.0/8
> c) 192.168.0.0/16
> d) 192.0.2.0/24
>> [!success]- Answer
>> **b) 10.0.0.0/8**

> [!question] What does the CAM table map?
> a) IP Address to MAC Address
> b) IP Address to Switch Port
> c) MAC Address to Switch Port
> d) Port Number to IP Address
>> [!success]- Answer
>> **c) MAC Address to Switch Port**

> [!question] How does a non-target host handle an incoming ARP Request broadcast?
> a) Forwards it to the default gateway
> b) Updates its ARP cache and drops it
> c) Replies with its own MAC address
> d) Drops the packet after comparing the target IP
>> [!success]- Answer
>> **d) Drops the packet after comparing the target IP**

> [!question] Which translation profile is best suited for an internal Web server that needs public inbound access?
> a) Static NAT
> b) Dynamic NAT
> c) PAT
> d) NAT Overload
>> [!success]- Answer
>> **a) Static NAT**

> [!question] What is the EtherType value for ARP in an Ethernet II frame?
> a) 0x0806
> b) 0x8100
> c) 0x86DD
> d) 0x0800
>> [!success]- Answer
>> **a) 0x0806** (0x0800 = IPv4, 0x86DD = IPv6, 0x8100 = 802.1Q VLAN tag)

> [!question] What type of address mapping is performed by the Address Resolution Protocol (ARP)?
> a) Logical IP to Physical MAC
> b) Logical IP to Port Number
> c) Domain Name to IP Address
> d) Physical MAC to Switch Port
>> [!success]- Answer
>> **a) Logical IP to Physical MAC**

> [!question] What is a primary disadvantage of PAT (NAT Overload)?
> a) Requires one public IP per internal host
> b) Prevents outbound client access
> c) Exposes the internal topology to the public network
> d) High router resources and state table overhead
>> [!success]- Answer
>> **d) High router resources and state table overhead**

> [!question] What happens to an ARP Request frame when it arrives at a Layer 2 switch port?
> a) Routed to the default gateway
> b) Forwarded directly to the target host's port
> c) Discarded unless target MAC is known
> d) Flooded out all ports except the receiving port
>> [!success]- Answer
>> **d) Flooded out all ports except the receiving port**

> [!question] What is the size of the port number field in TCP/UDP headers?
> a) 32 bits
> b) 16 bits
> c) 64 bits
> d) 8 bits
>> [!success]- Answer
>> **b) 16 bits** (range 0–65535)

> [!question] Which layer of the OSI model does the ARP cache operate at?
> a) Layer 4
> b) Layer 7
> c) Layer 1
> d) Layer 2/3 boundary
>> [!success]- Answer
>> **d) Layer 2/3 boundary** — it bridges L3 (IP) to L2 (MAC).

> [!question] Which parameter is NOT part of the 5-Tuple connection key?
> a) Destination IP Address
> b) Source IP Address
> c) Protocol
> d) Source MAC Address
>> [!success]- Answer
>> **d) Source MAC Address** — the 5-tuple is (Protocol, Src IP, Src Port, Dst IP, Dst Port).

> [!question] Which Class C private IP address block is defined by RFC 1918?
> a) 10.0.0.0/8
> b) 192.168.1.0/24 only
> c) 172.16.0.0/12
> d) 192.168.0.0/16
>> [!success]- Answer
>> **d) 192.168.0.0/16**

> [!question] How does a switch dynamically populate its MAC address table?
> a) Inspecting the source MAC address of incoming frames
> b) Manually configured by the administrator only
> c) Listening to ARP Reply broadcasts
> d) Querying the local DNS server
>> [!success]- Answer
>> **a) Inspecting the source MAC address of incoming frames**

> [!question] What is another term for Port Address Translation (PAT)?
> a) Dynamic Pool NAT
> b) NAT Overload
> c) Static Port Mapping
> d) 1:1 NAT
>> [!success]- Answer
>> **b) NAT Overload**

> [!question] What limitation exists in Dynamic NAT when mapping many-to-many addresses?
> a) Only one public IP can be utilized by the router
> b) Inbound connections are automatically forwarded to all hosts
> c) Outbound sessions fail if the public IP pool is exhausted
> d) It requires port-level translation state tracking
>> [!success]- Answer
>> **c) Outbound sessions fail if the public IP pool is exhausted**

> [!question] Which protocol resolves MAC addresses to IP addresses in IPv6?
> a) DHCPv6
> b) Neighbor Discovery Protocol (NDP)
> c) Address Resolution Protocol (ARP)
> d) ICMPv6 Redirect
>> [!success]- Answer
>> **b) Neighbor Discovery Protocol (NDP)** — ICMPv6 types 135 (NS) and 136 (NA).

> [!question] At what boundary device does NAT translation typically occur?
> a) Core Layer 2 Switch
> b) Client Host Operating System
> c) Perimeter Gateway Router
> d) Local DNS Server
>> [!success]- Answer
>> **c) Perimeter Gateway Router**

---

## Part 3 — Matching

> [!question] Match the networking component with its definition.
>> [!example] Group A
>> a) Hold-Down Timer
>> b) 172.16.0.0/12
>> c) 192.168.0.0/16
>
>> [!example] Group B
>> n) Class C private IP address block
>> o) Class B private IP address block
>> p) Ignores RIP updates with worse metrics for 60s
>
>> [!success]- Answer
>> a) → p)
>> b) → o)
>> c) → n)

> [!question] Match the networking component with its definition.
>> [!example] Group A
>> a) Split Horizon
>> b) Registered Ports
>> c) Class B range limit
>
>> [!example] Group B
>> n) Never advertise route out ingress interface
>> o) IANA registered vendor ports (1024 to 49151)
>> p) Ends at 172.31.255.255
>
>> [!success]- Answer
>> a) → n)
>> b) → o)
>> c) → p)

> [!question] Match the networking component with its definition.
>> [!example] Group A
>> a) arp -a
>> b) Static NAT
>> c) 0x0800
>
>> [!example] Group B
>> n) One-to-one permanent mapping of public/private IP
>> o) Command to view local ARP cache on PC
>> p) EtherType designating IPv4 payload
>
>> [!success]- Answer
>> a) → o)
>> b) → n)
>> c) → p)

> [!question] Match the networking component with its definition.
>> [!example] Group A
>> a) 192.168.0.0/16
>> b) 10.0.0.0/8
>> c) PAT / Overload
>
>> [!example] Group B
>> n) Class A private IP address block
>> o) Maps multiple private IPs to one public IP using ports
>> p) Class C private IP address block
>
>> [!success]- Answer
>> a) → p)
>> b) → n)
>> c) → o)

> [!question] Match the networking component with its definition.
>> [!example] Group A
>> a) Invalid Timer
>> b) FCS / CRC
>> c) NDP
>
>> [!example] Group B
>> n) Resolves L3 to L2 addresses in IPv6
>> o) Used to check Layer 2 frame corruption
>> p) Mark RIP route as cost 16 after 180s
>
>> [!success]- Answer
>> a) → p)
>> b) → o)
>> c) → n)

> [!question] Match the networking component with its definition.
>> [!example] Group A
>> a) Inside Global Address
>> b) ARP Cache
>> c) FF:FF:FF:FF:FF:FF
>
>> [!example] Group B
>> n) Public IP representing internal host on WAN
>> o) Maps IP addresses to physical MAC addresses
>> p) Layer 2 broadcast MAC address
>
>> [!success]- Answer
>> a) → n)
>> b) → o)
>> c) → p)

> [!question] Match the NAT type with its primary use case.
>> [!example] Group A
>> a) Static NAT
>> b) Dynamic NAT
>> c) PAT / Overload
>
>> [!example] Group B
>> n) Maps private IP to a public pool dynamically
>> o) One-to-one permanent mapping (for public servers)
>> p) Maps many private IPs to one public IP using ports (home/SMB)
>
>> [!success]- Answer
>> a) → o)
>> b) → n)
>> c) → p)

> [!question] Match the ARP packet field with its value in a Request.
>> [!example] Group A
>> a) Sender Hardware Address
>> b) Target Hardware Address
>> c) Operation (Opcode)
>
>> [!example] Group B
>> n) 1 (Request)
>> o) Sender's MAC (e.g., 00:0B:DB:16:E7:8A)
>> p) 00:00:00:00:00:00 (unknown)
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → n)

> [!question] Match the Cisco NAT term with its meaning.
>> [!example] Group A
>> a) Inside Local
>> b) Inside Global
>> c) Outside Global
>
>> [!example] Group B
>> n) Public IP of an external destination host
>> o) Public IP the NAT device translates an internal host to
>> p) Private IP of an internal host, as seen from the inside
>
>> [!success]- Answer
>> a) → p)
>> b) → o)
>> c) → n)

> [!question] Match the device with its primary role.
>> [!example] Group A
>> a) Layer 2 Switch
>> b) Layer 3 Router
>> c) Firewall
>
>> [!example] Group B
>> n) Forwards frames based on MAC addresses; one broadcast domain by default
>> o) Forwards packets based on IP addresses; terminates broadcast domains
>> p) Inspects traffic against ruleset; can be stateful or NGFW
>
>> [!success]- Answer
>> a) → n)
>> b) → o)
>> c) → p)

---

##  Score Interpretation

- **0–17 (≤ 50%):** Review ARP and NAT fundamentals.
- **18–25 (50–75%):** Decent. Review missed topics.
- **26–32 (75–95%):** Strong.
- **33+ (> 95%):** Excellent. Move to [[Quizzes/Quiz 07 - Routing Protocols|Quiz 07]].
