
### 4. **Axioms and Inference Rules**

In sequent calculus, **axioms** and **inference rules** define how sequents can be manipulated and how we derive new sequents from existing ones.

#### Definition 1.7.3: **Axioms and Inference Rules**

---

### 4.1 **Axiom of Sequent Calculus**

The axiom stated is:

- **Axiom**: $X \vdash X$

This means that any formula implies itself. It's a basic rule stating that if we have a formula `X`, we can immediately conclude `X` from it. This is the foundational **self-implication axiom** that serves as a basis for all other deductions in sequent calculus.

---

### 4.2 **Inference Rules**

Inference rules are the operations that allow us to manipulate and deduce new sequents based on existing ones. There are several types of inference rules in sequent calculus, which are structured as premises and conclusions.

#### Structure of an Inference Rule:

Each inference rule consists of:
- **Premise** (the top part of the rule),
- **Conclusion** (the bottom part of the rule).

If the premises hold true, then we can infer the conclusion.

---

### 5. **Types of Inference Rules in Sequent Calculus**

Let’s go over the different types of inference rules one by one.

---

#### 5.1 **Negation Rules**

These rules are used to handle negations (`¬`) in the logic.

- **Negation Left Rule (¬Left)**:
  $$
  \frac{\Gamma \vdash \Delta, X}{\Gamma, \neg X \vdash \Delta}
  $$
  - This rule allows us to introduce a negation `¬X` on the left-hand side of the sequent. If we can derive `X` from the premises and the conclusion, we can infer `¬X` in the hypotheses.

- **Negation Right Rule (¬Right)**:
  $$
  \frac{\Gamma, X \vdash \Delta}{\Gamma \vdash \neg X, \Delta}
  $$
  - This rule allows us to introduce a negation `¬X` on the right-hand side of the sequent. If `X` is in the hypotheses and we can derive the conclusion `∆`, we can infer `¬X` in the conclusions.

#### Intuitive Explanation

These rules help us manipulate negations in a logical proof. For example, if you know that `X` leads to a contradiction, you can infer `¬X` (that `X` is not true).

---

#### 5.2 **Conjunction Rules**

These rules handle conjunctions (`∧`), the logical "and".

- **Conjunction Left Rule (∧Left)**:
  $$
  \frac{\Gamma, X, Y \vdash \Delta}{\Gamma, X \land Y \vdash \Delta}
  $$
  - If we can prove `X` and `Y` from the hypotheses `Γ`, we can infer their conjunction `X ∧ Y` in the hypotheses.

- **Conjunction Right Rule (∧Right)**:
  $$
  \frac{\Gamma \vdash \Delta, X \quad \Gamma \vdash \Delta, Y}{\Gamma \vdash \Delta, X \land Y}
  $$
  - If we can derive `X` and `Y` independently in the conclusions, we can combine them into `X ∧ Y` in the conclusions.

#### Intuitive Explanation

These rules deal with the idea of **"and"** in logic. If you can prove `X` and `Y` separately, you can conclude that `X ∧ Y` is true. Similarly, if both `X` and `Y` are true, you can conclude that both must be true together.

---

#### 5.3 **Disjunction Rules**

These rules handle disjunctions (`∨`), the logical "or".

- **Disjunction Left Rule (∨Left)**:
  $$
  \frac{\Gamma, X \vdash \Delta \quad \Gamma, Y \vdash \Delta}{\Gamma, X \lor Y \vdash \Delta}
  $$
  - If we can prove `X` or `Y` separately, we can infer `X ∨ Y` in the hypotheses.

- **Disjunction Right Rule (∨Right)**:
  $$
  \frac{\Gamma \vdash \Delta, X \quad \Gamma \vdash \Delta, Y}{\Gamma \vdash \Delta, X \lor Y}
  $$
  - If we can derive `X` and `Y` independently in the conclusions, we can infer `X ∨ Y` in the conclusions.

#### Intuitive Explanation

Disjunction deals with **"or"** in logic. If you can show that either `X` or `Y` is true (independently), you can infer `X ∨ Y` (either `X` or `Y` is true). Similarly, if both are true, you can deduce that one of them is true.

---

#### 5.4 **Implication Rules**

These rules handle implications (`⇒`), representing logical "if... then...".

- **Implication Left Rule (⇒Left)**:
  $$
  \frac{\Gamma \vdash \Delta, X \quad \Gamma, Y \vdash \Delta}{\Gamma, X \Rightarrow Y \vdash \Delta}
  $$
  - If we can derive `X` implies `Y` from the premises, we can conclude the implication `X ⇒ Y` in the hypotheses.

- **Implication Right Rule (⇒Right)**:
  $$
  \frac{\Gamma, X \vdash Y, \Delta}{\Gamma \vdash X \Rightarrow Y, \Delta}
  $$
  - If we can derive `Y` from the premises `X`, we can infer `X ⇒ Y` in the conclusions.

#### Intuitive Explanation

Implication rules are about **"if... then"** statements. If you can show that `X` leads to `Y`, you can infer the implication `X ⇒ Y`. Similarly, if `X` leads to `Y`, the implication can be concluded from the premises.

---

### 6. **Summary of the Inference Rules**

To summarize, these inference rules allow the manipulation of logical statements according to the types of logical operations present in the sequent. Each rule specifies how to deal with negations, conjunctions, disjunctions, and implications, and they help in breaking down complex formulas into simpler parts that can be handled more easily during a formal proof.

---

Let me know if you'd like me to clarify any specific inference rule or part of the explanation, or if you're ready to move forward with more details!