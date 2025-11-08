

## Exercise 01: MAC Addresses

> **Problem:**
> Given the following MAC addresses:
> a) `01-00-5E-AB-CD-EF`
> b) `00-00-25-47-EF-CD`
> c) `11-52-AB-9B-DC-12`
> d) `00-01-4B-B4-A2-EF`
> 1.  Give the type of each MAC address.
> 2.  Can these addresses belong to the "source address" field of an Ethernet frame? Justify.

###  Theory from Your Notes

Your notes contain a table that is key to solving this. It shows different MAC addresses and categorizes them. The core concept is:

*   **The first byte of the MAC address determines its type.**
*   Specifically, we look at the **very last bit** (the Least Significant Bit or LSB) of that first byte.
*   **Unicast:** If the last bit is `0`, the address points to a single, unique device. This is like a specific street address for one house. In hexadecimal, the second digit of the first byte will be an even number (0, 2, 4, 6, 8, A, C, E).
*   **Multicast:** If the last bit is `1`, the address points to a group of devices. This is like sending a flyer to everyone on a specific mailing list. In hexadecimal, the second digit of the first byte will be an odd number (1, 3, 5, 7, 9, B, D, F).
*   **Source Address Rule:** A computer sending data must identify itself uniquely. Therefore, the source MAC address (`@mac SRC` in your notes) **must always be a Unicast address**. A sender can't pretend to be a whole group. Your notes confirm this with a "oui" (yes) for unicast and "non" for multicast in the source address column.

###  Solution

#### 1. Type of each MAC address

Let's analyze the first byte of each address:

*   **a) `01-00-5E-AB-CD-EF`**
    *   First byte: `01`.
    *   In binary, `01` is `0000000**1**`. The last bit is `1`.
    *   **Type: Multicast**. This is consistent with your notes which list this exact address format as multicast.

*   **b) `00-00-25-47-EF-CD`**
    *   First byte: `00`.
    *   In binary, `00` is `0000000**0**`. The last bit is `0`.
    *   **Type: Unicast**.

*   **c) `11-52-AB-9B-DC-12`**
    *   First byte: `11`.
    *   In binary, `11` is `0001000**1**`. The last bit is `1`.
    *   **Type: Multicast**.

*   **d) `00-01-4B-B4-A2-EF`**
    *   First byte: `00`.
    *   In binary, `00` is `0000000**0**`. The last bit is `0`.
    *   **Type: Unicast**.

#### 2. Can they be a source address?

Based on the rule that source addresses must be unicast:

*   **a) Multicast:** **No**, it cannot be a source address.
*   **b) Unicast:** **Yes**, it can be a source address.
*   **c) Multicast:** **No**, it cannot be a source address.
*   **d) Unicast:** **Yes**, it can be a source address.

---

## Exercise 02: Ethernet Frame Analysis

> **Problem:**
> The following is an Ethernet frame (Preamble and FCS removed).
> `ffff ffff ffff 09ab 14d8 0548 0806 0001 0800 0604 0001 09ab 14d8 0548 7d05 300a 0000 0000 0000 7d12 6e03`
> 1.  Analyze the frame, identifying the MAC addresses, the 'Type' field, and the 'Data' field. What do you notice about the data field?
> 2.  Indicate the type of the destination MAC address.

###  Theory from Your Notes

Your notes show a clear diagram of an Ethernet frame structure. After the (removed) Preamble, the structure is:

```
+---------------------+-------------------+------------+-----------------+
| Destination MAC     | Source MAC        | EtherType  | Data (Payload)  |
| (6 Bytes)           | (6 Bytes)         | (2 Bytes)  | (Variable)      |
+---------------------+-------------------+------------+-----------------+
```

Your notes also analyze a similar frame, pointing out that `FFFF FFFF FFFF` is a **Broadcast** address and that the protocol involved is **ARP** (Address Resolution Protocol), which is identified by the `EtherType` value `0806`.

###  Solution

#### 1. Frame Analysis

Let's break down the hexadecimal data stream based on the frame structure:

*   **Destination MAC (first 6 bytes):**
    `ffff ffff ffff`
    *   This translates to **`FF:FF:FF:FF:FF:FF`**.

*   **Source MAC (next 6 bytes):**
    `09ab 14d8 0548`
    *   This translates to **`09:AB:14:D8:05:48`**.

