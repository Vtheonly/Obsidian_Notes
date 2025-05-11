Okay, let's break down the concepts from the TD exercises, integrating explanations from the provided solution document and the presentation slides.

**Core Security Concepts (From Exercice 1 & Slides)**

These are the fundamental goals of information security, often referred to as the CIA Triad, plus Authentication.

1.  **Confidentiality (Confidentialité)**
    *   **Definition:** Ensuring that information is accessible only to those authorized to have access. It's about preventing unauthorized disclosure.
    *   **TD Context (Ex 1):** Scenarios like a stolen unencrypted USB (Case 1), unauthorized software copying (Case 2), unauthorized data reading/statistical analysis revealing underlying data (Case 5), and message reading/traffic analysis (Case 8) all represent breaches of confidentiality. The data/software/messages are exposed to unauthorized parties.
    *   **Slides Context:** Defined on Slide 20 as ensuring only authorized entities (people, machines, software) have access. Threats include network eavesdropping, file theft, espionage. Countermeasures include cryptography and access control. It's a core part of the CIA Triad (Slide 19) and a key objective (Slide 18). The goal of attacks is often to "extort information" (Slide 20).

2.  **Integrity (Intégrité)**
    *   **Definition:** Assuring the accuracy and completeness of information and processing methods. It ensures that data has not been tampered with or modified by unauthorized parties.
    *   **TD Context (Ex 1):** Modifying a program to alter its function (Case 3), modifying existing files or fabricating new ones (Case 6), and modifying, delaying, reorganizing, or duplicating messages, including fabricating false messages (Case 9) are all attacks against integrity. The information or system process is being illegitimately changed.
    *   **Slides Context:** Defined on Slide 21 as ensuring resources/information are not corrupted or altered by unauthorized entities. Data/messages shouldn't be modifiable without detection. Attack objectives include changing, adding, or deleting information. Threats include malicious attacks (viruses, logic bombs). Countermeasures include cryptography (signatures) and authentication. Illustrated in the CIA Triad (Slide 19) and objectives (Slide 18). Slide 21 shows examples like altering a check amount.

3.  **Availability (Disponibilité)**
    *   **Definition:** Ensuring that authorized users have access to information and associated assets when required. Systems and data should be accessible and usable upon demand.
    *   **TD Context (Ex 1):** Files being deleted or access refused (Case 4) and network configuration messages being destroyed or suppressed (Case 7) directly impact availability. Authorized users cannot access the required resources or services.
    *   **Slides Context:** Defined on Slide 22 as ensuring authorized users can access information or services when needed. Attack objective is to render the system unusable or inexploitable. Threats include malicious attacks (Denial of Service - DoS) and accidental issues (hardware failure, power outage - mentioned implicitly in policy elements Slide 56). Countermeasures include firewalls, Intrusion Detection Systems (IDS), and administrator training. Part of the CIA Triad (Slide 19) and objectives (Slide 18).

4.  **Authentication (Authentification)**
    *   **Definition:** Verifying the identity of a user, process, or device, often as a prerequisite to allowing access to resources in an information system. It answers the question "Are you really who you say you are?".
    *   **TD Context (Ex 1):** A hacker successfully using someone else's bank card details to make a purchase (Case 10) is a failure of authentication (and potentially authorization/confidentiality). The system incorrectly verified the identity of the user based on the stolen credentials.
    *   **Slides Context:** Defined on Slide 24 as information allowing identity validation. It verifies the claimed identity (established during Identification, Slide 23). Examples include passwords (basic) or multi-factor authentication (strong). It's listed as a security objective beyond the core triad (Slide 18, 24).

**Information System Security Lifecycle Phases (From Exercice 2 & Slides)**

Securing an Information System (IS) is a continuous process involving several phases, often modeled by the Plan-Do-Check-Act (PDCA) cycle (Slides 37, 38, 59, 61, 62, 65).

1.  **Context Analysis (Analyse du contexte)**
    *   **Definition:** Understanding the scope, environment, assets, and requirements of the system to be protected. It involves defining what needs to be secured and why.
    *   **TD Context (Ex 2):** "Determining the perimeter of the system to protect" (Action 3) clearly falls into this phase. It defines the boundaries of the security effort.
    *   **Slides Context:** Corresponds to the initial part of the "Plan" phase in PDCA (Slide 37/38/39). It involves identifying the scope and assets (Slide 39 - Identify assets, classify them). Slide 28 defines assets (primary/support). Slide 9 shows the components of an IS.

2.  **Risk Analysis (Analyse de risques)**
    *   **Definition:** Identifying potential threats and vulnerabilities, assessing the likelihood of their occurrence, and determining the potential impact on the organization's assets.
    *   **TD Context (Ex 2):** Identifying that "The web server runs on an old machine" (Action 4) and "The FTP server frequently crashes, redundancy should be planned" (Action 8) are findings typically resulting from a risk analysis, identifying vulnerabilities and potential impacts.
    *   **Slides Context:** This is a major part of the "Plan" phase (Slide 37/38/40-51). It involves identifying threats (Slide 30), vulnerabilities (Slide 29), impacts, and estimating the risk level (Slide 42, 45-48), often using methods like EBIOS, MEHARI, OCTAVE, CRAMM (Slide 40) or ISO 27005 (Slide 41). It involves identifying vulnerabilities (e.g., lack of firewall, bad configuration - Slide 29).

