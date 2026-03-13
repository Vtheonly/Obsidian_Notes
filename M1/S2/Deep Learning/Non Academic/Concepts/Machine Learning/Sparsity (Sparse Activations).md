# Sparsity / Sparse Activations

## Definition
A neural network is **sparse** when **most of its neurons are inactive (output zero) at any given time**.

---

## How It Happens
- **ReLU** naturally creates sparsity: negative inputs → output = 0
- These "dead" neurons don't contribute to the next layer

---

## Example
```
Layer with 1000 neurons
Only 300 neurons fire (output > 0) for a given input
→ 70% sparsity
```

---

## Visual: Dense vs Sparse Activations

```mermaid
graph LR
    subgraph Dense["Dense Activations"]
        D1["● 0.8"]
        D2["● 0.3"]
        D3["● 0.9"]
        D4["● 0.5"]
    end
    
    subgraph Sparse["Sparse Activations (ReLU)"]
        S1["● 0.8"]
        S2["○ 0"]
        S3["● 0.9"]
        S4["○ 0"]
    end
    
    Dense --> Sparse
```

---

## Why Sparsity Matters

| Benefit | Explanation |
|---------|-------------|
| **Computational Efficiency** | Fewer active neurons → fewer calculations |
| **Better Generalization** | Network focuses on important features, not all neurons |
| **Memory Efficiency** | Sparse matrices can be stored more compactly |
| **Reduced Overfitting** | Less reliance on every neuron reduces memorization |

---

## How ReLU Creates Sparsity

```mermaid
flowchart TD
    X[Input x] --> R{ReLU: max 0, x}
    R -->|x > 0| P[Output = x<br/>Neuron ACTIVE]
    R -->|x ≤ 0| Z[Output = 0<br/>Neuron INACTIVE]
    
    style P fill:#90EE90
    style Z fill:#FFB6C1
```

---

## Quick Memory Aid
**Sparse** = Many zeros = Efficiency + Better Generalization