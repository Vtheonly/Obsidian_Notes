# The Depth Rules Module (Code Architecture)

> "Good architecture makes the system easy to understand, easy to develop, and easy to maintain." — Robert C. Martin

## Architectural Overview

The Depth Rules Module is the **central nervous system** of the [[Depther]]. It encapsulates all depth extension rules, depth reduction rules, and [[Safety and Control Rules|safety constraints]] into a clean, extensible, and explainable architecture. The module is designed around three core principles:

1. **Open/Closed Principle**: New rules can be added without modifying existing code.
2. **Single Responsibility**: Each rule is a self-contained unit with its own logic and explanation.
3. **Explainability by Design**: Every depth adjustment carries a human-readable reason.

## Module Structure

```
depth_rules/
├── __init__.py
├── base.py              # DepthPolicy base class, DepthDelta data class
├── extensions/
│   ├── __init__.py
│   ├── check.py         # Check extension
│   ├── capture.py       # Capture extension
│   ├── promotion.py     # Promotion threat extension
│   ├── recapture.py     # Recapture extension
│   ├── trojan.py        # Trojan discovery extension
│   ├── sniper.py        # Sniper line extension
│   ├── forced.py        # Forced response extension
│   └── mate_threat.py   # Mate threat extension
├── reductions/
│   ├── __init__.py
│   ├── lmr.py           # Late Move Reduction
│   ├── quiet.py         # Quiet move reduction
│   ├── mindless.py      # Mindless exchange reduction
│   ├── rim_knight.py    # Rim knight reduction
│   ├── history.py       # Historical failure reduction
│   └── stable.py        # Stable quiet reduction
├── safety.py            # Safety and control rules
├── depther.py           # Main Depther orchestrator
└── registry.py          # Rule registry and discovery
```

## The DepthPolicy Base Class

Every depth rule (extension or reduction) implements the `DepthPolicy` interface:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class DepthDelta:
    """
    A depth adjustment proposed by a rule.
    Positive delta = extension, negative delta = reduction.
    """
    delta: int                        # The depth change (+1, -1, etc.)
    rule_name: str                    # Unique identifier for the rule
    reason: str                       # Human-readable explanation
    priority: int = 0                 # For ordering and conflict resolution
    metadata: Dict = field(default_factory=dict)  # Extra data for debugging

    @property
    def is_extension(self) -> bool:
        return self.delta > 0

    @property
    def is_reduction(self) -> bool:
        return self.delta < 0

    def __repr__(self) -> str:
        direction = "EXTEND" if self.is_extension else "REDUCE"
        return f"[{direction}] {self.rule_name}: {self.delta:+d} ply — {self.reason}"


@dataclass
class SearchContext:
    """
    Context passed to every depth rule for evaluation.
    Contains all the information a rule might need to make its decision.
    """
    board: 'Board'                    # Current board position
    move: 'Move'                      # The move being evaluated
    depth: int                        # Remaining search depth
    ply: int                          # Distance from root
    base_depth: int                   # Base search depth (before adjustments)
    accumulated_extensions: int       # Total extensions along this path
    move_index: int                   # Position in move ordering (0 = first)
    is_pv_node: bool                  # Is this a Principal Variation node?
    last_move: Optional['Move']       # The opponent's last move
    killer_moves: List['Move']        # Killer moves for this ply
    history_table: Dict               # History heuristic table
    in_check: bool                    # Is the side to move in check?
    game_phase: float                 # 0.0 (endgame) to 1.0 (middlegame)


class DepthPolicy(ABC):
    """
    Abstract base class for all depth adjustment rules.
    Every rule must implement get_delta(), which returns a DepthDelta.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name of this rule."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what this rule does."""
        pass

    @property
    def rule_type(self) -> str:
        """Either 'extension' or 'reduction'."""
        return "extension" if self.default_delta > 0 else "reduction"

    @property
    def default_delta(self) -> int:
        """Default depth delta for this rule (override in subclass)."""
        return 0

    @abstractmethod
    def get_delta(self, context: SearchContext) -> DepthDelta:
        """
        Evaluate the context and return a DepthDelta.
        Return delta=0 if the rule does not apply.
        """
        pass

    def is_applicable(self, context: SearchContext) -> bool:
        """
        Quick check if this rule might apply.
        Used for filtering before calling get_delta().
        Override for efficiency.
        """
        return True
