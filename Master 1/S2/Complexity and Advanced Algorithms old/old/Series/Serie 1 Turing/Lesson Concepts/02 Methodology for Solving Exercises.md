# 2. Methodology for Solving Exercises

> [!info] The DMTQ Format
> **DMTQ** stands for *Déterminer une Machine de Turing qui* (Determine a Turing Machine that...). 
> When an exercise begins with this phrase, it is an absolute requirement that you provide **three things**:
> 1. A High-Level Conceptual Description.
> 2. The Formal Mathematical Definition (the 7-tuple and all $\delta$ rules).
> 3. The State Diagram (usually using Mermaid or standard visual notation).

When approaching any DMTQ problem, or any Turing Machine construction, follow these proven algorithmic methodologies.

---

## 1. Tracing the "Happy Path"

Before writing states, manually trace how you, as a human, would solve the problem using only a pencil and one-cell-at-a-time vision.
1. **Where does the math happen?** Do you need to go left-to-right or right-to-left?
2. **What happens at the boundaries?** When you hit a blank $\sqcup$, what should the machine do? 
3. **What is the halting condition?** Where should the head be parked when it accepts? (Use the `S` command if needed to stay on the final answer).

---

## 2. Using Markers and Delimiters

A Turing Machine has no RAM. It cannot memorize a string. If an exercise asks you to compare two strings or copy a string, the TM must do it letter-by-letter. To avoid getting lost in the string, it must use two core techniques:

1. **Markers:** 
   When a chunk of data is processed, it must be "crossed out" or "marked" so the machine knows not to process it again when it loops back.
   * *Example:* Changing an `A` to a lowercase `a`, an `X`, or using an overline notation `Ā`.
   * *Cleanup:* Before accepting, the machine often needs a "cleanup phase" to sweep back across the tape and convert all markers back to their original characters.

2. **Delimiters:**
   If you are building a new string (like a copy), you need a wall to separate the original data from the new workspace.
   * *Example:* Scanning to the end of the input, writing a `#` symbol, and then using the space to the right of the `#` to build the copy.

---

## 3. Handling Left-Boundary Overflow

Because the tape is bounded on the left (index 0), you must act carefully when an algorithm naturally "grows" the data to the left.
* *Example:* Adding 1 to the Big-Endian binary number `11`. The math requires carrying a `1` to the left, resulting in `100`. But if `11` started at index 0, there is no physical space to its left. 
* *Solution:* In academia, we generally assume the input string is provided with a leading zero (e.g., `011`) to absorb the final carry. Alternatively, if forced, a highly complex "shift entire string right" subroutine is required. When solving course exercises, state your assumption. The `S` command is also an elegant way to write the final bit while absorbing the boundary.

---

## 4. Tracing Configurations (Execution Snapshots)

A configuration is a snapshot of the machine at an exact moment in time. It proves that your logic is sound.
It is written as `u q v`, where:
* `u` is the sequence of tape symbols to the left of the head.
* `q` is the current state.
* `v` is the tape sequence starting exactly at the read/write head.

**Example trace for $q0 a b$ reading `a` and transitioning to $q_1$ while moving right:**
1. $q0 a b$
2. $a q1 b$

When tracing, pay very close attention to how the machine treats the $\sqcup$ symbol to know when a pass is complete and when to turn around (bounce).

---

## 5. Proving Decidability

When asked if a problem is **Decidable** or **Undecidable**, remember the Golden Rule of Computability Theory:

> [!abstract] Finiteness Implies Decidability
> Complexity (taking a very long time) is not the same as Undecidability (being mathematically impossible).
> 
> * A problem is **Decidable** if an algorithm exists that is guaranteed to halt (with YES or NO) eventually.
> * If the search space of a problem is strictly finite—even if astronomically huge, like $1000^{1000}$ combinations—it is **Decidable**. A Turing machine can brute-force a finite space, and because the space has an end, the machine will 100% definitively halt.
> * Undecidability arises when the search space is infinite (like an unbounded sequence), meaning an algorithm might run forever without ever knowing if the answer is NO, or if it just hasn't searched long enough.
