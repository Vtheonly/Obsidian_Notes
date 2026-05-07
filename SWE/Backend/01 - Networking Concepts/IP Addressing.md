# IP Addressing

## What is an IP Address

An IP address (Internet Protocol address) is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication. IP addresses serve two primary functions: they identify the host or network interface (identification), and they provide the location of the host in the network (addressing). Every packet of data sent across the internet includes the source IP address and the destination IP address, allowing routers along the path to forward the packet toward its destination.

There are two versions of the Internet Protocol in active use: IPv4 and IPv6. IPv4, defined in RFC 791 (1981), uses 32-bit addresses and has been the dominant protocol since the early days of the internet. IPv6, defined in RFC 8200 (2017, replacing RFC 2460), uses 128-bit addresses and was developed to address the exhaustion of IPv4 addresses. While IPv4 remains widely used, IPv6 adoption continues to grow as more devices connect to the internet and more networks deploy dual-stack configurations that support both protocols simultaneously.

---

## IPv4 Structure

IPv4 addresses are 32-bit numbers, typically represented in dotted decimal notation as four decimal numbers (called octets) separated by periods. Each octet represents 8 bits of the address and can range from 0 to 255. For example, the IP address `192.168.1.1` corresponds to the 32-bit binary number `11000000.10101000.00000001.00000001`. This notation makes IP addresses easier for humans to read and remember compared to the raw binary representation.

The 32-bit address space of IPv4 allows for approximately 4.3 billion unique addresses (2^32 = 4,294,967,296). While this seemed like an enormous number when IPv4 was designed, the explosive growth of the internet, the proliferation of mobile devices, and the assignment of large address blocks to organizations and regions have exhausted the available IPv4 address pool. The Internet Assigned Numbers Authority (IANA) allocated the last remaining IPv4 address blocks to Regional Internet Registries (RIRs) in 2011, and several RIRs have since exhausted their pools. This exhaustion is the primary driver behind the adoption of IPv6 and the widespread use of Network Address Translation (NAT) to conserve IPv4 addresses.

---

## IPv6 Structure

IPv6 addresses are 128-bit numbers, providing an address space of approximately 3.4 x 10^38 unique addresses (2^128). This vast address space eliminates the scarcity issues that plague IPv4. IPv6 addresses are represented in hexadecimal notation as eight groups of four hexadecimal digits separated by colons, such as `2001:0db8:85a3:0000:0000:8a2e:0370:7334`.

To make IPv6 addresses more concise, several shorthand rules apply. Leading zeros within each group can be omitted, so `0db8` becomes `db8` and `0000` becomes `0`. Additionally, a single consecutive sequence of all-zero groups can be replaced by a double colon (`::`), but this substitution can only be used once per address to avoid ambiguity. Using these rules, the example address above becomes `2001:db8:85a3::8a2e:370:7334`.

IPv6 also introduces a simplified header format compared to IPv4, removing fields like the header checksum and fragmentation fields that were computationally expensive and largely unnecessary. The IPv6 header is fixed at 40 bytes, compared to the variable-length IPv4 header (minimum 20 bytes), which makes routing more efficient. Extension headers in IPv6 provide optional functionality (such as fragmentation, authentication, and encapsulation) without complicating the basic header.

---

## IP Address Classes

The original IPv4 addressing scheme divided the address space into five classes (A through E), each defined by the bit pattern at the beginning of the address. This classful addressing system has been largely replaced by Classless Inter-Domain Routing (CIDR), but the class designations remain relevant for understanding historical network design and for certain certification exams.

### Class A

Class A addresses have the first bit set to 0, meaning the first octet ranges from 1 to 126. The default subnet mask is `255.0.0.0` (/8), meaning the first octet identifies the network and the remaining three octets identify the host. Each Class A network can support approximately 16.7 million hosts (2^24 - 2). Class A networks are assigned to very large organizations. The `127.x.x.x` range is reserved for loopback and is not a valid Class A network address.

### Class B

Class B addresses have the first two bits set to `10`, meaning the first octet ranges from 128 to 191. The default subnet mask is `255.255.0.0` (/16), meaning the first two octets identify the network and the last two identify the host. Each Class B network can support approximately 65,534 hosts (2^16 - 2). Class B networks were typically assigned to large universities and corporations.

### Class C

Class C addresses have the first three bits set to `110`, meaning the first octet ranges from 192 to 223. The default subnet mask is `255.255.255.0` (/24), meaning the first three octets identify the network and the last octet identifies the host. Each Class C network can support 254 hosts (2^8 - 2). Class C networks are the most common class and were assigned to small organizations and businesses.

### Class D

