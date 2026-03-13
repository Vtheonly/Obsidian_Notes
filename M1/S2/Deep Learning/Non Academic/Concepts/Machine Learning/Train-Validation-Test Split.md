# Train-Validation-Test Split

## Overview

In supervised learning, datasets are commonly split into **three disjoint parts**, each serving a distinct purpose in the model development process.

```mermaid
pie title Data Split (Typical)
    "Training (70%)" : 70
    "Validation (15%)" : 15
    "Test (15%)" : 15
```

---

## The Three Sets

```mermaid
flowchart LR
    subgraph Split["Data Splitting"]
        Data[("Full Dataset")]
        
        Data --> Train["Training Set<br/>70%"]
        Data --> Val["Validation Set<br/>15%"]
        Data --> Test["Test Set<br/>15%"]
    end
    
    style Train fill:#90EE90
    style Val fill:#87CEEB
    style Test fill:#FFB6C1
```

---

## 1. Training Set (70%)

```mermaid
flowchart TB
    subgraph Training["Training Phase"]
        T1["Input X + Labels Y"]
        T2["Model Makes Predictions"]
        T3["Calculate Error"]
        T4["Update Weights/Biases"]
        
        T1 --> T2 --> T3 --> T4
        T4 -.->|"Repeat"| T2
    end
    
    style T4 fill:#90EE90
```

| Aspect | Details |
|--------|---------|
| **Purpose** | Used to "teach" the model |
| **Action** | Algorithm sees X and Y, calculates errors, updates parameters |
| **What It Does** | The model **learns** patterns from this data |

**Key Point:** This is where the model's weights and biases are adjusted through optimization (like gradient descent).

---

## 2. Validation Set (15%)

```mermaid
flowchart TB
    subgraph Validation["Validation Phase"]
        V1["Model Predicts on<br/>Unseen Validation Data"]
        V2["Evaluate Performance"]
        V3{"Good on Train<br/>Bad on Val?"}
        V4["⚠️ OVERFITTING<br/>Adjust Hyperparameters"]
        V5["✓ Continue Training"]
        
        V1 --> V2 --> V3
        V3 -->|Yes| V4
        V3 -->|No| V5
    end
    
    style V4 fill:#FFB6C1
    style V5 fill:#90EE90
```

| Aspect | Details |
|--------|---------|
| **Purpose** | **Model Selection** and **Hyperparameter Tuning** |
| **Action** | Used *during* training to check performance |
| **What It Does** | Detects overfitting, guides hyperparameter choices |

### Why Validation Matters

```mermaid
flowchart LR
    subgraph Overfitting["Detecting Overfitting"]
        O1["Training Accuracy: 95%"]
        O2["Validation Accuracy: 60%"]
        O3["Diagnosis: OVERFITTING!"]
        
        O1 --> O2 --> O3
    end
    
    style O1 fill:#90EE90
    style O2 fill:#FFB6C1
    style O3 fill:#FF6347
```

**If model performs well on Training but poorly on Validation → OVERFITTING**

### What We Use Validation For

| Hyperparameter | Example Values to Try |
|----------------|----------------------|
| K in KNN | 3, 5, 7, 9, 11 |
| Learning Rate | 0.001, 0.01, 0.1 |
| Number of Trees (Random Forest) | 50, 100, 200 |
| Max Depth | 5, 10, 20, None |
| Number of Epochs | Early stopping when val loss increases |

---

## 3. Test Set (15%)

```mermaid
flowchart TB
    subgraph Testing["Test Phase (Final Exam)"]
        TE1["Training Complete"]
        TE2["Model Predicts on<br/>Test Set (NEVER SEEN)"]
        TE3["Final Accuracy Reported"]
        
        TE1 --> TE2 --> TE3
    end
    
    style TE3 fill:#98FB98
```

| Aspect | Details |
|--------|---------|
| **Purpose** | **Final Evaluation** |
| **Action** | Used **only once** at the very end |
| **What It Does** | Acts as the "Final Exam" for real-world accuracy |

