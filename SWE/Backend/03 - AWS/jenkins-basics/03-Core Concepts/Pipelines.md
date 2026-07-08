---
tags: [jenkins, pipeline]
---

# Pipelines

> [!summary] TL;DR
> A **Pipeline** is a series of stages (build → test → deploy) defined as Groovy code. It's the modern way to model CI/CD in Jenkins.

## Why Pipelines?

- **As code** — versioned in a `Jenkinsfile` alongside your source.
- **Durable** — survives controller restarts.
- **Pausable** — manual approvals, input gates.
- **Parallel** — run stages in parallel for speed.
- **Reusable** — shared libraries.

## A Minimal Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'make build'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'make test'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'make deploy'
            }
        }
    }
}
```

## Pipeline Concepts

| Concept       | Description                                                                  |
| ------------- | ---------------------------------------------------------------------------- |
| `pipeline {}` | Top-level block.                                                             |
| `agent`       | Where to run (any, label, docker, kubernetes).                               |
| `stages`      | Container for one or more `stage` blocks.                                    |
| `stage`       | A named logical step (e.g. "Build").                                         |
| `steps`       | Concrete actions inside a stage (`sh`, `echo`, `git`, etc.).                 |
| `post`        | Actions after the run (`always`, `success`, `failure`).                      |
| `environment` | Env vars available throughout the pipeline.                                  |
| `options`     | Pipeline-level config (timeouts, retries, timestamps).                       |

## Stage Graph (Visual)

```mermaid
flowchart LR
    Checkout --> Build --> Test --> Scan --> Deploy_Staging --> Approve --> Deploy_Prod
```

## Parallel Stages

```groovy
stage('Test') {
    parallel {
        stage('Unit')   { steps { sh 'make unit' } }
        stage('Integration') { steps { sh 'make integration' } }
        stage('Lint')   { steps { sh 'make lint' } }
    }
}
```

## Declarative vs Scripted

| Style          | Look                                          | When to use                       |
| -------------- | --------------------------------------------- | --------------------------------- |
| **Declarative**| `pipeline { stages { stage { steps {} } } }`  | Default. Simpler, structured.     |
| **Scripted**   | `node { stage('X') { ... } }`                 | Need full Groovy flexibility.     |

> [!tip] Start with Declarative
> It's the modern default. Drop to Scripted only when you hit a limitation.

## Post Section

```groovy
post {
    always  { junit 'reports/**/*.xml' }
    success { slackSend channel: '#deploy', message: "Build OK: ${env.BUILD_URL}" }
    failure { emailext to: 'team@x.com', subject: 'Build failed', body: 'See ${BUILD_URL}' }
}
```

## Related Notes
- [[Pipeline as Code]] · [[Stages and Steps]] · [[Jobs]] · [[Build Triggers]]
