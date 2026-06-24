---
tags: [chapter-2, threading-models, scheduler-activations, popup-threads]
chapter: 2
---

# Chapter 2 — Multi-threading Models and Systems

> **Chapter purpose.** Chapter 1 established what a thread *is*. This chapter examines the **mapping between user-visible threads and kernel-managed execution contexts**. The choice of mapping has profound consequences: it determines whether your program can use multiple cores, whether a single blocking call freezes all threads, and how fast context switches are. We also cover two advanced architectures — **scheduler activations** and **pop-up threads** — that demonstrate how OS designers have tried to combine the best of user-level and kernel-level threading.

---

## What This Chapter Covers

```
Chapter 2: Multi-threading Models and Systems
    - 2.1. Threading Models and Thread Tables
    - 2.2. Scheduler Activations and Upcall Architecture
    - 2.3. Distributed Systems and Pop-Up Thread Design
```

### 2.1. Threading Models and Thread Tables
The three classic models: **many-to-one** (user-level threads), **one-to-one** (kernel-level threads), and **many-to-many** (hybrid). For each, we examine where the thread table lives, what happens on a blocking system call, and whether true parallelism is possible.

### 2.2. Scheduler Activations and Upcall Architecture
A clever design from the 1990s that tried to give user-level libraries the speed of user threads plus the parallelism of kernel threads. The kernel communicates with the user-space scheduler via **upcalls** — kernel-to-user function calls that notify the library of blocking events.

### 2.3. Distributed Systems and Pop-Up Thread Design
A different concern: in high-throughput network servers, the cost of waking up an idle worker thread can dominate latency. **Pop-up threads** are created from scratch for each incoming request, avoiding the cost of restoring a pre-existing thread's state.

---

## How This Chapter Connects to the Rest of the Course

```mermaid
graph LR
    Ch1["Chapter 1<br/>Foundations"] -->|"Defines thread/PCB/TCB"| Ch2["Chapter 2<br/>Threading Models"]
    Ch2 -->|"One-to-one model assumed"| Ch3["Chapter 3<br/>pthreads Exercises"]
    Ch2 -->|"User vs kernel threads<br/>drives conversion issues"| Ch4["Chapter 4<br/>Conversion Challenges"]
    Ch2 -->|"Modern languages use one-to-one"| Ch5["Chapter 5<br/>Python & C++"]
```

The key insight from Chapter 2 that propagates forward: **Python, C++, Java, and almost all modern languages use the one-to-one model.** Every Python `threading.Thread` and every C++ `std::thread` is backed by a real OS kernel thread. The many-to-one and many-to-many models are mostly of historical interest — but understanding them is essential for understanding the design trade-offs of modern systems.

---

## Three Models at a Glance

```mermaid
graph TB
    subgraph "Many-to-One"
        U1A["User Thread 1"] --> RTS1["Run-Time System"]
        U1B["User Thread 2"] --> RTS1
        U1C["User Thread 3"] --> RTS1
        RTS1 --> K1A["1 Kernel Thread"]
    end
    subgraph "One-to-One"
        U2A["User Thread 1"] --> K2A["Kernel Thread 1"]
        U2B["User Thread 2"] --> K2B["Kernel Thread 2"]
    end
    subgraph "Many-to-Many"
        U3A["User Thread 1"] --> K3A["Kernel Thread 1"]
        U3B["User Thread 2"] --> K3A
        U3C["User Thread 3"] --> K3B["Kernel Thread 2"]
    end
```

| Property | Many-to-One | One-to-One | Many-to-Many |
| :--- | :--- | :--- | :--- |
| Thread table location | User space | Kernel space | Both |
| Blocking system call | Blocks ALL threads | Blocks one thread | Blocks one thread (with scheduler activations) |
| True parallelism | No | Yes | Yes |
| Context switch speed | Fastest (user-space) | Slowest (kernel) | Mixed |
| Implementation complexity | Easy | Medium | Hard |

---

**Next:** Open `2.1. Threading Models and Thread Tables.md`.
