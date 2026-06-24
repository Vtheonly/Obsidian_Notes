---
sources:
  - "[[06.00 Introduction]]"
  - "[[06.01 Address Resolution Protocol (ARP) Deep Dive]]"
  - "[[06.02 Network Address Translation (NAT) & Port Address Translation (PAT)]]"
---

> [!question] An ARP packet is directly encapsulated inside an IP packet.
>> [!success]- Answer
>> False

> [!question] The ARP cache resides on Layer 2 switches and bridges.
>> [!success]- Answer
>> False

> [!question] NAT Overload requires a pool of public IP addresses equal to the number of active host sessions.
>> [!success]- Answer
>> False

> [!question] A switch floods an ARP broadcast out of all ports, including the port it was received on.
>> [!success]- Answer
>> False

> [!question] Under PAT, the router tracks connections by using unique source port numbers.
>> [!success]- Answer
>> True

> [!question] An ARP Reply is sent as a unicast frame containing the sender's MAC address.
>> [!success]- Answer
>> True

> [!question] PAT allows thousands of internal hosts to share a single public IP address.
>> [!success]- Answer
>> True

> [!question] A switch MAC address table maps IP addresses to physical switch ports.
>> [!success]- Answer
>> False

> [!question] The private IP block 192.168.0.0/16 is a Class C private range.
>> [!success]- Answer
>> True

> [!question] Class C private IP address range is 192.168.0.0/24 only.
>> [!success]- Answer
>> False

> [!question] Which destination MAC address is used to encapsulate an ARP Request?
> a) FF:FF:FF:FF:FF:FF
> b) 00:00:00:00:00:00
> c) 01:00:5E:00:00:01
> d) The target host's MAC address
>> [!success]- Answer
>> a) FF:FF:FF:FF:FF:FF

> [!question] What is the mapping type of the ARP Table?
> a) IP Address to Switch Port
> b) IP Address to MAC Address
> c) MAC Address to Switch Port
> d) Port Number to Switch Port
>> [!success]- Answer
>> b) IP Address to MAC Address

> [!question] What is translated in a Static NAT configuration?
> a) Both IP addresses and port numbers
> b) IP addresses only (1:1)
> c) MAC addresses only
> d) Port numbers only
>> [!success]- Answer
>> b) IP addresses only (1:1)

> [!question] What happens to an outbound packet's source port under PAT if two hosts use the same source port?
> a) The router drops the connections of both hosts
> b) The router discards the second host's packet
> c) The router forwards both packets without modification
> d) The router translates one to a unique, unused port
>> [!success]- Answer
>> d) The router translates one to a unique, unused port

> [!question] What command is used in Linux/Windows CLI to view the ARP table?
> a) ip neighbor show
> b) netstat -r
> c) show arp
> d) arp -a
>> [!success]- Answer
>> d) arp -a

> [!question] How does PAT track different translation sessions using a single public IP address?
> a) By using a round-robin IP allocation
> b) By tracking MAC addresses of clients
> c) By tracking unique source port numbers
> d) By appending hostnames to packets
>> [!success]- Answer
>> c) By tracking unique source port numbers

> [!question] Which private IP address range is a Class B private range?
> a) 172.16.0.0 to 172.16.255.255
> b) 192.168.0.0 to 192.168.255.255
> c) 10.0.0.0 to 10.255.255.255
> d) 172.16.0.0 to 172.31.255.255
>> [!success]- Answer
>> d) 172.16.0.0 to 172.31.255.255

> [!question] Which NAT type is most cost-effective for an office with 500 clients sharing one public IP?
> a) 1:1 Address Mapping
> b) Dynamic NAT
> c) Static NAT
> d) Port Address Translation (PAT)
>> [!success]- Answer
>> d) Port Address Translation (PAT)

> [!question] If a switch receives a unicast frame with a destination MAC not present in its CAM table, what does it do?
> a) Queries the default gateway router
> b) Floods the frame out of all ports except the ingress port
> c) Discards the frame immediately
> d) Sends an ARP Request to locate the MAC
>> [!success]- Answer
>> b) Floods the frame out of all ports except the ingress port

> [!question] What is the purpose of the Frame Check Sequence (FCS) in an Ethernet frame?
> a) To specify the destination MAC address
> b) To detect frame corruption
> c) To prevent routing loops
> d) To identify the payload protocol
>> [!success]- Answer
>> b) To detect frame corruption

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Hold-Down Timer
>> b) 10.0.0.0/8
>> c) Class C range limit
>
>> [!example] Group B
>> n) Ignores RIP updates with worse metrics for 60s.
>> o) Ends at 192.168.255.255.
>> p) Class A private IP address block.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Class B range limit
>> b) ARP Cache
>> c) ARP
>
>> [!example] Group B
>> n) Ends at 172.31.255.255.
>> o) Resolves logical IP addresses to physical MAC addresses.
>> p) Maps IP addresses to physical MAC addresses.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Class C range limit
>> b) arp -a
>> c) Private IP range
>
>> [!example] Group B
>> n) Ends at 192.168.255.255.
>> o) Command to view local ARP cache on PC.
>> p) Non-routable IP spaces defined in RFC 1918.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Dynamic NAT
>> b) ARP Reply
>> c) Static NAT
>
>> [!example] Group B
>> n) Maps private IP to a public pool dynamically.
>> o) Unicast frame returning target hardware address.
>> p) One-to-one permanent mapping of public/private IP.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 0x0800
>> b) ARP Cache
>> c) CAM Table
>
>> [!example] Group B
>> n) EtherType designating IPv4 payload.
>> o) Maps MAC addresses to physical switch ports.
>> p) Maps IP addresses to physical MAC addresses.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Class C range limit
>> b) Ephemeral Ports
>> c) Perimeter Gateway
>
>> [!example] Group B
>> n) Dynamic client ports (range 49152 to 65535).
>> o) Ends at 192.168.255.255.
>> p) Device where NAT translation occurs.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Port allocation
>> b) CAM Table
>> c) FCS / CRC
>
>> [!example] Group B
>> n) Maps MAC addresses to physical switch ports.
>> o) PAT router shifts ports to avoid collisions.
>> p) Used to check Layer 2 frame corruption.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 5-Tuple
>> b) FCS / CRC
>> c) Outside Global Address
>
>> [!example] Group B
>> n) Public IP assigned to external target host.
>> o) Used to check Layer 2 frame corruption.
>> p) Protocol, Src IP, Src Port, Dst IP, Dst Port.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) ARP Reply
>> b) show mac-address-table
>> c) Dynamic NAT
>
>> [!example] Group B
>> n) Cisco command to view switch CAM table.
>> o) Unicast frame returning target hardware address.
>> p) Maps private IP to a public pool dynamically.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Port allocation
>> b) PAT / Overload
>> c) Well-Known Ports
>
>> [!example] Group B
>> n) Reserved system ports (range 0 to 1023).
>> o) Maps multiple private IPs to one public IP using ports.
>> p) PAT router shifts ports to avoid collisions.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)
