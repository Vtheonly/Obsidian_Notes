# 5. Formal Tracing and Halting Proofs

To prove a Turing Machine actually works (and to score maximum points on exams), you cannot just say "it looks right". You must rigorously prove its execution and its halting properties.

---

## 1. Tracing Configurations Effectively

A **Configuration** is the mathematical equivalent of taking a photograph of the Turing Machine mid-execution. It captures the entire state of the universe in a single line.

**Format:** $u \ q \ v$
* $u$ = The entire sequence of tape cells to the **left** of the head.
* $q$ = The current internal state of the machine.
* $v$ = The entire sequence of tape cells starting **exactly at** the read/write head, going infinitely to the right (though we only write up to the last non-blank character).

### Trace Example Walkthrough
Imagine a tape reading $a a b b$. We are at state $q_0$ at index 0.
1. $q_0 \ a \ a \ b \ b$
   * *Rule:* $\delta(q_0, a) = (q_1, X, R)$ (Read 'a', write 'X', move Right).
2. $X \ q_1 \ a \ b \ b$
   * *Rule:* $\delta(q_1, a) = (q_1, a, R)$ (Read 'a', ignore it, move Right).
3. $X \ a \ q_1 \ b \ b$
   * *Rule:* $\delta(q_1, b) = (q_2, X, L)$ (Read 'b', write 'X', move Left).
4. $X \ q_2 \ a \ X \ b$
   * *Rule:* $\delta(q_2, a) = (q_2, a, L)$ (Read 'a', ignore it, move Left).
5. $q_2 \ X \ a \ X \ b$

**Pro Tip for Exams:** Align your configurations vertically when tracing so you can visually see the $q$ state sliding back and forth through the string! It exposes logic bugs instantly.

---

## 2. Proving Halting (Decidability)

A standard exam question asks: *"Prove that machine $M$ always halts for any input string."*
You cannot prove this by just running it on `aabb`. You must prove it logically for the infinite set of all possible inputs.

To prove an algorithmic state machine halts, you must prove **Search Space Shrinkage**. 

### The Shrinkage Argument:
If you want to prove a matching machine (like $a^n b^n$) always halts, write this exact logical argument:

1. **Finite Origin:** State that any valid input string provided by the user is, by definition, strictly finite in length.
2. **Consumption:** Identify the "Forward Loop" of the algorithm (e.g., $q_1 \to q_2 \to q_3$). Prove that every single time the machine successfully executes this loop, it irreversibly marks or deletes at least one character from the input.
3. **Impossibility of Infinity:** Because the string is finite, and the machine irreversibly consumes characters on every cycle, the machine mathematically **must** eventually run out of characters.
4. **Absence of Stationary Traps:** Inspect the transition table. Verify there are no transitions $\delta(q_x, a) = (q_x, a, S)$ that would allow the machine to freeze on a single spot forever without doing work.
5. **Implicit Crash Paths:** State that any improperly formatted string (like $a \ b \ a$) will inevitably lead the machine to expect a character it cannot find, forcing an undefined rule which immediately triggers the $q_{reject}$ termination.

Therefore, since all valid strings are logically consumed and all invalid strings trigger crashes, the machine is guaranteed to halt for $100\%$ of cases.

---

## 3. Complexity vs Undecidability (Revisited)

As highlighted in the Matrix Mortality Problem (Exercise 7), never confuse the time an algorithm takes with its Computability.

* **Complexity (Time/Space):** How many steps does it take to halt? An algorithm that takes $O(2^n)$ time is slow, but it is computable.
* **Undecidability:** Does it ever halt at all? The standard Matrix Mortality problem (infinite bound) or the Halting Problem are undecidable. There is no algorithm that can look at the raw matrix formulas and guarantee an answer within a finite number of steps. Once you bound the combinations to $m \le 1000$, it becomes a massive, ugly, but strictly finite subset—and finite sets are always Decidable by a simple brute-force Turing Machine.
