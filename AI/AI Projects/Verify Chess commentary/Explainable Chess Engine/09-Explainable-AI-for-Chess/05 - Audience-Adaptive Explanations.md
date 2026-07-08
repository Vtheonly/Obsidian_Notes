---
tags:
  - chapter-09
  - xai
  - audience-adaptive
  - beginner
  - intermediate
  - advanced
  - explanation-levels
  - rule-templates
---

# 05 - Audience-Adaptive Explanations

## Why One Explanation Doesn't Fit All

A chess move that requires a paragraph of strategic analysis for a master might need only a simple sentence for a beginner. Conversely, an explanation that satisfies a beginner ("this move attacks the queen") may be frustratingly incomplete for a master who wants to understand the deeper strategic implications.

**Audience-adaptive explanations** are explanations that adjust their depth, vocabulary, and focus based on the recipient's chess understanding. This is not merely a formatting difference—it is a fundamental requirement for any chess engine that aims to be both a playing tool and a teaching tool.

### The Three Audience Levels

Our engine supports three audience levels:

| Level | Rating Range | What They Need | Vocabulary |
|-------|-------------|---------------|-----------|
| **Beginner** | Under 1200 | Simple, concrete explanations focusing on material and basic safety | "captures," "attacks," "defends" |
| **Intermediate** | 1200-1800 | Positional concepts introduced; connections between strategy and tactics | "outpost," "weak square," "open file" |
| **Advanced** | 1800+ | Deep strategic analysis; prophylactic reasoning; subtle evaluations | "prophylaxis," "concept bottleneck," "tension in the center" |

## Beginner-Level Explanations

### Design Principles

1. **Focus on material and basic safety**: Beginners understand captures, threats, and king safety. These are the foundations.
2. **Simple sentence structure**: Short, declarative sentences. One idea per sentence.
3. **No jargon**: Avoid terms like "outpost," "prophylaxis," "LPDO," "weak square." Use everyday language.
4. **Concrete over abstract**: "This move attacks the queen" not "This move improves piece activity."
5. **Positive framing**: Emphasize what the move *does*, not what it prevents.

### Beginner Explanation Templates

```python
class BeginnerExplainer:
    """
    Generates explanations for beginner-level players.
    Uses simple language, focuses on material and basic tactics.
    """
    
    # Simplified concept names for beginners
    CONCEPT_NAMES = {
        "Material Count": "material",
        "Hanging Capture": "free capture",
        "LPDO Detection": "undefended piece",
        "Pin Detection": "pin",
        "Fork Detection": "fork",
        "Knight Outpost": "strong knight position",
        "Bad Bishop": "blocked bishop",
        "Rook on Open File": "rook on open file",
        "Pawn Shield": "pawn shield",
        "King Exposure": "king safety",
        "Prophylaxis": "preventing opponent's plan",
        "Isolated Pawn": "weak pawn",
        "Back Rank Mate": "checkmate threat",
        "Development": "piece development",
        "Castling": "king safety",
    }
    
    def explain(self, move_san: str, primary_driver: tuple[str, int],
                primary_objection: tuple[str, int] | None,
                reasons: dict[str, str]) -> str:
        """
        Generate a beginner-level explanation.
        """
        if primary_driver is None:
            return f"{move_san} is a solid move that doesn't change much."
        
        driver_name, driver_delta = primary_driver
        simple_name = self.CONCEPT_NAMES.get(driver_name, driver_name.lower())
        reason = self._simplify_reason(reasons.get(driver_name, ""))
        
        # Template: "This move [does something good] because [simple reason]."
        if driver_delta > 50:
            template = f"{move_san} is a strong move! {reason}."
        elif driver_delta > 20:
            template = f"{move_san} is a good move. {reason}."
        else:
            template = f"{move_san} is a useful move. {reason}."
        
        # Add warning about objections if significant
        if primary_objection and abs(primary_objection[1]) > 30:
            obj_name = self.CONCEPT_NAMES.get(primary_objection[0], "a weakness")
            template += f" But be careful — this creates {obj_name}."
        
        return template
    
    def _simplify_reason(self, reason: str) -> str:
        """
        Simplify a technical reason into beginner-friendly language.
        """
        # Remove centipawn values
        import re
        reason = re.sub(r'\([^)]*cp\)', '', reason)
        reason = re.sub(r'\([^)]*centipawns\)', '', reason)
        
        # Replace technical terms
        replacements = {
            "outpost": "strong square where it can't be attacked by pawns",
            "LPDO": "undefended piece",
            "prophylaxis": "stops the opponent's plan",
            "pawn shield": "pawns protecting the king",
            "king exposure": "the king is not safe",
            "material advantage": "you have more pieces",
            "bishop pair": "having both bishops",
            "isolated pawn": "weak pawn with no pawns next to it",
        }
        
        for technical, simple in replacements.items():
            reason = reason.replace(technical, simple)
        
        return reason.strip()
```

