# DNS and Domain Resolution

## What is DNS

DNS (Domain Name System) is often described as the phonebook of the internet. It is a hierarchical, decentralized naming system that translates human-readable domain names (such as `www.example.com`) into machine-readable IP addresses (such as `93.184.216.34`). Without DNS, users would need to memorize numerical IP addresses to access every website, email server, and online service. The DNS system is one of the most critical pieces of internet infrastructure, and virtually every network operation begins with a DNS lookup.

When you type a URL into your browser, the first step is to resolve the domain name to an IP address. The browser checks its own cache, then the operating system's cache, and finally queries a DNS resolver to find the answer. The entire process typically completes in milliseconds, but behind the simple act of typing a URL lies a complex system of distributed servers, caching mechanisms, and protocols that work together to provide fast and reliable name resolution for billions of devices worldwide.

DNS was originally designed in the early 1980s as a replacement for the HOSTS.TXT file system, which required manual updates and distribution. Paul Mockapetris designed the original DNS specifications (RFC 882 and RFC 883, later superseded by RFC 1034 and RFC 1035), creating a system that could scale to accommodate the rapidly growing internet. The fundamental design has proven remarkably resilient, though numerous extensions and enhancements have been added over the decades to address security (DNSSEC), privacy (DNS over HTTPS, DNS over TLS), and performance (EDNS0) concerns.

---

## DNS Resolution Process

DNS resolution is the process of converting a domain name into an IP address. This process involves two types of queries: recursive queries and iterative queries. Understanding the difference between them is essential for understanding how the DNS system operates as a whole.

### Recursive Queries

