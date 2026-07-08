---
title: "Quiz 05 — IP Routing"
type: quiz
chapter: 05
sources:
  - "[[07 - IP Routing/07.01 Routing Table Structure]]"
  - "[[07 - IP Routing/07.02 Administrative Distance & Metrics]]"
  - "[[07 - IP Routing/07.03 Longest Prefix Match]]"
  - "[[07 - IP Routing/07.04 Static Routing]]"
  - "[[07 - IP Routing/07.05 Router Operations & Packet Processing]]"
  - "[[07 - IP Routing/07.06 Route Aggregation]]"
  - "[[07 - IP Routing/07.07 Static vs Dynamic Routing]]"
  - "[[08 - Routing Protocols/08.01 Distance-Vector - RIP]]"
  - "[[08 - Routing Protocols/08.03 RIP Update Logic]]"
  - "[[08 - Routing Protocols/08.07 Dijkstra Algorithm Walkthrough]]"
tags: [quiz, routing, rip, ospf]
---

#  Quiz 05 — IP Routing

> [!abstract] Test Your Knowledge
> This quiz covers routing tables, Administrative Distance, Longest Prefix Match, static routing, and RIP basics. Answer each question before revealing the answer.

---

## Part 1 — True / False

> [!question] The Administrative Distance of a directly connected route is 0.
>> [!success]- Answer
>> **True.** Directly connected routes have AD = 0, the most trusted.

> [!question] The Administrative Distance of a static route is 1.
>> [!success]- Answer
>> **True.**

> [!question] The default Administrative Distance of RIP is lower than that of OSPF.
>> [!success]- Answer
>> **False.** RIP AD = 120; OSPF AD = 110. Lower = more trusted, so OSPF wins.

> [!question] When forwarding a packet, the router selects the route that matches the destination IP address with the longest prefix length.
>> [!success]- Answer
>> **True.** Longest Prefix Match (LPM) is the universal lookup rule.

> [!question] A directly attached static route uses the IP address of the next-hop router interface.
>> [!success]- Answer
>> **False.** A directly attached static route uses the local exit interface (e.g., `serial 0/0/0`). Next-hop IP would be a next-hop route.

> [!question] A default static route matches all destinations that do not have a specific route entry in the routing table.
>> [!success]- Answer
>> **True.** The default route `0.0.0.0/0` is the catch-all.

> [!question] RIPv2 is a classful routing protocol and does not support VLSM.
>> [!success]- Answer
>> **False.** RIPv2 is classless and supports VLSM. RIPv1 is classful.

> [!question] The maximum hop count metric value for RIPv2 is 15.
>> [!success]- Answer
>> **True.** 15 is reachable; 16 means "infinity" (unreachable).

> [!question] The passive-interface command prevents RIP from transmitting periodic updates out of the specified interface but still allows it to advertise that interface's subnet.
>> [!success]- Answer
>> **True.** This is exactly the purpose of `passive-interface`.

> [!question] When running OSPF, routers build a complete topological map of the network known as the Link-State Database.
>> [!success]- Answer
>> **True.** The LSDB is identical on all routers in the same area.

> [!question] Directly attached static routes require recursive lookup of the next-hop IP address.
>> [!success]- Answer
>> **False.** Directly attached routes specify the exit interface directly, so no recursion is needed. Next-hop routes do require recursive lookup.

> [!question] RIPv2 broadcasts routing updates to 255.255.255.255.
>> [!success]- Answer
>> **False.** RIPv2 multicasts to `224.0.0.9`. RIPv1 broadcasts to `255.255.255.255`.

> [!question] If a RIP router receives a worse metric update for an existing route from a different neighbor, it overwrites the route.
>> [!success]- Answer
>> **False.** It discards the update. Only if the same neighbor (next-hop) sends the worse metric does it overwrite.

> [!question] Dijkstra's algorithm constructs a Shortest Path Tree (SPT) with the calculating node as the root.
>> [!success]- Answer
>> **True.** Every router computes its own SPT rooted at itself.

