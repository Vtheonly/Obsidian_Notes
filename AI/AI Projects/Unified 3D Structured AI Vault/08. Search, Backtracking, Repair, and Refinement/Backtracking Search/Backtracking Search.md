---
tags: [repair, backtracking]
---

# Backtracking Search

> **Definition.** *Backtracking search* explores the space of structured outputs by partial construction, abandoning a partial output as soon as it violates a constraint.

## Algorithm

```
def backtrack(partial):
    if complete(partial):
        return partial
    for action in next_actions(partial):
        new_partial = apply(partial, action)
        if consistent(new_partial):  # local check
            result = backtrack(new_partial)
            if result is not None:
                return result
        # else: backtrack (try next action)
    return None
```

## Properties

- **Complete**: if a solution exists, backtracking finds it (given enough time).
- **Sound**: any returned solution satisfies all constraints.
- **Exponential**: in the worst case.

## Optimizations

- **Constraint propagation**: prune actions that cannot lead to a solution.
- **Forward checking**: check constraints early, not just at completion.
- **Heuristic ordering**: try most-constrained actions first.
- **Memoization**: cache failed partial states.

## Use in Structured Generation

- **Constraint satisfaction problems** (CSPs).
- **Parse tree generation** with grammar constraints.
- **Layout generation** with spatial constraints.
- **BIM generation** with geometric and topological constraints.

## Comparison to Beam Search

| Approach          | Memory           | Optimality            | Use case                          |
| ----------------- | ---------------- | --------------------- | --------------------------------- |
| Backtracking      | Linear in depth  | Optimal (if complete) | When correctness is critical.     |
| Beam search       | Linear in beam   | Approximate           | When speed and diversity matter.  |

See [[Tree Search and Beam Search]], [[Generate Validate Repair]].

## Related Concepts

- [[Tree Search and Beam Search]]
- [[Generate Validate Repair]]
- [[Iterative Refinement]]
