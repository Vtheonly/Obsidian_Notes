## II. ARP Poisoning (ARP Spoofing)

### A. What is ARP? (TD Exercice 02, Question 1)
**ARP (Address Resolution Protocol)** is a Layer 2 protocol used to map a known Layer 3 (IP) address to an unknown Layer 2 (MAC) address within the same local area network (LAN) or broadcast domain.
*   **Role:** When a host wants to send a packet to another host on the same LAN, it knows the destination IP address. However, Ethernet frames require a destination MAC address. ARP is used to discover this MAC address.
*   **ARP Table (ARP Cache):** Hosts maintain an ARP cache, which is a table mapping IP addresses to MAC addresses they have recently communicated with. This avoids repeating ARP requests for every packet.

**How ARP tables are updated:**
1.  **ARP Request:** If Host A (IP_A, MAC_A) wants to send data to Host B (IP_B) on the same LAN and doesn't have IP_B's MAC address in its cache:
    *   Host A broadcasts an ARP Request packet: "Who has IP_B? Tell IP_A." This packet contains IP_A, MAC_A (sender) and IP_B (target IP), target MAC is typically all zeros or FF:FF:FF:FF:FF:FF.
2.  **ARP Reply:** Host B (or a proxy) receives the broadcast. Since IP_B is its own IP address:
    *   Host B sends a unicast ARP Reply packet directly to Host A (using MAC_A from the request): "IP_B is at MAC_B."
3.  **Cache Update:** Host A receives the ARP Reply and updates its ARP cache with the mapping `(IP_B -> MAC_B)`.
4.  **Gratuitous ARP:** A host can also send an unsolicited ARP Reply (or an ARP Request for its own IP address). This is often done:
    *   On boot-up to announce its IP-MAC mapping.
    *   If its IP address changes.
    *   To update other hosts' caches if its MAC address changes (e.g., NIC replacement).
    ARP poisoning heavily abuses gratuitous ARPs or forged ARP replies.

### B. What is ARP Poisoning?
ARP Poisoning (also known as ARP Spoofing) is a Man-in-the-Middle (MitM) attack where an attacker sends falsified ARP messages onto a LAN. The goal is to associate the attacker's MAC address with the IP address of another host (e.g., the default gateway or a specific victim).
This tricks other machines on the LAN into sending network traffic destined for the legitimate IP address to the attacker instead.

### C. How ARP Poisoning Works (Process & TD Scenario)
Let's use the network diagram from TD Exercice 02.
*   **Attacker:** Machine C (192.168.1.3 / CC:..:CC)
*   **Victim 1 (Client):** Machine B (192.168.1.2 / BB:..:BB)
*   **Victim 2 (Gateway):** Router R1 (eth0 interface: 192.168.1.255 / R10:..:R10)

**Goal for C:** Intercept traffic between B and R1 (the internet).

**ARP Tables Before Attack (TD Question 5 - simplified):**
*   **Machine B's ARP Table:**
    *   `192.168.1.255 (R1_IP) -> R10:..:R10 (R1_MAC)`
    *   (Possibly other local IPs like A's IP -> A's MAC)
*   **Router R1's ARP Table (for eth0 segment):**
    *   `192.168.1.2 (B_IP) -> BB:..:BB (B_MAC)`
    *   `192.168.1.1 (A_IP) -> AA:..:AA (A_MAC)`
    *   `192.168.1.3 (C_IP) -> CC:..:CC (C_MAC)`

**Steps for Machine C to Perform the Attack (TD Question 6):**
1.  **Poison Machine B's ARP Cache:**
    *   C sends a forged ARP Reply (or gratuitous ARP) to Machine B.
    *   This packet claims: "The IP address 192.168.1.255 (R1's IP) is at MAC address CC:..:CC (C's MAC)."
    *   Machine B updates its ARP cache: `192.168.1.255 -> CC:..:CC`.
    *   Now, when B wants to send traffic to the internet (via R1), it will encapsulate packets in Ethernet frames addressed to C's MAC address.

2.  **Poison Router R1's ARP Cache:**
    *   C sends a forged ARP Reply (or gratuitous ARP) to Router R1 (on its eth0 interface).
    *   This packet claims: "The IP address 192.168.1.2 (B's IP) is at MAC address CC:..:CC (C's MAC)."
    *   Router R1 updates its ARP cache: `192.168.1.2 -> CC:..:CC`.
    *   Now, when R1 receives traffic from the internet destined for B, it will encapsulate packets in Ethernet frames addressed to C's MAC address.

