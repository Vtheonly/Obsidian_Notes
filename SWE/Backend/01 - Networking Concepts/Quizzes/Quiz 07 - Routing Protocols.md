---
title: "Quiz 07 — Routing Protocols"
type: quiz
chapter: 07
sources:
  - "[[08 - Routing Protocols/08.01 Distance-Vector - RIP]]"
  - "[[08 - Routing Protocols/08.02 RIP Loop Prevention]]"
  - "[[08 - Routing Protocols/08.04 Link-State - OSPF]]"
  - "[[08 - Routing Protocols/08.05 OSPF Areas & Router Types]]"
  - "[[08 - Routing Protocols/08.06 OSPF Cost & Gigabit Bottleneck]]"
  - "[[08 - Routing Protocols/08.07 Dijkstra Algorithm Walkthrough]]"
  - "[[08 - Routing Protocols/08.08 Path-Vector - BGP]]"
tags: [quiz, routing, rip, ospf, bgp, dijkstra]
---

#  Quiz 07 — Routing Protocols

> [!abstract] Test Your Knowledge
> This quiz covers RIP loop prevention, OSPF areas and cost, Dijkstra's algorithm, and BGP mechanics.

---

## Part 1 — True / False

> [!question] Longest Prefix Match selects the route with the shortest prefix length.
>> [!success]- Answer
>> **False.** LPM picks the **longest** matching prefix (most specific).

> [!question] The invalid timer in RIP is typically 60 seconds.
>> [!success]- Answer
>> **False.** Invalid timer is 180s. Hold-Down is 60s (Cisco).

> [!question] Dynamic routing consumes additional network bandwidth compared to static routing.
>> [!success]- Answer
>> **True.** Hellos, LSAs, periodic updates all consume bandwidth.

> [!question] Distance-vector protocols have a complete topological map of the entire network.
>> [!success]- Answer
>> **False.** Distance-vector routers know only their neighbors' tables. Link-state protocols (OSPF) have the full map.

> [!question] LSAs in OSPF are flooded only within the area they originate from.
>> [!success]- Answer
>> **True.** Type 1 and 2 LSAs stay in their area. Type 3, 4, 5 cross area boundaries.

> [!question] OSPF is a link-state routing protocol that uses Dijkstra's algorithm.
>> [!success]- Answer
>> **True.**

> [!question] If dest MAC of incoming frame doesn't match the router's interface MAC, the router still processes the Layer 3 header.
>> [!success]- Answer
>> **False.** The router drops the frame at L2 if the MAC doesn't match.

> [!question] The default Administrative Distance of OSPF is 120.
>> [!success]- Answer
>> **False.** OSPF = 110. RIP = 120.

> [!question] Connected interfaces have an Administrative Distance of 1.
>> [!success]- Answer
>> **False.** Connected = 0. Static = 1.

> [!question] IGPs are used to route traffic between different Autonomous Systems.
>> [!success]- Answer
>> **False.** IGPs (RIP, OSPF, EIGRP) route *within* an AS. EGPs (BGP) route *between* ASes.

> [!question] BGP is a path-vector routing protocol used for inter-domain routing.
>> [!success]- Answer
>> **True.**

> [!question] An ASBR connects OSPF to external networks or static routes.
>> [!success]- Answer
>> **True.**

> [!question] In OSPF, neighbor discovery is performed using multicast Hello packets.
>> [!success]- Answer
>> **True.** OSPF hellos go to `224.0.0.5` (all OSPF routers).

> [!question] BGP neighbors establish a TCP connection over port 179.
>> [!success]- Answer
>> **True.**

> [!question] BGP loop prevention relies on checking if the local ASN is present in the AS_PATH attribute.
>> [!success]- Answer
>> **True.**

> [!question] The default reference bandwidth for OSPF metric calculation is 100 Mbps.
>> [!success]- Answer
>> **True.** Default is $10^8$ bps.

> [!question] By default, OSPF assigns a cost of 1 to both Fast Ethernet and Gigabit Ethernet interfaces.
>> [!success]- Answer
>> **True.** This is the gigabit bottleneck — fix with `auto-cost reference-bandwidth 10000`.