### Beginner Examples

| Move | Explanation |
|------|------------|
| Nxf7 | "Nxf7 is a strong move! This captures a pawn and forks the rook and queen." |
| O-O | "Castling is a good move. This keeps your king safe behind the pawns." |
| Nd5 | "Nd5 is a good move. The knight moves to a strong square where it can't be attacked by pawns." |
| h3 | "h3 is a useful move. This stops the opponent from putting their bishop on g4 where it would pin your knight." |
| Rfd1 | "Rfd1 is a useful move. The rook moves to an open file where it can attack along the d-file." |

## Intermediate-Level Explanations

### Design Principles

1. **Introduce positional concepts**: Use terms like "outpost," "weak square," "open file," "bad bishop"
2. **Connect tactics to strategy**: "This tactical move achieves the strategic goal of..."
3. **Include secondary factors**: Mention supporting reasons, not just the primary one
4. **Acknowledge trade-offs**: If a move has a cost, mention it
5. **Named patterns**: Reference known patterns by name ("isolated queen pawn," "back rank mate")

### Intermediate Explanation Templates

```python
class IntermediateExplainer:
    """
    Generates explanations for intermediate-level players.
    Introduces positional vocabulary and strategic concepts.
    """
    
    def explain(self, move_san: str, deltas: dict[str, int],
                primary_driver: tuple[str, int] | None,
                primary_objection: tuple[str, int] | None,
                reasons: dict[str, str]) -> str:
        """Generate an intermediate-level explanation."""
        
        if primary_driver is None:
            return f"{move_san} maintains the current position."
        
        driver_name, driver_delta = primary_driver
        driver_reason = reasons.get(driver_name, "")
        
        # Primary reason
        parts = [f"{move_san} {self._phrase_improvement(driver_name, driver_reason)}"]
        
        # Secondary reasons (up to 2)
        secondary = [(n, d) for n, d in sorted(deltas.items(), key=lambda x: -x[1])
                     if d > 0 and n != driver_name][:2]
        if secondary:
            sec_phrases = [self._phrase_improvement(n, reasons.get(n, "")) for n, _ in secondary]
            parts.append(f"Additionally, it {', '.join(sec_phrases)}")
        
        # Objection (if significant)
        if primary_objection and abs(primary_objection[1]) > 15:
            obj_name, obj_delta = primary_objection
            obj_reason = reasons.get(obj_name, "")
            parts.append(f"However, {self._phrase_cost(obj_name, obj_reason)}")
        
        return ". ".join(parts) + "."
    
    def _phrase_improvement(self, rule_name: str, reason: str) -> str:
        """Phrase a positive delta as an improvement."""
        templates = {
            "Knight Outpost": "places the knight on an outpost where it cannot be attacked by pawns",
            "Bad Bishop": "improves the bishop by opening its diagonal",
            "Rook on Open File": "places the rook on an open file where it exerts pressure",
            "Prophylaxis": "prevents the opponent's plan",
            "Pawn Shield": "strengthens the king's pawn shield",
            "King Exposure": "improves king safety",
            "Isolated Pawn": "addresses the isolated pawn weakness",
            "Material Count": "gains material",
            "Hanging Capture": "captures an undefended piece",
            "LPDO Detection": "defends a previously undefended piece",
            "Development": "develops a piece to an active square",
        }
        return templates.get(rule_name, reason.lower() if reason else "improves the position")
    
    def _phrase_cost(self, rule_name: str, reason: str) -> str:
        """Phrase a negative delta as a cost."""
        templates = {
            "Knight Outpost": "the knight no longer occupies an outpost",
            "Bad Bishop": "the bishop becomes blocked by its own pawns",
            "Rook on Open File": "the rook leaves the open file",
            "King Exposure": "king safety is slightly reduced",
            "LPDO Detection": "this leaves a piece undefended",
            "Pawn Shield": "the pawn shield in front of the king is weakened",
        }
        return templates.get(rule_name, reason.lower() if reason else "this has a positional cost")
```

