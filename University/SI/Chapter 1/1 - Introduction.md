
# Introduction to Computer Security


## Definition

### Security

**Information**
*(Image: Database icon, data chart, folder with social media icons)*

**Computer System**
*(Image: Servers, Oracle database servers, desktop/laptop computers, Windows/Linux servers)*

**Information System**
*(Diagram showing an Information System involves collecting, grouping, classifying, processing, and disseminating INFORMATION using IT (Computer Systems) based on USES by USERS.)*
*   **Components:**
    *   Collect
    *   Group
    *   Classify
    *   Process
    *   Disseminate
*   **Elements:** USERS, Uses, IT (Computer System), INFORMATION

---

## Security

*   **Information Security:**
    *   A set of management strategies, processes, and policies aimed at **protecting, detecting, identifying, and countering** threats targeting **digital or non-digital information**.

*   **Computer Security:**
    *   The set of means implemented to reduce the vulnerability of a **computer system** against accidental or intentional threats it may face.
    *   In other words, it's the set of techniques ensuring that the **resources of an information system (hardware or software)** of an organization are used **only as intended**.

*   **IS Security (Information System Security):**
    *   The set of technical, organizational, legal, and human means necessary to implement measures aimed at preventing **unauthorized use, misuse, modification, or diversion** of the **information system**.

---

## Computer Security in Context

The term **computer security** as used in jargon is a generic term that applies to networks, the Internet, endpoints, APIs, the cloud, applications, container security, and others.

It encompasses the methods, techniques, and tools implemented for the **protection of systems, data, and services against accidental or intentional threats**.

---

## Computer Security in Context (Objectives)

*   Security aims to **reduce the risks** affecting the information system, to **limit their impacts** on the organization's operations and business activities...

*   Security management within an information system is not intended to be obstructive. On the contrary:
    *   It contributes to the **quality of service** that users are entitled to expect.
    *   It guarantees personnel the **level of protection** they are entitled to expect.

---

## Information Systems Security

*(Diagram showing layers of an Information System and its security)*

*   **Core:** USERS, Uses, IT (Computer Systems), INFORMATION
*   **Technical Security Controls (Inner Ring):** SSH, SSL/TLS, IDS, Firewall, HTTPS, Cryptography, VPN, Tor
*   **Security Layer:** Manages controls and policies.
*   **Threats (Middle Ring):** Malware, Ransomware, XSS, Backdoor, Virus, Worm
*   **Adversaries & Attack Vectors (Outer Ring):** Threat, Adversaries, Espionage (State), Hacker, Cracker, Pirates, Social Engineering, Adware, Colleagues (Insider Threat), Cybercriminal, Script Kiddies, Amateur, Government

---

## Security Stakes/Challenges

**Stakes:**

*(Diagram showing IS Security at the center, influenced by surrounding impacts)*

*   **Financial Impacts** *(Image: Bank facade)*
*   **Legal and Regulatory Impacts** *(Image: Scales of justice)*
*   **Image and Reputation Impacts** *(Image: Modern building exterior)*
*   **Organizational Impacts** *(Image: Person drawing an org chart)*

---

## Security Stakes/Challenges

**Why are attackers interested in organizational Information Systems or individual PCs?**

*   **Motivations evolve:**
    *   80s and 90s: Often enthusiastic tinkerers/hobbyists exploring systems.
    *   Nowadays: Predominantly organized and deliberate actions.

*   **Cybercrime / Delinquency Motivations:**
    *   Individuals motivated by financial gain.
    *   "Hacktivists" (hacking for political/social causes).
    *   Political, religious, ideological motivation.
    *   Direct competitors of the targeted organization.
    *   State-sponsored actors (government employees/contractors).
    *   Mercenaries acting on behalf of clients (hacking-for-hire).
    *   ...

---

## Security Stakes/Challenges

**Why are attackers interested...? (Specific Goals)**

*   **Financial Gains** (access to information, then monetization and resale)
    *   User accounts, emails
    *   Internal company organization details, plans
    *   Customer files, client lists
    *   Passwords, bank account numbers, credit cards

*   **Resource Utilization** (then resale or provision as a "service")
    *   Bandwidth & storage space (hosting illegal music, movies, C&C servers, etc.)
    *   Zombies (compromised machines forming botnets)

*   **Blackmail / Extortion**
    *   Denial of service (demanding payment to stop attack)
    *   Data modification / destruction (demanding payment to restore)
    *   Ransomware (encrypting data, demanding payment for decryption key)

*   **Espionage**
    *   Industrial / competitive (stealing trade secrets, R&D)
    *   State-sponsored (gathering intelligence, political disruption)

---

## Security Stakes: Cyberattacks

**Some examples of attacks:**

*   *(Image 1: Screenshot of Algerian news site chouroukonline.com reporting on a DDoS attack they suffered in 2009, attributed to Egyptian sources related to football tensions.)*
    **Attack against the "chouroukonline" site in 2009 via a DDoS attack.**

*   *(Image 2: Screenshot of an Egyptian Ministry website defaced by Algerian hackers "Team Dos-Dz" in apparent retaliation.)*
    **Retaliation: Attack against the Egyptian ministry site by the "Team Dos-Dz" hacker group.**

---

## Computer Security Objectives

Ensuring the security of a computer system involves achieving a set of objectives to guarantee the protection of information against any disclosure, alteration, or destruction. Access to this information must also be controlled through protected access.

*(Diagram: Wheel with "Objectives" at the center)*
*   **Confidentiality**
*   **Integrity**
*   **Availability**
*   **Identification**
*   **Authentication**
*   **Authorization**
*   **Non-repudiation**
*   **Traceability / Auditability**

---

## Triad of Fundamental Security Properties

**CIA Triad (or CID Triad)**

*(Diagram: Triangle showing the three core components)*
*   **Confidentiality**
*   **Integrity**
*   **Availability**

---

## Triad of Fundamental Security Properties

