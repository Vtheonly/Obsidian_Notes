# Backend Engineering Knowledge Vault

A comprehensive, structured reference covering backend engineering fundamentals -- from networking concepts and system design to Docker, Linux, database design, and PHP development.

---

## Vault Structure

### 01 - Networking Concepts

Foundational networking knowledge that underpins all backend development. Covers protocols, addressing, security, and communication patterns.

| File | Topic |
|------|-------|
| [[HTTP and HTTPS]] | HTTP methods, status codes, headers, HTTPS/TLS, HTTP evolution |
| [[SSL and TLS]] | TLS handshake, encryption, certificates, SNI, vulnerabilities |
| [[DNS and Domain Resolution]] | DNS hierarchy, record types, resolution process, caching |
| [[IP Addressing]] | IPv4/IPv6, address classes, subnet masks, CIDR notation |
| [[Private IP vs Public IP]] | RFC 1918 ranges, NAT, security implications, APIPA |
| [[SNI Injector Explained]] | SSH tunneling over TLS with SNI manipulation |
| [[WebSockets]] | Full-duplex communication, handshake, authentication, reconnection |
| [[XHR]] | XMLHttpRequest API, AJAX, progress tracking, comparison with fetch() |

---

### 02 - System Design

Principles and patterns for designing scalable, reliable systems. Covers the client-server model, network protocols, concurrency models, and scalability strategies.

| File | Topic |
|------|-------|
| [[Chapter 1 - Introduction to Design Fundamentals]] | Coding vs systems design, trade-offs, design fundamentals |
| [[Chapter 2 - Categories of Design Fundamentals]] | Foundational knowledge, key characteristics, system components, tools |
| [[Chapter 3 - The Client-Server Model]] | Client-server architecture, DNS resolution, ports, netcat demo |
| [[Chapter 4 - Network Protocols]] | IP, TCP, HTTP deep dive with Node.js and curl examples |
| [[Asynchronous and Multi-Threaded Programming]] | Event loop vs threads, I/O-bound vs CPU-bound, concurrency models |
| [[Scalability]] | Database sharding, load balancing, CDNs, microservices, fault tolerance |

**Quizzes:**

| File | Topic |
|------|-------|
| [[Quiz 1 - Async and Multi-Threaded]] | Asynchronous and multi-threaded programming concepts |
| [[Quiz 2 - IP Addressing]] | IP addressing fundamentals |
| [[Quiz 3 - IP Addressing Advanced]] | Advanced IP addressing questions |
| [[Quiz 4 - Private vs Public IP]] | Private vs public IP address concepts |

---

### 03 - Docker

Containerization with Docker -- from installation to multi-container orchestration. A progressive learning path from fundamentals to production use.

| File | Topic |
|------|-------|
| [[1. What is Docker]] | Containers, VMs, the "Works on My Machine" problem |
| [[2. Installing Docker]] | Mac/Windows/WSL2 installation, architecture |
| [[3. Images and Containers]] | Read-only images, writable container layer, lifecycle |
| [[3.1 Data Persistence (Volumes)]] | Named volumes, bind mounts, anonymous volumes |
| [[4. Parent Images and Docker Hub]] | Docker Hub, image layers, tags, Alpine variants |
| [[4.1 Advanced Layers and Image Efficiency]] | Layer caching, optimization, image size reduction |
| [[5. The Dockerfile]] | FROM, WORKDIR, COPY, RUN, EXPOSE, CMD, best practices |
| [[6. The .dockerignore File]] | Excluding files, security, reducing build context |
| [[7. Starting and Stopping Containers]] | Container lifecycle, flags, management commands |
| [[7.1 Advanced Interacting with Containers (Exec)]] | docker exec, STDIN/STDOUT/STDERR, streams |
| [[8. Docker Compose]] | Multi-container YAML, services, networking, volumes |

**Q&A and Quizzes:**

| File | Topic |
|------|-------|
| [[Qs1]] | Dockerfile and Layers Q&A |
| [[Qs2]] | Volumes and File Access Q&A |
| [[Docker Quiz 1]] | Fundamentals quiz (lessons 1-3) |
| [[Docker Quiz 2]] | Advanced quiz (lessons 3.1-8) |

