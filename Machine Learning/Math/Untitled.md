Here is the explanation rewritten in **MathJax** format for clarity and better compatibility with tools like **Obsidian**:

---

## **Basic Solutions and Matrix Invertibility**

### **1. Basic Solutions**

Given a matrix AA that is **square** (same number of rows and columns) and **invertible**:

- We solve the system Ax=bA \mathbf{x} = \mathbf{b} for x\mathbf{x} (unknowns).
- To find a **basic solution**:
    
    - Some variables xjx_j are set to 00 (non-basic variables).
    - The remaining variables xBx_B are solved using the formula: xB=AB−1bx_B = A_B^{-1} \mathbf{b}
    
    where ABA_B is the submatrix corresponding to the basic variables.

---

### **2. Matrix Invertibility**

A matrix AA is **invertible** if and only if its determinant is **non-zero**:

det⁡(A)≠0\det(A) \neq 0

For a square matrix AA, the inverse A−1A^{-1} is given by:

A−1=1det⁡(A)⋅com⁡(A)TA^{-1} = \frac{1}{\det(A)} \cdot \operatorname{com}(A)^T

where com⁡(A)\operatorname{com}(A) is the cofactor matrix of AA.

---

### **3. Inverse of a 2×22 \times 2 Matrix**

For a 2×22 \times 2 matrix:

A=[abcd]A = \begin{bmatrix} a & b \\ c & d \end{bmatrix}

1. **Find the determinant**:
    
    det⁡(A)=ad−bc\det(A) = ad - bc
2. **Find the cofactor matrix** (com⁡(A)\operatorname{com}(A)):
    
    com⁡(A)=[+d−b−c+a]\operatorname{com}(A) = \begin{bmatrix} +d & -b \\ -c & +a \end{bmatrix}
3. **Transpose the cofactor matrix**:
    
    com⁡(A)T=[d−c−ba]\operatorname{com}(A)^T = \begin{bmatrix} d & -c \\ -b & a \end{bmatrix}
4. **Divide by the determinant**:
    
    A−1=1det⁡(A)⋅com⁡(A)TA^{-1} = \frac{1}{\det(A)} \cdot \operatorname{com}(A)^T

---

### **Example**

Let AA be:

A=[2134]A = \begin{bmatrix} 2 & 1 \\ 3 & 4 \end{bmatrix}

1. **Compute the determinant**:
    
    det⁡(A)=(2)(4)−(1)(3)=8−3=5\det(A) = (2)(4) - (1)(3) = 8 - 3 = 5
2. **Find the cofactor matrix**:
    
    com⁡(A)=[+4−1−3+2]\operatorname{com}(A) = \begin{bmatrix} +4 & -1 \\ -3 & +2 \end{bmatrix}
3. **Transpose the cofactor matrix**:
    
    com⁡(A)T=[4−3−12]\operatorname{com}(A)^T = \begin{bmatrix} 4 & -3 \\ -1 & 2 \end{bmatrix}
4. **Divide by the determinant**:
    
    A−1=15⋅[4−3−12]A^{-1} = \frac{1}{5} \cdot \begin{bmatrix} 4 & -3 \\ -1 & 2 \end{bmatrix}
5. **Simplify**:
    
    A−1=[45−35−1525]A^{-1} = \begin{bmatrix} \frac{4}{5} & -\frac{3}{5} \\ -\frac{1}{5} & \frac{2}{5} \end{bmatrix}

---

### **Summary**

1. A matrix AA is invertible if det⁡(A)≠0\det(A) \neq 0.
2. To compute the inverse of a 2×22 \times 2 matrix: A−1=1det⁡(A)⋅com⁡(A)TA^{-1} = \frac{1}{\det(A)} \cdot \operatorname{com}(A)^T
3. To solve for a basic solution in Ax=bA \mathbf{x} = \mathbf{b}: xB=AB−1bx_B = A_B^{-1} \mathbf{b}

Let me know if you need additional clarification or further examples!