*   **EtherType (next 2 bytes):**
    `0806`
    *   This value, `0x0806`, is the standard identifier for the **ARP (Address Resolution Protocol)**. This confirms what's hinted at in your notes. The purpose of ARP is to ask, "Who has this IP address? Tell me your MAC address."

*   **Data (the rest of the stream):**
    `0001 0800 0604 0001 09ab 14d8 0548 7d05 300a 0000 0000 0000 7d12 6e03`
    *   **What is remarkable about this field?** Since the EtherType told us this is an ARP packet, the data field itself has a specific structure. It's not just random data; it contains the ARP message. If we were to decode it, we would find the sender's MAC and IP addresses and the IP address of the device it's looking for. The presence of a structured protocol message *inside* the Ethernet data field is the key observation.

#### 2. Type of the Destination MAC address

*   The destination MAC address is `FF:FF:FF:FF:FF:FF`.
*   This is a special address. As shown in your notes, it is the **Broadcast** address.
*   A broadcast is a message sent to **every single device** on the local network segment. This makes sense for an ARP request—the sending machine doesn't know the specific MAC address it's looking for, so it shouts the question out to everyone on the network.

---

## Exercise 03: IP Address Analysis

> **Problem:** For each of the following IP addresses, determine if it is a valid and usable address. If so, indicate its class, network part, host part, network address, and broadcast address.

###  Theory from Your Notes

Your whiteboard photos provide a complete guide for this:

1.  **IP Address Classes:** The class is determined by the **first octet** (the first number).
    *   **Class A:** `0 - 127` (Binary starts with `0`)
    *   **Class B:** `128 - 191` (Binary starts with `10`)
    *   **Class C:** `192 - 223` (Binary starts with `110`)
    *   **Class D:** `224 - 239` (Multicast)
    *   **Class E:** `240 - 255` (Experimental)
2.  **Default Structure (Network.Host):**
    *   Class A: `Network.Host.Host.Host`
    *   Class B: `Network.Network.Host.Host`
    *   Class C: `Network.Network.Network.Host`
3.  **Special Addresses (Not usable for a regular device):**
    *   **Network Address:** The address where all host bits are `0`. It identifies the network itself.
    *   **Broadcast Address:** The address where all host bits are `1`. Used to send a message to all devices on the network.
    *   **Loopback:** The `127.x.x.x` range is reserved for testing the local machine (like talking to yourself).
    *   **Invalid Address:** Any octet greater than `255` is impossible.

###  Solution

Here is a detailed breakdown in a table format:

| IP Address | Valid/Usable? | Reason | Class | Network Part | Host Part | Network Address | Broadcast Address |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `131.107.256.80` | **Invalid** | The third octet `256` is greater than 255. | - | - | - | - | - |
| `127.1.1.1` | **Valid, but not usable** | Reserved for Loopback. | A | `127` | `1.1.1` | `127.0.0.0` | `127.255.255.255` |
| `255.255.255.255`| **Valid, but not usable** | This is the limited broadcast address. | E | - | - | - | - |
| `214.0.0.4` | **Valid and Usable** | A standard host address. | C | `214.0.0` | `4` | `214.0.0.0` | `214.0.0.255` |
| `222.222.255.222`| **Valid and Usable** | A standard host address. | C | `222.222.255` | `222`| `222.222.255.0` | `222.222.255.255` |
| `198.121.254.255`| **Valid, but not usable** | This is the broadcast address for the `198.121.254.0` network. | C | `198.121.254` | `255`| `198.121.254.0` | `198.121.254.255` |
| `132.4.0.5` | **Valid and Usable** | A standard host address. | B | `132.4` | `0.5` | `132.4.0.0` | `132.4.255.255` |
| `248.5.10.156` | **Valid, but not usable** | Belongs to Class E (Experimental). | E | - | - | - | - |
| `231.200.1.1` | **Valid, but not usable** | Belongs to Class D (Multicast). | D | - | - | - | - |
| `10.4.200.200` | **Valid and Usable** | A standard host address. | A | `10` | `4.200.200`| `10.0.0.0` | `10.255.255.255` |
| `126.1.0.0` | **Valid, but not usable** | This is the network address for the `126.0.0.0` network. | A | `126` | `0.0.0` | `126.0.0.0` | `126.255.255.255` |
| `191.48.54.100` | **Valid and Usable** | A standard host address. | B | `191.48` | `54.100`| `191.48.0.0` | `191.48.255.255` |

---

## Exercise 04: Global Message (Broadcast)

