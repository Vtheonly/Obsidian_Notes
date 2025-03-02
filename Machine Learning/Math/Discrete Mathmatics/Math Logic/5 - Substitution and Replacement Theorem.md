[[Substitution and Replacement Theorem]]

## 1.3.1 Substitution

### Definition 1.3.1: Substitution
A substitution (or uniform substitution) associates a formula A with a propositional variable p. It is denoted as [p\A]. When applied to a formula B, denoted as (B)[p\A], it simultaneously replaces all occurrences of p with A in formula B.

#### Example 1.3.1
Given:
- Formula B ≡ (x ∧ y ⇒ z)
- Formula A ≡ (p ∨ q)

The substitution of y with A applied to B:
```
(B)[y\A] ≡ x ∧ (p ∨ q) ⇒ z
```

## 1.3.2 Replacement Theorem

### Theorem 1.3.1: Replacement Theorem
If F is a propositional formula containing variables x₁, x₂, ..., xₙ and E₁, E₂, ..., Eₙ are any propositional formulas:
> If F is a tautology, then the propositional formula E obtained by replacing occurrences of xᵢ (i ≤ n) with Eᵢ respectively is also a tautology.

#### Example 1.3.2
Given:
- F ≡ p ⇒ (q ⇒ p) is a tautology
- E₁ ≡ x ∨ y
- E₂ ≡ y ⇒ z

The resulting formula E:
```
E ≡ [E₁/p][E₂/q] ≡ (x ∨ y) ⇒ ((y ⇒ z) ⇒ (x ∨ y))
```

### Proposition 1.3.2: Duality
For a propositional formula A containing only ∧, ∨, ¬ connectors:
> Let A* be the propositional formula obtained by:
> 1. Interchanging ∧ and ∨ connectors
> 2. Replacing each variable p with its negation (¬p)
> 
> Then A* is logically equivalent to ¬A

---
