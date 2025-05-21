

# Introduction to IT Security (L3-S6 UMBB 2021/2022)

## Full Course Outline

1.  **Chapter 1: Introduction to IT Security**
2.  Chapter 2: Introduction to Cryptography
3.  Chapter 3: IT Threats
    *   Application and System Attacks
    *   Web Attacks
    *   Network Attacks
4.  Chapter 4: Defense Mechanisms

---

## Chapter 1: Introduction to IT Security

### Chapter 1 Outline

1.  Introduction to Information Systems (IS) Security
2.  The Stakes of IS Security
3.  Objectives of IT Security
4.  Main Concepts of IT Security
5.  Securing an IS through an Information Security Management System (ISMS)
6.  Conclusion
7.  Application Exercises

### 1. Introduction to Information Systems (IS) Security

#### Fundamental Definitions

*   **Information**: Structured and organized data, having meaning. Can be stored in databases (DB), files, etc.
*   **IT System**: Set of hardware (servers, workstations, network equipment) and software (operating systems like Windows/Linux, DBMS like Oracle, applications) used to process information.
*   **Information System (IS)**: An organized set of resources (personnel, data, procedures, hardware, software) allowing for the collection, grouping, classification, processing, and dissemination of information within an organization. It includes users, uses, and IT infrastructure.
    *   Information lifecycle in an IS: `collect -> group -> classify -> process -> disseminate`.

#### Security Levels

*   **Information Security**:
    *   Set of management strategies for processes and policies aimed at protecting, detecting, identifying, and countering threats targeting **digital or non-digital information**.
*   **IT Security (Cybersecurity)**:
    *   Set of means implemented to reduce the vulnerability of an **IT system** against accidental or intentional threats.
    *   Set of techniques ensuring that an organization's **information system resources (hardware or software)** are used only in the manner for which they are intended.
*   **IS Security**:
    *   The set of technical, organizational, legal, and human means necessary for implementing measures aimed at preventing unauthorized use, misuse, modification, or diversion of the **information system**.

#### IT Security in Nature

*   The term "IT security" is a generic term applying to networks, the Internet, endpoints, APIs, the cloud, applications, container security, etc.
*   These are the methods, techniques, and tools implemented for the protection of systems, data, and services against accidental or intentional threats.
*   **Main Objectives**:
    *   Reduce the **risks** weighing on the information system.
    *   Limit their **impacts** on the functioning and business activities of organizations.
*   Security management is not intended to be an obstruction, but rather:
    *   It **contributes to the quality of service** that users are entitled to expect.
    *   It **guarantees personnel the level of protection** they are entitled to expect.

#### Components of an Information System and Threats (Overview)

An Information System (IS) is composed of:
*   **Core**: Users, Uses, IT Infrastructure (Hardware: DB, Servers; Software: Oracle, Windows, Linux), Information.
*   **Security/Technology Layer**: HTTPS, Cryptography, Firewall, IDS (Intrusion Detection System), SSL/TLS, SSH, VPN.
*   **Potential Threats**: Viruses, Worms, Malware, Backdoors, XSS (Cross-Site Scripting), Ransomware, Adware, Social Engineering.
*   **Potential Adversaries**: Spies (state-sponsored or industrial), Hackers, Crackers, Pirates, Malicious Colleagues, Cybercriminals, Governments, Amateurs (Script Kiddies).

[[Q1]]
### 2. The Stakes of IS Security

IS security has multiple impacts:
*   **Financial Impacts**: Direct losses, remediation costs.
*   **Impacts on Image and Reputation**: Loss of customer/partner trust.
*   **Legal and Regulatory Impacts**: Fines, sanctions (e.g., GDPR).
*   **Organizational Impacts**: Disruption of operations, loss of productivity.

**Why are pirates interested in IS?**

*   **Evolution of Motivations**:
    *   80s-90s: Enthusiastic tinkerers (exploratory hackers).
    *   Nowadays: Mostly organized and deliberate actions.