*   **Confidentiality:**
    *   Aims to ensure that only **authorized** entities (people, machines, software) have access to resources and information they are entitled to.
    *   The goal of attacks on confidentiality is to **exfiltrate or steal information**.
    *   **Threats:**
        *   Network eavesdropping (sniffing)
        *   File theft
        *   Espionage
        *   Social engineering
    *   **Countermeasures:**
        *   Cryptography (encryption)
        *   Access control (Logical: passwords, tokens; Physical: biometrics, locks)
        *   Asset classification
        *   Personnel training
    *(Image: Laptop screen with a padlock icon)*

---

## Triad of Fundamental Security Properties

*   **Integrity:**
    *   Aims to ensure that resources and information are **not corrupted or altered** by unauthorized entities.
    *   Data or messages cannot be modified without the relevant parties being aware (or able to detect it).
    *   The goal of attacks on integrity is to **change, add, or delete** information or resources.
    *   **Threats:**
        *   Malicious attacks (Worms, viruses, Logic bombs modifying data)
        *   Unauthorized modification
    *   **Countermeasures:**
        *   Cryptography (Hashing, Digital signatures, Message Authentication Codes - MACs)
        *   Access controls
        *   Version control, backups
    *(Image: Illustrates altering a check - Original: 1000DA, Altered (added): 100000DA, Altered (deleted): DA)*

---

## Triad of Fundamental Security Properties

*   **Availability:**
    *   Ensures that authorized users can access information or services provided by the system **when needed**.
    *   The goal of attacks on availability is to render the system **unusable or inaccessible**.
    *   **Threats:**
        *   Malicious attacks (Denial of Service - DoS, Distributed DoS - DDoS)
        *   Accidental issues (e.g., the "Slashdot effect" - overwhelming legitimate traffic; hardware failure; software bugs)
        *   Outages/Failures (power, network)
    *   **Countermeasures:**
        *   Firewalls (to block malicious traffic)
        *   Intrusion Detection/Prevention Systems (IDS/IPS)
        *   Redundancy (servers, network links, power)
        *   Backups and Disaster Recovery plans
        *   Load balancing
        *   Administrator training
    *(Image: Server rack with one marked offline (X) and one online (check), "SERVICE 7j/7" logo)*

---

## Security Objectives Beyond the Triad

*   **Identification:**
    *   Information allowing an entity (user, system) to **claim an identity**.
    *   Basic identification is often the username entered into a computer system.
    *(Image: Google login screen asking for email or phone number)*

---

## Security Objectives Beyond the Triad

*   **Authentication:**
    *   Information used to **verify the claimed identity**, confirming you are who you say you are.
    *   Basic authentication is often the password entered after providing a username.
    *   **Strong authentication** typically combines multiple factors, like something you know (password), something you have (token, phone), and/or something you are (biometrics).
    *(Image: Google login screen asking for password after username)*

---

## Security Objectives Beyond the Triad

*   **Authorization:**
    *   Information determining which company resources an **authenticated** user is **permitted to access**, and what actions (read, write, delete, execute) are allowed on those resources.
    *   This covers all types of company resources.
    *   Access criteria can be based on various factors:
        *   Roles (Role-Based Access Control - RBAC)
        *   Groups
        *   Location
        *   Time of day
        *   Type of transaction
    *(Diagram: User -> assigned a Role -> associated Permissions [Grant/Deny])*

---

## Security Objectives Beyond the Triad

*   **Non-repudiation:**
    *   Provides proof of origin and/or delivery.
    *   **Non-repudiation of origin:** The sender cannot falsely deny having sent the message. (Proof of who sent it).
    *   **Non-repudiation of transmission/delivery:** The recipient cannot falsely deny having received the message (Proof of delivery). Often combined with integrity checks to prove the *content* sent/received.
    *   Mechanism ensures that a message was verifiably sent by a specific sender and/or received by a specific recipient.
    *(Images: Diagram 1 - Sender denies sending a transfer. Diagram 2 - Sender sent 500$ but recipient claims 1500$ was supposed to be sent, or sender denies sending that specific amount.)*

---

## Security Objectives Beyond the Triad

*   **Traceability / Auditability:**
    *   The set of mechanisms allowing the tracking and recording of operations performed on company resources and by whom.
    *   This implies that all relevant application and system events are logged (archived) for later investigation and auditing.
    *   Example: System logs, application logs, network logs, audit trails.
    *(Images: Magnifying glass over footprints suggesting investigation; Diagram showing email flow from Sender to Receiver via servers, implying the path can be traced)*

---

## Main Concepts of Computer Security

*   **Asset:**
    *   Any element that has **value** to the organization (e.g., hardware, software, information, reputation, personnel).
    *   Important elements of an organization are the components of its capital (in a broad sense) that enable it to conduct its business. These are commonly called **assets**.
    *(Diagram showing hierarchy)*
        *   **Primary Assets:** Business processes and information.
        *   **Supporting Assets:** Site (facilities), Personnel, Hardware, Network, Software, Organization (structure, policies).

---

## Main Concepts of Computer Security

*   **Vulnerability:**
    *   A **weakness** in an asset or control (at the design, implementation, installation, configuration, or usage level) that can be exploited by a threat actor.
    *   Represents the level of exposure of an asset to a threat in a specific context.
    *   A security weakness can be technical/logical or physical.
    *   **Example Vulnerabilities (from ISO 27005 Annex D):**
        *   Lack of a firewall
        *   Server misconfiguration
        *   Poor password management
        *   Sending sensitive messages in clear text
        *   Untrained personnel
    *(Image: Server icon with arrows pointing towards it, signifying potential weak points)*

---

## Main Concepts of Computer Security

*   **Threat:**
    *   A potential **cause of an unwanted incident**, which could result in harm to a system or organization (damage to assets).
    *   An action or event capable of causing harm. Refers to any intent or method used (by a threat actor/source) to exploit a vulnerability.
    *   **Example Threats (from ISO 27005 Annex C):**
        *   Physical damage: Fire, dust, water damage...
        *   Natural event: Earthquake, flood, storm...
        *   Information compromise: Data interception, equipment theft, espionage...
        *   Technical failures: Malfunction of equipment or software...
        *   Malicious actors: Hackers, malware, malicious insiders...
    *(Image: Server (asset) facing threats: Malicious code icon, Malicious intern causing service loss, External attackers)*

