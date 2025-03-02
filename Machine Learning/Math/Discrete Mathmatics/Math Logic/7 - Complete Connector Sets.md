# Propositional Logic & Complete Connector Sets
#logic #mathematics #connectors

## Overview
This note covers fundamental concepts in propositional logic, focusing on complete sets of connectors, interpretations, and validity of logical formulas.

## Complete Sets of Connectors
> [!definition] Definition
> A complete set of connectors is a set where any logical formula F can be expressed using an equivalent formula G containing only connectors from that set.

### Known Complete Sets
1. Basic Complete Sets:
   - {¬, ∧} (negation, conjunction)
   - {¬, ∨} (negation, disjunction)
   - {¬, ⇒} (negation, implication)

2. Special Complete Sets:
   - {|} (Sheffer stroke)
   - {↓} (NOR/Peirce arrow)

### Proof Examples
#### Example: Completeness of {¬, ∧}
To prove completeness, we can express other connectors using only ¬ and ∧:

| Original | Equivalent Expression |
|----------|---------------------|
| A ∨ B    | ¬(¬A ∧ ¬B)         |
| A ⇒ B    | ¬(A ∧ ¬B)          |

#### Example: Completeness of {|}
Express all basic connectors using only Sheffer stroke:

| Connector | Expression using \| |
|-----------|-------------------|
| ¬A        | A\|A              |
| A ∧ B     | (A\|B)\|(A\|B)    |
| A ∨ B     | (A\|A)\|(B\|B)    |
| A ⇒ B     | ((A\|A)\|B)\|((A\|A)\|B) |

### Truth Table for Special Operators
#### Sheffer Stroke (|) and NOR (↓)

| p   | q   | p↓q | p   |
| --- | --- | --- | --- |
| 0   | 0   | 1   | 1   |
| 0   | 1   | 0   | 1   |
| 1   | 0   | 0   | 1   |
| 1   | 1   | 0   | 0   |


## Interpretations & Models

> [!definition] Interpretation
> An interpretation (or valuation) is a function that assigns truth values (0 or 1) to propositional variables.
> - Notation: I: Vp → {0, 1}
> - Written as: {p₁ ↦ b₁, ..., pₙ ↦ bₙ}

### Key Concepts

> [!important] Model
> A model for a formula F is an interpretation I where I(F) = 1
> - Can exist for single formulas or sets of formulas
> - A set can have zero, one, or multiple models

### Formula Classifications

1. **Satisfiable Formula**
   - Has at least one model
   - Also called: consistent or non-contradictory

2. **Unsatisfiable Formula**
   - Has no models
   - Also called: inconsistent

3. **Valid Formula**
   - True under all interpretations
   - Every interpretation is a model

## Validity in Conjunctive Normal Form
Ah, let me explain it in that style!

> [!note] Understanding Validity in CNF
> The key insight is about "weak spots" in the formula:
> 
> 1. Remember, CNF means we have (stuff1) AND (stuff2) AND (stuff3)...
> 
> 2. For it to be VALID, it needs to be TRUE no matter what values we give it
> 
> 3. The "weak spot" idea:
>    - If ANY clause has only independent literals (like p ∨ q ∨ r)
>    - We can make that clause FALSE by setting all its variables to FALSE
>    - Then the whole formula becomes FALSE
>    - Therefore NOT valid!
> 
> 4. The only way to prevent "weak spots":
>    - Every clause MUST have a pair like (p and ¬p)
>    - Because p ∨ ¬p is ALWAYS TRUE
>    - Can't break it, no matter what value you try!
>    - No weak spots = Valid formula

Think of it like a chain - if even ONE link (clause) can be broken (made false), then the whole chain (formula) isn't unbreakable (valid). The only way to make each link unbreakable is to include a contradictory pair in each one!



## Common Pitfalls and Tips

> [!warning] Common Mistakes
> 1. Confusing completeness with validity
> 2. Assuming all interpretations are models
> 3. Mixing up satisfiability and validity
> 4. Forgetting to check all possible interpretations

> [!tip] Study Tips
> 1. Practice converting between different connector sets
> 2. Create truth tables to verify equivalences
> 3. Start with simple formulas before complex ones
> 4. Use systematic approach for finding models

## Practice Exercises
1. Prove that {↓} is a complete set of connectors
2. Find all models for: (p ⇒ q) ∧ (q ⇒ r)
3. Convert (p ⇒ q) ∨ r using only {¬, ∧}
