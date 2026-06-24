---
sources:
  - "[[07.00 Introduction]]"
  - "[[07.01 IP Router Operations & Packet Processing]]"
  - "[[07.02 Longest Prefix Match (LPM) Algorithmic Routing]]"
  - "[[07.03 Static vs. Dynamic Routing Paradigms]]"
  - "[[07.04 Distance Vector Protocols & RIPv2]]"
  - "[[07.05 Link-State Routing & OSPF]]"
  - "[[07.06 Path Vector Routing & BGP]]"
---

> [!question] Public Autonomous System Numbers (ASNs) range from 64512 to 65535.
>> [!success]- Answer
>> False

> [!question] BGP Notification messages are sent when a protocol error is detected, closing the session.
>> [!success]- Answer
>> True

> [!question] BGP peer relationships are established automatically using Hello broadcasts.
>> [!success]- Answer
>> False

> [!question] RIPv2 updates contain subnet masks, making it a classless protocol.
>> [!success]- Answer
>> True

> [!question] When the DF flag is set to 1 and the packet exceeds the outbound MTU, the router fragments the packet anyway.
>> [!success]- Answer
>> False

> [!question] If no route or default route matches the destination IP, the router returns ICMP Type 3 Code 0.
>> [!success]- Answer
>> True

> [!question] The IP header checksum remains unchanged when a router forwards a packet.
>> [!success]- Answer
>> False

> [!question] Administrative Distance ratings range from 0 to 255.
>> [!success]- Answer
>> True

> [!question] An Area Boundary Router (ABR) connects OSPF Area 0 to regular areas.
>> [!success]- Answer
>> True

> [!question] When a router drops a packet due to TTL expiration, it sends an ICMP Type 11 Code 0 message.
>> [!success]- Answer
>> True

> [!question] What algorithm is run locally by OSPF routers against the LSDB to calculate routes?
> a) Dijkstra's SPF algorithm
> b) Bellman-Ford
> c) Floyd-Warshall
> d) A* Search
>> [!success]- Answer
>> a) Dijkstra's SPF algorithm

> [!question] What RIP timer marks routes as unreachable (cost 16) if no updates are received?
> a) Invalid Timer (180s)
> b) Update Timer (30s)
> c) Flush Timer (240s)
> d) Hold-down Timer (60s)
>> [!success]- Answer
>> a) Invalid Timer (180s)

> [!question] Which administrative distance value represents a directly connected interface?
> a) 110
> b) 90
> c) 0
> d) 1
>> [!success]- Answer
>> c) 0

> [!question] What EtherType value designates an IPv4 payload inside an Ethernet II frame?
> a) 0x0800
> b) 0x86DD
> c) 0x0806
> d) 0x8100
>> [!success]- Answer
>> a) 0x0800

> [!question] Given destination IP 192.168.1.57, which route is selected among candidate routes?
> a) 192.168.1.0/24
> b) 192.168.1.48/28
> c) 0.0.0.0/0
> d) 192.168.0.0/16
>> [!success]- Answer
>> b) 192.168.1.48/28

> [!question] What algorithm is used by distance-vector protocols to calculate paths?
> a) Dijkstra SPF
> b) Prim's
> c) Kruskal's
> d) Bellman-Ford
>> [!success]- Answer
>> d) Bellman-Ford

> [!question] What range represents private Autonomous System Numbers (ASNs)?
> a) 1 to 64511
> b) 65536 to 99999
> c) 10000 to 20000
> d) 64512 to 65535
>> [!success]- Answer
>> d) 64512 to 65535

> [!question] Which protocol is the standard Exterior Gateway Protocol (EGP) of the Internet?
> a) BGP
> b) RIPv2
> c) OSPF
> d) EIGRP
>> [!success]- Answer
>> a) BGP

> [!question] If a router has routes for 10.0.0.0/24 from OSPF (AD 110) and RIP (AD 120), which route is selected?
> a) The OSPF route because it has the lower AD
> b) The RIP route because it has the lower metric
> c) It load balances between both
> d) The route learned first
>> [!success]- Answer
>> a) The OSPF route because it has the lower AD

> [!question] What design aspect keeps OSPF area topologies separate and reduces routing table size?
> a) Path-vector routing
> b) Multi-area design using ABRs
> c) Poison Reverse
> d) Split Horizon
>> [!success]- Answer
>> b) Multi-area design using ABRs

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Split Horizon
>> b) BGP
>> c) ASBR
>
>> [!example] Group B
>> n) Path-vector Exterior Gateway Protocol connecting the Internet.
>> o) Autonomous System Boundary Router importing external routes.
>> p) Loop prevention blocking route advertisement back to source port.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ABR
>> b) ICMP Type 11 Code 0
>> c) AD of 90
>
>> [!example] Group B
>> n) Administrative Distance of EIGRP protocol.
>> o) Message sent when a packet's TTL expires in transit.
>> p) Area Boundary Router connecting regular areas to Area 0.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) AD of 0
>> b) AD of 120
>> c) Metric
>
>> [!example] Group B
>> n) Protocol-specific value used as tie-breaker for identical ADs.
>> o) Administrative Distance of directly connected interfaces.
>> p) Administrative Distance of RIP protocol.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) BGP Open
>> b) Gigabit Bottleneck
>> c) EtherType
>
>> [!example] Group B
>> n) Fast Ethernet and Gigabit interfaces having same cost of 1.
>> o) Header field that identifies the Layer 3 protocol engine.
>> p) Message type negotiating peer session parameters.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) LPM Algorithm
>> b) auto-cost reference-bandwidth 10000
>> c) Invalid Timer
>
>> [!example] Group B
>> n) RIP timer (180s) that marks un-updated route as metric 16.
>> o) Cisco command to set reference bandwidth to 10 Gbps.
>> p) Longest Prefix Match used to find the most specific route.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Poison Reverse
>> b) Hello Packet
>> c) ABR
>
>> [!example] Group B
>> n) Multicast packet used by OSPF for neighbor discovery.
>> o) Loop prevention advertising failed route as hop count 16.
>> p) Area Boundary Router connecting regular areas to Area 0.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) OSPF Cost
>> b) Bellman-Ford
>> c) LSDB
>
>> [!example] Group B
>> n) Algorithmic foundation of distance-vector routing.
>> o) Link-State Database containing the complete topological map.
>> p) Metric calculated as Reference Bandwidth / Bandwidth.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Poison Reverse
>> b) BGP Keepalive
>> c) Hello Packet
>
>> [!example] Group B
>> n) Message type confirming peer status when no updates are sent.
>> o) Multicast packet used by OSPF for neighbor discovery.
>> p) Loop prevention advertising failed route as hop count 16.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) RIPv1
>> b) EtherType
>> c) ICMP Type 11 Code 0
>
>> [!example] Group B
>> n) Classful protocol broadcasting updates to 255.255.255.255.
>> o) Message sent when a packet's TTL expires in transit.
>> p) Header field that identifies the Layer 3 protocol engine.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TCP Port 179
>> b) RIPv2
>> c) AD of 1
>
>> [!example] Group B
>> n) Reliable connection port used for BGP peer sessions.
>> o) Administrative Distance of static routes.
>> p) Classless protocol multicasting updates to 224.0.0.9.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