---

## Main Concepts of Computer Security

*   **Attack:**
    *   A **malicious action** intended to compromise the security of an asset (exploit a vulnerability). An attack represents the **realization (or attempt)** of a threat.
    *   An attack requires the **exploitation of a vulnerability** by a threat actor.
    *   An attack can only occur (and potentially succeed) if the targeted asset possesses a relevant vulnerability.
    *   Any action that exploits one or more vulnerabilities (flaws) to carry out a threat with harmful intent.
    *   **Example Attacks:**
        *   SQL injection
        *   Cross-Site Scripting (XSS)
        *   Cross-Site Request Forgery (CSRF)
        *   Buffer overflow
        *   Distributed Denial of Service (DDoS)
    *   *Note: While the ideal goal of security experts is to ensure the IS has no vulnerabilities, in reality, the objective is to effectively manage these vulnerabilities rather than aiming for an unattainable goal of zero vulnerabilities.*
    *(Image: Icons representing attackers launching malicious code/bombs towards a server)*

---

## Main Concepts of Computer Security

*   **Countermeasure / Control:**
    *   The set of actions, devices, procedures, or techniques implemented to **reduce or eliminate risk** by mitigating threats, reducing vulnerabilities, or lessening the impact of an incident.
    *   **Example Countermeasures:**
        *   **Physical:**
            *   Installation of surveillance cameras (deterrence, detection)
            *   Installation of access control devices (locks, badges)
        *   **Technical:**
            *   Intrusion Detection/Prevention Systems (IDS/IPS)
            *   Firewall
            *   Virtual Private Network (VPN) (for confidentiality/integrity over public networks)
            *   Antivirus software
            *   HTTPS (encryption for web traffic)
            *   Backups
            *   Patching
    *(Image: Firewall icon acting as a barrier, blocking malicious code icons from reaching a server)*

---

## Main Concepts of Computer Security (Analogy)

*(Analogy using COVID-19 to illustrate concepts)*

*   **Threat:** Corona virus (SARS-CoV-2)
    *(Image: Virus particles)*
*   **Vulnerability:** Not wearing a mask / Poor hygiene / Lack of vaccination
    *(Image: Person without a mask)*
*   **Impact:** Experiencing symptoms / Getting sick / Hospitalization / Spreading the virus
    *(Image: Person sick in a hospital bed)*
*   **Countermeasure:** Wearing a mask / Good hygiene / Vaccination / Social distancing
    *(Image: Person wearing a mask and using hand sanitizer)*

---

## Information Security Management System (ISMS)

*   An ISMS is a **systematic approach** to managing sensitive company information so that it remains secure. It includes people, processes and IT systems by applying a risk management process.
*   It helps **establish, implement, operate, monitor, review, maintain, and continually improve** an organization's information security to achieve business objectives, based on a risk assessment and the organization's risk acceptance levels.
*   An ISMS consists of the set of **policies, standards, procedures, practices, organizational structures, roles & responsibilities, behaviors, and planned activities** that an organization uses to protect its critical information assets.
*   It provides a clear understanding of the **objectives and context** of information security both inside and outside the organization.
*   Successful ISMS implementations provide a practical and pragmatic framework for the **identification, assessment, and treatment** of information security risks.

---

## Standards and Methods for Securing an IS

*   Cybersecurity standards can be defined as the essential means by which the direction described in a company's cybersecurity strategy and policies is transformed into **actionable and measurable criteria**. They provide established best practices.

*   Several international standards for managing computer security exist:
    *   **ISO/IEC 27002 (formerly ISO 17799):** Provides a code of practice, offering guidelines and best practices for information security controls based on internationally recognized standards. It serves as a reference for selecting controls within the ISMS implementation process.
    *   **ISO/IEC 27000 series:** A family of standards dedicated to Information Security Management Systems (ISMS). Key standards include:
        *   **ISO/IEC 27000:** Overview and vocabulary.
        *   **ISO/IEC 27001:** Requirements for establishing, implementing, maintaining and continually improving an ISMS. (This is the main standard organizations get certified against).
        *   **ISO/IEC 27005:** Guidance on information security risk management.

---

## ISO 27000 Family of Standards

*   The ISO 27000 family of standards helps organizations ensure the security of their information. These standards facilitate information security management through a systematic approach.
*   The ISO/IEC 27000 family describes ISMS requirements and provides guidance on a multitude of methods, controls, and security measures.

*   **Key Standards in the Family:**
    *   **Overview & Vocabulary:** ISO 27000
    *   **ISMS Requirements:** ISO 27001 (Certification Standard)
    *   **Code of Practice (Controls):** ISO 27002 (Guidance on implementing controls listed in Annex A of 27001)
    *   **Implementation Guidance (ISMS):** ISO 27003
    *   **Metrics & Measurement:** ISO 27004
    *   **Risk Management:** ISO 27005
    *   **Audit & Certification Requirements (for Certification Bodies):** ISO 27006
    *   **Audit Guidelines (for ISMS):** ISO 27007, ISO 27008
    *   **Sector-Specific Guidelines:** e.g., ISO 27011 (Telecom), ISO 27017 (Cloud), ISO 27018 (Cloud PII), ISO 27799 (Health), etc.

---

## ISO 27001 Standard: ISMS

The ISO 27001 standard is process-oriented and recommends the **PDCA (Plan-Do-Check-Act)** continual improvement model to establish, implement, operate, monitor, review, maintain, and improve the ISMS.

**PDCA Cycle for ISMS:**

*   **Plan (Establish the ISMS):**
    1.  Define the scope, context, and policy of the ISMS.
    2.  Conduct a risk assessment (Identify, analyze, evaluate risks).
    3.  Select control objectives and controls; Produce a Statement of Applicability (SoA); Develop the risk treatment plan.
*   **Do (Implement and Operate the ISMS):**
    4.  Implement the risk treatment plan and the selected controls; Manage operations; Implement programs (e.g., awareness).
