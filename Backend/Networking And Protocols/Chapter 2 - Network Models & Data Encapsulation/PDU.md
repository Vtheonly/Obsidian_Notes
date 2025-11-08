
# Understanding Protocol Data Units (PDUs) and Encapsulation

This note explains the concept of a Protocol Data Unit (PDU) and the process of data encapsulation as visualized in the OSI model. This process is fundamental to preparing data for transmission across a network.

---

## The Encapsulation Process

> **Encapsulation** is the process where data moving down the OSI model layers is wrapped with headers and trailers from each respective layer. Each layer treats the information from the layer above it as its data payload.

As shown in the diagram, the process unfolds as follows:

1.  **Upper Layers (7-5):** The **Application**, **Presentation**, and **Session** layers generate the initial user **Data**.

2.  **Transport Layer (Layer 4):** The data is encapsulated into a **Segment** (or Datagram). A header is added containing the **Source and Destination Port** numbers, which identify the communicating applications.

3.  **Network Layer (Layer 3):** The segment is passed down and encapsulated into a **Packet**. An IP header is added, containing the **Source and Destination IP addresses** to route the data across networks.

4.  **Data Link Layer (Layer 2):** The packet is encapsulated into a **Frame**. This layer adds a header with the **Source and Destination MAC addresses** for local network delivery and a trailer, the **Frame Check Sequence (FCS)**, for error detection.

5.  **Physical Layer (Layer 1):** The frame is converted into a stream of **Bits** (e.g., `10010101011`) and transmitted as electrical signals, light pulses, or radio waves over the physical medium.

---

## PDU Summary by OSI Layer

This table summarizes the PDU at each of the lower four layers.

| OSI Layer      | PDU Name          | Key Information Added                                   |
| -------------- | ----------------- | ------------------------------------------------------- |
| 4: Transport   | **Segment/Datagram** | Source & Destination Port Numbers                       |
| 3: Network     | **Packet**        | Source & Destination IP Addresses                         |
| 2: Data Link   | **Frame**         | Source & Destination MAC Addresses, FCS Trailer          |
| 1: Physical    | **Bit**           | Raw binary stream for transmission                      |

---

> [!Note]
>  Building Blocks of Network Data
> Each PDU is a self-contained unit of information for its specific layer. The encapsulation process ensures that data has all the necessary addressing and control information to successfully travel from a source application on one device to a destination application on another.