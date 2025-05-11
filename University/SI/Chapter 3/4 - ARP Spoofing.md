
# Network Attacks: ARP Poisoning (Slides 39-44)

This section details the Address Resolution Protocol (ARP) and the common network attack known as ARP Poisoning (or ARP Spoofing).

## ARP Protocol Principle (Slide 39)

*   **Definition:** ARP (Address Resolution Protocol) is a communication protocol used for discovering the **Link Layer address (e.g., MAC address)** associated with a given **Internet Layer address (e.g., IPv4 address)**.
*   **Purpose:** When a device needs to send a packet to another device on the *same local network* for which it knows the IP address but not the physical (MAC) address, it uses ARP to find the corresponding MAC address.
*   **Simplicity & Security:** ARP is a very simple protocol and crucially, it **does not implement any security measures**. It inherently trusts the ARP messages received on the network. This lack of authentication is what makes ARP Poisoning possible.

## ARP Principle: Request / Reply (Slide 40)

This illustrates the standard ARP process:

1.  **Scenario:** Host A (192.168.1.1, MAC aaaa:aaaa:aaaa) wants to send data to Host B (192.168.1.2) on the same local network, but Host A does not know Host B's MAC address.
2.  **ARP Request:** Host A broadcasts an **ARP Request** message onto the network. This message essentially asks, "Who has the IP address 192.168.1.2? Tell MAC address aaaa:aaaa:aaaa".
3.  **ARP Reply:** Host B (whose IP is 192.168.1.2 and MAC is bbbb:bbbb:bbbb) receives the broadcast request. It recognizes its own IP address and sends a unicast **ARP Reply** directly back to Host A. This reply essentially says, "192.168.1.2 is at MAC address bbbb:bbbb:bbbb".
4.  **ARP Cache Update:** Host A receives the ARP Reply and updates its **ARP cache** (also known as the ARP table) with the mapping: `192.168.1.2 -> bbbb:bbbb:bbbb`. Host A can now send its data directly to Host B's MAC address.
5.  **(Implicit Cache Update):** Host B might also update its cache with Host A's information (`192.168.1.1 -> aaaa:aaaa:aaaa`) based on the initial ARP Request. Other devices, like Host C or the router, might also cache these mappings if they see the ARP messages.

<!-- Placeholder for ARP Request/Reply Diagram -->
<!-- ![Diagram showing ARP Request broadcast from A, and ARP Reply unicast from B to A, with ARP tables](placeholder_diagram_arp_req_rep.png) -->

## ARP Principle: Gratuitous ARP (Reply) (Slide 41)

*   **Definition:** A Gratuitous ARP is an ARP message (usually an ARP Reply, but sometimes an ARP Request for its *own* IP) that is sent **without being requested**.
*   **Mechanism:** A host sends an ARP message containing its own IP and MAC address mapping to the entire network (broadcast).
*   **Legitimate Uses:**
    *   **Announce Presence/Update Caches:** When a device boots up or changes its IP/MAC address, it sends a Gratuitous ARP to inform all other devices on the network of its current mapping, allowing them to update their ARP caches proactively.
    *   **IP Conflict Detection:** Before using an IP address, a device might send a Gratuitous ARP for that IP. If another device replies claiming ownership, an IP conflict is detected.
*   **Slide Example:** Host A sends a Gratuitous ARP, announcing that 192.168.1.1 is at MAC aaaa:aaaa:aaaa. Devices like Host C and Host B receive this and update their ARP tables accordingly.