> **Problem:** You are given a list of machine IPs. Machine 1 (`192.175.60.3`) wants to send a global message on its network. Give the destination IP address it will use and the numbers of the machines that can respond to its request.

###  Theory from Your Notes

The whiteboard example for this exact problem (`Exo4`) shows the clear logic:

1.  To send a message to everyone on your *local network*, you use the network's **broadcast address**.
2.  To find the broadcast address, you first identify the network portion of your own IP address based on its class.
3.  You then take that network portion and set all the bits in the host portion to `1`. For a full octet, this is `255`.
4.  Only machines that share the **exact same network address** as the sender will receive and process this broadcast message.

###  Solution

1.  **Find Machine 1's Network and Broadcast Address:**
    *   Machine 1's IP: `192.175.60.3`.
    *   The first octet is `192`, so this is a **Class C** address.
    *   For Class C, the network part is the first three octets: `192.175.60`. The network address is `192.175.60.0`.
    *   To get the broadcast address, we take the network part and set the host part (the last octet) to all `1`s, which is `255`.
    *   The destination IP address will be **`192.175.60.255`**. Your whiteboard notes confirm this with "`L'@ du dest = 192.175.60.255`".

2.  **Identify Machines on the Same Network:**
    We need to check which machines have the same network part: `192.175.60`.

    *   Machine 1: `192.175.60.3` (The sender)
    *   Machine 2: `192.175.60.4` -> **Matches.**
    *   Machine 3: `192.176.60.3` -> Does not match (network is `192.176.60`).
    *   Machine 4: `192.175.60.5` -> **Matches.**
    *   Machine 5: `192.175.60.38` -> **Matches.**
    *   Machine 6: `172.175.60.38` -> Does not match (this is a Class B address on network `172.175.0.0`).
    *   Machine 7: `92.175.60.38` -> Does not match (this is a Class A address on network `92.0.0.0`).

The machines that can respond are **Machine 2, Machine 4, and Machine 5**.

---

## Exercise 05: Subnetting

> **Problem:**
> A machine M has the IP address `184.65.94.20`.
> 1. What is the class and the address of the network hosting M?
>
> Now, assume this network is given the subnet mask `255.255.240.0`.
> 2. How many subnets are possible, and how many machines can be hosted in each?
> 3. What is the subnet number (address) hosting M?
> 4. Which of the machines M1...M6 belong to the same subnet as M?

###  Theory from Your Notes

Your whiteboard (`Exo5`) and notebook pages cover this extensively. Subnetting divides a large network into smaller, more manageable pieces (subnets).

*   **Subnet Mask:** The subnet mask tells us which part of the IP address is the network/subnet and which is the host. The `1`s in the mask represent the network/subnet part, and the `0`s represent the host part.
*   **Borrowing Bits:** We create subnets by "borrowing" bits from the host part of the address and adding them to the network part.
    *   If we borrow `n` bits, we can create `2^n` subnets.
    *   If `h` bits are left for the host part, we can have `2^h - 2` usable host addresses per subnet. We subtract 2 for the subnet's own address and its broadcast address.
*   **Finding the Subnet Address:** The key operation is a **bitwise AND** between the machine's IP address and the subnet mask. This operation isolates the network/subnet portion of the address, giving you the address of the subnet it belongs to.

###  Solution

#### 1. Class and Network Address

*   Machine M's IP: `184.65.94.20`.
*   The first octet `184` is between 128 and 191, so this is a **Class B** address.
*   By default (without subnetting), the network address for a Class B is the first two octets, so it is **`184.65.0.0`**.

#### 2. Number of Subnets and Hosts

*   **Default Class B mask:** `255.255.0.0`
    *   In binary: `11111111.11111111.00000000.00000000`
*   **Given Subnet Mask:** `255.255.240.0`
    *   In binary: `11111111.11111111.11110000.00000000`

*   **Bits Borrowed (n):** By comparing the masks, we can see that **4 bits** have been borrowed from the host portion in the third octet.
*   **Number of Possible Subnets:** `2^n = 2^4 = **16 subnets**`.
*   **Host Bits Remaining (h):** The default Class B has 16 host bits (the last two octets). We borrowed 4.
    *   `h = 16 - 4 = 12` bits remain for hosts.
*   **Number of Hosts per Subnet:** `2^h - 2 = 2^12 - 2 = 4096 - 2 = **4094 usable hosts**`.

#### 3. Subnet Address of Machine M

