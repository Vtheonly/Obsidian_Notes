---
tags: [pull-requests, fundamentals, philosophy]
aliases: [Purpose of PRs, Why Use PRs]
---

# Why Pull Requests Exist

Pull Requests didn't always exist. In the early days of software development, anyone with access to the codebase could push changes directly. This worked for small teams but became catastrophic as projects grew. Understanding *why* PRs exist helps you appreciate the process and write better ones.

## The Problems PRs Solve

### 1. Preventing Bugs from Reaching Production

Without PRs, a developer can push buggy code directly to the main branch, and every user is immediately affected. PRs create a **checkpoint**: changes must be reviewed and tested before they reach anyone else.

**Real-world impact:** In 2014, a single direct push with an undetected bug broke the Node.js package manager (npm), causing thousands of builds to fail worldwide. This kind of incident is exactly what PRs prevent.

### 2. Knowledge Sharing

When code is reviewed through a PR, at least one other person reads and understands the change. This means:

- **Bus factor increases** — If the original author leaves, someone else understands the code.
- **Cross-pollination** — Reviewers learn about parts of the codebase they don't normally work on.
- **Mentorship** — Senior developers can guide junior contributors through review feedback.

### 3. Maintaining Code Quality

PRs enforce quality standards consistently:

- **Automated checks** (tests, linters, type checks) run on every PR
- **Human review** catches logical errors that automated tools miss
- **Style consistency** is maintained across hundreds of contributors
- **Architecture alignment** — Reviewers ensure changes fit the project's design philosophy

### 4. Creating a Record

Every PR is a permanent, searchable record of:

- What changed and why
- Who made the change
- What alternatives were considered
- What feedback was given
- When and how the change was approved

This historical record is invaluable for:

- **Debugging** — Understanding why a change was made months later
- **Onboarding** — New contributors can read past PRs to learn the codebase
- **Compliance** — Some industries require audit trails for all code changes
- **Accountability** — Every change has a clear author and reviewer

### 5. Facilitating Discussion

PRs provide a structured space for technical discussion. Instead of debating changes in Slack, email, or meetings, the conversation is embedded right next to the code. This means:

- Discussions are **contextual** — you see the exact code being discussed
- Conversations are **permanent** — future readers can understand the reasoning
- Decisions are **transparent** — everyone can see why a choice was made

## Why Developers Use PRs Instead of Direct Pushes

### The "Trust But Verify" Principle

Even the most experienced developers make mistakes. They forget edge cases, introduce typos, or overlook unintended consequences. Direct pushes bypass the verification step entirely. PRs ensure that **every change, no matter who makes it, is verified**.

This is why even project maintainers with full write access typically use PRs for their own non-trivial changes. It's not about distrust — it's about **collective quality assurance**.

### The Difference in Practice

**Without PRs (Direct Push):**
```
Developer writes code → Pushes to main → Bug reaches users → Panic
```

**With PRs:**
```
Developer writes code → Opens PR → Automated tests run → 
Human review → Issues caught → Code fixed → Merged → Users safe
```

### Why It Matters for Open Source

In open source, the stakes are even higher:

| Factor | Corporate Project | Open Source Project |
|--------|------------------|-------------------|
| Contributors | Known employees | Anyone on the internet |
| Trust level | Varies by role | Cannot assume trust |
| Code quality | Varies by team | Varies wildly |
| Motivation | Salary-aligned | Diverse and unknown |
| Impact scope | Controlled deployment | Potentially millions of users |

PRs are the gate that makes it safe for open source projects to accept contributions from strangers while maintaining quality.

## The Psychological Benefits

### For Contributors

- **Safety net** — You can propose changes without fear of breaking anything. If there's a problem, it'll be caught in review.
- **Learning opportunity** — Review feedback is personalized teaching from experienced developers.
- **Visibility** — Your contributions are documented and attributed to you.
- **Low pressure** — A PR is a proposal, not a demand. You're asking, not forcing.

### For Maintainers

- **Control** — They decide what enters their project.
- **Efficiency** — They can review changes on their schedule, not at the mercy of direct pushes.
- **Standards enforcement** — PR templates and CI checks ensure consistent quality.
- **Community building** — The review process is a conversation that builds relationships with contributors.

## What Would Happen Without PRs?

Imagine an open source project where anyone could push directly to the main branch:

1. **Within hours:** Someone would push a "fun" commit that breaks the build.
2. **Within days:** Well-intentioned but incompatible changes would conflict with each other.
3. **Within weeks:** The codebase would be an inconsistent mess of different coding styles and architectural approaches.
4. **Within months:** Users would abandon the project due to instability.

This isn't hypothetical — it's exactly what happened in the early days of open source before PR workflows became standard. Projects that allowed direct pushes consistently struggled with quality, while projects that enforced code review thrived.

## PRs as a Cultural Practice

PRs aren't just a technical mechanism — they're a cultural practice. They encode the values of:

- **Collaboration** over solo work
- **Transparency** over secrecy
- **Quality** over speed
- **Shared ownership** over individual control
- **Continuous improvement** over perfection

When you open a PR, you're not just submitting code. You're participating in a culture of shared responsibility and mutual respect.

---

**Previous:** [[What is a Pull Request]]
**Next:** [[PR Workflow]]
