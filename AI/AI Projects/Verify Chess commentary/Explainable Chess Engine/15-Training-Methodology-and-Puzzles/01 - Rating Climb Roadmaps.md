# Rating Climb Roadmaps

> **Chapter 15.01** | [[02 - Defense and Swindling|Next: Defense & Swindling]] | [[03 - Strategic Themes and Rule Activation|Prev: Rule Activation]]
> **Related**: [[03 - The 100 Position Test|100 Position Test]], [[04 - Puzzle Training Integration|Puzzle Training]], [[01 - The Slav Defense Philosophy|Slav Defense]]

---

## Overview

One of the most powerful features of the [[Explainable Chess Engine]] is its ability to **adapt explanations to the player's skill level**. A 900 ELO player needs fundamentally different guidance than a 1900 ELO player. This note maps the specific skills needed at each rating level and shows how the engine's explanation system adjusts its depth, vocabulary, and focus accordingly.

The rating climb is not a smooth curve — it's a staircase where each "step" requires mastering a qualitatively different skill. Players often plateau for months because they haven't identified the missing skill at their level. The engine must serve as a diagnostic tool that identifies these gaps.

---

## Level 1: 800 ELO — Board Vision

### The Core Problem: "Hope Chess"

At 800 ELO, players suffer from **"hope chess"** — they make a move and *hope* it works, without verifying that it's safe. The defining characteristic:

> "I move my queen to f7. Oh wait, it can be captured. Hmm, let me try something else."

This is not calculation failure — it's **perception failure**. The player literally does not see that the f7 square is attacked.

### Skills Required

| Skill | Description | How to Train |
|-------|-------------|-------------|
| **Piece Vision** | See all pieces on the board at once | Board scanning exercises |
| **Capture Awareness** | Before every move, check: can my opponent capture it? | "Is it safe?" checklist |
| **Check Awareness** | Before every move, check: can my opponent check me? | "Is it safe?" checklist |
| **Hanging Piece Detection** | Identify unguarded pieces immediately | LPDO (Least Perimeter, Defended Once) scanning |
| **One-Move Threats** | See immediate threats: forks, pins, back rank | Tactical puzzles rated 600-900 |

### The "Is It Safe?" Checklist

The engine should present this checklist before every move at the 800 ELO level:

```python
class BeginnerExplanation(ExplanationLevel):
    """
    Explanation system for 800 ELO players.
    Focus: board vision, safety checks, and eliminating blunders.
    """

    def generate_pre_move_checklist(self, position: Position, move: Move) -> List[str]:
        """Generate a safety checklist before the player makes a move."""
        checklist = []

        # 1. Is the destination square attacked by the opponent?
        target_sq = move.target_square()
        if position.is_square_attacked(target_sq, opponent(position.side_to_move)):
            # Is the piece defended?
            if not position.is_piece_defended_after_move(move):
                checklist.append(
                    f" DANGER: The square {target_sq} is attacked by your "
                    f"opponent! Your {move.piece_name()} would be captured "
                    f"for free. This is a HANGING PIECE — do NOT play this move "
                    f"unless you have a very good reason."
                )

        # 2. Are you leaving a piece undefended?
        source_sq = move.source_square()
        if position.is_piece_on_square(source_sq, position.side_to_move):
            if not position.is_piece_defended_after_move(move):
                piece = position.piece_on_square(source_sq)
                if piece.value >= 300:  # Knight or higher
                    checklist.append(
                        f" WARNING: Moving your {piece.name()} from {source_sq} "
                        f"would leave it undefended. Your opponent could capture it."
                    )

        # 3. Does this move allow a check?
        opponent_checks = position.checks_available_after(move)
        if opponent_checks:
            checklist.append(
                f" CHECK ALERT: After this move, your opponent can check you "
                f"with {opponent_checks[0]}. Are you prepared for this?"
            )

        # 4. Are there any hanging opponent pieces you're missing?
        hanging_pieces = position.find_hanging_pieces(opponent(position.side_to_move))
        if hanging_pieces:
            for piece, square in hanging_pieces:
                if not move.captures_square(square):
                    checklist.append(
                        f" MISSED CAPTURE: Your opponent's {piece.name()} on "
                        f"{square} is hanging (undefended). Consider capturing it!"
                    )

        return checklist

    def generate_move_explanation(self, position: Position, move: Move) -> str:
        """Generate a simple explanation for 800 ELO players."""
        if move.is_capture:
            return (
                f" This move captures your opponent's {move.captured_piece_name()}. "
                f"Capturing free material is almost always a good idea!"
            )
        elif move.is_check:
            return (
                f" This move gives check! Forcing your opponent to respond "
                f"to the check limits their options."
            )
        elif position.is_developing_move(move):
            return (
                f" This move develops your {move.piece_name()} to an active square. "
                f"In the opening, developing pieces quickly is very important."
            )
        elif move.is_castling:
            return (
                f" Castling is an excellent move! It keeps your king safe and "
                f"brings your rook into the game. Try to castle early."
            )
        else:
            return (
                f"This move improves your position. Consider: is your king safe? "
                f"Are all your pieces developed? Is anything hanging?"
            )
```

