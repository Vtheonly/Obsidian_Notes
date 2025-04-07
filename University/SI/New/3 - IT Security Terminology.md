# Obsidian Note: Defining Core IT Security Terminology

**Tags:** #IT_Security #Terminology #Definitions #Asset #Vulnerability #Threat #Risk #Incident #Attack #Countermeasure #Security_Fundamentals #Lecture
**Source:** YouTube Video Subtitles (French) - Defining IT Security Terms

---

## I. Introduction: Purpose of the Video

*   **Objective:** To define a set of fundamental terms used within the domain of IT security.
*   **Goal:** Establish a common vocabulary for understanding security concepts.
*   **Terms Covered:**
    *   Actif (Asset)
    *   Vulnérabilité (Vulnerability)
    *   Incident (Incident)
    *   Menace (Threat)
    *   Risque (Risk)
    *   Attaque (Attack)
    *   Contre-mesure (Countermeasure)

---

## II. Defining the Core Terms

### A. Actif (Asset)

*   **Definition:** An asset is **anything that has value** to an organization or enterprise.
*   **Scope:** This concept is very broad and includes tangible and intangible items.
*   **Examples Provided:**
    *   **Hardware:** Computers, switches, routers, access points, etc.
    *   **Software:** Management software (e.g., accounting, financial), databases, user applications.
    *   **People:** Key personnel with valuable skills or knowledge within the enterprise.
    *   **Services & Protocols:** Network services (like DNS, DHCP) and communication protocols being used.
    *   **Information:** Data that is stored, shared, or transmitted across networks or on storage media.
    *   **Infrastructure:** The entire information system infrastructure.
    *   **Valuable Entities ("Personnes chères"):** Any entity considered valuable to the business.
*   **Core Security Goal related to Assets:** The primary objective of security is to **protect these various assets**.

> **Elaboration:** Understanding what constitutes an asset is the first step in security, as you cannot protect what you haven't identified as valuable. The breadth of examples shows that security concerns extend far beyond just computers and data.

### B. Vulnérabilité (Vulnerability)

*   **Definition:** A vulnerability is a **flaw ("faille") or weakness ("faiblesse")** associated with an asset.
*   **Analogy 1 (Physical):** A house with many cracks ("fissures") has vulnerabilities.
*   **Analogy 2 (Human):** A professional football player (an asset to the club) who doesn't eat well, sleep well, or take health precautions (especially during a pandemic) is considered **vulnerable** (to illness or injury). They have weaknesses ("failles," "faiblesses").
*   **IT Examples:**
    *   A computer (asset) without antivirus software installed.
    *   Antivirus software that is not updated.
    *   Using weak passwords.
    *   Having no password protection at all.
*   **Related Field: Vulnerability Testing:** The professor mentions **"test vulnérabilité"** (vulnerability assessment/testing) as a sub-domain of IT security focused specifically on analyzing assets to *find* these security flaws or vulnerabilities.

> **Elaboration:** Vulnerabilities are the security gaps or weaknesses that can potentially be exploited. They can exist in hardware, software, configurations, procedures, or even human behavior. Identifying vulnerabilities is crucial for prioritizing security efforts.

### C. Incident (Incident)

*   **Definition:** An incident is a **malfunction ("dysfonctionnement")** reported by users concerning one or more assets. It's an adverse event related to security.
*   **Analogy:** For the football player (asset), an incident could be an **injury or illness**. The player *is* actually hurt or sick.
*   **IT Example:** For a computer (asset), an incident could be:
    *   The computer being **hacked ("piraté")**.
    *   The computer being a **victim of malware** (e.g., a virus).
*   **General Meaning:** An incident signifies that something has gone wrong with an asset within the enterprise.

> **Elaboration:** An incident is an observable negative event that affects the confidentiality, integrity, or availability of an asset. It's distinct from a vulnerability (a weakness) or a threat (a potential cause). Incident response is a critical process for handling these events when they occur.

### D. Menace (Threat)

