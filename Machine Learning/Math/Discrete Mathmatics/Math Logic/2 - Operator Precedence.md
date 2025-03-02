I'll create a detailed Obsidian note with multiple examples of operator precedence evaluation in propositional logic.
[[Operator Precedence 2]]
# Operator Precedence in Propositional Logic: Examples

## Precedence Rules Reminder

>[!info] Operator Precedence (Highest to Lowest)
>1. $\neg$ (NOT)
>2. $\land$ (AND)
>3. $\lor$ (OR)
>4. $\Rightarrow$ (IMPLIES)
>5. $\Leftrightarrow$ (EQUIVALENT)

## Basic Examples

### Example 1: $\neg p \land q$
>[!example] Evaluation Steps
>This is interpreted as $(\neg p) \land q$ (not as $\neg(p \land q)$)
>
>For $(p = true, q = true)$:
>1. First: $\neg true = false$
>2. Then: $false \land true = false$

### Example 2: $p \lor q \land r$
>[!example] Evaluation Steps
>This is interpreted as $p \lor (q \land r)$ (not as $(p \lor q) \land r$)
>
>For $(p = true, q = true, r = false)$:
>1. First: $q \land r = true \land false = false$
>2. Then: $true \lor false = true$

## Complex Examples

### Example 3: $\neg p \lor q \Rightarrow r$
>[!example] Evaluation Steps
>This is evaluated as $((\neg p) \lor q) \Rightarrow r$
>
>For $(p = false, q = true, r = false)$:
>1. First: $\neg false = true$
>2. Then: $true \lor true = true$
>3. Finally: $true \Rightarrow false = false$

### Example 4: $p \land q \lor \neg r \Rightarrow s$
>[!example] Evaluation Steps
>This is evaluated as $((p \land q) \lor (\neg r)) \Rightarrow s$
>
>For $(p = true, q = false, r = true, s = false)$:
>1. First: $\neg true = false$
>2. Then: $true \land false = false$
>3. Then: $false \lor false = false$
>4. Finally: $false \Rightarrow false = true$

## Tricky Cases

### Example 5: $\neg p \land q \lor r$
>[!example] Two Different Interpretations
>1. $((\neg p) \land q) \lor r$ (correct by precedence)
>2. $(\neg p) \land (q \lor r)$ (if explicitly parenthesized)
>
>For $(p = true, q = true, r = false)$:
>1. Correct interpretation:
>   - $\neg true = false$
>   - $false \land true = false$
>   - $false \lor false = false$
>2. Alternative with parentheses:
>   - $\neg true = false$
>   - $true \lor false = true$
>   - $false \land true = false$

### Example 6: $p \Rightarrow q \Rightarrow r$
>[!example] Evaluation Steps
>This is typically interpreted as $p \Rightarrow (q \Rightarrow r)$ in most logical systems
>
>For $(p = true, q = true, r = false)$:
>1. First evaluate inner implication: $q \Rightarrow r = false$
>2. Then evaluate outer: $p \Rightarrow false = false$

## Truth Table Example

### Example 7: $\neg p \land q \lor r$
>[!note] Complete Truth Table
>```
>| p | q | r | ¬p | ¬p ∧ q | (¬p ∧ q) ∨ r |
>|---|---|---|----|--------|---------------|
>| T | T | T | F  | F      | T             |
>| T | T | F | F  | F      | F             |
>| T | F | T | F  | F      | T             |
>| T | F | F | F  | F      | F             |
>| F | T | T | T  | T      | T             |
>| F | T | F | T  | T      | T             |
>| F | F | T | T  | F      | T             |
>| F | F | F | T  | F      | F             |
>```

## Common Mistakes to Avoid

>[!warning] Common Pitfalls
>1. Forgetting that $\neg$ has highest precedence
>2. Assuming $\land$ and $\lor$ have equal precedence
>3. Confusing the order of evaluation in implications
>4. Not using parentheses when overriding natural precedence

## Practice Exercise

>[!example] Try These Examples
>Evaluate the following for $(p = true, q = false, r = true)$:
>1. $\neg p \land q \lor r$
>2. $p \Rightarrow \neg q \land r$
>3. $\neg(p \land q) \lor r$
>4. $(p \lor q) \land \neg r$
>
>Solutions:
>1. $false \land false \lor true = true$
>2. $true \Rightarrow (true \land true) = true$
>3. $\neg(false) \lor true = true$
>4. $(true \lor false) \land false = false$

Would you like me to add more examples or explain any of these in more detail?