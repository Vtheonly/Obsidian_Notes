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

> [!question] Longest Prefix Match selects the route with the shortest prefix length.
>> [!success]- Answer
>> False

> [!question] The invalid timer in RIP is typically 60 seconds.
>> [!success]- Answer
>> False

> [!question] Dynamic routing consumes additional network bandwidth compared to static routing.
>> [!success]- Answer
>> True

> [!question] Distance-vector protocols have a complete topological map of the entire network.
>> [!success]- Answer
>> False

> [!question] LSAs in OSPF are flooded only within the area they originate from.
>> [!success]- Answer
>> True

> [!question] OSPF is a link-state routing protocol that uses Dijkstra's algorithm.
>> [!success]- Answer
>> True

> [!question] If dest MAC of incoming frame doesn't match the router's interface MAC, the router still processes the Layer 3 header.
>> [!success]- Answer
>> False

> [!question] The default Administrative Distance of OSPF is 120.
>> [!success]- Answer
>> False

> [!question] Connected interfaces have an Administrative Distance of 1.
>> [!success]- Answer
>> False

> [!question] IGPs are used to route traffic between different Autonomous Systems.
>> [!success]- Answer
>> False

> [!question] During packet forwarding, which MAC address is placed as the Source MAC of the new frame?
> a) The MAC of the router's egress exit interface
> b) The MAC of the receiving switch interface
> c) The MAC of the sending host
> d) The MAC of the next-hop router
>> [!success]- Answer
>> a) The MAC of the router's egress exit interface

> [!question] Which protocol maintains a synchronized Link-State Database (LSDB) on all routers within an area?
> a) BGP
> b) OSPF
> c) Static Routing
> d) RIPv2
>> [!success]- Answer
>> b) OSPF

> [!question] If a router receives a packet with a TTL of 1 destined for a remote network, what does it do?
> a) Drops the packet and sends ICMP Type 11
> b) Increments TTL by 1
> c) Decrements TTL to 0 and forwards it
> d) Forwards to default gateway
>> [!success]- Answer
>> a) Drops the packet and sends ICMP Type 11

> [!question] What is a key difference between RIPv1 and RIPv2?
> a) RIPv1 has a lower metric limit
> b) RIPv2 is link-state based
> c) RIPv2 uses Dijkstra's algorithm
> d) RIPv2 is classless and supports VLSM
>> [!success]- Answer
>> d) RIPv2 is classless and supports VLSM

> [!question] In the OSPF cost metric, what is the cost of a 10-Gbps interface if reference-bandwidth is set to 10000?
> a) 1
> b) 100
> c) 10
> d) 1000
>> [!success]- Answer
>> a) 1

> [!question] What hop count value represents an unreachable route in RIP?
> a) 16
> b) 15
> c) 0
> d) 255
>> [!success]- Answer
>> a) 16

> [!question] How long does the RIP hold-down timer lock a route after an unreachable update is received?
> a) 30 seconds
> b) 180 seconds
> c) 120 seconds
> d) 60 seconds
>> [!success]- Answer
>> d) 60 seconds

> [!question] Which BGP message type is used to withdraw inactive routes?
> a) Notification
> b) Update
> c) Open
> d) Keepalive
>> [!success]- Answer
>> b) Update

> [!question] What does an Internal Router (IR) in OSPF represent?
> a) A router connecting different areas
> b) A router on the network border
> c) A router with all interfaces in a single area
> d) A central backbone router
>> [!success]- Answer
>> c) A router with all interfaces in a single area

> [!question] What is the Longest Prefix Match rule used for?
> a) Selecting the route learned first
> b) Selecting the route with the lowest metric
> c) Selecting the route with the lowest AD
> d) Selecting the route with the most specific match
>> [!success]- Answer
>> d) Selecting the route with the most specific match

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ICMP Type 3 Code 4
>> b) ICMP Type 11 Code 0
>> c) Bellman-Ford
>
>> [!example] Group B
>> n) Algorithmic foundation of distance-vector routing.
>> o) Message sent when packet exceeds MTU and DF flag is 1.
>> p) Message sent when a packet's TTL expires in transit.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) OSPF Area 0
>> b) AD of 120
>> c) LSDB
>
>> [!example] Group B
>> n) Administrative Distance of RIP protocol.
>> o) Backbone area to which all regular areas must connect.
>> p) Link-State Database containing the complete topological map.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) BGP
>> b) BGP Notification
>> c) CRC / FCS
>
>> [!example] Group B
>> n) Message type reporting errors and closing peer session.
>> o) Path-vector Exterior Gateway Protocol connecting the Internet.
>> p) Trailer check used to detect incoming frame corruption.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ICMP Type 3 Code 0
>> b) AD of 1
>> c) EtherType
>
>> [!example] Group B
>> n) Message sent when destination network is unreachable.
>> o) Administrative Distance of static routes.
>> p) Header field that identifies the Layer 3 protocol engine.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ASBR
>> b) DF Flag
>> c) EtherType
>
>> [!example] Group B
>> n) Autonomous System Boundary Router importing external routes.
>> o) Don't Fragment flag that blocks packet splitting.
>> p) Header field that identifies the Layer 3 protocol engine.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ICMP Type 3 Code 4
>> b) CRC / FCS
>> c) ASBR
>
>> [!example] Group B
>> n) Trailer check used to detect incoming frame corruption.
>> o) Autonomous System Boundary Router importing external routes.
>> p) Message sent when packet exceeds MTU and DF flag is 1.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) BGP Loop Prevention
>> b) BGP
>> c) ASBR
>
>> [!example] Group B
>> n) Path-vector Exterior Gateway Protocol connecting the Internet.
>> o) Discarding update if local ASN is in AS_PATH list.
>> p) Autonomous System Boundary Router importing external routes.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) auto-cost reference-bandwidth 10000
>> b) Reference Bandwidth
>> c) BGP
>
>> [!example] Group B
>> n) Default 100 Mbps value used for OSPF metric calculation.
>> o) Cisco command to set reference bandwidth to 10 Gbps.
>> p) Path-vector Exterior Gateway Protocol connecting the Internet.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) BGP Update
>> b) Metric
>> c) Hold-Down Timer
>
>> [!example] Group B
>> n) Locks a route for 60 seconds to allow network convergence.
>> o) Message type advertising new routes or withdrawing inactive ones.
>> p) Protocol-specific value used as tie-breaker for identical ADs.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) BGP Loop Prevention
>> b) LSA
>> c) OSPF Area 0
>
>> [!example] Group B
>> n) Discarding update if local ASN is in AS_PATH list.
>> o) Link-State Advertisement containing interface state and cost.
>> p) Backbone area to which all regular areas must connect.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
