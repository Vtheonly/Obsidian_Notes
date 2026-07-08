# Constrained Optimization

> **Chapter 11 — Parameter Tuning & Optimization** | ← [[L1 Regularization and Sparsity]] | → [[Feature Orthogonality Design]]

---

## Why Unconstrained Optimization Fails

If we run [[Texel Tuning Method|Texel tuning]] without constraints—just pure gradient descent on the MSE loss—the optimizer will find the mathematically optimal weights. But these weights will often be **absurd** from a chess perspective.

### Examples of Absurd Results

| Rule | Correct Weight | Unconstrained Weight | Problem |
|---|---|---|---|
| Pawn Material | 100 | 73 | Pawn should be the unit of measurement |
| Knight Material | 300-350 | -15 | A free knight can't be bad! |
| Knight_On_Rim | -30 to -50 | +25 | "Knight on the rim" should be penalized |
| King_Safety | 40-100 | -200 | You can't want an unsafe king |
| Bishop_Pair | 30-60 | -180 | Two bishops are an advantage |
| Doubled_Pawns | -15 to -30 | +45 | Doubled pawns are a weakness |

These results occur because:

1. **Confounding**: In the training data, positions where "Knight on Rim" fires might also have strong tactical features that correlate with winning. The optimizer attributes the win to "Knight on Rim" instead.
2. **Scale ambiguity**: Without a pawn anchor, all weights can scale arbitrarily.
3. **Feature correlation**: As discussed in [[Credit Assignment Problem]], correlated features can cause the optimizer to assign negative weights to naturally positive features.
4. **Insufficient data**: Rare features (like "Knight on Rim") have few training examples, so the optimizer can assign arbitrary values.

---

## The Pawn Value Anchor

### The Constraint

The most fundamental constraint: **W_pawn = 100 centipawns**, always. This is the unit of measurement for chess evaluation. Everything else is defined relative to the pawn.

### Why It's Necessary

Without anchoring the pawn value:

- The optimizer could set Pawn = 73, Knight = 273, Bishop = 284 — all ratios are preserved, but the centipawn scale is wrong
- Or worse: Pawn = 0.001, making all other weights enormous and numerically unstable
- The evaluation loses its intuitive meaning: "+1.50" no longer means "1.5 pawns ahead"

### Implementation

```python
# In the PyTorch training loop
def freeze_pawn_weight(model, pawn_idx):
    """Ensure the pawn weight stays at 100 after each gradient step."""
    with torch.no_grad():
        model.weights[pawn_idx] = 100.0

# After optimizer.step():
with torch.no_grad():
    model.weights[pawn_idx] = 100.0
    # Also zero the gradient for the pawn weight
    if model.weights.grad is not None:
        model.weights.grad[pawn_idx] = 0.0
```

---

## Sign Constraints

### The Principle

Many chess features have a **known sign**—we know whether they should be positive or negative, even if we don't know the exact magnitude:

| Rule | Known Sign | Reasoning |
|---|---|---|
| Material (all pieces) | Positive (+) | More material = better |
| Knight_On_Rim | Negative (-) | "Knight on the rim is dim" |
| Doubled_Pawns | Negative (-) | Structural weakness |
| Isolated_Pawn | Negative (-) | No adjacent pawns for support |
| Backward_Pawn | Negative (-) | Can't be defended by own pawns |
| Bishop_Pair | Positive (+) | Two bishops complement each other |
| Passed_Pawn | Positive (+) | Advancing toward promotion |
| Rook_On_Open_File | Positive (+) | Activity advantage |
| Bad_Bishop | Negative (-) | Bishop blocked by own pawns |
| King_Protection | Positive (+) | Safety is good |

### Implementation via Clamping

After each gradient step, we **clamp** weights to their known-sign range:

```python
class SignConstraints:
    """Defines and applies sign constraints to evaluation weights."""

    # Maps weight index to (min_value, max_value)
    # None means unconstrained in that direction
    CONSTRAINTS = {
        # Material weights (must be positive, with sensible bounds)
        'W_PAWN':   (100.0, 100.0),   # Frozen at 100
        'W_KNIGHT': (200.0, 500.0),   # Must be 200-500 cp
        'W_BISHOP': (200.0, 500.0),   # Must be 200-500 cp
        'W_ROOK':   (400.0, 800.0),   # Must be 400-800 cp
        'W_QUEEN':  (700.0, 1200.0),  # Must be 700-1200 cp

        # Pawn structure (must be negative — weaknesses)
        'W_DOUBLED_PAWNS':   (-80.0, 0.0),
        'W_ISOLATED_PAWN':   (-60.0, 0.0),
        'W_BACKWARD_PAWN':   (-50.0, 0.0),

        # Piece placement
        'W_KNIGHT_ON_RIM':   (-80.0, 0.0),   # Must be negative
        'W_KNIGHT_OUTPOST':  (0.0, 120.0),    # Must be positive
        'W_BISHOP_PAIR':     (0.0, 100.0),     # Must be positive
        'W_BAD_BISHOP':      (-60.0, 0.0),     # Must be negative

        # King safety
        'W_KING_SAFETY':     (0.0, 200.0),     # Must be positive
        'W_KING_PROTECTION': (0.0, 150.0),     # Must be positive
        'W_OPEN_FILE_NEAR_KING': (-100.0, 0.0), # Must be negative

        # Activity
        'W_ROOK_OPEN_FILE':  (0.0, 100.0),     # Must be positive
        'W_PASSED_PAWN':     (0.0, 200.0),      # Must be positive
        'W_MOBILITY_PER_SQ': (0.0, 10.0),      # Must be positive
    }

    @classmethod
    def apply(cls, model, rule_names: list):
        """Clamp all weights to their constrained ranges."""
        with torch.no_grad():
            for j, name in enumerate(rule_names):
                if name in cls.CONSTRAINTS:
                    min_val, max_val = cls.CONSTRAINTS[name]
                    model.weights[j] = torch.clamp(
                        model.weights[j],
                        min=min_val,
                        max=max_val
                    )
```

