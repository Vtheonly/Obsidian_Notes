---
tags: [checklist, pull-requests, reference]
aliases: [PR Checklist, Before You Submit, Pre-Submission]
---

# Pre-PR Checklist

Use this checklist before opening any Pull Request. Going through it carefully prevents the most common reasons PRs get rejected or stuck in review.

## Before You Start Coding

- [ ] **Read CONTRIBUTING.md** — Follow the project's specific workflow and conventions
- [ ] **Check for existing issues** — Make sure there's an open issue for the change you want to make
- [ ] **Comment on the issue** — Confirm no one else is working on it and that maintainers agree with the approach
- [ ] **Set up the project locally** — Clone, install dependencies, and verify the project runs
- [ ] **Run the test suite** — Make sure all tests pass before you make any changes (baseline)
- [ ] **Create a new branch** — Never work on `main` or `master`

## While Coding

- [ ] **Make only necessary changes** — Don't include unrelated modifications
- [ ] **Follow the project's code style** — Match existing conventions
- [ ] **Write clear, self-documenting code** — Code explains *what*, comments explain *why*
- [ ] **Handle edge cases** — Null inputs, empty strings, error states
- [ ] **Don't hardcode values** — Use configuration or constants
- [ ] **Don't introduce unnecessary dependencies** — Use what the project already has

## Tests

- [ ] **Write tests for new functionality** — Every new feature needs test coverage
- [ ] **Write a test for the bug fix** — The test should fail before your fix and pass after
- [ ] **Run the full test suite** — All tests pass, not just the new ones
- [ ] **Test edge cases** — Unusual inputs, boundary conditions, error scenarios
- [ ] **Test manually** — Verify your change works in the actual application

## Code Quality

- [ ] **Run the linter** — Fix all linting errors
- [ ] **Run the formatter** — Ensure code formatting matches the project's style
- [ ] **Remove debug code** — No `console.log`, `print()`, or temporary hacks
- [ ] **Remove commented-out code** — Unless it serves a documented purpose
- [ ] **Check for typos** — In code, comments, and strings
- [ ] **Review your own diff** — Read every line you changed before committing

## Commit Quality

- [ ] **Atomic commits** — Each commit does one logical thing
- [ ] **Meaningful commit messages** — Follow the project's convention (often Conventional Commits)
- [ ] **No "work in progress" commits** — Clean up before pushing (squash if needed)
- [ ] **Proper commit format** — Check if the project requires DCO sign-off (`Signed-off-by`)

## Before Opening the PR

- [ ] **Rebase on latest main** — Make sure your branch is up to date with the upstream
- [ ] **Resolve any merge conflicts** — Conflicts must be resolved before the PR can be merged
- [ ] **Run CI checks locally** — Tests, linter, build — whatever the CI will run
- [ ] **Verify the PR scope** — The PR does one thing and only one thing
- [ ] **Check for sensitive data** — No API keys, passwords, or personal information in the diff

## Writing the PR

- [ ] **Clear, descriptive title** — Summarizes the change in one line
- [ ] **Complete description** — What changed, why, and how
- [ ] **Link the issue** — "Fixes #123" or "Resolves #456"
- [ ] **Testing instructions** — How can the reviewer verify your change?
- [ ] **Screenshots** — For UI changes, include before/after images
- [ ] **Use the project's PR template** — If one exists
- [ ] **Note any breaking changes** — If your change could break existing functionality

## The Final Scan

- [ ] **Does the PR title make sense on its own?** — Without reading the description?
- [ ] **Could a reviewer understand this PR in under 10 minutes?** — If not, add more context
- [ ] **Am I prepared to respond to feedback?** — Set aside time in the next few days
- [ ] **Am I emotionally ready for feedback?** — Remember: feedback is about the code, not about you

---

## Quick Version (For Experienced Contributors)

When you're more experienced, you can use this abbreviated version:

- [ ] CONTRIBUTING.md read
- [ ] Issue linked and discussed
- [ ] Branch created from latest main
- [ ] Changes are focused and minimal
- [ ] Tests pass (automated + manual)
- [ ] Linter/formatter clean
- [ ] Self-reviewed the diff
- [ ] PR title and description are clear
- [ ] Ready for review

---

**Previous:** [[PR Description Template]]
**Next:** [[Glossary]]
