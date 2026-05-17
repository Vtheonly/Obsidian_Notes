# Chapter 4. Synchronization and Mutual Exclusion

## 1. Race Conditions and Critical Regions
When you cannot break a dependency or use a reduction, you must enforce **Mutual Exclusion**—ensuring only one thread can access a resource at a time.

### `#pragma omp critical`
A Critical Region defines a block of code that allows only one thread to enter at a time.
* If Thread 1 is inside the critical block, Thread 2 must pause and wait outside until Thread 1 completely exits the block.
* **Pros:** Can contain any valid C code, multiple variables, array updates, or heavy function calls.
* **Cons (The Serialization Trap):** It forces parallel threads to operate sequentially. If heavily used inside a loop, it will completely destroy your performance, making the code run *slower* than a non-parallelized program due to locking overhead.

```c
#pragma omp parallel
{
    double local_res = do_heavy_math();
    
    #pragma omp critical
    {
        // Only one thread allowed in here at a time!
        global_sum += local_res;
        log_to_file("Added to sum");
    }
}
```

---

## 2. Atomic Operations
For incredibly simple operations (like incrementing a counter), using a `critical` block is overkill. Instead, we use `#pragma omp atomic`.

### How it works
Atomic operations do not use software locks. They leverage specialized, low-level **Hardware Instructions** on the CPU to ensure the memory update happens in a single, uninterruptible clock cycle.

* **Restrictions:** It only applies to the **single statement** immediately following it. It only supports basic updates: `x++`, `x += expr`, `x *= expr`, etc.
* **Performance:** Vastly superior to `critical`.

> [!TIP] The Hierarchy of Choice
> When faced with a shared variable update, follow this order of preference:
> 1. Can I use a **Reduction**? If yes, do it. It is the fastest.
> 2. Can I use an **Atomic** operation? If yes, use it.
> 3. Use **Critical** only as a last resort for complex logic.

---

## 3. Barriers and Execution Constraints

### The Barrier Concept
A barrier is a synchronization point where threads must stop and wait. No thread is allowed to execute the code past the barrier until *every single thread* in the team has arrived at the barrier.

**Implicit Barriers:**
OpenMP is designed to be safe by default. It automatically inserts hidden barriers at the end of:
* `#pragma omp parallel` regions.
* `#pragma omp for` loops.
* `#pragma omp single` blocks.

**Explicit Barriers:**
If you have complex logic requiring synchronization *inside* a continuous parallel block, you can manually trigger one:
`#pragma omp barrier`

### Thread-Specific Constraints: `master` vs `single`
Sometimes, you want only one thread to do a specific job (like printing a report or initializing a library) while the rest of the team is active.

1. **`#pragma omp master`**
   * Executes **only** by Thread 0.
   * **NO implicit barrier** at the end. The other threads will simply skip this block and keep running at full speed.
2. **`#pragma omp single`**
   * Executes by the **first thread that arrives** at the block (could be T0, T3, whoever gets there first).
   * **HAS an implicit barrier** at the end. All other threads will wait at the end of this block until the chosen thread finishes the task.

### Removing Barriers: The `nowait` clause
If you have two completely independent loops back-to-back, the implicit barrier at the end of the first loop is a waste of time. You can remove it using the `nowait` clause.

```c
#pragma omp parallel
{
    // Threads will finish their chunk of this loop, and immediately move on.
    #pragma omp for nowait
    for(int i=0; i<N; i++) A[i] = i*2;
    
    // SAFE: Array B only relies on Array C, not Array A.
    #pragma omp for
    for(int i=0; i<N; i++) B[i] = C[i] + 5; 
}
```

> [!WARNING] The Danger of Nowait
> Only use `nowait` if there are absolutely ZERO data dependencies between the two loops. If Loop 2 tries to read a variable calculated in Loop 1, and a fast thread has bypassed the barrier, it will read uncalculated, garbage data!
