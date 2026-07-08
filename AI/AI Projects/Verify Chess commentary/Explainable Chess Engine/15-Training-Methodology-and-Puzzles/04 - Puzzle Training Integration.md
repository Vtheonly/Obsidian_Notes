# Puzzle Training Integration

> **Chapter 15.04** | [[03 - The 100 Position Test|Prev: 100 Position Test]] | [[05 - Android Puzzle App Architecture|Next: Android App]]
> **Related**: [[04 - The Puzzle Database System|Puzzle Database]], [[01 - Rating Climb Roadmaps|Rating Climb]], [[05 - Android Puzzle App Architecture|Android App]]

---

## Overview

The Puzzle Training Integration module connects the [[04 - The Puzzle Database System|Lichess Puzzle Database]] with the [[Explainable Chess Engine]]'s explanation system, creating a complete learning loop: the player attempts a puzzle, the engine validates the move, and then **explains why the correct move works** using rule-based reasoning. This transforms puzzle training from rote pattern memorization into deep strategic understanding.

The module also implements **spaced repetition** — puzzles the player struggles with are presented more frequently, while mastered puzzles fade into the background. Combined with theme-based and rating-based filtering, the system creates a personalized training curriculum that adapts to the player's [[01 - Rating Climb Roadmaps|skill level]].

---

## The Puzzle Flow

### Complete Puzzle Lifecycle

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. Present   │────│  2. Player   │────│  3. Validate │────│  4. Explain  │
│  Position     │     │  Makes Move  │     │  Move        │     │  Solution    │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                    │                     │                     │
       ▼                    ▼                     ▼                     ▼
  Show FEN after       Touch/click           Compare with         Generate
  opponent's first     interface            solution move         rule-based
  move (auto-applied)                                            explanation
                                                                           │
       ┌──────────────────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  5. Update    │────│  6. Schedule │
│  Spaced Rep   │     │  Next Review │
└──────────────┘     └──────────────┘
       │                    │
       ▼                    ▼
  Adjust difficulty     Determine
  based on result       next review
                       interval
```

### Step-by-Step Implementation

```python
# puzzle_training.py
import chess
from typing import Optional, List, Dict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import sqlite3
import math

from explainable_engine import ExplainableEngine
from puzzle_database import PuzzleDatabase


@dataclass
class PuzzleState:
    """Tracks the player's progress on a specific puzzle."""
    puzzle_id: str
    attempts: int = 0
    correct: int = 0
    last_attempt: Optional[datetime] = None
    next_review: Optional[datetime] = None
    ease_factor: float = 2.5       # SM-2 spaced repetition factor
    interval_days: float = 0.0     # Days until next review
    player_rating: int = 1200      # Estimated puzzle rating for this player

    @property
    def accuracy(self) -> float:
        return self.correct / max(self.attempts, 1)

    @property
    def is_mastered(self) -> bool:
        return self.accuracy >= 0.8 and self.attempts >= 3


@dataclass
class PuzzleSession:
    """A single puzzle training session."""
    puzzle: Dict
    board: chess.Board = None
    current_move_index: int = 0
    player_moves: List[str] = field(default_factory=list)
    is_complete: bool = False
    start_time: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.board is None:
            # Set up position after opponent's first move
            self.board = chess.Board(self.puzzle['fen'])
            opponent_move = chess.Move.from_uci(self.puzzle['opponent_move'])
            self.board.push(opponent_move)


