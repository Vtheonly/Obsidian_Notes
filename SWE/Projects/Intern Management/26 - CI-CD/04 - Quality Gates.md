---
tags: [concept, ci-cd, quality-gates]
type: concept
status: complete
related:
  - [[24 - Build and Tooling/07 - Static Analysis (SpotBugs, PMD, Checkstyle, Sonar)]]
---

# Quality Gates

## What it is

A **quality gate** is a set of criteria the build must pass to be deployable. If any criterion fails, the build fails.

## Typical gates

- **Tests pass** — 0 failures.
- **Coverage ≥ X%** — e.g., 80% line coverage.
- **No critical bugs** (SpotBugs, SonarQube).
- **No vulnerabilities** (OWASP Dependency-Check, CVSS ≥ 7).
- **No new code smells** (SonarQube).
- **Code duplication < X%** (SonarQube).
- **Checkstyle passes** (no style violations).

## Maven configuration

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>check</id>
            <goals><goal>check</goal></goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

`mvn verify` fails if coverage < 80%.

## SonarQube Quality Gate

SonarQube has its own quality gate concept:
- New code coverage ≥ 80%.
- New bugs = 0.
- New vulnerabilities = 0.
- New code smells = 0.

Configure in the SonarQube UI. The CI pipeline runs `mvn sonar:sonar` and checks the quality gate status.

## When to enforce

- **PR to main** — must pass quality gate before merge.
- **Release** — must pass stricter gate (e.g., 90% coverage).

## Don't over-enforce

- A 95% coverage requirement on legacy code blocks all PRs.
- Start lenient (50%), increase over time.
- Use "new code" metrics (SonarQube) — only enforce on changed code.

## Project Connection

The project has zero quality gates — no tests, no static analysis, no coverage. The fix:
1. Phase 0: add the tools (SpotBugs, PMD, Checkstyle, JaCoCo) with `failOnViolation=false` (just collect data).
2. Phase 1: write characterization tests; set coverage target to 20%.
3. Phase 2: increase to 60%.
4. Phase 4: increase to 80%.

## Further reading

- SonarQube Quality Gates.
