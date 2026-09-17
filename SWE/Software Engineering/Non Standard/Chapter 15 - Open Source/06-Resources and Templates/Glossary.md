---
tags: [reference, glossary, terminology]
aliases: [Terms, Definitions, PR Terminology]
---

# Glossary

A comprehensive reference for all the terms you'll encounter in open source contribution and Pull Request workflows.

## A

### Approval
A formal sign-off from a reviewer indicating that the PR is acceptable to merge. Projects typically require one or more approvals before a PR can be merged.

### Author
The person who created the Pull Request (or wrote the code). That's you when you submit a PR.

### Automated Check / CI Check
A test or validation that runs automatically when a PR is opened or updated. Examples: unit tests, linters, build verification, security scans.

## B

### Base Branch
The branch you want to merge your changes INTO. Usually `main` or `master`. Also called the "target branch."

### Blame
A Git feature that shows who last modified each line of a file and when. Useful for understanding the history of specific code.

### Branch
A parallel version of the repository. You create a branch to work on changes without affecting the main codebase.

### Bug Bounty
A reward program where projects pay developers for finding and reporting security vulnerabilities.

## C

### Cherry-Pick
Selectively applying a specific commit from one branch to another, without merging the entire branch.

### CI / Continuous Integration
The practice of automatically running tests and checks every time code is pushed. This ensures that changes don't break the existing codebase.

### CLA / Contributor License Agreement
A legal document that contributors sign, granting the project certain rights to use their contribution. Common in corporate-backed open source projects (e.g., Google, Facebook projects).

### Clone
Creating a local copy of a remote repository on your computer. Done with `git clone`.

### Code Owner
A person or team responsible for reviewing changes to specific files or directories in a project. Defined in `.github/CODEOWNERS`.

### Code Review
The process of having another developer examine your code before it's merged. Reviewers check for correctness, quality, security, and adherence to project standards.

### Code of Conduct
A document defining expected behavior within a project's community. It establishes standards for respectful and inclusive interaction.

### Commit
A snapshot of your changes saved in Git's history. Each commit has a unique hash, an author, a timestamp, and a message.

### Conventional Commits
A commit message format standard: `type(scope): description`. Common types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`.

### Contributor
Anyone who makes a contribution to an open source project — code, documentation, bug reports, design, etc.

### CONTRIBUTING.md
A file in the repository root that documents how to contribute to the project. It covers setup, style guides, commit conventions, PR requirements, and more.

## D

### DCO / Developer Certificate of Origin
A lighter alternative to a CLA. Contributors certify they have the right to submit the code by adding `Signed-off-by:` to their commit messages.

### Diff
The difference between two versions of a file. In a PR, the diff shows what lines were added (green) and removed (red).

### Draft PR
A Pull Request that is still a work in progress. It signals to maintainers that the PR is not ready for full review yet. Can be converted to a regular PR when ready.

## E

### Edge Case
An unusual or unexpected input or condition that your code should handle gracefully. Examples: empty lists, null values, extremely large numbers.

## F

### Feature Branch
A branch created specifically for developing a new feature or fixing a bug. Also called a "topic branch" or "working branch."

### Fork
A personal copy of someone else's repository on GitHub. You can make changes to your fork without affecting the original project.

### Fork and Pull Model
The standard contribution workflow for open source: fork the repo, make changes in your fork, and submit a Pull Request to the original.

## G

### `good first issue`
A GitHub label used to tag issues that are suitable for new contributors. These issues are typically small, well-defined, and don't require deep project knowledge.

### Governance
The system of rules, practices, and processes by which a project is directed and maintained. Includes decision-making processes, roles, and conflict resolution.

## H

### Head Branch
The branch that contains your changes (the source of the PR). Also called the "compare branch" or "feature branch."

### `help wanted`
A GitHub label indicating that maintainers are actively seeking help with an issue. Similar to `good first issue` but may include more complex tasks.

## I

### Issue
A report or discussion item in a project's tracker. Issues can be bug reports, feature requests, questions, or tasks.

### Issue Template
A pre-defined format for creating new issues, ensuring that all necessary information is included.

## L

### LGTM
"Looks Good To Me" — A common shorthand used by reviewers to indicate they approve of the code.

### Linter
A tool that analyzes source code to flag programming errors, bugs, stylistic errors, and suspicious constructs. Examples: ESLint, Pylint, RuboCop.

## M

### Main Branch
The primary branch of a repository, containing the latest stable code. Historically called `master` in many projects.

### Maintainer
A person with write access to a repository who is responsible for reviewing contributions, making decisions, and keeping the project healthy.

### Merge
The act of combining changes from one branch into another. When a PR is merged, the changes become part of the base branch.

### Merge Conflict
A situation where changes in different branches modify the same part of the same file, and Git cannot automatically reconcile them. Must be resolved manually.

### Merge Request (MR)
GitLab's term for a Pull Request. Functionally identical.

### Milestone
A way to group issues and PRs that are part of a specific release or objective.

## O

### Open Source
Software whose source code is publicly available and can be viewed, used, modified, and distributed by anyone, subject to the terms of its license.

### Open Source Initiative (OSI)
The organization that maintains the Open Source Definition and approves licenses as compliant with it.

### Origin
The default name Git gives to the remote repository you cloned from. In the fork-and-pull workflow, this is your fork.

### Upstream
The original repository from which a fork was created. You pull the latest changes from upstream and submit PRs to it.

## P

### PR / Pull Request
A proposal to merge changes from one branch into another. The primary mechanism for contributing to open source projects on GitHub.

### PR Template
A pre-formatted document that auto-populates when you create a new PR, ensuring you include all required information.

### Push
Sending your local commits to a remote repository (like GitHub). Done with `git push`.

## R

### Rebase
Re-applying your commits on top of another branch's latest commits. Creates a linear history but rewrites commit hashes.

### Refactor
Restructuring existing code without changing its external behavior. Done to improve readability, reduce complexity, or eliminate duplication.

### Remote
A version of your repository hosted on a server (like GitHub). You can have multiple remotes: `origin` (your fork) and `upstream` (the original).

### Repository (Repo)
A storage location for a project, including all its files, history, and metadata. Hosted on platforms like GitHub, GitLab, or Bitbucket.

### Resolve Conversation
A GitHub feature that lets you mark a review comment as "resolved" after it's been addressed. Helps reviewers track which feedback has been handled.

### Review
The process of examining a Pull Request's code. Reviews can result in approval, a request for changes, or comments.

### Reviewer
The person examining and providing feedback on a Pull Request.

## S

### Squash
Combining multiple commits into a single commit. Often used to clean up a PR's history before merging.

### Stale
A PR or issue that has had no activity for a long time. Some projects automatically close stale items.

### Status Check
An automated test or validation that runs on a PR. GitHub shows the results (pass/fail) on the PR page.

### Suggested Change
A GitHub feature that allows reviewers to propose specific code changes within a comment. The author can commit the suggestion with one click.

## T

### Tag
A label applied to a specific commit, often used to mark release versions (e.g., `v1.0.0`). Also used for categorizing issues and PRs.

### Travis CI / GitHub Actions
CI/CD platforms that run automated checks on PRs. GitHub Actions is the most common for projects hosted on GitHub.

### Triaging
The process of reviewing, categorizing, and prioritizing issues and PRs. Includes confirming bugs, adding labels, and assigning reviewers.

## U

### Upstream
The original repository from which your fork was created. You pull updates from upstream and submit PRs to it.

---

**Previous:** [[Pre-PR Checklist]]
**Next:** [[Home]]