---

### 04 - Linux

Linux system administration essentials -- package management, file handling, and command-line tools.

**Installing in Linux:**

| File | Topic |
|------|-------|
| [[0 - How to Install Apps in Linux]] | Overview of installation methods |
| [[1 - App Center]] | App Center vs open source downloads |
| [[2 - Location of Compilers]] | Where compilers live, finding them with which/whereis |
| [[3 - Location of Apps Installed from Terminal]] | /bin, /usr/bin, /usr/local/bin, PATH variable |
| [[4 - Understanding .deb Files]] | .deb structure, installation, dpkg |
| [[5 - Understanding .tar.gz Files]] | Archives vs installers, extraction, compilation |
| [[6 - Understanding APT]] | APT commands, repositories, package management |

**Tools and Commands:**

| File | Topic |
|------|-------|
| [[0 - dpkg]] | Package management: install, remove, query, troubleshoot |
| [[1 - tail]] | File tailing, follow mode, log monitoring |
| [[2 - .desktop Files]] | Application menu entries, desktop integration |
| [[3 - tar -xvf]] | Archive extraction flags, compression formats |
| [[4 - zip and rar]] | Compression, encryption, archive management |
| [[5 - grep]] | Pattern matching, regex, practical search examples |

---

### 05 - Database Design

A complete course on relational database design, from foundational concepts through normalization to SQL joins. Progressively numbered for sequential learning.

**Foundations (0-9):**

| File | Topic |
|------|-------|
| [[0 - Introduction]] | Course overview and what to expect |
| [[1 - What is a Database]] | Data, databases, database vs spreadsheet |
| [[2 - What is a Relational Database]] | Relations, entities, attributes, tables |
| [[3 - RDBMS]] | DBMS vs RDBMS, queries, views, transactions |
| [[4 - Introduction to SQL]] | DDL vs DML, SQL keywords, practical examples |
| [[5 - Naming Conventions]] | Lowercase, underscores, foreign key naming |
| [[6 - What is Database Design]] | Conceptual/logical/physical schemas, anomalies |
| [[7 - Data Integrity]] | Entity, referential, domain integrity |
| [[8 - Database Terms]] | Glossary: data, database, RDBMS, null, anomalies |
| [[9 - More Database Terms]] | Glossary: SQL, DDL, DML, client/server, view, join |

**Atomic Values and Relationships (10-19):**

| File | Topic |
|------|-------|
| [[10 - Atomic Values]] | Single-valued attributes, decomposition |
| [[11 - Relationships]] | Entity relationships overview, three types |
| [[12 - One-to-One Relationships]] | 1:1 concept, when to use separate tables |
| [[13 - One-to-Many Relationships]] | 1:many concept, foreign key placement |
| [[14 - Many-to-Many Relationships]] | many:many concept, junction tables |
| [[15 - Designing One-to-One Relationships]] | Shared primary key, unique foreign key |
| [[16 - Designing One-to-Many Relationships]] | Foreign key on the "many" side |
| [[17 - Parent Tables and Child Tables]] | Parent/child, weak entities, identifying relationships |
| [[18 - Designing Many-to-Many Relationships]] | Junction tables, composite primary keys |
| [[19 - Summary of Relationships]] | Comparison and quick reference |

**Keys (20-31):**

| File | Topic |
|------|-------|
| [[20 - Introduction to Keys]] | Superkeys, candidate keys, primary keys |
| [[21 - Primary Key Index]] | B-tree indexes for fast primary key lookups |
| [[22 - Lookup Table]] | Reference tables, normalization benefits |
| [[23 - Superkey and Candidate Key]] | Finding superkeys and candidate keys |
| [[24 - Primary Key and Alternate Key]] | Selecting primary keys, alternate keys |
| [[25 - Surrogate Key and Natural Key]] | Artificial vs existing-data keys |
| [[26 - Surrogate vs Natural Keys Decision Guide]] | When to use which, design framework |
| [[27 - Foreign Key]] | Referencing other tables, SQL examples |
| [[28 - NOT NULL Foreign Key]] | Mandatory vs optional relationships |
| [[29 - Foreign Key Constraints]] | ON UPDATE/ON DELETE: RESTRICT, CASCADE, SET NULL |
| [[30 - Simple Key Composite Key Compound Key]] | Single vs multi-column keys |
| [[31 - Review and Key Points]] | Summary of all key types |

