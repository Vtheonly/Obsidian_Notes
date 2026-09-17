---
tags: [project-analysis, guidelines, workflow]
aliases: [Contributing Guide, CONTRIBUTING.md]
---

# Reading Contribution Guidelines

The `CONTRIBUTING.md` file (or the contributing section of the README) is the rulebook for how a project accepts contributions. Ignoring it is the single most common mistake beginners make, and the fastest way to get your [[What is a Pull Request|Pull Request]] rejected. Every project has its own conventions, and following them signals to maintainers that you respect their time and their process.

## Where to Find Contribution Guidelines

Contribution guidelines can live in several places:

1. **`CONTRIBUTING.md`** — The most common location, in the repository root
2. **`.github/CONTRIBUTING.md`** — Some projects put it in the `.github` directory
3. **`docs/contributing.md`** — In the documentation directory
4. **README section** — Smaller projects may include a "Contributing" section in their README
5. **Wiki** — Some projects maintain contribution guides in their GitHub Wiki
6. **Website** — Large projects (like React or Python) often have dedicated contributor pages

> [!important] Always Read CONTRIBUTING.md Before Starting
> Even if you've contributed to other projects before, each project has unique requirements. Spending 15 minutes reading the guidelines can save you hours of rework.

## What Contribution Guidelines Typically Cover

### 1. Setup Instructions

How to get the project running on your machine. This usually includes:

- Prerequisites (language version, package manager, system dependencies)
- Installation steps (`npm install`, `pip install -e .`, etc.)
- Environment setup (`.env` files, configuration)
- How to run the project locally
- How to run the test suite

### 2. Code Style and Formatting

Projects enforce consistent code style so that the codebase looks like it was written by one person, not hundreds. Common requirements include:

- Linter rules (ESLint, Pylint, RuboCop, etc.)
- Formatter configuration (Prettier, Black, gofmt, etc.)
- Naming conventions (camelCase, snake_case, etc.)
- Import ordering
- Maximum line length
- Comment and documentation style

> [!tip] Automate Formatting
> Most projects have formatting tools configured. Run them before committing:
> - JavaScript: `npm run format` or `npx prettier --write .`
> - Python: `black .` or `ruff format .`
> - Go: `gofmt -w .`
> If the project has a pre-commit hook, set it up — it will catch issues automatically.

### 3. Commit Message Format

Many projects enforce specific commit message conventions. The most common is **Conventional Commits**:

```
type(scope): description

[optional body]

[optional footer]
```

Common types:

| Type | Usage |
|------|-------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation change |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring, no behavior change |
| `test` | Adding or updating tests |
| `chore` | Build, CI, or tooling changes |

Examples:
```
fix(auth): resolve login redirect loop on expired tokens
docs(api): update authentication endpoint parameters
feat(search): add fuzzy matching to search algorithm
```

> [!warning] Wrong Commit Format = Failed CI
> Many projects have CI checks that validate commit message format. If your commit message doesn't follow the convention, the CI will fail and your PR won't be merged until you fix it. This is one of the most common reasons PRs get stuck.

### 4. Branch Naming Conventions

Some projects require specific branch names:

- `fix/issue-123-login-bug`
- `feature/add-dark-mode`
- `docs/update-api-reference`
- `your-name/short-description`

### 5. Pull Request Requirements

What your PR must include to be accepted:

- **Template** — Fill out the PR template completely
- **Description** — Explain what changed and why
- **Linked issue** — Reference the issue number (e.g., "Fixes #123")
- **Tests** — New code must have corresponding tests
- **Documentation** — Features must be documented
- **Changelog entry** — Some projects require a changelog update
- **Screenshots** — For UI changes, before/after screenshots

### 6. Code Review Process

- Who reviews PRs (specific maintainers, or anyone?)
- Expected review timeline
- How many approvals are needed before merging
- How to handle requested changes

### 7. Legal Requirements

Some projects require:

- **CLA (Contributor License Agreement)** — A legal agreement that gives the project rights to use your contribution. Common in corporate-backed projects.
- **DCO (Developer Certificate of Origin)** — A simpler alternative where you certify that you wrote the code. Signified by adding `Signed-off-by: Your Name <email>` to your commit.

## How to Read CONTRIBUTING.md Effectively

### The Skim-Then-Deep-Read Approach

1. **First pass (5 minutes):** Skim the entire document to get an overview. Note the key sections.
2. **Second pass (15 minutes):** Read carefully, especially the setup instructions, commit conventions, and PR requirements.
3. **Bookmark it:** You'll reference this document repeatedly as you work.

### Create a Personal Checklist

Based on the contributing guide, create a checklist for yourself:

```
Before Starting:
- [ ] Read CONTRIBUTING.md
- [ ] Set up the project locally
- [ ] Run the test suite to confirm it passes
- [ ] Check the PR template

Before Committing:
- [ ] Run the linter
- [ ] Run the formatter
- [ ] Write/update tests
- [ ] Follow commit message format
- [ ] Sign the CLA/DCO if required

Before Submitting PR:
- [ ] Push to the correct branch
- [ ] Fill out the PR template
- [ ] Link the related issue
- [ ] Add screenshots if applicable
- [ ] Verify CI passes locally
```

## When CONTRIBUTING.md Doesn't Exist

Not all projects have a contributing guide. If it's missing:

1. **Check existing PRs** — Look at recently merged PRs to understand the expected format and workflow.
2. **Check the issue tracker** — See how maintainers interact with contributors.
3. **Ask in discussions** — Open a GitHub Discussion or comment on an issue asking about contribution expectations.
4. **Follow general best practices** — Use the conventions outlined in this vault as your default.

## Red Flags in Contribution Guidelines

| Red Flag | What It Means |
|----------|--------------|
| "We don't accept external contributions" | This isn't an open source project in practice |
| Extremely complex setup with no help | Onboarding will be painful |
| Hostile or dismissive tone | The review process will likely be unpleasant |
| No mention of review process | You won't know what to expect |
| Required CLA with aggressive terms | The project may have ulterior motives |

## The Bottom Line

Reading and following the contribution guidelines is the single most important thing you can do to ensure your PR is accepted. It shows respect for the project's conventions and saves everyone time. Think of it as the difference between walking into someone's house with your shoes on versus off — it's a small effort that makes a big impression.

---

**Previous:** [[Project Structure]]
**Next:** [[What is a Pull Request]]
