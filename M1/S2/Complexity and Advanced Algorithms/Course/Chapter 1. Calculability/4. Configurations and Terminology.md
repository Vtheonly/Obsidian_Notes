# 4. Configurations and Terminology

## What is a Configuration?
To track what a TM is doing at any exact moment, we use a "snapshot" called a **Configuration**. 
Given a TM $M$, a state $q$, and two strings $u$ and $v$ on the alphabet $\Gamma$, the string **$u q v$** represents the configuration where:
1. The current state is $q$.
2. The complete tape contents are $uv$.
3. The head is currently positioned on the **first symbol of $v$**.

### Example Trace for the $w\#w$ machine
Let the input be `011000#011000`. 
1. **Initial (Starting) Configuration:** $q_1 011000\#011000$ (State is $q_1$, head is on the first `0`).
2. After crossing out the first `0` (replacing with `x` and moving right to $q_2$): $x q_2 11000\#011000$.
3. ... Many steps later ...
4. **Accepting Configuration:** $xxxxxx\#xxxxxx q_{accept} \square$

> [!tip] Representation by Configurations
> You can represent a complete TM simply as a set of configuration transitions, as long as the values of $\delta(q, a)$ are defined for all values of $(q, a)$ where $q \in Q$ and $a \in \Sigma$.

---

## Terminology: Recognizable vs Decidable

This is the most critical terminology in the chapter.

### Acceptance
A Turing Machine $M$ **accepts** an input $w$ if and only if (ssi) there exists a sequence of configurations $C_1, C_2, \dots, C_k$ such that:
* $C_1$ is the initial configuration for $w$.
* Each $C_i$ leads to $C_{i+1}$ via a single TM instruction (for $i=1 \dots k-1$).
* $C_k$ is an accepting configuration.

**Language Recognized ($L(M)$):** The set of all words that the machine $M$ accepts.

### The Two Classes of Languages
1. **Turing-Recognizable (Turing-reconnaissable):** 
   A language is recognizable if there exists a TM that recognizes its words. 
   *(Danger: If a word is NOT in the language, the machine might reject it, or it might loop forever without answering).*

2. **Turing-Decidable (Turing-décidable):**
   A language is decidable if there exists a TM that recognizes its words **AND rejects everything else**. 
   *(Safety: The machine is guaranteed to halt and give a YES or NO answer for every possible input).*

> **Rule:** Turing-décidable $\rightarrow$ Turing-reconnaissable. 
> Every decidable language is recognizable, but NOT vice-versa.