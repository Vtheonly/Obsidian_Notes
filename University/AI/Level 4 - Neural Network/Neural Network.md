
# Neural Network Walkthrough: Perceptron Learning & Forward Propagation

---

## 1. Clarification & Corrections

- **Context**: These notes synthesize a handwritten walkthrough of (1) the Perceptron learning algorithm for the AND function, and (2) forward propagation in a small multilayer feed‑forward network using logistic activations.
- **Notation alignment**: Where the original diagrams referenced slide weights inconsistently, all numerical calculations below follow the slide‑specified values:
  - Perceptron weights initialized at zero.
  - Multilayer network weights from “slide 35” (input‑to‑hidden: 0.15, 0.20, 0.25, 0.30; hidden‑to‑output: 0.40, 0.45, 0.50, 0.55; biases 0.35 & 0.60).

---

## 2. Perceptron Learning Algorithm

### 2.1. Model & Activation

- **Artificial neuron**:  
  - Inputs: $$x_0=1$$ (bias), $$x_1, \dots, x_n$$  
  - Weights: $$w_0$$ (bias weight), $$w_1, \dots, w_n$$  
  - Net input:  
    $$
      \mathrm{net} \;=\; \sum_{i=0}^n w_i\,x_i
    $$
  - Activation (Heaviside step):  
    $$
      y = H(\mathrm{net}) = 
      \begin{cases}
        1 & \text{if }\mathrm{net} > 0,\\
        0 & \text{otherwise.}
      \end{cases}
    $$

### 2.2. AND‑Function Training Setup

| Input $$x_1, x_2$$ | Target $$d$$ |
|:------------------:|:------------:|
| (0, 0)             | 0            |
| (0, 1)             | 0            |
| (1, 0)             | 0            |
| (1, 1)             | 1            |

- **Architecture**: single neuron, no hidden layers.  
- **Learning rate**: $$r = 0.5$$.  
- **Initial weights**: $$w_0 = 0,\; w_1 = 0,\; w_2 = 0$$.

### 2.3. Epoch 1 Calculations

1. **Input (0, 0)**  
   - $$\mathrm{net} = 0\cdot1 + 0\cdot0 + 0\cdot0 = 0$$  
   - $$y = H(0) = 0$$, error $$e = 0 - 0 = 0$$; no update.

2. **Input (0, 1)**  
   - $$\mathrm{net} = 0$$, $$y = 0$$, error $$e = 0$$; no update.

3. **Input (1, 0)**  
   - $$\mathrm{net} = 0$$, $$y = 0$$, error $$e = 0$$; no update.

4. **Input (1, 1)**  
   - $$\mathrm{net} = 0$$, $$y = 0$$, error $$e = 1 - 0 = 1$$.  
   - **Weight updates** (Perceptron rule):  
     $$
       w_i \leftarrow w_i + r \cdot e \cdot x_i
     $$
     - $$w_0 \leftarrow 0 + 0.5\cdot1\cdot1 = 0.5$$  
     - $$w_1 \leftarrow 0 + 0.5\cdot1\cdot1 = 0.5$$  
     - $$w_2 \leftarrow 0 + 0.5\cdot1\cdot1 = 0.5$$  

- **Mean epoch error**:  
  $$
    \frac{|0|+|0|+|0|+|1|}{4} = 0.25
  $$

### 2.4. Stopping Criteria

- **Zero mean error** across an epoch, or  
- **Maximum epochs** reached (e.g. $$\text{iter}_{\max}=3$$).

### 2.5. Common Activation Functions

| Name      | Definition                                    |
|-----------|-----------------------------------------------|
| Heaviside | $$H(x) = 1 \;\text{if }x>0,\;0\text{ otherwise}$$ |
| Sign      | $$\operatorname{sgn}(x) = \pm1$$              |
| ReLU      | $$\max(0,x)$$                                 |
| Sigmoid   | $$\displaystyle\frac{1}{1+e^{-x}}$$            |
| Tanh      | $$\displaystyle\frac{e^x - e^{-x}}{e^x + e^{-x}}$$ |

---

## 3. Multilayer Network: Forward Propagation

### 3.1. Network Architecture

- **Inputs**: $$i_1=0.05,\;i_2=0.10$$.  
- **Hidden layer**: 2 neurons ($$h_1,h_2$$), bias $$b_1=0.35$$.  
- **Output layer**: 2 neurons ($$o_1,o_2$$), bias $$b_2=0.60$$.  
- **Weights** (from slide 35):

| From → To | Weight |
|-----------|--------|
| $$i_1\to h_1$$ | 0.15 |
| $$i_2\to h_1$$ | 0.20 |
| $$i_1\to h_2$$ | 0.25 |
| $$i_2\to h_2$$ | 0.30 |
| $$h_1\to o_1$$ | 0.40 |
| $$h_2\to o_1$$ | 0.45 |
| $$h_1\to o_2$$ | 0.50 |
| $$h_2\to o_2$$ | 0.55 |

