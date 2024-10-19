#### 1. Introduction
Monitors, a synchronization primitive introduced by Hoare (1974) and Brinch Hansen (1975), were designed to simplify the development of correct concurrent programs. A monitor is a set of procedures, variables, and data structures grouped within a special module. One of the most significant properties of monitors is that they ensure **mutual exclusion**, meaning only one process can be active inside a monitor at any given time.

Monitors differ from traditional programming structures in that the compiler treats them specially. When a process calls a procedure within a monitor, the first instructions check if another process is already active within the monitor. If another process is active, the calling process is suspended until the current process finishes and exits. If no process is using the monitor, the calling process can enter. Mutual exclusion in monitors is handled by the compiler, often using a **binary semaphore**.

This design ensures that the programmer no longer needs to explicitly manage mutual exclusion. All critical sections can be included in the monitor’s procedures, guaranteeing that no two processes will enter a critical section simultaneously.

#### 2. Definition of Monitors
Monitors are defined by the following components:

1. **Synchronization Variables:** These variables manage the synchronization of processes.
2. **Primitives:**
   - **External Primitives (Entry Points):** These manipulate resources on which processes synchronize. They are accessible outside the monitor.
   - **Internal Primitives:** Only accessible from within the monitor.
3. **One or More Wait Queues:** These queues hold processes waiting for the monitor to become available.

**Structure of a Monitor:**
```plaintext
Monitor_Name : monitor;
begin
    declaration of local variables (shared resources)
    declaration of procedure bodies within the monitor
    initialization of local variables
end
```

**Example 1:**
Incrementing a shared variable `N` by multiple processes.

```plaintext
Increment : monitor;
var
    N : integer;

Procedure increment
begin
    N := N + 1;
end;

% Initialization %
N := 0;
```

Processes that want to increment the value of `N` no longer execute `N := N + 1` directly. Instead, they call the `increment` procedure within the monitor:
```plaintext
Pi
Repeat
    Increment.increment;
Until false;
```

The format for calling procedures within a monitor is: `Monitor_Name.Procedure_Name`.

#### Advantages of Monitors
1. **Centralized Critical Sections:** Instead of being scattered across different processes, critical sections are transformed into functions or procedures within the monitor.
2. **Automated Synchronization:** The user no longer has to manage the synchronization of critical sections. The monitor’s implementation guarantees that only one process can access it at a time. The entire monitor functions like a critical section. If a process needs to operate on a shared variable, it simply calls a monitor procedure. If the monitor is occupied, the process is blocked in a queue. When the monitor is free, a waiting process is chosen to proceed.

#### 3. Condition Variables
A **condition variable** does not hold a value and cannot be initialized. It is declared within the monitor like this:
```plaintext
X : condition;
```

This variable represents a queue of waiting processes and is manipulated only inside the monitor using three operations:
1. `X.wait`: Suspends the calling process and places it in the queue for `X`.
2. `X.signal`: Wakes up one process waiting on `X`. If no process is waiting, `signal` has no effect.
3. `X.empty`: A Boolean function that returns `false` if at least one process is waiting on `X`.

**Remarks:**
1. If process `P1` calls `X.signal` and wakes up process `P2`, one of these processes must wait to ensure only one is active in the monitor at a time.
2. A process awakened by `signal` resumes execution from the instruction following the `wait` it had previously executed.

**Example 2:**
Allocating a resource with a single point of access for multiple processes.

```plaintext
allocator : monitor;
var
    occupied : boolean;
    free : condition;

Procedure acquire
begin
    if occupied then free.wait;
    occupied := true;
end;

Procedure release
begin
    occupied := false;
    free.signal;
end;

% Initialization %
begin
    occupied := false;
end;
```

**Example 3:**
Managing a class of resources with `N` access points, where each process requests only one resource at a time.

```plaintext
Resource_Allocator : monitor;
var
    N : integer;
    C : condition;

Procedure request
begin
    if (N = 0) then C.wait;
    N := N - 1;
end;

Procedure release
begin
    N := N + 1;
    C.signal;
end;

% Initialization %
begin
    N := K; % where K is the number of resources
end;
```

---

Monitors are a powerful abstraction for managing concurrency, ensuring both safety and liveness by automating the mutual exclusion of critical sections.