*   **Cybercrime and Various Motivations**:
    *   Lure of profit (theft of financial data, resale of information).
    *   "Hacktivists" (political, ideological motivations).
    *   Political, religious motivations.
    *   Unfair competition (industrial espionage).
    *   State-sponsored civil servants (cyber warfare, state espionage).
    *   Mercenaries acting for clients.
*   **Types of "Gains" Sought**:
    *   **Financial Gains**: Access to information (user accounts, emails, customer data, passwords, bank account numbers) then monetization and resale.
    *   **Resource Utilization**: Resale or provision "as a service" (bandwidth, storage space for illegal hosting, zombies/botnets for DDoS attacks or spam).
    *   **Blackmail**: Denial of Service (DoS/DDoS), data modification/encryption (ransomware).
    *   **Espionage**: Industrial/competitive, State-sponsored.

**Notable Cyberattack Examples (from the document):**
*   DDoS attack against the "chouroukonline.com" website in 2009.
*   In retaliation, an attack against an "Egyptian ministry" website by "Team Dos-Dz".
[[Q2]]
### 3. Objectives of IT Security

Ensuring the security of an IT system means achieving a set of objectives to guarantee the protection of information against any unauthorized disclosure, alteration, or destruction. Access to this information must be controlled.

The main objectives are often summarized by the **CIA Triad (or DIC)** and supplemented by others.

#### The CIA Triad

1.  **Confidentiality**
    *   **Definition**: Aims to ensure that only authorized entities (people, machines, software) have access to the resources and information they are entitled to.
    *   **Attack Objective**: To extort information.
    *   **Typical Threats**:
        *   Network sniffing.
        *   File theft.
        *   Espionage.
        *   Social engineering.
    *   **Countermeasures**:
        *   Cryptography (encryption).
        *   Access control (logical: passwords, ACLs; physical: biometrics, badges).
        *   Asset classification.
        *   Personnel training.

2.  **Integrity**
    *   **Definition**: Aims to ensure that resources and information are not corrupted or altered by unauthorized entities. Data or messages cannot be modified without the concerned parties knowing.
    *   **Attack Objective**: To change, add, or delete information or resources.
        *   Example: A check for 1000DA modified to 100000DA (addition) or to DA (deletion).
    *   **Typical Threats**:
        *   Malicious attacks (Viruses, Worms, Logic Bombs, data modification in transit).
    *   **Countermeasures**:
        *   Cryptography (digital signatures, HMAC).
        *   Hashing functions.
        *   Version controls.
        *   Regular backups.

3.  **Availability**
    *   **Definition**: Ensures that authorized users can access the information or service provided by the system at any time.
    *   **Attack Objective**: To render the system unusable or inoperable.
    *   **Typical Threats**:
        *   Malicious attacks: Denial of Service (DoS), Distributed Denial of Service (DDoS).
        *   Accidental attacks: "Slashdot effect" (overload due to sudden popularity).
        *   Hardware or software failures, natural disasters.
    *   **Countermeasures**:
        *   Firewalls, intrusion prevention/detection systems (IPS/IDS).
        *   System redundancy (clustering, RAID).
        *   Disaster Recovery Plans (DRP) and Business Continuity Plans (BCP).
        *   Backups.
        *   Administrator training.

#### Objectives Beyond the Triad

*   **Identification**:
    *   Information allowing to indicate who you claim to be.
    *   Basic example: Username.
*   **Authentication**:
    *   Information allowing to validate identity to verify that you are who you claim to be.
    *   Basic example: Password associated with a username.
    *   Strong authentication: Combines multiple factors (e.g., something you have - bank card, OTP token - and something you know - PIN, password).
*   **Authorization (Access Control)**:
    *   Information allowing to determine which company resources the authenticated user has access to, as well as the authorized actions on these resources.
    *   Covers all company resources.
    *   Access criteria based on trust/need level: Roles, Groups, Location, Time, Transaction Type.