- **Activation**: logistic sigmoid $$g(x)=1/(1+e^{-x})$$.

### 3.2. Hidden Layer Computations

1. **Neuron $$h_1$$**  
   $$
     \mathrm{net}_{h_1}
     = b_1 + w_{i_1h_1}\,i_1 + w_{i_2h_1}\,i_2
     = 0.35 + 0.15\cdot0.05 + 0.20\cdot0.10
     = 0.3775
   $$
   $$
     o_{h_1} = g(0.3775)\approx0.59327
   $$

2. **Neuron $$h_2$$**  
   $$
     \mathrm{net}_{h_2} = 0.35 + 0.25\cdot0.05 + 0.30\cdot0.10
     = 0.3925
   $$
   $$
     o_{h_2} = g(0.3925)\approx0.59688
   $$

### 3.3. Output Layer Computations

1. **Neuron $$o_1$$**  
   $$
     \mathrm{net}_{o_1} 
     = b_2 + w_{h_1o_1}\,o_{h_1} + w_{h_2o_1}\,o_{h_2}
     = 0.60 + 0.40\cdot0.59327 + 0.45\cdot0.59688
     = 1.1059
   $$
   $$
     o_{o_1} = g(1.1059)\approx0.75137
   $$

2. **Neuron $$o_2$$**  
   $$
     \mathrm{net}_{o_2}
     = 0.60 + 0.50\cdot0.59327 + 0.55\cdot0.59688
     = 1.2249
   $$
   $$
     o_{o_2} = g(1.2249)\approx0.77293
   $$

---

## 4. Additional Worked Examples

### Example 1: 2 → 2 → 1 Network

- **Inputs**: $$i_1=0.80,\;i_2=0.20$$  
- **Hidden weights**:  
  $$\{w_{i_1h_1}=0.10,\;w_{i_2h_1}=0.40,\;w_{i_1h_2}=0.30,\;w_{i_2h_2}=-0.20\}$$, biases $$b_{h1}=0.10,\;b_{h2}=0.20$$  
- **Output weights**: $$w_{h_1o}=0.50,\;w_{h_2o}=0.60$$, bias $$b_o=-0.10$$  

| Neuron | Net input                              | Output (sigmoid) |
|:------:|:---------------------------------------|:-----------------|
| $$h_1$$ | $$0.10·0.8 + 0.40·0.2 + 0.10 = 0.26$$  | ≈ 0.5646         |
| $$h_2$$ | $$0.30·0.8 –0.20·0.2 + 0.20 = 0.40$$   | ≈ 0.5987         |
| $$o$$   | $$0.50·0.5646 + 0.60·0.5987 – 0.10=0.5415$$ | ≈ 0.6321         |

**Final output**: $$\approx0.6321$$

---

### Example 2: 2 → 3 → 2 Network

- **Inputs**: $$i_1=i_2=0.50$$  
- **Hidden weights & biases**:

| Neuron | $$w_{i_1}$$ | $$w_{i_2}$$ | $$b_h$$ |
|:------:|:-----------:|:-----------:|:-------:|
| $$h_1$$| 0.20        | –0.10       | 0.10    |
| $$h_2$$| 0.10        | 0.30        | –0.10   |
| $$h_3$$| –0.20       | 0.10        | 0.00    |

- **Output weights & biases**:

| To → Neuron | $$w_{h_1}$$ | $$w_{h_2}$$ | $$w_{h_3}$$ | $$b_o$$ |
|:-----------:|:-----------:|:-----------:|:-----------:|:-------:|
| $$o_1$$     | 0.40        | 0.20        | –0.10       | 0.20    |
| $$o_2$$     | 0.10        | –0.30       | 0.50        | –0.20   |

| Neuron | Net input                                       | Output (sigmoid) |
|:------:|:------------------------------------------------|:-----------------|
| $$h_1$$ | $$0.2·0.5 –0.1·0.5 +0.1 = 0.15$$                | ≈ 0.5374         |
| $$h_2$$ | $$0.1·0.5 +0.3·0.5 –0.1 = 0.10$$                | ≈ 0.5250         |
| $$h_3$$ | $$-0.2·0.5 +0.1·0.5 +0.0 = -0.05$$              | ≈ 0.4875         |
| $$o_1$$ | $$0.4·0.5374 +0.2·0.5250 –0.1·0.4875 +0.2=0.4712$$| ≈ 0.6156         |
| $$o_2$$ | $$0.1·0.5374 –0.3·0.5250 +0.5·0.4875 –0.2=-0.06$$| ≈ 0.4850         |

**Final outputs**:  
$$
  o_1 \approx 0.6156,
  \quad
  o_2 \approx 0.4850
$$
```