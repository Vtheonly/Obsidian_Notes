# Information Security: Threats and Attacks

This document details the fundamental concepts related to threats and attacks in information security, based on the initial slides of a presentation, including attack methodology phases and basic classification.

## Threats

### Definition

*   A **threat** is a **potential cause of an incident**. It represents an event or action that, if realized, could cause **damage** to an asset (system, information, etc.).
*   It refers to an **incident likely to harm** a specific computer system or even an entire organization.
*   The concept of a threat encompasses various types of malicious actions aimed at harming a system, such as attacks, espionage, information theft, etc.

### Types of Threats

Threats can be broadly classified into two main categories:

*   **Accidental Threats (Non-intentional)**
    *   These threats **do not involve any premeditation** or intent to harm. They often result from errors, oversights, or unforeseen events.
    *   **Examples:**
        *   **Natural Events:** Fire, earthquake, flood, power outage.
        *   **User Error:** An employee mistakenly accessing incorrect information, mishandling equipment, accidental deletion.
        *   **Technical Failures:** Software bugs, hardware failures, other "uncontrollable" component failures.

*   **Intentional Threats**
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
[[Q1]]
## Attacks

### Definition and Context

*   Any computer connected to a computer network is **potentially vulnerable** to an attack.
*   An **attack** is a **malicious action** specifically intended to compromise the security of an asset (affecting its availability, integrity, or confidentiality).
*   An attack represents the **realization (concretization) of a threat**. For a threat to turn into a successful attack, it requires the **exploitation of a vulnerability** present in the target system.
*   An attack can only occur (and succeed) **if the targeted asset is affected by a vulnerability** that the attack can exploit.

### Prevalence of Attacks

*   On the Internet, attacks occur **constantly**. Several attacks per minute are often observed on each connected machine.
*   The majority of these attacks are launched **automatically** from previously infected machines (by viruses, Trojans, worms, etc.), often without the legitimate owner's knowledge.
*   More rarely, attacks are the result of targeted and deliberate action by a **malicious entity** (individual or group).
*   It is essential to **know the main types of attacks** to better prepare for and counter them.

## Attack Motivations and Objectives

The reasons attacks are carried out can be categorized into objectives (the technical goal) and motivations (the underlying reason).

### Objectives (What the attacker wants to *do*)

*   **Disinform:** Spread false information.
*   **Prevent access to a resource:** Denial of Service (DoS/DDoS) attacks.
*   **Take control of a resource:** Compromise a system for use.
*   **Recover information:** Theft of sensitive data, espionage.
*   **Use the compromised system to attack another (rebound/pivot):** Obscure the true origin of the attack.
*   **Etc.** (Other specific goals).

### Motivations (Why the attacker does it)

*   **Revenge/Grudge:** Personal motives against a target.
*   **Politics/Religion:** Hacktivism, cyberterrorism.
*   **Intellectual Challenges:** Proving skills, curiosity.
*   **Desire to harm others:** Pure malice.
*   **Impressing others:** Seeking recognition within a community.
*   **Information Theft:** For industrial or political espionage.
*   **Desire for money:** Ransomware, theft of banking details, fraud.
*   **Information Falsification:** Modifying data for personal gain or to cause harm.
*   **Etc.** (Other personal or ideological motives).
[[Q2]]
## Attacker Profiles

There are several attacker profiles, characterized by different factors:

### General Characteristics

*   **Their technical skills:** Level of expertise in IT and security.
*   **The time they are willing to spend to succeed:** Persistence and patience.
*   **Their motivations:** See the previous section.
*   **Their means/resources:** Financial, hardware, and software resources available.
*   **Their prior knowledge of the target:** Level of intelligence gathered before the attack.

### Types of Attacker Profiles (Hat Classification & Others)

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

## Attack Surface

### Definition

*   The **attack surface** is simply the **set of entry points or interaction points** through which a potential attacker can attempt to exploit a vulnerability to access or affect a system or data.
*   The larger and more complex the attack surface, the higher the likelihood it contains exploitable vulnerabilities.

### Components of the Attack Surface

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

<!-- Placeholder for attack surface diagram -->
<!-- ![Diagram showing a hacker targeting various components: Network, Application, Data, User, Hardware, OS, Power Supply, Environment](placeholder_diagram_attack_surface.png) -->

---

## Attack Methodology (Main Phases)

*   The methodology generally employed by attackers (hackers) to infiltrate a computer system.
*   The typical flow involves several distinct phases.
*   **(Diagram Reference)** The presentation shows a common 5-phase model: Reconnaissance, Scanning, Gaining Access, Maintaining Access, Covering Tracks.
*   **Other Methodology Frameworks:** Besides this common model, other structured frameworks exist, such as:
    *   **Cyber Kill Chain** (Lockheed Martin)
    *   **MITRE ATT&CK**

### Phase 1: Reconnaissance

*   **Definition:** The phase where the attacker **gathers all possible information** (technical, human) about the target, either passively or actively.
*   **Passive Gathering:** Collecting information **without directly interacting** with the target system.
    *   Examples: Search engines, Whois databases, social networks (finding info on clients, employees), public records, DNS lookups.
*   **Active Gathering:** **Directly querying or interacting** with the target system to gather information.
    *   Goal: Identify IP addresses, discover active services, map network topology.
*   **Example Tools:** NMAP (can be active), Maltego, Hping, search engines, Shodan.

