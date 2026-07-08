---
tags: [pull-requests, mistakes, pitfalls, beginner]
aliases: [PR Mistakes, Beginner Errors, Common Errors]
---

# Common Mistakes Beginners Make When Creating PRs

Learning from mistakes is powerful, but learning from *others'* mistakes is even better. This note catalogs the most frequent errors new contributors make, so you can avoid them entirely.

## Mistake 1: Not Reading CONTRIBUTING.md

**What happens:** You submit a PR that doesn't follow the project's conventions — wrong commit message format, missing tests, incorrect branch name. The reviewer has to point out these basic issues, which wastes everyone's time.

**Why it's a problem:** It signals to maintainers that you haven't done your homework. First impressions matter, and ignoring the contributing guide is the fastest way to make a bad one.

**How to avoid:**
- Read CONTRIBUTING.md thoroughly before starting any work
- Keep it open in a browser tab while you work
- Follow every instruction exactly — even the ones that seem trivial
- If something is unclear, ask before you start coding

## Mistake 2: Working on the Main Branch

**What happens:** You clone the repo and start making changes directly on `main` or `master`. When you try to open a PR, you can't — or your changes include unrelated commits that have nothing to do with your contribution.

**Why it's a problem:** Your PR should contain only the changes related to your specific fix or feature. Mixing in unrelated changes makes the review harder and increases the risk of accidentally including something you didn't intend.

**How to avoid:**
```bash
# ALWAYS create a new branch
git checkout -b fix/my-specific-issue

# NEVER work directly on main
```

## Mistake 3: Giant Pull Requests

**What happens:** You try to fix three bugs and add two features all in one PR. The PR has 47 changed files and 800+ lines of code. Reviewers take one look and close the tab.

**Why it's a problem:** Large PRs are intimidating, hard to review, and risky. Reviewers have limited time and mental bandwidth. A 50-line PR might get reviewed today; a 500-line PR might sit for weeks.

**How to avoid:**
- One PR = one logical change
- If you find multiple things to fix, create separate PRs for each
- Keep your PR as small as possible while still being complete
- Aim for under 200 lines of changes for your first PR

> [!quote] The Golden Rule of PRs
> "A PR should be small enough that a reviewer can understand it in one sitting." — Every experienced maintainer ever

## Mistake 4: Vague PR Titles and Descriptions

**What happens:**
```
Title: "Fix bug"
Description: "Fixed it"
```

**Why it's a problem:** Reviewers have no idea what "it" is. They have to read through all the code changes to understand what the PR does. Many maintainers will simply skip PRs with poor descriptions.

**How to avoid:**
```
Title: "Fix redirect loop when session token expires on /dashboard"

Description:
## Problem
Users are redirected in a loop when their session token expires 
while on the /dashboard route. Issue #123.

## Solution
Added a check for expired tokens before redirecting, and redirect 
to /login instead of /dashboard when the token is invalid.

## Testing
- Added unit test for the expired token check
- Manually tested the redirect flow with expired tokens
- All existing tests pass
```

## Mistake 5: Not Linking to an Issue

**What happens:** You find a bug, fix it, and open a PR — but you never created or referenced an issue.

**Why it's a problem:** Most projects want to discuss proposed changes before you invest time coding. Without an issue, maintainers can't evaluate whether the fix is aligned with the project's priorities. Some projects require all PRs to reference an issue.

**How to avoid:**
- Before coding, check if an issue already exists
- If not, create one and wait for maintainer feedback
- Reference the issue in your PR: "Fixes #123" or "Resolves #456"

## Mistake 6: Ignoring CI Failures

**What happens:** You push your PR, the CI checks fail, and you ignore it, hoping the reviewer will help you fix it.

**Why it's a problem:** CI failures mean something is wrong with your code. Reviewers expect you to fix these before they review. Ignoring them signals that you haven't verified your own work.

**How to avoid:**
- Run tests locally before pushing: `npm test`, `pytest`, etc.
- If CI fails, fix the issue and push again immediately
- If you can't figure out why CI is failing, ask for help in a comment

## Mistake 7: Not Running the Project Locally

**What happens:** You make changes without ever running the project. Your code is syntactically correct but functionally broken.

**Why it's a problem:** You're asking reviewers to catch bugs that you could have caught yourself by simply running the project.

**How to avoid:**
- Follow the setup instructions in CONTRIBUTING.md
- Run the project and use it before making changes
- Test your changes locally before pushing
- Run the full test suite

## Mistake 8: Changing Unrelated Code

**What happens:** While working on your fix, you notice a typo in a different file and fix it, reformat some code that's not related to your change, and "clean up" a function that you're not actually modifying.

**Why it's a problem:** Unrelated changes make the PR harder to review and increase the risk of introducing bugs. They also make it harder to revert specific changes if something goes wrong.

**How to avoid:**
- Only change what's necessary for your specific fix
- If you notice unrelated issues, create separate PRs for them
- Resist the urge to "clean up while you're here"

## Mistake 9: Getting Defensive About Feedback

**What happens:** A reviewer suggests a change, and you respond defensively, arguing that your approach is correct without considering their perspective.

**Why it's a problem:** Reviewers are trying to help. Defensive responses make the process unpleasant and may discourage reviewers from engaging with your future PRs.

**How to avoid:** See [[Responding to Review Feedback]] for detailed guidance on handling feedback gracefully.

## Mistake 10: Submitting Without Testing

**What happens:** You write code, push it, and open a PR without running any tests — not even verifying that the project still builds.

**Why it's a problem:** Untested code is almost guaranteed to have bugs. It wastes the reviewer's time and damages your credibility.

**How to avoid:**
```bash
# Before pushing, ALWAYS:
npm test          # Run the test suite
npm run lint      # Run the linter
npm run build     # Verify the build works

# For your specific change:
# Manually test the feature/fix you implemented
```

## Mistake 11: Abandoning Your PR

**What happens:** You open a PR, get feedback, and never respond. Weeks pass, and the maintainer eventually closes the PR.

**Why it's a problem:** You've wasted the reviewer's time. The feedback they wrote goes unused. And the project still has the bug or missing feature you were trying to address.

**How to avoid:**
- Only open a PR when you have time to follow through
- If you can't address feedback immediately, comment: "Thanks for the review! I'll address this within the next few days."
- If you need to abandon a PR, close it yourself with a note explaining why

## Mistake 12: Not Squashing "Work in Progress" Commits

**What happens:** Your PR has commits like:
```
fix: redirect bug
fix: actually fix it
fix: oops forgot a file
fix: lint errors
fix: real fix this time
fix: please work
```

**Why it's a problem:** This makes the project's Git history messy and hard to navigate. Maintainers want clean, meaningful commits.

**How to avoid:**
- Write meaningful commit messages from the start
- Before final review, use interactive rebase to squash messy commits
- See [[Updating a PR]] for details on squashing

## Quick Reference: The Anti-Pattern Checklist

Before submitting your PR, verify:

- [ ] I read CONTRIBUTING.md
- [ ] I'm working on a dedicated feature branch (not main)
- [ ] My PR addresses one specific issue
- [ ] My PR title is clear and descriptive
- [ ] My PR description explains what, why, and how
- [ ] I linked the related issue
- [ ] I ran the project locally and tested my changes
- [ ] All tests pass
- [ ] The linter passes
- [ ] I didn't include unrelated changes
- [ ] I wrote tests for my changes
- [ ] I'm prepared to respond to review feedback

---

**Previous:** [[Merging a PR]]
**Next:** [[PR Best Practices]]