```

## Extension Rules Collection

All extension rules are collected into a registry:

```python
# extensions/__init__.py

from depth_rules.base import DepthPolicy, DepthDelta, SearchContext
from depth_rules.extensions.check import CheckExtension
from depth_rules.extensions.capture import CaptureExtension
from depth_rules.extensions.promotion import PromotionThreatExtension
from depth_rules.extensions.recapture import RecaptureExtension
from depth_rules.extensions.trojan import TrojanDiscoveryExtension
from depth_rules.extensions.sniper import SniperLineExtension
from depth_rules.extensions.forced import ForcedResponseExtension
from depth_rules.extensions.mate_threat import MateThreatExtension

EXTENSIONS: List[DepthPolicy] = [
    CheckExtension(),
    CaptureExtension(),
    PromotionThreatExtension(),
    RecaptureExtension(),
    TrojanDiscoveryExtension(),
    SniperLineExtension(),
    ForcedResponseExtension(),
    MateThreatExtension(),
]
```

### Example: CheckExtension Implementation

```python
# extensions/check.py

from depth_rules.base import DepthPolicy, DepthDelta, SearchContext

class CheckExtension(DepthPolicy):
    """Extend by 1 ply when the move gives check."""

    @property
    def name(self) -> str:
        return "check_extension"

    @property
    def description(self) -> str:
        return "Extends search by 1 ply when a move delivers check, " \
               "as checks force the opponent's response and often lead " \
               "to tactical sequences."

    @property
    def default_delta(self) -> int:
        return 1

    def is_applicable(self, context: SearchContext) -> bool:
        """Only applicable if the move gives check."""
        return context.board.gives_check(context.move)

    def get_delta(self, context: SearchContext) -> DepthDelta:
        if not self.is_applicable(context):
            return DepthDelta(delta=0, rule_name=self.name, reason="")

        move_san = context.board.san(context.move)
        return DepthDelta(
            delta=1,
            rule_name=self.name,
            reason=f"Extending by 1 ply: {move_san} gives check, "
                   f"forcing the opponent to respond immediately",
            priority=10,  # High priority—checks are always important
            metadata={"check_type": _classify_check(context)}
        )


def _classify_check(context: SearchContext) -> str:
    """Classify the type of check for richer explanation."""
    board = context.board
    move = context.move
    piece = board.piece_at(move.from_square)

    # Check if it's a discovered check
    board.push(move)
    is_direct = board.is_check()
    board.pop()

    # (Simplified—real implementation would check if the moving piece
    # itself delivers the check or if a piece behind it does)
    if piece.type == 'N':
        return "knight_check"
    elif piece.type == 'B':
        return "bishop_check"
    elif piece.type == 'R':
        return "rook_check"
    elif piece.type == 'Q':
        return "queen_check"
    return "direct_check"
```

## Reduction Rules Collection

```python
# reductions/__init__.py

from depth_rules.base import DepthPolicy, DepthDelta, SearchContext
from depth_rules.reductions.lmr import LateMoveReduction
from depth_rules.reductions.quiet import QuietMoveReduction
from depth_rules.reductions.mindless import MindlessExchangeReduction
from depth_rules.reductions.rim_knight import RimKnightReduction
from depth_rules.reductions.history import HistoricalFailureReduction
from depth_rules.reductions.stable import StableQuietReduction

REDUCTIONS: List[DepthPolicy] = [
    LateMoveReduction(),
    QuietMoveReduction(),
    MindlessExchangeReduction(),
    RimKnightReduction(),
    HistoricalFailureReduction(),
    StableQuietReduction(),
]
```

### Example: LateMoveReduction Implementation

```python
# reductions/lmr.py

from depth_rules.base import DepthPolicy, DepthDelta, SearchContext

