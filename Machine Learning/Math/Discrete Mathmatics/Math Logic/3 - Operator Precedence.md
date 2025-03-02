I'll create a comprehensive Obsidian note focusing on implications in propositional logic with numerous examples.
[[Operator Precedence 3]]
# Logical Implication ($\Rightarrow$) in Propositional Logic

## Basic Definition

>[!info] Definition
>The implication $p \Rightarrow q$ is read as "if $p$ then $q$" or "$p$ implies $q$"
>
>Truth table for $p \Rightarrow q$:
>```
>| p | q | p ⇒ q |
>|---|---|-------|
>| T | T |   T   |
>| T | F |   F   |
>| F | T |   T   |
>| F | F |   T   |
>```

## Simple Examples

### Example 1: Direct Implication
>[!example] $p \Rightarrow q$
>"If it rains $(p)$, then the ground is wet $(q)$"
>
>For $(p = true, q = false)$:
>- It's raining but the ground isn't wet
>- This makes the implication false

### Example 2: Negated Antecedent
>[!example] $\neg p \Rightarrow q$
>"If it's not sunny $(¬p)$, then we'll stay inside $(q)$"
>
>For $(p = true, q = false)$:
>1. First: $\neg true = false$
>2. Then: $false \Rightarrow false = true$

## Complex Implications

### Example 3: Chained Implications
>[!example] $p \Rightarrow q \Rightarrow r$
>This is interpreted as $p \Rightarrow (q \Rightarrow r)$
>
>Complete evaluation table:
>```
>| p | q | r | q ⇒ r | p ⇒ (q ⇒ r) |
>|---|---|---|--------|--------------|
>| T | T | T |   T    |      T       |
>| T | T | F |   F    |      F       |
>| T | F | T |   T    |      T       |
>| T | F | F |   T    |      T       |
>| F | T | T |   T    |      T       |
>| F | T | F |   F    |      T       |
>| F | F | T |   T    |      T       |
>| F | F | F |   T    |      T       |
>```

### Example 4: Compound Antecedent
>[!example] $(p \land q) \Rightarrow r$
>"If it's raining $(p)$ AND cold $(q)$, then we'll stay inside $(r)$"
>
>For $(p = true, q = true, r = false)$:
>1. First: $true \land true = true$
>2. Then: $true \Rightarrow false = false$

### Example 5: Compound Consequent
>[!example] $p \Rightarrow (q \lor r)$
>"If it's hot $(p)$, then we'll go swimming $(q)$ OR get ice cream $(r)$"
>
>For $(p = true, q = false, r = true)$:
>1. First: $false \lor true = true$
>2. Then: $true \Rightarrow true = true$

## Advanced Implications

### Example 6: Mixed Operators
>[!example] $\neg p \land q \Rightarrow r \lor s$
>Evaluation order:
>1. $\neg p$ (negation first)
>2. $\neg p \land q$ (conjunction)
>3. $r \lor s$ (disjunction)
>4. Final implication

### Example 7: Nested Implications
>[!example] $p \Rightarrow (q \Rightarrow (r \Rightarrow s))$
>For $(p = true, q = true, r = true, s = false)$:
>1. Innermost: $r \Rightarrow s = false$
>2. Middle: $q \Rightarrow false = false$
>3. Outermost: $p \Rightarrow false = false$

## Special Cases

### Example 8: Vacuous Truth
>[!example] False Antecedent Cases
>When $p$ is false, $p \Rightarrow q$ is always true
>
>This explains why:
>- $false \Rightarrow true = true$
>- $false \Rightarrow false = true$

### Example 9: Double Implication
>[!example] $(p \Rightarrow q) \Rightarrow r$
>Different from $p \Rightarrow (q \Rightarrow r)$
>
>Truth table comparison:
>```
>| p | q | r | p⇒q | (p⇒q)⇒r | p⇒(q⇒r) |
>|---|---|---|-----|----------|-----------|
>| T | T | T |  T  |    T     |     T     |
>| T | T | F |  T  |    F     |     F     |
>| T | F | T |  F  |    T     |     T     |
>| T | F | F |  F  |    T     |     T     |
>| F | T | T |  T  |    T     |     T     |
>| F | T | F |  T  |    F     |     T     |
>| F | F | T |  T  |    T     |     T     |
>| F | F | F |  T  |    F     |     T     |
>```

## Common Logical Equivalences with Implications

>[!note] Important Equivalences
>1. $p \Rightarrow q \equiv \neg p \lor q$
>2. $\neg(p \Rightarrow q) \equiv p \land \neg q$
>3. $(p \Rightarrow q) \land (q \Rightarrow r) \equiv p \Rightarrow r$ (transitivity)

## Practice Problems

>[!example] Evaluate These
>1. $(p \land q) \Rightarrow (p \lor r)$
>2. $p \Rightarrow (q \Rightarrow p)$
>3. $(\neg p \Rightarrow q) \Rightarrow p$
>4. $(p \Rightarrow q) \land (p \Rightarrow \neg q)$

Would you like solutions to these practice problems or more examples of any particular type of implication?