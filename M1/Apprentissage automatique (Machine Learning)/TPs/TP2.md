
### 1. Environment Setup Commands

For this lab, you'll need `numpy` for efficient numerical calculations and `matplotlib` for plotting the graphs.

**Step 1 & 2: Create and Activate your Virtual Environment**
(If you are continuing from the previous lab and the `venv` is already active, you can skip this part).

*On macOS or Linux:*
```bash
python3 -m venv venv
source venv/bin/activate
```

*On Windows:*
```bash
python -m venv venv
venv\Scripts\activate
```

**Step 3: Install Required Packages**
With your environment active (`(venv)` showing in the prompt), run the following command. We use the `python -m pip` method to avoid any potential `externally-managed-environment` errors.

```bash
python -m pip install numpy matplotlib
```
You are now ready to write the code.

---

### 2. Detailed README.md File

Copy this into a `README.md` file in your project folder. It explains the concepts behind both jobs in the lab.


# Lab 2: Formal Neuron - Solution Guide

This guide provides a complete solution and conceptual explanation for "Lab 2: Formal Neuron." The goal is to understand and implement the two core components of a single artificial neuron: its activation function and its computation process.

---

### **Job 1: Visualizing Activation Functions**

#### The Concept: What is an Activation Function?

In a neural network, a neuron computes a "weighted sum" of its inputs. The **activation function** then takes this sum and performs a transformation on it to produce the neuron's final output.

Its primary purpose is to introduce **non-linearity** into the network. Without non-linearity, no matter how many layers a neural network has, it would behave just like a single linear regression model, which cannot learn complex patterns in data.

#### The Functions We Will Visualize:

1.  **Binary Step:**
    *   **Formula:** `f(x) = 1 if x > 0 else 0`
    *   **Behavior:** A simple threshold function. If the input is positive, it "fires" (output 1); otherwise, it doesn't (output 0).
    *   **Use Case:** Rarely used in modern deep learning because its derivative is zero almost everywhere, which makes it impossible to train using gradient-based methods like backpropagation.

2.  **Linear:**
    *   **Formula:** `f(x) = x`
    *   **Behavior:** The output is simply equal to the input. It does not introduce non-linearity.
    *   **Use Case:** Primarily used in the output layer of a network for regression tasks (where you want to predict a continuous value, like a price).

3.  **ReLU (Rectified Linear Unit):**
    *   **Formula:** `f(x) = max(0, x)`
    *   **Behavior:** If the input is positive, the output is the input itself. If the input is negative, the output is zero.
    *   **Use Case:** The most popular activation function in deep learning. It's computationally very efficient and helps mitigate the "vanishing gradient" problem.

4.  **Sigmoid:**
    *   **Formula:** `f(x) = 1 / (1 + e^-x)`
    *   **Behavior:** An "S"-shaped curve that squashes any input value into a range between 0 and 1.
    *   **Use Case:** Very common in the output layer for binary classification problems, where the output can be interpreted as a probability. It suffers from the vanishing gradient problem in deep networks.

5.  **Tanh (Hyperbolic Tangent):**
    *   **Formula:** `f(x) = (e^x - e^-x) / (e^x + e^-x)`
    *   **Behavior:** Similar to Sigmoid but squashes values into a range between -1 and 1.
    *   **Use Case:** Often preferred over Sigmoid in hidden layers because its output is zero-centered, which can help in learning. It also suffers from the vanishing gradient problem.

---

### **Job 2: Computing a Neuron's Output**

#### The Concept: How a Neuron Calculates its Output

A formal neuron's computation is a two-step process:

**Step 1: Calculate the Potential (also called Net Input or Weighted Sum)**
The neuron takes all its inputs, multiplies each by its corresponding weight, sums them all up, and then adds a bias term.

*   **Formula:** `z = (w₁x₁ + w₂x₂ + ... + wₙxₙ) + b`
*   In vector form, this is much simpler: `z = W · X + b` (where `·` is the dot product).