### Phase 2: Scanning (Vulnerability Identification)

*   **Definition:** This process involves a **more in-depth investigation** based on reconnaissance findings. It helps the attacker analyze the target network or machine to **find exploitable vulnerabilities**.
*   **Three Important Steps:**
    1.  **Pre-attack Phase:** Analyzing the network to find specific information based on reconnaissance data (e.g., identifying live hosts, specific OS versions).
    2.  **Port Scanning:** Analyzing the target for information like open TCP/UDP ports, services running on those ports, and their versions.
    3.  **Information Extraction:** Gathering detailed information about live machines, OS details, network topology, routers, firewalls, servers, and potential vulnerabilities associated with discovered services/versions.
*   **Example Tools:** Nexpose, Nessus, NMAP, OpenVAS.

### Phase 3: Gaining Access

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

### Phase 4: Maintaining Access

*   **Definition:** This is the phase after the attacker has successfully gained initial access to the target system. The attacker tries to **maintain this access** to fulfill the ultimate goal of the attack (data exfiltration, long-term monitoring, etc.).
*   **Methods for Maintaining Access:**
    *   **Privilege Escalation:** (Often done in Gaining Access but crucial for maintaining control) Increasing privileges to the administrator level to install applications, modify/hide data.
    *   **Installing Backdoors:** Planting hidden software or configuration changes that allow easy re-entry into the system in the future, bypassing normal authentication.
    *   **Installing Rootkits:** Installing stealthy software (often at the kernel level) designed to hide the attacker's presence and activities, providing persistent, privileged access.
*   **Example Tool:** Metasploit (can be used to deploy payloads for persistence), various rootkits and backdoor tools.

### Phase 5: Covering Tracks (Erasing Traces)

*   **Definition:** An intelligent or cautious attacker will always attempt to **erase all evidence** of their presence and actions. The goal is to ensure that, later, no one can find traces leading back to them or even detect that a compromise occurred.
*   **Methods for Covering Tracks:**
    *   Clearing system cache and browser cookies/history.
    *   Modifying registry values (Windows).
    *   Modifying, corrupting, or deleting system and application logs (event logs, authentication logs, web server logs).
    *   Deleting any emails sent or received during the attack.
    *   Closing ports that were opened for the attack (less about hiding *past* action, more about cleanup).
    *   Uninstalling all tools, scripts, and applications used during the attack.
[[Q3]]
---

## Attack Classification

Attacks can be classified in several ways to better understand their nature and origin. The presentation outlines three main axes:

*   **By Attacker Location:** Internal vs. External
*   **By Attack Nature:** Passive vs. Active
*   **By Objective:** Interception, Modification, Interruption, Fabrication

*(Details for Objective-based classification are on later slides, but the overview is introduced here).*

### Classification by Attacker Location

*   **External Attack:**
    *   Initiated from **outside the organization's security perimeter**.
    *   Carried out by an **unauthorized or illegitimate user** of the system.
    *   Generally **more difficult to achieve** initially (must bypass perimeter defenses like firewalls) BUT often **easier to detect** (logs showing external connections, firewall alerts).
*   **Internal Attack:**
    *   Initiated by an entity **within the security perimeter**.
    *   Often involves an **authorized entity** (e.g., employee, contractor) accessing system resources but **using them in an unapproved or malicious manner**.
    *   Generally **easier to achieve** (attacker is already inside, potentially with some level of trust/access) BUT often **more difficult to detect** (actions might seem legitimate initially).

<!-- Placeholder for internal/external attack diagram -->
<!-- ![Diagram showing external attacker outside firewall and internal attacker inside network](placeholder_diagram_location.png) -->

### Classification by Attack Nature

*   **Passive Attacks:**
    *   Attempt to **learn or make use of information** from the system **without affecting system resources** or operations.
    *   Primarily involves **listening to or monitoring transmissions** on a channel.
    *   The goal is to **intercept transmitted information**.
    *   **Two main types:**
        1.  **Reading Message Contents (Eavesdropping):** Capturing data sent in cleartext.
        2.  **Traffic Analysis:** Observing patterns of communication even if the content is encrypted.
    *   Characteristics: **Relatively difficult to detect** (as they don't alter data or system state), but potentially **easier to prevent** (e.g., through encryption).

*   **Active Attacks:**
    *   Attempt to **alter system resources or affect their operation**.
    *   Involve some **modification** of the data stream or the **creation** of a false stream.
    *   Actions include unauthorized and deliberate **modification, suppression, or creation** of data or system state.
    *   Result: Causes **damage or alteration** to the system's integrity or availability.
    *   Characteristics: **Detection is generally easier** (as changes occur), but detection might happen **too late** after damage is done.

### Passive Attacks in Detail (Slide 17)

*   **1. Reading Message Contents:**
    *   Occurs when data is sent **in cleartext** (e.g., unencrypted phone calls, emails, files, web traffic).
    *   This data might contain **sensitive or confidential information**.
    *   **Prevention:** Using **encryption** makes message contents unreadable to eavesdroppers.

*   **2. Traffic Analysis:**
    *   Even if messages are **unreadable (encrypted)**, an adversary **can still analyze traffic patterns**.
    *   They can observe:
        *   Location and identity of communicating hosts.
        *   Frequency and length of messages exchanged.
        *   Timing of communications.
    *   Usefulness: This information can be used to **infer the nature of the communication** taking place, even without knowing the exact content.

[[Q4]]