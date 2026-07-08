---
tags:
  - chapter-08
  - rule-engine
  - code-architecture
  - python
  - class-hierarchy
  - module-system
  - rule-modules
  - reasoning-collection
---

# 05 - The Rule Module System (Code)

## Architecture Overview

The Rule Module System is the complete Python implementation of the rule engine described in the previous notes. It brings together the [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|declarative rule architecture]], [[08-Rule-Based-Reasoning-Systems/02 - Chess Knowledge Representation|knowledge representation]], [[08-Rule-Based-Reasoning-Systems/03 - Multi-Rule Decision Making|multi-rule decision making]], and [[08-Rule-Based-Reasoning-Systems/04 - Confidence Scoring and Rule Weighting|confidence scoring]] into a cohesive, production-ready codebase.

## The Class Hierarchy

### Base Class: Rule

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import chess


@dataclass
class RuleResult:
    """
    Encapsulates the result of a rule evaluation.
    """
    score: int = 0               # Centipawns (>0 good for moving side)
    reason: str = ""             # Human-readable explanation
    activation: float = 1.0      # Activation strength [0.0, 1.0]
    confidence: float = 1.0      # Confidence in this result [0.0, 1.0]
    
    @property
    def fired(self) -> bool:
        """Whether this rule produced a meaningful result."""
        return self.reason != ""
    
    @property
    def effective_score(self) -> int:
        """Score adjusted by activation and confidence."""
        return int(self.score * self.activation * self.confidence)
    
    def __repr__(self) -> str:
        if not self.fired:
            return "RuleResult(not fired)"
        return (f"RuleResult(score={self.score}, effective={self.effective_score}, "
                f"reason='{self.reason}')")


class Rule(ABC):
    """
    Abstract base class for all evaluation rules.
    
    Every rule in the system inherits from this class and implements
    the evaluate() method. The base class provides:
    - Identity: name, description, category
    - Weighting: weight (base importance), dynamic_weight (context-adjusted)
    - Evaluation interface: evaluate() returns RuleResult
    - Utility methods: condition_met(), compute_score(), generate_reason()
    """
    
    # Identity
    name: str = "Unnamed Rule"
    description: str = "No description"
    category: str = "general"
    
    # Weighting
    weight: float = 1.0
    
    # Priority (used for conflict resolution)
    priority: int = 2  # 0=min, 4=critical
    
    @abstractmethod
    def evaluate(self, board: chess.Board, move: Optional[chess.Move] = None,
                 color: Optional[chess.Color] = None) -> RuleResult:
        """
        Evaluate the rule for the given context.
        
        Args:
            board: The current board state
            move: Optional candidate move
            color: Optional perspective color
            
        Returns:
            RuleResult with score, reason, activation, and confidence
        """
        pass
    
    def evaluate_position(self, board: chess.Board, 
                          color: chess.Color) -> RuleResult:
        """Convenience method: evaluate for a position (no specific move)."""
        return self.evaluate(board, move=None, color=color)
    
    def evaluate_move(self, board: chess.Board, move: chess.Move,
                      color: chess.Color) -> RuleResult:
        """
        Evaluate the effect of a move.
        Compares rule scores before and after the move.
        """
        # Score before the move
        result_before = self.evaluate(board, move=None, color=color)
        
        # Score after the move
        board.push(move)
        result_after = self.evaluate(board, move=None, color=color)
        board.pop()
        
        # Delta
        delta = result_after.effective_score - result_before.effective_score
        
        if abs(delta) < 5:  # Below significance threshold
            return RuleResult(score=0, reason="")
        
        reason = self._describe_delta(result_before, result_after, delta)
        return RuleResult(
            score=delta,
            reason=reason,
            activation=max(result_before.activation, result_after.activation),
            confidence=min(result_before.confidence, result_after.confidence)
        )
    
    def _describe_delta(self, before: RuleResult, after: RuleResult, 
                         delta: int) -> str:
        """Generate a description of the change caused by a move."""
        if delta > 0:
            return f"Improves {self.name.lower()}: {after.reason}"
        else:
            return f"Worsens {self.name.lower()}: {after.reason}"
    
    def __repr__(self) -> str:
        return f"Rule({self.name}, w={self.weight}, cat={self.category}, p={self.priority})"
    
    def __str__(self) -> str:
        return f"[{self.category}/{self.name}] {self.description} (weight: {self.weight})"
```

### Category Base Classes

```python
class MaterialRule(Rule):
    """Base class for material-related rules."""
    category = "material"
    priority = 3  # Material is high priority


