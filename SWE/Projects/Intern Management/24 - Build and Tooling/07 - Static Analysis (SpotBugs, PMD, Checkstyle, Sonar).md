---
tags: [concept, build, static-analysis, quality]
type: concept
status: complete
related:
  - [[27 - Testing/00 - MOC - Testing]]
---

# Static Analysis (SpotBugs, PMD, Checkstyle, Sonar)

## What they do

| Tool | What it finds |
|---|---|
| **Checkstyle** | Style violations (naming, formatting, imports). |
| **PMD** | Code smells (empty catch, unused fields, complex methods). |
| **SpotBugs** (was FindBugs) | Bug patterns (null derefs, resource leaks, SQL injection). |
| **SonarQube** | All of the above + coverage + duplication + complexity. |
| **Error Prone** | Compile-time bug detection (Google). |
| **NullAway** | Null-pointer analysis (Uber). |

## Maven configuration

```xml
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.7.3</version>
    <executions>
        <execution>
            <goals><goal>check</goal></goals>
        </execution>
    </executions>
    <configuration>
        <effort>Max</effort>
        <threshold>Low</threshold>
        <failOnError>true</failOnError>
    </configuration>
</plugin>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.3.0</version>
    <configuration>
        <configLocation>google_checks.xml</configLocation>
        <failOnViolation>true</failOnViolation>
    </configuration>
</plugin>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-pmd-plugin</artifactId>
    <version>3.21.0</version>
    <configuration>
        <failOnViolation>true</failOnViolation>
    </configuration>
</plugin>
```

`mvn verify` runs all of them. The build fails if violations are found.

## SonarQube

Self-hosted (or SonarCloud SaaS). Scans code for:
- Bugs (like SpotBugs).
- Vulnerabilities (OWASP Top 10).
- Code smells.
- Coverage (integrates with JaCoCo).
- Duplication.
- Complexity.

```bash
mvn sonar:sonar -Dsonar.projectKey=intern-management -Dsonar.host.url=http://localhost:9000
```

## What they'd catch in the project

- **SpotBugs**: `value == ""` (string comparison bug), `Map` iteration order reliance, `getMaxId` SQL injection.
- **PMD**: `oracleConnector` God Class, `JOptionPane` in DAO, dead code (`DataPreprocessor`, `isHashEqual`).
- **Checkstyle**: lowercase class names, missing Javadoc, magic numbers.
- **SonarQube**: all of the above + duplication (95% duplicated CRUD), complexity, coverage (0%).

## Further reading

- SpotBugs bug descriptions.
- SonarQube rules.