> [!question] Static routing adapts automatically to link failures.
>> [!success]- Answer
>> **False.** Static routes don't adapt — manual intervention needed.

> [!question] Split Horizon prevents routing loops by not advertising a route back out the interface it was learned from.
>> [!success]- Answer
>> **True.**

> [!question] Poison Reverse immediately advertises a failed route with a hop count of 16.
>> [!success]- Answer
>> **True.**

---

## Part 2 — Multiple Choice

> [!question] During packet forwarding, which MAC address is placed as the Source MAC of the new frame?
> a) The MAC of the router's egress exit interface
> b) The MAC of the receiving switch interface
> c) The MAC of the sending host
> d) The MAC of the next-hop router
>> [!success]- Answer
>> **a) The MAC of the router's egress exit interface**

> [!question] Which protocol maintains a synchronized Link-State Database (LSDB) on all routers within an area?
> a) BGP
> b) OSPF
> c) Static Routing
> d) RIPv2
>> [!success]- Answer
>> **b) OSPF**

> [!question] If a router receives a packet with a TTL of 1 destined for a remote network, what does it do?
> a) Drops the packet and sends ICMP Type 11
> b) Increments TTL by 1
> c) Decrements TTL to 0 and forwards it
> d) Forwards to default gateway
>> [!success]- Answer
>> **a) Drops the packet and sends ICMP Type 11** (Time Exceeded in Transit).

> [!question] What is a key difference between RIPv1 and RIPv2?
> a) RIPv1 has a lower metric limit
> b) RIPv2 is link-state based
> c) RIPv2 uses Dijkstra's algorithm
> d) RIPv2 is classless and supports VLSM
>> [!success]- Answer
>> **d) RIPv2 is classless and supports VLSM**

> [!question] In the OSPF cost metric, what is the cost of a 10-Gbps interface if reference-bandwidth is set to 10000?
> a) 1
> b) 100
> c) 10
> d) 1000
>> [!success]- Answer
>> **a) 1** — 10000 / 10000 = 1.

> [!question] What hop count value represents an unreachable route in RIP?
> a) 16
> b) 15
> c) 0
> d) 255
>> [!success]- Answer
>> **a) 16** (15 is the max reachable)

> [!question] How long does the RIP hold-down timer lock a route after an unreachable update is received?
> a) 30 seconds
> b) 180 seconds
> c) 120 seconds
> d) 60 seconds
>> [!success]- Answer
>> **d) 60 seconds** (Cisco default; RFC says 180s)

> [!question] Which BGP message type is used to withdraw inactive routes?
> a) Notification
> b) Update
> c) Open
> d) Keepalive
>> [!success]- Answer
>> **b) Update** — Update messages can advertise new routes OR withdraw dead ones.

> [!question] What does an Internal Router (IR) in OSPF represent?
> a) A router connecting different areas
> b) A router on the network border
> c) A router with all interfaces in a single area
> d) A central backbone router
>> [!success]- Answer
>> **c) A router with all interfaces in a single area**

> [!question] What is the Longest Prefix Match rule used for?
> a) Selecting the route learned first
> b) Selecting the route with the lowest metric
> c) Selecting the route with the lowest AD
> d) Selecting the route with the most specific match
>> [!success]- Answer
>> **d) Selecting the route with the most specific match**

> [!question] Which area in a multi-area OSPF design is the backbone area?
> a) Area 1.1.1.1
> b) The non-backbone area
> c) Area 0.0.0.0
> d) The stub area
>> [!success]- Answer
>> **c) Area 0.0.0.0** (Area 0)

> [!question] What type of updates does RIPv1 use?
> a) Broadcast updates to 255.255.255.255
> b) Unicast updates to neighbors
> c) Path-vector updates
> d) Multicast updates to 224.0.0.9
>> [!success]- Answer
>> **a) Broadcast updates to 255.255.255.255** (RIPv2 uses multicast 224.0.0.9)