We perform a bitwise AND between M's IP (`184.65.94.20`) and the subnet mask (`255.255.240.0`). The only interesting part is the third octet.

*   `94` in binary is `0101 1110`
*   `240` in binary is `1111 0000`

```
  0101 1110  (IP's 3rd octet: 94)
& 1111 0000  (Mask's 3rd octet: 240)
-----------------
  0101 0000  (Result in binary)
```
*   `0101 0000` in decimal is `64 + 16 = 80`.
*   Therefore, the subnet address for machine M is **`184.65.80.0`**.

#### 4. Machines on the Same Subnet

We perform the same AND operation for all other machines. A machine is on the same subnet if the result is also `184.65.80.0`.

| Machine | IP Address | 3rd Octet `AND` 240 | Resulting Subnet Address | Same Subnet? |
| :--- | :--- | :--- | :--- | :--- |
| M1 | `184.65.75.1` | `75 & 240 = 64` | `184.65.64.0` | No |
| M2 | `184.65.100.1` | `100 & 240 = 96` | `184.65.96.0` | No |
| M3 | `184.65.90.1` | `90 & 240 = 80` | `184.65.80.0` | **Yes** |
| M4 | `184.65.78.1` | `78 & 240 = 64` | `184.65.64.0` | No |
| M5 | `184.65.87.1` | `87 & 240 = 80` | `184.65.80.0` | **Yes** |
| M6 | `184.65.94.1` | `94 & 240 = 80` | `184.65.80.0` | **Yes** |

The machines on the same subnet as M are **M3, M5, and M6**.

---

## Exercise 06: Calculating Subnet Masks

> **Problem:** For each network ID and required number of subnets (SR), calculate the necessary subnet mask and the number of machines per subnet.

###  Theory from Your Notes

This exercise is the reverse of Exercise 5. The whiteboard table provides the answers, and the method is based on this logic:

1.  **Identify the Class:** Find the class of the network ID to know the default number of host bits available.
    *   Class A: 24 host bits
    *   Class B: 16 host bits
    *   Class C: 8 host bits
2.  **Find Bits to Borrow (n):** Given the required number of subnets (SR), find the smallest integer `n` such that `2^n ≥ SR`. Your notes show this formula as `n_bits = log2(N_SR)`.
3.  **Calculate the Subnet Mask:** Start with the default mask for the class and change the first `n` host bits from `0` to `1`.
4.  **Calculate Hosts per Subnet:** Find the number of remaining host bits, `h = (default host bits) - n`. The number of usable machines is `2^h - 2`.

###  Solution

This table breaks down the calculation for each case, matching the results on your whiteboard.

| NetID | Required SR | Class / Default Host Bits | Bits to Borrow (n) `(2^n ≥ SR)` | Mask Calculation | Final Mask | Machines/SR `(2^h - 2)` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `148.25.0.0` | 37 | **Class B** / 16 | `2^5=32` (too small), `2^6=64` (ok) -> **n=6** | `255.255.` followed by 6 ones: `11111100.0` -> `.252.0` | **`255.255.252.0`** | `h=16-6=10`. `2^10 - 2 = 1024 - 2 = **1022**` |
| `198.63.24.0`| 2 | **Class C** / 8 | `2^1=2` (ok) -> **n=1** | `255.255.255.` followed by 1 one: `10000000` -> `.128` | **`255.255.255.128`**| `h=8-1=7`. `2^7 - 2 = 128 - 2 = **126**` |
| `110.0.0.0` | 1000 | **Class A** / 24 | `2^9=512` (too small), `2^10=1024` (ok) -> **n=10**| `255.` followed by 10 ones: `11111111.11000000.0` -> `.255.192.0`| **`255.255.192.0`** | `h=24-10=14`. `2^14 - 2 = 16384 - 2 = **16382**` |
| `175.23.0.0` | 550 | **Class B** / 16 | `2^9=512` (too small), `2^10=1024` (ok) -> **n=10**| `255.255.` followed by 10 ones: `11111111.11000000` -> `.255.192` | **`255.255.255.192`**| `h=16-10=6`. `2^6 - 2 = 64 - 2 = **62**` |
| `209.206.202.0`| 60 | **Class C** / 8 | `2^5=32` (too small), `2^6=64` (ok) -> **n=6** | `255.255.255.` followed by 6 ones: `11111100` -> `.252` | **`255.255.255.252`**| `h=8-6=2`. `2^2 - 2 = 4 - 2 = **2**` |