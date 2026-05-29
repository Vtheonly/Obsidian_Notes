This is one of the most important concepts in computer science, and it is a **classic "trick"** that computer science professors put on exams to see if you are paying attention. 

The way you pass variables to a function completely changes how much work the computer has to do *before the function even starts running*.

Here is a simple, real-world explanation of why **Pass by Reference** costs $2$ operations, while **Pass by Value** costs $n^2$ operations.

---

This is one of the most important concepts in computer science, and it is a **classic "trick"** that computer science professors put on exams to see if you are paying attention. 

The way you pass variables to a function completely changes how much work the computer has to do *before the function even starts running*.

Here is a simple, real-world explanation of why **Pass by Reference** costs $2$ operations, while **Pass by Value** costs $n^2$ operations.

---

### 1. Pass by Reference (The "Google Doc" Method)
When a variable is passed by **reference**, the computer does **not** give the function the actual data. Instead, it gives the function the **memory address** (the location) of where the data is stored.

*   **The Analogy:** Imagine you wrote a massive, 10,000-page book on Google Docs. Your friend wants to read it. Do you print out all 10,000 pages and hand them a heavy box? No. You just **send them the URL link**. Sending the link takes 1 second, no matter how big the book is. 
*   **How the Computer does it:** The computer sends a "pointer" (a single memory address). 
*   **The Complexity:**
    *   Passing the URL/Pointer for the matrix `M` = **1 operation**
    *   Passing the integer `n` = **1 operation**
    *   Total Cost = **2 operations**. 
    *   *It is constant time $\mathcal{O}(1)$. The size of the matrix does not matter.*

---

### 2. Pass by Value (The "Photocopy" Method)
When a variable is passed by **value**, the computer must protect the original data. It does this by creating a **brand new, completely independent copy** of the data in memory for the function to use.

*   **The Analogy:** You wrote a 10,000-page book, but it's a physical book. Your friend wants to read it, but you are afraid they will draw on it with a pen. So, you go to a copy machine and **photocopy every single page, one by one**. If the book is 10 pages, it takes 10 seconds. If the book is 10,000 pages, it takes 10,000 seconds.
*   **How the Computer does it:** The computer literally loops through every single cell of the matrix and copies the number into a new space in RAM.
*   **The Complexity:**
    *   The matrix $M$ has $n$ rows and $n$ columns. Total elements = $n \times n = n^2$.
    *   The computer must copy $n^2$ elements. This takes **$n^2$ operations**.
    *   Passing the integer `n` = **1 operation**.
    *   Total Cost = **$n^2 + 1$ operations**.
    *   *The larger the matrix, the longer this takes. This alone is $\mathcal{O}(n^2)$.*

---

### How this ruins the "Best Case" in your exam
Look at how this rule completely changes the answer for the **Best Case ($C_{min}$)** in the exams.

Imagine the algorithm is searching for the number `0`. The number `0` happens to be in the very first cell `M[1][1]`.

*   **If Passed by Reference (Pages 1-2):**
    The computer sends the URL (2 operations). The algorithm checks `M[1][1]`, sees the `0`, and stops immediately. 
    **Total time:** Just a few operations. The best case is incredibly fast: **$\mathcal{O}(1)$ or $\mathcal{O}(n)$**.

*   **If Passed by Value (Pages 3-4):**
    Before the algorithm is even allowed to look at `M[1][1]`, the computer says *"Wait! I have to photocopy the entire matrix first!"* It spends $n^2$ operations copying the matrix. *Then* the algorithm checks `M[1][1]`, sees the `0`, and stops.
    **Total time:** Even though the search was instant, the setup took $n^2$ operations. The best case is severely slowed down to **$\mathcal{O}(n^2)$**.

**Summary:** The professor is testing to see if you remember that "Pass by Value" forces the computer to run a hidden `for` loop to copy the array before the actual code begins!
When a variable is passed by **reference**, the computer does **not** give the function the actual data. Instead, it gives the function the **memory address** (the location) of where the data is stored.

*   **The Analogy:** Imagine you wrote a massive, 10,000-page book on Google Docs. Your friend wants to read it. Do you print out all 10,000 pages and hand them a heavy box? No. You just **send them the URL link**. Sending the link takes 1 second, no matter how big the book is. 
*   **How the Computer does it:** The computer sends a "pointer" (a single memory address). 
*   **The Complexity:**
    *   Passing the URL/Pointer for the matrix `M` = **1 operation**
    *   Passing the integer `n` = **1 operation**
    *   Total Cost = **2 operations**. 
    *   *It is constant time $\mathcal{O}(1)$. The size of the matrix does not matter.*

---

### 2. Pass by Value (The "Photocopy" Method)
When a variable is passed by **value**, the computer must protect the original data. It does this by creating a **brand new, completely independent copy** of the data in memory for the function to use.

*   **The Analogy:** You wrote a 10,000-page book, but it's a physical book. Your friend wants to read it, but you are afraid they will draw on it with a pen. So, you go to a copy machine and **photocopy every single page, one by one**. If the book is 10 pages, it takes 10 seconds. If the book is 10,000 pages, it takes 10,000 seconds.
*   **How the Computer does it:** The computer literally loops through every single cell of the matrix and copies the number into a new space in RAM.
*   **The Complexity:**
    *   The matrix $M$ has $n$ rows and $n$ columns. Total elements = $n \times n = n^2$.
    *   The computer must copy $n^2$ elements. This takes **$n^2$ operations**.
    *   Passing the integer `n` = **1 operation**.
    *   Total Cost = **$n^2 + 1$ operations**.
    *   *The larger the matrix, the longer this takes. This alone is $\mathcal{O}(n^2)$.*

---

### How this ruins the "Best Case" in your exam
Look at how this rule completely changes the answer for the **Best Case ($C_{min}$)** in the exams.

Imagine the algorithm is searching for the number `0`. The number `0` happens to be in the very first cell `M[1][1]`.

*   **If Passed by Reference (Pages 1-2):**
    The computer sends the URL (2 operations). The algorithm checks `M[1][1]`, sees the `0`, and stops immediately. 
    **Total time:** Just a few operations. The best case is incredibly fast: **$\mathcal{O}(1)$ or $\mathcal{O}(n)$**.

*   **If Passed by Value (Pages 3-4):**
    Before the algorithm is even allowed to look at `M[1][1]`, the computer says *"Wait! I have to photocopy the entire matrix first!"* It spends $n^2$ operations copying the matrix. *Then* the algorithm checks `M[1][1]`, sees the `0`, and stops.
    **Total time:** Even though the search was instant, the setup took $n^2$ operations. The best case is severely slowed down to **$\mathcal{O}(n^2)$**.

**Summary:** The professor is testing to see if you remember that "Pass by Value" forces the computer to run a hidden `for` loop to copy the array before the actual code begins!