class TacticalRule(Rule):
    """Base class for tactical rules."""
    category = "tactical"
    priority = 3  # Tactical threats are high priority


class OpeningRule(Rule):
    """Base class for opening rules."""
    category = "opening"
    priority = 2  # Opening rules are medium priority
    
    def _is_opening(self, board: chess.Board) -> bool:
        """Check if we're still in the opening phase."""
        piece_count = len(board.piece_map())
        return piece_count >= 24  # Rough heuristic


class TrapRule(Rule):
    """Base class for trap detection rules."""
    category = "trap"
    priority = 3


class StrategyRule(Rule):
    """Base class for strategic/positional rules."""
    category = "strategy"
    priority = 1  # Strategy is lower priority than tactics


class SafetyRule(Rule):
    """Base class for king safety rules."""
    category = "safety"
    priority = 4  # Safety is critical priority
```

## Complete Rule Implementations

### Material Rules

```python
class MaterialCountRule(MaterialRule):
    name = "Material Count"
    description = "Evaluates the material balance based on standard piece values"
    weight = 1.0
    
    PIECE_VALUES = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
        chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0
    }
    
    def evaluate(self, board, move=None, color=None):
        if color is None:
            color = board.turn
        
        white_mat = sum(self.PIECE_VALUES.get(p.piece_type, 0)
                       for p in board.piece_map().values()
                       if p.color == chess.WHITE and p.piece_type != chess.KING)
        black_mat = sum(self.PIECE_VALUES.get(p.piece_type, 0)
                       for p in board.piece_map().values()
                       if p.color == chess.BLACK and p.piece_type != chess.KING)
        
        score = (white_mat - black_mat) if color == chess.WHITE else (black_mat - white_mat)
        
        if abs(score) < 10:
            return RuleResult(score=0, reason="Material is equal")
        
        side = "advantage" if score > 0 else "disadvantage"
        pawns = abs(score) / 100
        return RuleResult(
            score=score,
            reason=f"Material {side} of {pawns:.1f} pawns",
            activation=min(1.0, abs(score) / 300),
            confidence=1.0
        )


class BishopPairRule(MaterialRule):
    name = "Bishop Pair"
    description = "Bonus for having both bishops"
    weight = 0.8
    
    def evaluate(self, board, move=None, color=None):
        if color is None:
            color = board.turn
        
        bishops = [p for p in board.piece_map().values()
                   if p.piece_type == chess.BISHOP and p.color == color]
        
        if len(bishops) < 2:
            return RuleResult(score=0, reason="")
        
        # Check if bishops are on different color complexes
        squares = [sq for sq, p in board.piece_map().items()
                   if p.piece_type == chess.BISHOP and p.color == color]
        colors = set(chess.square_color(sq) for sq in squares)
        
        if len(colors) >= 2:
            return RuleResult(
                score=45,
                reason="Bishop pair — controls both color complexes",
                activation=1.0,
                confidence=0.9
            )
        
        return RuleResult(score=0, reason="")
```

### Tactical Rules

```python
class LPDORule(TacticalRule):
    name = "LPDO Detection"
    description = "Detects undefended pieces that are tactical targets"
    weight = 0.9
    
    PIECE_VALUES = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
        chess.ROOK: 500, chess.QUEEN: 900
    }
    
    def evaluate(self, board, move=None, color=None):
        if color is None:
            color = board.turn
        
        enemy_color = not color
        loose_pieces = []
        
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece is None or piece.color != color:
                continue
            if piece.piece_type in [chess.PAWN, chess.KING]:
                continue
            
            is_defended = board.is_attacked_by(color, sq)
            is_attacked = board.is_attacked_by(enemy_color, sq)
            
            if not is_defended and is_attacked:
                value = self.PIECE_VALUES.get(piece.piece_type, 0)
                loose_pieces.append((sq, piece, value))
        
        if not loose_pieces:
            return RuleResult(score=0, reason="")
        
        total_value = sum(v for _, _, v in loose_pieces)
        descriptions = [
            f"undefended {chess.piece_name(p.piece_type)} on {chess.square_name(sq)}"
            for sq, p, _ in loose_pieces[:3]
        ]
        
        return RuleResult(
            score=-total_value // 4,  # Penalty proportional to value
            reason=f"LPDO: {', '.join(descriptions)}",
            activation=min(1.0, total_value / 600),
            confidence=0.9
        )