**ER Modeling and Normalization (32-39):**

| File | Topic |
|------|-------|
| [[32 - Introduction to Entity Relationship Modeling]] | ER diagrams, Chen notation |
| [[33 - Cardinality]] | Min/max notation in ER diagrams |
| [[34 - Modality]] | Mandatory vs optional participation |
| [[35 - Introduction to Database Normalization]] | Why normalize, normal forms overview |
| [[36 - 1NF First Normal Form]] | Atomic values, no repeating groups |
| [[37 - 2NF Second Normal Form]] | Removing partial dependencies |
| [[38 - 3NF Third Normal Form]] | Removing transitive dependencies |
| [[39 - Indexes]] | Clustered, nonclustered, composite indexes |

**Data Types and Joins (40-50):**

| File | Topic |
|------|-------|
| [[40 - Data Types]] | Numeric, string, date/time, boolean types |
| [[41 - Introduction to Joins]] | Why joins exist, join types overview |
| [[42 - Inner Join]] | INNER JOIN syntax, matching rows |
| [[43 - Inner Join on 3 Tables]] | Chaining joins across multiple tables |
| [[44 - Inner Join on 3 Tables Example]] | Practical walkthrough with sample data |
| [[45 - Introduction to Outer Joins]] | LEFT, RIGHT, FULL outer joins |
| [[46 - Right Outer Join]] | RIGHT JOIN details and examples |
| [[47 - JOIN with NOT NULL Columns]] | NOT NULL behavior in inner vs outer joins |
| [[48 - Outer Join Across 3 Tables]] | Chaining outer joins across multiple tables |
| [[49 - Alias]] | Column and table aliases in SQL |
| [[50 - Self Join]] | Joining a table to itself, hierarchical data |

---

### 06 - PHP MySQL

PHP development fundamentals with MySQL -- from execution models and server setup through core language constructs.

**Level 1 -- PHP Basics:**

| File | Topic |
|------|-------|
| [[0. Execution Models of PHP]] | Share-Nothing vs Long-Running models |
| [[0.1 Apache Server]] | Apache as web server, installation, serving PHP |
| [[0.2 PHP server]] | Built-in development server, why NOT for production |
| [[0.3 MariaDB VS MySQL]] | History, licensing, performance, storage engines |
| [[0.4 PHP Architectures]] | Spaghetti code to MVC/API to Front Controller |
| [[1. echo]] | Output, single vs double quotes, variable interpolation |
| [[1.1 echo vs. print vs. print_r]] | Comparison of output methods |
| [[2. Mixing PHP and HTML]] | Variables and echo in HTML templates |
| [[3. Errors]] | Parse, Fatal, Warning, Notice; php.ini configuration |
| [[4. define]] | Constants vs variables, define() vs const, magic constants |
| [[5. Index]] | Zero-based string indexing, immutability |
| [[6. Indexed Array]] | Creating, accessing, modifying arrays |
| [[6.1 Associative Arrays]] | Key-value pairs, CRUD, foreach |
| [[6.2 Multi-Dimensional Arrays]] | Nested arrays, stack/queue operations |
| [[6.3 htmlspecialchars]] | XSS prevention, output escaping |
| [[7. strings and numbers]] | String functions and math operations |
| [[8. Loops]] | for, foreach, while with HTML generation |
| [[9. Boolean and Comparison]] | Loose vs strict comparison, type juggling |
| [[10. Conditions]] | if/elseif/else, logical operators, alternative syntax |
| [[11. break and continue]] | Loop control, switch fall-through |

**Level 2 -- PHP Intermediate:**

| File | Topic |
|------|-------|
| [[1. Functions]] | Parameters, return values, type hints, anonymous/arrow functions |
| [[2. Variable scope]] | Global vs local, `global` keyword, $GLOBALS |
| [[3. Include and Require]] | include vs require, _once variants, page structure |

**Production Mode Practices:**

| File | Topic |
|------|-------|
| [[0. Docker vs Apache]] | Traditional vs Docker deployment comparison |
