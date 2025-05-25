
# SSH SSL/TLS SNI Injector Explained

## Core Concept

An **SSH SSL/TLS SNI Injector** is a technique used to tunnel SSH (Secure Shell) traffic over a standard SSL/TLS (HTTPS) connection. The "SNI Injector" part specifically refers to manipulating the **Server Name Indication (SNI)** field in the TLS handshake. This makes the SSH traffic appear as legitimate HTTPS traffic to an "allowed" domain, often to bypass firewalls or ISP restrictions that might block direct SSH connections but permit HTTPS traffic.

## Why Use It?

1.  **Bypass Censorship/Firewalls:** Many networks (corporate, public Wi-Fi, restrictive countries) block outbound connections on port 22 (standard SSH) but allow outbound connections on port 443 (standard HTTPS).
2.  **Conceal SSH Traffic:** Wrapping SSH in TLS makes it look like regular web browsing traffic, making it harder to detect and block based on protocol.
3.  **Leverage "Free" or "Whitelisted" Domains:** Some ISPs or mobile carriers offer unmetered access to specific websites (e.g., Facebook, WhatsApp, specific CDNs). By using the SNI of one of these whitelisted domains, the SSH traffic might not count against a data cap or might be allowed through even if other traffic is heavily restricted.

## Key Components

