---
tags: [vault-management, readme]
iteration: 12
---

# 00 — Vault Management

> [!info] This folder is the project-state layer of the vault. It is the **first thing every iteration reads** and the **last thing every iteration updates**.

## Purpose

The vault is built iteratively per the protocol in `Master AI/What to do.md`. To allow any future iteration to recover state cleanly, this folder maintains a persistent record of:

- What the vault should eventually contain (the roadmap).
- What the current state is (status snapshot).
- What has been completed (historical log).
- What remains to be done (prioritized backlog).
- What the current and next iterations are doing (handoff).
- Why structural decisions were made (ADR log).
- How well the vault covers the master prompt (audit).
- What research is still open (research queue).

## Files

| File                       | Purpose                                                                  | Updated when                           |
|----------------------------|--------------------------------------------------------------------------|----------------------------------------|
| `README.md`                | This file.                                                               | Rarely.                                |
| `Master Roadmap.md`        | The complete intended vault. Source of truth for structure and scope.    | When roadmap changes.                  |
| `Vault Status.md`          | Concise current-state snapshot.                                          | Every iteration.                       |
| `Completed Work.md`        | Historical log of what each iteration produced.                          | Every iteration.                       |
| `Remaining Work.md`        | Prioritized backlog.                                                     | Every iteration.                       |
| `Current Iteration.md`     | What the current iteration is doing.                                     | Start and end of every iteration.      |
| `Next Iteration.md`        | Handoff for the next iteration.                                          | End of every iteration.                |
| `Architecture Decisions.md`| ADR log — append-only record of structural choices.                      | When a structural decision is made.    |
| `Coverage Audit.md`        | Periodic audit against the master prompt.                                | End of every iteration (or periodically).|
| `Research Queue.md`        | Open research questions and unresolved factual claims.                   | Whenever research items are identified.|

## Reading Order for a New Iteration

1. `Next Iteration.md`
2. `Vault Status.md`
3. `Master Roadmap.md`
4. `Remaining Work.md`
5. `Coverage Audit.md`
6. `Research Queue.md`
7. `Architecture Decisions.md`
8. `Completed Work.md` (skim — for context)
9. Then up one level to the top-level `MOC.md` and `README.md`.

## Editing Rules

- **Never delete completed work** — supersede it with a new entry that links back.
- **Never silently renumber top-level domains** — see [[Architecture Decisions]] ADR-001.
- **Always update `Vault Status.md` before stopping an iteration.**
- **Always prepare `Next Iteration.md` before stopping an iteration.**
- **Always record structural changes in `Architecture Decisions.md`.**

## See Also

- Top-level [[README|Vault README]]
- Top-level [[MOC|Master Map of Content]]
- [[Master Roadmap]]