*   **Check (Monitor and Review the ISMS):**
    5.  Monitor, measure, analyze, and evaluate ISMS performance and effectiveness (Validation):
        *   Internal Audits
        *   Management Reviews
        *   Vulnerability assessments / scans
        *   Penetration tests (optional but common)
        *   Measure control effectiveness
*   **Act (Maintain and Improve the ISMS):**
    6.  Address non-conformities; Implement preventive and corrective actions based on check results; Continually improve the ISMS.

---

## ISO 27001 Standard: ISMS (PDCA Cycle - Plan Phase)

*(PDCA Diagram with the 'Plan' section highlighted)*

**Plan (Establish the ISMS):**
1.  Define the scope, context, and policy of the ISMS.
2.  Conduct a risk assessment (Identify, analyze, evaluate risks).
3.  Select control objectives and controls; Produce a Statement of Applicability (SoA); Develop the risk treatment plan.

*(Rest of Do, Check, Act phases as described previously)*

*This slide highlights the **Plan** phase.*

---

## Step 1: Identifying the Security Scope (Plan Phase)

*   Define the scope to be managed within the ISMS: This can be geographic, but is primarily defined in terms of **business activities, functions, or specific systems**.
*   **Mapping and classification of assets** within the defined scope is crucial.
*   Identify vital resources or **assets** to be protected:
    *   **Hardware** (computers, servers, network equipment, mobile devices, etc.)
    *   **Software** (OS, applications, source code, utilities, etc.)
    *   **Data / Information** (databases, files, backups, intellectual property, etc.)
    *   **People** (employees, contractors, skills, knowledge)
    *   **Services** (network connectivity, power, HVAC)
    *   **Intangibles** (reputation, brand image)
*   The choice of scope is an organizational decision, often starting small and expanding.
*   Identify **critical elements** within the scope that require the highest level of protection.

*(Diagram shows network segmentation for Finance, IT, HR services, servers, and internet connectivity)*
*(Table shows an example asset inventory/classification: Format: Asset Type | ID | Name | Owner | Description... Example: Hardware | M000001 | Server1 | IT Service | ...)*

---

## Step 2: Risk Management (Plan Phase)

**Risk Management Methods:**

*(Logos/diagrams illustrate several common methodologies)*

*   **ANSSI EBIOS Risk Manager:** (French cybersecurity agency method) Focuses on digital risk scenarios related to business objectives. Iterative process involving context setting, threat source analysis, target scenario building, risk assessment, and treatment.
*   **MEHARI:** (Method for Harmonized Analysis of Risks - France) Comprehensive method focusing on classifying stakes, auditing services/controls, detecting critical risks, analyzing risk situations, and defining action plans.
*   **OCTAVE:** (Operationally Critical Threat, Asset, and Vulnerability Evaluation - Carnegie Mellon SEI, USA) A framework focusing on organizational risk assessment. Different variations exist (OCTAVE-S for smaller orgs). Generally involves phases: Build Asset-Based Threat Profiles (Organizational View), Identify Infrastructure Vulnerabilities (Technological View), Develop Security Strategy and Plans.
*   **CRAMM:** (CCTA Risk Analysis and Management Method - UK Government origin) Structured method involving asset identification/valuation, threat/vulnerability assessment leading to risk calculation, countermeasure identification/selection, and implementation support.

---

## Step 2: Risk Management (Plan Phase)

**ISO/IEC 27005**

*   The ISO/IEC 27005 standard provides guidelines for **information security risk management** compatible with the ISMS described in ISO 27001.
*   The risk management process includes the following main activities:
    *   **Context Establishment:** Define scope, criteria (risk evaluation, impact, acceptance), organization.
    *   **Risk Assessment:**
        *   **Risk Identification:** Identify assets, threats, existing controls, vulnerabilities, consequences.
        *   **Risk Analysis:** Determine likelihood and impact; estimate the level of risk.
        *   **Risk Evaluation:** Compare risk levels against acceptance criteria; prioritize risks for treatment.
    *   **Risk Treatment:** Select and implement risk treatment options (Avoid, Mitigate, Transfer, Accept).
    *   **Risk Acceptance:** Management formally accepts residual risks.
    *   **Risk Communication and Consultation:** Ongoing throughout the process.
    *   **Risk Monitoring and Review:** Continuously monitor risks, controls, and the context.

*(Diagram shows the ISO 27005 process flow: Establish Context -> Risk Assessment [Identify -> Analyze -> Evaluate] -> Risk Treatment -> Risk Acceptance. Communication & Consultation and Monitoring & Review are ongoing activities encompassing the entire process.)*

---

## Step 2: Risk Analysis (Plan Phase)

**Risk Assessment > Risk Analysis > Risk Identification & Estimation**

*   Risk analysis serves to identify, estimate, and prioritize risks affecting the organization's assets stemming from the operation and use of information systems.

*   **Key Questions & Concepts:**
    *   What are the system's **vulnerabilities (1)**? (Weaknesses)
    *   What are the **threats (2)** that could exploit these vulnerabilities? (Potential causes of harm)
    *   What is the potential **impact (3)** if a threat exploits a vulnerability? (Consequences)
    *   What is the **probability (likelihood) (4)** that the threat will occur and exploit the vulnerability? (Chance of happening)

*   **Risk:** Generally understood as the combination of the **likelihood (probability)** of an event occurring and its **consequences (impact)**. (Ref: ISO/IEC Guide 73:2002).

*(Diagram shows Risk as the intersection/combination of Threat, Vulnerability, and Impact, influenced by Likelihood/Probability)*

*   *Note: Since absolute security does not exist, the company must determine the level of risk it is prepared to accept (risk appetite) for its resources, considering the potential impact versus the cost of implementing controls (risk treatment).*

---

## Example: Password Hijacking / Theft (Risk Perspective)

*   **Threat:** Password hijacking/theft (e.g., via network sniffing)
    *(Image: Graphic depicting password theft)*
*   **Vulnerability:** Sending the password unencrypted over the network (e.g., using plain HTTP for login)
    *(Image: Login form asking for name/password)*