class HangingCaptureRule(TacticalRule):
    name = "Hanging Capture"
    description = "Detects undefended pieces that can be captured"
    weight = 1.0
    priority = 4  # Critical — can win material immediately
    
    PIECE_VALUES = {
        chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
        chess.ROOK: 500, chess.QUEEN: 900
    }
    
    def evaluate(self, board, move=None, color=None):
        if color is None:
            color = board.turn
        
        captures = []
        
        for move_candidate in board.legal_moves:
            if board.is_capture(move_candidate):
                target_sq = move_candidate.to_square
                target_piece = board.piece_at(target_sq)
                
                if target_piece is None:
                    continue
                
                # Check if the capture wins material
                attacker = board.piece_at(move_candidate.from_square)
                if attacker is None:
                    continue
                
                attacker_value = self.PIECE_VALUES.get(attacker.piece_type, 0)
                target_value = self.PIECE_VALUES.get(target_piece.piece_type, 0)
                
                # Is the target undefended?
                board.push(move_candidate)
                is_recaptured = board.is_attacked_by(not color, target_sq)
                board.pop()
                
                if target_value > attacker_value or not is_recaptured:
                    net_gain = target_value - (attacker_value if is_recaptured else 0)
                    if net_gain > 0:
                        captures.append((move_candidate, net_gain))
        
        if not captures:
            return RuleResult(score=0, reason="")
        
        best_capture = max(captures, key=lambda x: x[1])
        move_obj, gain = best_capture
        
        return RuleResult(
            score=gain,
            reason=f"Can capture: {board.san(move_obj)} wins {gain}cp",
            activation=1.0,
            confidence=1.0
        )
```

### Strategy Rules

```python
class KnightOutpostRule(StrategyRule):
    name = "Knight Outpost"
    description = "Bonus for knights on strong outposts"
    weight = 0.7
    
    def evaluate(self, board, move=None, color=None):
        if color is None:
            color = board.turn
        
        outpost_bonus = 0
        outpost_descriptions = []
        
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece is None or piece.piece_type != chess.KNIGHT or piece.color != color:
                continue
            
            rank = chess.square_rank(sq)
            
            # Check if this is an outpost
            if not self._is_outpost(board, sq, color):
                continue
            
            # Score based on depth
            if color == chess.WHITE:
                depth = rank - 3
            else:
                depth = (7 - rank) - 3
            
            bonus = 30 + max(0, depth) * 15
            outpost_bonus += bonus
            outpost_descriptions.append(
                f"knight on {chess.square_name(sq)} (rank {rank + 1} outpost)"
            )
        
        if not outpost_descriptions:
            return RuleResult(score=0, reason="")
        
        return RuleResult(
            score=outpost_bonus,
            reason=f"Outpost knight(s): {', '.join(outpost_descriptions)}",
            activation=min(1.0, outpost_bonus / 60),
            confidence=0.8
        )
    
    def _is_outpost(self, board, square, color):
        """Check if a square is an outpost for the given color."""
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        # Outposts are on ranks 4-6
        if color == chess.WHITE and rank < 3:
            return False
        if color == chess.BLACK and rank > 4:
            return False
        
        # Must be supported by a friendly pawn
        supported = False
        for adj_file in [file - 1, file + 1]:
            support_rank = rank - 1 if color == chess.WHITE else rank + 1
            if 0 <= adj_file <= 7 and 0 <= support_rank <= 7:
                pawn_sq = chess.square(adj_file, support_rank)
                pawn = board.piece_at(pawn_sq)
                if pawn and pawn.piece_type == chess.PAWN and pawn.color == color:
                    supported = True
                    break
        
        if not supported:
            return False
        
        # No enemy pawn can attack this square
        enemy_color = not color
        for adj_file in [file - 1, file + 1]:
            attack_rank = rank + 1 if enemy_color == chess.WHITE else rank - 1
            if 0 <= adj_file <= 7 and 0 <= attack_rank <= 7:
                pawn_sq = chess.square(adj_file, attack_rank)
                pawn = board.piece_at(pawn_sq)
                if pawn and pawn.piece_type == chess.PAWN and pawn.color == enemy_color:
                    return False
        
        return True
