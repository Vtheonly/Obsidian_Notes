# Exercise 6: Completing the Reject State

## 1. Problem Statement
We are given a state diagram from a course example (a Turing Machine designed to recognize the language $w\#w$, where a word is repeated exactly once after a delimiter). 
By standard convention, the diagram omits transitions to the **Reject State ($q_{reject}$)** to save space and improve human readability. We are asked to formally complete the state diagram by writing out the transitions that lead to rejection.

---

## 2. Deep Methodological Breakdown

### Total Functions vs Partial Functions
The heart of this exercise lies in the fundamental definition of a Turing Machine. 
In pure mathematics, the transition function $\delta$ of a Deterministic Turing Machine is defined as a **Total Function**. This means its domain is perfectly mapped. For *every single combination* of existing States ($Q$) and Alphabet Symbols ($\Sigma$ and $\Gamma$), there MUST be an explicitly defined instruction. 

When humans draw a diagram where some arrows are "missing," they are drawing a **Partial Function**. 

The implicit rule for converting a human diagram into a mathematical machine is:
> "If I am in State $q$, and I read Symbol $x$, and there is no arrow telling me what to do, I must transition into $q_{reject}$, write the same symbol $x$, and halt computation."

### Strategy for the Exercise
Assume the tape alphabet for the $w\#w$ machine is defined as $\Gamma = \{0, 1, x, \#, \sqcup\}$. 

To formally complete the diagram, we must execute an exhaustive, mechanical checklist:
1. Look at $q_1$. List the arrows leaving $q_1$.
2. Compare the list of arrows against the entire alphabet $\{0, 1, x, \#, \sqcup\}$.
3. For whatever symbols are "missing", create a rule pointing to $q_{reject}$.
4. Repeat this for all states in the diagram.

---

## 3. The Complete and Exhaustive Solution

Applying the mechanical checklist to the states given in the problem's source material, here are the explicit rejection rules that must be added to make $\delta$ a Total Function.

*Note: The machine halts in $q_{reject}$, so the head movement (`L`, `R`, or logically `S`) is irrelevant as computation instantly ceases, but we traditionally assign a movement just to satisfy tuple syntax.*

**From State $q_1$:**
* **Arrows that exist:** `0`, `1`, `#`.
* **Missing symbols in domain:** `x`, $\sqcup$.
* **Rule to Add:** Draw an arrow from $q_1 \to q_{reject}$ labeled $x, \sqcup \to S$.

**From State $q_2$:**
* **Arrows that exist:** `0`, `1` (via self-loop), `#`.
* **Missing symbols in domain:** `x`, $\sqcup$.
* **Rule to Add:** Draw an arrow from $q_2 \to q_{reject}$ labeled $x, \sqcup \to S$.

**From State $q_3$ (if applicable in diagram):**
* **Arrows that exist:** `0`, `1`, `#`.
* **Missing symbols in domain:** `x`, $\sqcup$.
* **Rule to Add:** Draw an arrow from $q_3 \to q_{reject}$ labeled $x, \sqcup \to S$.

**From State $q_4$:**
* **Arrows that exist:** `x`.
* **Missing symbols in domain:** `0`, `1`, `#`, $\sqcup$.
* **Rule to Add:** Draw an arrow from $q_4 \to q_{reject}$ labeled $0, 1, #, \sqcup \to S$.

**From State $q_5$:**
* **Arrows that exist:** `x`.
* **Missing symbols in domain:** `0`, `1`, `#`, $\sqcup$.
* **Rule to Add:** Draw an arrow from $q_5 \to q_{reject}$ labeled $0, 1, #, \sqcup \to S$.

**From State $q_6$:**
* **Arrows that exist:** `0`, `1`, `x`, `#`.
* **Missing symbols in domain:** $\sqcup$.
* **Rule to Add:** Draw an arrow from $q_6 \to q_{reject}$ labeled $\sqcup \to S$.

**From State $q_7$:**
* **Arrows that exist:** `0`, `1`, `x`.
* **Missing symbols in domain:** `#`, $\sqcup$.
* **Rule to Add:** Draw an arrow from $q_7 \to q_{reject}$ labeled $#, \sqcup \to S$.

**From State $q_8$:**
* **Arrows that exist:** `x`, $\sqcup$.
* **Missing symbols in domain:** `0`, `1`, `#`.
* **Rule to Add:** Draw an arrow from $q_8 \to q_{reject}$ labeled $0, 1, # \to S$.

*(By strictly adding these arrows, the machine achieves mathematical totality).*