<!-- Placeholder for Gratuitous ARP Diagram -->
<!-- ![Diagram showing Host A broadcasting a Gratuitous ARP, updating Host C and B's tables](placeholder_diagram_arp_grat.png) -->

## ARP Poisoning (Slides 42-44)

*   **Definition (Slide 42):** ARP cache poisoning (also known as ARP spoofing) is a common attack against the ARP protocol.
*   **Goal:** Attackers **trick a victim** into accepting **falsified IP-to-MAC mappings** by sending malicious ARP messages.
*   **Consequence:** This can lead to the **redirection of the victim's network traffic** towards the attacker's machine (using the attacker's MAC address), enabling potential **Man-in-the-Middle (MitM)** attacks or Denial of Service.

### Principle (Slide 42)

*   An attacker machine **impersonates another machine at the physical layer (Layer 2)** within the same Local Area Network (LAN).
*   It aims to **poison the ARP cache of the target(s)**.
*   It **associates the attacker's MAC address (`@MAC=pirate`) with the IP address of another machine (`@ip src = machine spoofée`)**.

### Methods (Slide 42)

ARP Poisoning is typically achieved by sending unsolicited/forged ARP messages:

1.  **Sending an ARP Reply without a prior Request (Abusing Gratuitous ARP):** The attacker broadcasts ARP Replies claiming that a victim's IP address belongs to the attacker's MAC address.
2.  **Sending a Forged ARP Request:** The attacker can send an ARP Request where the *sender's* IP/MAC mapping is forged.
3.  **Sending a Forged ARP Reply:** Directly replying to a victim's legitimate ARP request with the attacker's MAC address instead of the correct one.
*   **Typical Malicious ARP Message Structure:** The attacker sends ARP messages where the source IP field contains the IP address of the machine they want to impersonate, and the source MAC field contains the attacker's own MAC address.

### Attack Illustration (Slide 43)

1.  **Attacker Action:** The Attacker (Host C, MAC cccc:cccc:cccc) sends forged ARP replies:
    *   To Host A: "ARP reply: 192.168.1.2 (Host B's IP) is at cccc:cccc:cccc (Attacker's MAC)"
    *   To Host B: "ARP reply: 192.168.1.1 (Host A's IP) is at cccc:cccc:cccc (Attacker's MAC)"
2.  **Cache Poisoning:**
    *   Host A updates its ARP table: `192.168.1.2 -> cccc:cccc:cccc` (Incorrect mapping)
    *   Host B updates its ARP table: `192.168.1.1 -> cccc:cccc:cccc` (Incorrect mapping)
    *   Host C's own ARP table might contain the correct mappings initially (or it doesn't matter for the attack).

<!-- Placeholder for ARP Poisoning Attack Diagram -->
<!-- ![Diagram showing Attacker C sending fake ARP replies to A and B, poisoning their ARP tables](placeholder_diagram_arp_poison1.png) -->

### Consequence: Man-in-the-Middle (Slide 44)

1.  **Traffic Redirection:**
    *   When Host A now wants to send data to Host B (IP 192.168.1.2), it consults its poisoned ARP table. It finds the mapping `192.168.1.2 -> cccc:cccc:cccc`.
    *   Host A sends the Ethernet frame containing the IP packet (Data: secret) to the **attacker's MAC address** (cccc:cccc:cccc) instead of Host B's real MAC address.
    *   Similarly, when Host B wants to send data to Host A (IP 192.168.1.1), it consults its poisoned ARP table and sends the frame to the attacker's MAC address (cccc:cccc:cccc).
2.  **Man-in-the-Middle Position:** The attacker (Host C) now receives all traffic originally intended to flow between Host A and Host B.
3.  **Attacker Capabilities:** From this position, the attacker can:
    *   **Eavesdrop:** Read the traffic (if unencrypted).
    *   **Modify:** Alter the traffic before forwarding it.
    *   **Block:** Drop the traffic (Denial of Service).
    *   **Forward:** Optionally, forward the (potentially modified) traffic to the original intended recipient to keep the communication flowing and remain undetected longer.
[[Q8]]


---


![[Screenshot From 2025-04-29 07-05-04.png]]




Okay, let's break down Exercice 01 from the second image (the exam paper).

**The Goal:**

Machine C wants to intercept traffic sent from Machine A *to* Machine B. To do this using ARP poisoning, Machine C needs to trick Machine A into believing that Machine B's IP address (192.168.1.2) actually belongs to Machine C's MAC address (let's assume CC:CC:CC:CC:CC:CC based on the diagram label).

The question specifically asks for the fields and values of a **gratuitous ARP request** (`requête ARP gratuite`) that C should send.

**Understanding Gratuitous ARP:**

A gratuitous ARP is an ARP packet (often a reply, but can be framed as a request asking about oneself) that is sent without being prompted by an ARP request. Its primary legitimate use is to announce a machine's IP-to-MAC mapping (e.g., when it first joins the network or changes its IP/MAC). Attackers abuse this to poison the ARP caches of other machines.

When a machine receives an ARP packet (request or reply), it typically updates its ARP cache with the Sender IP -> Sender MAC mapping contained within that packet.

**Constructing the Malicious Gratuitous ARP Request (Sent by C):**

Machine C will craft an ARP packet with the following key fields in the ARP payload:

1.  **Opcode:** The question specifies a "requête" (request), so the opcode should be **1**.
2.  **Sender MAC Address:** This is the actual MAC address of the machine sending the packet, which is Machine C. From the diagram label, this is **CC:CC:CC:CC:CC:CC**.
3.  **Sender IP Address:** This is the IP address that Machine C *wants* other machines (specifically A) to associate with C's MAC address. To intercept traffic for B, C must claim B's IP address. So, this is **192.168.1.2**.
4.  **Target MAC Address:** In a standard ARP request, this field asks "what is the MAC for the Target IP?" and is typically set to **00:00:00:00:00:00**. This remains the case for a gratuitous ARP *request*.
5.  **Target IP Address:** In a gratuitous ARP *request*, the machine is effectively asking about its *own* claimed IP address (the Sender IP). So, the Target IP is the same as the Sender IP: **192.168.1.2**.

**Ethernet Frame Context:**

Although not strictly part of the ARP payload fields requested, C would typically send this ARP packet inside an Ethernet frame:

*   **Source Ethernet MAC:** CC:CC:CC:CC:CC:CC (C's MAC)
*   **Destination Ethernet MAC:** FF:FF:FF:FF:FF:FF (Broadcast MAC, to ensure all hosts on the LAN segment, including A, receive and process the ARP packet)

**Summary of ARP Payload Fields and Values:**

Therefore, the fields and values of the gratuitous ARP request sent by C are:

*   **Opcode:** 1 (Request)
*   **Sender MAC Address:** CC:CC:CC:CC:CC:CC
*   **Sender IP Address:** 192.168.1.2
*   **Target MAC Address:** 00:00:00:00:00:00
*   **Target IP Address:** 192.168.1.2

**Effect:**

When Machine A receives this gratuitous ARP request, it will update its ARP cache based on the *sender* information. It will create or update an entry mapping the Sender IP (192.168.1.2) to the Sender MAC (CC:CC:CC:CC:CC:CC). Subsequently, when A tries to send data to 192.168.1.2 (Machine B's IP), it will encapsulate the data in an Ethernet frame addressed to CC:CC:CC:CC:CC:CC (Machine C's MAC), thus diverting the traffic to C.


---


Of course. I'll break your explanation down into **polished, organized tables** to make it crystal clear, while keeping everything clean and descriptive — like you asked.

---

# 🛠️ Gratuitous ARP Request Construction (Malicious - Machine C)

## ⚙️ ARP Payload Fields

|**Field**|**Value**|**Explanation**|
|:--|:--|:--|
|**Opcode**|`1` (Request)|Indicates this is an ARP _Request_ packet, even if unsolicited (gratuitous).|
|**Sender MAC Address**|`CC:CC:CC:CC:CC:CC`|Machine C’s physical address (claiming ownership of B’s IP).|
|**Sender IP Address**|`192.168.1.2`|IP address Machine C wants others to associate with its MAC (B’s IP).|
|**Target MAC Address**|`00:00:00:00:00:00`|Standard for ARP requests; means "unknown" or "querying."|
|**Target IP Address**|`192.168.1.2`|The same as the Sender IP; asking about its own fake claim.|

---

## 🧵 Ethernet Frame Context

|**Ethernet Field**|**Value**|**Explanation**|
|:--|:--|:--|
|**Source MAC Address**|`CC:CC:CC:CC:CC:CC`|Frame comes from Machine C.|
|**Destination MAC Address**|`FF:FF:FF:FF:FF:FF`|Ethernet Broadcast address, so all machines receive the packet.|
|**EtherType**|`0x0806` (ARP)|Type field indicates this is an ARP message.|

---

## 🧠 What Happens After?

|**Step**|**Action**|
|:--|:--|
|1|Machine A receives the ARP Request from C.|
|2|A inspects the packet and **updates its ARP table**, binding `192.168.1.2` (B's IP) to `CC:CC:CC:CC:CC:CC` (C's MAC).|
|3|When A later sends packets intended for B (`192.168.1.2`), it unknowingly sends them to C’s MAC address instead.|
|4|C can now intercept, read, modify, or forward traffic as desired.|

---

# 🛡️ Important Notes

- Although it's called a **gratuitous ARP request**, **the main goal here is not to "ask" for anything**, but **to trick** other hosts into associating an IP with the wrong MAC address.
    
- Gratuitous ARP is normally a security _feature_ (to announce a machine's presence) — but here it's being _weaponized_.
    
- This is **ARP Cache Poisoning**, and it’s the basis for many **Man-in-the-Middle (MitM)** attacks.
    

---

If you want, I can also show you a small **diagram of the packet structure**, layer-by-layer, or an even more detailed timeline of the poisoning process.  
Would you like that?