class PuzzleTrainer:
    """
    The puzzle training system that integrates with the Explainable Chess Engine.
    """

    def __init__(self, db_path: str, engine: ExplainableEngine, player_id: str):
        self.db = PuzzleDatabase(db_path)
        self.engine = engine
        self.player_id = player_id
        self.state_db = self._init_state_db()

    def _init_state_db(self) -> sqlite3.Connection:
        """Initialize the spaced repetition state database."""
        conn = sqlite3.connect(f"puzzle_state_{self.player_id}.db")
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS puzzle_states (
                puzzle_id TEXT PRIMARY KEY,
                attempts INTEGER DEFAULT 0,
                correct INTEGER DEFAULT 0,
                last_attempt TEXT,
                next_review TEXT,
                ease_factor REAL DEFAULT 2.5,
                interval_days REAL DEFAULT 0.0,
                player_rating INTEGER DEFAULT 1200
            );
        """)
        conn.commit()
        return conn

    # ─── Step 1: Present Position ───────────────────────────────────

    def present_puzzle(self, theme: str = None, rating_range: tuple = None) -> PuzzleSession:
        """
        Select and present a puzzle appropriate for the player.
        Uses spaced repetition to prioritize due puzzles.
        """
        # First, check for due reviews
        due_puzzles = self._get_due_puzzles()
        if due_puzzles:
            puzzle = self._select_from_due(due_puzzles)
        else:
            # Select a new puzzle
            player_rating = self._get_player_rating()
            if rating_range is None:
                rating_range = (player_rating - 200, player_rating + 100)

            if theme:
                puzzle = self.db.query_by_theme(theme, limit=1,
                    min_rating=rating_range[0], max_rating=rating_range[1])
            else:
                puzzle = self.db.query_by_rating(
                    min_rating=rating_range[0],
                    max_rating=rating_range[1],
                    limit=1
                )

        return PuzzleSession(puzzle=puzzle)

    # ─── Step 2: Player Makes Move ──────────────────────────────────

    def submit_move(self, session: PuzzleSession, uci_move: str) -> MoveResult:
        """
        Validate the player's move against the puzzle solution.
        """
        solution_moves = session.puzzle['moves'].split()
        expected_move = solution_moves[session.current_move_index]

        is_correct = (uci_move == expected_move)

        if is_correct:
            session.player_moves.append(uci_move)
            session.current_move_index += 1

            # Apply the player's move to the board
            move = chess.Move.from_uci(uci_move)
            session.board.push(move)

            # If there are more moves, apply the opponent's response
            if session.current_move_index < len(solution_moves):
                opponent_move_uci = solution_moves[session.current_move_index]
                opponent_move = chess.Move.from_uci(opponent_move_uci)
                session.board.push(opponent_move)
                session.current_move_index += 1

                return MoveResult(
                    is_correct=True,
                    is_complete=False,
                    message="Correct! The opponent replies. Your turn again.",
                    explanation=None  # Don't explain until puzzle is complete
                )
            else:
                # Puzzle is complete!
                session.is_complete = True
                return MoveResult(
                    is_correct=True,
                    is_complete=True,
                    message="Puzzle solved! Excellent work.",
                    explanation=None  # Will be generated by explain_solution()
                )
        else:
            session.player_moves.append(uci_move)
            return MoveResult(
                is_correct=False,
                is_complete=False,
                message=f"Incorrect. The correct move was {expected_move}.",
                hint=self._generate_hint(session.board, expected_move)
            )

    # ─── Step 4: Explain Solution ───────────────────────────────────

    def explain_solution(self, session: PuzzleSession) -> PuzzleExplanation:
        """
        Generate a comprehensive explanation of the puzzle solution
        using the Explainable Chess Engine's rule-based system.
        """
        # Reset board to the puzzle position (after opponent's first move)
        board = chess.Board(session.puzzle['fen'])
        opponent_move = chess.Move.from_uci(session.puzzle['opponent_move'])
        board.push(opponent_move)

        solution_moves = session.puzzle['moves'].split()
        themes = session.puzzle['themes'].split()

        move_explanations = []

        for i, uci_move in enumerate(solution_moves):
            if i == 0:
                # Opponent's move — explain what weakness it created
                explanation = self._explain_opponent_move(board, uci_move, themes)
                move_explanations.append(explanation)
            else:
                # Player's (or opponent's) move — explain the logic
                is_player_move = (i % 2 == 1)

                if is_player_move:
                    explanation = self.engine.evaluate_and_explain(board)
                    move_explanations.append({
                        'move_uci': uci_move,
                        'move_san': board.san(chess.Move.from_uci(uci_move)),
                        'role': 'player',
                        'explanation': explanation['explanation'],
                        'active_rules': explanation['active_rules'],
                        'evaluation': explanation['evaluation'],
                        'theme_relevance': self._match_themes(explanation, themes)
                    })
                else:
                    explanation = self._explain_opponent_response(board, uci_move)
                    move_explanations.append(explanation)

            # Apply move
            move = chess.Move.from_uci(uci_move)
            board.push(move)

        # Generate overall puzzle explanation
        overall_explanation = self._generate_overall_explanation(
            move_explanations, themes, session.puzzle
        )

        return PuzzleExplanation(
            puzzle_id=session.puzzle['puzzle_id'],
            themes=themes,
            move_explanations=move_explanations,
            overall_explanation=overall_explanation
        )

    def _explain_opponent_move(self, board: chess.Board, uci_move: str,
                                themes: List[str]) -> Dict:
        """Explain what weakness the opponent's move created."""
        move = chess.Move.from_uci(uci_move)
        move_san = board.san(move)

        # Evaluate before and after
        eval_before = self.engine.evaluate(board)
        board.push(move)
        eval_after = self.engine.evaluate(board)
        board.pop()

        # What changed?
        features_before = self.engine.extract_features(board)
        features_after = self.engine.extract_features(board.after(move))

        changed_features = []
        for i in range(len(features_before)):
            if abs(features_after[i] - features_before[i]) > 0.5:
                changed_features.append({
                    'name': FEATURE_NAMES[i],
                    'before': features_before[i],
                    'after': features_after[i],
                    'contribution': TRAINED_WEIGHTS[i] * (features_after[i] - features_before[i])
                })

        changed_features.sort(key=lambda x: abs(x['contribution']), reverse=True)

        # Generate explanation
        if 'sacrifice' in themes:
            explanation = (
                f"The opponent plays {move_san}, sacrificing material! "
                f"This creates tactical threats that you must address. "
                f"The sacrifice aims to: {self._describe_sacrifice_motives(changed_features)}"
            )
        elif 'fork' in themes:
            explanation = (
                f"The opponent plays {move_san}, creating a position where "
                f"you can deliver a fork. Look for a piece that can attack "
                f"two targets simultaneously."
            )
        else:
            explanation = (
                f"The opponent plays {move_san}. "
                f"This move {'creates' if eval_after < eval_before else 'does not create'} "
                f"a weakness that you can exploit."
            )

        return {
            'move_uci': uci_move,
            'move_san': move_san,
            'role': 'opponent',
            'explanation': explanation,
            'changed_features': changed_features[:5],
            'eval_change': eval_after - eval_before
        }

    def _match_themes(self, explanation: Dict, puzzle_themes: List[str]) -> Dict[str, bool]:
        """
        Check if the engine's explanation matches the puzzle's designated themes.
        This is the key quality metric for the explainable engine.
        """
        explanation_text = explanation['explanation'].lower()
        active_rules = [r['name'] for r in explanation.get('active_rules', [])]

        theme_matches = {}
        for theme in puzzle_themes:
            theme_keywords = THEME_KEYWORD_MAP.get(theme, [theme.lower()])
            theme_rules = THEME_RULE_MAP.get(theme, [])

            keyword_match = any(kw in explanation_text for kw in theme_keywords)
            rule_match = any(rule in active_rules for rule in theme_rules)

            theme_matches[theme] = keyword_match or rule_match

        return theme_matches

    # ─── Step 5: Update Spaced Repetition ───────────────────────────

    def update_spaced_repetition(self, session: PuzzleSession, success: bool):
        """
        Update the spaced repetition state for this puzzle.
        Uses the SM-2 algorithm (SuperMemo 2).
        """
        puzzle_id = session.puzzle['puzzle_id']

        # Load current state
        state = self._load_state(puzzle_id)
        state.attempts += 1
        if success:
            state.correct += 1

        # SM-2 quality rating (0-5)
        if success and session.player_moves == session.puzzle['moves'].split()[1::2]:
            quality = 5  # Perfect — solved on first try
        elif success:
            quality = 3  # Correct but with errors
        else:
            quality = 1  # Incorrect

        # SM-2 algorithm
        if quality >= 3:
            # Correct response — increase interval
            if state.interval_days == 0:
                state.interval_days = 1
            elif state.interval_days == 1:
                state.interval_days = 6
            else:
                state.interval_days *= state.ease_factor
        else:
            # Incorrect response — reset interval
            state.interval_days = 0  # Will be reviewed again soon

        # Update ease factor
        state.ease_factor = max(1.3,
            state.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        )

        # Calculate next review date
        state.last_attempt = datetime.now()
        state.next_review = state.last_attempt + timedelta(days=state.interval_days)

        # Update player's estimated puzzle rating
        puzzle_rating = session.puzzle['rating']
        if success:
            state.player_rating += 10
        else:
            state.player_rating -= 15
        state.player_rating = max(400, min(3000, state.player_rating))

        # Save state
        self._save_state(state)

    def _load_state(self, puzzle_id: str) -> PuzzleState:
        """Load puzzle state from the database."""
        cursor = self.state_db.cursor()
        cursor.execute("SELECT * FROM puzzle_states WHERE puzzle_id = ?", (puzzle_id,))
        row = cursor.fetchone()

        if row:
            return PuzzleState(
                puzzle_id=row[0],
                attempts=row[1],
                correct=row[2],
                last_attempt=datetime.fromisoformat(row[3]) if row[3] else None,
                next_review=datetime.fromisoformat(row[4]) if row[4] else None,
                ease_factor=row[5],
                interval_days=row[6],
                player_rating=row[7]
            )
        else:
            return PuzzleState(puzzle_id=puzzle_id)

    def _save_state(self, state: PuzzleState):
        """Save puzzle state to the database."""
        self.state_db.execute("""
            INSERT OR REPLACE INTO puzzle_states
            (puzzle_id, attempts, correct, last_attempt, next_review,
             ease_factor, interval_days, player_rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            state.puzzle_id,
            state.attempts,
            state.correct,
            state.last_attempt.isoformat() if state.last_attempt else None,
            state.next_review.isoformat() if state.next_review else None,
            state.ease_factor,
            state.interval_days,
            state.player_rating
        ))
        self.state_db.commit()

    # ─── Filtering Puzzles ──────────────────────────────────────────

    def get_puzzles_by_theme(self, theme: str, limit: int = 20) -> List[Dict]:
        """Get puzzles filtered by tactical theme."""
        return self.db.query_by_theme(theme, limit=limit)

    def get_puzzles_by_rating(self, min_rating: int, max_rating: int,
                               limit: int = 20) -> List[Dict]:
        """Get puzzles filtered by difficulty rating."""
        return self.db.query_by_rating(min_rating, max_rating, limit=limit)

    def get_puzzles_by_opening(self, opening: str, limit: int = 20) -> List[Dict]:
        """Get puzzles from a specific opening (e.g., 'Slav_Defense')."""
        return self.db.query_by_opening(opening, limit=limit)

    def get_adaptive_puzzle_set(self, count: int = 10) -> List[Dict]:
        """
        Get an adaptive set of puzzles based on the player's performance.
        Prioritizes themes the player struggles with.
        """
        # Find the player's weakest themes
        weak_themes = self._find_weak_themes()

        puzzles = []
        for theme, accuracy in weak_themes:
            theme_puzzles = self.db.query_by_theme(theme, limit=3)
            puzzles.extend(theme_puzzles)
            if len(puzzles) >= count:
                break

        # Fill remaining slots with rating-appropriate puzzles
        if len(puzzles) < count:
            player_rating = self._get_player_rating()
            more = self.db.query_by_rating(
                player_rating - 100, player_rating + 100,
                limit=count - len(puzzles)
            )
            puzzles.extend(more)

        return puzzles[:count]

    def _find_weak_themes(self) -> List[tuple]:
        """Find the themes where the player has the lowest accuracy."""
        cursor = self.state_db.cursor()
        cursor.execute("""
            SELECT p.primary_theme,
                   SUM(ps.correct) as total_correct,
                   SUM(ps.attempts) as total_attempts
            FROM puzzle_states ps
            JOIN puzzles p ON ps.puzzle_id = p.puzzle_id
            WHERE ps.attempts > 0
            GROUP BY p.primary_theme
            ORDER BY (SUM(ps.correct) * 1.0 / SUM(ps.attempts)) ASC
        """)

        results = []
        for theme, correct, attempts in cursor.fetchall():
            accuracy = correct / max(attempts, 1)
            results.append((theme, accuracy))

        return results


# ─── Theme-Keyword Mapping for Explanation Matching ────────────────

THEME_KEYWORD_MAP = {
    'fork': ['fork', 'attacks two', 'simultaneous attack', 'two pieces'],
    'pin': ['pin', 'pinned', 'cannot move without exposing'],
    'skewer': ['skewer', 'forced to move', 'exposes behind'],
    'discoveredAttack': ['discovered attack', 'reveals attack', 'unmasked attack'],
    'doubleCheck': ['double check', 'two pieces give check'],
    'deflection': ['deflect', 'lure away', 'removing defender', 'diversion'],
    'decoy': ['decoy', 'lure to', 'entice'],
    'sacrifice': ['sacrifice', 'give up material', 'material for'],
    'backRankMate': ['back rank', 'trapped by own pawns', 'mated on back rank'],
    'smotheredMate': ['smothered', 'knight mate', 'surrounded by own pieces'],
    'attraction': ['attract', 'force to square', 'lure king'],
    'interference': ['interfere', 'cut off', 'between defenders'],
    'clearance': ['clear', 'vacate', 'open line'],
    'xRayAttack': ['x-ray', 'see through', 'through the piece'],
    'overloading': ['overloaded', 'too many tasks', 'defending both'],
    'trappedPiece': ['trapped', 'no escape', 'nowhere to go'],
    'mateIn1': ['checkmate', 'mate in one'],
    'mateIn2': ['mate in two', 'force checkmate'],
    'endgame': ['endgame', 'king and pawn', 'opposition'],
    'advantage': ['advantage', 'convert', 'winning position'],
    'defensiveMove': ['defensive', 'only move', 'saving move', 'best defense'],
    'quietMove': ['quiet', 'non-forcing', 'improving'],
    'zugzwang': ['zugzwang', 'any move loses', 'forced to worsen'],
}

THEME_RULE_MAP = {
    'fork': ['fork_possible'],
    'pin': ['pins_exist'],
    'sacrifice': ['material_sacrifice'],
    'backRankMate': ['back_rank_weakness'],
    'trappedPiece': ['trapped_piece'],
    'overloading': ['overloaded_piece'],
    'defensiveMove': ['in_check', 'hanging_piece'],
}
```

---

## Example: Complete Puzzle Session

```
┌──────────────────────────────────────────────────────────────────┐
│ PUZZLE #A7x3f | Rating: 1350 | Themes: fork, middlegame         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Position after opponent's move (Rhe8):                           │
│                                                                  │
│   a b c d e f g h                                               │
│ 8 . . .   . . .  8                                           │
│ 7    .      7                                           │
│ 6 . .  . . . . .  6                                           │
│ 5 . . .  .  . .  5                                           │
│ 4 . . .  . . . .  4                                           │
│ 3 . .  . . . . .  3                                           │
│ 2   . .      2                                           │
│ 1  .    . .   1                                           │
│   a b c d e f g h                                               │
│                                                                  │
│ Your turn. Find the best move for White.                         │
│                                                                  │
│ ─────────────────────────────────────────────                    │
│                                                                  │
│ Your move: Nc3e4                                                 │
│                                                                  │
│  CORRECT! The knight on e4 forks the rook on e8 and the        │
│   bishop on b5/d6. The opponent cannot save both pieces.        │
│                                                                  │
│ ─── EXPLANATION ─────────────────────────────                    │
│                                                                  │
│ WHY THIS WORKS:                                                  │
│                                                                  │
│ 1. OPPONENT'S WEAKNESS: After ...Rhe8, Black's rook and bishop   │
│    are on the same diagonal/rank. The rook on e8 and the bishop  │
│    on b5 are both vulnerable to a knight fork from e4.           │
│                                                                  │
│ 2. THE FORK: Ne4 attacks both the rook (e8) and the bishop       │
│    (via the knight's L-shaped movement to c5/d6/f6/g3).          │
│    More precisely, the knight on e4 controls:                     │
│    • d6 (attacking the bishop)                                   │
│    • f6 (a central square)                                       │
│    • c5 and g3 (attacking from different angles)                  │
│    • d2, f2 (defensive squares)                                  │
│                                                                  │
│ 3. ACTIVE RULES:                                                 │
│     fork_possible = 1.0 — Knight can attack two targets         │
│     knight_outpost_w = 0.8 — e4 is close to an outpost         │
│     LPDO_b = 1.0 — Black has a loosely defended piece           │
│                                                                  │
│ 4. THEME MATCH: This puzzle is tagged 'fork' — the engine's      │
│    explanation correctly identifies the fork as the key tactical  │
│    motif.                                                        │
│                                                                  │
│ ─── SPACED REPETITION UPDATE ──────────────                      │
│ • Quality: 5/5 (solved on first attempt)                         │
│ • Next review: 1 day from now                                    │
│ • Ease factor: 2.5 → 2.6                                        │
│ • Puzzle rating estimate: 1340 → 1350 (+10)                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## Spaced Repetition Schedule

The SM-2 algorithm produces the following review schedule for a successfully solved puzzle:

| Attempt | Result | Interval | Next Review |
|---------|--------|----------|-------------|
| 1st | Correct (5) | 1 day | Tomorrow |
| 2nd | Correct (5) | 6 days | Next week |
| 3rd | Correct (5) | 15 days | 2 weeks |
| 4th | Correct (5) | 37 days | ~5 weeks |
| 5th | Correct (5) | 93 days | ~3 months |
| 6th | Correct (5) | 232 days | ~8 months |

If the player fails at any point, the interval resets to 0 (review again soon), and the ease factor decreases, making future intervals shorter.

---

## Integration with the 100 Position Test

The Puzzle Training system connects directly to the [[03 - The 100 Position Test|100 Position Test]] results:

```python
def generate_training_plan(test_results: TestReport, trainer: PuzzleTrainer) -> TrainingPlan:
    """
    Generate a personalized puzzle training plan based on test results.
    """
    plan = TrainingPlan()

    # Focus on the 3 weakest skills
    for skill, accuracy in test_results.weakest_skills:
        # Map skill to puzzle theme
        skill_theme_map = {
            'pawn_structure': ['advantage', 'endgame'],
            'piece_activity': ['quietMove', 'advantage'],
            'king_safety': ['backRankMate', 'sacrifice', 'defensiveMove'],
            'calculation': ['fork', 'pin', 'skewer', 'mateIn2'],
            'prophylaxis': ['defensiveMove', 'quietMove'],
            'endgame_awareness': ['endgame', 'advantage'],
        }

        themes = skill_theme_map.get(skill, [skill])
        for theme in themes:
            puzzles = trainer.get_puzzles_by_theme(theme, limit=5)
            plan.add_daily_puzzles(theme, puzzles, target_accuracy=0.7)

    return plan
```

---

## Summary

The Puzzle Training Integration module provides:

1. **Complete puzzle flow**: Present → Move → Validate → Explain → Update spaced repetition
2. **Rule-based explanations**: Every puzzle solution is explained using the engine's rule system, connecting the tactical theme to positional features
3. **Theme matching verification**: The engine's explanation is checked against the puzzle's designated themes to measure explanation quality
4. **SM-2 spaced repetition**: Puzzles are reviewed at optimal intervals to maximize long-term retention
5. **Adaptive filtering**: Puzzles are selected by theme, rating, opening, and the player's weakest skills
6. **Integration with diagnostics**: The [[03 - The 100 Position Test|100 Position Test]] results directly feed into the training plan

This module bridges the gap between the [[04 - The Puzzle Database System|puzzle database]] and the [[05 - Android Puzzle App Architecture|mobile app]], creating a complete learning ecosystem.
