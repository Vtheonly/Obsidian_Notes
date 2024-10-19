
### Introduction

In operating systems, multiple processes often do not evolve independently. They cooperate to accomplish a common task, sharing data and resources. To enable this cooperation, synchronization mechanisms must be provided by the operating system to establish execution order between cooperating processes.

### 1. Sharing Resources and Data

The execution of processes requires a set of logical (files, data, code) and physical (memory, processor, disk, printer) resources. Resources are categorized into:
- **Shareable resources**: These have multiple entry points and can be accessed by several processes simultaneously.
- **Non-shareable resources**: These have a single entry point and require exclusive access. In this case, access must be coordinated to avoid inconsistencies.

#### 1.1 Inconsistent Scenario Example

A shared variable without proper precautions can lead to unpredictable results. For example:

```c
// Reservation program
if (place_dispo > 0) {
    place_dispo--;
    printf('Place reserved');
} else {
    printf('No more places');
}
```

When translated into machine language, multiple processes attempting to access and modify `place_dispo` can create a race condition. Imagine if two processes (P1 and P2) try to reserve the last available spot (`place_dispo == 1`). If P1 reaches an intermediate step and is preempted, allowing P2 to finish, both might end up reserving the same place, leading to data inconsistency.

To prevent this, the section of code where the shared variable (`place_dispo`) is manipulated must be made atomic. This shared variable is known as a **critical resource**, and the part of the code that manipulates it is called the **critical section**.

### 2. Critical Section

#### 2.1 Definition

A critical section in a program is a sequence of instructions whose execution must be managed in mutual exclusion. A process executing in parallel cannot enter its critical section if another process is already executing in its own.

#### 2.2 The Mutual Exclusion Problem

In a system with `n` processes (P1, P2, ..., Pn), each process may have its own critical section (S.Ci), and only one process can execute within its critical section at a time. To achieve this, protocols are designed to ensure mutual exclusion for accessing critical resources.

The general form of a process becomes:

```pseudocode
repeat
    <Entry protocol>
    <Critical section>
    <Exit protocol>
until false;
```

A process waits in the entry section until a condition is met to enter the critical section and signals its exit when done.

### 3. Mutual Exclusion Mechanisms

#### 3.1 Hypotheses
1. The system has `n` processes executing in parallel.
2. Processes may have varying execution speeds.
3. Basic machine instructions are indivisible.

#### 3.2 Software Solutions

**Solution 1: Alternation-based Mutual Exclusion**

Two processes (Pi and Pj) use a shared variable `turn` to control access to the critical section. The process whose turn it is gets access to the critical section, ensuring mutual exclusion.

**Drawbacks**: If one process halts, the other can no longer enter its critical section, even if it’s available.

**Solution 2: Flag-based Mutual Exclusion**

A boolean array `flag[0,1]` is used where each process sets its flag to true when attempting to enter its critical section. The process checks if the other’s flag is set and only proceeds if it isn’t. However, this can lead to deadlock.

**Solution 3: Peterson’s Algorithm**

Peterson's algorithm improves upon earlier methods by combining the advantages of both alternation and flag solutions. It ensures that both processes cannot enter their critical sections at the same time, even if they both attempt to do so simultaneously.

```pseudocode
// Pi process
flag[i] = true; 
turn = j;
while (flag[j] && turn == j) {
    // Wait
}
<critical section>
flag[i] = false;
```

#### 3.3 Hardware Solutions

**1) Disabling Interrupts**: Interrupts are disabled during the execution of the critical section, ensuring that the process retains control of the CPU until it completes. However, this may block higher-priority processes.

**2) Test-and-Set Instruction (TAS)**: A hardware-supported solution where a single atomic instruction reads and writes to a shared variable in an indivisible manner.

```pseudocode
function Test_and_Set(lock):
    temp = lock;
    lock = true;
    return temp;
```

This solution works for any number of processes, allowing only one to enter the critical section at a time by setting a lock. All other processes are blocked until the lock is released.


### 4. Semaphores

#### 1. **Challenges with Previous Solutions**
The previously discussed solutions to process synchronization have limitations:
1. They cannot be generalized to an unlimited number of processes.
2. They are not adaptable to general synchronization problems.
3. They introduce the issue of **busy-waiting** when a process is in its critical section (resulting in wasted CPU time).

Thus, we need a mechanism that can **block** a process if the condition for entering the critical section (S.C) is not met and **wake it up** once the condition is satisfied.

