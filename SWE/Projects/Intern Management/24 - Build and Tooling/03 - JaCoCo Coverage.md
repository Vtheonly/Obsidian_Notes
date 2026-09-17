---
tags: [concept, build, coverage, jacoco]
type: concept
status: complete
related:
  - [[27 - Testing/00 - MOC - Testing]]
---

# JaCoCo Coverage

## What it is

**JaCoCo** (Java Code Coverage) measures which lines of code are executed by tests.

## Configuration

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals><goal>report</goal></goals>
        </execution>
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
                                <minimum>0.60</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

`mvn verify` runs tests with JaCoCo, generates a report (`target/site/jacoco/index.html`), and fails if coverage < 60%.

## Reading the report

- **Line coverage** — % of lines executed.
- **Branch coverage** — % of branches taken.
- **Method coverage** — % of methods called.
- **Class coverage** — % of classes instantiated.

Aim for 80% line coverage on the service and repository layers. UI controllers are harder to test; lower coverage is acceptable.

## Project Connection

The project has zero tests → 0% coverage. The fix:
1. Write characterization tests (Phase 1 of the roadmap).
2. Add JaCoCo.
3. Set initial target to 20% (realistic for legacy code).
4. Increase to 60% after Phase 2 (refactor).
5. Target 80% after Phase 4 (enterprise hardening).

## Further reading

- JaCoCo documentation.
