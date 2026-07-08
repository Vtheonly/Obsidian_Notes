---
tags: [postman, newman, cli]
---

# Newman (CLI)

> [!summary] TL;DR
> **Newman** is the command-line companion to Postman. It runs collections headlessly — perfect for CI/CD, scheduled jobs, and Docker.

## Install

```bash
# Requires Node.js 18+
npm install -g newman

# Optional reporters
npm install -g newman-reporter-htmlextra newman-reporter-junitfull

newman --version
```

## Basic Run

```bash
# Run a collection JSON
newman run collection.json

# With environment
newman run collection.json -e env.dev.json

# With globals
newman run collection.json -g globals.json

# With data file (CSV)
newman run collection.json -d users.csv

# Multiple iterations
newman run collection.json -n 5
```

## Exporting from Postman

1. Right-click your collection → **Export** → **Collection v2.1**.
2. (Optional) Export environment as JSON.

## Common Flags

| Flag                          | Purpose                                |
| ----------------------------- | -------------------------------------- |
| `-e, --environment <file>`    | Environment JSON file.                 |
| `-g, --globals <file>`        | Globals JSON file.                     |
| `-d, --iteration-data <file>` | CSV/JSON data file.                    |
| `-n, --iteration-count <n>`   | Number of iterations.                  |
| `--folder <name>`             | Run only a specific folder/request.    |
| `--delay-request <ms>`        | Delay between requests.                |
| `--bail`                      | Stop on first error.                   |
| `--suppress-exit-code`        | Don't fail the shell on test failure.  |
| `-r, --reporters <...>`       | Reporters: cli, json, junit, htmlextra.|
| `--reporter-htmlextra-export <path>` | HTML report output file.       |
| `--env-var "k=v"`             | Override an env var.                   |
| `--color off`                 | Disable color.                         |

## Reporters

```bash
# CLI (default) + JSON + JUnit + HTML
newman run collection.json \
  -e env.dev.json \
  -r cli,json,junit,htmlextra \
  --reporter-json-export results.json \
  --reporter-junit-export junit.xml \
  --reporter-htmlextra-export report.html
```

## CI/CD Examples

### GitHub Actions

```yaml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm install -g newman newman-reporter-htmlextra
      - run: newman run tests/collection.json -e tests/env.ci.json -r cli,htmlextra --reporter-htmlextra-export report.html
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: newman-report
          path: report.html
```

### GitLab CI

```yaml
api-tests:
  image: node:20
  script:
    - npm install -g newman newman-reporter-htmlextra
    - newman run tests/collection.json -e tests/env.ci.json -r cli,junit --reporter-junit-export junit.xml
  artifacts:
    when: always
    reports:
      junit: junit.xml
```

### Docker

```bash
docker run --rm \
  -v "$PWD:/etc/newman" \
  -w /etc/newman \
  postman/newman:latest \
  run collection.json -e env.ci.json -r cli
```

## Exit Codes

| Code | Meaning                                    |
| ---- | ------------------------------------------ |
| 0    | All tests passed.                          |
| 1    | One or more tests failed.                  |
| 2    | Collection could not be loaded / other error. |

Use `--suppress-exit-code` if you want to always return 0 (e.g. when generating reports).

## Tips

-  Store collections + environments in Git.
-  Never commit secrets — inject via CI secrets / `--env-var`.
-  Generate JUnit XML for Jenkins/GitLab test result visualization.
-  Pin Newman version (`newman@6.x`) in CI to avoid surprises.
-  Combine with [[Monitors]] for cloud-scheduled runs.

## Related Notes
- [[Collection Runner]] · [[Assertions and Automated API Testing]] · [[Real-World Workflows]] · [[Best Practices and Troubleshooting]]
