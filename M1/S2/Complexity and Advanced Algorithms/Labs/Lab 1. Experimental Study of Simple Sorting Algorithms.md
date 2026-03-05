
## 🎯 1. Lab Objectives
This practical session bridges the gap between theoretical algorithmic complexity and physical execution time. The main goals are:
1. **Understand and implement** three basic iterative sorting algorithms: Selection Sort, Insertion Sort, and Bubble Sort.
2. **Benchmark performance** by measuring execution time on arrays of vastly different sizes ($N=100$ to $N=100,000$).
3. **Master C basics for benchmarking**, specifically using `<time.h>` for execution time and `<stdlib.h>` for random data generation.
4. **Compare theoretical vs. empirical complexity**: Prove that an $O(n^2)$ algorithm practically scales quadratically.

---

## 🧠 2. Theoretical Background & Pseudocode Translation

> [!warning] CRITICAL PITFALL: 1-Based vs 0-Based Indexing
> The pseudocode provided in the lab uses **1-based indexing** (arrays start at index 1 and end at index $n$). However, the **C programming language uses 0-based indexing** (arrays start at 0 and end at $n-1$). 
> *If you copy the pseudocode directly into C, your program will crash with a "Segmentation Fault" because it will try to access `T[n]`, which is out of bounds!*

### 2.1. Selection Sort (Tri par sélection)
**Concept:** The array is divided into a sorted left part and an unsorted right part. At each step, we scan the entire unsorted part to find the absolute minimum value, and we swap it with the first element of the unsorted part.

*   **Pseudocode (1-based):** `for i = 1 to n-1`, `for j = i+1 to n`
*   **C Implementation (0-based):** `for i = 0 to n-2`, `for j = i+1 to n-1`
*   **Theoretical Complexity:** $O(n^2)$ in Best, Average, and Worst cases. It *always* does the exact same number of comparisons regardless of the data.

### 2.2. Insertion Sort (Tri par insertion)
**Concept:** Imagine sorting a hand of playing cards. You pick up one card at a time and insert it into its correct position among the cards you are already holding. It shifts larger elements to the right to make room.

*   **Pseudocode (1-based):** `for i = 2 to n`, `while j >= 1`
*   **C Implementation (0-based):** `for i = 1 to n-1`, `while j >= 0`
*   **Theoretical Complexity:** 
    *   *Worst/Average Case:* $O(n^2)$ (Array is reversed or random).
    *   *Best Case:* $O(n)$ (Array is already sorted). 

### 2.3. Bubble Sort (Tri à bulles)
**Concept:** Repeatedly step through the list, compare adjacent pairs, and swap them if they are in the wrong order. The largest unsorted element "bubbles" up to its correct position at the end of the array in each pass.

*   **Pseudocode (1-based):** `for i = 1 to n-1`, `for j = 1 to n-i`
*   **C Implementation (0-based):** `for i = 0 to n-2`, `for j = 0 to n-2-i`
*   **Theoretical Complexity:** $O(n^2)$ Worst/Average. 

---

## ⚙️ 3. Essential C Mechanisms for Benchmarking

To build a rigorous scientific benchmark, you need to understand two C libraries thoroughly:

### A. Generating Random Numbers (`<stdlib.h>` & `<time.h>`)
Computers cannot generate truly random numbers; they use mathematical formulas to generate *pseudo-random* sequences.
*   **`rand()`**: Returns a pseudo-random integer.
*   **`srand(seed)`**: Sets the starting point (seed) for the formula. 
> [!danger] The Seed Mistake
> If you do not call `srand()`, `rand()` will produce the **exact same sequence** of numbers every time you run the program! To fix this, we use the current time as the seed: `srand(time(NULL));`. This must be called **only once** at the very beginning of the `main()` function.

### B. Measuring CPU Time (`<time.h>`)
We want to measure how much time the CPU spent executing *our sorting function*, excluding time spent generating the arrays.
*   `clock_t`: A special type representing processor clock ticks.
*   `clock()`: Returns the number of clock ticks since the program started.
*   **Formula:** `(double)(end - start) / CLOCKS_PER_SEC` converts ticks into human-readable seconds.

```mermaid
flowchart LR
    A[Start Timer: clock()] --> B[Run Sorting Algorithm]
    B --> C[Stop Timer: clock()]
    C --> D[Calculate: end - start]
    D --> E[Divide by CLOCKS_PER_SEC]
```

### C. The Stack Overflow Threat (`malloc`)
The lab asks us to sort an array of size $100,000$. 
If you write `int T[100000];` inside a function, the compiler tries to put it on the **Stack memory**, which is typically limited to 1MB - 8MB. An array of 100,000 integers takes $100,000 \times 4 \text{ bytes} = 400 \text{ KB}$, which is risky and might cause a **Stack Overflow** crash if multiple arrays are declared.
*   **The Professional Solution:** Use **Heap memory** via dynamic allocation: `int *T = (int *)malloc(n * sizeof(int));`. Don't forget to `free(T)` at the end!

---

## 💻 4. The Complete, Bug-Free C Implementation

This code satisfies all parts of the lab: it implements the algorithms, generates random data, executes 30 times for sizes 100, 1000, 10000, and 100000, and calculates the true average.

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// ==========================================
// 1. SORTING ALGORITHMS
// ==========================================

// Selection Sort
void SelectionSort(int T[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int min = i;
        for (int j = i + 1; j < n; j++) {
            if (T[j] < T[min]) {
                min = j;
            }
        }
        // Swap T[i] and T[min]
        int temp = T[i];
        T[i] = T[min];
        T[min] = temp;
    }
}

