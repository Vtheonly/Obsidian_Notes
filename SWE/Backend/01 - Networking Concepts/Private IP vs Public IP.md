# Private IP vs Public IP

## What is a Public IP Address

A public IP address is a globally unique IP address that is assigned to a device by an Internet Service Provider (ISP) and is directly reachable from anywhere on the internet. Public IP addresses are allocated by the Internet Assigned Numbers Authority (IANA) to Regional Internet Registries (RIRs), which in turn assign them to ISPs and large organizations. Every device that needs to be directly accessible from the internet, such as web servers, email servers, and VPN gateways, must have a public IP address.

Public IP addresses are routable on the internet, meaning that routers across the global network know how to forward packets destined for any valid public IP address. When you visit a website, your device sends packets to the website's public IP address, and the routers along the path forward those packets hop by hop until they reach the destination. Similarly, the website's server sends response packets back to your public IP address. Because public IP addresses must be globally unique, they are a finite and increasingly scarce resource, especially under IPv4 where the available pool has been exhausted.

For most home and mobile users, their router or modem receives a single public IP address from the ISP, and all devices on the local network share this address through Network Address Translation (NAT). Business users may lease blocks of public IP addresses to assign to individual servers or services. The cost and scarcity of public IPv4 addresses has driven the adoption of IPv6, which provides a vastly larger address space, as well as the widespread use of NAT and cloud-based services that can share a smaller number of public addresses among many customers.

---

## What is a Private IP Address

A private IP address is an IP address from a reserved range that is used within a local network and is not routable on the public internet. Private IP addresses allow organizations and home users to create internal networks without consuming scarce public IP addresses. Devices on a local network communicate with each other using private IP addresses, and when they need to access the internet, a router performing NAT translates the private address to a public address.

The Internet Engineering Task Force (IETF) defined three private address ranges in RFC 1918, one for each of the IPv4 address classes. These ranges are guaranteed never to be assigned as public addresses, so there is no conflict between internal networks using private addresses and the global internet. Any organization can use any of these private address ranges internally without coordinating with any external authority, and the same private addresses can be used simultaneously by millions of independent networks around the world.

---

## Private IP Ranges

### 10.0.0.0/8 (Class A Range)

The `10.0.0.0/8` range spans from `10.0.0.0` to `10.255.255.255`, providing over 16 million private addresses. This range is commonly used by large organizations and enterprise networks that need a vast address space for their internal infrastructure. The large size of this range allows for extensive subnetting, enabling network administrators to create many subnets of varying sizes to organize different departments, regions, or functions within the organization.

### 172.16.0.0/12 (Class B Range)

The `172.16.0.0/12` range spans from `172.16.0.0` to `172.31.255.255`, providing over 1 million private addresses (specifically, 1,048,576 addresses across 16 Class B networks). This range is commonly used by medium-sized organizations. It provides a good balance between address space and manageability, allowing for multiple subnets without the overhead of managing the extremely large 10.0.0.0/8 range.

### 192.168.0.0/16 (Class C Range)

The `192.168.0.0/16` range spans from `192.168.0.0` to `192.168.255.255`, providing 65,536 private addresses (256 Class C networks). This range is by far the most commonly used in home and small office networks. Most consumer routers are configured by default to assign addresses from `192.168.0.0/24` or `192.168.1.0/24` to devices on the local network using DHCP. The 256 available Class C subnets within this range provide flexibility for small networks that may need a few separate subnets.

---

## NAT (Network Address Translation)

NAT is the mechanism that allows devices with private IP addresses to communicate with the public internet. When a device on a private network sends a packet to an internet destination, the router performing NAT replaces the source private IP address with the router's own public IP address and records the mapping in a translation table. When the response arrives, the router looks up the mapping in its translation table and replaces the destination public IP address with the original private IP address before forwarding the packet to the internal device.

The most common form of NAT is Port Address Translation (PAT), also called NAT overload or NAPT. PAT allows hundreds or thousands of devices on a private network to share a single public IP address by mapping each connection to a unique port number on the router's public address. For example, if a device at `192.168.1.10` makes an HTTP request to a web server, the NAT router might translate the source address from `192.168.1.10:54321` to `203.0.113.5:54321`, where `203.0.113.5` is the router's public IP address. When the response arrives addressed to `203.0.113.5:54321`, the router translates it back to `192.168.1.10:54321`.

NAT has several important implications. It provides a degree of security by hiding internal IP addresses from the internet, making it harder for attackers to directly reach internal devices. However, NAT also breaks the end-to-end connectivity model that the internet was originally designed around, creating complications for peer-to-peer protocols, VoIP, and other applications that need to accept inbound connections. Various NAT traversal techniques (such as STUN, TURN, and ICE) have been developed to work around these limitations.