### Engine Output Example (800 ELO)

```
┌─────────────────────────────────────────────────────────────┐
│ YOUR MOVE: Qf7                                               │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  DANGER! Your queen on f7 can be captured by the           │
│    knight on e5 (Nxf7). This is a FREE QUEEN for your       │
│    opponent!                                                  │
│                                                               │
│  DID YOU NOTICE: The knight on e5 is actually undefended.  │
│    You could capture it with your pawn (dxe5) instead!       │
│                                                               │
│ TIP: Before every move, ask yourself:                        │
│    1. Can my opponent capture the piece I'm moving?           │
│    2. Am I leaving any of my pieces undefended?              │
│    3. Are any of my opponent's pieces hanging?               │
│                                                               │
│ RECOMMENDATION: Play dxe5 instead — it captures a free      │
│    knight AND avoids hanging your queen.                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Level 2: 1000 ELO — Threat Perception

### The Core Problem: Ignoring the Opponent's Intent

At 1000 ELO, players can see immediate captures and checks, but they don't consider **what the opponent's last move threatened**:

> "My opponent played Bb5. I'll continue with my plan of ...e5. Oh wait, my knight on c6 is pinned!"

### Skills Required

| Skill | Description | How to Train |
|-------|-------------|-------------|
| **Opponent's Intent** | After every opponent move, ask: "What does this threaten?" | [[04 - The Puzzle Database System|Puzzle]] training focused on pins/forks |
| **Threat Verification** | Before every move, check: "Does my move address the threat?" | "What's the threat?" exercises |
| **Basic Pattern Scanning** | Recognize common tactical patterns | Pattern recognition drills |
| **Piece Coordination** | Understand how pieces work together | Study basic checkmates |
| **Opening Principles** | Develop, control center, castle early | Opening principle exercises |

### The "What's the Threat?" Framework

```python
class IntermediateExplanation(ExplanationLevel):
    """
    Explanation system for 1000 ELO players.
    Focus: threat perception, opponent's intent, pattern recognition.
    """

    def analyze_opponent_move(self, position: Position, last_move: Move) -> str:
        """Analyze what the opponent's last move threatened."""

        threats = position.find_threats_after(last_move)

        if not threats:
            return (
                "Your opponent's last move doesn't create an immediate threat. "
                "This is a good time to focus on your own plan: develop your "
                "remaining pieces, improve your worst-placed piece, or prepare "
                "a pawn break."
            )

        explanations = []
        for threat in threats[:3]:  # Limit to top 3 threats
            if threat.threat_type == 'fork':
                explanations.append(
                    f" THREAT: Your opponent's {threat.piece_name()} on "
                    f"{threat.square} is attacking BOTH your {threat.target1} "
                    f"and {threat.target2}. This is a FORK! You need to deal "
                    f"with both threats simultaneously."
                )
            elif threat.threat_type == 'pin':
                explanations.append(
                    f" THREAT: Your opponent's {threat.piece_name()} on "
                    f"{threat.square} is PINNING your {threat.pinned_piece} "
                    f"against your {threat.backing_piece}. The pinned piece "
                    f"cannot move without exposing a more valuable piece."
                )
            elif threat.threat_type == 'capture':
                explanations.append(
                    f" THREAT: Your opponent's {threat.piece_name()} on "
                    f"{threat.square} threatens to capture your "
                    f"{threat.target_piece} on {threat.target_square}. You "
                    f"should defend it, move it, or counterattack."
                )
            elif threat.threat_type == 'checkmate':
                explanations.append(
                    f" CHECKMATE THREAT: Your opponent is threatening "
                    f"checkmate with {threat.move}! This is an EMERGENCY — "
                    f"you must prevent it immediately."
                )

        return '\n\n'.join(explanations)