*   **Risk:** Unauthorized access leads to account compromise / loss of control over the account.
    *(Image: Screen saying "YOU HAVE BEEN HACKED!")*

---

## Example: Password Hijacking / Theft (Attack & Countermeasure)

*   **Attack:** Man-in-the-Middle (MitM) attack where a pirate intercepts the unencrypted password during transmission.
    *(Diagram: Attacker between user and server intercepting plain PASSWORD)*
*   **Countermeasure:** Encrypt the password before sending it / Encrypt the entire communication channel (e.g., using HTTPS instead of HTTP).
    *(Diagram: Attacker between user and server, but communication is encrypted (lock icon) and cannot be read or is blocked)*

---

## Step 2: Risk Analysis (Plan Phase)

**Risk Estimation:**

*   The risk equation (or concept) summarizes the approach and allows evaluating the **risk level**, i.e., the criticality of the risk. While sometimes represented by a formula, it's often a conceptual model rather than a strict mathematical calculation, especially in qualitative analysis.

*   Conceptual Formula:
    *(Considering Likelihood/Probability of Occurrence)*
    **Risk Level ≈ Likelihood * Impact**
    *(Where Likelihood depends on Threat & Vulnerability factors)*

*   Depending on the circumstances, data availability, and requirements, risk estimation methodologies can be:
    *   **Qualitative:** Using descriptive scales (e.g., High, Medium, Low).
    *   **Quantitative:** Using numerical values (e.g., monetary loss, frequency).
    *   **Semi-Quantitative:** A combination or hybrid approach.

*(Diagram: Venn diagram showing Risk influenced by Vulnerability, Impact, and Threat factors)*

---

## Step 2: Risk Analysis (Plan Phase)

**Risk Estimation Methods:**

*   **Qualitative Estimation:**
    *   Does not assign numerical values but uses descriptive scales (e.g., Low, Medium, High; or 1-5 ratings) to assess likelihood and impact.
    *   Provides an **assessment or appreciation** of the risk level.
    *   Useful when numerical data is unavailable or difficult to obtain, or for initial high-level assessments.
    *   Relies heavily on subjective judgment, expertise, and experience.
    *   **Data:** Subjective opinions, expert judgment.

*   **Quantitative Estimation:**
    *   Aims to **numerically characterize** the risk components.
    *   Determines metrics like Annualized Loss Expectancy (ALE), probability of occurrence (e.g., failure rate), financial cost of consequences.
    *   Requires sufficient objective data for meaningful calculations.
    *   Often involves mathematical modeling, statistical analysis, and financial analysis.
    *   **Data:** Objective, measurable, often historical data (e.g., incident frequency, repair costs, downtime costs).

---

## Step 2: Risk Analysis (Plan Phase)

**Risk Characterization [Example using a Risk Matrix - ref: Ebios, ANSSI]:**

*   To characterize risks, a risk assessment matrix is commonly used. This matrix plots the estimated **Impact** against the estimated **Probability (Likelihood)** to determine a resulting risk level.
*   Example 3x3 evaluation matrix (Colors: Red=High, Yellow=Medium, Green=Low):

| Impact    ↓ / Likelihood → | Improbable    | Probable      | Very Probable |
| :----------------------- | :------------ | :------------ | :------------ |
| **High (Severe)**        | Medium (Yellow) | High (Red)    | High (Red)    |
| **Medium**               | Low (Green)   | Medium (Yellow) | High (Red)    |
| **Low**                  | Low (Green)   | Low (Green)   | Medium (Yellow)|

---

## Step 2: Risk Analysis (Plan Phase - Process Flow)

*(Diagram illustrating the risk analysis process leading to risk ranking)*

1.  **Identify Assets to Protect:** What is valuable?
2.  **Identify Threats:** What dangers exist for these assets?
3.  Assess Potential **Impact:** How bad would it be if the threat occurs? (e.g., Low, Medium, High)
4.  Assess **Likelihood (Probability):** How likely is the threat to occur and succeed? (e.g., Improbable, Probable, Very Probable)
5.  Determine **Risk Level:** Plot Impact vs. Likelihood on the **Risk Matrix**.
    *(Diagram points Impact & Likelihood inputs to the Risk Matrix)*
6.  **Rank Risks:** List risks based on their determined level (e.g., Risk 1 [High], Risk 2 [High], Risk 3 [Medium], ...).
7.  Compare to **Acceptable Risk Threshold:** Decide which risks require treatment based on the organization's risk appetite. Risks below the threshold might be accepted.
    *(Diagram shows ranked risks compared to an "Acceptable Risk Threshold" line)*

*Conceptual Formula Reminder: Risk Level depends on Threat, Vulnerability, Impact, and Likelihood factors.*

---

## Step 2: Risk Analysis (Plan Phase)

**Risk Treatment:**

*   The process of selecting and implementing measures (controls) to **modify** identified risks that exceed the acceptable risk threshold. The most common goal is to reduce the risk.
*   Based on the risk assessment, organizations decide which measures to take (or not take) to **reduce or eliminate** unacceptable risks, often guided by control frameworks like ISO 27002 Annex A or NIST SP 800-53.
*   For each identified risk requiring treatment, there are generally four main options:

    *(Diagram: Cycle showing options surrounding "Risk Treatment")*
    *   **Risk Avoidance (Refuser):** Deciding not to start or continuing with the activity that gives rise to the risk (e.g., not launching a new service).
    *   **Risk Reduction / Mitigation (Réduire):** Applying controls to lessen the likelihood or impact of the risk (e.g., installing a firewall, implementing encryption, training users). This is the most common treatment.
    *   **Risk Transfer / Sharing (Transférer):** Shifting some or all of the risk to a third party (e.g., buying insurance, outsourcing a function). Note: Accountability often remains with the organization.
    *   **Risk Acceptance / Retention (Accepter):** Knowingly and objectively deciding not to take action, accepting the risk (usually done for risks below the acceptable threshold or where the cost of treatment outweighs the potential impact). Requires explicit management approval.

