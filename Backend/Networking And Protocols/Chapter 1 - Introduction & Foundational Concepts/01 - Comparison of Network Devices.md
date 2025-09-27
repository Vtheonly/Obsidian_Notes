# Comparison of Network Devices

## Corrected Context

This note provides a high-level comparison of fundamental networking devices. Understanding their distinct roles in handling data is crucial for comprehending how networks are built, from a simple home setup to the global internet.

---

## Comparison Table

| Device                     | Primary Function                                   | Key Technology / Method                                  | Intelligence Level |
| -------------------------- | -------------------------------------------------- | -------------------------------------------------------- | ------------------ |
| **[[02 - Modem|Modem]]**              | Interface with the Internet Service Provider (ISP) | Modulates/Demodulates ISP signal (Cable, Fiber, DSL)     | Specialized      |
| **[[03 - Repeater|Repeater]]**           | Regenerate a weak signal over a long distance      | Signal amplification and re-transmission                 | Unintelligent    |
| **[[04 - Network Hub|Network Hub]]**        | Connect multiple devices in a simple LAN           | Broadcasts all data to every port (Multi-port Repeater)  | Unintelligent    |
| **[[05 - Network Bridge|Network Bridge]]**     | Segment a network to reduce traffic                | Learns which hosts are on its two ports, contains traffic  | Basic            |
| **[[06 - Network Switch|Network Switch]]**     | Intelligently connect devices in a LAN             | Forwards data to specific ports using a **MAC Address Table** | Intelligent      |
| **[[07 - Router|Router]]**             | Connect two or more different networks             | Forwards data between networks using **IP Addresses**    | Highly Intelligent |
| **[[08 - Wireless Access Point (AP)|Wireless Access Point (AP)]]** | Provide wireless network access                  | Transmits data over radio waves (Wi-Fi)                | Intelligent      |

---

> [!Note] Modern Combination Devices
> Most "wireless routers" sold for home use are actually **combination devices**. They typically integrate a **router**, a **multi-port switch**, and a **wireless access point** into a single plastic box. Some even include a built-in **modem**.