```

### Engine Output Example (1000 ELO)

```
┌──────────────────────────────────────────────────────────────┐
│ OPPONENT'S MOVE: Bb5                                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  THREAT: The bishop on b5 is PINNING your knight on c6    │
│    against your king on e8. If the knight moves, the bishop  │
│    would capture... wait, that's a check. The knight CANNOT  │
│    move without exposing your king to capture.               │
│                                                              │
│ WHAT YOU SHOULD DO:                                          │
│    Option 1: Break the pin with ...a6 (forcing the bishop    │
│              to retreat or trade)                             │
│    Option 2: Block the pin with ...Bd7 (interposing)         │
│    Option 3: Move your king to escape the pin (...Kf8)       │
│                                                              │
│  DON'T: Play ...e5 ignoring the pin. Your knight on c6     │
│    is pinned and cannot defend e5! If you play ...e5, the    │
│    knight can't recapture.                                    │
│                                                              │
│ RECOMMENDATION: ...a6 is the best move — it breaks the pin   │
│    and forces the bishop to make a decision.                 │
└──────────────────────────────────────────────────────────────┘
```

---

## Level 3: 1200 ELO — 3-Ply Calculation

### The Core Problem: Shallow Calculation

At 1200 ELO, players can identify threats but fail to calculate deeply enough. They think:

> "If I play Nxe5, I capture a pawn. Done!"

They don't consider the opponent's response (Nxe5 → what does the opponent do?):

> "I play Nxe5, opponent plays ...Bxd1. Oh no, I lost my queen for a knight and pawn!"

### Skills Required

| Skill | Description | How to Train |
|-------|-------------|-------------|
| **3-Ply Calculation** | My move → Opponent's response → My follow-up | Forced move sequences |
| **Forcing Moves First** | Check > Capture > Threat | Calculation discipline |
| **LPDO Awareness** | Loose Pieces Drop Off — notice undefended pieces | Scanning for LPDO |
| **Candidate Moves** | Generate 2-3 candidate moves before calculating | Structured thinking |
| **Blunder Checking** | After finding a "good" move, check if it loses material | Anti-blunder protocol |

### The Calculation Framework

```python
class CalculationExplanation(ExplanationLevel):
    """
    Explanation system for 1200 ELO players.
    Focus: structured calculation, forcing moves, LPDO.
    """

    def demonstrate_calculation(self, position: Position) -> str:
        """Show the player how to calculate 3-ply."""

        # Step 1: Identify forcing moves
        checks = position.find_checks()
        captures = position.find_captures()
        threats = position.find_threats()

        forcing_order = checks + captures + threats

        if not forcing_order:
            return (
                "There are no forcing moves (checks, captures, or threats) in "
                "this position. Focus on positional improvement: develop your "
                "worst piece, improve your pawn structure, or prepare a break."
            )

        # Step 2: Calculate each forcing move
        calculation_lines = []
        for move in forcing_order[:5]:  # Top 5 candidates
            line = self._calculate_line(position, move, depth=3)
            calculation_lines.append(line)

        # Step 3: Present the calculation tree
        output = "CALCULATION EXERCISE:\n\n"
        output += "Step 1: Identify forcing moves (Checks → Captures → Threats)\n"

        if checks:
            output += f"  Checks: {', '.join(str(m) for m in checks)}\n"
        if captures:
            output += f"  Captures: {', '.join(str(m) for m in captures)}\n"
        if threats:
            output += f"  Threats: {', '.join(str(m) for m in threats[:3])}\n"

        output += "\nStep 2: Calculate each line (3 moves deep)\n\n"

        for i, line in enumerate(calculation_lines):
            output += f"Line {i+1}: {line.notation}\n"
            output += f"  {line.explanation}\n\n"

        return output

    def _calculate_line(self, position: Position, move: Move, depth: int) -> CalculationLine:
        """Calculate a line to the given depth."""
        # Apply move
        new_pos = position.after(move)

        if depth <= 1:
            return CalculationLine(
                notation=str(move),
                explanation=f"After {move}, evaluation: {new_pos.evaluate():+.0f} cp"
            )

        # Find opponent's best response
        opponent_best = new_pos.find_best_move()
        if opponent_best:
            after_opp = new_pos.after(opponent_best)

            # Find our best follow-up
            our_best = after_opp.find_best_move()
            if our_best:
                return CalculationLine(
                    notation=f"{move} {opponent_best} {our_best}",
                    explanation=(
                        f"If {move}, then {opponent_best}, then {our_best}. "
                        f"Result: {after_opp.after(our_best).evaluate():+.0f} cp"
                    )
                )

        return CalculationLine(
            notation=str(move),
            explanation=f"After {move}, evaluation: {new_pos.evaluate():+.0f} cp"
        )