### Intermediate Examples

| Move | Explanation |
|------|------------|
| Nxf7 | "Nxf7 captures material by forking the rook and queen. Additionally, it removes a key defender near the king, opening the f-file for the rook." |
| O-O | "O-O secures the king behind the pawn shield. Additionally, it connects the rooks and brings the rook to the f-file." |
| Nd5 | "Nd5 places the knight on an outpost where it cannot be attacked by pawns, controlling the critical f6 and e7 squares. Additionally, it prevents the opponent's ...c5 pawn break." |
| h3 | "h3 prevents the opponent's plan of ...Bg4 which would pin the knight. However, this slightly weakens the kingside pawn structure." |
| Rac1 | "Rac1 places the rook on the semi-open c-file where it exerts pressure on c7. Additionally, it prepares to double rooks on the c-file." |

## Advanced-Level Explanations

### Design Principles

1. **Full strategic depth**: Use the complete vocabulary of chess strategy
2. **Prophylactic reasoning**: Explain what the move prevents and why that matters
3. **Positional nuance**: Acknowledge subtle trade-offs and long-term implications
4. **Multiple perspectives**: Present the move from both sides' perspectives
5. **Connecting concepts**: Show how different strategic themes interact

### Advanced Explanation Templates

```python
class AdvancedExplainer:
    """
    Generates explanations for advanced-level players.
    Full strategic depth, prophylactic reasoning, and nuance.
    """
    
    def explain(self, move_san: str, deltas: dict[str, int],
                primary_driver: tuple[str, int] | None,
                primary_objection: tuple[str, int] | None,
                reasons: dict[str, str],
                total_delta: int) -> str:
        """Generate an advanced-level explanation."""
        
        lines = [f"{move_san} (net evaluation delta: {total_delta:+d}cp)"]
        
        # Primary driver with full detail
        if primary_driver:
            name, delta = primary_driver
            reason = reasons.get(name, "")
            lines.append(f"  Primary: {name} (+{delta}cp) — {reason}")
        
        # All significant positive deltas
        positive = [(n, d) for n, d in sorted(deltas.items(), key=lambda x: -x[1]) if d > 0]
        for name, delta in positive[1:4]:  # Skip primary, show next 3
            reason = reasons.get(name, "")
            lines.append(f"  Supporting: {name} (+{delta}cp) — {reason}")
        
        # All significant negative deltas
        negative = [(n, d) for n, d in sorted(deltas.items(), key=lambda x: x[1]) if d < 0]
        for name, delta in negative[:3]:
            reason = reasons.get(name, "")
            lines.append(f"  Cost: {name} ({delta}cp) — {reason}")
        
        # Strategic synthesis
        synthesis = self._synthesize(move_san, deltas, primary_driver, primary_objection, reasons)
        lines.append(f"  Synthesis: {synthesis}")
        
        return "\n".join(lines)
    
    def _synthesize(self, move_san, deltas, driver, objection, reasons) -> str:
        """
        Create a one-sentence strategic synthesis that captures
        the essence of the move.
        """
        if driver is None:
            return f"{move_san} maintains the status quo."
        
        driver_name, driver_delta = driver
        
        syntheses = {
            "Knight Outpost": f"{move_san} establishes a permanent knight outpost, creating a strategic anchor that the opponent cannot challenge with pawns",
            "Prophylaxis": f"{move_san} serves a prophylactic function, denying the opponent their desired plan and maintaining positional control",
            "King Exposure": f"{move_san} exploits the opponent's king exposure, adding to the attacking potential while maintaining structural integrity",
            "Material Count": f"{move_san} gains material through a tactical sequence, converting a temporary advantage into a permanent one",
            "Bad Bishop": f"{move_san} resolves the bad bishop problem by opening the diagonal, transforming a passive piece into an active one",
        }
        
        base_synthesis = syntheses.get(driver_name, 
            f"{move_san} addresses the primary strategic concern: {reasons.get(driver_name, driver_name.lower())}")
        
        if objection:
            obj_name, obj_delta = objection
            base_synthesis += f", though at the cost of {reasons.get(obj_name, obj_name.lower())}"
        
        return base_synthesis
```

