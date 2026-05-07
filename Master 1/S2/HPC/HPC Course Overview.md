---
tags: [hpc, overview, course-map]
---

# HPC Course — One-Night Mastery Vault

> [!info] How to Use This Vault
> This is an **Obsidian vault** designed for rapid, structured mastery of High Performance Computing fundamentals. Each chapter is split into focused notes connected by `[[wikilinks]]`. Start from the top and follow the links, or jump to any note that interests you.

---

## Course Structure at a Glance

```text
HPC Course
│
├── Chapter 1 ── Performance Measurement and Algorithmic Optimization
│   ├── 1.1 HPC Basics and Speedup
│   ├── 1.2 Profiling and Timing Tools
│   └── 1.3 Algorithmic Optimization Exercises
│
├── Chapter 2 ── Cluster Computing and SSH
│   ├── 2.1 SSH and HPC Environments
│   ├── 2.2 Remote Execution and File Transfer
│   └── 2.3 Hardware vs Software — Fairness in Comparison
│
└── Chapter 3 ── Shared-Memory Parallelism with OpenMP
    ├── 3.1 OpenMP and the Fork-Join Model
    ├── 3.2 Synchronization and Race Conditions
    ├── 3.3 Loop Scheduling and Load Balancing
    └── 3.4 OpenMP Applied Exercises
```

---

## Learning Objectives (All Labs Combined)

- **Measure** execution time correctly (wall-clock vs CPU time) and compute speedup.
- **Profile** Python and C code to identify bottlenecks using `cProfile` and `gprof`.
- **Optimize** algorithms using Big-O analysis, mathematical formulas, and better data structures.
- **Connect** to remote HPC clusters via SSH, transfer files with SCP, and set up key-based authentication.
- **Parallelize** C code with OpenMP using `parallel`, `parallel for`, `reduction`, `atomic`, and `critical`.
- **Identify and fix** race conditions using synchronization primitives.
- **Choose** appropriate scheduling strategies (`static`, `dynamic`, `guided`) based on workload characteristics.

---

## Recommended Reading Order

1. [[1.1 HPC Basics and Speedup]] → [[1.2 Profiling and Timing Tools]] → [[1.3 Algorithmic Optimization Exercises]]
2. [[2.1 SSH and HPC Environments]] → [[2.2 Remote Execution and File Transfer]] → [[2.3 Hardware vs Software — Fairness in Comparison]]
3. [[3.1 OpenMP and the Fork-Join Model]] → [[3.2 Synchronization and Race Conditions]] → [[3.3 Loop Scheduling and Load Balancing]] → [[3.4 OpenMP Applied Exercises]]

---

*Course: High Performance Computing — University of Boumerdes, Semester 2 (2025/2026)*
*Instructor: Dr. Tayeb BENZENATI*