> [!question] What message is sent when a BGP protocol error occurs, immediately closing the peer connection?
> a) Update
> b) Keepalive
> c) Open
> d) Notification
>> [!success]- Answer
>> **d) Notification**

> [!question] Over which TCP port do BGP neighbors establish peer sessions?
> a) Port 443
> b) Port 80
> c) Port 22
> d) Port 179
>> [!success]- Answer
>> **d) Port 179**

> [!question] How is OSPF cost metric calculated?
> a) Administrative Distance / Link Speed
> b) Reference Bandwidth / Interface Bandwidth
> c) Hop Count to Destination
> d) Path Bandwidth * Delay
>> [!success]- Answer
>> **b) Reference Bandwidth / Interface Bandwidth**

> [!question] Which routing protocol has a default Administrative Distance of 110?
> a) EIGRP
> b) RIPv2
> c) BGP
> d) OSPF
>> [!success]- Answer
>> **d) OSPF**

> [!question] What OSPF router role connects a regular area to the backbone area?
> a) Internal Router (IR)
> b) Autonomous System Boundary Router (ASBR)
> c) Area Boundary Router (ABR)
> d) Backbone Router (BR)
>> [!success]- Answer
>> **c) Area Boundary Router (ABR)**

> [!question] What reference bandwidth value is used by default in Cisco IOS OSPF cost calculations?
> a) 10^9 bps (1 Gbps)
> b) 10^8 bps (100 Mbps)
> c) 10^10 bps (10 Gbps)
> d) 10^7 bps (10 Mbps)
>> [!success]- Answer
>> **b) 10^8 bps (100 Mbps)**

> [!question] Which mechanism prevents a router from advertising a route out the same interface it was learned from?
> a) Hold-down Timers
> b) Loop Prevention Vector
> c) Poison Reverse
> d) Split Horizon
>> [!success]- Answer
>> **d) Split Horizon**

> [!question] What algorithm is run locally by OSPF routers against the LSDB to calculate routes?
> a) Dijkstra's SPF algorithm
> b) Bellman-Ford
> c) Floyd-Warshall
> d) A* Search
>> [!success]- Answer
>> **a) Dijkstra's SPF algorithm**

> [!question] What is BGP classified as?
> a) Path-Vector Routing Protocol
> b) Static Routing Protocol
> c) Distance-Vector Routing Protocol
> d) Link-State Routing Protocol
>> [!success]- Answer
>> **a) Path-Vector Routing Protocol**

> [!question] What does the router do if a packet exceeds the outbound MTU and the DF flag is set to 1?
> a) Fragments the packet anyway
> b) Buffers the packet
> c) Drops the packet and sends ICMP Type 3 Code 4
> d) Ignores the MTU limit
>> [!success]- Answer
>> **c) Drops the packet and sends ICMP Type 3 Code 4** (Fragmentation Needed)

> [!question] How does BGP prevent routing loops across Autonomous Systems?
> a) Checking if its own ASN is in the AS_PATH attribute
> b) Hop Count limits
> c) Split Horizon
> d) Poison Reverse
>> [!success]- Answer
>> **a) Checking if its own ASN is in the AS_PATH attribute**

> [!question] Which command resolves the OSPF Gigabit bottleneck issue?
> a) auto-cost reference-bandwidth 10000
> b) ospf reference-bandwidth 1000
> c) ip ospf cost 1
> d) reference-bandwidth gigabit
>> [!success]- Answer
>> **a) auto-cost reference-bandwidth 10000**

> [!question] What action does a router take if the incoming L2 frame fails the CRC/FCS check?
> a) Extracts the IP packet
> b) Floods the frame
> c) Requests retransmission
> d) Discards the frame immediately
>> [!success]- Answer
>> **d) Discards the frame immediately**

---

## Part 3 — Matching

> [!question] Match the protocol with its algorithm.
>> [!example] Group A
>> a) RIPv2
>> b) OSPF
>> c) BGP
>
>> [!example] Group B
>> n) Dijkstra SPF (link-state)
>> o) Bellman-Ford (distance-vector)
>> p) Best-path selection (path-vector)
>
>> [!success]- Answer
>> a) → o)
>> b) → n)
>> c) → p)