*   **Definition:** A threat is the **potential cause ("cause potentielle")** of an incident.
*   **Mechanism:** A threat **exploits a vulnerability** on an asset to provoke an incident.
*   **Nature:** A threat is a **possibility** that has **not yet materialized** ("pas encore réalisée," "pas encore concrétisée"). It represents the *potential* for harm.
*   **Impact:** If a threat materializes, it can cause **serious damage** to assets.
*   **Analogy:** For the football player who doesn't eat well (vulnerability), the *potential cause* of injury (incident) is the unhealthy lifestyle itself (threat).
*   **IT Example:** For a computer without updated antivirus (vulnerability), a **potential infection by viruses** is the threat. The *cause* of the potential incident (infection) is the existence and potential action of the virus.
*   **Recap:** A threat is the *cause* of a potential incident, enabled by the *exploitation* of a vulnerability.

> **Elaboration:** Threats are entities or events that have the potential to cause harm by leveraging vulnerabilities. Examples include malware, hackers, natural disasters, system failures, or even accidental user actions. Threat modeling involves identifying potential threats relevant to the organization's assets.

### E. Risque (Risk)

*   **Definition:** Risk is the **probability ("probabilité")** that a specific **threat will materialize** ("se transforme en réalité") and successfully exploit a vulnerability, resulting in damage or an incident.
*   **Analogy:** The player who doesn't eat well (vulnerability) *risks* getting injured (incident). The risk is the likelihood of the threat (poor health leading to injury) actually occurring.
*   **Conceptual Formula Mentioned:** **Risk = Threat x Vulnerability x Asset (Value/Impact)**.
    *   *Interpretation:* High levels of threats, numerous vulnerabilities, or highly valuable assets lead to a higher overall risk.
*   **Key Idea:** Risk is fundamentally about **likelihood and potential impact**.

> **Elaboration:** Risk management involves identifying, assessing, and prioritizing risks. It combines the likelihood of a threat exploiting a vulnerability with the potential impact on the asset. This allows organizations to decide how to handle the risk (e.g., mitigate, transfer, accept, avoid).

### F. Attaque (Attack)

*   **Definition:** An attack is a **deliberate and malicious action ("action volontaire et malveillante")** aimed at causing damage to an asset.
*   **Relationship to Threat:** An attack is the **concretization ("concrétisation")** or realization of a threat. It's the threat in action.
*   **State:** When an attack occurs, the threat is no longer just a potential; it has transformed into a **real event**.
*   **Analogy:** The football player *is* injured (the potential risk has become reality through some event/action).
*   **IT Example:** The computer *is* hacked (the threat actor has successfully exploited a vulnerability).

> **Elaboration:** An attack is the active attempt to compromise security. Examples include deploying malware, launching a DDoS attack, attempting unauthorized access, or conducting a phishing campaign. It's the "verb" corresponding to the "noun" of a threat.

### G. Contre-mesure (Countermeasure)

*   **Definition:** Countermeasures are **IT security measures**; essentially **defensive measures ("mesures défensives")**.
*   **Form:** They can be technical (e.g., software, hardware devices), procedural (e.g., policies, guidelines), or other types of controls.
*   **Objective:**
    *   To **oppose an incident** affecting an asset.
    *   To **counter an attack** that could harm assets.
*   **Two Types:**
    1.  **Preventive Countermeasures ("préventives"):**
        *   **Timing:** Implemented *before* an attack, during the threat phase, to prevent the threat from materializing or exploiting a vulnerability.
        *   **Analogy:** Advising the player to eat well *before* they get injured.
        *   **IT Example:** Installing and updating antivirus software *before* an infection occurs. Aims to minimize the probability (risk) of an incident.
    2.  **Corrective Countermeasures ("correctives"):**
        *   **Timing:** Implemented *after* an attack or incident has occurred.
        *   **Analogy:** Starting the treatment/healing process for the player *after* they have been injured.
        *   **IT Example:** Performing system maintenance, cleanup, or restoration *after* a computer has been hacked. Aims to recover from the incident and potentially prevent recurrence.

> **Elaboration:** Countermeasures are the tools and strategies used to manage risk. Preventive measures aim to reduce the likelihood of incidents, while corrective measures aim to reduce the impact of incidents that do occur. A comprehensive security strategy employs both types.

---

## III. Conclusion and Call for Questions

*   **Summary:** The professor believes the definitions provided should clarify these fundamental terms.
*   **Engagement:** Encourages viewers to ask questions in the comments if anything is unclear.
*   **Goal:** To enrich the content further and ensure better comprehension ("acquérir plus de prévention" - likely meant "compréhension" or understanding) of IT security.

---