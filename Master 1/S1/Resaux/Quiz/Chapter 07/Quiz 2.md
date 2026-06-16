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

> [!question] BGP is a path-vector routing protocol used for inter-domain routing.
>> [!success]- Answer
>> True

> [!question] An ASBR connects OSPF to external networks or static routes.
>> [!success]- Answer
>> True

> [!question] In OSPF, neighbor discovery is performed using multicast Hello packets.
>> [!success]- Answer
>> True

> [!question] BGP neighbors establish a TCP connection over port 179.
>> [!success]- Answer
>> True

> [!question] BGP loop prevention relies on checking if the local ASN is present in the AS_PATH attribute.
>> [!success]- Answer
>> True

> [!question] During L2 re-encapsulation, the source MAC address is set to the MAC of the router's exit interface.
>> [!success]- Answer
>> True

> [!question] The default reference bandwidth for OSPF metric calculation is 100 Mbps.
>> [!success]- Answer
>> True

> [!question] Prefix length /28 is more specific than prefix length /24.
>> [!success]- Answer
>> True

> [!question] CRC/FCS failures cause frames to be dropped immediately.
>> [!success]- Answer
>> True

> [!question] Autonomous Systems are managed by a single administrative authority.
>> [!success]- Answer
>> True

> [!question] Which area in a multi-area OSPF design is the backbone area?
> a) Area 1.1.1.1
> b) The non-backbone area
> c) Area 0.0.0.0
> d) The stub area
>> [!success]- Answer
>> c) Area 0.0.0.0

> [!question] What type of updates does RIPv1 use?
> a) Broadcast updates to 255.255.255.255
> b) Unicast updates to neighbors
> c) Path-vector updates
> d) Multicast updates to 224.0.0.9
>> [!success]- Answer
>> a) Broadcast updates to 255.255.255.255

> [!question] What message is sent when a BGP protocol error occurs, immediately closing the peer connection?
> a) Update
> b) Keepalive
> c) Open
> d) Notification
>> [!success]- Answer
>> d) Notification

> [!question] Which multicast IP address is used by RIPv2 for periodic routing updates?
> a) 255.255.255.255
> b) 224.0.0.9
> c) 224.0.0.5
> d) 224.0.0.6
>> [!success]- Answer
>> b) 224.0.0.9

> [!question] Over which TCP port do BGP neighbors establish peer sessions?
> a) Port 443
> b) Port 80
> c) Port 22
> d) Port 179
>> [!success]- Answer
>> d) Port 179

> [!question] How is OSPF cost metric calculated?
> a) Administrative Distance / Link Speed
> b) Reference Bandwidth / Interface Bandwidth
> c) Hop Count to Destination
> d) Path Bandwidth * Delay
>> [!success]- Answer
>> b) Reference Bandwidth / Interface Bandwidth

> [!question] Which routing protocol has a default Administrative Distance of 110?
> a) EIGRP
> b) RIPv2
> c) BGP
> d) OSPF
>> [!success]- Answer
>> d) OSPF

> [!question] What OSPF router role connects a regular area to the backbone area?
> a) Internal Router (IR)
> b) Autonomous System Boundary Router (ASBR)
> c) Area Boundary Router (ABR)
> d) Backbone Router (BR)
>> [!success]- Answer
>> c) Area Boundary Router (ABR)

> [!question] What reference bandwidth value is used by default in Cisco IOS OSPF cost calculations?
> a) 10^9 bps (1 Gbps)
> b) 10^8 bps (100 Mbps)
> c) 10^10 bps (10 Gbps)
> d) 10^7 bps (10 Mbps)
>> [!success]- Answer
>> b) 10^8 bps (100 Mbps)

> [!question] Which mechanism prevents a router from advertising a route out the same interface it was learned from?
> a) Hold-down Timers
> b) Loop Prevention Vector
> c) Poison Reverse
> d) Split Horizon
>> [!success]- Answer
>> d) Split Horizon

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Invalid Timer
>> b) OSPF Cost
>> c) ABR
>
>> [!example] Group B
>> n) RIP timer (180s) that marks un-updated route as metric 16.
>> o) Metric calculated as Reference Bandwidth / Bandwidth.
>> p) Area Boundary Router connecting regular areas to Area 0.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ICMP Type 11 Code 0
>> b) LPM Algorithm
>> c) Gigabit Bottleneck
>
>> [!example] Group B
>> n) Message sent when a packet's TTL expires in transit.
>> o) Longest Prefix Match used to find the most specific route.
>> p) Fast Ethernet and Gigabit interfaces having same cost of 1.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) RIPv1
>> b) CRC / FCS
>> c) Reference Bandwidth
>
>> [!example] Group B
>> n) Trailer check used to detect incoming frame corruption.
>> o) Classful protocol broadcasting updates to 255.255.255.255.
>> p) Default 100 Mbps value used for OSPF metric calculation.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TCP Port 179
>> b) ICMP Type 11 Code 0
>> c) Autonomous System
>
>> [!example] Group B
>> n) Reliable connection port used for BGP peer sessions.
>> o) Message sent when a packet's TTL expires in transit.
>> p) Network under single admin with unified routing policy.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) TTL
>> b) LSDB
>> c) BGP Open
>
>> [!example] Group B
>> n) Message type negotiating peer session parameters.
>> o) Link-State Database containing the complete topological map.
>> p) Time to Live field decremented by routers to prevent loops.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) LSA
>> b) Hello Packet
>> c) AD of 110
>
>> [!example] Group B
>> n) Link-State Advertisement containing interface state and cost.
>> o) Administrative Distance of OSPF protocol.
>> p) Multicast packet used by OSPF for neighbor discovery.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) auto-cost reference-bandwidth 10000
>> b) Invalid Timer
>> c) TTL
>
>> [!example] Group B
>> n) Time to Live field decremented by routers to prevent loops.
>> o) Cisco command to set reference bandwidth to 10 Gbps.
>> p) RIP timer (180s) that marks un-updated route as metric 16.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) BGP Keepalive
>> b) OSPF Cost
>> c) AD of 90
>
>> [!example] Group B
>> n) Message type confirming peer status when no updates are sent.
>> o) Administrative Distance of EIGRP protocol.
>> p) Metric calculated as Reference Bandwidth / Bandwidth.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) BGP Update
>> b) ICMP Type 3 Code 0
>> c) AS_PATH
>
>> [!example] Group B
>> n) Message type advertising new routes or withdrawing inactive ones.
>> o) BGP attribute list of ASNs traversed by a route.
>> p) Message sent when destination network is unreachable.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Autonomous System
>> b) Dijkstra Algorithm
>> c) ABR
>
>> [!example] Group B
>> n) Area Boundary Router connecting regular areas to Area 0.
>> o) SPF calculation algorithm run locally by OSPF routers.
>> p) Network under single admin with unified routing policy.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