> [!question] A static route next-hop configured with an exit interface is referred to as a directly attached route.
>> [!success]- Answer
>> **True.** Specifying the exit interface makes it "directly attached."

---

## Part 2 — Multiple Choice

> [!question] What is the default Administrative Distance of OSPF?
> a) 120
> b) 90
> c) 100
> d) 110
>> [!success]- Answer
>> **d) 110**

> [!question] Which destination network and subnet mask representation denotes a default static route?
> a) 192.168.1.0 255.255.255.0
> b) 127.0.0.1 255.0.0.0
> c) 0.0.0.0 0.0.0.0
> d) 255.255.255.255 255.255.255.255
>> [!success]- Answer
>> **c) 0.0.0.0 0.0.0.0**

> [!question] What is the multicast address used by RIPv2 to transmit periodic routing updates?
> a) 224.0.0.10
> b) 224.0.0.6
> c) 224.0.0.9
> d) 224.0.0.5
>> [!success]- Answer
>> **c) 224.0.0.9** (224.0.0.5 is OSPF all-routers; 224.0.0.10 is EIGRP)

> [!question] What metric does the Routing Information Protocol (RIP) use to measure path distance?
> a) Bandwidth
> b) Link delay
> c) Link cost
> d) Hop count
>> [!success]- Answer
>> **d) Hop count**

> [!question] Which Cisco IOS command disables classful automatic summarization under the RIP process?
> a) passive-interface
> b) version 2
> c) no auto-summary
> d) no summary
>> [!success]- Answer
>> **c) no auto-summary**

> [!question] What is the default Administrative Distance of RIP?
> a) 110
> b) 120
> c) 1
> d) 90
>> [!success]- Answer
>> **b) 120**

> [!question] Under Dijkstra's algorithm, what does the Permanent (P) set represent?
> a) Blocked exit interfaces
> b) Confirmed shortest paths
> c) Tentative paths under evaluation
> d) Unreachable destinations
>> [!success]- Answer
>> **b) Confirmed shortest paths**

> [!question] If a RIP router receives an update for an existing subnet with a higher metric from the SAME neighbor that advertised it, what action is taken?
> a) Overwrites the existing route with the new metric
> b) Decrements the incoming metric by 1
> c) Discards the incoming update
> d) Places the update in a hold-down state
>> [!success]- Answer
>> **a) Overwrites the existing route with the new metric** — this is the "same neighbor" rule.

> [!question] In OSPF, what is the database name where all routers in the same area maintain identical topological map information?
> a) Link-State Database (LSDB)
> b) Neighbor Adjacency Table
> c) Routing Information Base (RIB)
> d) Distance-Vector Table
>> [!success]- Answer
>> **a) Link-State Database (LSDB)**

> [!question] Which command prevents a RIP router from transmitting updates on FastEthernet 0/0 while still advertising its subnet?
> a) passive fastethernet 0/0
> b) ip rip passive fastethernet 0/0
> c) passive-interface fastethernet 0/0
> d) no routing-update fastethernet 0/0
>> [!success]- Answer
>> **c) passive-interface fastethernet 0/0**

> [!question] If a router learns paths to the same subnet from OSPF (AD 110) and RIP (AD 120), which path will be installed in the routing table?
> a) Neither path
> b) Both paths (multipath forwarding)
> c) The OSPF path
> d) The RIP path
>> [!success]- Answer
>> **c) The OSPF path** — lower AD wins.

> [!question] What is the RIPv2 metric value that represents an unreachable destination (infinity)?
> a) 16
> b) 100
> c) 15
> d) 255
>> [!success]- Answer
>> **a) 16**

> [!question] Which algorithm is run locally by OSPF routers to compute the shortest-path tree?
> a) Kruskal's algorithm
> b) Dijkstra's algorithm
> c) Floyd-Warshall algorithm
> d) Bellman-Ford algorithm
>> [!success]- Answer
>> **b) Dijkstra's algorithm**

