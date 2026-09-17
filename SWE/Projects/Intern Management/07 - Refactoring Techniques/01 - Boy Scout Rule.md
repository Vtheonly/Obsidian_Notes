---
tags: [concept, refactoring, boy-scout]
type: concept
status: complete
related:
  - [[07 - Refactoring Techniques/12 - What Is Refactoring]]
  - [[04 - OOD and SOLID/22 - Technical Debt]]
---

# Boy Scout Rule

> "Leave the campground cleaner than you found it." — Robert Stephenson Smyth Baden-Powell, *Scouting for Boys*, 1908

## What it is

The **Boy Scout Rule** (applied to code) says: every time you touch a file, leave it a little better than you found it.

- Rename a cryptic variable.
- Extract a small method.
- Fix a typo.
- Add a missing test.
- Remove a dead import.
- Update a stale comment.

## Why it exists

- **Continuous improvement** — the codebase gets better over time, even without dedicated refactoring sprints.
- **Low risk** — small improvements are less likely to break things.
- **Habit** — it builds a culture of craftsmanship.

## How to apply

Every time you:
- Fix a bug — also refactor the surrounding code.
- Add a feature — also clean up the file you're editing.
- Review a PR — suggest small improvements.
- Read code — fix what you notice.

## The balance

- **Don't go overboard** — if you spend 4 hours refactoring instead of 30 minutes fixing the bug, you're slowing down.
- **Stay focused** — clean up *this* file, not the whole codebase.
- **Run tests** — make sure your cleanup doesn't break anything.

## Project Connection

The project's 85 issues won't be fixed in one sprint. The Boy Scout Rule is the sustainable approach: every PR fixes a few issues. Over months, the codebase transforms.

## Common pitfalls

- **"I'll clean it up later"** — later never comes. Clean up now.
- **Scope creep** — "while I'm here, let me refactor the whole module." Don't. Stay focused.
- **Breaking tests** — your cleanup must keep tests green. If you break a test, fix it or revert.

## Further reading

- *Clean Code* (Martin), Chapter 14 (Boy Scout Rule).