// Insertion Sort
void InsertionSort(int T[], int n) {
    for (int i = 1; i < n; i++) {
        int x = T[i];
        int j = i - 1;
        // Shift elements to the right to make room for x
        while (j >= 0 && T[j] > x) {
            T[j + 1] = T[j];
            j = j - 1;
        }
        T[j + 1] = x;
    }
}

// Bubble Sort
void BubbleSort(int T[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - 1 - i; j++) {
            if (T[j] > T[j + 1]) {
                // Swap T[j] and T[j+1]
                int temp = T[j];
                T[j] = T[j + 1];
                T[j + 1] = temp;
            }
        }
    }
}

// ==========================================
// 2. HELPER FUNCTIONS
// ==========================================

// Fills an array with random numbers from 0 to 9999
void GenerateRandomArray(int T[], int n) {
    for (int i = 0; i < n; i++) {
        T[i] = rand() % 10000; 
    }
}

// Copies src array into dest array
// Crucial: We must sort the EXACT SAME random array for all 3 algorithms to be fair!
void CopyArray(int src[], int dest[], int n) {
    for (int i = 0; i < n; i++) {
        dest[i] = src[i];
    }
}

// ==========================================
// 3. MAIN BENCHMARKING PROGRAM
// ==========================================
int main() {
    // Seed the random number generator ONCE
    srand(time(NULL)); 
    
    // Test parameters according to the lab
    int sizes[] = {100, 1000, 10000, 100000};
    int num_sizes = 4;
    int runs = 30; // 30 executions per size for a valid average
    
    printf("Starting Benchmark (Average of %d executions)...\n\n", runs);
    
    for (int s = 0; s < num_sizes; s++) {
        int n = sizes[s];
        
        // Accumulators for total time
        double total_selection = 0.0;
        double total_insertion = 0.0;
        double total_bubble = 0.0;
        
        // Dynamic memory allocation to prevent Stack Overflow on N=100000
        int *T_original = (int*)malloc(n * sizeof(int));
        int *T_test     = (int*)malloc(n * sizeof(int));
        
        if (T_original == NULL || T_test == NULL) {
            printf("Memory allocation failed!\n");
            return 1;
        }
        
        for (int r = 0; r < runs; r++) {
            // Generate ONE random array for this run
            GenerateRandomArray(T_original, n);
            clock_t start, end;
            
            // --- 1. Test Selection Sort ---
            CopyArray(T_original, T_test, n); // Reset to unsorted
            start = clock();
            SelectionSort(T_test, n);
            end = clock();
            total_selection += ((double)(end - start)) / CLOCKS_PER_SEC;
            
            // --- 2. Test Insertion Sort ---
            CopyArray(T_original, T_test, n); // Reset to unsorted
            start = clock();
            InsertionSort(T_test, n);
            end = clock();
            total_insertion += ((double)(end - start)) / CLOCKS_PER_SEC;
            
            // --- 3. Test Bubble Sort ---
            CopyArray(T_original, T_test, n); // Reset to unsorted
            start = clock();
            BubbleSort(T_test, n);
            end = clock();
            total_bubble += ((double)(end - start)) / CLOCKS_PER_SEC;
        }
        
        // Calculate and display averages
        printf("Array Size (N) = %d\n", n);
        printf("  Selection Sort : %f seconds\n", total_selection / runs);
        printf("  Insertion Sort : %f seconds\n", total_insertion / runs);
        printf("  Bubble Sort    : %f seconds\n", total_bubble / runs);
        printf("----------------------------------------\n");
        
        // Free memory to prevent memory leaks
        free(T_original);
        free(T_test);
    }
    
    return 0;
}
```

---

## 📈 5. Empirical vs. Theoretical Complexity Analysis

Once you run the program, your output will look something like this (exact numbers depend on your CPU speed):

| Array Size ($N$) | Selection Sort (sec) | Insertion Sort (sec) | Bubble Sort (sec) |
| :--- | :--- | :--- | :--- |
| **100** | 0.000001 | 0.000001 | 0.000002 |
| **1,000** | 0.001200 | 0.000800 | 0.002500 |
| **10,000** | 0.115000 | 0.075000 | 0.280000 |
| **100,000** | 11.50000 | 7.500000 | 28.00000 |

### Part 5 Analysis: Bridging the Theory

**1. The Quadratic Scaling ($O(n^2)$) in Reality:**
Look at the jump from $N = 10,000$ to $N = 100,000$. 
*   The input size increased by a factor of **10** ($100,000 / 10,000 = 10$).
*   The execution time increased by a factor of roughly **100** ($11.5 / 0.115 = 100$).
*   **Conclusion:** This is the exact empirical proof of $O(n^2)$ complexity. Because time $T(n) \approx c \cdot n^2$, if you do $T(10n)$, the result is $c \cdot (10n)^2 = 100 \cdot c \cdot n^2 = 100 \cdot T(n)$.

**2. Why is Insertion Sort the fastest if they are all $O(n^2)$?**
Big-O notation ignores **constants**. Even though both are $O(n^2)$, the exact number of operations differs:
*   **Bubble Sort** does a massive number of writes (swaps require 3 assignments) to memory in the worst case. 
*   **Insertion Sort** only shifts elements (1 assignment) and writes the swapped element once at the end. Memory writes are "expensive" operations for a CPU. 
*   **Conclusion:** The constant factor $c$ in $c \cdot n^2$ is much smaller for Insertion Sort, making it highly efficient in practical, real-world scenarios for small or partially sorted arrays.
