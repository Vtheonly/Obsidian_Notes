# 1. Turing Machine Foundations

> [!important] Crucial Conventions for this Course
> Before solving any computational problem using a Turing Machine (TM), it is completely mandatory to understand the physical constraints of the machine we are modeling. A Turing Machine is a mathematical model of computation, but its "hardware" rules define how we write our algorithms.

## The Physical Constraints: Left-Bounded Tape

In classical theory, a Turing Machine tape is often doubly infinite. **However, in this course, the tape is bounded to the left.**

1. **The Left Wall:** The tape is infinite to the right, but it has a hard wall on the left side (Cell 0).
2. **The "Bounce" Effect:** If the read/write head is currently at Cell 0 and receives an instruction to move Left (`L`), it **bounces**. It stays in Cell 0. It does not crash, but it cannot move into negative indices.
3. **Initial Configuration:** When the machine boots up:
   - The input string starts exactly at Cell 0.
   - Immediately following the last character of the input, the rest of the infinite tape is filled with blank symbols (denoted as $\sqcup$ or $\Box$).
   - The read/write head starts at Cell 0.

---

## The 7-Tuple Definition

A deterministic Turing Machine (DTM) is formally defined mathematically as a 7-tuple: 
**$M = (Q, \Sigma, \Gamma, \delta, q_{start}, q_{accept}, q_{reject})$**

1. **$Q$**: The finite set of states (e.g., $q_0, q_1, q_f, q_{acc}$).
2. **$\Sigma$**: The input alphabet. This is what the user is allowed to write on the tape before the machine starts. It *never* includes the blank symbol $\sqcup$.
3. **$\Gamma$**: The tape alphabet. This includes everything in $\Sigma$, plus the blank symbol $\sqcup$, and any temporary "marker" or delimiter symbols (like $A, \bar{B}, \#$) the machine uses during computation.
4. **$\delta$**: The transition function. This is the "code" of the machine. It takes the current state and the current symbol being read, and outputs: `(New State, Symbol to Write, Direction to Move)`.
5. **$q_{start}$**: The state where execution begins.
6. **$q_{accept}$**: The state that immediately halts the machine and outputs "YES" or finishes the computation.
7. **$q_{reject}$**: The state that immediately halts the machine and outputs "NO" or crashes.

---

## The Transition Function $\delta$ and the Missing Rule

> [!info] Total vs Partial Functions
> A rigorous mathematical definition states that the transition function $\delta$ is a **Total Function**. This means for *every single combination* of State $\times$ Alphabet Symbol, there MUST be an explicitly defined output rule.
>
> However, to save space, humans typically draw TMs as partial functions. Any input that doesn't have a explicitly drawn arrow in a diagram implicitly defaults to: `Go to Reject State, Write same symbol, Move Right (or Left)`.

This means if you are in a state $q_x$ reading a symbol $a$, and you have not explicitly defined a rule for $\delta(q_x, a)$, the machine automatically transitions to $q_{reject}$ and dies. You do not always need to draw arrows to $q_{reject}$ in your diagrams; it is implicitly assumed unless the question asks you to complete the diagram fully.

---

## The "S" (Stay) Direction Command

In classical Turing Machine theory, the head *must* move Left (`L`) or Right (`R`) after every transition. 

However, **this specific course permits an extra command: `S`.**
* `S` stands for **Stay** (or Stationary/Stop). 
* To the possible movements `R` and `L`, we add `S`.
* This command is incredibly useful when you want to safely halt the machine without moving the head off the final computed answer, or when handling an overflow condition at the tape's boundary.

### Example Uses for `S`:
- Halting precisely on the last bit of a binary number after completing an addition.
- Performing a calculation when stuck against the left-boundary wall where an `L` move would be conceptually risky or visually misleading.

---

## Data Encoding: Endianness

When dealing with binary representations, it is vital to know how the number is physically laid out on the tape. 

> [!info] What is Endianness?
> **Little Endian:** The Least Significant Bit (LSB) is stored at the smallest address (the leftmost cell). It's "backwards" to how humans naturally read, but highly convenient for TMs because addition math starts at the LSB. 
> *Example:* The number Three ($3$) is written `110`.
> 
> **Big Endian:** The Most Significant Bit (MSB) is on the left. This is normal human reading order. 
> *Example:* The number Three ($3$) is written `011`.
> 
> *Key takeaway for TMs:* Because binary addition always starts at the Least Significant Bit (due to carries), Little Endian allows a TM to start math immediately. Big Endian requires the TM to first traverse the entire string to the right before doing any logic.
