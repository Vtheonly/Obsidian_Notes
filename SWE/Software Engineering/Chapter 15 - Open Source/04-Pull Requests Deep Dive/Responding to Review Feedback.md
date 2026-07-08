---
tags: [pull-requests, feedback, communication]
aliases: [Handling Reviews, PR Feedback, Code Review Response]
---

# Responding to Review Feedback

Receiving feedback on your code can feel personal, especially when you're new. But code review is one of the most valuable parts of the open source process — it's how you learn, how the project maintains quality, and how trust is built between contributors. This note teaches you how to handle feedback gracefully and effectively.

## The Mindset Shift

### Code Review Is Not About You

When a reviewer suggests a change, they are commenting on **the code**, not on **you as a developer**. This distinction is crucial:

-  "They think I'm a bad programmer."
-  "They see something in the code that could be improved."

Even the most experienced developers receive feedback on their PRs. In fact, senior developers at companies like Google and Meta go through multiple rounds of review on every change. Feedback is not a sign of incompetence — it's a sign of a healthy review process.

### Feedback Is a Gift

Every piece of feedback is free mentorship. Someone with more experience in the codebase is taking the time to help you improve your code. This kind of personalized instruction would cost hundreds of dollars per hour if you hired a private tutor. In open source, it's free.

## How to Read Review Comments

### Categorize the Feedback

Not all feedback is the same. Understanding the type helps you respond appropriately:

| Type | Example | How to Respond |
|------|---------|---------------|
| **Critical fix** | "This has a SQL injection vulnerability" | Fix immediately — no debate |
| **Functional issue** | "This doesn't handle the case where the list is empty" | Fix — this is a real bug |
| **Style/convention** | "We use camelCase for variable names in this project" | Fix — follow the project's conventions |
| **Performance** | "This loop runs in O(n²), consider using a hash map" | Usually fix — but can discuss alternatives |
| **Design suggestion** | "Have you considered using the observer pattern here?" | Discuss — explain your reasoning, be open to alternatives |
| **Nit/minor** | "Extra blank line here" or "Typo in variable name" | Fix — it's trivial and shows attention to detail |
| **Question** | "Why did you use recursion here instead of iteration?" | Answer — the reviewer wants to understand your thinking |
| **Praise** | "Great approach!" or "This is really clean" | Appreciate — you earned it! |

### Don't Take It Personally

Common reactions to avoid:

-  "They're just being picky." → They're helping you match the project's standards.
-  "I'm not cut out for this." → Every contributor gets feedback. It's how you grow.
-  "I'll just do what they say without understanding." → Ask questions if you don't understand the "why."
-  "My way is better." → It might be, but explain your reasoning rather than being dismissive.

## How to Respond

### Step 1: Read All Comments First

Before responding to any comment, read through **all** the feedback. This gives you the full picture and prevents you from addressing comments in isolation when they might be related.

### Step 2: Acknowledge and Thank

Always start by thanking the reviewer for their time:

```markdown
Thanks for the thorough review! I'll address all the points.
```

### Step 3: Address Each Comment

For each piece of feedback, respond in one of these ways:

**When you agree and will fix it:**
```markdown
Good catch! Fixed in abc1234.
```
(Reference the commit hash where you made the fix)

**When you agree but want to discuss the approach:**
```markdown
I agree this needs to be fixed. I was considering [approach A], but your suggestion of [approach B] is cleaner. I'll implement it that way.
```

**When you disagree (respectfully):**
```markdown
I see your point, but I chose this approach because [reason]. Would [alternative compromise] work for you? Happy to change if you still prefer your suggestion.
```

**When you don't understand:**
```markdown
Could you elaborate on this? I'm not sure I understand what you mean by [specific part]. An example would be really helpful!
```

**When a suggestion is out of scope:**
```markdown
That's a great idea, but I think it's beyond the scope of this PR which focuses on [specific fix]. I can open a follow-up issue for that improvement if you'd like.
```

### Step 4: Make the Changes

After addressing all comments in writing, make the actual code changes:

```bash
# Make your changes locally
# ...

# Stage and commit
git add .
git commit -m "fix: address review feedback - handle empty input case"

# Push to the same branch
git push origin fix/my-branch
```

> [!important] Push to the Same Branch
> Do NOT close your PR and open a new one. Just push new commits to the same branch. The PR will automatically update with your new changes.

### Step 5: Confirm All Feedback Is Addressed

After pushing, leave a comment on the PR:

```markdown
I've addressed all the feedback:
-  Added empty input handling (comment 1)
-  Renamed function to be more descriptive (comment 2)  
-  Added test for timeout case (comment 3)

Ready for another look when you have time!
```

## Handling Specific Situations

### When Multiple Reviewers Disagree

Sometimes two reviewers give conflicting suggestions. In this case:

1. Acknowledge both perspectives
2. Ask which approach the maintainers prefer
3. Follow the maintainer's direction

```markdown
@reviewer1 suggests approach A, and @reviewer2 suggests approach B. Both seem valid — @maintainer, do you have a preference?
```

### When Feedback Is Unclear

If a comment is vague ("This could be better"), ask for specifics:

```markdown
Could you clarify what you'd like to see improved? Are you suggesting a different algorithm, better naming, or something else? A brief example would be really helpful.
```

### When You Disagree Strongly

It's okay to disagree, but do so with respect and reasoning:

```markdown
I understand the concern, but I'd like to push back on this suggestion because:
1. The current approach is consistent with how [other part of the codebase] handles this
2. The suggested change would add [specific complexity] that doesn't seem warranted for this use case
3. The performance impact would be [specific impact]

That said, I'm happy to change it if you feel strongly. Just want to make sure we've considered the tradeoffs.
```

### When Review Is Taking Too Long

If you haven't received feedback after a week:

```markdown
Hi! Just bumping this PR. I know everyone's busy — no rush, but I wanted to make sure it's still on your radar. Happy to make any changes needed.
```

### When You're Overwhelmed by Feedback

If you receive a large number of comments:

1. Don't panic — it's not unusual for complex PRs
2. Tackle the most critical issues first (security, correctness)
3. Then address style/convention issues
4. Finally, handle nits and minor suggestions
5. Take breaks between addressing comments
6. Ask for help if you're stuck on a specific piece of feedback

## What NOT to Do

|  Don't |  Instead |
|----------|-----------|
| Ignore feedback you disagree with | Respond respectfully with your reasoning |
| Get defensive or argue | Consider the feedback objectively |
| Delete and resubmit the PR | Push new commits to the same branch |
| Mark comments as resolved without fixing them | Fix the issue, then mark as resolved |
| Ghost the PR (stop responding) | Communicate if you need more time |
| Make changes without commenting | Explain what you changed and why |
| Respond emotionally | Take a break before responding |

## The Emotional Reality

It's normal to feel a sting when someone critiques your code, especially the first few times. Here are some perspective shifts that help:

- **Your code is not your identity.** A suggestion to change your code is not a suggestion to change you.
- **The reviewer invested time to help you.** They could have just ignored your PR. Their feedback means they care enough to engage.
- **Every PR improvement makes you a better developer.** Each piece of feedback teaches you something you didn't know before.
- **The best code is the code that gets merged.** If incorporating feedback gets your code merged, that's a win.

---

**Previous:** [[Code Review Process]]
**Next:** [[Updating a PR]]
