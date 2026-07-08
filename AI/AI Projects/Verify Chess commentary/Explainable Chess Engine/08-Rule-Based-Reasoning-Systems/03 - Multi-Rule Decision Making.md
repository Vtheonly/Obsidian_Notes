---
tags:
  - chapter-08
  - rule-engine
  - multi-rule
  - decision-making
  - score-combination
  - conflict-resolution
  - additive-aggregation
  - explanation
---

# 03 - Multi-Rule Decision Making

## The Challenge of Combining Multiple Rules

A single rule tells you one thing about a position. But chess positions are complex—they have material considerations, tactical threats, structural features, and safety concerns all at once. The engine must combine the outputs of many rules into a single decision, and the way it combines them determines both the quality of the decision and the quality of the explanation.

This is the **multi-rule decision problem**: given $N$ rules, each producing a score $s_i$ and a reason $r_i$, how do we produce a single total score $S$ and a coherent explanation?

## Additive Combination

### The Weighted Sum

The simplest and most transparent combination method is **weighted additive aggregation**:

$$S_{total} = \sum_{i=1}^{N} w_i \cdot s_i$$

This formula has several important properties:

1. **Decomposability**: The total score can be decomposed into individual contributions: $S_{total} = c_1 + c_2 + \ldots + c_N$ where $c_i = w_i \cdot s_i$
2. **Independence**: Each rule's contribution is independent of other rules—changing one rule's score doesn't affect other rules' contributions
3. **Transparency**: You can see exactly which rules contributed positively and which contributed negatively
4. **Simplicity**: The formula is easy to understand and implement

### Implementation

```python
def combine_rules_weighted_sum(results: list[tuple[str, int, str, float]]) -> tuple[int, dict[str, float], list[str]]:
    """
    Combine rule scores using weighted additive aggregation.
    
    Args:
        results: List of (rule_name, score, reason, weight) tuples
    
    Returns:
        (total_score, contributions, explanations)
        - total_score: The combined weighted score
        - contributions: Dict mapping rule_name to its weighted contribution
        - explanations: List of explanation strings (only for rules that fired)
    """
    total_score = 0
    contributions = {}
    explanations = []
    
    for rule_name, score, reason, weight in results:
        weighted_score = int(score * weight)
        total_score += weighted_score
        contributions[rule_name] = weighted_score
        
        if reason:  # Only include rules that fired
            explanations.append(f"[{rule_name}] {reason} (contribution: {weighted_score:+d}cp)")
    
    return total_score, contributions, explanations
```

### Example: Multi-Rule Evaluation of a Position

Consider a position where White is considering the move Nd5:

| Rule | Raw Score | Weight | Weighted Contribution | Reason |
|------|-----------|--------|----------------------|--------|
| Material Count | 0 | 1.0 | 0 | Material is equal |
| Knight Outpost | +50 | 0.7 | +35 | Knight on d5 outpost, controlling 8 squares |
| Pawn Structure | -10 | 0.8 | -8 | Isolated e-pawn |
| King Safety | +20 | 0.9 | +18 | Pawn shield intact |
| LPDO Detection | -30 | 0.9 | -27 | Undefended bishop on c1 |
| Prophylaxis | +15 | 0.5 | +7 | Prevents opponent's ...c5 break |
| **Total** | | | **+25** | |

The total score is +25 centipawns (¼ pawn advantage), and the explanation is immediately available: "This move is slightly better because the knight reaches a powerful outpost on d5 (+35cp), though this is partially offset by an undefended bishop on c1 (-27cp) and an isolated e-pawn (-8cp). The move also prevents the opponent's ...c5 break (+7cp)."

### Why Not More Complex Combination Methods?

You might wonder why we don't use more sophisticated combination methods like:
- **Multiplicative**: $S = \prod s_i$ — Amplifies individual contributions but makes decomposition impossible
- **Neural combination**: A small neural net that takes rule scores as inputs — Powerful but opaque
- **Weighted voting**: Rules vote for moves, majority wins — Loses score magnitude information
- **Max/min aggregation**: Take the best/worst rule score — Ignores all other rules

The additive combination is the right choice because it **preserves decomposability**, which is essential for explanation. The total score is always the sum of individual contributions, and each contribution can be inspected independently. More complex methods might produce better scores in some cases, but they would sacrifice the core property that makes our engine explainable.

