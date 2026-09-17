---
tags: [concept, security, dependencies, cve]
type: concept
status: complete
related:
  - [[24 - Build and Tooling/05 - OWASP Dependency-Check]]
---

# Dependency Vulnerabilities (CVEs)

## The project's outdated dependencies

| Dependency | Version | Issue |
|---|---|---|
| `ojdbc8` | 19.8.0.0 | Old; CVE-2022-21369 in older 19.x. Current is 23.x. |
| `pdfbox` | 2.0.24 | CVE-2022-23711 (DoS). Fixed in 2.0.25+. |
| `openpdf` | 1.3.29 | Old. Current is 2.0.x. |
| `javax.mail` | 1.6.2 | Deprecated. Replaced by `jakarta.mail`. |
| JavaFX | 21.0.1 | Old. Current is 21.0.4 (security patches). |
| Java | 20 | Non-LTS, EOL. Use Java 21 LTS. |

## Why this matters

Outdated dependencies are the #1 source of preventable vulnerabilities. CVEs in PDFBox and OpenPDF can be triggered by crafted input. An attacker who controls an intern's email body or HTML report content may trigger a DoS or RCE.

## Detection

### Manual
Check each dependency against the CVE database (NVD, Snyk).

### Automated (recommended)
- **OWASP Dependency-Check** — Maven plugin, scans dependencies against NVD.
- **Snyk** — cloud-based, integrates with GitHub.
- **GitHub Dependabot** — opens PRs to update vulnerable deps.
- **Sonatype Nexus Lifecycle** — enterprise.

### Maven configuration
```xml
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>8.4.0</version>
    <configuration>
        <failBuildOnCVSS>7</failBuildOnCVSS>
    </configuration>
</plugin>
```

`mvn dependency-check:check` fails the build if any dependency has CVSS ≥ 7.

## The fix

```xml
<!-- Update -->
<dependency>
    <groupId>com.oracle.database.jdbc</groupId>
    <artifactId>ojdbc11</artifactId>
    <version>23.5.0.24.7</version>
</dependency>
<dependency>
    <groupId>org.apache.pdfbox</groupId>
    <artifactId>pdfbox</artifactId>
    <version>3.0.1</version>
</dependency>
<dependency>
    <groupId>com.github.librepdf</groupId>
    <artifactId>openpdf</artifactId>
    <version>2.0.3</version>
</dependency>
<!-- Replace javax.mail with jakarta.mail -->
<dependency>
    <groupId>jakarta.mail</groupId>
    <artifactId>jakarta.mail-api</artifactId>
    <version>2.1.3</version>
</dependency>
<dependency>
    <groupId>org.eclipse.angus</groupId>
    <artifactId>jakarta.mail</artifactId>
    <version>2.0.3</version>
</dependency>
```

Use Java 21 LTS, JavaFX 21.0.4+.

## Further reading

- OWASP Dependency-Check.
- Snyk vulnerability database.