*   **Non-repudiation**:
    *   **Non-repudiation of origin**: The sender cannot deny having written/sent the message.
    *   **Non-repudiation of transmission/receipt**: The sender cannot deny having sent the message content, and the recipient cannot deny having received it.
    *   Mechanism ensuring that a message was indeed sent by a sender and received by a recipient. Often based on digital signatures.
*   **Traceability (Auditability / Accountability)**:
    *   Set of mechanisms allowing to track operations performed on company resources (who did what, when, on what).
    *   Assumes that every application or system event is logged (logs) for later investigation.
    *   Example: Log files (event logs).
[[Q3]]
### 4. Main Concepts of IT Security

*   **Asset**:
    *   Any element that has value to the organization (hardware, software, information, personnel, reputation, etc.).
    *   **Primary assets**: Business processes and critical information.
    *   **Supporting assets**: Site, person, hardware, network, software, organization.
*   **Vulnerability**:
    *   Weakness in an asset (at the design, implementation, installation, configuration, or usage level).
    *   Represents the level of exposure of an asset to a threat in a particular context. Can be logical or physical.
    *   **Examples (ISO 27005 Annex D)**: Absence of a firewall, misconfigured server, poor password management, sending messages in clear text, untrained personnel.
*   **Threat**:
    *   Potential cause of an incident, which could lead to damage to an asset if the threat materializes.
    *   Action likely to cause harm in absolute terms. Intention or method used to exploit a vulnerability.
    *   **Examples (ISO 27005 Annex C)**:
        *   Physical damage: Fire, dust, flood.
        *   Natural event: Earthquake.
        *   Information compromise: Data interception, equipment theft.
        *   Technical failures: Malfunction of equipment or software.
        *   Actors: Malicious intern, malicious external parties, malicious code.
*   **Attack**:
    *   Malicious action intended to undermine the security of an asset.
    *   Represents the **materialization of a threat** and requires the **exploitation of a vulnerability**.
    *   An attack can therefore only occur (and succeed) if the asset is affected by a vulnerability exploitable by the threat.
    *   **Examples**: SQL injection, XSS, CSRF, Buffer overflow, DDoS.
    *   *Note*: The goal of zero vulnerabilities is unattainable. The aim is to manage vulnerabilities.
*   **Countermeasure (Safeguard)**:
    *   Set of actions implemented to reduce or eliminate risk.
    *   **Physical examples**: Control cameras, physical access control devices.
    *   **Technical examples**: IDS/IPS, Firewall, VPN, Antivirus, HTTPS, security patches.
*   **Impact**:
    *   Consequence of a security incident on the organization's assets. Can be financial, reputational, legal, operational.
*   **Risk**:
    *   Probability that a threat will exploit a vulnerability of an asset and cause an impact.
    *   Often expressed as: `Risk = Probability (Threat * Vulnerability) * Impact`.

**Analogy (Public Health):**
*   **Threat**: Corona virus
*   **Vulnerability**: Not wearing a mask, poor hygiene
*   **Impact**: Experiencing symptoms of the disease, spreading it
*   **Countermeasure**: Wearing a mask, good hygiene, vaccination
[[Q4]]
### 5. Securing an IS through an Information Security Management System (ISMS)

#### ISMS Definition

*   An **ISMS (Information Security Management System)** is a systematic approach to **establishing, implementing, operating, monitoring, reviewing, maintaining, and improving** an organization's information security risk acceptance levels, designed to effectively address and manage risks.
*   It consists of the set of **policies, standards, procedures, practices, behaviors, and planned activities** an organization uses to secure its (critical) informational assets.
*   It provides a clear understanding of the objectives and context of information security both inside and outside the organization.
*   Successful ISMS implementations provide a practical and pragmatic framework for identifying and managing information security risks.

#### Standards and Methods for Securing an IS