### ⚠️ Critical Rule

```mermaid
flowchart TB
    subgraph Rule["The Golden Rule"]
        R1["NEVER use Test Set<br/>during training"]
        R2["NEVER tune hyperparameters<br/>based on Test Set"]
        R3["Test Set = Final Exam<br/>Only used ONCE"]
        
        R1 --> R2 --> R3
    end
    
    style R1 fill:#FF6347
    style R2 fill:#FF6347
    style R3 fill:#90EE90
```

**If you use the Test Set to tune your model, you're cheating!** The test set should represent truly unseen data.

---

# The Validation Step (Deep Dive)

## What Is the Validation Step?

The **validation step** is the phase where:

> The current version of the trained model is evaluated on unseen data (validation set) **without updating parameters**.

```mermaid
flowchart LR
    subgraph ValStep["Validation Step"]
        VS1["Forward Pass Only"]
        VS2["Compute Loss/Accuracy"]
        VS3["NO Backpropagation"]
        VS4["NO Weight Updates"]
        
        VS1 --> VS2
        VS2 --> VS3
        VS3 --> VS4
    end
    
    style VS3 fill:#FFB6C1
    style VS4 fill:#FFB6C1
```

**Formally:**
- No backpropagation
- No weight updates
- No gradient computation
- Only forward pass + metric computation

**Its role is diagnostic and regulatory, not learning.**

It is not part of learning the weights. It is part of **learning how to train the model correctly**.

---

## How It Works During Each Epoch

```mermaid
flowchart TB
    subgraph Epoch["One Training Epoch"]
        subgraph TrainPhase["Step 1 — Training Phase"]
            T1["For each batch:"]
            T2["Forward pass"]
            T3["Compute loss"]
            T4["Backward pass"]
            T5["Update weights"]
        end
        
        subgraph ValPhase["Step 2 — Validation Phase"]
            V1["For each batch:"]
            V2["Forward pass only"]
            V3["Compute loss/accuracy"]
            V4["NO backward pass"]
        end
        
        TrainPhase --> ValPhase
    end
    
    style T5 fill:#90EE90
    style V4 fill:#87CEEB
```

After every epoch, you get:
- Training Loss
- Training Accuracy
- Validation Loss
- Validation Accuracy

These values are tracked over time.

---

## Why the Validation Step Exists

### 1. Detecting Overfitting

```mermaid
flowchart TB
    subgraph OverfitPattern["Overfitting Pattern"]
        E10["Epoch 10<br/>Train: 0.20 | Val: 0.25"]
        E20["Epoch 20<br/>Train: 0.05 | Val: 0.40"]
        E30["Epoch 30<br/>Train: 0.01 | Val: 0.70"]
        
        E10 --> E20 --> E30
    end
    
    style E10 fill:#90EE90
    style E20 fill:#FFA07A
    style E30 fill:#FF6347
```

| Epoch | Train Loss | Val Loss | Interpretation |
|-------|------------|----------|----------------|
| 10 | 0.20 | 0.25 | ✓ Good |
| 20 | 0.05 | 0.40 | ⚠️ Starting to overfit |
| 30 | 0.01 | 0.70 | ✗ Severe overfitting |

**Interpretation:**
- Model keeps improving on training
- Gets worse on validation
- Means: **memorizing, not generalizing**

**Without validation, you would never see this.**

---

### 2. Hyperparameter Selection

```mermaid
flowchart TB
    subgraph HyperTune["Hyperparameter Tuning Process"]
        H1["Train with Config A"]
        H2["Validate"]
        H3["Train with Config B"]
        H4["Validate"]
        H5["Choose Best Config"]
        
        H1 --> H2 --> H3 --> H4 --> H5
    end
    
    style H5 fill:#90EE90
```

**Hyperparameters cannot be learned by gradient descent.**

