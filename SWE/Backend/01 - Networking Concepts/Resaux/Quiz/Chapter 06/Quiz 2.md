---
sources:
  - "[[06.00 Introduction]]"
  - "[[06.01 Address Resolution Protocol (ARP) Deep Dive]]"
  - "[[06.02 Network Address Translation (NAT) & Port Address Translation (PAT)]]"
---

> [!question] Port Address Translation has higher router CPU and memory overhead than Static NAT.
>> [!success]- Answer
>> True

> [!question] An ARP Reply is flooded out of all ports by a switch.
>> [!success]- Answer
>> False

> [!question] A router decapsulates the Layer 2 header of an incoming frame to expose the Layer 3 IP packet.
>> [!success]- Answer
>> True

> [!question] ARP resolves L3 IP addresses to L2 MAC addresses.
>> [!success]- Answer
>> True

> [!question] Static NAT is more efficient in public IP space consumption than PAT.
>> [!success]- Answer
>> False

> [!question] Static NAT is typically used for internal servers that must be accessible from the public Internet.
>> [!success]- Answer
>> True

> [!question] An ARP Request is sent as a unicast frame to the target host.
>> [!success]- Answer
>> False

> [!question] Private IP addresses defined in RFC 1918 are routable across the public Internet.
>> [!success]- Answer
>> False

> [!question] A Layer 2 switch dynamically populates its CAM table by inspecting the source MAC addresses of incoming frames.
>> [!success]- Answer
>> True

> [!question] Static ARP entries in a host's cache never expire unless manually deleted.
>> [!success]- Answer
>> True

> [!question] What type of address mapping is performed by the Address Resolution Protocol (ARP)?
> a) Logical IP to Physical MAC
> b) Logical IP to Port Number
> c) Domain Name to IP Address
> d) Physical MAC to Switch Port
>> [!success]- Answer
>> a) Logical IP to Physical MAC

> [!question] What is a primary disadvantage of PAT (NAT Overload)?
> a) Requires one public IP per internal host
> b) Prevents outbound client access
> c) Exposes the internal topology to the public network
> d) High router resources and state table overhead
>> [!success]- Answer
>> d) High router resources and state table overhead

> [!question] What happens to an ARP Request frame when it arrives at a Layer 2 switch port?
> a) Routed to the default gateway
> b) Forwarded directly to the target host's port
> c) Discarded unless target MAC is known
> d) Flooded out all ports except the receiving port
>> [!success]- Answer
>> d) Flooded out all ports except the receiving port

> [!question] What is the size of the port number field in TCP/UDP headers?
> a) 32 bits
> b) 16 bits
> c) 64 bits
> d) 8 bits
>> [!success]- Answer
>> b) 16 bits

> [!question] Which layer of the OSI model does the ARP cache operate at?
> a) Layer 4
> b) Layer 7
> c) Layer 1
> d) Layer 2/3 boundary
>> [!success]- Answer
>> d) Layer 2/3 boundary

> [!question] Which parameter is NOT part of the 5-Tuple connection key?
> a) Destination IP Address
> b) Source IP Address
> c) Protocol
> d) Source MAC Address
>> [!success]- Answer
>> d) Source MAC Address

> [!question] Which Class C private IP address block is defined by RFC 1918?
> a) 10.0.0.0/8
> b) 192.168.1.0/24 only
> c) 172.16.0.0/12
> d) 192.168.0.0/16
>> [!success]- Answer
>> d) 192.168.0.0/16

> [!question] How does a switch dynamically populate its MAC address table?
> a) Inspecting the source MAC address of incoming frames
> b) Manually configured by the administrator only
> c) Listening to ARP Reply broadcasts
> d) Querying the local DNS server
>> [!success]- Answer
>> a) Inspecting the source MAC address of incoming frames

> [!question] What is another term for Port Address Translation (PAT)?
> a) Dynamic Pool NAT
> b) NAT Overload
> c) Static Port Mapping
> d) 1:1 NAT
>> [!success]- Answer
>> b) NAT Overload

> [!question] What limitation exists in Dynamic NAT when mapping many-to-many addresses?
> a) Only one public IP can be utilized by the router
> b) Inbound connections are automatically forwarded to all hosts
> c) Outbound sessions fail if the public IP pool is exhausted
> d) It requires port-level translation state tracking
>> [!success]- Answer
>> c) Outbound sessions fail if the public IP pool is exhausted

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Inside Global Address
>> b) Port allocation
>> c) Dynamic NAT
>
>> [!example] Group B
>> n) PAT router shifts ports to avoid collisions.
>> o) Public IP representing internal host on WAN.
>> p) Maps private IP to a public pool dynamically.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Well-Known Ports
>> b) Perimeter Gateway
>> c) FF:FF:FF:FF:FF:FF
>
>> [!example] Group B
>> n) Reserved system ports (range 0 to 1023).
>> o) Device where NAT translation occurs.
>> p) Layer 2 broadcast MAC address.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Well-Known Ports
>> b) Outside Global Address
>> c) Unicast
>
>> [!example] Group B
>> n) Reserved system ports (range 0 to 1023).
>> o) Public IP assigned to external target host.
>> p) Direct one-to-one L2 delivery.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) CAM Table
>> b) 0x0800
>> c) PAT / Overload
>
>> [!example] Group B
>> n) Maps MAC addresses to physical switch ports.
>> o) EtherType designating IPv4 payload.
>> p) Maps multiple private IPs to one public IP using ports.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Hold-Down Timer
>> b) Perimeter Gateway
>> c) Outside Global Address
>
>> [!example] Group B
>> n) Ignores RIP updates with worse metrics for 60s.
>> o) Device where NAT translation occurs.
>> p) Public IP assigned to external target host.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) FCS / CRC
>> b) 0x0806
>> c) PAT / Overload
>
>> [!example] Group B
>> n) Used to check Layer 2 frame corruption.
>> o) Maps multiple private IPs to one public IP using ports.
>> p) EtherType designating ARP payload.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Outside Global Address
>> b) FF:FF:FF:FF:FF:FF
>> c) Class A range limit
>
>> [!example] Group B
>> n) Public IP assigned to external target host.
>> o) Layer 2 broadcast MAC address.
>> p) Ends at 10.255.255.255.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Invalid Timer
>> b) Broadcast
>> c) Class A range limit
>
>> [!example] Group B
>> n) Ends at 10.255.255.255.
>> o) Mark RIP route as cost 16 after 180s.
>> p) One-to-all L2 delivery in local subnet.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Port allocation
>> b) FCS / CRC
>> c) ARP
>
>> [!example] Group B
>> n) Resolves logical IP addresses to physical MAC addresses.
>> o) PAT router shifts ports to avoid collisions.
>> p) Used to check Layer 2 frame corruption.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> p)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 0x0800
>> b) Dynamic NAT
>> c) ARP Cache
>
>> [!example] Group B
>> n) EtherType designating IPv4 payload.
>> o) Maps private IP to a public pool dynamically.
>> p) Maps IP addresses to physical MAC addresses.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)