class LateMoveReduction(DepthPolicy):
    """
    Late Move Reduction: reduce depth for quiet moves that appear late
    in the move ordering. These moves are unlikely to be the best move.
    """

    @property
    def name(self) -> str:
        return "lmr"

    @property
    def description(self) -> str:
        return "Reduces search depth by 1-2 plies for quiet moves that appear " \
               "late in the move ordering. Based on the observation that " \
               "later-ordered moves are rarely the best move in the position."

    @property
    def default_delta(self) -> int:
        return -1

    # Minimum move index to trigger LMR
    LMR_MIN_INDEX = 3
    # Minimum depth for LMR to be meaningful
    LMR_MIN_DEPTH = 3
    # Move index for aggressive (2-ply) reduction
    LMR_AGGRESSIVE_INDEX = 6
    LMR_AGGRESSIVE_DEPTH = 6

    def is_applicable(self, context: SearchContext) -> bool:
        """LMR applies to late, quiet moves at sufficient depth."""
        if context.depth < self.LMR_MIN_DEPTH:
            return False
        if context.move_index < self.LMR_MIN_INDEX:
            return False
        if context.is_pv_node:
            return False  # Don't reduce in the PV
        if context.in_check:
            return False  # Don't reduce when in check

        # Must be a quiet move
        move = context.move
        board = context.board
        if board.is_capture(move):
            return False
        if board.gives_check(move):
            return False
        if move.promotion:
            return False
        if move in context.killer_moves:
            return False

        return True

    def get_delta(self, context: SearchContext) -> DepthDelta:
        if not self.is_applicable(context):
            return DepthDelta(delta=0, rule_name=self.name, reason="")

        # Determine reduction amount
        reduction = 1
        if (context.move_index >= self.LMR_AGGRESSIVE_INDEX and
            context.depth >= self.LMR_AGGRESSIVE_DEPTH):
            reduction = 2

        move_san = context.board.san(context.move)
        return DepthDelta(
            delta=-reduction,
            rule_name=self.name,
            reason=f"Reducing by {reduction} ply: {move_san} is a quiet move "
                   f"ranked {context.move_index + 1} in the move order—"
                   f"unlikely to improve the current best option",
            priority=5,
            metadata={
                "move_index": context.move_index,
                "depth": context.depth,
                "reduction_amount": reduction
            }
        )
```

## The Depther Orchestrator

The `Depther` class orchestrates all rules, applies safety constraints, and produces the final depth adjustment:

```python
# depther.py

from depth_rules.base import DepthPolicy, DepthDelta, SearchContext
from depth_rules.extensions import EXTENSIONS
from depth_rules.reductions import REDUCTIONS
from depth_rules.safety import SafetyController
from typing import List, Tuple, Optional

class Depther:
    """
    The main depth policy orchestrator.
    Combines all extension and reduction rules with safety constraints.
    Produces explainable depth adjustments.
    """

    def __init__(self, extensions: List[DepthPolicy] = None,
                 reductions: List[DepthPolicy] = None,
                 safety: SafetyController = None):
        self.extensions = extensions or EXTENSIONS
        self.reductions = reductions or REDUCTIONS
        self.safety = safety or SafetyController()

    def compute_depth_delta(self, context: SearchContext) -> DepthDelta:
        """
        Compute the total depth delta for a move.
        Combines all applicable rules, applies safety constraints,
        and produces a combined DepthDelta with full reasoning.
        """
        # Phase 1: Compute extensions
        extension_deltas = []
        for rule in self.extensions:
            if rule.is_applicable(context):
                delta = rule.get_delta(context)
                if delta.delta != 0:
                    extension_deltas.append(delta)

        # Phase 2: Compute reductions
        reduction_deltas = []
        for rule in self.reductions:
            if rule.is_applicable(context):
                delta = rule.get_delta(context)
                if delta.delta != 0:
                    reduction_deltas.append(delta)

        # Phase 3: Sum deltas
        total_extension = sum(d.delta for d in extension_deltas)
        total_reduction = sum(d.delta for d in reduction_deltas)

        # Phase 4: Apply safety constraints
        total_extension = self.safety.cap_extension(
            total_extension, context
        )
        total_reduction = self.safety.cap_reduction(
            total_reduction, context
        )

        # Check global constraints
        if self.safety.should_deny_extension(
            context.base_depth, context.accumulated_extensions + total_extension
        ):
            total_extension = 0
            extension_deltas = []

        # Phase 5: Compute final delta
        final_delta = total_extension + total_reduction

        # Phase 6: Build combined reason string
        reasons = []
        for d in extension_deltas:
            if d.reason:
                reasons.append(d.reason)
        for d in reduction_deltas:
            if d.reason:
                reasons.append(d.reason)

        # Add safety reason if applicable
        if total_extension == 0 and any(d.delta > 0 for d in extension_deltas):
            reasons.append(
                "[SAFETY] Extensions denied: accumulated extension limit reached"
            )

        combined_reason = "; ".join(reasons) if reasons else "No depth adjustment"

        return DepthDelta(
            delta=final_delta,
            rule_name="depther_combined",
            reason=combined_reason,
            priority=0,
            metadata={
                "extensions": [d.rule_name for d in extension_deltas],
                "reductions": [d.rule_name for d in reduction_deltas],
                "total_extension_before_safety": sum(d.delta for d in extension_deltas),
                "total_reduction": total_reduction,
                "safety_applied": total_extension < sum(d.delta for d in extension_deltas if d.delta > 0),
            }
        )

    def get_effective_depth(self, base_depth: int,
                            context: SearchContext) -> Tuple[int, DepthDelta]:
        """
        Compute the effective search depth for a move.
        Returns (effective_depth, delta) where delta contains full reasoning.
        """
        delta = self.compute_depth_delta(context)
        effective = max(1, base_depth + delta.delta)  # Never go below 1

        return effective, delta