| Hyperparameter | What It Controls |
|----------------|------------------|
| Learning Rate | Step size in optimization |
| Batch Size | Samples per gradient update |
| Number of Layers | Network depth |
| K in KNN | Number of neighbors |
| Regularization Strength | Penalty on complexity |
| Dropout Rate | Fraction of neurons to drop |

**Process:**
1. Train model with config A → Validate
2. Train model with config B → Validate
3. Choose best config based on validation performance

**Validation set decides.**

---

### 3. Early Stopping

```mermaid
flowchart TB
    subgraph EarlyStop["Early Stopping Logic"]
        ES1["Monitor Validation Loss"]
        ES2{"Improved in<br/>last 10 epochs?"}
        ES3["Continue Training"]
        ES4["STOP Training<br/>Restore Best Weights"]
        
        ES1 --> ES2
        ES2 -->|Yes| ES3
        ES2 -->|No| ES4
    end
    
    style ES4 fill:#90EE90
```

**Rule Example:**
> If validation loss does not improve for 10 epochs → stop training.

This prevents over-training and automatically selects the best epoch.

---

## Validation vs Training vs Test (Key Differences)

```mermaid
flowchart TB
    subgraph Compare["Key Differences"]
        C1["Training: Updates Weights ✓"]
        C2["Validation: Updates Weights ✗"]
        C3["Test: Updates Weights ✗"]
        
        C4["Training: Used During Training ✓"]
        C5["Validation: Used During Training ✓"]
        C6["Test: Used During Training ✗"]
        
        C7["Training: Hyperparameter Tuning ✗"]
        C8["Validation: Hyperparameter Tuning ✓"]
        C9["Test: Hyperparameter Tuning ✗"]
    end
    
    style C1 fill:#90EE90
    style C5 fill:#87CEEB
    style C9 fill:#FFB6C1
```

| Property | Training | Validation | Test |
|----------|----------|------------|------|
| **Updates Weights** | ✓ Yes | ✗ No | ✗ No |
| **Used During Training** | ✓ Yes | ✓ Yes | ✗ No |
| **Hyperparameter Tuning** | ✗ No | ✓ Yes | ✗ No |
| **Performance Reporting** | ✗ No | ✗ No | ✓ Yes |
| **Seen by Model** | ✓ Yes | Indirectly | ✗ Never |

**Important:** The model **never learns directly from validation**, but training decisions depend on it.

---

## Mathematical View

Let:
- θ = model parameters (weights)
- λ = hyperparameters

```mermaid
flowchart LR
    subgraph Math["Mathematical View"]
        M1["Training:<br/>θ* = argmin L_train(θ, λ)"]
        M2["Validation:<br/>λ* = argmin L_val(θ*(λ))"]
        M3["Test:<br/>Final = L_test(θ*, λ*)"]
        
        M1 --> M2 --> M3
    end
    
    style M1 fill:#90EE90
    style M2 fill:#87CEEB
    style M3 fill:#FFB6C1
```

**Meaning:**
- **Training** optimizes θ (weights)
- **Validation** optimizes λ (hyperparameters)
- **Test** evaluates final model

---

## Cross-Validation vs Validation Set

```mermaid
flowchart TB
    subgraph Choice["When to Use What"]
        Large["Large Dataset<br/>→ Fixed Validation Set"]
        Small["Small Dataset<br/>→ K-Fold Cross-Validation"]
    end
    
    style Large fill:#90EE90
    style Small fill:#87CEEB
```

**When you don't have enough data:**

Instead of a fixed validation set, use **K-Fold Cross-Validation**:
- Split data into K folds
- Rotate which fold is validation
- Average results across all folds

This replaces a static validation set when data is limited.

---

## Common Mistakes

### Mistake 1: Tuning on Test Set

```mermaid
flowchart LR
    subgraph Bad1["❌ WRONG"]
        B1["Tune on Test Set"]
        B2["Information Leakage"]
        B3["Biased Results"]
    end
    
    B1 --> B2 --> B3
    
    style B1 fill:#FF6347
```