> [!question] Which Cisco IOS command correctly configures a static default route using next-hop IP 192.168.1.1?
> a) ip route 0.0.0.0 0.0.0.0 192.168.1.1
> b) route static 0.0.0.0 0.0.0.0 192.168.1.1
> c) ip default-route 192.168.1.1
> d) ip route default 192.168.1.1
>> [!success]- Answer
>> **a) ip route 0.0.0.0 0.0.0.0 192.168.1.1**

> [!question] Which component of a routing table entry measures the reliability or trustworthiness of the routing source?
> a) Next-Hop IP
> b) Local Exit Interface
> c) Metric
> d) Administrative Distance
>> [!success]- Answer
>> **d) Administrative Distance**

> [!question] What is the first step when a RIP router processes a routing update from a neighbor?
> a) Increment the metric of all incoming route entries by 1
> b) Broadcast the update to all other neighbors
> c) Compare each entry to the current routing table
> d) Overwrite the entire routing table
>> [!success]- Answer
>> **a) Increment the metric of all incoming route entries by 1**

> [!question] In the Dijkstra walkthrough from Node F, which node has the lowest path cost from F?
> a) Node D
> b) Node C
> c) Node B
> d) Node E
>> [!success]- Answer
>> **b) Node C** (cost 1)

> [!question] What is the default Administrative Distance of a static route?
> a) 1
> b) 0
> c) 120
> d) 110
>> [!success]- Answer
>> **a) 1**

> [!question] If a router is using longest prefix matching, which route will it select to forward a packet destined to 172.16.128.5?
> a) 0.0.0.0/0
> b) 172.0.0.0/8
> c) 172.16.128.0/17
> d) 172.16.0.0/16
>> [!success]- Answer
>> **c) 172.16.128.0/17** — longest prefix wins.

> [!question] What is the default OSPF cost assigned to a Gigabit Ethernet interface under the default reference bandwidth?
> a) 0
> b) 100
> c) 1
> d) 10
>> [!success]- Answer
>> **c) 1** — the gigabit bottleneck.

---

## Part 3 — Matching

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
>> a) → o) (0)
>> b) → p) (1)
>> c) → n) (120)

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
>> a) → p) (uses next-hop IP)
>> b) → o) (uses exit interface)
>> c) → n) (matches everything)

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
>> a) → o) (install new)
>> b) → p) (replace with better)
>> c) → n) (always overwrite, even if worse)

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
>> a) → o) (tentative = under evaluation)
>> b) → n) (permanent = confirmed)
>> c) → p) (accumulated cost)

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
>> a) → p) (AD = trustworthiness)
>> b) → n) (LPM = longest prefix)
>> c) → o) (metric = path cost)

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
>> a) → o)
>> b) → p)
>> c) → n)

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
>> a) → p)
>> b) → o)
>> c) → n)

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
>> a) → o) (matches everything)
>> b) → p) (single host, /32)
>> c) → n) (class C /24)

> [!question] Match the routing protocol with its operational classification.
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
>> a) → o)
>> b) → n)
>> c) → p)

> [!question] Match the Dijkstra path from Node F to its target with the path cost (referencing the [[08 - Routing Protocols/08.07 Dijkstra Algorithm Walkthrough|walkthrough]]).
>> [!example] Group A
>> a) Path F → C
>> b) Path F → E
>> c) Path F → C → D
>
>> [!example] Group B
>> n) Cost 3
>> o) Cost 1
>> p) Cost 2
>
>> [!success]- Answer
>> a) → o) (F → C is cost 1)
>> b) → p) (F → E is cost 2)
>> c) → n) (F → C → D is cost 1+2=3)

---

##  Score Interpretation

- **0–17 correct (≤ 50%):** Study the chapter again, especially [[07 - IP Routing/07.02 Administrative Distance & Metrics|AD]] and [[08 - Routing Protocols/08.03 RIP Update Logic|RIP Update Logic]].
- **18–25 (50–75%):** Decent foundation. Review the missed questions' source notes.
- **26–32 (75–95%):** Strong. Ready to move on.
- **33+ (> 95%):** Excellent. Try [[Quizzes/Quiz 07 - Routing Protocols|Quiz 07]] next.