#### 2. **Semaphores (Dijkstra, 1965)**
A **semaphore** is an integer variable associated with a queue of processes. The semaphore variable can take positive, zero, or negative values, though it is always initialized to a non-negative number. The queue's management is often FIFO (First In, First Out), although this is not mandatory.

A semaphore is manipulated using three primitives:

- **INIT(s, n):**
  ```text
  Begin
    S := n; 
    F(s) := Ø;
  End;
  ```

- **P(S):** Decrement the semaphore by 1. If the result is negative, block the process.
  ```text
  Begin
    S := S - 1;
    If S < 0 then 
      Process state (P) := blocked; 
      Put P into the queue f(s);
      [Call the scheduler to select another process]
    EndIf;
  End;
  ```

- **V(S):** Increment the semaphore by 1. If the result is zero or negative, wake up one blocked process from the queue.
  ```text
  Begin
    S := S + 1;
    If S <= 0 then 
      Remove a process from f(s); 
      Process state := ready;
    EndIf;
  End;
  ```

**Note:** The execution of `P` and `V` must be atomic, meaning they cannot be interrupted.

#### 3. **Types of Semaphores**

##### A. **Binary Semaphore**
- Initial value: `1`
- Used for **mutual exclusion**. It ensures that only one process can access the critical section at a time.
  
  ```text
  Process Pi
  Begin
    P(S);
    <Critical Section>;
    V(S);
  End;
  ```

##### B. **Private Semaphore**
- Initial value: `0`
- Used when a process voluntarily blocks itself. A common use case is when one process must finish its part of a task before another process begins.
  
  **Example:**
  ```text
  Semaphore s initialized to 0;
  
  Process P1:
  Begin
    <Complete part one>;
    V(S);
  End;
  
  Process P2:
  Begin
    P(S);
    <Begin part two>;
  End;
  ```

##### C. **Counting Semaphore**
- Initial value: `n > 1`
- Used when multiple processes need to access a resource with `n` access points. The first `n` processes will pass without blocking, but subsequent processes will block until a resource is freed.
  
  ```text
  Semaphore s initialized to n;
  
  Process Pi:
  Begin
    P(S);
    <Use the resource>;
    V(S);
  End;
  ```

#### 4. **Interprocess Communication (IPC) and Synchronization**
Processes not only compete for resources but also **cooperate** to achieve shared tasks, requiring communication tools like shared memory and message passing for synchronization.

##### A. **Producer/Consumer Model**
In this model, **producers** generate information consumed by **consumers**. Buffers are used to store the produced items temporarily. If the buffer is full, producers must wait; if the buffer is empty, consumers must wait.

**Example: Single Producer/Single Consumer with Circular Buffer**
```text
nbplein := 0; % Semaphore for blocking consumer if buffer is empty %
nbvide := n;  % Semaphore for counting available spaces in the buffer %

Process Producer:
Begin
  Repeat
    P(nbvide);
    Deposit(item);
    V(nbplein);
  Until false;
End;

Process Consumer:
Begin
  Repeat
    P(nbplein);
    Remove(item);
    V(nbvide);
  Until false;
End;
```

- The buffer operates in a **circular** manner with two pointers:
  - `t`: Points to the first filled slot.
  - `q`: Points to the first empty slot.

##### B. **Readers/Writers Problem**
This scenario involves two types of processes:
- **Readers**: Can access the shared resource simultaneously.
- **Writers**: Need exclusive access to the shared resource.

The resource is a **critical section** for writers, so if a writer is accessing the resource, no other process (reader or writer) can access it. Multiple readers can access the resource concurrently.

**Example: No Priority Scheme**
```text
nl := 0;  % Counter for the number of active readers %
mutex := 1;  % Semaphore for protecting nl %
w := 1;  % Semaphore for exclusive access to the resource %

Process Reader:
Begin
  Repeat
    P(mutex);
    nl := nl + 1;
    If nl == 1 then P(w); EndIf;
    V(mutex);
    <Read>;
    P(mutex);
    nl := nl - 1;
    If nl == 0 then V(w); EndIf;
    V(mutex);
  Until false;
End;

Process Writer:
Begin
  Repeat
    P(w);
    <Write>;
    V(w);
  Until false;
End;
```


Semaphores provide a powerful mechanism for synchronizing processes, especially in managing shared resources. They prevent race conditions and ensure proper mutual exclusion, allowing for cooperative and competitive interactions between processes.

