# SSL and TLS

## What is SSL and TLS

SSL (Secure Sockets Layer) and TLS (Transport Layer Security) are cryptographic protocols designed to provide secure communication over a network. SSL was the original protocol developed by Netscape in the mid-1990s to encrypt web traffic between browsers and servers. SSL went through versions 1.0, 2.0, and 3.0, each addressing security flaws found in the previous version. However, SSL 3.0 itself was found to have serious vulnerabilities, most notably the POODLE attack discovered in 2014, which exploited a flaw in SSL 3.0's padding scheme.

TLS was introduced as the successor to SSL, starting with TLS 1.0 (which was essentially SSL 3.1 with minor improvements and a new name to signal that the protocol was no longer under Netscape's control). The evolution continued through TLS 1.1 (RFC 4346, 2006), TLS 1.2 (RFC 5246, 2008), and TLS 1.3 (RFC 8446, 2018). Each version improved security by removing weak cipher suites, adding stronger hashing algorithms, and streamlining the handshake process. Today, SSL is considered entirely deprecated, and the term "SSL certificate" is still commonly used in marketing and casual conversation, but the actual protocol in use is TLS. All modern browsers and servers support TLS 1.2 and TLS 1.3, and older versions (SSL 3.0, TLS 1.0, TLS 1.1) have been disabled by default in most software due to known security vulnerabilities.

---

## The TLS Handshake Process

The TLS handshake is the sequence of messages exchanged between a client and a server to establish a secure connection before any application data is transmitted. The handshake accomplishes three critical goals: it authenticates the server (and optionally the client), it negotiates the encryption algorithms and parameters to be used, and it establishes a shared secret key that both parties will use to encrypt subsequent communication.

### TLS 1.2 Handshake

The TLS 1.2 handshake typically requires two round trips (four flights of messages) before application data can be sent.

1. **ClientHello:** The client initiates the handshake by sending a ClientHello message to the server. This message contains the highest TLS version the client supports, a list of supported cipher suites (ordered by preference), a list of supported compression methods, a client-generated random number (32 bytes), and optional extensions such as the Server Name Indication (SNI) field, which tells the server which hostname the client is trying to reach.

2. **ServerHello:** The server responds with a ServerHello message, selecting the highest TLS version supported by both parties, choosing a cipher suite from the client's list, and providing its own 32-byte random number. The server also sends its digital certificate (X.509), which contains its public key and is signed by a Certificate Authority. If the server requests client authentication, it sends a CertificateRequest message. The server may also send a ServerKeyExchange message if the chosen cipher suite requires additional key exchange parameters (such as Diffie-Hellman parameters).

3. **Key Exchange:** The client verifies the server's certificate by checking its validity period, confirming that it chains back to a trusted root CA, and ensuring the hostname matches the server's identity. The client then generates a pre-master secret, encrypts it with the server's public key (in RSA key exchange), and sends it to the server in a ClientKeyExchange message. Alternatively, in Diffie-Hellman key exchange, both sides exchange DH parameters and independently compute the shared secret without ever transmitting it directly. The client sends a ChangeCipherSpec message indicating that subsequent messages will be encrypted, followed by a Finished message encrypted with the newly negotiated keys.

4. **Server Finished:** The server processes the client's key exchange message, derives the same session keys, sends its own ChangeCipherSpec message, and sends an encrypted Finished message. At this point, both sides have confirmed that the handshake was not tampered with, and secure communication can begin.

### TLS 1.3 Handshake

TLS 1.3 significantly streamlined the handshake by reducing it to one round trip (or even zero round trips for resumed sessions). The key improvements include the removal of RSA key exchange in favor of Diffie-Hellman (providing forward secrecy by default), the elimination of obsolete and insecure cipher suites, and the merging of the ServerHello and key exchange into a single flight.

1. **ClientHello:** The client sends its supported TLS version (1.3), cipher suites, random number, and key share extension containing Diffie-Hellman public values. This allows the server to immediately compute the shared secret without waiting for a second round trip.

2. **ServerHello:** The server responds with its selected cipher suite, its own random number, its Diffie-Hellman public value, and its certificate. Because the server can compute the shared secret immediately from the client's key share, it can encrypt its certificate and the rest of the handshake messages right away. The server sends an encrypted Finished message to confirm the handshake.

3. **Client Finished:** The client verifies the server's certificate, computes the shared secret, and sends its own encrypted Finished message. Application data can now flow in both directions.

For resumed sessions, TLS 1.3 supports 0-RTT (zero round-trip time) resumption, where the client can send application data along with its first flight of handshake messages using a pre-shared key from a previous session. This dramatically reduces latency for returning visitors.

---

## Symmetric vs Asymmetric Encryption in TLS

TLS uses both symmetric and asymmetric encryption in a complementary fashion, leveraging the strengths of each while mitigating their weaknesses.

### Asymmetric Encryption

Asymmetric encryption (also called public-key cryptography) uses a pair of keys: a public key that can be freely shared and a private key that must be kept secret. Data encrypted with the public key can only be decrypted with the corresponding private key, and vice versa. In TLS, asymmetric encryption is used during the handshake phase for two purposes: authenticating the server (the server proves it holds the private key corresponding to its certificate's public key) and securely exchanging or deriving the symmetric session key. Common asymmetric algorithms include RSA, ECDSA (for digital signatures), and ECDH (for key exchange). The main disadvantage of asymmetric encryption is its computational cost; it is orders of magnitude slower than symmetric encryption and is impractical for encrypting large amounts of data.

### Symmetric Encryption

Symmetric encryption uses a single shared key for both encryption and decryption. Both the client and the server derive the same session key during the TLS handshake and use it to encrypt all subsequent application data. Symmetric encryption is extremely fast and efficient, making it suitable for encrypting the potentially large volumes of data exchanged during a web session. Common symmetric algorithms include AES (Advanced Encryption Standard) in modes like GCM (Galois/Counter Mode), which provides both encryption and integrity, and ChaCha20-Poly1305, which is designed for performance on devices without hardware AES acceleration. The main challenge with symmetric encryption is key distribution; both parties need to agree on the same key without an eavesdropper intercepting it, which is exactly what the TLS handshake solves using asymmetric encryption.

---

## Certificate Authorities and the Chain of Trust

The TLS ecosystem relies on a hierarchical trust model built on Certificate Authorities (CAs). At the top of the hierarchy are root CAs, whose self-signed certificates are pre-installed in browsers and operating systems as trust anchors. Below the root CAs are intermediate CAs, whose certificates are signed by root CAs or other intermediate CAs. At the bottom are end-entity (leaf) certificates, issued to specific domains or organizations by intermediate CAs.

When a browser receives a server certificate during the TLS handshake, it validates the certificate by building a chain from the leaf certificate through one or more intermediate certificates up to a trusted root. At each step, it verifies the digital signature on the certificate using the issuer's public key, checks that the certificate has not expired, confirms that the certificate has not been revoked (via CRL or OCSP), and ensures that the hostname in the URL matches the subject name or Subject Alternative Names (SANs) in the certificate.

This chain of trust model means that if any CA in the chain is compromised, an attacker could issue fraudulent certificates for any domain. Several high-profile CA breaches have occurred, including the DigiNotar compromise in 2011, which led to the fraudulent issuance of certificates for Google, Yahoo, and other major domains. To mitigate such risks, the industry has developed mechanisms like Certificate Transparency (CT), which requires all publicly trusted certificates to be logged in publicly auditable, append-only logs, making it possible to detect unauthorized certificates.

---

## Self-Signed Certificates vs CA-Signed Certificates

A self-signed certificate is one where the issuer and the subject are the same entity; the certificate is signed with its own private key rather than by a CA. Self-signed certificates are useful for development and testing environments, internal services that do not face the public internet, and scenarios where the client can be pre-configured to trust the specific certificate. However, self-signed certificates are not trusted by default by any browser or operating system, because there is no third-party vouching for the identity of the certificate holder. Users connecting to a server with a self-signed certificate will see a browser warning and must manually accept the risk.

CA-signed certificates are issued by a trusted Certificate Authority after the applicant proves control over the domain (through DNS challenges, HTTP file placement, or email verification). CA-signed certificates are automatically trusted by browsers and operating systems that include the issuing CA in their trust store. For public-facing websites, CA-signed certificates are the only practical option. Let's Encrypt, a free and automated CA, has made it trivially easy to obtain CA-signed certificates, removing cost as a barrier to HTTPS adoption.

---

## SNI (Server Name Indication)

Server Name Indication (SNI) is a TLS extension that allows the client to specify which hostname it is trying to connect to during the TLS handshake, specifically in the ClientHello message. Without SNI, when multiple HTTPS websites are hosted on the same IP address (virtual hosting), the server would not know which certificate to present during the handshake, because the HTTP Host header is not available until after the TLS connection is established. SNI solves this chicken-and-egg problem by including the target hostname in the ClientHello, allowing the server to select the correct certificate for that hostname before the TLS handshake completes.

SNI is critical for the modern web, where many websites share a single IP address on shared hosting platforms. However, the standard SNI extension sends the hostname in plaintext as part of the ClientHello, which means that any network observer can see which website a user is connecting to, even though they cannot see the content of the communication. This privacy concern has led to the development of Encrypted Client Hello (ECH), a TLS 1.3 extension that encrypts the SNI field, preventing passive observers from determining the target hostname.

The [[SNI Injector Explained]] technique exploits the fact that SNI is transmitted in plaintext during the TLS handshake. By injecting a specific hostname into the SNI field, the traffic can be made to appear as if it is destined for a whitelisted domain, allowing it to pass through restrictive firewalls that filter based on SNI values.

---

## Common TLS Vulnerabilities and Mitigations

### BEAST (Browser Exploit Against SSL/TLS)

BEAST, disclosed in 2011, exploited a vulnerability in CBC (Cipher Block Chaining) mode in SSL 3.0 and TLS 1.0, where the initialization vector (IV) for each block was predictable. This allowed an attacker to decrypt parts of the encrypted traffic using a chosen-plaintext attack. The mitigation was to use TLS 1.1 or higher, which uses explicit IVs, and to prefer AEAD (Authenticated Encryption with Associated Data) cipher suites like AES-GCM.

### POODLE (Padding Oracle On Downgraded Legacy Encryption)

POODLE, disclosed in 2014, exploited SSL 3.0's flawed padding validation in CBC mode, allowing attackers to decrypt ciphertext one byte at a time. The primary mitigation was to disable SSL 3.0 entirely in both clients and servers. The POODLE attack also highlighted the danger of protocol downgrade attacks, where an attacker forces the client and server to fall back to an older, weaker protocol version.

### Heartbleed

Heartbleed, disclosed in 2014, was a critical vulnerability in OpenSSL's implementation of the TLS Heartbeat extension. It allowed an attacker to read up to 64KB of the server's memory per heartbeat request, potentially exposing private keys, session tokens, and other sensitive data. The vulnerability was not in the TLS protocol itself but in a specific implementation. The fix was to patch OpenSSL and reissue certificates for affected servers.

### ROBOT (Return Of Bleichenbacher's Oracle Threat)

ROBOT, disclosed in 2017, revived a 1998 attack by Bleichenbacher against RSA PKCS#1 v1.5 encryption. Some TLS implementations incorrectly handled errors in RSA padding, creating an oracle that an attacker could use to decrypt traffic or forge signatures. The mitigation involved implementing constant-time RSA padding checks and, ideally, disabling RSA key exchange in favor of Diffie-Hellman-based key exchange.

### Forward Secrecy

Forward secrecy (also called perfect forward secrecy) is a property of key exchange mechanisms where compromise of the server's long-term private key does not compromise past session keys. TLS 1.3 provides forward secrecy by default by mandating ephemeral Diffie-Hellman key exchange. In TLS 1.2, forward secrecy is achieved by using DHE or ECDHE cipher suites, but it is not the default; servers must be explicitly configured to prefer these suites over static RSA key exchange.

---

## Relationship to Other Concepts

[[HTTP and HTTPS]] is the most direct consumer of TLS. HTTPS is simply HTTP running over a TLS-encrypted connection, and every aspect of web security, from encrypted data transmission to certificate validation, depends on the TLS protocol. Understanding the TLS handshake is essential for understanding how HTTPS connections are established and secured.

[[SNI Injector Explained]] relies on the mechanics of the TLS handshake, specifically the SNI extension. The technique of injecting a specific hostname into the ClientHello message to bypass network filters is only possible because SNI is transmitted in plaintext during the handshake. Understanding TLS is essential for understanding both how SNI injection works and its limitations.

---

## Key Takeaways

SSL and TLS are the cryptographic protocols that secure network communication, with TLS being the modern standard. The TLS handshake establishes encryption parameters, authenticates the server, and derives session keys using a combination of asymmetric and symmetric cryptography. The chain of trust model based on Certificate Authorities ensures that clients can verify the identity of the servers they connect to. SNI enables virtual hosting over HTTPS but introduces privacy considerations that are being addressed by newer extensions like Encrypted Client Hello. Understanding TLS vulnerabilities and their mitigations is essential for maintaining secure systems in an evolving threat landscape.
