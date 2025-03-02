[[ Propositional Logic]]

Propositional logic deals with propositions and the relationships between them. At this stage of the course, we cannot define "proposition" precisely. However, we can think of a proposition as a possible situation or condition that can be either true or false. For example, "it is raining," or "the sky is cloudy." Importantly, the condition does not have to be satisfied for it to qualify as a proposition; in other words, a proposition does not need to be true.

In this chapter, we first cover the syntactic rules that define expressions in propositional logic. We then explore the semantics of these expressions. Based on this semantic framework, we will discuss evaluation, satisfaction, and various properties of these expressions.

---

## 1.1 Syntax of Propositional Logic

In propositional logic, there are two types of statements: simple statements, called atoms, and complex statements. Simple statements express basic facts about the world, while complex statements express logical relationships between simple statements.

### Simple Statements
Simple statements, or atomic propositions, are expressed using constants composed of letters, numbers, and underscores. They must always start with a lowercase letter. Examples of simple propositions include:

- $p$
- $\text{pleuvoir23}$
- $\text{pleuvoir\_ou\_neiger}$

### Complex Statements
Complex statements are built from simpler ones using logical connectors. There are five types of logical connectors in propositional logic: negation, conjunction, disjunction, implication, and equivalence.

---

## 1.1.1 Logical Connectors

### Negation
Negation is represented by the operator $\neg$ followed by a simple or complex statement. The negation of a proposition $p$ is written as $\neg p$. The rule for negation is straightforward:

- If $p$ is true, then $\neg p$ is false.
- If $p$ is false, then $\neg p$ is true.

**Truth Table for Negation:**

| $p$ | $\neg p$ |
| --- | --- |
| V   | F   |
| F   | V   |

---

### Conjunction
Conjunction connects two statements with the operator $\land$, which means "and." A conjunction of $p$ and $q$ is written as $p \land q$. The expression $p \land q$ is true only when both $p$ and $q$ are true. It is false in all other cases.

**Truth Table for Conjunction:**

| $p$ | $q$ | $p \land q$ |
| --- | --- | --- |
| V   | V   | V   |
| V   | F   | F   |
| F   | V   | F   |
| F   | F   | F   |

---

### Disjunction
Disjunction connects two statements with the operator $\lor$, which means "or." A disjunction of $p$ and $q$ is written as $p \lor q$. In natural language, it means "p or q," and it is true when at least one of $p$ or $q$ is true. The only case where $p \lor q$ is false is when both $p$ and $q$ are false.

**Truth Table for Disjunction:**

| $p$ | $q$ | $p \lor q$ |
| --- | --- | --- |
| V   | V   | V   |
| V   | F   | V   |
| F   | V   | V   |
| F   | F   | F   |

---

### Implication
Implication is formed by pairing two statements with the operator $\Rightarrow$, which means "if...then." The statement on the left of the operator is called the antecedent, and the one on the right is the consequence. The implication $p \Rightarrow q$ translates to "if $p$ then $q$." The only case where $p \Rightarrow q$ is false is when $p$ is true and $q$ is false; otherwise, it is true.

**Truth Table for Implication:**

| $p$ | $q$ | $p \Rightarrow q$ |
| --- | --- | --- |
| V   | V   | V   |
| V   | F   | F   |
| F   | V   | V   |
| F   | F   | V   |

---

### Equivalence
Equivalence represents a bidirectional implication using the operator $\Leftrightarrow$, meaning "if and only if." The equivalence $p \Leftrightarrow q$ is true if both $p$ and $q$ have the same truth value; that is, both are true or both are false.

**Truth Table for Equivalence:**

| $p$ | $q$ | $p \Leftrightarrow q$ |
| --- | --- | --- |
| V   | V   | V   |
| V   | F   | F   |
| F   | V   | F   |
| F   | F   | V   |

---

This completes the essential concepts of propositional logic syntax and logical connectors.