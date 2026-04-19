# Backpropagation — Merged Obsidian Vault

A comprehensive, unified knowledge base on Backpropagation, merging content from 9 original source files with all duplicates removed and conflicts resolved.

## Vault Structure

```
01 - Prerequisites/
    1. Derivatives, Power Rule, and the Chain Rule
    2. Gradients and Gradient Descent

02 - Foundations/
    3. Neural Network Architecture and Notation
    4. Forward Propagation and Activation Functions

03 - Error and Optimization/
    5. Loss Functions and Error Calculation
    6. Gradient Descent — The Update Rule and Convergence

04 - Backpropagation/
    7. Backpropagating to the Output Layer
    8. Backpropagating to the Hidden Layer
    9. Matrix Implementation and the Delta Weight Formula
```

## Source Files Merged

| Original File | Key Content | Merged Into |
| --- | --- | --- |
| Backpropagation 1 Coding Training | Intuitive proportional blame, feedforward | 1, 4, 7, 8 |
| Backpropagation 2 Coding Training | JS matrix code, transposition, error backprop | 5, 9 |
| Backpropagation 3 Coding Training | Architecture, gradient descent, delta weight | 3, 4, 6, 9 |
| Backpropagation | Rigorous calculus derivations, delta notation | 4, 7, 8 |
| Chatgpt Gradients | Gradient definition, geometric meaning | 2 |
| Stat quest Backpropagation 1 | Drug dosage, SSR, chain rule for b3 | 2, 3, 5, 6, 7 |
| Stat quest Backpropagation 2 | Multiple parameters, fancy notation, BFEs | 3, 5, 6, 7, 8 |
| Stat quest Backpropagation 3 | Hidden layer BFEs, Softplus derivative | 8 |
| Stat quest Chain-rule | Derivatives, power rule, chain rule, RSS | 1 |

## Reading Order

For maximum comprehension, read the files in numerical order (1 → 9). Each file builds on the concepts introduced in the previous ones:

1. **Start with the math prerequisites** (derivatives, chain rule) — these are the engines under the hood.
2. **Understand the network structure** (architecture, forward pass) — you can't go backward until you know how to go forward.
3. **Learn how error is measured** (loss functions) — without error, there's nothing to propagate.
4. **Master gradient descent** (the update mechanism) — how the network actually learns.
5. **Study backpropagation** (output layer → hidden layer → matrix implementation) — putting it all together.