**If you tune using test data → You leak information → Result is biased → Not publishable.**

---

### Mistake 2: Training on Validation Later

```mermaid
flowchart LR
    subgraph Caution["⚠️ Caution"]
        C1["Merging Train + Val<br/>after tuning"]
        C2["Allowed ONLY after<br/>ALL decisions finished"]
    end
    
    C1 --> C2
    
    style C2 fill:#FFA07A
```

Sometimes people merge train+val after tuning. This is allowed **only after all decisions are finished**.

---

### Mistake 3: Ignoring Validation Curves

```mermaid
flowchart TB
    subgraph Always["✓ Always Plot"]
        A1["Train vs Val Loss"]
        A2["Train vs Val Accuracy"]
    end
    
    style A1 fill:#90EE90
    style A2 fill:#90EE90
```

Only looking at final accuracy hides overfitting. **Always plot curves over time.**

---

## Mental Model

```mermaid
mindmap
    root((ML Process))
        Training
            Learning
            Updates weights
            Like studying
        Validation
            Supervision
            Checks if learning correctly
            Like practice exams
        Test
            Certification
            Final proof
            Like final exam
```

| Phase | Analogy | Purpose |
|-------|---------|---------|
| **Training** | Learning / Studying | Makes you better |
| **Validation** | Supervision / Practice Exams | Checks if you're learning correctly |
| **Test** | Certification / Final Exam | Proves your ability |

---

## Why Validation Matters (Opinion)

> Validation is one of the most underestimated parts of ML.

Many "good" models are actually:
- Overfit models with bad validation discipline
- Poorly tuned models with no early stopping
- Models optimized on leaked test data

**A clean validation pipeline matters more than fancy architectures.**

**If validation is wrong, your results are meaningless.**

---

## Comparison Table

| Set | Purpose | When Used | Can Model "See" It? |
|-----|---------|-----------|---------------------|
| **Training** | Learn patterns | Throughout training | ✓ Yes (weights updated) |
| **Validation** | Tune & detect overfitting | During training | ✗ No (only evaluation) |
| **Test** | Final evaluation | Once at the end | ✗ No (final exam) |

---

## Visual: The Complete Workflow

```mermaid
flowchart TB
    subgraph Workflow["ML Development Workflow"]
        Start[("Full Dataset")]
        
        Start --> Split["Split Data<br/>70/15/15"]
        
        Split --> Train["Training Set"]
        Split --> Val["Validation Set"]
        Split --> Test["Test Set"]
        
        Train --> Learn["Train Model<br/>(Update Weights)"]
        Val --> Check["Validate<br/>(Check Overfitting)"]
        
        Check --> Tune["Tune Hyperparameters"]
        Tune --> Learn
        
        Learn --> Done["Training Complete"]
        Done --> Final["Evaluate on Test Set<br/>(Final Score)"]
    end
    
    style Final fill:#90EE90
```

---

## Analogy: Student Learning

| Set | Student Analogy |
|-----|-----------------|
| **Training** | Textbook, notes, practice problems (student learns from these) |
| **Validation** | Practice exams (check understanding, adjust study methods) |
| **Test** | Final exam (never seen before, real measure of knowledge) |

---

## Common Split Ratios

| Ratio | When to Use |
|-------|-------------|
| **70/15/15** | Standard, balanced approach |
| **80/10/10** | Large datasets, less need for validation |
| **60/20/20** | Small datasets, need more validation reliability |
| **98/1/1** | Very large data (millions of samples) |

---

## Quick Memory Aid

| Set | Purpose | Remember As |
|-----|---------|-------------|
| **Training** | Learn | "Textbook" - model learns here |
| **Validation** | Tune | "Practice Exam" - adjust hyperparameters |
| **Test** | Evaluate | "Final Exam" - used ONCE for final score |

**Training = Learn | Validation = Tune | Test = Final Score**