```

---

## Level 4: 1500 ELO — Positional Awareness

### The Core Problem: Tactical Without Strategic Foundation

At 1500 ELO, players can calculate and avoid blunders, but they lack **positional understanding**. They play move-by-move without a strategic plan:

> "I calculated 3 moves deep and nothing bad happens. Let me play h3."
> (Meanwhile, the opponent is building a devastating queenside majority)

### Skills Required

| Skill | Description | How to Train |
|-------|-------------|-------------|
| **Weak Squares** | Identify squares that cannot be defended by pawns | Square weakness exercises |
| **Pawn Structures** | Understand pawn chains, islands, majorities, minorities | Study [[01 - The Slav Defense Philosophy\|Slav Defense]] structures |
| **Prophylaxis** | Prevent opponent's plans before they materialize | "What does my opponent want?" exercises |
| **Piece Placement** | Put pieces on their best squares (knight outposts, rook open files) | [[03 - Strategic Themes and Rule Activation\|Strategic theme]] training |
| **Planning** | Create multi-move plans based on pawn structure | Positional study |

### The Positional Assessment Framework

```python
class PositionalExplanation(ExplanationLevel):
    """
    Explanation system for 1500 ELO players.
    Focus: positional understanding, pawn structures, prophylaxis.
    """

    def generate_positional_assessment(self, position: Position) -> str:
        """Generate a positional assessment of the current position."""

        assessment = []

        # 1. Pawn Structure Assessment
        pawn_features = self._assess_pawn_structure(position)
        assessment.append(pawn_features)

        # 2. Piece Placement Assessment
        piece_features = self._assess_piece_placement(position)
        assessment.append(piece_features)

        # 3. Weak Squares Assessment
        weak_squares = self._assess_weak_squares(position)
        assessment.append(weak_squares)

        # 4. Prophylaxis — What does the opponent want?
        opponent_plans = self._identify_opponent_plans(position)
        assessment.append(opponent_plans)

        # 5. Recommended Plan
        plan = self._recommend_plan(position)
        assessment.append(plan)

        return '\n\n'.join(assessment)

    def _assess_pawn_structure(self, position: Position) -> str:
        features = position.features
        lines = ["PAWN STRUCTURE ASSESSMENT:"]

        if features['isolated_pawn_w'] > 0:
            lines.append(
                "   White has an isolated pawn — it cannot be defended by "
                "other pawns. This is a long-term weakness that becomes "
                "more severe in the endgame."
            )

        if features['doubled_pawn_b'] > 0:
            lines.append(
                "   Black has doubled pawns — they cannot defend each other "
                "and the rear pawn blocks the advance of the front pawn."
            )

        if features['passed_pawn_w'] > 0:
            lines.append(
                "   White has a passed pawn — a potential promotion threat "
                "that must be blockaded."
            )

        if features['pawn_chain_b'] > 0:
            lines.append(
                "   Black has a solid pawn chain providing structural "
                "integrity."
            )

        if features['pawn_island_w'] > 2:
            lines.append(
                f"   White has {int(features['pawn_island_w'])} pawn islands — "
                f"more islands mean more weaknesses to defend."
            )

        return '\n'.join(lines)

    def _assess_weak_squares(self, position: Position) -> str:
        """Find squares that cannot be defended by pawns."""
        weak_squares = position.find_weak_squares()
        lines = ["WEAK SQUARES:"]

        if not weak_squares:
            lines.append("  No significant weak squares detected.")
        else:
            for sq, side in weak_squares[:5]:
                color = "White" if side == 'white' else "Black"
                lines.append(
                    f"   {sq} is a weak square for {color} — no pawn can "
                    f"defend it. An enemy piece placed here would be very "
                    f"strong."
                )

        return '\n'.join(lines)

    def _identify_opponent_plans(self, position: Position) -> str:
        """What is the opponent trying to achieve?"""
        plans = position.find_opponent_plans()
        lines = ["PROPHYLAXIS — What does your opponent want?"]

        for plan in plans[:3]:
            lines.append(
                f"   {plan.description}\n"
                f"     Counter-measure: {plan.counter_measure}"
            )

        return '\n'.join(lines)
