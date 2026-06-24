---
sources:
  - "[[05.00 Introduction]]"
  - "[[05.01 Route Entries & Administrative Distance]]"
  - "[[05.02 Static Routing Mechanics]]"
  - "[[05.03 Distance-Vector Routing (RIPv2)]]"
  - "[[05.04 RIP Route Table Update Logic]]"
  - "[[05.05 Link-State Routing (OSPF & Dijkstra's Algorithm)]]"
---

> [!question] Open Shortest Path First (OSPF) is a distance-vector routing protocol.
>> [!success]- Answer
>> False

> [!question] Under Dijkstra's algorithm, if a shorter path to a tentative node is discovered, its cost and next-hop in the tentative list are updated.
>> [!success]- Answer
>> True

> [!question] Directly attached static routes require both a local exit interface and the next-hop router's IP address.
>> [!success]- Answer
>> False

> [!question] OSPF routers build a complete topological map of the network area locally before calculating routes.
>> [!success]- Answer
>> True

> [!question] Routing Information Protocol (RIP) updates are transmitted periodically every 30 seconds.
>> [!success]- Answer
>> True

> [!question] Disabling classful auto-summarization is required for RIPv2 to support VLSM and classless routing.
>> [!success]- Answer
>> True

> [!question] The passive-interface command suppresses all routing updates on an interface and prevents advertising its subnet to neighbors.
>> [!success]- Answer
>> False

> [!question] A routing source with an administrative distance of 120 is more trusted than one with an administrative distance of 110.
>> [!success]- Answer
>> False

> [!question] If a RIP update for a known subnet with a worse metric is received from a different neighbor, it is discarded.
>> [!success]- Answer
>> True

> [!question] In Dijkstra's algorithm, paths in the Tentative list (T) are confirmed shortest paths.
>> [!success]- Answer
>> False

> [!question] If a router learns paths to the same subnet from OSPF (AD 110) and RIP (AD 120), which path will be installed in the routing table?
> a) Neither path
> b) Both paths (multipath forwarding)
> c) The OSPF path
> d) The RIP path
>> [!success]- Answer
>> c) The OSPF path

> [!question] What is the RIPv2 metric value that represents an unreachable destination (infinity)?
> a) 16
> b) 100
> c) 15
> d) 255
>> [!success]- Answer
>> a) 16

> [!question] Which algorithm is run locally by OSPF routers to compute the shortest-path tree?
> a) Kruskal's algorithm
> b) Dijkstra's algorithm
> c) Floyd-Warshall algorithm
> d) Bellman-Ford algorithm
>> [!success]- Answer
>> b) Dijkstra's algorithm

> [!question] Which Cisco IOS command correctly configures a static default route using next-hop IP 192.168.1.1?
> a) ip route 0.0.0.0 0.0.0.0 192.168.1.1
> b) route static 0.0.0.0 0.0.0.0 192.168.1.1
> c) ip default-route 192.168.1.1
> d) ip route default 192.168.1.1
>> [!success]- Answer
>> a) ip route 0.0.0.0 0.0.0.0 192.168.1.1

> [!question] Which component of a routing table entry measures the reliability or trustworthiness of the routing source?
> a) Next-Hop IP
> b) Local Exit Interface
> c) Metric
> d) Administrative Distance
>> [!success]- Answer
>> d) Administrative Distance

> [!question] RIPv2 periodic updates are transmitted to which destination address?
> a) 224.0.0.9
> b) 224.0.0.5
> c) 224.0.0.6
> d) 224.0.0.1
>> [!success]- Answer
>> a) 224.0.0.9

> [!question] In Dijkstra's algorithm, what does the Tentative (T) candidate list contain?
> a) Routes with a metric of 16
> b) Confirmed shortest paths
> c) Unconfirmed paths under evaluation
> d) Downed interfaces
>> [!success]- Answer
>> c) Unconfirmed paths under evaluation