**Step 2: Apply the Activation Function**
The potential `z` is then passed through an activation function (`f`) to produce the final output `y`.

*   **Formula:** `y = f(z)`

#### Walkthrough of the Lab Example:

*   **Inputs (X):** `[3, -2, 0, -1.5]`
*   **Weights (W):** `[1, 2, 3, 4]`
*   **Bias (b):** `1`
*   **Activation Function (f):** `TanH`

1.  **Calculate Potential (z):**
    `z = (3 * 1) + (-2 * 2) + (0 * 3) + (-1.5 * 4) + 1`
    `z = 3 - 4 + 0 - 6 + 1`
    `z = -6`

2.  **Apply Activation (y):**
    `y = tanh(-6)`
    The `tanh` of a large negative number is very close to -1.
    `y ≈ -0.9999877`



---

### 3. The Complete Python Solution Code

This single script solves both Job 1 and Job 2. You can save it as `lab2_solution.py` and run it from your terminal.

```python
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Job 1: Visualize Activation Functions
# =============================================================================
print("--- Starting Job 1: Visualizing Activation Functions ---")

# Define the input range from -10 to 10 with a step of 0.1
x = np.arange(-10, 10.1, 0.1)

# --- Define the activation functions ---

def binary_step(x):
    """Returns 1 if x > 0, else 0."""
    return np.where(x >= 0, 1, 0)

def linear(x):
    """Returns the input value itself."""
    return x

def relu(x):
    """Returns max(0, x)."""
    return np.maximum(0, x)

def sigmoid(x):
    """Sigmoid function: 1 / (1 + e^-x)"""
    return 1 / (1 + np.exp(-x))

def tanh(x):
    """Hyperbolic tangent function."""
    return np.tanh(x)

# --- Calculate the outputs for each function ---
y_step = binary_step(x)
y_linear = linear(x)
y_relu = relu(x)
y_sigmoid = sigmoid(x)
y_tanh = tanh(x)

# --- Plotting the functions ---
plt.figure(figsize=(12, 8))
plt.title('Common Activation Functions', fontsize=16)

plt.plot(x, y_step, label='Binary Step', linestyle='--')
plt.plot(x, y_linear, label='Linear', linestyle='--')
plt.plot(x, y_relu, label='ReLU', linewidth=2)
plt.plot(x, y_sigmoid, label='Sigmoid', linewidth=2)
plt.plot(x, y_tanh, label='Tanh', linewidth=2)

# Add grid, axis lines, labels, and legend for clarity
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.axhline(y=0, color='k', linewidth=0.8)
plt.axvline(x=0, color='k', linewidth=0.8)
plt.xlabel('Input (z)', fontsize=12)
plt.ylabel('Output (f(z))', fontsize=12)
plt.legend(fontsize=12)
plt.ylim(-1.5, 2.0) # Set y-axis limits for better visualization

# Show the plot
print("Displaying the plot for Job 1. Please close the plot window to continue to Job 2.")
plt.show()


# =============================================================================
# Job 2: Compute the Output of a Formal Neuron
# =============================================================================
print("\n--- Starting Job 2: Computing Neuron Output ---")

# Given values from the example
inputs = np.array([3, -2, 0, -1.5])
weights = np.array([1, 2, 3, 4])
bias = 1

# Step 1: Compute the potential (net input), z = W · X + b
# np.dot() performs the dot product (w1*x1 + w2*x2 + ...)
potential = np.dot(weights, inputs) + bias

# Step 2: Compute the output by applying the TanH activation function
output = np.tanh(potential)

# Display the results in a clear, readable format
print("\n--- Neuron Calculation ---")
print(f"Inputs (X):  {inputs}")
print(f"Weights (W): {weights}")
print(f"Bias (b):    {bias}")
print("-" * 25)
print(f"1. Potential (z = W.X + b): {potential:.4f}")
print(f"2. Output (y = tanh(z)):    {output:.4f}")
print("\nLab successfully completed!")

```