# 4. Memory and Advanced Patterns

Turing Machines do not have variables. They do not have RAM. All they have is the physical tape and their internal states. To accomplish complex tasks (like copying strings or matching palindromes), you must use advanced algorithmic patterns.

---

## Pattern 1: States as "Memory Buffers"

When an algorithm requires the TM to "remember" a character while it travels to a different part of the tape, it must use its internal states. 

**Example Scenario:** You are copying the string `AABCA`. The head reads the letter `B`. It must carry this `B` across the tape past a `#` delimiter to write it on the other side.
* The head can only see one cell at a time. By the time it traverses the tape, it will have lost sight of the `B`. 
* **The Solution:** We create a dedicated state precisely for this action. When the machine reads `B`, it transitions into state $q_{carryB}$.
* The ONLY way the machine can ever be inside state $q_{carryB}$ is if it just picked up a `B`. Therefore, the state *itself* acts as a 1-character memory buffer. 

When the machine is in $q_{carryB}$, it simply ignores everything on the tape (moving right) until it finds a blank space, at which point it executes the rule: $\delta(q_{carryB}, \sqcup) = (q_{return}, B, L)$. The memory buffer is "flushed" onto the tape.

If your alphabet has 3 characters (`A, B, C`), you need 3 parallel "carry" paths ($q_{carryA}, q_{carryB}, q_{carryC}$). 
*This is why copying algorithms have massive state diagrams!*

---

## Pattern 2: The "Ping-Pong" Matching Algorithm

A classic category of TM problems involves validating symmetry or tracking pairs. 
* Languages like $L = \{ a^n b^n \}$ (Equal number of 'a's then 'b's)
* Languages like $L = \{ w \# w \}$ (A mirrored word)

To solve these, the machine uses a "ping-pong" rhythm, crossing off characters from the outside in (or matching them sequentially).

### The Standard $a^n b^n$ Playbook:
1. **Strike the First:** Start at the far left. Read an `a`. Erase it (or turn it into an `X` or $\sqcup$). 
2. **Scan Forward:** Travel all the way to the right across all remaining `a`s until you find the first `b`.
3. **Strike the Match:** Erase that `b` (turn it into an `X`).
4. **Return:** Travel all the way back to the left over the `a`s. You know to stop when you hit the boundary ($\sqcup$) or the first erased marker (`X`). Step one cell right.
5. **Repeat:** Repeat the process. 

### Why Markers are Mandatory
In the ping-pong algorithm, markers (`X` or $a \to \bar{a}$) are your navigational beacons. 
Without replacing `a` with `X`, when the head returns on step 4, it would have no idea which `a` it had already processed and which `a` was next in line.

---

## Pattern 3: The Subroutine

If you find yourself drawing the same cluster of states repeatedly, you are dealing with a subroutine. In complex machines, we modularize these to prevent getting overwhelmed:
* **The "Find End" Subroutine:** `read anything -> write same -> move Right`. Only breaks on $\sqcup$.
* **The "Return to Start" Subroutine:** `read anything -> write same -> move Left`. Only breaks on hitting the left wall or a specific marker.
* **The "Cleanup" Subroutine:** A final scan across the tape converting structural markers (like $\bar{A}, \bar{B}$) back to clean user data (`A, B`), followed by an acceptance halt.