```

## Module Organization

### File Structure

```
rules/
├── __init__.py
├── base.py                    # Rule, RuleResult, category base classes
├── material/
│   ├── __init__.py
│   ├── material_count.py      # MaterialCountRule
│   ├── bishop_pair.py         # BishopPairRule
│   └── exchange_advantage.py  # ExchangeAdvantageRule
├── tactical/
│   ├── __init__.py
│   ├── lpdo.py                # LPDORule
│   ├── pin_detection.py       # PinDetectionRule
│   ├── hanging_capture.py     # HangingCaptureRule
│   └── fork_detection.py      # ForkDetectionRule
├── opening/
│   ├── __init__.py
│   ├── development.py         # DevelopmentRule
│   ├── castling.py            # CastlingRule
│   └── central_control.py     # CentralControlRule
├── trap/
│   ├── __init__.py
│   ├── back_rank_mate.py      # BackRankMateRule
│   └── sacrifice_pattern.py   # SacrificePatternRule
├── strategy/
│   ├── __init__.py
│   ├── pawn_structure.py      # IsolatedPawnRule, DoubledPawnRule, PassedPawnRule
│   ├── knight_outpost.py      # KnightOutpostRule
│   ├── bad_bishop.py          # BadBishopRule
│   ├── rook_open_file.py      # RookOnOpenFileRule
│   └── prophylaxis.py         # ProphylaxisRule
├── safety/
│   ├── __init__.py
│   ├── pawn_shield.py         # PawnShieldRule
│   ├── king_exposure.py       # KingExposureRule
│   └── attack_units.py        # AttackUnitsRule
└── registry.py                # RuleDictionary, RuleEngine
```

## The RuleEngine: Orchestrating All Rules

```python
class RuleEngine:
    """
    The main engine that orchestrates all rule evaluations.
    Manages rule registration, evaluation, score combination,
    and explanation generation.
    """
    
    def __init__(self):
        self.dictionary = RuleDictionary()
        self.weight_calculator = DynamicWeightCalculator(
            {rule.name: rule.weight for rule in self.dictionary.get_all_rules()}
        )
    
    def evaluate_position(self, board: chess.Board, 
                          color: Optional[chess.Color] = None) -> PositionEvaluation:
        """
        Evaluate a complete position using all rules.
        """
        if color is None:
            color = board.turn
        
        # Compute dynamic weights
        dynamic_weights = self.weight_calculator.compute_weights(board)
        
        # Evaluate all rules
        results = {}
        for rule in self.dictionary.get_all_rules():
            result = rule.evaluate(board, color=color)
            
            # Apply dynamic weight
            adjusted_weight = dynamic_weights.get(rule.name, rule.weight)
            results[rule.name] = (result, adjusted_weight)
        
        # Combine scores
        total_score = 0
        contributions = {}
        explanations = []
        
        for rule_name, (result, weight) in results.items():
            if not result.fired:
                continue
            
            contribution = int(result.effective_score * weight)
            total_score += contribution
            contributions[rule_name] = contribution
            explanations.append((rule_name, contribution, result.reason, weight))
        
        return PositionEvaluation(
            total_score=total_score,
            contributions=contributions,
            explanations=explanations,
            board=board,
            color=color
        )
    
    def evaluate_move(self, board: chess.Board, move: chess.Move,
                      color: Optional[chess.Color] = None) -> MoveEvaluation:
        """
        Evaluate a specific move using the heuristic delta method.
        """
        if color is None:
            color = board.turn
        
        # Evaluate before the move
        eval_before = self.evaluate_position(board, color)
        
        # Evaluate after the move
        board.push(move)
        eval_after = self.evaluate_position(board, color)
        board.pop()
        
        # Compute deltas
        deltas = {}
        delta_explanations = []
        
        for rule_name in eval_before.contributions:
            before_val = eval_before.contributions.get(rule_name, 0)
            after_val = eval_after.contributions.get(rule_name, 0)
            delta = after_val - before_val
            
            if abs(delta) >= 5:  # Significance threshold
                deltas[rule_name] = delta
                delta_explanations.append((rule_name, delta))
        
        total_delta = eval_after.total_score - eval_before.total_score
        
        return MoveEvaluation(
            move=move,
            total_delta=total_delta,
            deltas=deltas,
            delta_explanations=delta_explanations,
            eval_before=eval_before,
            eval_after=eval_after
        )


@dataclass
class PositionEvaluation:
    """Complete evaluation of a position."""
    total_score: int
    contributions: dict[str, int]
    explanations: list[tuple[str, int, str, float]]
    board: chess.Board
    color: chess.Color
    
    def top_contributors(self, n: int = 5) -> list[tuple[str, int]]:
        """Return the n rules with the largest absolute contributions."""
        sorted_contribs = sorted(self.contributions.items(), 
                               key=lambda x: abs(x[1]), reverse=True)
        return sorted_contribs[:n]
    
    def summary(self) -> str:
        """Generate a summary explanation."""
        top = self.top_contributors(3)
        total = self.total_score
        
        lines = [f"Position evaluation: {total:+d}cp"]
        for name, contrib in top:
            direction = "supports" if contrib > 0 else "opposes"
            lines.append(f"  {name}: {contrib:+d}cp ({direction})")
        
        return "\n".join(lines)


