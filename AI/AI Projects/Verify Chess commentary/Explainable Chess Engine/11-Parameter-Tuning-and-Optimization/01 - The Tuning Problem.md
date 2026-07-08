# The Tuning Problem

> **Chapter 11 — Parameter Tuning & Optimization** | → [[Texel Tuning Method]] → [[Credit Assignment Problem]] → [[L1 Regularization and Sparsity]] → [[Constrained Optimization]] → [[Feature Orthogonality Design]]

---

## The Scale of the Problem

Our explainable chess engine uses over **200 heuristic rules**, each contributing a centipawn score to the position evaluation. Each rule has at least one weight parameter that determines how strongly it influences the evaluation. Some rules have multiple parameters (e.g., a passed pawn rule might have different weights for rank, file, and protection status).

The total parameter count easily exceeds **300 weights**. The tuning problem is: **what should each weight be?**

### Why This Matters for Explainability

The weight values directly determine the engine's behavior, and therefore the content of its explanations. If `Knight_Outpost` has a weight of 5 centipawns (trivial), the engine will rarely choose moves based on outposts, and the explanation will never mention them. If the weight is 150 centipawns (absurdly high), the engine will overvalue outposts and produce poor play, but its explanations will obsess over outposts.

**Correct weights = correct play = correct explanations.** The tuning problem is not merely an optimization problem—it's the foundation of the entire explainable system.

---

## Why Manual Weight Assignment Fails

### The Naive Approach

One might think: "I'm a chess expert. I know that a knight outpost is worth about 40 centipawns, a bishop pair about 50 centipawns, and an open file for a rook about 30 centipawns." This seems reasonable, but it breaks down immediately.

### Problem 1: Interdependency

Weights are not independent. The value of a knight outpost depends on:
- The game phase (more valuable in middlegame than endgame)
- The pawn structure (more valuable if the outpost is permanent)
- The opponent's ability to challenge it
- The king safety situation (outpost near the king is worth more)
- The presence of a bishop pair (knight + bishop synergies)

Changing one weight can dramatically change the optimal value of many others. With 300 parameters, the search space is:

$$\text{Search Space} = \prod_{i=1}^{300} V_i$$

Where $V_i$ is the range of valid values for weight $i$. Even with a coarse granularity of 1 centipawn and a range of [-100, +100]:

$$\text{Search Space} = 201^{300} \approx 10^{693}$$

This is astronomically larger than the number of atoms in the observable universe ($\sim 10^{80}$). Manual search is impossible.

### Problem 2: The Centipawn Scale

Chess evaluation is in centipawns (1/100 of a pawn). A 5 centipawn error in a weight is small in isolation, but with 200+ rules, compounding errors can produce evaluations that are off by hundreds of centipawns—equivalent to several pawns.

### Problem 3: Context Sensitivity

A rule's weight should ideally vary by position context. A passed pawn on the 7th rank is worth far more than on the 2nd rank. A knight on the rim is bad in the opening but might be fine in an endgame. Manual assignment can't capture this nuance for hundreds of rules.

### Problem 4: Confirmation Bias

Human experts tend to overvalue rules they understand well and undervalue subtle, hard-to-articulate rules. A chess programmer might set `King_Safety = 80cp` because they can clearly see when a king is unsafe, but set `Piece_Coordination = 10cp` because the concept is fuzzier—even though coordination might be equally important in practice.

### Historical Example

The chess engine **Crafty** by Robert Hyatt was hand-tuned for years. Despite Hyatt's deep chess knowledge and extensive testing, Crafty was consistently outplayed by engines with automated tuning (like Stockfish with its SPSA-tuned parameters). The lesson: even world-class chess understanding can't match systematic optimization on game data.

---

## The Need for Automated Optimization

### What We Need

An automated tuning system that:

1. **Uses game data**: Real games between strong players provide ground truth about which positions are winning
2. **Optimizes all weights simultaneously**: Captures interdependencies
3. **Respects domain constraints**: Pawn = 100cp, Knight_On_Rim must be negative, etc.
4. **Produces interpretable weights**: We need to understand the tuned values for explanation
5. **Scales**: Must handle 300+ parameters efficiently

### The Data: Game Outcomes

Our training data consists of positions extracted from high-level games with known outcomes:

| Data Point | Content |
|---|---|
| Position $i$ | Board state as FEN or feature vector |
| Features $\mathbf{F}_i$ | The 300 rule activations for this position |
| Outcome $R_i$ | Game result: 1.0 (White wins), 0.5 (draw), 0.0 (Black wins) |

