---
title: Advanced Networks & Communication Protocols — Obsidian Vault
version: 2.0
type: master-index
tags: [moc, networking, index]
---

# Advanced Networks & Communication Protocols

> [!info] Vault Overview
> A polished, modern, and comprehensive Obsidian vault covering computer networks from physical signaling up through application-layer protocols. This vault merges two source documents — a master syllabus roadmap and a fragmented study vault — into a single coherent knowledge base, with every topic rewritten, expanded, and cross-linked.

## What's Inside

This vault is organized into **15 thematic chapters**, plus consolidated quizzes, a Cisco IOS reference, a dedicated memory-aids chapter, and reusable templates. Every chapter opens with a `00 - Chapter Overview` note that lists its topics with `[[wikilinks]]`, so you can navigate via Obsidian's graph view or the embedded topic index.

| # | Chapter | Scope |
| :-: | :--- | :--- |
| 01 | [[01 - Network Fundamentals]] | Definitions, devices, media, topologies, connection modes, application architectures |
| 02 | [[02 - Reference Models (OSI & TCP-IP)]] | OSI 7-layer model, TCP/IP DoD model, encapsulation, PDUs |
| 03 | [[03 - Physical & Data Link Layer]] | LLC/MAC, MAC addressing, Ethernet II frames, hubs vs switches, STP, CAM vs ARP |
| 04 | [[04 - IPv4 Network Layer]] | Classful addressing, RFC 1918, FLSM, VLSM, CIDR, summarization, gateway design |
| 05 | [[05 - IP Datagram & Fragmentation]] | IPv4 header, fragmentation math, MTU, PMTUD, practical walkthroughs |
| 06 | [[06 - ARP & Address Resolution]] | ARP lifecycle, packet format, gratuitous ARP, ARP probe, NDP for IPv6 |
| 07 | [[07 - IP Routing]] | Routing tables, AD, LPM, static routing, router packet processing |
| 08 | [[08 - Routing Protocols]] | RIP, OSPF, BGP, Dijkstra walkthrough, loop prevention, areas, cost metrics |
| 09 | [[09 - NAT & Perimeter Security]] | Static/Dynamic/PAT, port forwarding, DMZ, proxies, VPN |
| 10 | [[10 - Transport Layer]] | Ports, sockets, UDP, TCP, handshake, sliding window, congestion control |
| 11 | [[11 - Application Layer]] | DNS, HTTP/HTTPS, TLS, SNI, WebSockets, XHR, SMTP/POP3/IMAP, FTP |
| 12 | [[12 - Tunnels & Remote Access]] | Tunneling fundamentals, Ngrok, Cloudflare Tunnels, comparison |
| 13 | [[13 - Cisco IOS CLI]] | EXEC modes, configuration, diagnostics, RIP/OSPF config snippets |
| 14 | [[14 - Memory Aids & Mnemonics]] | Consolidated mnemonics for subnetting, fragmentation, routing |
| — | [[Quizzes]] | Self-test decks for chapters 5–8 with answers in collapsible callouts |

## Navigation

- **Start here:** [[00 - Master Index/MOC - Map of Content| Map of Content]]
- **Linear path:** [[00 - Master Index/Learning Path| Recommended Learning Path]]
- **Quick reference:** [[00 - Master Index/Quick Reference Cheatsheet| Cheatsheet]]

## Conventions

- **Wikilinks** (`[[Note Name]]`) — used everywhere for cross-references; they will work the moment you open this folder as an Obsidian vault.
- **Callouts** (`> [!info]`, `> [!warning]`, `> [!example]`, `> [!success]`) — used to highlight definitions, pitfalls, worked examples, and quiz answers.
- **Mermaid diagrams** — embedded throughout for topology, sequence, and flow visualizations. Obsidian renders these natively.
- **LaTeX math** (`$$…$$`) — used for formulas (subnet math, fragmentation offsets, OSPF cost). Obsidian renders these via MathJax.
- **Frontmatter** — every note begins with a YAML block for tagging and metadata.

## How to Use This Vault

1. **Open the folder in Obsidian** — *File → Open vault → Open folder as vault*, then select the `Networking-Vault` folder.
2. **Bookmark the MOC** — open [[00 - Master Index/MOC - Map of Content]] and pin it; it's your home base.
3. **Follow the learning path** — the [[00 - Master Index/Learning Path|learning path]] suggests a study order for a 6-week sprint.
4. **Practice with quizzes** — every chapter from 5 onward has a paired quiz file under `Quizzes/`.
5. **Use graph view** — `Ctrl+G` (or click the icon) to see how topics interconnect; the chapter overviews act as local hubs.

## Source Material

This vault was produced by refactoring and merging two source documents:

1. **Master Syllabus Roadmap** — a 9-chapter academic syllabus covering advanced networks and communication protocols.
2. **Existing Obsidian Vault** — a 68-file study vault with chapter notes, quizzes, and isolated application-layer notes.

Both sources were treated as raw material. Content was deduplicated, reorganized into a more progressive structure, rewritten for clarity, and expanded with worked examples, mermaid diagrams, and cross-references. Memory-aids originally scattered across chapter 02 and chapter 03 of the old vault were consolidated into [[14 - Memory Aids & Mnemonics]].
