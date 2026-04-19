# 3. Data Representations and Arithmetic

> [!info] The Medium is the Message
> A Turing Machine tape only holds symbols from a finite alphabet (like `0`, `1`, $\sqcup$). The machine doesn't mathematically "know" what the number $5$ is. It only knows how to manipulate symbols according to rules. Therefore, how data is physically laid out on the tape completely dictates how the algorithm must be designed.

There are two primary ways numbers are represented in this course: **Unary** and **Binary**.

---

## 1. Unary Representation

Unary counting is the most primitive form of arithmetic—it is identical to drawing tally marks on a chalk board.
* The number $N$ is represented by $N$ consecutive `1`s.
* $0 = \epsilon$ (the empty string, so the tape is just $\sqcup \sqcup \dots$)
* $1 = 1$
* $2 = 11$
* $3 = 111$

### Arithmetic in Unary
**Addition ($N+1$ or $N+M$):**
Addition in unary does not involve complex logic gates or "carries". It is simply **concatenation**.
* To add $1$ (the Successor): You just find the end of the string (the first $\sqcup$) and overwrite it with a `1`.
* To add $M$ to $N$: You simply push the two blocks of `1`s together.

**Multiplication ($N \times M$):**
Multiplication in unary requires a string copy algorithm. To do $3 \times 2$, you take the string `111` and copy it twice.

---

## 2. Binary Representation

Binary is infinitely more efficient spatially, but algorithmically much harder for a Turing Machine to process because operations on one bit affect surrounding bits (the "carry" in addition, the "borrow" in subtraction).

### Endianness dictates the Algorithm
Because binary arithmetic manually cascades exactly like grade-school math (right to left on paper, starting at the ones column), the layout of the bits on the physical tape determines where the machine must start.

1. **Little-Endian:** The absolute best case for a Turing Machine.
   * **Layout:** The Least Significant Bit (LSB) is at the leftmost index (Cell 0).
   * **Example ($3$):** `110`
   * **Advantage:** The machine head boots up at Cell 0. Because the math starts at the LSB, the machine can begin its calculation on the very first step! It sweeps Left-to-Right naturally carrying overflow.

2. **Big-Endian:** Natural for humans, highly annoying for state machines.
   * **Layout:** The Most Significant Bit (MSB) is at Cell 0. The LSB is on the right.
   * **Example ($3$):** `011`
   * **Disadvantage:** The machine head boots up at Cell 0, which is the wrong end of the number! A Big-Endian algorithm must first blindly scan all the way to the right until it hits a $\sqcup$, step one cell back to the left, and *then* compute the math moving Right-to-Left. 

> [!warning] The Left Boundary Hazard in Big-Endian Addition
> If you are processing Big-Endian addition (moving right-to-left) and the number undergoes a major overflow (e.g., $3 \to 4$ which is $11 \to 100$), you will eventually hit Cell 0 while still holding a carry digit of `1`.
> 
> Because the tape has a physical wall at Cell 0, the machine cannot blindly move left to write the final `1`. The standard academic workaround in this course is either passing leading zeros (e.g., padding `11` as `011`) or utilizing the non-standard `S` (Stay) instruction provided in your TD rules to overwrite the boundary blank safely.