1.  **SSH Client:** Your local machine wanting to connect.
2.  **SSH Server:** The remote server you want to access.
3.  **Client-Side Injector Software:** Runs on your local machine. It listens for local SSH connections, wraps them in TLS, and sends them to the server-side injector, using a specific SNI.
4.  **Server-Side Injector/Proxy Software:** Runs on your remote server (often a VPS). It listens on port 443 (or another HTTPS port), receives the TLS-wrapped traffic, unwraps it, and forwards the actual SSH traffic to the local SSH server daemon (sshd) on the remote server.
5.  **Allowed SNI Hostname:** A domain name that is typically allowed through the restrictive network (e.g., `www.google.com`, `cdn.example.com`). This doesn't mean your server *is* that domain, just that it's *pretending* to be for the initial handshake.
6.  **SSL/TLS Certificate:** The server-side injector needs a valid SSL/TLS certificate. This can be a self-signed certificate (if the client injector is configured to trust it) or a certificate from a recognized CA (like Let's Encrypt) for the domain the server *actually* controls, or even for the SNI hostname if you somehow control it (less common for "bypassing" scenarios).

## How It Works (Behind the Scenes)

Let's assume:
*   Your SSH server is at `your_server_ip`.
*   You want to use `allowed.example.com` as the SNI, which your ISP allows.
*   Direct SSH to `your_server_ip:22` is blocked.
*   HTTPS to `any_ip:443` is allowed, *especially* if the SNI is `allowed.example.com`.

**Flow:**

1.  **Setup:**
    *   **Server-Side:** You install an injector proxy (e.g., `stunnel`, `gost`, `haproxy`, or custom scripts) on your VPS. It's configured to:
        *   Listen on port 443.
        *   Expect TLS connections.
        *   Terminate TLS (decrypt the incoming traffic).
        *   Forward the decrypted payload (which will be SSH traffic) to `localhost:22` (where your actual SSH server is listening on the VPS).
    *   **Client-Side:** You install an injector client (e.g., `stunnel`, `gost`, or specific "injector" apps common on mobile). It's configured to:
        *   Listen on a local port (e.g., `localhost:1080`).
        *   When it receives a connection on `localhost:1080`, it initiates a TLS connection to `your_server_ip:443`.
        *   **Crucially, during the TLS handshake's "Client Hello" message, it inserts `allowed.example.com` into the SNI field.**
        *   It then wraps the traffic from `localhost:1080` inside this TLS tunnel.

2.  **Connection:**
    *   You configure your SSH client (e.g., PuTTY, `ssh` command) to connect to `localhost:1080` instead of `your_server_ip:22`.
    *   `ssh client -> localhost:1080` (unencrypted SSH traffic locally)

3.  **Client-Side Injection:**
    *   The client-side injector software receives this SSH traffic on `localhost:1080`.
    *   It initiates a TCP connection to `your_server_ip:443`.
    *   It starts a TLS handshake with the server-side injector.
    *   **During the "Client Hello" part of the TLS handshake, it sends `SNI: allowed.example.com`.**
    *   The intermediate firewall/ISP sees a TLS handshake destined for `your_server_ip:443` that *claims* to be for `allowed.example.com`. If `allowed.example.com` is whitelisted, or if port 443 is generally open, the connection is often allowed.
    *   Once the TLS tunnel is established, the client-side injector encrypts your SSH traffic and sends it through this tunnel.
    *   `SSH_Client -> Local_Injector (localhost:1080) --[TLS with SNI 'allowed.example.com']--> your_server_ip:443`

4.  **Server-Side Unwrapping:**
    *   The server-side injector on `your_server_ip:443` receives the TLS connection.
    *   It completes the TLS handshake (it doesn't necessarily *care* what the SNI was, as long as it can provide *a* certificate to complete the handshake; its main job is to listen and decrypt).
    *   It decrypts the incoming TLS traffic, revealing the original SSH traffic.
    *   It forwards this decrypted SSH traffic to the actual SSH server running on `localhost:22` on the VPS.
    *   `Server_Injector (your_server_ip:443) --[Decrypted SSH]--> SSH_Server_Daemon (localhost:22 on VPS)`

5.  **Communication:**
    *   The SSH server processes the request and sends a response.
    *   This response travels back: `SSH_Server_Daemon -> Server_Injector (encrypts with TLS) -> Client_Injector (decrypts TLS) -> SSH_Client`.

**Simplified Diagram:**

```
Your PC                                     Restrictive Network (ISP/Firewall)       Your VPS
+-------------+       +-------------------+                                        +---------------------+       +-----------+
| SSH Client  | ----> | Client Injector   | --- (TLS with SNI='allowed.example.com') --> | Server Injector     | ----> | SSH       |
| (e.g. PuTTY)|       | (e.g. stunnel on  | --- (Traffic to your_server_ip:443) ---->  | (e.g. stunnel on   |       | Server    |
| connects to |       |  localhost:1080)  |                                        |  your_server_ip:443 |       | (sshd on  |
| localhost   |       +-------------------+                                        |  listens, decrypts, |       |  VPS@22)  |
+-------------+                                                                    |  forwards to local  |       +-----------+
                                                                                   |  sshd)              |
                                                                                   +---------------------+
                                            Firewall sees: HTTPS connection to
                                            your_server_ip:443 claiming to be
                                            for 'allowed.example.com'
```

## Conceptual Simulation (Step-by-Step)

**Scenario:**
*   **You (User):** Want to SSH to your VPS.
*   **Your PC:** Has an SSH client and a "client-side injector" app.
*   **ISP Firewall:** Blocks port 22. Allows port 443, especially if SNI looks like `popular-cdn.com`.
*   **Your VPS:** Has an SSH server (sshd) and a "server-side injector" proxy.
*   **SNI to use:** `popular-cdn.com`

**Steps:**

1.  **Server Setup (One-time):**
    *   On VPS, install `sshd` (usually default).
    *   Install `stunnel` (as server-side injector).
    *   Configure `stunnel` on VPS:
        *   `accept = 0.0.0.0:443` (listen on all interfaces, port 443)
        *   `connect = 127.0.0.1:22` (forward decrypted traffic to local sshd)
        *   `cert = /path/to/your/ssl_certificate.pem` (needs a cert to complete TLS)
        *   `key = /path/to/your/private_key.pem`
    *   Start `stunnel` service on VPS.

2.  **Client Setup (One-time):**
    *   On Your PC, install `stunnel` (as client-side injector).
    *   Configure `stunnel` on Your PC:
        *   `client = yes`
        *   `accept = 127.0.0.1:2222` (your local SSH client will connect here)
        *   `connect = YOUR_VPS_IP:443` (where the server-side stunnel listens)
        *   `sni = popular-cdn.com` (**THE CRITICAL INJECTION STEP**)
        *   (Optional: `checkHost` or `verifyChain` if you want to validate the server's actual cert, or disable if using self-signed and you know what you're doing).
    *   Start `stunnel` service on Your PC.

3.  **User Action (Connecting):**
    *   User opens terminal/PuTTY.
    *   User types: `ssh your_username@127.0.0.1 -p 2222`

4.  **Behind the Scenes - Client Side:**
    *   SSH client sends SSH protocol data to `127.0.0.1:2222`.
    *   Client-side `stunnel` receives this data.
    *   Client-side `stunnel` initiates a TCP connection to `YOUR_VPS_IP:443`.
    *   Client-side `stunnel` starts a TLS handshake. In the "ClientHello" message, it includes `Extension: server_name` with `server_name: popular-cdn.com`.

5.  **Behind the Scenes - ISP Firewall:**
    *   Firewall sees an outgoing connection from Your PC to `YOUR_VPS_IP:443`.
    *   It inspects the (unencrypted at this stage) TLS ClientHello.
    *   It sees `SNI: popular-cdn.com`.
    *   Since `popular-cdn.com` is whitelisted (or port 443 traffic is generally trusted), the firewall allows the connection to proceed.

6.  **Behind the Scenes - Server Side:**
    *   Server-side `stunnel` on VPS at `YOUR_VPS_IP:443` receives the TLS connection.
    *   It responds with its SSL certificate and completes the TLS handshake. It doesn't strictly *need* to care that the SNI was `popular-cdn.com` unless it's hosting multiple sites/certs on that IP and needs SNI to pick the right one. For this purpose, it just needs *a* cert to establish TLS.
    *   A secure TLS tunnel is now established between client `stunnel` and server `stunnel`.
    *   Server-side `stunnel` receives the encrypted SSH data from the client.
    *   It decrypts the data.
    *   It forwards the plain SSH data to `127.0.0.1:22` on the VPS.

7.  **Behind the Scenes - SSH Server on VPS:**
    *   `sshd` on the VPS (listening on `127.0.0.1:22`) receives the SSH connection as if it came directly.
    *   It performs SSH authentication (password, key-based, etc.).
    *   User gets an SSH prompt!

8.  **Return Traffic:**
    *   `sshd` sends data back.
    *   Server-side `stunnel` receives it from `sshd`, encrypts it with TLS, and sends it back over the tunnel to Your PC.
    *   Client-side `stunnel` receives the TLS data, decrypts it, and sends the plain SSH data to your SSH client on `127.0.0.1:2222`.
    *   User sees output in their terminal.

## Important Considerations

*   **Legality and Ethics:** Bypassing network restrictions can violate terms of service or local laws. Use responsibly.
*   **Performance:** There's an overhead due to double encapsulation (SSH within TLS) and the encryption/decryption processes at both ends.
*   **Complexity:** Setting it up requires some technical know-how on both client and server.
*   **Detection:** While it hides the SSH *protocol*, sophisticated deep packet inspection (DPI) might still detect anomalies in traffic patterns if the "allowed" SNI domain behaves very differently from the tunneled traffic. However, for most common firewalls, SNI-based rules are simpler and this technique is effective.
*   **Server-Side Certificate:** The server needs a valid SSL certificate for the TLS part. This can be a self-signed one (client must be configured to accept it) or one from a CA like Let's Encrypt.

