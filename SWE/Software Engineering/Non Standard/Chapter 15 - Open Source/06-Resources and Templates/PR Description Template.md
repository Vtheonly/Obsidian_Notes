---
tags: [template, pull-requests, reference]
aliases: [PR Template, Pull Request Template]
---

# PR Description Template

Copy and adapt this template for your Pull Requests. A well-structured PR description makes reviews faster and increases the chance of your PR being merged.

## Standard Template

```markdown
## Summary
<!-- Brief description of what this PR does (1-3 sentences) -->

## Related Issue
<!-- Link to the issue this PR addresses -->
Fixes #

## Type of Change
<!-- Check the relevant option -->
- [ ]  Bug fix (non-breaking change that fixes an issue)
- [ ]  New feature (non-breaking change that adds functionality)
- [ ]  Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ]  Documentation update
- [ ]  Style/refactor (no functional changes)
- [ ]  Test addition/update
- [ ]  Chore (build, CI, tooling)

## Changes
<!-- List the specific changes made -->
-
-
-

## How to Test
<!-- Step-by-step instructions for the reviewer to verify your changes -->
1.
2.
3.

**Expected behavior:**

## Screenshots (if applicable)
<!-- Add before/after screenshots for UI changes -->
| Before | After |
|--------|-------|
| | |

## Checklist
- [ ] I have read the project's CONTRIBUTING.md
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation accordingly
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] Any dependent changes have been merged and published

## Additional Notes
<!-- Any context, tradeoffs, or alternatives considered -->
```

## Minimal Template (For Small PRs)

```markdown
## What
<!-- One sentence describing the change -->

## Why
<!-- One sentence explaining the motivation, or the issue number -->
Fixes #

## How to Verify
<!-- Quick verification step -->
```

## Bug Fix Template

```markdown
## Bug Description
<!-- What was the bug? -->

## Root Cause
<!-- What was causing the bug? -->

## Fix
<!-- How does this PR fix it? -->

## Issue
Fixes #

## Test Plan
- [ ] Reproduce the original bug (describe steps)
- [ ] Verify the fix resolves it
- [ ] Verify no regressions in related functionality
- [ ] Edge cases tested:
  -
  -

## Regression Risk
<!-- Could this fix break anything else? -->
```

## Feature Template

```markdown
## Feature Description
<!-- What does this feature do? -->

## Motivation
<!-- Why is this feature needed? -->

## Implementation
<!-- How does this feature work? Key design decisions. -->

## Issue
Closes #

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed
- [ ] Edge cases covered

## Documentation
- [ ] API documentation updated
- [ ] User guide updated
- [ ] Changelog entry added
- [ ] Migration guide needed? (for breaking changes)

## Screenshots / Demo
<!-- For UI features, show the result -->
```

## Documentation Template

```markdown
## What Changed
<!-- Which documentation was updated? -->

## Why
<!-- Why was the update needed? -->

## Issue (if applicable)
Fixes #

## Review Focus
<!-- What should the reviewer pay attention to? -->
- [ ] Technical accuracy
- [ ] Clarity and readability
- [ ] Completeness
- [ ] Code examples are correct and runnable
```

> [!tip] Always Check for a Project-Specific Template
> Many projects include a `.github/PULL_REQUEST_TEMPLATE.md` file that auto-populates when you open a PR. If the project provides one, use it instead of these generic templates. Following the project's format shows you respect their conventions.

---

**Previous:** [[Step-by-Step First Contribution]]
**Next:** [[Pre-PR Checklist]]