*   Cybersecurity standards can be defined as the essential means by which the guidance described in a company's cybersecurity strategy and policies is transformed into actionable and measurable criteria.
*   **Key International Standards**:
    *   **ISO/IEC 17799 (now ISO/IEC 27002)**: Defines objectives and recommendations (best practices) for information security. A framework for developing a security policy, risk analysis, and audit.
    *   **ISO/IEC 27000 Family**: Dedicated to the information security management system. Includes many sub-standards:
        *   `ISO 27000`: Vocabulary and fundamental principles.
        *   `ISO 27001`: Requirements for an ISMS (certifiable).
        *   `ISO 27002`: Code of practice for information security controls.
        *   `ISO 27003`: ISMS implementation guidance.
        *   `ISO 27004`: ISMS metrics and measurements.
        *   `ISO 27005`: Information security risk management.
        *   `ISO 27006`: Requirements for ISMS auditing and certification bodies.
        *   `ISO 27007`: ISMS audit guidance.
        *   Others (27011 for telecom, 27799 for health, etc.).




#### PCDA Summery:

Here’s a concise **phase-by-phase summary** of the ISMS lifecycle in **3–4 bullet points per phase**, following the **Plan-Do-Check-Act (PDCA)** structure:

---

### **PLAN**

- **Define ISMS Scope & Assets**: Identify critical assets (data, systems, personnel), perform asset mapping and classification, and decide the scope.
    
- **Risk Assessment**: Identify threats, vulnerabilities, and potential impacts; use standards like ISO 27005 and methods like EBIOS or OCTAVE.
    
- **Risk Evaluation & Treatment**: Estimate risk likelihood and impact (qualitative/quantitative), use a risk matrix, and determine treatment (avoid, mitigate, transfer, accept).
    
- **Security Policy Development**: Draft a security policy with control objectives, using a policy pyramid (policy → standards → procedures). Differentiate between policy and procedure.
    

---

### **DO**

- **Implement Controls and Procedures**: Apply selected measures, enforce procedures, and align with the established policy.
    
- **Training & Resources**: Train staff and allocate appropriate human, technical, and financial resources.
    
- **Operationalization**: Deploy and integrate security into daily operations.
    

---

### **CHECK**

- **Effectiveness Review**: Ensure ISMS implementation aligns with documentation and effectively addresses key risks.
    
- **Audits & Scanning**: Perform internal/external audits, vulnerability scans (e.g., Nessus, OWASP ZAP), and penetration tests (White/Grey/Black Box).
    
- **Management Review**: Periodically review ISMS status and effectiveness with top management.
    

---

### **ACT**

- **Continuous Improvement**: Address issues from the Check phase through corrective, preventive, and improvement actions.
    
- **Adapt to Change**: Respond to changes in risks, scope, or organizational structure.
    
- **Iterate**: Feed insights back into the Plan phase for the next ISMS cycle.
    
- **Focus Areas**: Prevention (proactive), correction (reactive), and systemic improvement.
    

---

Let me know if you'd like this reformatted into an Obsidian-friendly Markdown structure.
#### ISO 27001 Standard: The PDCA Cycle (Plan-Do-Check-Act)

The ISO 27001 standard is process-oriented and recommends the **PDCA (Deming Wheel)** quality model to establish, implement, monitor, maintain, and improve the ISMS.

**PLAN**
1.  **Define the Scope and Policy of the ISMS**:
    *   Identify critical assets to protect (hardware, software, data, people).
    *   Asset mapping and classification.
    *   The choice of scope is up to the organization.
2.  **Identify and Assess Security Risks (Risk Analysis)**:
    *   Identify vulnerabilities, threats, and potential impacts.
    *   Estimate the likelihood of occurrence.
    *   **Risk management methods**: ANSSI EBIOS, MEHARI, OCTAVE, CRAMM.
    *   **Risk management process (ISO 27005)**:
        *   **Risk Assessment**:
            *   *Risk Analysis*:
                *   Risk Identification (What vulnerabilities? What threats? What impact? What likelihood?)
                *   Risk Estimation (Qualitative: low/medium/high; Quantitative: in monetary value).
                    *   Risk matrix (Impact vs. Likelihood) to characterize risks (e.g., Severe/Medium/Low vs. Unlikely/Likely/Very Likely).
            *   *Risk Evaluation*: Compare the risk level to the accepted risk threshold.
        *   **Risk Treatment**: Select options to treat risks (Avoid, Mitigate/Reduce, Transfer/Share, Accept/Tolerate).
    *   **Main risks for organizations**: Data loss/interception/destruction, image degradation, system unavailability, activity hijacking, legal sanctions.