Class D addresses have the first four bits set to `1110`, meaning the first octet ranges from 224 to 239. Class D addresses are reserved for multicast communication, where a single packet is sent to a group of hosts simultaneously. Multicast is used in applications like streaming media, online gaming, and financial trading. Class D addresses cannot be assigned to individual hosts.

### Class E

Class E addresses have the first four bits set to `1111`, meaning the first octet ranges from 240 to 255. Class E addresses are reserved for experimental and research purposes and are not used in production networks.

---

## Subnet Masks and CIDR Notation

A subnet mask is a 32-bit number that divides an IPv4 address into a network portion and a host portion. The mask consists of a contiguous sequence of 1 bits followed by a contiguous sequence of 0 bits. The 1 bits indicate the network portion of the address, and the 0 bits indicate the host portion. For example, the subnet mask `255.255.255.0` (binary `11111111.11111111.11111111.00000000`) indicates that the first 24 bits of the IP address identify the network and the last 8 bits identify the host.

CIDR (Classless Inter-Domain Routing) notation provides a more compact way to express the subnet mask. Instead of writing the full dotted-decimal mask, CIDR uses a slash followed by the number of network bits. For example, `192.168.1.0/24` means the first 24 bits are the network portion (equivalent to subnet mask `255.255.255.0`), and the remaining 8 bits are the host portion. CIDR replaced the classful addressing system because it allows for more flexible allocation of address blocks. A `/24` network has 256 addresses (254 usable after excluding the network and broadcast addresses), a `/25` has 128 addresses (126 usable), a `/26` has 64 addresses (62 usable), and so on.

Subnetting is the process of dividing a larger network into smaller sub-networks by extending the subnet mask. For example, a `/24` network can be divided into two `/25` subnets, four `/26` subnets, eight `/27` subnets, and so on. This allows network administrators to allocate address space efficiently, creating subnets that match the actual size of each network segment rather than wasting addresses by using the classful defaults.

---

## Default Gateway and Routing

The default gateway is the IP address of the router that a device uses to send traffic to destinations outside its local subnet. When a device needs to communicate with another device, it first checks whether the destination IP address is on the same subnet by comparing the destination address with its own address and subnet mask. If the destination is on the same subnet, the device sends the packet directly using ARP (Address Resolution Protocol) to find the destination's MAC address. If the destination is on a different subnet, the device sends the packet to the default gateway, which forwards it toward the destination based on its routing table.

Routing is the process of selecting the best path for packets to travel from their source to their destination across interconnected networks. Routers maintain routing tables that map destination networks to next-hop addresses and interfaces. The routing table can be populated statically (by manual configuration) or dynamically (by routing protocols such as OSPF, BGP, EIGRP, and RIP). Each router along the path makes an independent forwarding decision based on its own routing table, passing the packet from hop to hop until it reaches the destination network.

---

## Loopback Address (127.0.0.1)

The loopback address is a special IP address that always refers to the local machine itself. The entire `127.0.0.0/8` block is reserved for loopback purposes, though `127.0.0.1` is the address most commonly used. When a program sends data to `127.0.0.1`, the operating system's network stack processes the data locally without ever transmitting it on the physical network interface. This makes the loopback address useful for testing and development, where you want to run client and server software on the same machine without needing a network connection.

In IPv6, the loopback address is `::1` (the full representation is `0000:0000:0000:0000:0000:0000:0000:0001`). It serves the same purpose as `127.0.0.1` in IPv4. Many services default to listening on the loopback address for security reasons, because connections to the loopback address can only originate from the local machine, preventing remote access. When configuring a service to listen on `0.0.0.0` (all interfaces) or a specific network interface, it becomes accessible from other machines on the network.

---

## Relationship to Other Concepts

[[Private IP vs Public IP]] builds directly on the concepts of IP addressing. Private IP addresses are a special subset of the IPv4 address space that are reserved for use within local networks and are not routable on the public internet. Understanding the distinction between private and public IP addresses, and how NAT bridges the gap between them, is essential for understanding how devices on local networks communicate with the internet.

[[DNS and Domain Resolution]] is the system that translates human-readable domain names into the IP addresses described in this note. DNS A records map domain names to IPv4 addresses, and AAAA records map domain names to IPv6 addresses. The DNS resolution process returns these IP addresses to clients, which then use them to establish network connections.

---

## Key Takeaways

IP addressing is the fundamental addressing system of the internet, with IPv4 providing 32-bit addresses and IPv6 providing 128-bit addresses. The classful addressing system has been superseded by CIDR, which allows for flexible subnet allocation. Subnet masks divide IP addresses into network and host portions, and the default gateway routes traffic between subnets. The loopback address provides a way to test network software locally. Understanding IP addressing is essential for network configuration, troubleshooting, and security.
