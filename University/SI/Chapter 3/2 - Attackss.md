

## Active Attacks in Detail 

Following the classification by *nature*, active attacks involve modifying data streams or system states.

### Masquerade (Identity Usurpation)

*   **Definition (Slide 18):** This attack occurs when one entity **pretends to be a different entity**.
*   **Mechanism:** An attacker assumes the identity of an authorized user or system component to gain unauthorized privileges or access.
*   **Significance:** It's considered a fundamental form of active attack, often being the origin or enabling factor for other active attacks like replay, modification, and denial of service.
*   **Example Scenario:** An attacker sends a message that appears to originate from a legitimate user (A) to another user (B).


### Replay

*   **Definition (Slide 19):** This attack is carried out in two phases:
    1.  **Passive capture** of a data unit (message, transaction).
    2.  Subsequent **retransmission** of this captured data unit to produce an unauthorized effect.
*   **Goal:** To trick the receiving system into processing the same valid (but old) message again, leading to unintended consequences.
*   **Example Scenario:** Capturing a legitimate bank transfer message from user A to B, where the attacker (Pirate) is the beneficiary, and then replaying it later to receive the funds again.


### Modification of Messages

*   **Definition (Slide 20):** This means that portions of a legitimate message are **altered**, or that messages are **delayed or reordered** to produce an unauthorized effect.
*   **Mechanism:** The attacker intercepts a message, changes its content, and then forwards it to the intended recipient.
*   **Example Scenario:**
    *   Original message: "Allow A to read confidential account files."
    *   Attacker intercepts and modifies it to: "Allow **Pirate** to read confidential account files."
    *   The modified message is then sent to the system managing access control.


### Denial of Service (DoS)

*   **Definition (Slide 21):** Prevents or inhibits the **normal use or management** of communication facilities or system resources.
*   **Targeting:**
    *   Can target a **specific entity:** e.g., suppressing all messages directed to a particular destination.
    *   Can target the **entire network:** Disrupting the network as a whole.
*   **Mechanisms:**
    *   Disabling the network itself.
    *   **Overloading** the network or a specific server with messages/requests to degrade performance or make it unresponsive.
*   **Goal:** To impact the **availability** of a service or resource.
[[Q5]]

---

## Classification by Targeted Objective (Slides 22-25)

This classification focuses on the primary goal the attacker aims to achieve concerning the information or system resources, aligning closely with security properties (Confidentiality, Integrity, Availability, Authenticity).

### Interception

*   **Targeted Security Property (Slide 22):** **Confidentiality** of information.
*   **Definition:** The attacker **intercepts information** circulating on the network, thereby gaining **unauthorized access** to it.
*   **Impact:** Involves **reading** data but **not modifying** it. No changes are made to the system state itself (though confidentiality is breached).
*   **Examples:**
    *   Eavesdropping on communications (like phone calls, network traffic) to capture data.
    *   Unauthorized copying of files or programs.
*   **Techniques:**
    *   **Sniffing:** Capturing network packets.
### Modification

*   **Targeted Security Property (Slide 23):** **Integrity** of data.
*   **Definition:** The attacker gains **unauthorized access** to a resource (data, program) and **alters** it.
*   **Impact:** Data or system behavior is changed without authorization.
*   **Examples:**
    *   Altering a program so it behaves differently (e.g., inserting malicious code).
    *   Deleting specific files on a server.
    *   Modifying the content of messages transmitted over the network (as seen in Active Attacks).
*   **Techniques:**
    *   **Malware** (viruses, worms, trojans) often perform modifications.
    *   Direct alteration of database records.
    *   Modifying packets in transit.

<!-- Placeholder for Modification diagram -->
<!-- ![Diagram showing normal flow Source -> Destination, with Attacker intercepting and altering the flow before it reaches Destination](placeholder_diagram_mod.png) -->

### Interruption

*   **Targeted Security Property (Slide 24):** **Availability** of resources.
*   **Definition:** This attack aims to make resources **unusable or inaccessible** to legitimate users.
*   **Impact:** Blocks transmitted messages, destroys resources, or renders systems non-functional.
*   **Examples:**
    *   Destruction of a hard drive.
    *   Cutting a communication line.
    *   Disabling a file management system.
    *   Denial of Service (DoS) attacks.
*   **Techniques:**
    *   **Flooding:** Overwhelming a target with traffic (network floods, SYN floods).
    *   **Smurf Attack:** A type of DDoS attack using ICMP echo requests.
    *   **Buffer Overflow:** Can sometimes crash a service, making it unavailable.
    *   Physical destruction.

<!-- Placeholder for Interruption diagram -->
<!-- ![Diagram showing flow from Source blocked before reaching Destination](placeholder_diagram_interruption.png) -->

### Fabrication

*   **Targeted Security Property (Slide 25):** **Authenticity** of entities and information.
*   **Definition:** The attacker **inserts counterfeit objects** (new information, fake messages) into the system in an unauthorized manner.
*   **Impact:** Creates false data or impersonates legitimate entities, undermining trust in the system's information or communication partners.
*   **Examples:**
    *   Inserting spurious (fake) messages into a network.
    *   Adding unauthorized records to a file or database.
    *   Impersonating a user to send fraudulent emails.
*   **Techniques:**
    *   **IP Spoofing:** Creating IP packets with a forged source IP address.
    *   **ARP Spoofing:** Sending fake ARP messages to associate the attacker's MAC address with the IP address of a legitimate host (leads to MitM or DoS).
[[Q6]]