3.  **Enable IP Forwarding on Machine C:**
    *   For the attack to be a true MitM (and not just a Denial of Service), C must forward the intercepted packets to their intended destinations.
    *   On Linux: `echo 1 > /proc/sys/net/ipv4/ip_forward`
    *   C receives packets from B (destined for R1), sniffs them, then forwards them to R1 (using R1's real MAC).
    *   C receives packets from R1 (destined for B), sniffs them, then forwards them to B (using B's real MAC).

**ARP Tables After Successful Attack (TD Question 7):**
*   **Machine B's ARP Table:**
    *   `192.168.1.255 (R1_IP) -> CC:..:CC (C's_MAC)` (Poisoned!)
    *   `192.168.1.1 (A_IP) -> AA:..:AA (A_MAC)` (Likely unchanged)
*   **Router R1's ARP Table (for eth0 segment):**
    *   `192.168.1.2 (B_IP) -> CC:..:CC (C's_MAC)` (Poisoned!)
    *   `192.168.1.1 (A_IP) -> AA:..:AA (A_MAC)` (Likely unchanged)
    *   `192.168.1.3 (C_IP) -> CC:..:CC (C_MAC)` (Unchanged, C's own entry)
*   **Machine C's ARP Table:**
    *   `192.168.1.2 (B_IP) -> BB:..:BB (B_MAC)` (Must be correct for forwarding)
    *   `192.168.1.255 (R1_IP) -> R10:..:R10 (R1_MAC)` (Must be correct for forwarding)
    *   `192.168.1.1 (A_IP) -> AA:..:AA (A_MAC)`

**Machines that can launch ARP spoofing on R1's eth0 network (TD Question 4):**
Any machine on the same Layer 2 broadcast domain as R1's eth0 interface. In the diagram, these are:
*   Machine A (192.168.1.1)
*   Machine B (192.168.1.2)
*   Machine C (192.168.1.3)
They can all send ARP packets that will be received by other devices on the 192.168.1.0/24 subnet, including R1's eth0 interface.

**What Machine C can sniff (TD Question 2):**
*   **Normally (on a switched network like with Sw1):**
    *   Broadcast traffic (e.g., ARP requests from A or B).
    *   Multicast traffic C is subscribed to.
    *   Unicast traffic specifically addressed to C's MAC address (CC:..:CC).
    *   It would *not* see unicast traffic between A and B, or B and R1.
*   **After successful ARP poisoning (intercepting B and R1):**
    *   All traffic between Machine B and Router R1 will pass through Machine C. C can therefore sniff all this traffic.

### D. Tools for ARP Poisoning
*   **arpspoof (part of the dsniff suite):** A common command-line tool.
    *   `arpspoof -i <interface> -t <victim_IP> <gateway_IP>` (poisons victim)
    *   `arpspoof -i <interface> -t <gateway_IP> <victim_IP>` (poisons gateway)
*   **Ettercap:** A comprehensive suite for MitM attacks, supports ARP poisoning.
*   **Cain & Abel:** (Windows-only) A password recovery tool with ARP poisoning capabilities.
*   **BetterCAP:** A powerful, modular, portable and easily extensible MitM framework.

### E. Prevention and Detection of ARP Poisoning
1.  **Static ARP Entries:** Manually configure ARP entries on hosts and routers. This is highly effective but difficult to manage in large networks.
2.  **ARP Spoofing Detection Software:**
    *   **Arpwatch:** Monitors Ethernet activity and logs changes to IP-MAC pairings, can send alerts.
    *   **XArp, ArpON:** Actively block or detect suspicious ARP activity.
3.  **Dynamic ARP Inspection (DAI):** A feature on managed switches. DAI intercepts all ARP requests and replies. It validates them against a trusted database of IP-MAC bindings (often built from DHCP snooping). Invalid ARP packets are dropped. This is a very effective enterprise-level solution.
4.  **Port Security (on switches):** Can limit the number of MAC addresses learned on a port or bind specific MAC addresses to specific ports, making it harder for an attacker to spoof.
5.  **Use of Encrypted Protocols (HTTPS, SSH, VPNs):** Even if traffic is intercepted via ARP spoofing, encryption prevents the attacker from reading the content. However, the attacker might still be able to perform other attacks (e.g., SSL stripping if HSTS is not used).
