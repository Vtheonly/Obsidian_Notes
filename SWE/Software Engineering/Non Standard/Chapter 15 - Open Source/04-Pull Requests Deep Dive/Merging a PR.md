---
tags: [pull-requests, merging, completion]
aliases: [Merge PR, PR Merge, Merge Strategies]
---

# How a PR Is Merged

The moment your PR is merged is the moment your contribution officially becomes part of the project. Your code is now running for every user of that software. This note covers the different merge strategies, what happens after merge, and what you should do next.

## Prerequisites for Merging

Before a PR can be merged, it typically needs to satisfy all of these conditions:

| Requirement | Description |
|------------|-------------|
|  CI checks pass | All automated tests, linters, and builds succeed |
|  Required approvals | The minimum number of reviewers have approved (usually 1-2) |
|  No unresolved conversations | All review comments have been addressed or resolved |
|  No merge conflicts | The branch can be cleanly integrated into the base |
|  Branch is up to date | The branch includes all changes from the base branch |
|  CLA/DCO signed | If the project requires it, you've signed the agreement |

Some projects also have:
- **Required status checks** — Specific CI jobs that must pass
- **Required reviewers** — Specific people who must approve
- **Conversation resolution** — All conversations must be marked as resolved

## Merge Strategies

GitHub offers three merge strategies. The project maintainers choose which one to use:

### 1. Create a Merge Commit

```
git merge --no-ff fix/my-branch
```

This creates a merge commit that preserves the complete branch history. The resulting history shows both the individual commits and the merge point.

**Result:**
```
*   abc1234 Merge pull request #42 from you/fix/my-branch
|\  
| * def5678 fix: resolve redirect loop
| * ghi9012 fix: add tests for redirect
|/  
* jkl3456 some other commit on main
```

**Pros:** Complete history, easy to revert the entire PR as one unit.  
**Cons:** History can become cluttered with many small commits.

### 2. Squash and Merge

```
git merge --squash fix/my-branch
git commit -m "fix: resolve redirect loop (#42)"
```

This combines all commits from the PR into a single commit on the base branch.

**Result:**
```
* abc1234 fix: resolve redirect loop (#42)
* jkl3456 some other commit on main
```

**Pros:** Clean, linear history. Each PR is a single commit.  
**Cons:** Loses the individual commit history and the review discussion context in the Git log.

### 3. Rebase and Merge

```
git rebase fix/my-branch
```

This replays each commit from the PR onto the base branch, creating a linear history without a merge commit.

**Result:**
```
* abc1234 fix: add tests for redirect
* def5678 fix: resolve redirect loop
* ghi9012 some other commit on main
```

**Pros:** Linear history, preserves individual commits.  
**Cons:** Commits are re-created with new hashes, which can confuse anyone who has the original branch checked out.

### Which Strategy Do Projects Use?

| Strategy | Common In |
|----------|----------|
| Merge commit | Projects that value complete history (Linux kernel, Git itself) |
| Squash and merge | Most common for open source projects — keeps history clean |
| Rebase and merge | Projects that want linear history + individual commits |

> [!note] You Don't Choose the Merge Strategy
> The maintainer decides how to merge. You don't need to worry about this — just make sure your commits are well-organized and your PR description is clear. Some projects will ask you to squash your commits before they merge; they'll tell you if that's the case.

## What Happens After Merge

### Immediately

1. **Your code is in the main branch** — It's now part of the official codebase
2. **GitHub closes the PR** — The PR status changes to "Merged" (purple)
3. **Linked issues close** — If your PR description included "Fixes #123," that issue is automatically closed
4. **You get credit** — Your GitHub profile shows the contribution
5. **Notifications** — People watching the repo get notified

### Short-Term (Days)

1. **CI/CD runs** — The merge may trigger additional deployment or release pipelines
2. **Nightly builds** — If the project has nightly builds, your change is included
3. **Other contributors see your change** — They may build on it or comment on it

### Long-Term (Weeks to Months)

1. **Release** — Your change ships in the next version of the software
2. **Users benefit** — People using the software experience your improvement
3. **Follow-up changes** — Your change may inspire others to build on it

## After Your PR Is Merged

### 1. Celebrate! 

You did it. Your code is now part of a project used by real people. Take a moment to appreciate this — it's a significant milestone.

### 2. Clean Up Your Local Repository

```bash
# Switch back to main
git checkout main

# Pull the latest changes (including your merged PR)
git pull upstream main

# Delete your feature branch locally
git branch -d fix/my-branch

# Delete the remote branch on your fork
git push origin --delete fix/my-branch

# Keep your fork in sync
git push origin main
```

### 3. Update Your Fork

After your PR is merged, make sure your fork is up to date:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### 4. Reflect on the Experience

Ask yourself:
- What did I learn from the review feedback?
- What would I do differently next time?
- Was the project's workflow clear? What confused me?
- Do I want to contribute to this project again?

### 5. Look for Your Next Contribution

Now that you've completed the full workflow once, the second time is dramatically easier. Consider:
- Tackling a slightly more complex issue in the same project
- Contributing to a different project that interests you
- Helping other new contributors navigate the process

## The GitHub Contribution Graph

After your PR is merged, it appears on your GitHub contribution graph (the green squares on your profile). This provides visible proof of your open source activity, which is valuable for:

- **Job applications** — Employers often check GitHub profiles
- **Credibility** — Other contributors can see your track record
- **Motivation** — Watching your graph fill up is genuinely satisfying

> [!tip] Maintaining Your Fork
> After your PR is merged, your fork still exists on GitHub. Keep it around — you'll use it for future contributions. Just remember to sync it with the upstream repository before starting new work:
> ```bash
> git fetch upstream
> git checkout main
> git merge upstream/main
> ```

## Common Post-Merge Issues

### Your Change Needs a Follow-Up Fix

Sometimes bugs are discovered after merge. Don't worry — this happens to everyone. Open a new PR with the fix, referencing the original PR:

```markdown
Follow-up to #42 — the redirect fix introduced a regression when the session is null.
```

### The Maintainer Reverts Your Change

In rare cases, a maintainer may need to revert your change (usually because it caused an unforeseen issue). Don't take it personally. Reach out, understand the issue, and submit a new PR that addresses the problem.

### You Want to Add More Features

Great! But **don't reuse the same branch**. Create a new branch from the updated main:

```bash
git checkout main
git pull upstream main
git checkout -b feature/new-feature
```

---

**Previous:** [[Updating a PR]]
**Next:** [[Common PR Mistakes]]