## The Conflict Problem

### When Rules Disagree

One of the most interesting aspects of multi-rule decision making is **conflict**: when some rules support a move and others oppose it. In the example above, the Knight Outpost rule supports Nd5 (+35cp weighted) while the LPDO rule opposes it (-27cp weighted). These rules are in conflict.

Conflicts are not bugs—they are features. They reflect the genuine complexity of chess, where a move can be both good and bad for different reasons. The engine's job is not to resolve conflicts but to **present them honestly** in the explanation.

### Types of Conflicts

| Conflict Type | Example | Resolution |
|---------------|---------|------------|
| **Material vs. Position** | Sacrifice material for positional advantage | Net score decides; explanation presents both sides |
| **Safety vs. Activity** | Risk king safety for piece activity | Context-dependent; safety usually wins when close |
| **Short-term vs. Long-term** | Immediate gain vs. long-term weakness | Depends on game phase and position type |
| **Offense vs. Defense** | Attack vs. prophylaxis | Depends on who has the initiative |

### Conflict Detection

```python
def detect_conflicts(contributions: dict[str, float], 
                      threshold: float = 15.0) -> list[tuple[str, str, str]]:
    """
    Detect conflicts between rules.
    A conflict exists when one rule supports a move and another opposes it,
    both with significant magnitude.
    
    Returns list of (supporting_rule, opposing_rule, conflict_type) tuples.
    """
    positive = {name: score for name, score in contributions.items() if score > threshold}
    negative = {name: score for name, score in contributions.items() if score < -threshold}
    
    conflicts = []
    
    for pos_name, pos_score in positive.items():
        for neg_name, neg_score in negative.items():
            # Classify the conflict
            pos_rule = get_rule_by_name(pos_name)
            neg_rule = get_rule_by_name(neg_name)
            
            if pos_rule.category != neg_rule.category:
                conflict_type = f"{pos_rule.category} vs. {neg_rule.category}"
            else:
                conflict_type = f"within {pos_rule.category}"
            
            conflicts.append((pos_name, neg_name, conflict_type))
    
    return conflicts
```

## Priority Schemes

### When Weights Aren't Enough

In some cases, simple weighted addition isn't sufficient because certain rules should **override** others regardless of their weights. For example:
- A checkmate threat should override everything
- A hanging queen should override positional considerations
- A back-rank mate should override development concerns

We handle these cases with a **priority scheme**:

```python
class RulePriority:
    """
    Priority levels for rule evaluation.
    Higher priority rules are evaluated first and can override lower priority results.
    """
    CRITICAL = 4   # Checkmate, hanging queen, etc.
    HIGH = 3       # Material changes, king safety threats
    MEDIUM = 2     # Tactical threats, pawn structure
    LOW = 1        # Positional nuances, prophylaxis
    MINIMUM = 0    # Cosmetic adjustments
    
    @staticmethod
    def get_priority(rule: Rule) -> int:
        """Get the priority level for a rule."""
        if rule.category == "safety" and rule.weight >= 0.9:
            return RulePriority.CRITICAL
        elif rule.category in ["material", "safety"]:
            return RulePriority.HIGH
        elif rule.category in ["tactical", "trap"]:
            return RulePriority.MEDIUM
        elif rule.category in ["strategy", "opening"]:
            return RulePriority.LOW
        else:
            return RulePriority.MINIMUM
```

### The Priority-Aware Combiner

```python
def combine_rules_priority_aware(results: list[tuple[str, int, str, float, int]]) -> tuple[int, dict, list[str]]:
    """
    Combine rules with priority awareness.
    
    Critical rules can flag the position as requiring immediate attention,
    which modifies how other rules' contributions are weighted.
    """
    # Sort by priority (highest first)
    sorted_results = sorted(results, key=lambda x: x[4], reverse=True)
    
    total_score = 0
    contributions = {}
    explanations = []
    has_critical = False
    
    for rule_name, score, reason, weight, priority in sorted_results:
        weighted_score = int(score * weight)
        
        # If a critical rule fires, reduce the weight of lower-priority rules
        if has_critical and priority < RulePriority.HIGH:
            weighted_score = int(weighted_score * 0.5)  # Halve contribution
        
        if priority == RulePriority.CRITICAL and abs(weighted_score) > 50:
            has_critical = True
        
        total_score += weighted_score
        contributions[rule_name] = weighted_score
        
        if reason:
            explanations.append(f"[{rule_name}] {reason} ({weighted_score:+d}cp, priority: {priority})")
    
    return total_score, contributions, explanations
```

