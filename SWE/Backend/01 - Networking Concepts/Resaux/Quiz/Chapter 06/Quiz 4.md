---
sources:
  - "[[06.00 Introduction]]"
  - "[[06.01 Address Resolution Protocol (ARP) Deep Dive]]"
  - "[[06.02 Network Address Translation (NAT) & Port Address Translation (PAT)]]"
---

> [!question] A PAT router modifies both source IP addresses and source port numbers on outbound packets.
>> [!success]- Answer
>> True

> [!question] The command to view the local ARP cache on a Windows or Linux machine is 'arp -a'.
>> [!success]- Answer
>> True

> [!question] The target protocol address in an ARP Request is the IP address of the host being resolved.
>> [!success]- Answer
>> True

> [!question] Port Address Translation (PAT) is also known as NAT Overload.
>> [!success]- Answer
>> True

> [!question] Non-target hosts that receive an ARP Request drop the packet after inspecting the Target Protocol Address.
>> [!success]- Answer
>> True

> [!question] If a Dynamic NAT public IP pool is exhausted, subsequent outbound connection attempts will fail.
>> [!success]- Answer
>> True

> [!question] When a host receives an ARP Request, it updates its local ARP cache with the sender's IP and MAC address.
>> [!success]- Answer
>> True

> [!question] NAT translation occurs at the core network switches.
>> [!success]- Answer
>> False

> [!question] The CAM table operates at Layer 3 of the OSI model.
>> [!success]- Answer
>> False

> [!question] Dynamic NAT supports bidirectional connection initiation from the public Internet.
>> [!success]- Answer
>> False

> [!question] If Host A knows Host B's IP address but not its MAC address, what must it do first?
> a) Drop the packet
> b) Send the data packet to the switch MAC
> c) Send an ARP Request
> d) Consult the local DNS server
>> [!success]- Answer
>> c) Send an ARP Request

> [!question] On which device does the Switch MAC Address Table (CAM Table) primarily reside?
> a) DHCP Server
> b) Layer 2 Switch
> c) Local Client Host
> d) Layer 3 Router
>> [!success]- Answer
>> b) Layer 2 Switch

> [!question] Which field in the Ethernet header determines that the payload is an ARP packet?
> a) EtherType
> b) Source MAC
> c) Frame Check Sequence
> d) Preamble
>> [!success]- Answer
>> a) EtherType

> [!question] What does the PAT translation engine do to inbound packets returning from the Internet?
> a) Checks client MAC address registry table
> b) Performs reverse lookup on destination port to rewrite Dst IP/Port
> c) Sends an ARP request to locate the destination host
> d) Floods the packet to all inside interfaces
>> [!success]- Answer
>> b) Performs reverse lookup on destination port to rewrite Dst IP/Port

> [!question] What type of frame transmission is used for an ARP Reply?
> a) Anycast
> b) Broadcast
> c) Multicast
> d) Unicast
>> [!success]- Answer
>> d) Unicast

> [!question] What does Host B do when it receives an ARP Request targeting its own IP address?
> a) Broadcasts an ARP Reply to all hosts
> b) Updates its cache with Host A's info and sends a unicast reply
> c) Discards the frame and does nothing
> d) Sends its MAC address to the local DNS server
>> [!success]- Answer
>> b) Updates its cache with Host A's info and sends a unicast reply

> [!question] Which of the following is an RFC 1918 private IP address block?
> a) 10.0.0.0/16 only
> b) 192.168.1.0/24 only
> c) 169.254.0.0/16
> d) 172.16.0.0/12
>> [!success]- Answer
>> d) 172.16.0.0/12

> [!question] At what boundary device does NAT translation typically occur?
> a) Core Layer 2 Switch
> b) Client Host Operating System
> c) Perimeter Gateway Router
> d) Local DNS Server
>> [!success]- Answer
>> c) Perimeter Gateway Router

> [!question] Why does Dynamic NAT block unsolicited inbound traffic from the Internet?
> a) The router drops all incoming packets by default
> b) There is no permanent mapping for internal hosts in the translation table
> c) It requires client MAC authorization
> d) The public IP address pool is kept disabled
>> [!success]- Answer
>> b) There is no permanent mapping for internal hosts in the translation table

> [!question] Which protocol resolves MAC addresses to IP addresses in IPv6?
> a) DHCPv6
> b) Neighbor Discovery Protocol (NDP)
> c) Address Resolution Protocol (ARP)
> d) ICMPv6 Redirect
>> [!success]- Answer
>> b) Neighbor Discovery Protocol (NDP)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Inside Local Address
>> b) Unicast
>> c) Perimeter Gateway
>
>> [!example] Group B
>> n) Device where NAT translation occurs.
>> o) Direct one-to-one L2 delivery.
>> p) Private IP assigned to internal host.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) show mac-address-table
>> b) Well-Known Ports
>> c) 0x0806
>
>> [!example] Group B
>> n) Cisco command to view switch CAM table.
>> o) Reserved system ports (range 0 to 1023).
>> p) EtherType designating ARP payload.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Dynamic NAT
>> b) 192.168.0.0/16
>> c) arp -a
>
>> [!example] Group B
>> n) Class C private IP address block.
>> o) Maps private IP to a public pool dynamically.
>> p) Command to view local ARP cache on PC.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) PAT / Overload
>> b) Inside Global Address
>> c) Perimeter Gateway
>
>> [!example] Group B
>> n) Public IP representing internal host on WAN.
>> o) Device where NAT translation occurs.
>> p) Maps multiple private IPs to one public IP using ports.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Inside Local Address
>> b) CAM Table
>> c) Split Horizon
>
>> [!example] Group B
>> n) Maps MAC addresses to physical switch ports.
>> o) Private IP assigned to internal host.
>> p) Never advertise route out ingress interface.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Hold-Down Timer
>> b) Class B range limit
>> c) Outside Global Address
>
>> [!example] Group B
>> n) Ends at 172.31.255.255.
>> o) Public IP assigned to external target host.
>> p) Ignores RIP updates with worse metrics for 60s.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 172.16.0.0/12
>> b) Dynamic NAT
>> c) Private IP range
>
>> [!example] Group B
>> n) Maps private IP to a public pool dynamically.
>> o) Non-routable IP spaces defined in RFC 1918.
>> p) Class B private IP address block.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) DF = 1 Flag
>> b) Broadcast
>> c) CAM Table
>
>> [!example] Group B
>> n) One-to-all L2 delivery in local subnet.
>> o) Blocks packet fragmentation at WAN boundary.
>> p) Maps MAC addresses to physical switch ports.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) CAM Table
>> b) Port allocation
>> c) Inside Global Address
>
>> [!example] Group B
>> n) Maps MAC addresses to physical switch ports.
>> o) Public IP representing internal host on WAN.
>> p) PAT router shifts ports to avoid collisions.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Class C range limit
>> b) Split Horizon
>> c) 172.16.0.0/12
>
>> [!example] Group B
>> n) Class B private IP address block.
>> o) Ends at 192.168.255.255.
>> p) Never advertise route out ingress interface.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)