---

## Step 2: Risk Analysis (Example Risk Assessment Table)

| Asset   | Threat                             | Vulnerability                                             | Impact (Severity)             | Likelihood                                   | Risk Level | Recommendation / Treatment                        |
| :------ | :--------------------------------- | :-------------------------------------------------------- | :---------------------------- | :------------------------------------------- | :--------- | :------------------------------------------------ |
| Server  | System failure - overheat in server room | Air conditioning system is 10 years old (**ELEVATED**)      | All services unavailable (**SEVERE**) | **VERY LIKELY** (Server room temp often 40°C) | **HIGH**   | **Reduce:** Purchase new air conditioner (£2700 estimate) |
| Website | DDoS attack by malicious actors    | Firewall correctly configured but lacks robust DDoS mitigation features (**ELEVATED**) | Website resources unavailable (**SEVERE**) | **UNLIKELY** (Major attack detected approx. every 5 years) | **MEDIUM** | **Reduce:** Enhance DDoS protection & Monitor firewall closely. (Potentially **Accept** if cost is too high and impact duration limited) |

*(Note: Likelihood/Impact/Risk levels are illustrative based on the matrix in slide 47. Currency/costs are examples.)*

---

## Step 2: Risk Analysis (Plan Phase)

**Main Risks for Organizations:**

*   **Loss, Interception, and Destruction of Data:**
    *   Industrial/economic espionage (theft/loss of trade secrets, R&D, customer lists).
    *   Data breaches leading to exposure of sensitive personal or financial information.
    *   Ransomware encrypting or exfiltrating data.
*   **Reputation / Image Degradation:**
    *   Loss of customer trust due to security incidents.
    *   Damage to brand image and intellectual property.
    *   Negative media coverage.
*   **System Unavailability / Business Disruption:**
    *   Inability to conduct business operations due to system outages (DDoS, hardware failure, malware).
    *   Loss of productivity.
*   **Activity Hijacking / Misuse of Resources:**
    *   Infection of IT resources used for C&C, spamming, crypto mining.
    *   Hijacking of computing capabilities for unauthorized purposes.
    *   Taking control of systems/assets for extortion (ransomware, threatening data release).
*   **Legal / Regulatory Sanctions & Liability:**
    *   Fines for non-compliance with regulations (e.g., GDPR, HIPAA).
    *   Lawsuits from affected parties (customers, employees).
    *   The organization being implicated (and potentially liable) if its compromised systems are used in attacks against other targets.

---

## Step 3: Security Policy (Plan Phase output, Do Phase input)

*   The security policy is a high-level **plan and statement of intent** defining actions and principles to maintain a desired level of security.
*   It reflects the organization's overall security objectives and risk appetite.
*   It determines the necessary means and assigns responsibilities for risk reduction and incident management.
*   The Information Security Policy is the **key reference document** defining the security objectives pursued and the commitment/means implemented to achieve them. It typically requires management approval.
*   The policy framework often includes or refers to supporting documents like **standards, guidelines, and procedures** that enable a level of security consistent with the organization's needs and regulatory requirements.

---

## Step 3: Security Policy (Policy Hierarchy/Pyramid)

*(Diagram: Pyramid structure)*

1.  **Policy (Top Level):**
    *   High-level statement of management intent, objectives, scope, and responsibilities regarding information security. (e.g., Corporate Information Security Policy).
2.  **Standards / Guidelines / Baselines (Middle Level):**
    *   **Standards:** Mandatory rules or controls supporting the policy (e.g., Password Standard, Encryption Standard). Often derived from external sources (ISO, NIST, IETF, ANSSI) or defined internally.
    *   **Guidelines:** Recommended best practices, not strictly mandatory but strongly advised (e.g., Secure Coding Guidelines, SANS Best Practices).
    *   **Baselines:** Define a minimum level of security configuration for specific system types (e.g., Windows Server baseline).
3.  **Procedures (Bottom Level):**
    *   Detailed, step-by-step instructions for specific tasks required to implement policies and standards. Operational and technical in nature (e.g., User Access Request Procedure, Incident Response Procedure, Backup Procedure).

*Example documents shown on slide relate to this hierarchy: SANS Acceptable Use Policy (Policy/Standard), NIST SP 800-128 Config Management (Guide/Standard), SANS Anti-Virus Guidelines (Guide/Procedure).*

---

## Distinguishing Policy from Procedure

**Security Policy (The "What" & "Why" / The Need):**
*   The policy expresses the high-level requirement, objective, or need. It states *what* must be done and often *why*.
*   *Example Policy Statement:* "Remote access to the internal company network (intranet) is authorized only for approved personnel using company-managed devices, requires multi-factor authentication, and must occur over an encrypted network connection to protect company data."

**Security Procedures (The "How" / The Implementation):**
*   The procedure provides the detailed, step-by-step instructions on *how* to implement the policy requirement. It's the technical or operational implementation of the need.
*   *Example Procedure Snippet (implementing the above policy):* "To establish a remote connection: 1. Launch the Corporate VPN Client application. 2. Enter your AD username and password when prompted. 3. Approve the push notification sent to your registered mobile device via the MFA app. 4. The connection will be established using an IPsec tunnel configured with AES-256 encryption..."

---

## Relationships between Policies, Guidelines, and Procedures

*(Diagram showing a hierarchical structure)*

*   **Overall Security Policy** (Top-level document)
    *   Branches into specific **Issue-Specific Policies**, such as:
        *   **Personnel Security Policy** (Hiring, termination, roles)
            *   May inform **System Access Policy**
        *   **Information Security Policy** (Classification, handling)
            *   May inform **System Access Policy**, **Encryption Policy**
        *   **Organizational / Physical Security Policy**
            *   May inform **Accident / Disaster Recovery Policy**
    *   These specific policies are then implemented through:
        *   **Standards** (Mandatory rules)
        *   **Guidelines** (Recommended practices)
        *   **Procedures** (Step-by-step instructions)

*(The diagram illustrates that a high-level policy framework cascades down into more specific policies and is ultimately put into practice via detailed standards, guidelines, and procedures.)*

