

# Module 3: Cryptography

**Author:** Dr. RIAHLA
**Year:** 2020
**Institutions:** University De Boumerdes

*(Note: University of Limoges logo is missing from this module's title slide in the OCR)*

---

## Outline

1.  Introduction, Definition, and History
2.  Current Cryptography
3.  Digital Signatures and Certificates
4.  Applications of Cryptography

---

## Introduction and History

*(This slide serves as a section marker)*

-   (Image depicts a Roman general, likely Caesar, and legionaries).

---

## History and Introduction (Caesar Cipher)

-   When Julius Caesar sent messages to his generals, he did not trust his messengers.
-   He therefore replaced all 'A's in his messages with 'D's, 'B's with 'E's, and so on for the entire alphabet (a shift of 3).
-   Only the person knowing the rule of "shift by three" could decipher his messages.
-   "And that's how it all began..."

---

## History and Introduction (Modern Uses)

-   Nowadays, cryptography is found in:
    -   Military applications.
    -   Banking systems.
    -   Internet (purchases, identification).
    -   Mobile phones.
    -   Pay TV.
    -   Electronic identity cards.
    -   Electronic voting.

---

## History and Introduction (Protecting Information)

-   To protect information:
    -   **Steganography**
    -   **Cryptography**
        -   Transposition
        -   Substitution

---

## History and Introduction (Steganography)

-   **Steganography: Covered Writing**
-   Ancient example: Certain generals shaved their slaves' heads, tattooed a message, and waited for the hair to regrow to pass important information.
-   (Image shows a bust with a shaved head).
-   Modern definition: Information is hidden within other information to make it invisible.
-   (Image shows text hidden within other text, revealed by a magnifying glass labeled "Steganography").

---

## History and Introduction (Cryptography)

-   **Cryptography:** Information is modified according to a pre-established method to make it incomprehensible.
-   (Diagram shows Symmetric Encryption: Plain Text -> Encryption with Secret Key -> Cipher Text -> Decryption with Same Secret Key -> Plain Text).

---

## History and Introduction (Cryptography Categories)

-   Cryptography: Two major categories exist:
    -   **By transposition:** The order of elements in information is modified (shifting characters in a phrase, pixels in an image, ...).
    -   **By substitution:** Elements of information are replaced by others (replace all A's with B's, B's with C's, etc...).

---

## Cryptography (Section Marker)

*(This slide transitions to core definitions)*

---

## Definitions

-   **Traditional Protagonists:**
    -   **Alice** or Anne and **Bob** wish to transmit data to each other.
    -   **Oscar** or **Mallory**, an opponent who wishes to spy on Alice and Bob.
    -   (Diagram shows Alice, Bob, and Mallory icons).
-   (Network diagram shows Alice on Network A communicating with Bob on Network B via the internet, with Mallory potentially intercepting in the middle/tunnel).

---

## Definitions (Terminology)

-   **Plaintext 'M':** This expression denotes the original message that has undergone no modification.
-   **Key:** Designates the information allowing a message to be encrypted and decrypted.
-   **Encryption:**
    -   Function 'E' transforming a message M in such a way as to render it incomprehensible.
    -   Based on an encryption function E.
    -   Thus generates an encrypted message (Ciphertext) **C = E(M)**.

---

## Definitions (Terminology Cont.)

-   **Decryption:**
    -   Function 'D' for reconstructing the plaintext message from the ciphertext.
    -   Based on a decryption function D.
    -   We thus have **D(C) = D(E(M)) = M**.
-   **In practice:** E and D are generally parameterized by keys Ke (Encryption Key) and Kd (Decryption Key):
    -   **E<sub>ke</sub>(M) = C**
    -   **D<sub>kd</sub>(C) = M**
-   (Diagrams illustrate these formulas, showing function, key, plaintext, ciphertext relationships).

---

## Definitions (Encryption and Decryption Flow)

-   (Diagram shows: Plaintext Document -> Encryption Process (Padlock) -> Ciphertext Document -> Decryption Process (Key) -> Plaintext Document).

---

## Definitions (Cryptography and Cryptanalysis)

-   **Cryptography:** The science that uses mathematics for the encryption and decryption of data.
-   **Cryptanalysis:** The study of encrypted information in order to discover the secret.
-   **Cryptology:** Encompasses both cryptography and cryptanalysis.

---

## Definitions (Cryptography Example: Caesar Cipher)

*(Section marker for the Caesar cipher example)*

---

## Caesar Cipher

-   Consists of shifting the plaintext alphabet. The shift amount is the key for the cipher.
-   **Example:** We want to encrypt the word CRYPTOGRAPHIE with a shift of 3. For this, we write the plaintext and ciphertext alphabets as follows:
    -   Plain:  ABCDEFGHIJKLMNOPQRSTUVWXYZ
    -   Cipher: DEFGHIJKLMNOPQRSTUVWXYZABC
-   And we replace:
    -   CRYPTOGRAPHIE ---> **FUBSWRJUDSKLH**

---

## Caesar Cipher (Diagram)

-   (Diagram shows Alice sending FUBSWRJUDSKLH to Bob. Mallory intercepts but sees gibberish ['????...']. Both Alice and Bob have the A->D shift mapping).

---

## Caesar Cipher (Formula)

-   K = x, x < 26 (The key 'K' is the shift amount, less than 26).
-   Encryption: C = E(M) = (M + k) mod 26
-   Decryption: M = D(C) = (C - k) mod 26
-   (Mallory doesn't know K).

---

## Caesar Cipher (Components Diagram)

-   (Diagram relates the shift 'K' to the general concepts: E<sub>ke</sub>(M) = C uses 'Shift amount?' as the key. D<sub>kd</sub>(C) = M uses 'Inverse Shift' as the key).

---

## Caesar Cipher (Cryptanalysis)

-   **Weakness:** There are only 26 possible keys!
-   Given an encrypted message, one only needs to test the 26 possible keys to find the plaintext message.
-   This can be done in a few minutes!!
-   **Solution:** Use a randomly shuffled ciphertext alphabet.

---

## Caesar Cipher (Random Substitution)

-   **Example:**
    -   Plain:  ABCDEFGHIJKLMNOPQRSTUVWXYZ
    -   Cipher: OHGFEDCBUKJPNMIQRXSTLZXYWV (A random permutation)
-   In this case, the number of possible keys increases to 400,000,000,000,000,000,000,000,000 (4 x 10<sup>26</sup>)!!!
-   **Cryptanalysis:** It is obviously impossible to test all possible keys, even a very powerful computer is incapable of doing it in a reasonable time (300,000 years!!).

---

## Caesar Cipher (Random Substitution: Cryptanalysis)

-   **However, it is still possible to break this cipher in a few minutes!!**
-   In the French language, for example, we know that the frequency of appearance of each letter is relatively stable. It is therefore sufficient to:
    -   Measure the frequency of appearance of each letter in a ciphertext text.
    -   Compare with the frequency table of French letters.
    -   Deduce the ciphertext alphabet.
-   (Table and graph show letter frequencies for French, English, Spanish, German. A comparison table shows letter counts/percentages for plaintext 'e', 'a', 's', 'i', etc. being mapped to ciphertext 'h', 'j', 'e', 'k' etc. based on frequency).

---

## Other Classical Systems

-   Homophones (solution for frequency analysis attack).
-   Affine cipher (polynomial).
-   Playfair cipher (polygraphic cipher).
-   Hill cipher (matrices).
-   Vigenère cipher (improvement on Caesar cipher).
-   Vernam cipher (one-time pad).
-   Transpositions.
-   ...
-   The Enigma machine.
-   ...

---

## Definitions (Modern Cryptography)

*(Section marker)*

---

## Symmetric Cryptography

-   Also known as private key cryptography.
-   Uses the **same key** to encrypt and decrypt a message (**ke = kd = k**).
-   The two communicants must both be in possession of this key.
-   The Data Encryption Standard (DES, 3DES, AES) are examples of this type of system widely used by the U.S. federal government.
-   (Flowcharts for DES and AES algorithms are shown).
-   (Diagram shows encryption and decryption using the same single key).

---

## Symmetric Cryptography (Advantages and Disadvantages)

-   **Advantage:**
    -   It is very fast.
-   **Disadvantage:**
    -   **Key distribution** remains the major problem of conventional encryption, especially when the number of communicants becomes large.
-   In other words, how can the key be delivered to its recipient without any person intercepting it?
-   (Diagram shows Mallory with a pirate eye patch intercepting the key being sent from Network A to Network B).
-   (Note: The solution was found in the early 70s, based on research since the 50s).

---

## Symmetric Cryptography (How to Share a Secret?)

-   (Analogy: The classic river crossing puzzle with a man, wolf, two sheep, and a boat is shown).
-   **Postman Example:** Assume Alice wants to send a secret package to Bob by post, but their postman (Mallory) cannot help but read unsealed correspondence. How can she send it to him?

---

## Symmetric Cryptography (How to Share a Secret? - Padlock Protocol)

1.  Alice puts her package in a box that she closes with a padlock and sends it to Bob.
2.  Bob receives the package, adds a padlock to the box, and sends it all back to Alice.
3.  Alice removes her padlock with her key and sends the box back to Bob.
4.  Bob can now open the box with his key and enjoy the package.
-   **Remark:** At no point was the postman able to open the box.
-   (Diagram illustrates this multi-step process with padlocks).

---

## Symmetric Cryptography (Problem?)

-   Still and always problems!!
-   In particular, the **order** in which the successive encryptions and decryptions are performed plays a crucial role, not to mention the **flow**!!!
-   Furthermore, exchanges can only happen when **both parties are present** (interactive).
-   From this arises asymmetric (public key) cryptography.

---

## Asymmetric Cryptography

-   Each entity possesses a **pair of keys**:
    -   A **public key**, known by all other entities and used to encrypt a given message.
    -   A **private key**, which must only be known by the entity possessing the pair in question, and which is used to decrypt a message.
-   A message encrypted with a public key can **only be decrypted with the corresponding private key**.
-   (Diagrams conceptually show key pairs, one public [happy face], one private [faces + key]).
-   (Diagram shows Alice, Bob, Mallory. Alice uses Bob's public key to encrypt. Bob uses his private key to decrypt. Mallory cannot decrypt).

---

## Asymmetric Cryptography (Padlock Analogy)

-   Bob leaves his (open) padlocks freely accessible at the post office (like public keys).
-   Alice can at any time come to the post office, take a padlock, and send a message to Bob secured by it.
-   Bob can easily open his padlock with his key and retrieve the message.
-   (Diagram shows public padlock icons and private key icons).

---

## Asymmetric Cryptography (Encryption/Decryption Flow)

-   (Diagram shows Plaintext -> Encrypt with Public Key (open lock) -> Ciphertext -> Decrypt with Private Key (key) -> Plaintext).

---

## Asymmetric Cryptography (Details)

-   **Difficulty:** Need an encryption system having different keys ke and kd.
-   **Goal:** Find mathematical functions that are:
    -   Easy to use in one direction (encryption).
    -   Very difficult to reverse (decryption without private key).
-   **Problem:** Very demanding in computation, especially with a large message to encrypt!!! **1000 times slower than AES.**
-   **Solution:** Asymmetric encryption is used to distribute symmetric keys (Hybrid approach).

---

## Asymmetric Cryptography (Example in PGP System)

-   (Diagram shows: Plaintext -> Encrypt with Session Key -> Ciphertext. Session Key -> Encrypt with Public Key -> Encrypted Session Key. Both are sent. Reverse process for decryption).
-   *Functioning of PGP encryption.*
-   *Functioning of PGP decryption.* (Separate diagram showing receiving Ciphertext + Encrypted Session Key -> Decrypt Session Key with Private Key -> Use Session Key to Decrypt Ciphertext -> Plaintext).

---

## Asymmetric Cryptography (Algorithms)

-   Based on computationally hard problems:
    -   Exponentiation of large prime numbers (**RSA**).
    -   The discrete logarithm problem (**ElGamal**).
    -   The knapsack problem (**Merkle-Hellman**).

---

## Asymmetric Cryptography (RSA: The First Public Key Protocol)

-   Alice chooses two large prime numbers p and q and calculates: **n = p\*q** and **z = (p-1)(q-1)**.
-   She chooses an integer **e** that has no common factor with z (coprime).
-   She calculates **d** such that (e\*d - 1) is exactly divisible by z.
-   She deduces: **Public Key = (n, e)** and **Private Key = (n, d)**.
-   Thanks to her public key, Bob can encrypt his message using the RSA formula. But he can no longer decrypt it, because RSA is impossible to reverse unless p and q are known.
-   Alice receives the encrypted message from Bob and can decrypt it thanks to p and q (via d).
-   Bob wants to send message m to Alice:
    -   Encryption: **c = m<sup>e</sup> mod n**
-   Alice receives message c and calculates:
    -   Decryption: **m = c<sup>d</sup> mod n = (m<sup>e</sup> mod n)<sup>d</sup> mod n**

---

## Asymmetric Cryptography (RSA Example)

-   Parameters: p=5, q=7, message m=12
-   Calculations:
    -   n = 5\*7 = 35, z = (5-1)(7-1) = 4\*6 = 24.
    -   Alice chooses e=5 (coprime with 24) and deduces d=29 (since 5\*29 - 1 = 144, which is divisible by 24).
    -   Bob (encryption): m=12, m<sup>e</sup> = 12<sup>5</sup> = 248832. c = 248832 mod 35 = **17**.
    -   Alice (decryption): c=17, c<sup>d</sup> = 17<sup>29</sup> = 48196857210675091411825223072000. m = (huge number) mod 35 = **12**.

---

## Asymmetric Cryptography (RSA Challenge)

-   Factor the number: (RSA-129, a 129-digit number is shown).
-   And use this factorization to decrypt a message encoded with RSA.
-   $100 was offered to the first who managed to decrypt the message.
-   The goal of this contest was to test the robustness of RSA.
-   It took **17 years** for a team of 600 people to win the contest!!!

---

## Asymmetric Cryptography (New Challenge Launched)

-   (A much larger number, RSA-2048 likely, is shown).
-   Reward **$200,000** !!!

---

## How to Ensure Other Security Objectives???

-   So far, we have only dealt with **confidentiality**!!!!!
-   What about the other objectives?
    -   **Authentication**
    -   **Integrity of data,**
    -   **Non-repudiation**
-   **Solution:** **Digital Signature**

---

## Digital Signature

-   One of the main advantages of public key cryptography is that it offers a method for using digital signatures.
-   It is a data string that associates a message (in its digital form) with the entity from which it originated.
-   Digital signatures are widely used in IT security, for **authentication** or **data integrity**, and **non-repudiation**.
-   (Image shows a hand signing a document).
-   (Diagram shows: Original Text -> Sign with Private Key -> Signed Text -> Verify with Public Key -> Verified Text). *Simple digital signatures.*

---

## Digital Signature (Problem & Solution)

-   **Problem:** Very demanding in computation, especially with a large message to encrypt!!!
-   (Diagram shows asymmetry - signing is like encrypting with private key, verification like decrypting with public key).
-   **Solution: Hash Function**

---

## Digital Signature (Hash Function)

-   The previous system is slow and produces a large volume of data.
-   Adding a one-way **hash function** improves the previous scheme.
-   This function processes a variable-length input and outputs a fixed-length element, namely 160 bits (for SHA-1).
-   (Diagram shows: Plaintext -> Hash function (SHA-1) -> HASH value).
-   In case of data modification, the hash function gives a different output value.

---

## Digital Signature (Hash Function: PGP Example)

-   (Diagram shows: Plaintext -> Hash Function -> Hash Summary. Hash Summary -> Encrypt with Private Key (Signature). Plaintext + Signature are sent. Verification: Received Plaintext -> Hash Function -> Compare Hashes. Received Signature -> Decrypt with Public Key -> Compare Hashes). *Secured digital signatures*.

---

## Digital Signature (Examples of Hash Functions)

-   **MD5:** Message Digest 5, generates a 128-bit fingerprint.
-   **SHA-1:** Secure Hash Algorithm, generates a 160-bit fingerprint.

---

## Another Problem with Asymmetric Cryptography

-   (Diagram shows Mallory intercepting communication between Alice and Bob, with a pirate eye patch, saying "I am Alice, here is my public key").
-   A person can place a false key (e.g., the pirate's key) bearing the name and user ID of the recipient.
-   Encrypted (and intercepted) data intended for the real owner of this erroneous key is now in the wrong hands.
-   Therefore, users must constantly verify that they are encrypting to the correct user's key.
-   **Solution:** The use of **Digital Certificates**.

---

## Digital Certificates

-   Certificates are issued by a **Certificate Authority (CA)**.
-   Digital certificates simplify the task of determining if a public key truly belongs to its supposed owner.
-   A certificate corresponds to a reference. It could be, for example, your driver's license, your social security card, or your birth certificate.
-   Each of these items contains information identifying you and stating that **another person has confirmed your identity**.
-   (Diagram shows components: Public Key, Name, Validity Period, Attributes, CA Signature, CA Name).
-   (Image shows a sample student ID card as an analogy).

---

## Digital Certificates (Examples)

-   **Example PGP Certificate:** (Diagram shows PGP certificate structure: Public key details, User ID, Signature linking ID to key, including certifier's details, hash algorithm, signed hash, key ID).
-   **Example X.509 Certificate:** (Diagram shows X.509 structure: Public key value, Subject unique name (DN), Issuer unique name, Certificate format version, Serial number, Signature algorithm identifier, Issuer name, Validity period, Subject name, Extensions. Signed by CA's private key).

---

## Digital Certificates (Principle)

-   (Diagram shows flow: 1. Alice registers with Authority. 2. Bob requests Alice's public key from Directory. 3. Authority provides certificate to Bob).
-   Alice makes a request for certification of a public key to a certification authority (CA).
-   The CA verifies the veracity of the information contained in this certificate (authentication of info) then the certificate is issued in a directory.
-   Bob retrieves Alice's public key via the directory, also retrieves a self-signed certificate via the CA, and verifies its integrity thanks to the CA's signature.
-   (Screenshot shows details of a digital certificate in a Windows properties dialog).

---

## PKI (Public Key Infrastructure)

-   **Nature:** Infrastructure (set of elements, protocols, and services).
-   **Role:** Large-scale management of public keys.
    -   Registration and issuance.
    -   Storage and distribution.
    -   Revocation and status verification.
    -   Use of certificates.
-   It's the entire infrastructure necessary for the functioning of one or more CAs to deliver certificates:
    -   **Hardware:** computers, premises…
    -   **IT:** software
    -   **Human:** employees
    -   **Organizational:** revocation procedures…
    -   **Administrative:** designation of a responsible person
    -   **Financial:** risk insurance in case of damage from certificate use.
-   (Diagram shows PKI components: Sender, Recipient, Certification Authority, Registration Authority, Verification Authority, Signed Data, Certificate Public Key, Certificate Private Key).

---

## Summary (Cryptography)

-   **Confidentiality (hybrid encryption):**
    -   Symmetric (session) Key to encrypt messages.
    -   Asymmetric Key to encrypt the symmetric key.
-   **Integrity, Authentication, Non-repudiation:**
    -   Hash functions for the digital signature.
    -   Certificates to authenticate public keys.

---

## Other Encryption Systems

-   Diffie-Hellman key exchange
-   Threshold cryptography
-   Quantum cryptography (using properties of quantum physics)
-   MAC (Message Authentication Code)
-   ECC (Elliptic Curve Cryptography)
-   TESLA (Timed Efficient Stream Loss-Tolerant Authentication)
-   ...

---

## Uses of Cryptography / Secure Applications and Communications

-   (Images: Kerberos logo, PGP logo, VPN map, HTTPS lock, SSH terminal, various bank/ID cards).
-   The applications and Secure Communications.

---

## Secure Communications

*(Section marker)*

---

## The SSH Protocol (Secure Shell)

-   Remote access protocols like Telnet, rlogin, etc., are limited:
    -   Circulation of passwords in clear text.
    -   Weak authentication based on IP number.
    -   Insecure remote commands.
    -   Insecure file transfers.
-   **Solution:** Use the SSH protocol.
-   SSH uses asymmetric (RSA) and symmetric cryptography.

---

## The SSH Protocol (Principle)

-   The server has a key pair stored (e.g., in /etc/ssh) and generated at startup.
1.  When an SSH client connects to the server, the latter sends its public key to the client.
2.  The client generates a secret key (for symmetric encryption) and sends it to the server, encrypting the exchange with the server's public key.
3.  The server decrypts the secret key with its private key.
4.  To prove to the client that it is indeed the correct server (server authentication), it encrypts a standard message with the secret key and sends it to the client.
5.  If the client recovers the standard message using the secret key, it has proof that the server is genuine.
6.  Once the secret key is exchanged, the client and server can then establish a secure channel (thanks to the shared secret key).

---

## Flaw of the SSH Protocol

-   Attack based on the **Man In The Middle** method.
-   (Diagram shows a 'Pirate' computer sitting between the 'Host' client and the 'Server', intercepting and relaying the SSH session, potentially deceiving both ends).

---

## SSL/TLS

-   (Image shows HTTPS lock in a browser bar).
-   **SSL (Secure Socket Layer):**
    -   Is situated between the application layer and the transport layer.
    -   Guarantees authentication, integrity, and confidentiality.
    -   Developed by Netscape and widely used for securing www sites (https).
    -   The last version mentioned is SSL 3.0.
-   **TLS (Transport Layer Security):**
    -   TLS 1.0 replaces SSL (very few differences).
    -   TLS 1.1 is the latest version mentioned.
    -   All Web servers and browsers support TLS version 1.1 (as of the slide's creation).

---

## VPN Network (Virtual Private Network)

-   (Image shows a world map with VPN connection points).
-   Allows establishing secure communications by relying on an existing non-secure network.
-   VPN uses the **IPsec** protocol which is composed of four protocols:
    -   **AH (Authentication Header):** Guarantees the authenticity of exchanged packets by including a checksum (encrypted header + packet data).
    -   **ESP (Encapsulating Security Payload):** Allows encrypting all packet data, guaranteeing confidentiality.
    -   **IPComp:** Allows compressing a packet before encrypting it with ESP.
    -   **IKE (Internet Key Exchange):** Used for key exchange for the different ciphers.
-   VPN also uses protocols:
    -   **PPTP** (Point-to-Point Tunnelling Protocol)
    -   **L2TP** (Layer 2 Tunnelling Protocol)

---

## Secure Applications

*(Section marker)*

---

## The PGP Tool

-   (Image shows PGP logo and the hybrid encryption diagram again).
-   Is cryptography software well-suited for Internet use.
-   PGP is a combination of the functionalities of public key cryptography and secret key cryptography: **It's a hybrid system**.
-   PGP additionally uses **data compression** to enhance information security, reduce transmission time, and save disk space.

---

## The PGP Tool (Encryption and Decryption)

-   PGP creates a single-use **session key**. This key corresponds to a random number, generated by random mouse movements and keystroke sequences.
-   To encrypt plaintext, the session key uses a conventional symmetric encryption algorithm (DES, AES,...).
-   Once the data is encoded, the session key is encrypted using the recipient's public key (using an asymmetric encryption method).
-   The encrypted session key, as well as the ciphertext, is transmitted to the recipient.
-   The decryption process is inverse: the recipient uses their private key to recover the temporary session key which will then allow decrypting the ciphertext.

---

## The Kerberos Protocol

-   (Image shows Kerberos logo).
-   Kerberos is a network **authentication** protocol.
-   Kerberos uses a system of **tickets** instead of clear text passwords. This principle reinforces system security and prevents unauthorized persons from intercepting user passwords.
-   The entire system relies on **symmetric encryption** (private keys).

---

## The Kerberos Protocol (Elements)

-   In a simple network using Kerberos, we distinguish:
    -   **The client (C):** has its own private key KC.
    -   **The Key Distribution Center (KDC):** knows the private keys KC and KTGS (also called AS: Authentication Server).
    -   **The Ticket Granting Server (TGS):** has a private key KTGS and knows the server's private key KS.
    -   **The server (S):** also has a private key KS.
-   (Diagram shows relationships: AS <-> C <-> TGS <-> S).

---

## Bank Card Protocol

-   (Images show various bank cards and a national ID card).

---

## Card Fabrication

-   (Diagram shows PIN + Account -> Triple DES (using Work Key) -> Encrypted Block. Work Key -> One-way function -> PIN offset). *Note: This diagram is simplified and potentially incomplete as presented.*

---

## Use OpenSSL for Hybrid Crypto Practical Sessions (TPs)

*(Indicates practical exercises using OpenSSL)*

---

## Finally!!!

*(End of the Cryptography module)*

---
---

## Explanation of Subjects Discussed

1.  **Threats Overview:** This section introduces the concept of threats in IT, including security flaws, attacks, and vulnerabilities. The objective is to understand these threats, know how to protect against them, and assess their impact.
2.  **Electronic Messaging Risks:** Email is identified as a critical but inherently insecure tool because messages often travel in clear text. Specific risks detailed include data loss/theft, message alteration, system infection via attachments (viruses, worms, Trojans), message flooding, identity theft, and denial of service. The ease of **forging sender addresses** using basic SMTP commands is explicitly demonstrated.
3.  **Spam (Junk Email):** Defined as unsolicited, non-targeted mass email with falsified sender addresses. The slides explain how spammers abuse legitimate servers, the resulting damage (server overload, filled disks, wasted bandwidth, blacklisting, increased costs for ISPs and users), and provide advice on what *not* to do (e.g., replying validates the address). Protection involves server relay prevention, blacklists, and content filtering. The evolution towards using **botnets** (rented networks of infected machines) and the increasing effectiveness of **anti-spam laws** are mentioned.
4.  **Malware (Viruses, Worms, Trojans, etc.):**
    *   **Viruses:** Code fragments needing other programs to spread, propagating via disk exchange, email attachments, or downloaded executables.
    *   **Worms:** Autonomous programs that spread across networks, often exploiting vulnerabilities or address books (e.g., Code Red, Blaster, "I Love You").
    *   **Trojan Horses:** Malicious programs disguised as legitimate ones, often hiding a payload like a **keylogger**. They can open **backdoors** for remote control, turning the machine into part of a **botnet**.
    *   **Backdoors:** Provide hidden remote access, often installed by Trojans. Characterized by small size and malicious functionalities (downloading code, spying).
    *   **Rootkits:** Malware designed to hide the presence of an intruder and their malicious activities.
    *   **Spyware:** Steals private information and can modify browser behavior.
    *   **Other Types:** Includes **Ransomware** (encrypts files demanding payment), **Adware**, **Dialers**, **Downloaders/Droppers** (install other malware), **Hoaxes**, **Logic Bombs**, etc.
    *   **Impact:** Malware causes data loss, wasted time, reputational damage, system outages, theft, and confidentiality breaches. Modern malware spreads rapidly via the internet. The **Bugbear** worm is detailed as a case study, showcasing multiple propagation methods and malicious payloads (backdoor, keylogger, disabling security).
5.  **Cryptography Introduction:** This section defines cryptography as the science of using mathematics for secure communication (encryption/decryption). It distinguishes it from **steganography** (hiding existence of data) and **cryptanalysis** (breaking codes). The historical origin (Caesar cipher) and modern applications (military, banking, internet) are presented. Basic concepts like **plaintext**, **ciphertext**, **key**, **encryption**, and **decryption** are defined, along with the main categories: **transposition** and **substitution**.
6.  **Caesar Cipher & Cryptanalysis:** This simple substitution cipher (shifting the alphabet by a fixed key) is explained. Its major weakness – only 26 possible keys – makes it easy to break via brute force. Using a random substitution alphabet dramatically increases keyspace, making brute force infeasible. However, it's still vulnerable to **frequency analysis**, comparing letter frequencies in the ciphertext to known language statistics.
7.  **Symmetric Cryptography:** Uses the *same* key for encryption and decryption (e.g., DES, AES). It's very fast but suffers from the **key distribution problem**: how to securely share the secret key? The padlock protocol analogy illustrates a conceptual (though impractical for general crypto) solution to transferring a secret without the intermediary learning it. The need for an interactive protocol highlights limitations leading to asymmetric methods.
8.  **Asymmetric (Public Key) Cryptography:** Each user has a *pair* of keys: a public key (shared widely, used for encryption) and a private key (kept secret, used for decryption). Solves the key distribution problem for confidentiality but is computationally slow (e.g., RSA, ElGamal). Often used in a **hybrid approach** to securely exchange a fast symmetric session key. PGP is cited as an example.
9.  **RSA Algorithm:** The first major public key algorithm is explained step-by-step: choosing primes p, q; calculating n, z; choosing e; calculating d; forming public (n,e) and private (n,d) keys; encryption (m<sup>e</sup> mod n); decryption (c<sup>d</sup> mod n). The difficulty relies on factoring the large number n. RSA challenges demonstrate the computational effort required to break it.
10. **Digital Signatures:** A key application of asymmetric crypto, providing **authentication, integrity, and non-repudiation**. A message is typically *hashed*, and the hash is encrypted with the sender's *private* key. Verification involves decrypting the signature with the sender's *public* key and comparing the hash value. Hash functions (MD5, SHA-1) create fixed-size message digests.
11. **Digital Certificates & PKI:** Address the problem of trusting that a public key actually belongs to the claimed owner. A **Certificate Authority (CA)** verifies an entity's identity and binds it to their public key in a signed **digital certificate** (e.g., X.509 standard). This prevents impersonation (Man-in-the-Middle attacks where Mallory substitutes her key). **Public Key Infrastructure (PKI)** is the entire system (hardware, software, policies, CAs, RAs) for managing certificates at scale.
12. **Secure Communication Protocols:**
    *   **SSH (Secure Shell):** Replaces insecure protocols like Telnet. Uses hybrid crypto (asymmetric for key exchange/server auth, symmetric for session). Vulnerable to sophisticated Man-in-the-Middle attacks if server keys aren't properly verified initially.
    *   **SSL/TLS:** Secures communication between application and transport layers (primarily for HTTPS). Provides confidentiality, integrity, authentication. TLS is the successor to SSL.
    *   **VPN (Virtual Private Network):** Creates secure tunnels over insecure networks using protocols like **IPsec** (which includes AH for authentication, ESP for encryption, IKE for key exchange) or others like PPTP/L2TP.
13. **Secure Applications/Protocols:**
    *   **PGP (Pretty Good Privacy):** Email/file encryption software using a hybrid approach and compression.
    *   **Kerberos:** Network authentication protocol using tickets and symmetric crypto, common in enterprise environments.
    *   **Bank Card Protocols:** Mentioned but not detailed beyond a simplified manufacturing diagram suggesting DES and PIN offsets.