> [!question] What does a RIP router do if it receives a worse metric update for an existing subnet from a different neighbor?
> a) Discards the update
> b) Enters a hold-down state
> c) Overwrites the route with the worse metric
> d) Forwards the update to other neighbors
>> [!success]- Answer
>> a) Discards the update

> [!question] Which of the following routing protocols is classified as link-state?
> a) OSPF
> b) IGRP
> c) RIPv2
> d) RIPv1
>> [!success]- Answer
>> a) OSPF

> [!question] In the Node F Dijkstra walkthrough, what is the next-hop interface/node choice for Node A?
> a) Direct Interface to B
> b) Direct Interface to D
> c) Direct Interface to E
> d) Direct Interface to C
>> [!success]- Answer
>> c) Direct Interface to E

> [!question] Match the routing table entry field with its purpose.
>> [!example] Group A
>> a) DP
>> b) NH
>> c) ADM
>
>> [!example] Group B
>> n) Displays the next-hop IP address
>> o) Destination network prefix and length
>> p) Administrative distance and metric bracket
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the IP Routing Architecture section file with its corresponding topic.
>> [!example] Group A
>> a) 05.01
>> b) 05.02
>> c) 05.05
>
>> [!example] Group B
>> n) Link-State Routing (OSPF & Dijkstra's Algorithm)
>> o) Route Entries & Administrative Distance
>> p) Static Routing Mechanics
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the RIP route update logic step with the resulting metric.
>> [!example] Group A
>> a) Incoming metric is 2, processed through step 1
>> b) Incoming metric is 3, processed through step 1
>> c) Incoming metric is 1, processed through step 1
>
>> [!example] Group B
>> n) Metric 3
>> o) Metric 4
>> p) Metric 2
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the routing protocol type with its operational classification.
>> [!example] Group A
>> a) RIPv2
>> b) OSPF
>> c) Static Route
>
>> [!example] Group B
>> n) Link-state routing protocol
>> o) Classless distance-vector routing protocol
>> p) Manually configured routing path
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Dijkstra algorithm node from F with its permanent confirmation step in the walkthrough.
>> [!example] Group A
>> a) Node C confirmed
>> b) Node E confirmed
>> c) Node B confirmed
>
>> [!example] Group B
>> n) Step 2 (lowest cost in T is 1)
>> o) Step 4 (tied cost is 3)
>> p) Step 3 (lowest cost in T is 2)
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the Cisco IOS command with its routing configuration role.
>> [!example] Group A
>> a) router rip
>> b) network 10.0.0.0
>> c) passive-interface fastethernet 0/0
>
>> [!example] Group B
>> n) Enables the RIP routing process
>> o) Associates classful network 10.0.0.0 with the RIP process
>> p) Suppresses periodic outgoing routing updates on FastEthernet 0/0
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the routing prefix type with its description.
>> [!example] Group A
>> a) Host Route
>> b) Default Route
>> c) Longest Prefix Matching
>
>> [!example] Group B
>> n) Route matching a single IP address with a /32 mask
>> o) Route matching 0.0.0.0/0
>> p) Lookup rule selecting the most specific match
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the routing source with its default Administrative Distance (AD).
>> [!example] Group A
>> a) OSPF
>> b) RIP
>> c) Static Route
>
>> [!example] Group B
>> n) 1
>> o) 110
>> p) 120
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the RIP Route Update Logic case with its respective decision.
>> [!example] Group A
>> a) Worse metric (different neighbor)
>> b) Better metric (any neighbor)
>> c) Same next hop (worse metric)
>
>> [!example] Group B
>> n) Replace the route with the lower metric
>> o) Discard the update
>> p) Overwrite the route with the higher metric
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the Dijkstra path from Node F to its target with the path cost.
>> [!example] Group A
>> a) Path F -> C
>> b) Path F -> E
>> c) Path F -> C -> D
>
>> [!example] Group B
>> n) Cost 3
>> o) Cost 1
>> p) Cost 2
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