3.  **Security Policy (Politique de sécurité)**
    *   **Definition:** A high-level document outlining an organization's security goals, rules, responsibilities, and commitment to security. It sets the direction for security efforts. *(Note: The TD uses this phase slightly differently, including specific technical rules within it, blurring the line with 'Security Measures' somewhat compared to the slides' hierarchy).*
    *   **TD Context (Ex 2):** The statement "The password must be strong and changed regularly..." (Action 10) is a specific rule that would typically be defined *based on* or *within* a security policy or a related standard/guideline derived from it. *(The TD/Solution places Action 8 here as well, potentially seeing the *need* for redundancy as a policy-level decision to ensure availability, although identifying the crash itself is Risk Analysis).*
    *   **Slides Context:** Defined as a plan of action (Slide 52), a reference document defining objectives and means (Slide 52), and the top of the policy pyramid (Slide 53). ISO 27001 requires establishing a policy (Slide 37/38). Slides 56-58 discuss elements often covered by policies (hardware/software failure, human error, physical theft, network attacks). Slide 54 distinguishes policy (the need) from procedure (the implementation).

4.  **Security Measures (Mesures de sécurité)**
    *   **Definition:** Specific controls, safeguards, and countermeasures implemented to enforce the security policy and reduce risks. These can be technical, organizational, or physical.
    *   **TD Context (Ex 2):** "Recruiting a competent network administrator" (Action 1 - organizational measure), "Personal computers are protected by a firewall" (Action 6 - technical measure), "Offices are locked with smart keys outside office hours" (Action 9 - physical/technical measure), and the password requirements (Action 10 - technical/policy rule) are all specific security measures.
    *   **Slides Context:** Defined as technical measures (Firewall, AV, IDS, PKI) allowing policy application (Solution page 2). Slide 32 defines countermeasures (actions to reduce/eliminate risk) including physical (cameras, access control) and technical (IDS/IPS, Firewall, VPN, AV, HTTPS). Slide 7 shows Preventative, Active, and Reactive mechanisms.

5.  **Implementation (Implémentation)**
    *   **Definition:** The process of deploying and putting into operation the selected security measures and policies. This is the "Do" phase.
    *   **TD Context (Ex 2):** "Install Kaspersky Total Security antivirus on all workstations" (Action 2) and "Install a Cisco ASA firewall" (Action 7) are concrete implementation actions.
    *   **Slides Context:** This corresponds to the "Do" phase of PDCA (Slide 37/38/59/60). It involves putting the security policy and measures into execution (Slide 60) and applying specific procedures.

6.  **Validation (Validation)**
    *   **Definition:** Assessing the effectiveness of the implemented security measures and verifying compliance with the security policy. This is the "Check" phase.
    *   **TD Context (Ex 2):** "Test the vulnerabilities of the implemented security system" (Action 5) is a direct validation activity.
    *   **Slides Context:** This is the "Check" phase of PDCA (Slide 37/38/61/62/63). It verifies that measures are effective and conform to policy (Slide 62). Methods include audits, vulnerability scans, and penetration tests (Slide 63, 64). Slide 64 details the goals and deliverables of Audits, Vulnerability Scans, and Penetration Tests.

**Other Key Concepts**

*   **Vulnerability (Vulnérabilité - Ex 3):** A weakness in an asset or control that can be exploited by one or more threats. (Slides 29, 33, 42). Examples in Ex 3: Employees connecting personal smartphones, administrator working for a competitor, use of default passwords, lack of physical protection.
*   **Threat (Menace - Ex 3):** A potential cause of an unwanted incident, which may result in harm to a system or organization. (Slides 30, 33, 42). Examples in Ex 3 solution: Virus propagation, disclosure of secrets, unauthorized access, theft of equipment.
*   **Risk (Risque - Ex 4):** The potential for loss or damage when a threat exploits a vulnerability. Often expressed as a combination of likelihood and impact. (Slides 4, 40, 41, 42, 45-51). Ex 4 calculates *Annualized Loss Expectancy (ALE)* (though not named as such) quantitatively and critiques this approach, suggesting qualitative methods (Solution p3, Slides 45-48).
*   **Baseline Security (Niveau de sécurité de base - Ex 7):** A standard level of security controls applied to all systems, providing protection against common threats. (Solution p5). Often associated with standards like IT Grundschutz (GSHB) (Solution p6).
*   **Security Certification (Certification de sécurité - Ex 7):** Formal verification by an accredited body that a product, service, or system meets specific security criteria defined in a standard. (Solution p5). Associated with standards like Common Criteria (ISO 15408) (Solution p6).
*   **Security Policy (Politique de sécurité - Ex 7):** As defined above - the overall set of rules guiding security. Associated with management standards like ISO 27001 (which includes defining a policy). (Solution p5, p6, Slides 52-55).
*   **ISMS (Information Security Management System - SMSI):** A systematic approach to managing sensitive company information so that it remains secure. It includes people, processes and IT systems by applying a risk management process. ISO 27001 defines requirements for an ISMS. (Slides 4, 34, 35, 36, 37).

This breakdown should cover the main concepts presented in the TD, linking them to the provided solutions and the context given in the slides.


[[Q10]]