[[Operator Precedence 1]]

# Logical Connectives and Propositional Logic

## Operator Precedence (Priorité des connecteurs)

In propositional logic, operators follow a strict precedence order (from highest to lowest):

1. $\neg$ (NOT/négation)
2. $\land$ (AND/et)
3. $\lor$ (OR/ou)
4. $\Rightarrow$ (IMPLIES/implique)
5. $\Leftrightarrow$ (EQUIVALENT/équivalent)

>[!example] Example
>The formula $p \lor q \Rightarrow r$ is evaluated as $(p \lor q) \Rightarrow r$ because $\lor$ has higher precedence than $\Rightarrow$
>
>For values $(p = true, q = true, r = false)$:
>1. First evaluate $p \lor q = true$
>2. Then evaluate $true \Rightarrow false = false$

## Propositional Formulas (Formules Propositionnelles)

### Definition (Définition 1.1.1)

A propositional formula is defined inductively as follows:

1. **Base Case**: Propositional variables ($p, q, r, ...$) are propositional formulas
2. **Negation**: If $p$ is a propositional formula, then $\neg p$ is a propositional formula
3. **Binary Operators**: If $p$ and $q$ are propositional formulas, then:
   - $p \land q$ (conjunction)
   - $p \lor q$ (disjunction)
   - $p \Rightarrow q$ (implication)
   - $p \Leftrightarrow q$ (equivalence)
   are all propositional formulas
4. **Closure**: All propositional formulas are constructed using rules 1-3

## Syntax Trees (Arbres syntaxiques)

Propositional formulas can be represented as binary trees where:
- Internal nodes = logical connectives
- Leaf nodes = atomic propositions (variables)

>[!example] Example Tree
>The formula $(x \land (y \lor \neg z))$ can be represented as:
>```mermaid
>graph TD
>    A[∧] --> B[x]
>    A --> C[∨]
>    C --> D[y]
>    C --> E[¬]
>    E --> F[z]
>```

### Uses of Syntax Trees
1. Machine representation of formulas
2. Unique decomposition of propositional formulas
3. Foundation for formula manipulation algorithms
4. Basis for reasoning about formulas

>[!note] Parentheses Usage
>While operator precedence helps reduce parentheses, they cannot be completely eliminated. For example:
>- $(p \lor q) \Rightarrow r$ is different from $p \lor (q \Rightarrow r)$
>- Parentheses are needed when we want to override the natural operator precedence

Would you like me to elaborate on any particular aspect or add more examples?