## Net Score = Decision, Individual Rules = Explanation

### The Fundamental Principle

The key insight of multi-rule decision making is the **separation between decision and explanation**:

- **Decision**: The net total score determines which move is best
- **Explanation**: The individual rule contributions explain *why* the decision was made

This separation is what makes our engine fundamentally different from a conventional engine. A conventional engine says "Nd5 is the best move with score +0.25." Our engine says "Nd5 is the best move because it places the knight on an outpost (+35cp), prevents the opponent's ...c5 break (+7cp), and supports the king safety (+18cp), though it leaves the c1 bishop undefended (-27cp) and doesn't address the isolated e-pawn (-8cp)."

The decision is the same (+25cp), but the explanation is rich, informative, and actionable. The player knows what's good about the move, what's bad, and what to watch out for.

### The Explanation Hierarchy

Not all rules are equally important for the explanation. The explanation pipeline presents rules in order of their contribution:

```python
def generate_explanation(contributions: dict[str, float], 
                         reasons: dict[str, str],
                         audience: str = "intermediate") -> str:
    """
    Generate a structured explanation from rule contributions.
    """
    # Sort by absolute contribution (most important first)
    sorted_contribs = sorted(contributions.items(), 
                            key=lambda x: abs(x[1]), 
                            reverse=True)
    
    # Filter to only rules that fired
    active = [(name, score) for name, score in sorted_contribs 
              if name in reasons and reasons[name]]
    
    if not active:
        return "This move maintains the current position without significant changes."
    
    # Primary driver (largest contribution)
    primary_name, primary_score = active[0]
    primary_reason = reasons[primary_name]
    
    # Supporting factors
    supporting = [(name, score) for name, score in active[1:] if score > 0]
    # Opposing factors
    opposing = [(name, score) for name, score in active[1:] if score < 0]
    
    # Build explanation
    if primary_score > 0:
        explanation = f"The primary benefit is {primary_reason.lower()}."
    else:
        explanation = f"The main concern is {primary_reason.lower()}."
    
    if supporting and audience != "beginner":
        support_strs = [reasons[name].lower() for name, _ in supporting[:2]]
        explanation += f" Additionally, {', '.join(support_strs)}."
    
    if opposing and audience != "beginner":
        oppose_strs = [reasons[name].lower() for name, _ in opposing[:2]]
        explanation += f" However, {', '.join(oppose_strs)}."
    
    return explanation
```

## When Additive Combination Fails

### Known Limitations

Additive combination has known limitations that we must acknowledge:

1. **Non-linear interactions**: Some rules interact non-linearly. A knight on an outpost is much more valuable when the position is closed than when it's open. The additive model treats these the same.
2. **Redundancy**: Two rules may be measuring the same thing (e.g., "bad bishop" and "blocked bishop"), leading to double-counting.
3. **Threshold effects**: Some positional features have threshold effects—they don't matter at all below a certain level, but matter enormously above it. The additive model can't capture this.

These limitations are accepted as a trade-off for explainability. Our engine prioritizes transparency over maximum accuracy, and the additive combination model is the most transparent possible.

### Mitigation Strategies

- **Category-level normalization**: Prevent double-counting by normalizing within categories
- **Redundancy detection**: Check for rules that always fire together and merge them
- **Context-dependent weights**: Adjust weights based on game phase and position type (see [[08-Rule-Based-Reasoning-Systems/04 - Confidence Scoring and Rule Weighting|Confidence Scoring and Rule Weighting]])

---

*Previous: [[08-Rule-Based-Reasoning-Systems/02 - Chess Knowledge Representation|02 - Chess Knowledge Representation]] ←*
*Next: [[08-Rule-Based-Reasoning-Systems/04 - Confidence Scoring and Rule Weighting|04 - Confidence Scoring and Rule Weighting]] →*
*See also: [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]] | [[09-Explainable-AI-for-Chess/06 - Rule Conflict Resolution in Explanations|Rule Conflict Resolution in Explanations]]*
