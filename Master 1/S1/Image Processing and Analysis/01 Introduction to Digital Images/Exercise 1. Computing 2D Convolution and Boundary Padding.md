## Exercise 1: Computing 2D Convolution and Boundary Padding

### Problem Statement
Given an input $5 \times 5$ image channel $f(x, y)$ and a $3 \times 3$ high-pass filter kernel $h(i, j)$, calculate the filtered intensity of the central pixel $f(2, 2)$ using two boundary handling strategies:
1. **Zero Padding**
2. **Mirror Padding**

The input image $f(x, y)$ is:

$$f(x, y) = \begin{pmatrix} 
100 & 130 & 110 & 120 & 110 \\ 
110 & 90  & 100 & 90  & 100 \\ 
130 & 100 & 90  & 130 & 110 \\ 
120 & 100 & 130 & 110 & 120 \\ 
90  & 110 & 80  & 120 & 100 
\end{pmatrix}$$

The $3 \times 3$ high-pass filter kernel $h(i, j)$ is:

$$h(i, j) = \begin{pmatrix} 
-1 & -1 & -1 \\ 
-1 &  8 & -1 \\ 
-1 & -1 & -1 
\end{pmatrix}$$

---

### Solution Strategy
The central pixel of the image is at coordinates $(2, 2)$ (using 0-based indexing), which corresponds to the value $90$:

$$f(2, 2) = 90$$

Since the pixel is at the center of a $5 \times 5$ image, its $3 \times 3$ neighborhood is fully defined and does not touch the outer borders. Therefore, boundary padding is not required for this pixel. Let's select a pixel on the border, such as $f(0, 0) = 100$, to demonstrate how padding affects the convolution calculation.

#### local neighborhood centered at $f(0, 0)$ prior to padding:

$$\begin{array}{ccc} 
? & ? & ? \\ 
? & 100 & 130 \\ 
? & 110 & 90 
\end{array}$$

---

### Step-by-Step Convolution with Zero Padding

With zero padding, any coordinate index that falls outside the boundaries $[0, 4] \times [0, 4]$ is assigned an intensity of $0$.

#### 1. Define the Padded Neighborhood for $f(0, 0)$:

$$f_{\text{zero}} = \begin{pmatrix} 
0 & 0 & 0 \\ 
0 & 100 & 130 \\ 
0 & 110 & 90 
\end{pmatrix}$$

#### 2. Perform Element-wise Multiplication with Kernel $h(i, j)$:

$$\begin{aligned}
g(0, 0) = & (0 \times -1) + (0 \times -1) + (0 \times -1) \\
+ & (0 \times -1) + (100 \times 8) + (130 \times -1) \\
+ & (0 \times -1) + (110 \times -1) + (90 \times -1)
\end{aligned}$$

#### 3. Calculate the Sum:

$$g(0, 0) = 0 + 0 + 0 + 0 + 800 - 130 + 0 - 110 - 90$$

$$g(0, 0) = 800 - 330 = 470$$

---

### Step-by-Step Convolution with Mirror Padding

With mirror padding, the out-of-boundary values are filled by reflecting the image across its borders:
* $f(-1, -1) = f(1, 1) = 90$
* $f(-1, 0) = f(1, 0) = 110$
* $f(-1, 1) = f(1, 1) = 90$
* $f(0, -1) = f(0, 1) = 130$
* $f(1, -1) = f(1, 1) = 90$

#### 1. Define the Padded Neighborhood for $f(0, 0)$:

$$f_{\text{mirror}} = \begin{pmatrix} 
90  & 110 & 90 \\ 
130 & 100 & 130 \\ 
90  & 110 & 90 
\end{pmatrix}$$

#### 2. Perform Element-wise Multiplication with Kernel $h(i, j)$:

$$\begin{aligned}
g(0, 0) = & (90 \times -1) + (110 \times -1) + (90 \times -1) \\
+ & (130 \times -1) + (100 \times 8) + (130 \times -1) \\
+ & (90 \times -1) + (110 \times -1) + (90 \times -1)
\end{aligned}$$

#### 3. Calculate the Sum:

$$g(0, 0) = -90 - 110 - 90 - 130 + 800 - 130 - 90 - 110 - 90$$

$$g(0, 0) = 800 - 840 = -40$$

#### Summary of Results
* **Zero Padding:** $g(0, 0) = 470$
* **Mirror Padding:** $g(0, 0) = -40$

> **Key Takeaway:** Zero padding introduces an artificial, high-contrast dark border, causing the high-pass filter to output a large value ($470$). Mirror padding preserves the continuity of local intensities, producing a more accurate and stable result ($-40$).
