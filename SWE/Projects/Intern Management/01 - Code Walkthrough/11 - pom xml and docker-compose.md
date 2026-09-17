---
tags: [case-study, code-walkthrough, maven, docker]
type: case-study
status: complete
---

# pom.xml and docker-compose.yml

## pom.xml (194 lines)

### Coordinates (with typos)
- `groupId: com.example`
- `artifactId: Intern_Mnagement_app` (typo: "Mnagement")
- `name: Intern Mnagement app` (same typo)
- `version: 1.0-SNAPSHOT`

### Properties
- `project.build.sourceEncoding: UTF-8` (correct)
- `junit.version: 5.10.0`
- **No `maven.compiler.release`** — uses `<source>20</source><target>20</target>` instead. Java 20 is non-LTS, EOL.

### Dependencies
- `javafx-controls 21.0.1` (declared 3 times — duplicate)
- `javafx-fxml 21.0.1`
- `javafx-web 21.0.1` (declared twice)
- `javafx-graphics 21.0.1`
- `com.sun.mail:javax.mail 1.6.2` (deprecated; replaced by `jakarta.mail`. **Never used in code.**)
- `com.oracle.database.jdbc:ojdbc8 19.8.0.0` (old; current is `ojdbc11 23.x`. CVE-2022-21369 in older 19.x.)
- `org.apache.pdfbox:pdfbox 2.0.24` (CVE-2022-23711 fixed in 2.0.25+. **Never used in code.**)
- `com.github.librepdf:openpdf 1.3.29` (old; current is 2.0.x. Used via `com.lowagie.text.*`.)
- `org.junit.jupiter:junit-jupiter-api/engine 5.10.0` (test scope. **No tests exist.**)

### Plugins
- `maven-compiler-plugin 3.11.0` with `<source>20</source><target>20</target>` (should be `<release>21</release>`).
- `javafx-maven-plugin 0.0.8` with `mainClass: com.example.intern_mnagement_app/com.example.intern_manegement_app.main` (module/package/class typos).

### What's wrong
1. **Three different misspellings of "management"** in the same project.
2. **Java 20** — non-LTS, EOL. Use Java 21 LTS.
3. **Duplicate JavaFX dependencies** — `javafx-controls` declared 3 times, `javafx-web` twice.
4. **Old dependencies with CVEs** — `ojdbc8 19.8`, `pdfbox 2.0.24`, `openpdf 1.3.29`.
5. **Deprecated `javax.mail`** — should be `jakarta.mail`.
6. **Declared but unused dependencies** — `javax.mail`, `pdfbox` (the code uses `openpdf` via `com.lowagie.text.*`).
7. **JUnit declared but no tests** — `src/test/` does not exist.
8. **No BOM** — explicit versions everywhere; should use `dependencyManagement` with BOMs for JavaFX, JUnit, etc.
9. **No quality plugins** — no SpotBugs, PMD, Checkstyle, JaCoCo, Sonar, OWASP Dependency-Check.
10. **No profiles** — no dev/test/prod separation.
11. **No shade/assembly plugin** — no fat JAR for distribution.
12. **No `jpackage` config** — no native installer.

### Fix
```xml
<properties>
    <maven.compiler.release>21</maven.compiler.release>
    <javafx.version>21.0.4</javafx.version>
    <junit.version>5.10.0</junit.version>
</properties>
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.openjfx</groupId>
            <artifactId>javafx-controls</artifactId>
            <version>${javafx.version}</version>
        </dependency>
        <!-- ... -->
    </dependencies>
</dependencyManagement>
```
Add: HikariCP, jbcrypt (or argon2-jvm), SLF4J, Logback, Flyway, Mockito, Testcontainers, TestFX, SpotBugs, PMD, Checkstyle, JaCoCo, OWASP Dependency-Check. See [[24 - Build and Tooling/00 - MOC - Build and Tooling]].

## docker-compose.yml (27 lines)

```yaml
services:
  oracle-db:
    image: gvenzl/oracle-xe
    container_name: oracle-db-container
    ports:
      - "1521:1521"
    environment:
      ORACLE_PASSWORD: rootroot
    volumes:
      - oracle_data:/opt/oracle/oradata
      - ./sql-scripts:/container-entrypoint-initdb.d   # WRONG PATH
    shm_size: 2g
    # healthcheck commented out
volumes:
  oracle_data:
```

### What's wrong
1. **`ORACLE_PASSWORD: rootroot`** in plaintext YAML, committed to git.
2. **`./sql-scripts` mount path doesn't exist** — SQL files are in `src/main/sql/`. Init scripts never load.
3. **Healthcheck commented out** — app may try to connect before Oracle is ready, fail, never retry.
4. **No `restart: unless-stopped`** — container doesn't auto-restart on host reboot.
5. **No `secrets:`** — password in environment, visible via `docker inspect`.
6. **No `depends_on` with `condition: service_healthy`** for any app service.
7. **No app service** — only Oracle is containerized.
8. **`gvenzl/oracle-xe` (unversioned)** — should pin to `gvenzl/oracle-xe:21-slim`.
9. **No network isolation** — no custom network defined.

### Fix
```yaml
services:
  oracle-db:
    image: gvenzl/oracle-xe:21-slim
    restart: unless-stopped
    ports: ["1521:1521"]
    environment:
      ORACLE_PASSWORD_FILE: /run/secrets/oracle_password
      APP_USER: intern_app
      APP_USER_PASSWORD_FILE: /run/secrets/app_password
    volumes:
      - oracle_data:/opt/oracle/oradata
      - ./src/main/sql:/container-entrypoint-initdb.d:ro
    shm_size: 2g
    secrets: [oracle_password, app_password]
    healthcheck:
      test: ["CMD", "healthcheck.sh"]
      interval: 15s
      timeout: 10s
      retries: 5
    networks: [app-tier]
  app:
    build: .
    depends_on:
      oracle-db: { condition: service_healthy }
    environment:
      DB_URL: jdbc:oracle:thin:@oracle-db:1521/XE
      DB_USER_FILE: /run/secrets/app_user
      DB_PASSWORD_FILE: /run/secrets/app_password
    secrets: [app_user, app_password]
    networks: [app-tier]
secrets:
  oracle_password: { file: ./secrets/oracle_password.txt }
  app_password: { file: ./secrets/app_password.txt }
  app_user: { file: ./secrets/app_user.txt }
volumes:
  oracle_data:
networks:
  app-tier:
    driver: bridge
```
See [[25 - Docker and Deployment/00 - MOC - Docker]].
