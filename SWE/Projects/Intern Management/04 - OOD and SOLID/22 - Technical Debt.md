---
tags: [concept, technical-debt, quality]
type: concept
status: complete
related:
  - [[04 - OOD and SOLID/03 - Code Smells Catalog]]
  - [[32 - Putting It All Together/00 - MOC - Rebuild]]
---

# Technical Debt

> "Shipping first time code is like going into debt. A little debt speeds development so long as it is paid back promptly with a rewrite. ... The danger occurs when the debt is not repaid. Every minute spent on not-quite-right code counts as interest on that debt. Entire engineering organizations can be brought to a stand-still under the debt load of an unconsolidated implementation." — Ward Cunningham, 1992

## What it is

**Technical debt** is the implied cost of future rework caused by choosing an easy solution now instead of a better approach. Like financial debt, it accumulates interest.

## Types of technical debt

1. **Deliberate, prudent** — "We know this is a hack, but we need to ship. We'll fix it next sprint." (Acknowledged and tracked.)
2. **Deliberate, reckless** — "We don't have time for design. Just make it work." (Acknowledged but not tracked.)
3. **Accidental, prudent** — "We didn't realize this design was wrong until we used it for 6 months. Now we know." (Discovered in hindsight.)
4. **Accidental, reckless** — "What's layering?" (Ignorance-driven debt.)

## Symptoms

- **"It takes forever to add a simple feature"** — the codebase resists change.
- **"Every change breaks something else"** — high regression rate.
- **"Nobody understands module X"** — knowledge concentration.
- **"We're afraid to refactor"** — fear of breaking things.
- **"The tests don't pass"** or **"We have no tests"** — no safety net.

## The project's technical debt

The 85 issues in the reviews are all technical debt. Critical debts:
- 940-LOC God Class.
- Hardcoded credentials.
- Unsalted SHA-256.
- No transactions, no logging, no tests.
- Two conflicting schemas.
- Mixed Swing + JavaFX.

Estimated payoff time: 60-160 hours across 4 phases. See [[32 - Putting It All Together/00 - MOC - Rebuild]].

## How to pay down debt

1. **Acknowledge it** — write it down (issue tracker, TODO with reason).
2. **Prioritize** — pay down the highest-interest debt first (critical bugs, security).
3. **Allocate time** — 20% of every sprint for refactoring (the "boy scout rule": leave the code better than you found it).
4. **Test before refactoring** — characterization tests lock in current behavior.
5. **Refactor in small steps** — one method at a time, run tests after each.
6. **Don't add new debt** — write new code cleanly.

## The boy scout rule

> "Leave the campground cleaner than you found it." — Robert Stephenson Smyth Baden-Powell

Every time you touch a file, leave it a little better. Rename a variable, extract a method, fix a typo. Over time, the codebase improves.

## Common pitfalls

- **"We'll rewrite it from scratch"** — usually a mistake. Joel Spolsky's "Things You Should Never Do" explains why.
- **"Refactoring is a separate phase"** — no, it's continuous. Refactor as you go.
- **"We don't have time for refactoring"** — you don't have time *not* to refactor. The debt is slowing you down.
- **Big-bang refactors** — touching 100 files in one PR. Break into small refactors with tests.

## Project Connection

The project is the debt. The reviews are the audit. The refactoring roadmap is the repayment plan.

## Further reading

- Cunningham, "The WyCash Portfolio Management System" (1992 OOPSLA).
- *Refactoring* (Fowler), Chapter 2.
- Martin Fowler's blog posts on technical debt (martinfowler.com).
