---
tags: [concept, maven, build]
type: concept
status: complete
---

# Maven

## What it is

**Maven** is Java's standard build tool. It manages dependencies, compiles, tests, packages, and deploys.

## POM (Project Object Model)

`pom.xml` is the project descriptor:
```xml
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>intern-management</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.release>21</maven.compiler.release>
        <javafx.version>21.0.4</javafx.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.openjfx</groupId>
            <artifactId>javafx-controls</artifactId>
            <version>${javafx.version}</version>
        </dependency>
        <!-- ... -->
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.openjfx</groupId>
                <artifactId>javafx-maven-plugin</artifactId>
                <version>0.0.8</version>
            </plugin>
        </plugins>
    </build>
</project>
```

## Lifecycle phases

| Phase | What happens |
|---|---|
| `validate` | Validate POM. |
| `compile` | Compile src/main/java. |
| `test` | Run unit tests (src/test/java). |
| `package` | Package into JAR/WAR. |
| `verify` | Run integration tests, quality checks. |
| `install` | Install to local repo (~/.m2). |
| `deploy` | Deploy to remote repo. |

`mvn package` runs all phases up to `package`. `mvn clean package` cleans first.

## Dependency scopes

| Scope | Available in | Used for |
|---|---|---|
| `compile` (default) | All | Main dependencies |
| `test` | Test only | JUnit, Mockito |
| `provided` | Compile, not runtime | Servlet API (provided by container) |
| `runtime` | Runtime only | JDBC driver |
| `system` | (avoid) | Local JAR |

## dependencyManagement (BOMs)

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.openjfx</groupId>
            <artifactId>javafx-controls</artifactId>
            <version>${javafx.version}</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

Declare versions once; sub-modules omit the version.

## Profiles

```xml
<profiles>
    <profile>
        <id>dev</id>
        <activation><activeByDefault>true</activeByDefault></activation>
        <!-- dev-specific config -->
    </profile>
    <profile>
        <id>prod</id>
        <!-- prod-specific config -->
    </profile>
</profiles>
```

`mvn package -Pprod` activates the prod profile.

## Project's pom.xml issues

1. Java 20 (non-LTS) — use Java 21 LTS.
2. Duplicate JavaFX dependencies (controls 3 times, web twice).
3. Old dependencies (ojdbc8 19.8, pdfbox 2.0.24, openpdf 1.3.29).
4. Deprecated `javax.mail` — use `jakarta.mail`.
5. No quality plugins (no SpotBugs, PMD, Checkstyle, JaCoCo).
6. No BOM — explicit versions everywhere.
7. Typo in artifactId: `Intern_Mnagement_app`.
8. No profiles (no dev/test/prod separation).

## Fix

```xml
<properties>
    <maven.compiler.release>21</maven.compiler.release>
    <javafx.version>21.0.4</javafx.version>
    <junit.version>5.10.0</junit.version>
</properties>
<!-- ... updated dependencies, BOM, quality plugins ... -->
```

## Further reading

- Maven: The Complete Reference (Sonatype).
