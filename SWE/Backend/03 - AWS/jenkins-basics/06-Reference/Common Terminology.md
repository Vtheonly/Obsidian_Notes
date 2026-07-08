---
tags: [jenkins, reference, glossary]
---

# Common Terminology

> [!summary] TL;DR
> Quick glossary of Jenkins terms. Bookmark this page.

## A–F

| Term              | Short definition                                                | See                  |
| ----------------- | --------------------------------------------------------------- | -------------------- |
| **Agent**         | A worker that runs builds.                                       | [[Jenkins Architecture]] |
| **Artifact**      | File produced by a build (jar, image, zip).                      | [[Stages and Steps]]  |
| **Blue Ocean**    | Modern pipeline UI.                                              | [[Dashboard Overview]]|
| **Build**         | One execution of a job.                                          | [[Jobs]]              |
| **Controller**    | The main Jenkins server (formerly "master").                     | [[Jenkins Architecture]] |
| **Credential**    | Stored secret.                                                   | [[Managing Credentials]] |
| **Declarative Pipeline** | Structured `pipeline {}` syntax.                         | [[Pipelines]]         |
| **Executor**      | A slot on an agent that runs one build at a time.                | [[Jenkins Architecture]] |

## G–N

| Term              | Short definition                                                | See                  |
| ----------------- | --------------------------------------------------------------- | -------------------- |
| **Groovy**        | Language used to write `Jenkinsfile`s.                          | [[Pipelines]]         |
| **`Jenkinsfile`** | File at repo root defining a pipeline.                          | [[Pipeline as Code]]  |
| **Job**           | A runnable unit (formerly "project").                           | [[Jobs]]              |
| **Multibranch Pipeline** | Auto-creates a pipeline per branch/PR.                  | [[Pipeline as Code]]  |
| **Node**          | Generic term for controller or agent.                           | [[Jenkins Architecture]] |

## O–Z

| Term              | Short definition                                                | See                  |
| ----------------- | --------------------------------------------------------------- | -------------------- |
| **Pipeline**      | Multi-stage workflow defined in code.                           | [[Pipelines]]         |
| **Plugin**        | Extension that adds capability.                                  | [[Plugins]]           |
| **Post section**  | Block that runs after the pipeline (success/failure/always).    | [[Pipelines]]         |
| **Scripted Pipeline** | Free-form Groovy pipeline.                                   | [[Pipelines]]         |
| **Stage**         | Named block of work (Build, Test, Deploy).                      | [[Stages and Steps]]  |
| **Step**          | Single action inside a stage.                                    | [[Stages and Steps]]  |
| **Trigger**       | What causes a build to start.                                    | [[Build Triggers]]    |
| **Webhook**       | HTTP push from Git to Jenkins to trigger builds.                 | [[Build Triggers]]    |
| **Workspace**     | Per-job directory on the agent where checkout & build happen.   | [[Jobs]]              |
| **`JENKINS_HOME`** | Jenkins data directory.                                         | [[Jenkins Architecture]] |

## Related Notes
- [[Best Practices for Beginners]] · [[Shared/readme]]