---

## Elements often addressed in a Security Policy Framework

*   **Hardware Failure:**
    *   Physical equipment is subject to failure (wear, aging, defects...). Policy may mandate purchasing quality, standardized equipment with warranties/support. However, only **backups and redundancy** can effectively protect data and ensure service continuity. *Procedures* define backup schedules and restoration tests.
    *(Image: Technician working on server hardware)*

*   **Software Failure / Bugs:**
    *   All non-trivial software contains bugs. Policy may mandate **regular patching** and using supported software versions. **Backups** are crucial for recovery from data corruption caused by bugs. *Procedures* detail patching process and backup execution.
    *(Image: Windows Blue Screen of Death error screen)*

---

## Elements often addressed in a Security Policy Framework

*   **Accidents (outages, fires, floods...):**
    *   Policy should require **Business Continuity and Disaster Recovery (BCDR) planning**. **Backups** are indispensable. BCDR plans and backup *procedures* detail response actions, recovery steps, and testing schedules.
    *(Image: Computer components damaged by fire/heat)*

*   **Human Error:**
    *   Mistakes happen. Policy should mandate **security awareness training** and define clear roles/responsibilities. Procedures should be clear and easy to follow. Controls like the principle of least privilege limit the potential impact of errors.
    *(Image: Cartoon characters pointing blame at each other)*

---

## Elements often addressed in a Security Policy Framework

*   **Theft via Physical Devices (e.g., USB keys, Laptops):**
    *   Policy should address physical security and removable media usage. May require **controlling physical access** to equipment, restricting/disabling USB ports where not essential, mandating **encryption** for laptops and removable media. Surveillance or logging may be required. *Procedures* define how to request exceptions or handle lost devices.
    *(Image: USB stick plugged into laptop with "?!" symbols)*

*   **Network Hacking and Viruses:**
    *   This is a major focus. Policy will mandate various technical controls like **firewalls, IDS/IPS, antivirus/anti-malware, network segmentation, secure configuration, vulnerability management (patching), encryption (HTTPS, VPNs)**. Procedures detail configuration, monitoring, and response actions (Incident Response Plan).
    *(Image: Laptops connected via a network overlaying a city, suggesting network connectivity and potential threats)*

---

## ISO 27001 Standard: ISMS (PDCA Cycle - Do Phase)

*(PDCA Diagram with the 'Do' section highlighted)*

**Do (Implement and Operate the ISMS):**
4.  Implement the risk treatment plan and the selected controls; Manage operations; Implement programs (e.g., awareness).

*(Rest of Plan, Check, Act phases as described previously)*

*This slide highlights the **Do** phase.*

---

## Step 4: Deployment Phase "Do"

This phase involves putting the plans into action:

*   **Implementation** of the security policy and deployment of the security measures (controls) identified in the risk treatment plan, relevant to the organization's context.
*   **Application** of specific operational procedures (e.g., access control process, backup procedures, change management).
*   **Awareness-raising and training** for employees and relevant stakeholders regarding security policies, procedures, and their responsibilities.
*   **Allocation** of necessary resources (budget, personnel, tools) to implement and manage the controls and the ISMS.

---

## ISO 27001 Standard: ISMS (PDCA Cycle - Do Phase)

*(PDCA Diagram with the 'Do' section highlighted - Appears to be a duplicate of Slide 59)*

**Do (Implement and Operate the ISMS):**
4.  Implement the risk treatment plan and the selected controls; Manage operations; Implement programs (e.g., awareness).

*(Rest of Plan, Check, Act phases as described previously)*

*This slide highlights the **Do** phase.*

---

## ISO 27001 Standard: ISMS (PDCA Cycle - Check Phase)

*(PDCA Diagram with the 'Check' section highlighted)*

**Check (Monitor and Review the ISMS):**
5.  Monitor, measure, analyze, and evaluate ISMS performance and effectiveness (Validation):
    *   Internal Audits
    *   Management Reviews
    *   Vulnerability assessments / scans
    *   Penetration tests (optional but common)
    *   Measure control effectiveness

*(Rest of Plan, Do, Act phases as described previously)*

*This slide highlights the **Check** phase.*
*Note: The validation phase ensures that the implemented measures conform to the security policy and effectively protect the information system.*

---

## Step 5: Verification Phase "Check"

This is a fundamental step in the ISMS continual improvement cycle, aiming to **verify**:

*   That there are no major gaps between what the ISMS **defines** (policies, procedures) and what is actually **implemented** and operating in practice.
*   That the security measures (controls) implemented to address the most critical risks are **appropriate, effective, and sufficient**.

The CHECK phase relies on various monitoring and measurement activities, including:

*   **Internal audits** (checking conformity to ISO 27001 and internal policies/procedures).
*   **Vulnerability scans** (identifying technical weaknesses).
*   **Penetration testing** (simulating attacks to test control effectiveness).
*   **Periodic reviews** of the ISMS by management (assessing overall performance, suitability, adequacy).
*   Monitoring security metrics and incident logs.

...with the goal of detecting any **non-conformities or deviations** from objectives and identifying areas for improvement.

---

## Step 5: Validation Methods Comparison (Check Phase Activities)

