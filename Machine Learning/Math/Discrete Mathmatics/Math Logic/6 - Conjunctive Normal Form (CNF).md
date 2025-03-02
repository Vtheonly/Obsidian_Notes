# 📚 Conjunctive Normal Form (CNF) - Complete Guide
[[Conjunctive Normal Form (CNF)]]
## 🎯 Introduction
Conjunctive Normal Form (CNF) is a standardized way to represent complex propositional formulas. It's particularly useful when:
- Dealing with complex formulas where truth tables would be too cumbersome
- Performing automated theorem proving
- Simplifying logical analysis

CNF uses only three logical operators:
- Conjunctions (∧)
- Disjunctions (∨)
- Negations (¬)

## 🔍 Core Concepts

### 📌 Basic Notation

| Symbol | Meaning | Description |
|--------|---------|-------------|
| [X₁, X₂, ..., Xₙ] | Disjunction | X₁ ∨ X₂ ∨ ... ∨ Xₙ (OR) |
| ⟨X₁, X₂, ..., Xₙ⟩ | Conjunction | X₁ ∧ X₂ ∧ ... ∧ Xₙ (AND) |
| ¬X | Negation | NOT X |

### 📌 Key Definitions

#### Literal
A **literal** is either:
- A propositional variable (p, q, r, etc.)
- The negation of a propositional variable (¬p, ¬q, ¬r, etc.)

#### Clause
A **clause** is:
- A disjunction of literals: [X₁, X₂, ..., Xₙ]
- Example: [p, ¬q, r] represents p ∨ ¬q ∨ r

#### CNF Formula
A formula in CNF is:
- A conjunction of clauses: ⟨C₁, C₂, ..., Cₙ⟩
- Each Cᵢ is a clause
- Example: ⟨[p, q], [¬p, r]⟩ represents (p ∨ q) ∧ (¬p ∨ r)

## 🧮 Formula Classification

### α-Formulas (Conjunctive Type)

| Formula | Component 1 | Component 2 |
|---------|------------|-------------|
| x ∧ y | x | y |
| ¬(x ∨ y) | ¬x | ¬y |
| ¬(x ⇒ y) | x | ¬y |

### β-Formulas (Disjunctive Type)

| Formula | Component 1 | Component 2 |
|---------|------------|-------------|
| x ∨ y | x | y |
| ¬(x ∧ y) | ¬x | ¬y |
| x ⇒ y | ¬x | y |

## 🔄 CNF Conversion Algorithm

### Step-by-Step Process
1. Start with ⟨[F]⟩ where F is the original formula
2. Eliminate outer conjunctions
3. While the formula is not in CNF:
   - Choose a subformula Di
   - If Di is ¬¬Z, replace with Z
   - If Di is a β-formula, replace with [β₁, β₂]
   - If Di is an α-formula, create two copies with α₁ and α₂

### Conversion Rules
- Double negation: ¬¬Z → Z
- β-formula replacement: β → [β₁, β₂]
- α-formula duplication: α → α₁ and α₂
- and by duplication  means that you gotta do it in all clause like "NECHR"

![[flowchart - 1.png]]
## 📝 Examples

### Example 1: F₁ ≡ (p ⇒ ¬(p ⇒ q))
Step-by-step conversion:
1. ⟨[F₁]⟩ ≡ ⟨[p ⇒ ¬(p ⇒ q)]⟩
2. ≡ ⟨[¬p, ¬(p ⇒ q)]⟩
3. ≡ ⟨[¬p, p], [¬p, ¬q]⟩
**Final result**: F₁ ≡ (¬p ∨ p) ∧ (¬p ∨ ¬q)

### Example 2: F₂ ≡ ((q ∨ p) ∧ (¬p ⇒ ¬q))
Step-by-step conversion:
1. ⟨[F₂]⟩
2. ≡ ⟨[q ∨ p], [¬p ⇒ ¬q]⟩
3. ≡ ⟨[q, p], [¬¬p, ¬q]⟩
4. ≡ ⟨[q, p], [p, ¬q]⟩
**Final result**: F₂ ≡ (q ∨ p) ∧ (p ∨ ¬q)

### Example 3: F₃ ≡ (¬(p ∨ q) ⇒ r) ∧ s
Step-by-step conversion:
1. Rewrite implication: ¬(p ∨ q) ⇒ r becomes (p ∨ q ∨ r)
2. Combine with s
**Final result**: (p ∨ q ∨ r) ∧ s

## 💡 Important Properties

### Evaluation Rules
- A disjunction [X₁, X₂, ..., Xₙ] is true if at least one Xᵢ is true
- A conjunction ⟨X₁, X₂, ..., Xₙ⟩ is true if all Xᵢ are true

### Key Benefits
1. Standardized representation
2. Easier to process algorithmically
3. Useful for automated theorem proving
4. Simplifies certain logical operations

## ⚠️ Common Pitfalls to Avoid
1. Forgetting to eliminate double negations
2. Incorrectly classifying α and β formulas
3. Missing outer conjunctions
4. Incorrect handling of implications
5. Not maintaining logical equivalence during transformations

## 🎯 Best Practices
1. Identify formula type (α or β) before transformations
2. Handle negations first when possible
3. Work from the outside in
4. Keep careful track of parentheses and scope
5. Verify logical equivalence at each step

---
*Tags: #logic #propositional-logic #normal-forms #cnf #computer-science*