3.  **Develop the Security Policy and Select Control Objectives and Controls (Measures)**:
    *   The security policy is an action plan to maintain a certain level of security. It groups security objectives and determines the necessary means.
    *   It is the reference document defining objectives and means.
    *   **Policy Pyramid**:
        *   *Global security policy* (high level).
        *   *Standards/Guides/Recommendations* (internal standards, best practices).
        *   *Procedures* (operational documents describing how to do things).
    *   **Distinguish Policy from Procedure**:
        *   *Policy*: Expression of need (e.g., "Remote access to the internal network is authorized under the condition of strong authentication and an encrypted connection.").
        *   *Procedure*: Technical implementation (e.g., "External access to the internal network (intranet) is authenticated by an electronic certificate validated by the company's PKI. Furthermore, the network connection is encrypted using the IPsec protocol.").
    *   **Elements of a security policy**: Covers hardware/software failures, accidents, human errors, physical theft (USB drives), hacking/network viruses.

**DO (Implement / Deploy)**
4.  **Implement and Operate the ISMS Security Policy, Controls, Processes, and Procedures**:
    *   Implementation of the security policy and selected measures.
    *   Application of specific procedures.
    *   Awareness and training of collaborators.
    *   Allocate necessary resources (human, financial, technical).

**CHECK (Monitor / Review)**
5.  **Monitor and Review the Effectiveness of the ISMS (Validation)**:
    *   Fundamental step to verify:
        *   That there are no major discrepancies between what the ISMS defines and what is implemented in practice.
        *   That security measures covering the most critical risks are appropriate, effective, and sufficient.
    *   **Based on**:
        *   **Internal/External Audit**: Assessment of the security level against a standard/framework. Verifies rule application. Deliverable: Audit reports.
        *   **Vulnerability Scan**: Identify the presence of known/unknown vulnerabilities. Input: Internal topology. Tools: OWASP ZAP, Nessus. Deliverable: List of vulnerabilities and corrections.
        *   **Penetration Test (PenTest)**: Exploit (attack) vulnerabilities. Modes: White Box (all info), Grey Box (partial info), Black Box (no info). Deliverable: Technical report of attacks, assets recovered, criticality, solutions.
        *   **Periodic ISMS Review** by management.

**ACT (Maintain / Improve)**
6.  **Maintain and Improve the ISMS**:
    *   Implement **preventive, improvement, or corrective actions** for incidents and discrepancies found during the Check phase.
    *   Take into account any changes (scope, new risks, new threats/vulnerabilities).
    *   **Resulting Actions**:
        *   *Corrective actions*: For an incident or identified gap.
        *   *Preventive actions*: For a potential anomaly.
        *   *Improvement actions*: Enhancing the performance of the existing process.
    *   Prepare a new iteration of the Plan phase.
    *   **Levels of Action**:
        *   *Prevention*: Act on causes before the incident occurs.
        *   *Correction*: Act on effects to correct gaps, then on causes to prevent recurrence.
        *   *Improvement*: Improve the overall performance of the ISMS.

**Examples of Rules and Practices for Data Protection (summary):**
Raise user awareness -> Authenticate and limit access (need-to-know) -> Secure workstations -> Secure servers -> Secure websites -> Archive securely -> Secure exchanges with other organizations -> Protect internal/external IT network -> Secure mobile IT -> Trace access and manage incidents -> Protect premises.
[[Q5]]

### 7. Application Exercises (Based on "Série N°1")

#### Exercise 1: Affected Security Objectives

For each of the following scenarios, indicate the affected security objective (Availability, Confidentiality, Integrity, Authentication).