### Integration into Training

```python
class ConstrainedTexelTuner(TexelTuner):
    """Texel tuner with domain constraints applied after each step."""

    def __init__(self, n_features, pawn_idx=0, k=1.13,
                 l1_lambda=0.01, rule_names=None):
        super().__init__(n_features, pawn_idx, k, l1_lambda)
        self.rule_names = rule_names or []

    def train_step(self, features, results, optimizer):
        """Training step with constraint enforcement."""
        # Standard gradient step
        optimizer.zero_grad()
        predictions = self.forward(features)
        loss = self._compute_loss(predictions, results)
        loss.backward()

        # Zero gradient for frozen pawn weight
        self.weights.grad[self.pawn_idx] = 0.0

        optimizer.step()

        # Apply domain constraints
        SignConstraints.apply(self, self.rule_names)

        # Apply L1 proximal step
        if self.l1_lambda > 0:
            self.weights = nn.Parameter(
                soft_threshold(self.weights, self.l1_lambda, self.pawn_idx)
            )

        # Re-apply constraints after soft thresholding
        # (thresholding might violate a constraint)
        SignConstraints.apply(self, self.rule_names)

        return loss.item()
```

---

## Order Constraints

### The Principle

Beyond sign constraints, we know certain **ordering relationships** between weights:

| Constraint | Reasoning |
|---|---|
| W_Queen > W_Rook | Queen is strictly more valuable |
| W_Rook > W_Bishop ≈ W_Knight | Rook is more valuable than minor pieces |
| W_Bishop ≥ W_Knight | Bishop pair advantage; bishops slightly preferred |
| W_Passed_Pawn_7th > W_Passed_Pawn_6th | Closer to promotion = more valuable |
| W_Knight_Outpost_Center > W_Knight_Outpost_Flank | Central outposts are stronger |

### Implementation

```python
class OrderConstraints:
    """Enforces ordering constraints between weight pairs."""

    # Each tuple: (higher_weight_name, lower_weight_name)
    ORDERINGS = [
        ('W_QUEEN', 'W_ROOK'),
        ('W_ROOK', 'W_BISHOP'),
        ('W_ROOK', 'W_KNIGHT'),
        ('W_BISHOP', 'W_PAWN'),
        ('W_KNIGHT', 'W_PAWN'),
        ('W_PASSED_PAWN_7TH', 'W_PASSED_PAWN_6TH'),
        ('W_PASSED_PAWN_6TH', 'W_PASSED_PAWN_5TH'),
        ('W_KNIGHT_OUTPOST_CENTER', 'W_KNIGHT_OUTPOST_FLANK'),
    ]

    @classmethod
    def apply(cls, model, rule_names: list):
        """Enforce ordering constraints by swapping if violated."""
        with torch.no_grad():
            name_to_idx = {name: i for i, name in enumerate(rule_names)}

            for higher_name, lower_name in cls.ORDERINGS:
                if higher_name not in name_to_idx:
                    continue
                if lower_name not in name_to_idx:
                    continue

                h_idx = name_to_idx[higher_name]
                l_idx = name_to_idx[lower_name]

                h_val = model.weights[h_idx].item()
                l_val = model.weights[l_idx].item()

                # If ordering is violated, swap and average
                if h_val < l_val:
                    avg = (h_val + l_val) / 2.0
                    model.weights[h_idx] = avg + 1.0  # Ensure h > l
                    model.weights[l_idx] = avg - 1.0
```

---

## Phase-Dependent Constraints

### The Principle

Many weights have separate values for middlegame (MG) and endgame (EG). These need phase-specific constraints:

| Rule | MG Constraint | EG Constraint | Reasoning |
|---|---|---|---|
| King_Safety | Positive, large | Near zero | King safety matters in MG, not EG |
| Passed_Pawn | Moderate | Large | Passed pawns are crucial in EG |
| King_Activity | Negative | Positive | Bad to activate king in MG, good in EG |
| Center_Control | Large | Moderate | Center matters most in MG |

