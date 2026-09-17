---
tags: [concept, security, secrets, configuration]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/08 - Principle of Least Privilege]]
  - [[25 - Docker and Deployment/02 - Docker Secrets]]
---

# Secrets Management

## The problem

The project hardcodes DB credentials in source:
```java
private static final String URL = "jdbc:oracle:thin:@localhost:1521:XE";
private static final String USERNAME = "system";
private static final String PASSWORD = "rootroot";
```

Anyone with repo access has the credentials. Anyone with the compiled JAR can extract them (strings in class files). You can't rotate without recompiling. You can't have different credentials per environment.

## The rule

> "Never store secrets in source code."

## Where to store secrets

### 1. Environment variables (simple)
```java
String dbUrl = System.getenv("DB_URL");
String dbUser = System.getenv("DB_USER");
String dbPassword = System.getenv("DB_PASSWORD");
```
Pro: simple, standard, works everywhere.
Con: visible in process listing (`ps auxe`); leaks via `java -D` command line.

### 2. `.env` file (dev only)
```
DB_URL=jdbc:oracle:thin:@localhost:1521:XE
DB_USER=intern_app
DB_PASSWORD=secret
```
Add `.env` to `.gitignore`. Load via dotenv library.
Pro: convenient for dev.
Con: still plaintext on disk; don't use in prod.

### 3. Docker Secrets
```yaml
services:
  app:
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
    secrets: [db_password]
secrets:
  db_password: { file: ./secrets/db_password.txt }
```
The secret is mounted as a file; the app reads it. Not visible in `docker inspect`.

### 4. Secrets manager (prod)
- **AWS Secrets Manager** — cloud-native.
- **HashiCorp Vault** — self-hosted, popular.
- **Azure Key Vault** — Azure.
- **GCP Secret Manager** — GCP.

The app fetches secrets at startup from the manager. Secrets are encrypted at rest, access-controlled, auditable, and rotatable.

### 5. OS keyring (desktop apps)
- **Windows Credential Manager**.
- **macOS Keychain**.
- **Linux secret-service (dbus)**.

For a desktop app, store per-user secrets (like saved DB credentials) in the OS keyring.

## Project Connection

The fix:
1. **Dev**: `.env` file (gitignored), loaded via dotenv.
2. **CI**: GitHub Actions secrets, injected as env vars.
3. **Prod (if server)**: Vault or AWS Secrets Manager.
4. **Prod (if desktop)**: OS keyring via `jkeyring` library.

```java
// Dev: env vars
String dbUrl = System.getenv("DB_URL");
// Prod: secrets manager
String dbPassword = secretsManager.getSecret("db_password");
```

## Further reading

- 12-Factor App — Config.
- OWASP Secrets Management Cheat Sheet.