| Feature       | Internal Audit                              | Vulnerability Scanning                       | Penetration Testing                             |
| :------------ | :------------------------------------------ | :------------------------------------------- | :---------------------------------------------- |
| **Who**       | Typically internal auditors or third party  | Often internal security team or third party  | Typically a trusted, qualified third party      |
| **Objective** | Evaluate ISMS conformity to ISO 27001 standard & internal policies; Verify control implementation & effectiveness. | Identify known technical vulnerabilities in systems and applications using automated tools. | Simulate real-world attacks to exploit vulnerabilities and assess actual security posture & control effectiveness. |
| **Inputs**    | ISMS documentation (Policy, SoA, procedures), previous audit results, network diagrams, configurations. | List of target IP addresses/ranges, network topology (optional). | Scope definition (IPs, apps), Rules of Engagement. Info level varies: Black Box (no info), Grey Box (some info, e.g., user creds), White Box (full info, source code, diagrams). |
| **How**       | Interviews, documentation review, observation, technical checks (sampling). Follows audit standards (e.g., ISO 19011). | Automated scanning tools (e.g., Nessus, OpenVAS) based on vulnerability databases. Uses methodologies like OWASP Top 10 for web apps. | Combination of automated tools and manual techniques. Follows methodologies like PTES (Penetration Testing Execution Standard), OWASP Testing Guide. |
| **Deliverable**| Audit report detailing findings (conformities, non-conformities), observations, opportunities for improvement; Recommendations for corrective actions. | Report listing identified vulnerabilities (often ranked by severity), potentially affected systems, and recommendations for remediation (e.g., patching, configuration changes). | Detailed report describing scope, methodology, findings (exploited vulnerabilities, compromised systems/data), evidence (screenshots), risk ratings, root cause analysis, and actionable recommendations for remediation. |

---

## ISO 27001 Standard: ISMS (PDCA Cycle - Act Phase)

*(PDCA Diagram with the 'Act' section highlighted)*

**Act (Maintain and Improve the ISMS):**
6.  Address non-conformities; Implement preventive and corrective actions based on check results; Continually improve the ISMS.

*(Rest of Plan, Do, Check phases as described previously)*

*This slide highlights the **Act** phase.*

---

## Step 6: Adjustment Phase "Act"

This step involves taking actions based on the results of the **Check** phase to maintain and improve the ISMS. It focuses on defining and implementing:

*   **Corrections and improvements** identified during monitoring, reviews, and audits (Check phase).
*   Adjustments needed due to **changes** in the internal or external context (e.g., new threats, new business processes, new technology, changes in scope, new legal requirements).

Consider inputs like:
*   Changes in scope (technical, organizational, functional).
*   New risks (new threats appearing, new vulnerabilities discovered).

Resulting actions are typically classified into:
*   **Corrective actions:** To address the root cause of identified non-conformities or incidents and prevent recurrence.
*   **Preventive actions:** To address potential non-conformities before they occur (less emphasized in newer ISO management standards, often covered by risk treatment).
*   **Improvement actions:** To enhance the effectiveness, efficiency, or suitability of the ISMS processes and controls.

This phase feeds back into the **Plan** phase, preparing for the next iteration of the PDCA cycle and driving **continual improvement**.

---

## Step 6: Improvement Phase (Act) Actions

*(Staircase diagram illustrating levels of action)*

1.  **Prevention:** Act on potential causes *before* an incident or non-conformity occurs (proactive, often part of risk management/planning).
2.  **Correction:** Act on the immediate effects to fix deviations or incidents (containment, fixing the symptom). Then, act on the root causes to prevent recurrence (Corrective Action).
3.  **Improvement:** Enhance the overall performance, efficiency, or suitability of an ISMS process or control, beyond just fixing problems (optimization, evolution).

*(These actions ensure the ISMS adapts and becomes more effective over time)*

---

## Examples of Rules and Practices for Data Protection (Controls)

*(Circular diagram showing interconnected security practices)*

*   **Raise User Awareness:** Training on policies, threats, responsibilities.
*   **Authenticate Users & Control Access:** Implement strong authentication, enforce least privilege, manage access rights.
*   **Secure Workstations:** Antivirus, patching, configuration hardening, encryption.
*   **Secure Servers:** Hardening, patching, monitoring, access control, backups.
*   **Secure Websites / Applications:** Secure coding practices (OWASP), WAF, vulnerability scanning.
*   **Archive Securely:** Data retention policies, secure storage for archives, proper disposal.
*   **Secure Exchanges with Other Organizations:** VPNs, encryption, secure protocols, contractual agreements.
*   **Protect the Network:** Firewalls, IDS/IPS, network segmentation, VPNs, secure Wi-Fi.
*   **Secure Mobile Computing:** MDM solutions, encryption, device passcodes, remote wipe.
*   **Trace Access & Manage Incidents:** Logging, monitoring (SIEM), Incident Response Plan & Team.
*   **Protect Physical Premises:** Access control (doors, locks, badges), surveillance, environmental controls.

---

## Conclusion

*   Computer security is critical and **should not be ignored**.

*   **Know Yourself:**
    *   Identify the **assets** that need protection and understand their value and security requirements (Confidentiality, Integrity, Availability).
    *   Determine the security **objectives** to achieve based on business needs and risks.

*   **Know Your Enemies:**
    *   Identify the relevant **threats** and threat actors you need to protect against.
    *   Understand potential **vulnerabilities** in your systems and processes.

*   **React / Respond / Protect:**
    *   Implement a comprehensive **Security Policy** framework.
    *   Apply known **principles, standards, guides, and best practices**.
    *   **Inform and train** personnel – security is everyone's responsibility.
    *   Implement appropriate **controls** (technical, administrative, physical).
    *   Follow a **structured approach** (like ISMS / PDCA) for continual improvement.

---

## References

*   Lloren Cédric, et al. *Tableaux de bord de la sécurité réseau* (Network Security Dashboards), (2010, Eyrolles).
*   Bloch Laurent, Wolfhugel Christophe. *Sécurité informatique principes et méthodes à l'usage des DSI, RSSI et administrateurs* (Computer Security Principles and Methods for CIOs, CISOs, and Administrators), (3rd ed., 2013, Eyrolles).
*   Ghernaouti, Solange. *Cybersécurité - 6e éd.: Analyser les risques, mettre en œuvre les solutions* (Cybersecurity - 6th ed.: Analyze risks, implement solutions), (2019, Dunod).

*(Images of book covers)*

---

## References

*   *EBIOS risk manager*, Agence nationale de la sécurité et des systèmes d'information (National Cybersecurity Agency of France - ANSSI). (2018).
*   Link: [`https://www.ssi.gouv.fr/uploads/2018/10/guide-methode-ebios-risk-manager.pdf`](https://www.ssi.gouv.fr/uploads/2018/10/guide-methode-ebios-risk-manager.pdf)