@dataclass
class MoveEvaluation:
    """Complete evaluation of a move's effect."""
    move: chess.Move
    total_delta: int
    deltas: dict[str, int]
    delta_explanations: list[tuple[str, int]]
    eval_before: PositionEvaluation
    eval_after: PositionEvaluation
    
    @property
    def primary_driver(self) -> Optional[tuple[str, int]]:
        """The rule with the largest positive delta (primary reason for the move)."""
        positive = [(name, delta) for name, delta in self.deltas.items() if delta > 0]
        if not positive:
            return None
        return max(positive, key=lambda x: x[1])
    
    @property
    def primary_objection(self) -> Optional[tuple[str, int]]:
        """The rule with the largest negative delta (primary objection to the move)."""
        negative = [(name, delta) for name, delta in self.deltas.items() if delta < 0]
        if not negative:
            return None
        return min(negative, key=lambda x: x[1])
    
    def explain(self, audience: str = "intermediate") -> str:
        """Generate a move explanation for the given audience level."""
        driver = self.primary_driver
        objection = self.primary_objection
        
        move_san = self.eval_before.board.san(self.move)
        
        if driver is None and objection is None:
            return f"{move_san} maintains the current position."
        
        parts = [f"{move_san}"]
        
        if driver:
            parts.append(f"improves {driver[0].lower()} by {driver[1]:+d}cp")
        
        if objection:
            parts.append(f"though {objection[0].lower()} worsens by {objection[1]:+d}cp")
        
        return " — ".join(parts) + f". Net: {self.total_delta:+d}cp"
```

## Reasoning Collection

### The ReasoningTrace

Every evaluation produces a **reasoning trace**—a complete record of which rules fired, what they said, and how they contributed to the final score. This trace is the primary input to the [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|explanation pipeline]]:

```python
@dataclass
class ReasoningTrace:
    """
    A complete record of the reasoning process for a single evaluation.
    """
    position_fen: str
    rules_evaluated: int
    rules_fired: int
    total_score: int
    contributions: dict[str, int]       # rule_name → weighted contribution
    raw_scores: dict[str, int]          # rule_name → raw score
    reasons: dict[str, str]             # rule_name → reason string
    activations: dict[str, float]       # rule_name → activation strength
    weights: dict[str, float]           # rule_name → applied weight
    timestamp: float = 0.0
    
    def dominant_rule(self) -> tuple[str, int]:
        """The rule with the largest absolute contribution."""
        return max(self.contributions.items(), key=lambda x: abs(x[1]))
    
    def supporting_rules(self) -> list[tuple[str, int]]:
        """Rules with positive contributions."""
        return [(n, s) for n, s in self.contributions.items() if s > 0]
    
    def opposing_rules(self) -> list[tuple[str, int]]:
        """Rules with negative contributions."""
        return [(n, s) for n, s in self.contributions.items() if s < 0]
    
    def to_dict(self) -> dict:
        """Serialize the trace for logging or transmission."""
        return {
            "fen": self.position_fen,
            "total": self.total_score,
            "fired": f"{self.rules_fired}/{self.rules_evaluated}",
            "contributions": self.contributions,
            "reasons": self.reasons,
        }
```

This complete code architecture ensures that every evaluation is transparent, traceable, and explainable—from the individual rule that fired to the final combined score that drives the engine's decision.

---

*Previous: [[08-Rule-Based-Reasoning-Systems/04 - Confidence Scoring and Rule Weighting|04 - Confidence Scoring and Rule Weighting]] ←*
*Next: [[09-Explainable-AI-for-Chess/01 - Explainable AI (XAI) Overview|09 - Explainable AI (XAI) Overview]] →*
*See also: [[06-Adaptive-Depth-Control/07 - The Depth Rules Module (Code Architecture)|The Depth Rules Module]] | [[08-Rule-Based-Reasoning-Systems/01 - Rule Engine Architecture|Rule Engine Architecture]] | [[09-Explainable-AI-for-Chess/04 - Move Explanation Architecture|Move Explanation Architecture]]*
