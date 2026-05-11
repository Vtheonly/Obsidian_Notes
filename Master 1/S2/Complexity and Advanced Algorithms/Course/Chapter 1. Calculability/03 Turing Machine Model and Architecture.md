# 2. The Turing Machine - Model and Architecture

## What is a Turing Machine?
A **Turing Machine (TM)** is an abstract model of computation. Despite having no real physical gears or circuits, it perfectly represents the logic of any modern computer. 

It is composed of three main parts:
![[image 1.png]]
### 1. A Tape (Un ruban)
* It is **infinite to the right**, meaning the machine will never run out of memory.
* It is divided into cells (cases), each containing a symbol.
* **The Blank Character ($\square$):** Among all possible symbols, there is a special symbol called the blank character ($\square$), which represents an empty cell.
* **Initial State:** At the very beginning, the tape contains the input string placed on the far left. Every other cell to the right is filled with blanks ($\square$).

### 2. A Read/Write Head (Une tête de lecture/écriture)
* It is placed over exactly one cell on the tape at a time.
* It can **read** the current symbol.
* It can **write** a new symbol.
* It can **move** exactly one cell to the **left (L)** or one cell to the **right (R)**.

### 3. A Control Unit (Un contrôleur)
This is the "brain" of the machine. Based on the **current state** of the machine and the **symbol currently being read**, it emits an instruction that determines:
1. What symbol to write.
2. In which direction to move the head.
3. What the new state will be.

> [!info] Finite States and Halting
> The set of states in a TM is **finite**. There are three highly specific states you must know:
> * **$q_{start}$**: The starting state.
> * **$q_{accept}$**: The state of acceptance.
> * **$q_{reject}$**: The state of rejection.
> 
> $q_{accept}$ and $q_{reject}$ are strictly **distinct** from one another, and reaching either of them marks the absolute **end of the execution**.

## The Church-Turing Thesis (Thèse de Church-Turing)
> **A function is Turing-computable if there exists a Turing Machine that can implement it.**

**Why is this important?**
Because *any* function that can be computed by a modern physical computer using *any* programming language (C, Python, Java) is Turing-computable. If a Turing Machine cannot solve it, no computer in the world ever will.