```

## The Safety Controller

```python
# safety.py

from dataclasses import dataclass

@dataclass
class SafetyConfig:
    """Configuration for safety constraints."""
    max_extension_per_move: int = 2
    max_reduction_per_move: int = 3
    max_accumulated_extensions: int = 8
    max_depth_ratio: float = 2.0
    max_global_depth: int = 64
    no_extensions_at_depth: int = 1


class SafetyController:
    """
    Enforces safety constraints on depth adjustments.
    Prevents depth inflation, infinite extensions, and other pathologies.
    """

    def __init__(self, config: SafetyConfig = None):
        self.config = config or SafetyConfig()

    def cap_extension(self, extension: int, context) -> int:
        """Cap extension at the per-move maximum."""
        return min(extension, self.config.max_extension_per_move)

    def cap_reduction(self, reduction: int, context) -> int:
        """Cap reduction at the per-move maximum."""
        return max(reduction, -self.config.max_reduction_per_move)

    def should_deny_extension(self, base_depth: int,
                              accumulated_extensions: int) -> bool:
        """Check if extensions should be denied due to inflation."""
        if accumulated_extensions >= self.config.max_accumulated_extensions:
            return True
        if base_depth > 0 and accumulated_extensions / base_depth > self.config.max_depth_ratio:
            return True
        return False

    def validate_depth(self, effective_depth: int, base_depth: int,
                       current_depth: int) -> bool:
        """Validate that the effective depth is within bounds."""
        if effective_depth < 1:
            return False
        if current_depth >= self.config.max_global_depth:
            return False
        return True
```

## Reasoning Strings: The Explainability Layer

Every `DepthDelta` carries a `reason` string. These strings are designed to be **composable** and **human-readable**. When the engine explains a move, it can report the depth reasoning:

```python
def format_depth_explanation(delta: DepthDelta, move_san: str) -> str:
    """Format a depth delta into a human-readable explanation."""
    if delta.delta == 0:
        return f"  {move_san}: searched at standard depth (no adjustments)"

    direction = "extended" if delta.delta > 0 else "reduced"
    amount = abs(delta.delta)
    ply_str = "ply" if amount == 1 else "plies"

    header = f"  {move_san}: {direction} by {amount} {ply_str}"

    # Split reasons by semicolons and format as sub-items
    reasons = [r.strip() for r in delta.reason.split(";") if r.strip()]
    if not reasons:
        return header

    sub_items = "\n".join(f"    • {r}" for r in reasons)
    return f"{header}\n{sub_items}"
```

### Example Output

```
Search explanation for position after 1.e4 e5 2.Nf3:

  Nxe5: extended by 1 ply
    • Extending by 1 ply: Nxe5 captures a pawn, changing the material balance
  d4: searched at standard depth (no adjustments)
  Bd3: reduced by 1 ply
    • Reducing by 1 ply: Bd3 is a quiet move ranked 5th in the move order—unlikely to improve the current best option
  a3: reduced by 2 plies
    • Reducing by 1 ply: a3 is a quiet move ranked 8th in the move order
    • Reducing by 1 ply: placing no piece (pawn move) with no tactical significance
```

## The Rule Registry

New rules can be registered dynamically:

```python
# registry.py

from depth_rules.base import DepthPolicy, DepthDelta, SearchContext
from typing import Dict, Type, List