> [!question] Match the OSPF router role with its description.
>> [!example] Group A
>> a) Internal Router (IR)
>> b) Area Border Router (ABR)
>> c) Autonomous System Boundary Router (ASBR)
>
>> [!example] Group B
>> n) Connects a regular area to Area 0
>> o) All interfaces in a single non-zero area
>> p) Imports routes from external protocols
>
>> [!success]- Answer
>> a) → o)
>> b) → n)
>> c) → p)

> [!question] Match the RIP timer with its default value (Cisco).
>> [!example] Group A
>> a) Update Timer
>> b) Invalid Timer
>> c) Hold-Down Timer
>
>> [!example] Group B
>> n) 60 seconds
>> o) 30 seconds
>> p) 180 seconds
>
>> [!success]- Answer
>> a) → o) (30s)
>> b) → p) (180s)
>> c) → n) (60s)

> [!question] Match the OSPF packet type with its purpose.
>> [!example] Group A
>> a) Hello
>> b) Database Description (DBD)
>> c) Link-State Request (LSR)
>
>> [!example] Group B
>> n) Request specific LSAs from a neighbor
>> o) Discover and maintain neighbor adjacencies
>> p) Summarize LSDB contents for synchronization
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → n)

> [!question] Match the BGP message type with its purpose.
>> [!example] Group A
>> a) Open
>> b) Update
>> c) Notification
>> d) Keepalive
>
>> [!example] Group B
>> n) Verify session is alive when no updates are sent
>> o) Establish a BGP session
>> p) Advertise new routes or withdraw dead routes
>> q) Report errors and close the session
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → q)
>> d) → n)

> [!question] Match the routing protocol with its metric.
>> [!example] Group A
>> a) RIPv2
>> b) OSPF
>> c) EIGRP (internal)
>
>> [!example] Group B
>> n) Composite (BW + delay, by default)
>> o) Hop count
>> p) Cost (Reference BW / Interface BW)
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → n)

> [!question] Match the loop prevention mechanism with its protocol.
>> [!example] Group A
>> a) TTL decrement
>> b) AS_PATH check
>> c) Split Horizon
>
>> [!example] Group B
>> n) RIP (and all distance-vector protocols)
>> o) IP (Layer 3)
>> p) BGP
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → n)

> [!question] Match the OSPF area type with its LSA behavior.
>> [!example] Group A
>> a) Normal area
>> b) Stub area
>> c) NSSA
>
>> [!example] Group B
>> n) No type 5 external LSAs; can originate type 7
>> o) All LSA types accepted
>> p) No type 5 external LSAs; default route injected
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → n)

> [!question] Match the multicast address with its protocol.
>> [!example] Group A
>> a) 224.0.0.5
>> b) 224.0.0.9
>> c) 224.0.0.10
>
>> [!example] Group B
>> n) EIGRP
>> o) RIPv2
>> p) OSPF (all routers)
>
>> [!success]- Answer
>> a) → p)
>> b) → o)
>> c) → n)

> [!question] Match the Dijkstra algorithm step (from Node F walkthrough) with the resulting permanent list.
>> [!example] Group A
>> a) Step 1 (initial state)
>> b) Step 2 (after C permanent)
>> c) Step 3 (after E permanent)
>
>> [!example] Group B
>> n) P = {[F,0,-], [C,1,F], [E,2,F]}
>> o) P = {[F,0,-]}
>> p) P = {[F,0,-], [C,1,F]}
>
>> [!success]- Answer
>> a) → o)
>> b) → p)
>> c) → n)

---

##  Score Interpretation

- **0–17 (≤ 50%):** Re-read Chapter 8 carefully, especially [[08 - Routing Protocols/08.07 Dijkstra Algorithm Walkthrough|the Dijkstra walkthrough]].
- **18–25 (50–75%):** Decent. Review the missed questions' source notes.
- **26–32 (75–95%):** Strong.
- **33+ (> 95%):** Excellent. Move to [[Quizzes/Quiz 08 - Transport Layer|Quiz 08]].
