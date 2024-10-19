### Introduction

This chapter introduces important concepts in operating systems, specifically focused on tasks (also called processes) and how they interact, either sequentially or in parallel, within a system. We'll explore fundamental notions such as sequential processes, task precedence, task behavior, determinism, and structures that allow for parallel processing.

### 1. Sequential Processes

#### 1.1. The Notion of a Task

A task is the fundamental unit of computation that exhibits logical coherence. If we denote a process by $P$, the process is made up of several tasks executed sequentially, represented as: $P = (T_1 T_2 \dots T_n)$ where each $T_i$ is a task, and each task $T_i$ has two associated events:

- **$d_i$**: The task begins execution.
- **$f_i$**: The task finishes execution.

For example, if we have the task $T: X = X / 2$, the task's initialization ($d$) corresponds to reading the value of $X$, and its termination ($f$) corresponds to writing the result back to $X$.

Tasks often involve acquiring necessary resources at initialization (like reading input parameters) and releasing resources at termination (like writing results).

### 2. Task Systems and Precedence Graphs

A task system consists of a set of tasks and a precedence relation that defines the execution order between tasks. The precedence relation, denoted by '<', must satisfy:

1. For any task $T$, we cannot have $T < T$.

2. For any two tasks $T_i$ and $T_j$, both $T_i < T_j$ and $T_j < T_i$ cannot hold simultaneously.

3. The relation is transitive: if $T_i < T_j$ and $T_j < T_k$, then $T_i < T_k$.

#### Example 1: Simple Precedence

Let $E = \{T_1, T_2, T_3, T_4\}$, where the relations are:

- $T_1 < T_2$, $T_2 < T_4$, $T_1 < T_3$, and $T_1 < T_4$.

A precedence graph is a directed graph where nodes represent tasks, and edges represent the precedence relations between them. The graph for the above example contains tasks with the following characteristics:

- $T_1$ is the initial task.
- $T_4$ is the final task.
- $T_2$ is the immediate successor of $T_1$.
- $T_2$ and $T_3$ are independent (they can execute in parallel).

#### Redundant Arcs

Precedence graphs should avoid redundant arcs, such as $T_1 \to T_4$, when this path can already be inferred from other arcs. Redundant arcs don't add value and can confuse the graph's interpretation.

### 3. Behavior of a Task System

The behavior of a task system is defined by the interleaving of task executions, which must respect the precedence constraints. For example, consider a system with tasks $T_1$, $T_2$, $T_3$, and $T_4$ where:

- $T_1$: Read value $N$,
- $T_2$: $N = N + 2$,
- $T_3$: $N = N / 3$,
- $T_4$: Write value $N$.

This system can have multiple valid execution sequences that satisfy the precedence constraints, such as:

- $C_1$: $T_1$, then execute $T_2$ and $T_3$ in parallel, followed by $T_4$.
- $C_2$: $T_1$, then execute $T_3$ before $T_2$, and finally $T_4$.

### 4. Determinism in Task Systems

A task system is deterministic if, for each possible execution order, the sequence of variable values remains the same. This property is governed by Bernstein's conditions. For two tasks $T_1$ and $T_2$ to be non-interfering, they must either have a defined order or must not share variables in ways that affect each other's execution. Specifically, the following must hold:

1. $T_1$ is either a predecessor or successor of $T_2$.
2. There are no conflicts between the read and write sets of variables for the tasks.

#### Example 2: Bernstein’s Conditions

Consider the following process $P$ :

- $T_1$: Read $A$,
- $T_2$: Read $B$,
- $T_3$: $B = 3 * B$,
- $T_4$: $C = A + B$,
- $T_5$: Write $C$.

We can break this down into two parallel processes, $P_1$ and $P_2$, where:

- $P_1$ reads $A$, computes $C = A + B$, and writes $C$,
- $P_2$ reads $B$, modifies it, and writes $C$.

However, tasks $T_3$ and $T_4$ interfere, meaning the system is not deterministic. According to Bernstein's conditions, a task system is deterministic if all tasks are non-interfering.

### 5. Parallelism and Parallel Programming Languages

Parallel programming languages provide structures to express both sequential and parallel task execution. Two commonly used structures are **parbegin/parend** and **fork/join**.

#### 5.1. Parbegin/Parend Structure

The **parbegin/parend** structure allows tasks to run in parallel. The execution completes only when all parallel tasks finish. For example:

```pseudo
parbegin
    Task1;
    Task2;
    ...;
    TaskN;
parend;

```

#### 5.2. Fork/Join Structure

The **fork** instruction creates a new parallel activity that starts at a specific label and runs concurrently with the current task. The **join** instruction merges multiple parallel activities back into a single one. The following example illustrates a simple fork/join structure:

```pseudo
Begin
    Task1;
    fork label1;
    Task2;
    goto stop;
label1:
    Task3;
stop:
End.

```

In this case, Task1 is executed first, followed by a fork creating a parallel execution path for Task3, while Task2 continues in the main path.