class RuleRegistry:
    """
    Registry for depth rules.
    Allows dynamic registration and discovery of rules.
    """

    _extensions: Dict[str, Type[DepthPolicy]] = {}
    _reductions: Dict[str, Type[DepthPolicy]] = {}

    @classmethod
    def register_extension(cls, name: str):
        """Decorator to register an extension rule."""
        def decorator(rule_class: Type[DepthPolicy]):
            cls._extensions[name] = rule_class
            return rule_class
        return decorator

    @classmethod
    def register_reduction(cls, name: str):
        """Decorator to register a reduction rule."""
        def decorator(rule_class: Type[DepthPolicy]):
            cls._reductions[name] = rule_class
            return rule_class
        return decorator

    @classmethod
    def get_all_extensions(cls) -> List[DepthPolicy]:
        """Instantiate all registered extension rules."""
        return [rule_class() for rule_class in cls._extensions.values()]

    @classmethod
    def get_all_reductions(cls) -> List[DepthPolicy]:
        """Instantiate all registered reduction rules."""
        return [rule_class() for rule_class in cls._reductions.values()]

    @classmethod
    def get_rule_by_name(cls, name: str) -> Optional[DepthPolicy]:
        """Look up a rule by name."""
        if name in cls._extensions:
            return cls._extensions[name]()
        if name in cls._reductions:
            return cls._reductions[name]()
        return None
```

### Usage

```python
@RuleRegistry.register_extension("double_check")
class DoubleCheckExtension(DepthPolicy):
    """Extend by 2 plies for double checks (only king moves are legal)."""

    @property
    def name(self) -> str:
        return "double_check"

    @property
    def description(self) -> str:
        return "Extends by 2 plies when a double check occurs, " \
               "since only king moves are legal and the position is highly forced."

    @property
    def default_delta(self) -> int:
        return 2

    def get_delta(self, context: SearchContext) -> DepthDelta:
        # Implementation...
        pass
```

## Integration with the Search

The Depther integrates with the main search loop:

```python
def negamax(board: Board, depth: int, alpha: int, beta: int,
            depther: Depther, path: SearchPath, ply: int) -> int:
    """
    Negamax search with the Depther integrated.
    """
    if depth <= 0:
        return quiescence(board, alpha, beta)

    moves = board.legal_moves()
    move_list = list(moves)
    move_list = sort_moves(board, move_list)  # Heuristic sort

    for i, move in enumerate(move_list):
        # Build context for the Depther
        context = SearchContext(
            board=board,
            move=move,
            depth=depth,
            ply=ply,
            base_depth=depth,  # Simplified
            accumulated_extensions=path.total_extensions,
            move_index=i,
            is_pv_node=(alpha + 1 >= beta),  # Approximation
            last_move=None,  # Track separately
            killer_moves=get_killers(ply),
            history_table=get_history(),
            in_check=board.is_check(),
            game_phase=compute_phase(board),
        )

        # Get depth adjustment from the Depther
        effective_depth, delta = depther.get_effective_depth(depth, context)

        # Search
        board.push(move)
        score = -negamax(board, effective_depth - 1, -beta, -alpha,
                         depther, path, ply + 1)
        board.pop()

        # Re-search if reduced and surprisingly good
        if delta.is_reduction and score > alpha:
            full_depth = depth - 1
            board.push(move)
            score = -negamax(board, full_depth, -beta, -alpha,
                             depther, path, ply + 1)
            board.pop()

        # Alpha-beta update
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha
```

## Summary

The Depth Rules Module is the architectural backbone of the [[Depther]]. It provides:

1. A **clean interface** (`DepthPolicy.get_delta()`) that every rule implements.
2. **Separate collections** for extensions and reductions.
3. A **Depther orchestrator** that combines rules and applies safety constraints.
4. **Reasoning strings** that make every depth adjustment explainable.
5. A **rule registry** for dynamic registration and discovery.
6. **Safety guarantees** that prevent depth inflation and ensure termination.

This architecture is **extensible** (add new rules without changing existing code), **testable** (each rule can be unit-tested independently), and **explainable** (every adjustment carries a human-readable reason). It embodies the project's core philosophy: the engine should not just find the best move—it should explain *how* it found it.

---

**See also:** [[The Depther Philosophy]], [[Depth Extension Rules]], [[Depth Reduction Rules]], [[Safety and Control Rules]], [[Quiescence Termination Rules]], [[Alpha-Beta Search]], [[Move Ordering]], [[History Heuristic]], [[Killer Moves]]
