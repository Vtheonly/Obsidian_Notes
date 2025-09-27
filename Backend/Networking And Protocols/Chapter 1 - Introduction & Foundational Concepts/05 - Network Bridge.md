
# Network Bridge

## Corrected Context

A **network bridge** is a device that connects two or more network segments, acting as a single network. It represents an evolutionary step between the unintelligent hub and the modern switch by introducing basic traffic filtering.

---

## How a Bridge Works

A bridge "learns" which devices (hosts) are on each of its network segments. Typically featuring two ports, it inspects incoming traffic and decides whether to forward it to the other segment.

> If a device on Segment A sends data to another device on Segment A, the bridge **contains** that traffic and does not forward it to Segment B. This reduces unnecessary traffic and prevents collisions between the segments.

By selectively forwarding packets only when necessary, bridges improve network efficiency compared to hubs.

---

## Key Points

*   Connects network segments
*   Has two main ports
*   Learns host locations (MAC addresses)
*   Contains local traffic
*   Reduces network collisions
*   Predecessor to the modern switch

