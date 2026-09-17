---
tags: [home, index]
---

# Unified Backend Engineering Vault

This is an Obsidian vault that teaches backend engineering as a single unified discipline. It is organized by **concept**, not by framework. Every concept is taught once at the conceptual level, then implemented deeply in the Spring Boot anchor stack, then rapidly translated into Express, Django, Flask, and Laravel as deltas. Ecosystem-specific concepts are taught in full — **unification without omission**.

## Start Here

1. Read [[00.01. Master Architectural Mental Model]] to install the global mental model.
2. Read [[00.02. The Anchor and Delta Learning Protocol]] to understand how to study this vault without burning out.
3. Read [[00.03. Unified Backend Engineering Terminology Dictionary]] and [[00.04. Cross Ecosystem Equivalence Graph]].
4. Open [[00.00. Map of Content - Systems Overview]] to begin working through the sections.

## The 14 Sections

- [[00.00. Map of Content - Systems Overview]] — 00. Systems Overview and Meta Index
- [[01.00. Map of Content - Toolchains and Bootstrapping]] — 01. Toolchains Runtimes and Zero-to-One Bootstrapping
- [[02.00. Map of Content - Operating Systems]] — 02. Operating Systems and POSIX Kernel Foundations
- [[03.00. Map of Content - Networking]] — 03. Networking and Application Transport Protocols
- [[04.00. Map of Content - Runtime Concurrency]] — 04. Runtime Concurrency and Execution Models
- [[05.00. Map of Content - Core Framework Abstractions]] — 05. Core Framework Abstractions and Web Architecture
- [[06.00. Map of Content - Data Persistence]] — 06. Data Persistence Storage Engines and Data Access
- [[07.00. Map of Content - Messaging and Streaming]] — 07. Asynchronous Messaging and Event Streaming
- [[08.00. Map of Content - Distributed Systems]] — 08. Distributed Systems Architecture and Big Data Compute
- [[09.00. Map of Content - Software Architecture]] — 09. Software Architecture and Design Patterns
- [[10.00. Map of Content - Infrastructure and Networking]] — 10. Infrastructure Containers and Ingress Networking
- [[11.00. Map of Content - Observability and Ops]] — 11. Observability Telemetry and Operations
- [[12.00. Map of Content - Serverless and BaaS]] — 12. Serverless Edge Computing and BaaS
- [[13.00. Map of Content - Practical Projects]] — 13. Practical Transfer Projects and Capstones

## The Anchor and Delta Protocol

Pick **one** ecosystem (Spring Boot + PostgreSQL is the default) and build deep, production-grade scars in it. Master routing, ORM execution plans, thread pools, socket exhaustion, race conditions, memory profiling, and deployment **in that one stack**. Then — and only then — open the other ecosystems and implement the **same** feature as a translation exercise. Ask: what is automatic here that I had to do manually in the anchor, and what is manual here that was automatic there? Document the delta. Move on.

Do **not** rotate frameworks every time you learn a new concept. That path leads to context thrashing and shallow understanding.

## What This Vault Is Not

- It is **not** a tutorial. Notes assume you will read source code, run load tests, and break things.
- It is **not** a simplified common denominator. Every ecosystem's specific concepts are taught in full.
- It is **not** a reference manual. The goal is to build a mental model, not to document every API.

## How to Open This Vault

1. Install [Obsidian](https://obsidian.md/).
2. Open this folder as a vault (File → Open vault → Open folder as vault).
3. Open `HOME.md` as your landing page.
4. Enable Backlinks and Graph View for the full experience.

