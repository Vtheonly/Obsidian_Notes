# Cross-Validation (K-Fold)

## Definition
**Cross-validation** is a technique to evaluate model performance by splitting data into multiple training/validation sets.

---

## K-Fold Cross-Validation Visual

```mermaid
block-beta
    columns 5
    
    block:fold1
        A1["TEST"]
        A2["TRAIN"]
        A3["TRAIN"]
        A4["TRAIN"]
        A5["TRAIN"]
    end
    
    block:fold2
        B1["TRAIN"]
        B2["TEST"]
        B3["TRAIN"]
        B4["TRAIN"]
        B5["TRAIN"]
    end
    
    block:fold3
        C1["TRAIN"]
        C2["TRAIN"]
        C3["TEST"]
        C4["TRAIN"]
        C5["TRAIN"]
    end
    
    block:fold4
        D1["TRAIN"]
        D2["TRAIN"]
        D3["TRAIN"]
        D4["TEST"]
        D5["TRAIN"]
    end
    
    block:fold5
        E1["TRAIN"]
        E2["TRAIN"]
        E3["TRAIN"]
        E4["TRAIN"]
        E5["TEST"]
    end
```

**Final Score = Average of all 5 fold scores**

---

## How It Works

```mermaid
flowchart LR
    A[Full Dataset] --> B[Split into K parts]
    B --> C[Train on K-1 folds]
    C --> D[Validate on 1 fold]
    D --> E[Repeat K times]
    E --> F[Average all scores]
    
    style F fill:#90EE90
```

1. **Split data into K equal parts** (folds)
2. **Train on K-1 folds**, validate on 1 fold
3. **Repeat K times**, each fold used as validation once
4. **Average all K scores** for final evaluation

---

## Why Use Cross-Validation?

| Benefit | Explanation |
|---------|-------------|
| **More Reliable Evaluation** | Uses all data for validation eventually |
| **Detects Overfitting** | High variance across folds indicates overfitting |
| **Better for Small Data** | Maximizes use of limited data |
| **Hyperparameter Tuning** | More robust than single train/test split |

---

## Common Values of K

```mermaid
graph LR
    K5["K=5<br/>★ Recommended"] --- K10["K=10<br/>More thorough"]
    K10 --- KN["K=N<br/>Leave-One-Out"]
    
    style K5 fill:#90EE90
    style K10 fill:#98FB98
    style KN fill:#FFA07A
```

| K Value | Use Case |
|---------|----------|
| **K=5** | Standard choice, good balance |
| **K=10** | More thorough, more computation |
| **K=N** (Leave-One-Out) | Maximum accuracy, very expensive |

---

## Stratified K-Fold

For **imbalanced datasets**, use Stratified K-Fold to maintain class distribution:

```mermaid
flowchart TB
    subgraph Regular["Regular K-Fold (Imbalanced Data)"]
        R1["Fold 1: 80% Class A, 20% Class B"]
        R2["Fold 2: 60% Class A, 40% Class B"]
        R3["Fold 3: 90% Class A, 10% Class B"]
    end
    
    subgraph Stratified["Stratified K-Fold (Balanced)"]
        S1["Fold 1: 70% Class A, 30% Class B"]
        S2["Fold 2: 70% Class A, 30% Class B"]
        S3["Fold 3: 70% Class A, 30% Class B"]
    end
    
    Regular --> Stratified
    
    style R2 fill:#FFA07A
    style R3 fill:#FFB6C1
    style S1 fill:#90EE90
    style S2 fill:#90EE90
    style S3 fill:#90EE90
```

---

## Python Example

```python
from sklearn.model_selection import cross_val_score, KFold
from sklearn.ensemble import RandomForestClassifier

# Set up K-Fold
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Perform cross-validation
model = RandomForestClassifier()
scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')

print(f"Fold scores: {scores}")
print(f"Mean accuracy: {scores.mean():.3f}")
print(f"Standard deviation: {scores.std():.3f}")
```

### Stratified Version

```python
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf)
```

---

## Cross-Validation vs Single Split

```mermaid
flowchart TB
    subgraph Single["Single Train/Test Split"]
        ST[One evaluation] --> SR["Result may be lucky/unlucky"]
    end
    
    subgraph CV["K-Fold Cross-Validation"]
        CT[K evaluations] --> CR["Reliable average score"]
    end
    
    style SR fill:#FFA07A
    style CR fill:#90EE90
```

---

## Quick Memory Aid
**Cross-Validation** = Rotate test data → Reliable scores → Use K=5 or K=10