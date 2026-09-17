---
tags: [concept, database, oracle, editions]
type: concept
status: complete
related:
  - [[12 - Advanced Database Features/00 - MOC - Advanced DB]]
---

# Oracle XE vs Standard vs Enterprise

## Oracle Database editions

| Edition | License | Limits | Use case |
|---|---|---|---|
| **XE** (Express Edition) | Free | 2 CPU threads, 2 GB RAM, 12 GB user data | Dev, small apps |
| **Standard Edition 2** | Paid | 4 sockets, unlimited RAM/data | Small-medium business |
| **Enterprise Edition** | Paid (expensive) | Unlimited | Large enterprise |

## XE limitations

- **2 CPU threads** — even on a 16-core server, XE uses 2.
- **2 GB RAM** — limited SGA/PGA.
- **12 GB user data** — total user data across all schemas.
- **No parallel query** — single-threaded execution.
- **No partitioning** — tables can't be partitioned.
- **No advanced compression** — only basic compression.
- **No TDE** (Transparent Data Encryption).
- **No Active Data Guard** (read replicas).
- **No RAC** (Real Application Clusters).
- **No VPD** (Virtual Private Database) — wait, this is debated. Some sources say XE has VPD, others not. Check your version.

## What this means for the project

The project uses Oracle XE. The advanced schema redesign (with partitioning, VPD, redaction, materialized views) requires **Enterprise Edition** features. On XE:
- Partitioning won't work.
- `ROW STORE COMPRESS ADVANCED` won't work (only basic compression).
- VPD might work (check version).
- DBMS_REDACT might work (check version).

For a portfolio project, develop on XE but document the Enterprise Edition features. Or use `gvenzl/oracle-xe:21-slim` in Docker for free, and mention that production would use Enterprise.

## Alternatives

- **PostgreSQL** — free, open source, supports partitioning, MVCC, full-text search, JSON. Often a better choice than Oracle XE for new projects.
- **MySQL** — free, popular, simpler than PostgreSQL.
- **MariaDB** — MySQL fork.
- **SQLite** — embedded, no server. For dev/testing.

## Project Connection

The project targets Oracle XE. The reviews recommend upgrading to `ojdbc11 23.x` (Oracle 23c driver) but the database can stay on XE 21 for development. For production-like testing, use `gvenzl/oracle-xe:21-slim` in Docker.

If the project were to be re-architected for a different database, PostgreSQL would be a strong choice — free, full-featured, well-supported by Spring Boot.

## Further reading

- Oracle Database Licensing Information.
- `gvenzl/oracle-xe` Docker image documentation.
