---
sources:
  - "[[06.00 Introduction]]"
  - "[[06.01 Address Resolution Protocol (ARP) Deep Dive]]"
  - "[[06.02 Network Address Translation (NAT) & Port Address Translation (PAT)]]"
---

> [!question] The IP address block 172.16.0.0/12 is reserved for private network use.
>> [!success]- Answer
>> True

> [!question] Static NAT provides a one-to-one permanent mapping between private and public IP addresses.
>> [!success]- Answer
>> True

> [!question] Class A private IP address range is 10.0.0.0/8.
>> [!success]- Answer
>> True

> [!question] NAT was primarily developed to improve routing latency on WAN boundaries.
>> [!success]- Answer
>> False

> [!question] The EtherType value for an ARP frame in Ethernet II is 0x0806.
>> [!success]- Answer
>> True

> [!question] ARP is used to resolve IPv6 addresses to MAC addresses.
>> [!success]- Answer
>> False

> [!question] An ARP Request packet has the target hardware address set to the sender's MAC address.
>> [!success]- Answer
>> False

> [!question] Inbound packets entering a PAT router are translated by matching the destination port against the translation table.
>> [!success]- Answer
>> True

> [!question] Dynamic NAT maps private IP addresses to public IP addresses from a pool of registered public addresses.
>> [!success]- Answer
>> True

> [!question] The destination MAC address in an Ethernet header for an ARP Request is FF:FF:FF:FF:FF:FF.
>> [!success]- Answer
>> True

> [!question] What security advantage does PAT provide?
> a) Automatically filters malware downloads
> b) Encrypts all payload data passing through the router
> c) Conceals internal network topology and blocks unsolicited inbound traffic
> d) Protects against all Layer 7 application exploits
>> [!success]- Answer
>> c) Conceals internal network topology and blocks unsolicited inbound traffic

> [!question] What is the maximum number of concurrent translation sessions theoretically possible per public IP under PAT?
> a) Dependent on the IP pool size
> b) Unlimited
> c) Exactly 254
> d) Up to 65,536 (limited by port range)
>> [!success]- Answer
>> d) Up to 65,536 (limited by port range)

> [!question] What is the default value of the target hardware address field inside an ARP Request payload?
> a) FF:FF:FF:FF:FF:FF
> b) Randomly generated
> c) The sender's MAC address
> d) 00:00:00:00:00:00
>> [!success]- Answer
>> d) 00:00:00:00:00:00

> [!question] What CLI command displays the ARP cache on Cisco IOS devices?
> a) show arp
> b) arp -a
> c) show mac-address-table
> d) show ip route
>> [!success]- Answer
>> a) show arp

> [!question] What NAT type establishes a permanent one-to-one mapping between internal and external IP addresses?
> a) Dynamic NAT
> b) Static NAT
> c) Port Address Translation
> d) NAT Overload
>> [!success]- Answer
>> b) Static NAT

> [!question] Which IP address block represents the Class A RFC 1918 private range?
> a) 172.16.0.0/12
> b) 10.0.0.0/8
> c) 192.168.0.0/16
> d) 192.0.2.0/24
>> [!success]- Answer
>> b) 10.0.0.0/8

> [!question] What does the CAM table map?
> a) IP Address to MAC Address
> b) IP Address to Switch Port
> c) MAC Address to Switch Port
> d) Port Number to IP Address
>> [!success]- Answer
>> c) MAC Address to Switch Port

> [!question] How does a non-target host handle an incoming ARP Request broadcast?
> a) Forwards it to the default gateway
> b) Updates its ARP cache and drops it
> c) Replies with its own MAC address
> d) Drops the packet after comparing the target IP
>> [!success]- Answer
>> d) Drops the packet after comparing the target IP

> [!question] Which translation profile is best suited for an internal Web server that needs public inbound access?
> a) Static NAT
> b) Dynamic NAT
> c) PAT
> d) NAT Overload
>> [!success]- Answer
>> a) Static NAT

> [!question] What is the EtherType value for ARP in an Ethernet II frame?
> a) 0x0806
> b) 0x8100
> c) 0x86DD
> d) 0x0800
>> [!success]- Answer
>> a) 0x0806

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Hold-Down Timer
>> b) 172.16.0.0/12
>> c) 192.168.0.0/16
>
>> [!example] Group B
>> n) Class C private IP address block.
>> o) Class B private IP address block.
>> p) Ignores RIP updates with worse metrics for 60s.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Split Horizon
>> b) Registered Ports
>> c) Class B range limit
>
>> [!example] Group B
>> n) Never advertise route out ingress interface.
>> o) IANA registered vendor ports (range 1024 to 49151).
>> p) Ends at 172.31.255.255.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) arp -a
>> b) Static NAT
>> c) 0x0800
>
>> [!example] Group B
>> n) One-to-one permanent mapping of public/private IP.
>> o) Command to view local ARP cache on PC.
>> p) EtherType designating IPv4 payload.
>
>> [!success]- Answer
>> a) -> o)
>> b) -> n)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) 192.168.0.0/16
>> b) 10.0.0.0/8
>> c) PAT / Overload
>
>> [!example] Group B
>> n) Class A private IP address block.
>> o) Maps multiple private IPs to one public IP using ports.
>> p) Class C private IP address block.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Invalid Timer
>> b) FCS / CRC
>> c) NDP
>
>> [!example] Group B
>> n) Resolves L3 to L2 addresses in IPv6.
>> o) Used to check Layer 2 frame corruption.
>> p) Mark RIP route as cost 16 after 180s.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> o)
>> c) -> n)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Inside Global Address
>> b) ARP Cache
>> c) FF:FF:FF:FF:FF:FF
>
>> [!example] Group B
>> n) Public IP representing internal host on WAN.
>> o) Maps IP addresses to physical MAC addresses.
>> p) Layer 2 broadcast MAC address.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) arp -a
>> b) FCS / CRC
>> c) Private IP range
>
>> [!example] Group B
>> n) Command to view local ARP cache on PC.
>> o) Used to check Layer 2 frame corruption.
>> p) Non-routable IP spaces defined in RFC 1918.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> o)
>> c) -> p)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Target Hardware Address
>> b) CAM Table
>> c) Split Horizon
>
>> [!example] Group B
>> n) Maps MAC addresses to physical switch ports.
>> o) Never advertise route out ingress interface.
>> p) Unknown field set to zero in ARP Request.
>
>> [!success]- Answer
>> a) -> p)
>> b) -> n)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Perimeter Gateway
>> b) Class C range limit
>> c) FCS / CRC
>
>> [!example] Group B
>> n) Device where NAT translation occurs.
>> o) Used to check Layer 2 frame corruption.
>> p) Ends at 192.168.255.255.
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)

> [!question] Match the networking component or command with its correct definition or profile.
>> [!example] Group A
>> a) Perimeter Gateway
>> b) Well-Known Ports
>> c) Hold-Down Timer
>
>> [!example] Group B
>> n) Device where NAT translation occurs.
>> o) Ignores RIP updates with worse metrics for 60s.
>> p) Reserved system ports (range 0 to 1023).
>
>> [!success]- Answer
>> a) -> n)
>> b) -> p)
>> c) -> o)