### Advanced Examples

| Move | Explanation |
|------|------------|
| Nd5 | "Nd5 (net: +65cp)\n  Primary: Knight Outpost (+50cp) — Knight occupies d5 outpost supported by e4 pawn\n  Supporting: Prophylaxis (+15cp) — Prevents ...c5 pawn break\n  Synthesis: Nd5 establishes a permanent knight outpost, creating a strategic anchor that the opponent cannot challenge with pawns, while simultaneously preventing ...c5." |
| h3 | "h3 (net: +8cp)\n  Primary: Prophylaxis (+15cp) — Prevents ...Bg4 pin on the knight\n  Cost: Pawn Structure (-5cp) — Creates potential weakness on g3\n  Synthesis: h3 serves a prophylactic function, denying the opponent their desired plan of ...Bg4 and maintaining positional control, though at the cost of slightly weakening the kingside pawn structure." |

## How the Same Rule Set Produces Different Explanations

### The Key Insight

The three audience levels are **not** three different rule sets—they are three different **renderings** of the same underlying data. The [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|heuristic deltas]] are identical at all levels; only the *presentation* changes.

```python
def explain_move_adaptive(board: chess.Board, move: chess.Move,
                          audience: str = "intermediate") -> str:
    """
    Explain a move at the specified audience level.
    
    The SAME rule evaluation produces DIFFERENT explanations
    based on the audience.
    """
    # Compute deltas (same for all levels)
    deltas = compute_rule_deltas(board, move, board.turn)
    primary_driver = find_primary_driver(deltas)
    primary_objection = find_primary_objection(deltas)
    reasons = get_reasons(board, move)
    move_san = board.san(move)
    
    # Select explainer based on audience
    if audience == "beginner":
        explainer = BeginnerExplainer()
    elif audience == "intermediate":
        explainer = IntermediateExplainer()
    elif audience == "advanced":
        explainer = AdvancedExplainer()
    else:
        explainer = IntermediateExplainer()
    
    return explainer.explain(move_san, deltas, primary_driver, 
                            primary_objection, reasons)
```

### The Same Move at Three Levels

**Move**: Nd5 in a position where the knight reaches a central outpost, prevents ...c5, and slightly exposes the c1 bishop.

| Level | Explanation |
|-------|------------|
| **Beginner** | "Nd5 is a good move. The knight moves to a strong square in the center where it can't be attacked by pawns. It also stops the opponent from pushing their c-pawn." |
| **Intermediate** | "Nd5 places the knight on an outpost where it cannot be attacked by pawns, controlling the critical f6 and e7 squares. Additionally, it prevents the opponent's ...c5 pawn break. However, the c1 bishop becomes temporarily undefended." |
| **Advanced** | "Nd5 (net: +40cp)\n  Primary: Knight Outpost (+50cp) — Knight occupies d5 outpost supported by e4 pawn, no enemy pawn can challenge\n  Supporting: Prophylaxis (+15cp) — Prevents ...c5 break that would activate Black's QS\n  Cost: LPDO (-20cp) — c1 bishop undefended during transition\n  Synthesis: Nd5 establishes a permanent knight outpost, creating a strategic anchor that the opponent cannot challenge with pawns, while simultaneously preventing ...c5, though the temporary undefended status of the c1 bishop must be monitored." |

This audience-adaptive system ensures that every player, regardless of skill level, receives an explanation they can understand and learn from—fulfilling the engine's core mission as a chess teacher.

---

*Previous: [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|04 - Move Explanation Architecture]] ←*
*Next: [[09-Explainable-AI-for-Chess/06 - Rule Conflict Resolution in Explanations|06 - Rule Conflict Resolution in Explanations]] →*
*See also: [[07-Chess-Psychology-and-Human-Thinking/01 - Human Chess Thinking Models|Human Chess Thinking Models]] | [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|Move Explanation Architecture]] | [[08-Rule-Based-Reasoning-Systems/03 - Multi-Rule Decision Making|Multi-Rule Decision Making]]*