```python
class PhaseConstraints:
    """Constraints that differ by game phase."""

    PHASE_CONSTRAINTS = {
        'W_KING_SAFETY_MG':  (20.0, 200.0),    # Important in middlegame
        'W_KING_SAFETY_EG':  (-20.0, 20.0),     # Less important in endgame
        'W_KING_ACTIVITY_MG': (-50.0, 0.0),     # Bad to activate king in MG
        'W_KING_ACTIVITY_EG': (0.0, 100.0),      # Good to activate king in EG
        'W_PASSED_PAWN_MG':  (0.0, 80.0),        # Moderate in MG
        'W_PASSED_PAWN_EG':  (0.0, 200.0),       # Crucial in EG
        'W_CENTER_MG':       (10.0, 80.0),       # Important in MG
        'W_CENTER_EG':       (-10.0, 40.0),      # Less important in EG
    }

    @classmethod
    def apply(cls, model, rule_names: list):
        """Apply phase-specific constraints."""
        with torch.no_grad():
            for j, name in enumerate(rule_names):
                if name in cls.PHASE_CONSTRAINTS:
                    min_val, max_val = cls.PHASE_CONSTRAINTS[name]
                    model.weights[j] = torch.clamp(
                        model.weights[j], min=min_val, max=max_val
                    )
```

---

## Full Constrained Training Loop

```python
class FullyConstrainedTexelTuner:
    """Complete Texel tuner with all constraint types."""

    def __init__(self, n_features: int, rule_names: list,
                 pawn_idx: int = 0, k: float = 1.13,
                 l1_lambda: float = 0.01,
                 learning_rate: float = 0.5):
        self.model = TexelTuner(n_features, pawn_idx, k)
        self.rule_names = rule_names
        self.pawn_idx = pawn_idx
        self.l1_lambda = l1_lambda
        self.optimizer = optim.SGD(
            self.model.parameters(), lr=learning_rate
        )

    def train(self, dataset, n_epochs=100, batch_size=16384):
        """Full training loop with all constraints."""
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        for epoch in range(n_epochs):
            for features, results in loader:
                # 1. Forward pass
                self.optimizer.zero_grad()
                predictions = self.model(features)
                loss = nn.MSELoss()(predictions, results)

                # Add L1 penalty
                if self.l1_lambda > 0:
                    weights_ex_pawn = torch.cat([
                        self.model.weights[:self.pawn_idx],
                        self.model.weights[self.pawn_idx + 1:]
                    ])
                    loss += self.l1_lambda * torch.sum(
                        torch.abs(weights_ex_pawn)
                    )

                # 2. Backward pass
                loss.backward()
                self.model.weights.grad[self.pawn_idx] = 0.0

                # 3. Gradient step
                self.optimizer.step()

                # 4. Apply ALL constraints in order:
                # a) Pawn anchor
                with torch.no_grad():
                    self.model.weights[self.pawn_idx] = 100.0

                # b) Sign constraints
                SignConstraints.apply(self.model, self.rule_names)

                # c) Order constraints
                OrderConstraints.apply(self.model, self.rule_names)

                # d) Phase constraints
                PhaseConstraints.apply(self.model, self.rule_names)

                # e) L1 soft thresholding
                if self.l1_lambda > 0:
                    self.weights = nn.Parameter(
                        soft_threshold(
                            self.model.weights,
                            self.l1_lambda,
                            self.pawn_idx
                        )
                    )

                # f) Re-apply all constraints after thresholding
                with torch.no_grad():
                    self.model.weights[self.pawn_idx] = 100.0
                SignConstraints.apply(self.model, self.rule_names)
                OrderConstraints.apply(self.model, self.rule_names)
                PhaseConstraints.apply(self.model, self.rule_names)

            if epoch % 10 == 0:
                n_zero = sum(
                    1 for j, w in enumerate(self.model.weights)
                    if j != self.pawn_idx and abs(w.item()) < 2.0
                )
                sparsity = n_zero / (len(self.model.weights) - 1)
                print(f"Epoch {epoch}: loss={loss.item():.6f}, "
                      f"sparsity={sparsity:.1%}")

        return self.model.get_weights()
```

---

## The Constraint Hierarchy

Constraints have a priority order. When they conflict, higher-priority constraints win:

```
Priority 1: Pawn Anchor (W_pawn = 100, absolutely fixed)
Priority 2: Sign Constraints (positive/negative direction)
Priority 3: Order Constraints (relative ordering)
Priority 4: Phase Constraints (phase-specific bounds)
Priority 5: L1 Sparsity (soft thresholding)
```

After each gradient step, constraints are applied in this order. If L1 thresholding violates a sign constraint, the sign constraint wins (the weight is restored to its sign-appropriate minimum value rather than being zeroed).

---

## Connections

- **Previous**: [[L1 Regularization and Sparsity]] — The regularization that works with constraints
- **Next**: [[Feature Orthogonality Design]] — Design-time approach to reduce constraint violations
- **Related**: [[Texel Tuning Method]] — The base optimization algorithm
- **Related**: [[Credit Assignment Problem]] — Why confounding causes constraint violations
- **Related**: [[The Tuning Problem]] — The original motivation for all optimization