In a recursive query, the client (typically the operating system's DNS resolver stub) asks a recursive DNS resolver to find the answer, and the resolver is responsible for either returning the final answer or returning an error. The recursive resolver handles all the intermediate steps needed to reach the answer, chasing down referrals from the root servers to the TLD servers to the authoritative servers. The client does not need to know anything about the DNS hierarchy; it simply sends its query to the recursive resolver and waits for the result. Most home and corporate networks configure their devices to use a recursive resolver provided by the ISP, a public resolver like Google DNS (8.8.8.8) or Cloudflare DNS (1.1.1.1), or an internal resolver on the corporate network.

### Iterative Queries

When the recursive resolver receives a query that it cannot answer from its cache, it performs a series of iterative queries to resolve the name. It starts by querying one of the root servers, which responds with a referral to the appropriate TLD server. The resolver then queries the TLD server, which responds with a referral to the authoritative server for the domain. Finally, the resolver queries the authoritative server, which provides the actual answer (the IP address or other DNS record). At each step, the resolver follows the referral to the next server in the chain, building up the complete answer through a sequence of iterative lookups.

### Step-by-Step Example

Consider resolving `www.example.com`. The recursive resolver first queries a root server for `www.example.com`. The root server does not know the IP address, but it knows which servers are authoritative for the `.com` TLD, so it returns a referral to the `.com` TLD servers. The resolver then queries a `.com` TLD server for `www.example.com`. The TLD server does not know the specific IP address either, but it knows which servers are authoritative for `example.com`, so it returns a referral to those servers. The resolver then queries the `example.com` authoritative server, which returns the IP address for `www.example.com`. The resolver caches this result (according to the TTL) and returns it to the client.

---

## DNS Record Types

DNS is not limited to mapping domain names to IP addresses. It supports a variety of record types, each serving a specific purpose in the DNS ecosystem.

### A Record (Address Record)

The A record maps a domain name to an IPv4 address. It is the most fundamental DNS record type and is what most people think of when they talk about DNS resolution. For example, the A record for `www.example.com` might point to `93.184.216.34`. Every domain that needs to be accessible over IPv4 must have at least one A record.

### AAAA Record (IPv6 Address Record)

The AAAA record (pronounced "quad-A") maps a domain name to an IPv6 address. As IPv6 adoption grows, AAAA records are becoming increasingly important. For example, the AAAA record for `www.example.com` might point to `2606:2800:220:1:248:1893:25c8:1946`. Domains that support both IPv4 and IPv6 will have both A and AAAA records.

### CNAME Record (Canonical Name Record)

The CNAME record creates an alias from one domain name to another. It is commonly used to point subdomains to another domain name that already has an A record. For example, `blog.example.com` might be a CNAME pointing to `example.wordpress.com`, which in turn has an A record pointing to WordPress's IP address. CNAME records cannot coexist with other record types on the same name; a name that has a CNAME record cannot also have an A record, MX record, or any other type.

### MX Record (Mail Exchange Record)

The MX record specifies the mail server responsible for accepting email for a domain. Each MX record has a priority value; lower numbers indicate higher priority. When sending email to `user@example.com`, the sending mail server looks up the MX records for `example.com` and attempts to deliver the mail to the server with the lowest priority value first, falling back to higher-priority servers if the primary is unavailable.

### NS Record (Name Server Record)

The NS record specifies the authoritative name servers for a DNS zone. When a recursive resolver queries a TLD server for a domain, the TLD server responds with the NS records for that domain, telling the resolver which servers hold the authoritative answers for the domain's records. Every DNS zone must have at least two NS records for redundancy.

### TXT Record (Text Record)

The TXT record allows domain administrators to associate arbitrary text with a domain name. Originally intended for human-readable notes, TXT records are now widely used for machine-readable data. Common uses include SPF (Sender Policy Framework) records for email authentication, DKIM (DomainKeys Identified Mail) public keys, domain verification tokens for services like Google Search Console, and DNS-based challenges for ACME certificate issuance (Let's Encrypt).

### SOA Record (Start of Authority Record)

The SOA record marks the beginning of a DNS zone and contains administrative information about the zone, including the primary name server, the email address of the responsible person (with the `@` replaced by a dot), the serial number of the zone (used for synchronization between primary and secondary servers), the refresh interval, the retry interval, the expire time, and the default TTL. Every DNS zone must have exactly one SOA record.

### PTR Record (Pointer Record)

The PTR record is used for reverse DNS lookups, mapping an IP address back to a domain name. Reverse DNS is important for email servers (many mail servers reject messages from IPs without valid PTR records) and for network diagnostics. PTR records are stored in the special `in-addr.arpa` domain for IPv4 and `ip6.arpa` for IPv6.

---

## DNS Hierarchy

The DNS namespace is organized as an inverted tree, with the root at the top and subdomains branching out below. This hierarchical structure is what allows DNS to scale to billions of records across millions of domains.

### Root Servers

At the top of the DNS hierarchy are the root servers, which are responsible for answering queries for the root zone (the top of the DNS tree). There are 13 logical root server addresses, labeled A through M, though each address is served by a cluster of physical servers distributed around the world using anycast routing. The root servers do not know the IP addresses of individual domains; instead, they know the authoritative servers for each top-level domain (TLD). When a recursive resolver queries a root server, the root server responds with a referral to the appropriate TLD server.

### TLD Servers

Below the root servers are the TLD (Top-Level Domain) servers, which are authoritative for a specific top-level domain such as `.com`, `.org`, `.net`, or a country-code TLD like `.uk` or `.jp`. The TLD servers know the authoritative name servers for each domain registered under their TLD. When a recursive resolver queries a `.com` TLD server for `example.com`, the TLD server responds with the NS records for `example.com`, pointing to that domain's authoritative servers.

### Authoritative Servers

Authoritative name servers are the final authority on the DNS records for a specific domain. They hold the actual zone file containing all the DNS records (A, AAAA, MX, CNAME, TXT, etc.) for the domain. When a recursive resolver queries an authoritative server, it receives the definitive answer for the queried record. Authoritative servers can be operated by the domain owner, a DNS hosting provider, or a CDN service.

### Recursive Resolvers

Recursive resolvers (also called caching resolvers or resolving name servers) are the workhorses of the DNS system. They sit between the client and the rest of the DNS hierarchy, handling the full resolution process on behalf of the client. When a recursive resolver receives a query, it checks its cache first. If the answer is not in the cache or has expired, it performs the iterative query process described above, starting at the root and following referrals until it reaches the authoritative server. The resolver then caches the result according to its TTL and returns the answer to the client. Major public recursive resolvers include Google DNS (8.8.8.8, 8.8.4.4), Cloudflare DNS (1.1.1.1, 1.0.0.1), and Quad9 (9.9.9.9).

---

## DNS Caching

DNS caching is essential for the performance and reliability of the DNS system. Without caching, every DNS lookup would require a full recursive resolution, creating enormous load on the root and TLD servers and adding significant latency to every network request.

### Browser Cache

Modern web browsers maintain their own DNS cache to avoid even the overhead of querying the operating system's resolver. When a browser needs to resolve a domain name, it first checks its internal cache. If the entry is present and has not expired, the browser uses the cached IP address immediately. Browser DNS caches typically have shorter TTLs than the records specify, often capping the cache duration at a few minutes.

### Operating System Cache

The operating system's DNS resolver stub also maintains a cache. Before querying a recursive resolver, the OS checks its cache. On Linux, the `systemd-resolved` service (or `nscd` on older systems) handles DNS caching. On Windows, the DNS Client service manages the cache, and the `ipconfig /displaydns` command shows cached entries. On macOS, the `mDNSResponder` process handles DNS caching.

### Resolver Cache

Recursive resolvers maintain large caches that serve many clients simultaneously. Because a popular resolver like Google DNS or Cloudflare DNS handles billions of queries per day, its cache is likely to already contain answers for most common domain names, making resolution nearly instantaneous for the majority of queries. The cache entries are stored according to the TTL values specified in the DNS records, with popular records frequently being re-cached before they expire.

---

## DNS Propagation and TTL

DNS propagation refers to the time it takes for changes to DNS records to become visible across the entire DNS system. Because DNS relies heavily on caching, a change made to a zone file on an authoritative server will not be immediately reflected everywhere. Instead, resolvers and clients that have cached the old record will continue to use it until the cached entry expires based on its TTL (Time to Live).

TTL is a value specified in seconds on each DNS record that tells caching resolvers how long they are allowed to cache the record before they must query the authoritative server again. A TTL of 3600 means the record can be cached for one hour. Shorter TTLs mean faster propagation but more frequent queries to the authoritative server, while longer TTLs mean slower propagation but reduced load and lower latency for cached lookups.

When planning a DNS change (such as migrating a website to a new IP address), best practice is to lower the TTL to a short value (such as 300 seconds) at least 24-48 hours before the change, wait for the old TTL to expire across the network, make the change, and then raise the TTL back to a normal value. This minimizes the window during which some resolvers may return the old IP address while others return the new one.

---

## Common DNS Tools

### dig (Domain Information Groper)

`dig` is the most powerful and flexible DNS lookup tool available on Linux and macOS. It queries DNS servers and returns detailed information about the response, including the query time, the server that responded, the full set of records returned, and the TTL of each record. Common usage includes `dig example.com` (basic A record lookup), `dig example.com MX` (MX record lookup), `dig @8.8.8.8 example.com` (query a specific resolver), and `dig example.com +trace` (trace the full resolution path from root to authoritative server).

### nslookup

`nslookup` is a simpler DNS lookup tool available on Windows, Linux, and macOS. It provides basic name resolution functionality and is commonly used for quick lookups. Usage includes `nslookup example.com` and `nslookup example.com 8.8.8.8` (specifying a resolver). While `nslookup` is considered deprecated on some Linux distributions in favor of `dig`, it remains widely used, especially on Windows.

### host

The `host` command is a simple DNS lookup utility on Linux and macOS that provides concise output. It is useful for quick lookups when you do not need the detailed output of `dig`. Usage includes `host example.com` (A record lookup), `host -t MX example.com` (MX record lookup), and `host -t NS example.com` (NS record lookup).

---

## Relationship to Other Concepts

[[HTTP and HTTPS]] depends on DNS to function. Before a browser can establish an HTTP or HTTPS connection to a web server, it must resolve the domain name in the URL to an IP address using DNS. The entire web browsing experience begins with DNS resolution, and slow or failed DNS lookups directly impact the user's ability to access websites.

[[IP Addressing]] is the counterpart to DNS. While DNS provides the human-friendly naming layer, IP addressing provides the numerical addressing layer that network equipment uses to route traffic. DNS records (A and AAAA) map domain names to IP addresses, bridging the gap between the two systems.

---

## Key Takeaways

DNS is the foundational naming system of the internet, translating domain names to IP addresses through a hierarchical system of root servers, TLD servers, and authoritative servers. Recursive resolvers handle the full resolution process on behalf of clients, with extensive caching at every level to ensure performance and reliability. Understanding DNS record types, the resolution process, and caching behavior is essential for web developers, system administrators, and network engineers alike.
