---
tags: [concept, build, security, owasp, cve]
type: concept
status: complete
related:
  - [[17 - Application Security/04 - Dependency Vulnerabilities (CVEs)]]
---

# OWASP Dependency-Check

## What it is

A Maven plugin that scans dependencies against the NVD (National Vulnerability Database) and fails the build if CVEs are found.

## Configuration

```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>8.4.0</version>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
        <suppressionFile>owasp-suppressions.xml</suppressionFile>
    </configuration>
    <executions>
        <execution>
            <goals><goal>check</goal></goals>
        </execution>
    </executions>
</plugin>
```

`mvn verify` runs the check. Fails if any dependency has CVSS ≥ 7.

## Suppressing false positives

```xml
<!-- owasp-suppressions.xml -->
<suppressions>
    <suppress>
        <packageUrl>pkg:maven/com.oracle.database.jdbc/ojdbc8@19.8.0.0</packageUrl>
        <cve>CVE-2022-21369</cve>
        <cve>CVE-2020-14701</cve>
    </suppress>
</suppressions>
```

Only suppress after verifying the CVE doesn't apply.

## The project's vulnerable dependencies

| Dependency | Version | CVE |
|---|---|---|
| `ojdbc8` | 19.8.0.0 | CVE-2022-21369 |
| `pdfbox` | 2.0.24 | CVE-2022-23711 |
| `javax.mail` | 1.6.2 | (deprecated, no patches) |

`mvn dependency-check:check` would flag all three. The fix: upgrade (`ojdbc11 23.5`, `pdfbox 3.0`, `jakarta.mail 2.1`).

## Further reading

- OWASP Dependency-Check documentation.
- NVD (nvd.nist.gov).