| Scenario                                                                                                   | Availability | Confidentiality | Integrity | Authentication |
| :--------------------------------------------------------------------------------------------------------- | :----------: | :-------------: | :-------: | :------------: |
| 1. An unencrypted USB key is stolen                                                                        |              |        X        |           |                |
| 2. An unauthorized copy of the software is made                                                            |              |        X        |           |                |
| 3. A work program is modified (to make it fail or redirect data)                                           |       X      |        X        |     X     |                |
| 4. Files are deleted, access is denied to users                                                            |       X      |                 |           |                |
| 5. Unauthorized data reading is performed. Statistical analysis reveals underlying data.                   |              |        X        |           |                |
| 6. Existing files are modified or new files are fabricated                                                 |              |                 |     X     |                |
| 7. Network configuration messages are destroyed or deleted                                                 |       X      |                 |           |                |
| 8. Messages are read. The message traffic pattern is observed                                              |              |        X        |           |                |
| 9. Messages are modified, delayed, reordered, or duplicated. Fake messages are fabricated                  |              |                 |     X     |                |
| 10. A hacker successfully uses another individual's bank card to buy a phone from an online sales site.   |              |                 |           |       X        |

*(Solution based on the provided exercise sheet)*

#### Exercise 2: IS Securing Phases

Securing an IS requires several phases. Classify the following actions into the corresponding step.
*   **Process Steps**: Situation Analysis (Context) -> Risk Analysis -> Security Policy -> Security Measures -> Implementation -> Validation.
    *   **Risk Analysis**: Identify potential problems with associated costs.
    *   **Security Policy**: Protection means to be implemented (Confidentiality, authentication, integrity, redundancy...).
    *   **Security Measures**: Set of technical measures (Firewall, AV, IDS, PKI...) that will allow the policy to be applied.
    *   **Implementation**: Installation and deployment of the different measures.

| Action                                                                                                                              | Corresponding Step    |
| :---------------------------------------------------------------------------------------------------------------------------------- | :-------------------- |
| 1. Recruit a competent network administrator                                                                                        | Security Measures     |
| 2. Install Kaspersky Total Security antivirus on all workstations.                                                                  | Implementation        |
| 3. Determine the perimeter of the system to be protected                                                                            | Context Analysis      |
| 4. The web server runs on an old machine                                                                                            | Risk Analysis         |
| 5. Test the vulnerabilities of the implemented security system.                                                                     | Validation            |
| 6. Personal computers are protected by a firewall                                                                                   | Security Measures     |
| 7. Install a Cisco ASA firewall                                                                                                     | Implementation        |
| 8. The FTP server frequently fails, redundancy should be planned                                                                    | Security Policy       |
| 9. Offices are locked with smart keys outside of business hours                                                                     | Security Measures     |
| 10. The password must be strong and changed regularly (min 8 chars, upper/lower case, numbers, special chars)                       | Security Measures     |

*(Solution based on the provided exercise sheet)*

#### Exercise 3: Vulnerabilities, Threats, and Impacts (CAID)

| Vulnerability                                                                          | Threat                                                               | C | A | I | D |
| :------------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :-: | :-: | :-: | :-: |
| Some employees connect to the internet with their smartphones via the company network  | Propagation of viruses in the company network                        | * | * | * |   |
| The company's network administrator works as a consultant for a competitor             | Disclosure of secret information                                     | * |   |   |   |
| The company uses a default password to access its management applications.             | Unauthorized persons can access these applications                   | * | * | * | * |
| Lack of physical protection for the server room                                        | Theft of equipment                                                   | * | * | * |   |