The key insight: **a well-tuned evaluation function should predict game outcomes**. If the engine evaluates a position as +1.50 for White, White should win with high probability.

### The Learning Framework

This is essentially a **regression problem**: learn a mapping from position features to game outcomes.

$$\hat{R}_i = f(\mathbf{F}_i; \mathbf{W})$$

Where:
- $\hat{R}_i$ = predicted outcome for position $i$
- $\mathbf{F}_i$ = feature vector (rule activations)
- $\mathbf{W}$ = weight vector (what we're learning)
- $f$ = the evaluation function with sigmoid mapping

The most successful approach for chess is [[Texel Tuning Method]], which uses logistic regression on game outcomes with a sigmoid mapping.

---

## Why Not Reinforcement Learning?

One might ask: why not use RL (like AlphaZero) to learn the weights? Several reasons:

1. **Data efficiency**: RL requires millions of self-play games. Texel tuning works with ~10,000 positions from real games.
2. **Interpretability**: RL can produce opaque weight patterns. Gradient descent on a fixed dataset produces more interpretable weights.
3. **Stability**: RL training is notoriously unstable. Supervised learning on game outcomes is well-understood.
4. **Explainability constraint**: Our weights must be interpretable. RL tends to find correlations that aren't human-meaningful.
5. **Computational cost**: RL requires GPU clusters. Texel tuning runs on a laptop.

That said, RL can be used as a *complementary* approach for fine-tuning after initial Texel tuning. The [[Neuro-Symbolic Architecture Overview|neuro-symbolic architecture]] supports this.

---

## The Weight Vector

Let's define the weight vector formally:

$$\mathbf{W} = [w_1, w_2, \ldots, w_n]$$

Where $n$ is the number of tunable parameters (typically 200-350). Each weight $w_j$ corresponds to a rule or a sub-feature of a rule.

### Weight Categories

| Category | Count | Example Rules | Typical Range |
|---|---|---|---|
| Material | 6 | Pawn, Knight, Bishop, Rook, Queen, King | Fixed or narrow |
| Pawn Structure | 30+ | Doubled, Isolated, Backward, Passed, Connected | -50 to +100 |
| Piece Placement | 50+ | Outpost, Rim, Center, Development | -40 to +80 |
| King Safety | 25+ | Pawn Shield, Open File, Attack Units | -100 to +50 |
| Mobility | 15+ | Per-piece mobility coefficients | -2 to +5 per square |
| Space | 10+ | Per-rank space bonus | 1 to 10 |
| Threats | 20+ | Hanging, Overloaded, Pin | -100 to +30 |
| Phase-Dependent | 60+ | MG/EG split for above | Two values each |

### The Phase Split

Many rules have different weights for the middlegame (MG) and endgame (EG). The interpolated score is:

$$S = \frac{\text{Phase} \cdot S_{MG} + (24 - \text{Phase}) \cdot S_{EG}}{24}$$

Where $\text{Phase}$ ranges from 0 (all heavy pieces gone → pure endgame) to 24 (all pieces present → pure middlegame), with each non-pawn non-king piece contributing: Queen=4, Rook=2, Bishop=1, Knight=1.

This effectively doubles the parameter count for phase-dependent rules.

---

## The Optimization Landscape

The loss function for chess evaluation tuning is **non-convex** due to the sigmoid mapping and feature interactions. However, it is:

- **Smooth** (differentiable almost everywhere)
- **Bounded** (the sigmoid output is in [0, 1])
- **Well-conditioned** near the optimum (if features are reasonably scaled)

This makes gradient-based optimization feasible, which is the basis of [[Texel Tuning Method]].

### Local Minima

The main concern is local minima—weight configurations that are locally optimal but globally suboptimal. Mitigations:

1. **Multiple random restarts**: Start optimization from different initial points
2. **Simulated annealing**: Occasionally accept worse solutions to escape local minima
3. **SPSA**: Simultaneous Perturbation Stochastic Approximation (used by Stockfish)
4. **Good initialization**: Start from hand-tuned values rather than random

---

## Connections

- **Next**: [[Texel Tuning Method]] — The specific optimization algorithm we use
- **Related**: [[Credit Assignment Problem]] — Why tuning is hard with correlated features
- **Related**: [[L1 Regularization and Sparsity]] — Ensuring interpretability of tuned weights
- **Related**: [[Constrained Optimization]] — Domain constraints on weights
- **Related**: [[Feature Orthogonality Design]] — Designing rules that are easier to tune
- **Broader**: [[Declarative Rule Engine with Bitboards]] — The rules that produce the features
