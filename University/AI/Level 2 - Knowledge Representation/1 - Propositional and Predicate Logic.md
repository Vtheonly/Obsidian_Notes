
## Propositional Logic

#### What It Is

Propositional logic is a basic form of logic that deals with propositions—statements that are either true or false. Each proposition is treated as a standalone fact, with no internal structure or variables.

How It’s Used in the Document

In the document, propositional logic is used to list specific family relationships as individual statements. Examples include:

1. "Claude est fils de Michel" (Claude is the son of Michel).
    
2. "Chantal est fille de Michel" (Chantal is the daughter of Michel).
    
3. "Michel est grand-père de Thomas" (Michel is the grandfather of Thomas).
    

Each of these is a separate proposition, written in natural language but representing a single, atomic fact.

Key Features

1. Simple Statements: Each proposition is a complete, specific assertion (e.g., "Claude is the son of Michel" could be assigned a symbol like P and treated as true or false).
    
2. No Variables: It doesn’t use placeholders for people or relationships; every statement is about specific individuals.
    
3. No General Rules: It can’t express general relationships, like "all parents have children." Each fact must be explicitly stated.
    

Example

Imagine a family where Michel is Claude’s father, and Claude is Thomas’s father:

- P: "Michel is the father of Claude" (true).
    
- Q: "Claude is the father of Thomas" (true).
    
- R: "Michel is the grandfather of Thomas" (true).
    

These are separate propositions. To connect them (e.g., to say Michel is Thomas’s grandfather because he’s Claude’s father and Claude is Thomas’s father), you’d need additional rules, but propositional logic doesn’t naturally provide a way to link them.

---

Predicate Logic

What It Is

Predicate logic builds on propositional logic by adding predicates, variables, and quantifiers. This allows it to express relationships between entities and general rules, making it more powerful and flexible.

How It’s Used in the Document

The document defines the "grandfather" relationship using a formal predicate logic expression:

- ∀x, y, z : [mâle(z) ∧ [fille(y, z) ∨ fils(y, z)] ∧ [fille(x, y) ∨ fils(x, y)] ⇒ grand-père(z, x)]
    

Let’s break this down:

- ∀x, y, z: "For all x, y, z" (universal quantifier—applies to all individuals).
    
- mâle(z): "z is male" (a predicate stating z’s gender).
    
- [fille(y, z) ∨ fils(y, z)]: "y is a daughter or son of z" (y is a child of z).
    
- [fille(x, y) ∨ fils(x, y)]: "x is a daughter or son of y" (x is a child of y).
    
- ⇒ grand-père(z, x): "then z is the grandfather of x."
    

This formula means: "If z is male, and y is a child of z, and x is a child of y, then z is the grandfather of x." It’s a general rule that applies to any family.

Key Features

- Predicates: Relationships like "fils(y, z)" (y is the son of z) or "mâle(z)" (z is male) describe properties or connections between entities.
    
- Variables: x, y, and z act as placeholders, allowing the logic to apply to any individuals, not just specific ones like Claude or Michel.
    
- Quantifiers: Symbols like ∀ ("for all") and ∃ ("there exists") enable general statements (e.g., "all males with grandchildren are grandfathers").
    
- Inference: You can deduce new facts from rules (e.g., if Michel is male, Claude is his son, and Thomas is Claude’s son, then Michel is Thomas’s grandfather).
    

Example

Using the same family:

- mâle(Michel): "Michel is male."
    
- fils(Claude, Michel): "Claude is the son of Michel."
    
- fils(Thomas, Claude): "Thomas is the son of Claude."
    

Applying the rule:

- Since Michel is male, Claude is his child, and Thomas is Claude’s child, we infer grand-père(Michel, Thomas) ("Michel is the grandfather of Thomas").
    

---

Key Differences Between Propositional Logic and Predicate Logic

Here’s a side-by-side comparison to make the distinction clear:

|Aspect|Propositional Logic|Predicate Logic|
|---|---|---|
|Expressiveness|Limited to specific, atomic statements (e.g., "Claude is the son of Michel").|Can express general rules and relationships (e.g., "all males with grandchildren are grandfathers").|
|Structure|No internal structure; each proposition is standalone.|Uses predicates, variables, and quantifiers to show connections between entities.|
|Scalability|Requires a new proposition for each fact, which can get unwieldy (e.g., listing every grandfather relationship).|One rule can cover many cases (e.g., the grandfather rule applies to all families).|
|Variables|None; specific to named individuals.|Uses variables (x, y, z) to generalize across individuals.|
|Inference|Limited; connections between facts must be explicitly stated.|Powerful; can deduce new facts from rules (e.g., inferring grandparenthood).|
|Example from Document|"Michel est grand-père de Thomas" as a single fact.|∀x, y, z rule defining "grand-père" for any x, y, z.|

---

Why It Matters

- Propositional Logic is simpler and works well for small, specific sets of facts. However, it becomes impractical for complex systems like family trees with many relationships, as you’d need to list every single fact explicitly.
    
- Predicate Logic is more sophisticated and scalable. It can define relationships once (e.g., what makes someone a grandfather) and apply that rule universally, making it ideal for reasoning and knowledge representation in fields like artificial intelligence.
    

---

Putting It Together with an Example

Let’s revisit the family: Michel is Claude’s father, and Claude is Thomas’s father.

- Propositional Logic:
    
    - "Michel is the father of Claude."
        
    - "Claude is the father of Thomas."
        
    - "Michel is the grandfather of Thomas."
        
    - These are three separate statements. If we add another family member (e.g., Chantal as Michel’s daughter and mother of Sophie), we’d need more propositions, like "Michel is the grandfather of Sophie," with no way to connect them automatically.
        
- Predicate Logic:
    
    - mâle(Michel): "Michel is male."
        
    - parent(Michel, Claude): "Michel is the parent of Claude."
        
    - parent(Claude, Thomas): "Claude is the parent of Thomas."
        
    - Rule: ∀x, y, z : [mâle(x) ∧ parent(x, y) ∧ parent(y, z) ⇒ grand-père(x, z)].
        
    - From this, we infer grand-père(Michel, Thomas). If we add parent(Michel, Chantal) and parent(Chantal, Sophie), the same rule infers grand-père(Michel, Sophie)—no extra statements needed.
        

---