```

### Engine Output Example (1500 ELO)

```
┌──────────────────────────────────────────────────────────────────┐
│ POSITIONAL ASSESSMENT                                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ PAWN STRUCTURE:                                                  │
│    White has an isolated d4 pawn. This is a classic Carlsbad   │
│     structure weakness. In the middlegame, the pawn can be       │
│     defended by pieces, but in the endgame it becomes a target.  │
│    Black has a solid c6-d5 pawn chain.                          │
│   White has 3 pawn islands vs Black's 2.                         │
│                                                                  │
│ WEAK SQUARES:                                                    │
│    d5 is a weak square for White — no White pawn can control    │
│     it. If Black places a knight on d5, it would dominate the    │
│     board.                                                       │
│    b4 is a potential outpost (see [[03 - Strategic Themes and    │
│     Rule Activation|Knight Outposts]]).                           │
│                                                                  │
│ PROPHYLAXIS — What does your opponent want?                      │
│    White wants to play a minority attack with b4-b5            │
│      Counter-measure: Play ...a5 to prevent b4, or prepare       │
│      ...c5 to counter in the center                              │
│    White wants to place a knight on d5                         │
│      Counter-measure: Keep the d5 square under control with      │
│      ...Nbd7 or ...Ne4                                           │
│                                                                  │
│ RECOMMENDED PLAN for Black:                                      │
│   1. Complete development (Nbd7, Be7 or Bf5)                     │
│   2. Prevent White's minority attack (...a5 or ...c5)            │
│   3. Aim for the ...e5 pawn break when the time is right         │
│   4. Trade into an endgame where the isolated d4 pawn is weak    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Level 5: 1800+ ELO — Advanced Positional Play

### Skills at This Level

| Skill | Description |
|-------|-------------|
| **Prophylactic Thinking** | Anticipate and prevent opponent's plans 2-3 moves ahead |
| **Pawn Break Mastery** | Know when and how to execute critical pawn breaks |
| **Exchange Technique** | Which pieces to trade and which to keep |
| **Endgame Awareness** | Evaluate positions with endgame in mind |
| **Opening Preparation** | Memorized theory with understanding of resulting structures |

At this level, the engine's explanations become more sophisticated:

```python
class AdvancedExplanation(ExplanationLevel):
    """For 1800+ ELO — detailed, technical, and precise."""

    def generate_explanation(self, position: Position, move: Move) -> str:
        # Include evaluation in centipawns
        eval_cp = position.evaluate()

        # Reference specific pawn structures by name
        structure = position.classify_pawn_structure()

        # Mention long-term strategic themes
        themes = position.identify_strategic_themes()

        return (
            f"Evaluation: {eval_cp:+.1f} cp | Structure: {structure}\n"
            f"Themes: {', '.join(themes)}\n"
            f"Move: {move} — {self.explain_strategic_content(move, position)}"
        )
```

---

## The Rating-Adaptive Engine Architecture

```python
class RatingAdaptiveEngine:
    """
    The main engine that adapts its explanations to the player's rating.
    """

    def __init__(self, player_rating: int):
        self.player_rating = player_rating
        self.explanation_level = self._select_level(player_rating)

    def _select_level(self, rating: int) -> ExplanationLevel:
        if rating < 900:
            return BeginnerExplanation()      # Board Vision
        elif rating < 1100:
            return IntermediateExplanation()  # Threat Perception
        elif rating < 1400:
            return CalculationExplanation()   # 3-Ply Calculation
        elif rating < 1700:
            return PositionalExplanation()    # Positional Awareness
        else:
            return AdvancedExplanation()      # Advanced Positional Play

    def explain(self, position: Position, move: Move) -> str:
        """Generate a rating-appropriate explanation."""
        return self.explanation_level.generate_explanation(position, move)
```

---

## Summary

The Rating Climb Roadmap shows how the [[Explainable Chess Engine]] adapts to each skill level:

| Rating | Core Skill | Engine Focus | Explanation Style |
|--------|-----------|-------------|-------------------|
| 800 | Board Vision | Safety checks, hanging pieces | Simple warnings, "Is it safe?" |
| 1000 | Threat Perception | Opponent's intent, pins/forks | "What's the threat?" |
| 1200 | 3-Ply Calculation | Forcing moves, candidate moves | Calculation trees |
| 1500 | Positional Awareness | Pawn structures, weak squares | Positional assessment |
| 1800+ | Advanced Play | Prophylaxis, exchange technique | Technical analysis |

Each level builds on the previous one — you can't calculate 3-ply if you can't see hanging pieces, and you can't assess pawn structures if you can't calculate forcing lines. The engine's adaptive system ensures that players always receive the most relevant guidance for their current stage of development.
