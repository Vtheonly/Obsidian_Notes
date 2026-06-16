---
sources:
  - "[[05.00 Introduction]]"
  - "[[05.01 Route Entries & Administrative Distance]]"
  - "[[05.02 Static Routing Mechanics]]"
  - "[[05.03 Distance-Vector Routing (RIPv2)]]"
  - "[[05.04 RIP Route Table Update Logic]]"
  - "[[05.05 Link-State Routing (OSPF & Dijkstra's Algorithm)]]"
---

> [!question] The Administrative Distance of a directly connected route is 0.
>> [!success]- Answer
>> True

> [!question] The Administrative Distance of a static route is 1.
>> [!success]- Answer
>> True

> [!question] The default Administrative Distance of RIP is lower than that of OSPF.
>> [!success]- Answer
>> False

> [!question] When forwarding a packet, the router selects the route that matches the destination IP address with the longest prefix length.
>> [!success]- Answer
>> True

> [!question] A directly attached static route uses the IP address of the next-hop router interface.
>> [!success]- Answer
>> False

> [!question] A default static route matches all destinations that do not have a specific route entry in the routing table.
>> [!success]- Answer
>> True

> [!question] RIPv2 is a classful routing protocol and does not support VLSM.
>> [!success]- Answer
>> False

> [!question] The maximum hop count metric value for RIPv2 is 15.
>> [!success]- Answer
>> True

> [!question] The passive-interface command prevents RIP from transmitting periodic updates out of the specified interface but still allows it to advertise that interface's subnet.
>> [!success]- Answer
>> True

> [!question] When running OSPF, routers build a complete topological map of the network known as the Link-State Database.
>> [!success]- Answer
>> True

> [!question] What is the default Administrative Distance of OSPF?
> a) 120
> b) 90
> c) 100
> d) 110
>> [!success]- Answer
>> d) 110

> [!question] Which destination network and subnet mask representation denotes a default static route?
> a) 192.168.1.0 255.255.255.0
> b) 127.0.0.1 255.0.0.0
> c) 0.0.0.0 0.0.0.0
> d) 255.255.255.255 255.255.255.255
>> [!success]- Answer
>> c) 0.0.0.0 0.0.0.0

> [!question] What is the multicast address used by RIPv2 to transmit periodic routing updates?
> a) 224.0.0.10
> b) 224.0.0.6
> c) 224.0.0.9
> d) 224.0.0.5
>> [!success]- Answer
>> c) 224.0.0.9

> [!question] What metric does the Routing Information Protocol (RIP) use to measure path distance?
> a) Bandwidth
> b) Link delay
> c) Link cost
> d) Hop count
>> [!success]- Answer
>> d) Hop count

> [!question] Which Cisco IOS command disables classful automatic summarization under the RIP process?
> a) passive-interface
> b) version 2
> c) no auto-summary
> d) no summary
>> [!success]- Answer
>> c) no auto-summary

> [!question] What is the default Administrative Distance of RIP?
> a) 110
> b) 120
> c) 1
> d) 90
>> [!success]- Answer
>> b) 120

> [!question] Under Dijkstra's algorithm, what does the Permanent (P) set represent?
> a) Blocked exit interfaces
> b) Confirmed shortest paths
> c) Tentative paths under evaluation
> d) Unreachable destinations
>> [!success]- Answer
>> b) Confirmed shortest paths

> [!question] If a RIP router receives an update for an existing subnet with a higher metric from the SAME neighbor that advertised it, what action is taken?
> a) Overwrites the existing route with the new metric
> b) Decrements the incoming metric by 1
> c) Discards the incoming update
> d) Places the update in a hold-down state
>> [!success]- Answer
>> a) Overwrites the existing route with the new metric

> [!question] In OSPF, what is the database name where all routers in the same area maintain identical topological map information?
> a) Link-State Database (LSDB)
> b) Neighbor Adjacency Table
> c) Routing Information Base (RIB)
> d) Distance-Vector Table
>> [!success]- Answer
>> a) Link-State Database (LSDB)

> [!question] Which command prevents a RIP router from transmitting updates on FastEthernet 0/0 while still advertising its subnet?
> a) passive fastethernet 0/0
> b) ip rip passive fastethernet 0/0
> c) passive-interface fastethernet 0/0
> d) no routing-update fastethernet 0/0
>> [!success]- Answer
>> c) passive-interface fastethernet 0/0

> [!question] Match the routing protocol or route source with its default Administrative Distance.
>> [!example] Group A
>> a) Directly Connected
>> b) Static Route
>> c) RIP
>
>> [!example] Group B
>> n) 120
>> o) 0
>> p) 1
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the static route type with its corresponding Cisco IOS configuration command.
>> [!example] Group A
>> a) Next-hop route
>> b) Directly attached route
>> c) Default route
>
>> [!example] Group B
>> n) ip route 0.0.0.0 0.0.0.0 209.165.202.129
>> o) ip route 192.168.2.0 255.255.255.0 serial 0/0/0
>> p) ip route 192.168.2.0 255.255.255.0 10.10.10.2
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the RIP route table update logic case with the correct action taken by the receiving router.
>> [!example] Group A
>> a) New Route
>> b) Better Metric
>> c) Same Next Hop
>
>> [!example] Group B
>> n) Always overwrite existing route with the new metric
>> o) Install the new route in the routing table
>> p) Replace the existing route with the lower metric
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the OSPF Dijkstra candidate list with its role in the shortest path computation.
>> [!example] Group A
>> a) Tentative (T)
>> b) Permanent (P)
>> c) Path Cost
>
>> [!example] Group B
>> n) Confirmed shortest paths
>> o) Unconfirmed paths under evaluation
>> p) Accumulated cost of links along the path
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the routing table term with its operational definition.
>> [!example] Group A
>> a) Administrative Distance
>> b) Longest Prefix Matching
>> c) Routing Metric
>
>> [!example] Group B
>> n) Selects the route with the longest prefix length
>> o) Value representing path desirability or cost
>> p) Trustworthiness of a route source
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the OSPF Dijkstra algorithm step from Node F with its calculated path.
>> [!example] Group A
>> a) Shortest path to C
>> b) Shortest path to E
>> c) Shortest path to B
>
>> [!example] Group B
>> n) F -> E -> B
>> o) F -> C
>> p) F -> E
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the RIPv2 configuration command with the feature it enables or configures.
>> [!example] Group A
>> a) passive-interface
>> b) no auto-summary
>> c) version 2
>
>> [!example] Group B
>> n) Enforces version 2 (required for VLSM)
>> o) Prevents periodic routing updates out of interface
>> p) Disables classful automatic summarization
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the routing table entry component with its description.
>> [!example] Group A
>> a) AD
>> b) Metric
>> c) Next-Hop
>
>> [!example] Group B
>> n) IP address of the next-hop router interface
>> o) Cost value to reach the destination network
>> p) Trustworthiness score of the route source
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the RIP incoming metric behavior with the correct resulting metric.
>> [!example] Group A
>> a) Original metric in update is 3
>> b) Original metric in update is 2
>> c) Original metric in update is 4
>
>> [!example] Group B
>> n) Incremented metric becomes 5
>> o) Incremented metric becomes 4
>> p) Incremented metric becomes 3
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the network destination type with its address/prefix representation.
>> [!example] Group A
>> a) Default Route
>> b) Host Route
>> c) Class C Network
>
>> [!example] Group B
>> n) 192.168.1.0/24
>> o) 0.0.0.0/0
>> p) 192.168.1.5/32
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