---

## When to Use Public vs Private IPs

The decision to use a public or private IP address depends on the requirements of the device or service in question.

### Use a Public IP Address When

- The device is a server that must be directly reachable from the internet, such as a web server, mail server, DNS server, or game server.
- The device provides a service that external clients need to connect to without going through a reverse proxy or port forwarding.
- The device needs to participate in peer-to-peer protocols that require direct inbound connectivity.
- The device is a VPN endpoint that remote clients connect to.

### Use a Private IP Address When

- The device is a workstation, laptop, phone, or tablet that only needs to initiate outbound connections to the internet.
- The device is an internal server (file server, print server, database server) that only needs to be accessible from within the local network.
- The device is part of an internal infrastructure that should not be directly exposed to the internet for security reasons.
- The device is on a home or office network that uses a shared public IP address through NAT.

In cloud environments, the distinction is often managed by assigning both a private IP (for internal communication within the virtual network) and a public IP (for external access) to the same virtual machine. The cloud provider's networking infrastructure handles the NAT between them.

---

## Security Implications

Private IP addresses provide an inherent layer of security because they are not routable on the public internet. A device with only a private IP address cannot be reached directly by an external attacker; all inbound traffic must pass through the NAT router, which acts as an implicit firewall. This does not make the device immune to attack, but it significantly reduces the attack surface.

However, private IP addresses alone do not provide comprehensive security. An attacker on the same local network can reach devices using their private IP addresses directly. Malware on an internal device can establish outbound connections to command-and-control servers, bypassing the NAT router's inbound restrictions. And misconfigured port forwarding rules on the NAT router can inadvertently expose internal devices to the internet. A proper security strategy combines private IP addressing with firewalls, intrusion detection systems, network segmentation, and access controls.

Public IP addresses, by contrast, are directly reachable from the internet and must be protected with appropriate security measures. Any device with a public IP address should have a properly configured firewall that blocks all unnecessary ports and services. Security patches must be applied promptly, and services should be hardened against common attack vectors. The exposure of a public IP address makes it a target for automated scanning and exploitation attempts, which are constant on the modern internet.

---

## APIPA and Link-Local Addresses (169.254.0.0/16)

APIPA (Automatic Private IP Addressing) is a feature that allows a device to automatically assign itself a private IP address from the `169.254.0.0/16` range when no DHCP server is available. This range is defined in RFC 3927 and is designated for link-local communication, meaning that addresses in this range are only valid on the local network segment and are not forwarded by routers.

When a device configured for DHCP boots up and cannot reach a DHCP server, it randomly selects an address from the `169.254.1.0` to `169.254.254.255` range and uses ARP to verify that no other device on the network is already using that address. If there is a conflict, it selects another address and tries again. Once a unique address is found, the device configures itself with that address and a `/16` subnet mask.

APIPA addresses are useful for small networks where devices need to communicate with each other but no DHCP server is available, such as a temporary ad-hoc network or a home network where the DHCP server on the router has malfunctioned. However, devices with APIPA addresses cannot access the internet or communicate with devices on other subnets, because the `169.254.0.0/16` range is not routable. In IPv6, link-local addresses from the `fe80::/10` range serve a similar purpose and are actually required for IPv6 to function, as they are used for neighbor discovery and other essential protocols.

---

## Relationship to Other Concepts

[[IP Addressing]] provides the foundational understanding of how IP addresses work, including the structure of IPv4 and IPv6 addresses, subnet masks, and CIDR notation. The private and public IP address concepts build directly on this foundation, distinguishing between addresses that are globally routable and those that are reserved for local use.

[[DNS and Domain Resolution]] works in conjunction with public IP addresses to make services accessible by name rather than by address. DNS A and AAAA records map domain names to public IP addresses, while internal DNS zones can map names to private IP addresses for use within an organization's network. The split between internal and external DNS resolution mirrors the split between private and public IP addressing.

---

## Key Takeaways

Public IP addresses are globally unique and directly reachable from the internet, while private IP addresses are reserved for use within local networks and are not routable on the internet. The three private IPv4 ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) allow organizations to create internal networks without consuming public addresses. NAT bridges the gap between private and public addressing, enabling millions of devices with private addresses to share a smaller number of public addresses. APIPA provides automatic link-local addressing when DHCP is unavailable. Understanding the distinction between private and public IP addresses is fundamental to network design, security, and troubleshooting.