*(C: Confidentiality, A: Availability, I: Integrity, D: (In this context, the provided solution for the French version used D for Disponibilité/Availability. Let's assume A here stands for Authentication, and the original table might have different column orders. The asterisks indicate impacts according to the solution sheet, mapping French CIDA to English CAID where D means Disruption/Availability and A means Authentication)*

*Self-correction: The original French table was C I D A (Confidentialité, Intégrité, Disponibilité, Authentification).
The provided solution marks were:
1. C, I, D
2. C
3. C, I, D, A
4. C, I, D

Let's re-map to English CAID (Confidentiality, Authentication, Integrity, Availability/Disruption).
For "Propagation de virus": It can impact **Confidentiality** (stealing data), **Integrity** (corrupting files), **Availability** (making systems unusable).
For "Divulgation d'informations secrètes": Primarily **Confidentiality**.
For "Des personnes non autorisées peuvent accéder": This is an **Authentication** bypass, leading to potential **Confidentiality**, **Integrity**, and **Availability** issues.
For "Vol d'équipements": Impacts **Availability** directly. Can impact **Confidentiality** and **Integrity** if data is on the equipment.

Corrected table according to understanding:

| Vulnerability                                                                          | Threat                                                               | Confidentiality | Authentication | Integrity | Availability |
| :------------------------------------------------------------------------------------- | :------------------------------------------------------------------- | :-------------: | :------------: | :-------: | :----------: |
| Some employees connect to the internet with their smartphones via the company network  | Propagation of viruses in the company network                        |        *        |                |     *     |      *       |
| The company's network administrator works as a consultant for a competitor             | Disclosure of secret information                                     |        *        |                |           |              |
| The company uses a default password to access its management applications.             | Unauthorized persons can access these applications                   |        *        |       *        |     *     |      *       |
| Lack of physical protection for the server room                                        | Theft of equipment                                                   |        *        |                |     *     |      *       |



*(This is a more standard interpretation of impacts for CAID. The original solution provided seems to have a slightly different mapping, especially for the first and last rows if "A" meant Authentication there.)*

#### Exercise 4: Annual Risk Analysis

A company statistically suffers 5 virus infections per year (remediation cost: €2000/infection, 2 admin days) and 3 website defacements (cost: €500/defacement, a few hours). Annual cost of antivirus and website protection: €30000.

1.  **Calculate the annual risk due to viruses and defacements and judge the usefulness of the stated security measures.**
    *   Annual Risk (quantitative) = (5 infections * €2000) + (3 defacements * €500)
        = €10000 + €1500 = **€11500**
    *   Comparison: Annual risk cost (€11500) < Cost of countermeasures (€30000).
    *   **Judgment (based solely on quantitative)**: From a purely direct quantitative perspective, implementing security measures (€30000) seems more expensive than the current annual risk (€11500). The CISO might opt to accept these risks.

2.  **Critique the way risk is calculated and propose a more adequate method.**
    *   **Critiques**:
        *   The calculation is purely quantitative and does not account for **qualitative and indirect damages**, which are often difficult to quantify but can be very significant:
            *   **Image degradation**: A viral infection can harm the company's reputation, affecting customer and partner trust.
            *   **System unavailability**: Service downtime, loss of productivity, lost revenue.
            *   **Activity hijacking**: Use of company resources for illicit purposes.
            *   **Legal and regulatory consequences**: Fines, lawsuits.
            *   **Loss of sensitive data**: Impact on confidentiality and integrity.
    *   **More Adequate Method**:
        *   Use a **mixed approach (quantitative and qualitative)**.
        *   The qualitative method defines risk as `Risk = Vulnerability * Threat * Impact`.
        *   Assign impact levels (e.g., low, medium, high) and likelihood of occurrence (e.g., rare, frequent).
        *   Use a **risk matrix** (e.g., 2x2 or 3x3) to visualize and prioritize risks.
            *   Example risk matrix (Impact vs. Likelihood):




                | Likelihood / Impact | Low             | High                |
                | :------------------ | :-------------- | :------------------ |
                | **Frequent**        | Medium Risk     | High Risk (Severe)  |
                |                     | (Recovery Plan) | (Apply Measures)    |
                | **Rare**            | Low Risk        | Medium Risk         |
                |                     | (Accept)        | (Analyze Cost/Benefit)|
        *   This approach allows for better decision-making by considering the overall criticality of risks.

#### Exercise 5: Evolution of Security Level

The actual security level is always lower than the estimated level. Without precautions, this difference tends to increase over time.

1.  **Give two reasons that explain the constant increase of this difference in security levels.**
    *   **Discovery of new vulnerabilities (Zero-days)**: New vulnerabilities are discovered daily in existing software and equipment, increasing risk exposure if patches are not applied.
    *   **IS Configuration Modification**: Information systems evolve (new services, updates, personnel changes). Each modification can introduce new flaws or weaken existing measures if not properly managed and tested.

    *(The provided graph shows an initial drop in risk level after IS/measure installation, then a gradual increase in risk ("drift") until a re-evaluation/application of corrective measures brings it down again, creating a cycle.)*

2.  **Describe the kind of measures to take to prevent a decrease in the security level.**
    *   **Regular security audits**: Internal and external, to identify weaknesses and non-conformities.
    *   **Continuous technological watch**: Monitor new threats, vulnerabilities, and available patches.
    *   **Patch Management**: Regularly update systems and software.
    *   **Reconfiguration and testing after each major IS modification**.
    *   **Continuous personnel training and awareness**.
    *   **Review and update of security policy and procedures**.
    *   **Maintenance and testing of disaster recovery/business continuity plans**.

#### Exercise 6: Audience for Security Documents

A company has defined a global security policy. Which people should read the following documents?

*   **User Regulations / Acceptable Use Policy**:
    *   All users of the information system.
    *   The CISO (Chief Information Security Officer).
*   **Recovery Plan and Continuity Plan**:
    *   The CISO.
    *   Technical administrators (web server, email service, etc.).
    *   Personnel involved in customer relations and critical operations continuity (management, communication officer, key department heads).
*   **Security Policy (Global)**:
    *   The CISO.
    *   Management.
    *   Users and administrators may also have access (or adapted versions), but they are not always the *directly* concerned recipients for defining the policy itself, but rather for its application.

#### Exercise 7: Security Terms and References

1.  **Explain the following terms**:
    *   **Baseline Security Level**: Represents the set of fundamental and generally accepted security measures implemented to protect an information system against common and usual threats. Aims to achieve a minimal and essential level of protection.
    *   **Security Certification**: Process by which a third party (certification body) formally attests that a given product, system, service, or organization meets specified security criteria, defined according to a recognized standard or framework.
    *   **Security Policy**: A high-level document that defines the organization's intentions, general orientations, objectives, and principles regarding information security. It expresses management's commitment and serves as a basis for establishing rules, procedures, and security measures.

2.  **Indicate to which term from the previous question each of the following references primarily relates**:
    *   **IT Grundschutz-Handbuch (GSHB)** (BSI, Germany): Primarily relates to **Baseline Security Level**. It is a catalog of threats and concrete security measures to achieve a standard protection level.
    *   **ISO 27001 (or ISO 17799 as indicated in the solution, which is the old name for ISO 27002, the code of practice for controls)**: Primarily relates to **Security Policy** (and its implementation via an ISMS). It provides a framework for establishing, implementing, maintaining, and improving security management.
    *   **Common Criteria (ISO 15408)**: Primarily relates to **Security Certification**. It is an international standard for the evaluation and certification of the security of IT products and systems.

### References (from the document)

*   Tableaux de bord de la sécurité réseau (Network Security Dashboards), (2010, Eyrolles). Cédric Llorens, Laurent Levier, Denis Valois, Benjamin Morin.
*   Sécurité informatique principes et méthodes à l'usage des DSI, RSSI et administrateurs (IT Security Principles and Methods for CIOs, CISOs, and Administrators), (2013, Eyrolles). Laurent Bloch, Christophe Wolfhugel.
*   Cybersécurité - 6e éd.: Analyser les risques, mettre en œuvre les solutions (Cybersecurity - 6th ed.: Analyze Risks, Implement Solutions), (2019, Dunod). Solange Ghernaouti.
*   EBIOS risk manager, Agence nationale de la sécurité et des systèmes d'information (National Cybersecurity Agency of France), (2018, ANSSI). Link: `https://www.ssi.gouv.fr/uploads/2018/10/guide-methode-ebios-risk-manager.pdf` (French)
