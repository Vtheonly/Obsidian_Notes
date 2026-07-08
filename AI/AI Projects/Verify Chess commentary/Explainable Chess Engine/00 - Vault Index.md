---
tags: [index, vault-map, readme]
project: Explainable Chess Engine
---

# Explainable Chess Engine — Vault Index

> **Core Goal:** Build a chess engine that doesn't just play strong moves — it *explains why* using human-understandable reasoning, supported by multiple chess principles, rules, heuristics, and strategic concepts.

This vault contains everything you need to understand the theory, architecture, algorithms, and implementation behind an explainable chess engine. It is organized as a learning roadmap from foundations to advanced integration.

---

## Reading Order (Recommended Path)

Read chapters in sequence. Each chapter builds on the previous one.

### Phase 1: Foundations & Search
| # | Chapter | Notes | Core Question |
|---|---------|-------|---------------|
| 01 | [[01 - Chess as a Zero-Sum Game]] → [[02 - Board Representation]] → [[03 - Move Generation]] → [[04 - The Explainability Problem]] | 4 | Why is chess hard? How do we represent it? What are we trying to build? |
| 02 | [[01 - Minimax Algorithm]] → [[02 - Negamax Formulation]] → [[03 - Alpha-Beta Pruning]] → [[04 - Principal Variation Search (PVS)]] | 4 | How do engines search the game tree? |
| 03 | [[01 - Iterative Deepening]] → [[02 - Move Ordering]] → [[03 - Late Move Reductions (LMR)]] → [[04 - Null Move Pruning (NMP)]] → [[05 - Quiescence Search]] | 5 | How do engines search deeper without exploding? |
| 04 | [[01 - Zobrist Hashing]] → [[02 - Transposition Table Architecture]] | 2 | How do engines avoid redundant computation? |

### Phase 2: Evaluation & Depth Control
| # | Chapter | Notes | Core Question |
|---|---------|-------|---------------|
| 05 | [[01 - Static Evaluation Overview]] → [[02 - Material Evaluation]] → [[03 - Piece-Square Tables]] → [[04 - Pawn Structure Evaluation]] → [[05 - King Safety Evaluation]] → [[06 - Mobility and Piece Activity]] → [[07 - Threats and Tactical Patterns]] | 7 | How does the engine evaluate positions using human concepts? |
| 06 | [[01 - The Depther Philosophy]] → [[02 - Root-Level Selectivity]] → [[03 - Depth Extension Rules]] → [[04 - Depth Reduction Rules]] → [[05 - Quiescence Termination Rules]] → [[06 - Safety and Control Rules]] → [[07 - The Depth Rules Module (Code Architecture)]] | 7 | How does the engine decide how deep to search each line? |

### Phase 3: Psychology, Rules & Explanation
| # | Chapter | Notes | Core Question |
|---|---------|-------|---------------|
| 07 | [[01 - Human Chess Thinking Models]] → [[02 - Feeling for the Pieces]] → [[03 - Square Weakness and Outposts]] → [[04 - Prophylaxis]] → [[05 - The Six Chess Crimes]] → [[06 - Tactical Blindness Patterns]] | 6 | How do humans think about chess and what mistakes do they make? |
| 08 | [[01 - Rule Engine Architecture]] → [[02 - Chess Knowledge Representation]] → [[03 - Multi-Rule Decision Making]] → [[04 - Confidence Scoring and Rule Weighting]] → [[05 - The Rule Module System (Code)]] | 5 | How are chess rules encoded, combined, and weighted? |
| 09 | [[01 - Explainable AI (XAI) Overview]] → [[02 - Concept Bottleneck Models]] → [[03 - Post-Hoc Rationalization and Surrogate Models]] → [[04 - Move Explanation Architecture]] → [[05 - Audience-Adaptive Explanations]] → [[06 - Rule Conflict Resolution in Explanations]] | 6 | How does the system produce human-readable explanations? |

### Phase 4: Language, Tuning & Integration
| # | Chapter | Notes | Core Question |
|---|---------|-------|---------------|
| 10 | [[01 - NLG for Chess Analysis Overview]] → [[02 - The Heuristic Delta Pipeline]] → [[03 - LLM Narrator Architecture]] → [[04 - Template-Based vs LLM-Based Generation]] → [[05 - Explanation Quality Metrics]] | 5 | How are structured rule outputs converted to natural language? |
| 11 | [[01 - The Tuning Problem]] → [[02 - Texel Tuning Method]] → [[03 - Credit Assignment Problem]] → [[04 - L1 Regularization and Sparsity]] → [[05 - Constrained Optimization]] → [[06 - Feature Orthogonality Design]] | 6 | How are rule weights automatically optimized from game data? |
| 12 | [[01 - Neuro-Symbolic Architecture Overview]] → [[02 - C++ Python Interfacing via Ctypes]] → [[03 - Declarative Rule Engine with Bitboards]] → [[04 - The Verbalization Pipeline]] → [[05 - Combining Stockfish with Explanations]] | 5 | How do the C++ fast core and Python explanation layer work together? |

### Phase 5: Data, Openings & Application
| # | Chapter | Notes | Core Question |
|---|---------|-------|---------------|
| 13 | [[01 - Data Pipeline Architecture]] → [[02 - Feature Extraction in C++]] → [[03 - Python PyTorch Optimization Engine]] → [[04 - The Puzzle Database System]] | 4 | How is training data processed and features extracted? |
| 14 | [[01 - The Slav Defense Philosophy]] → [[02 - Main Line, Exchange, and Slow Systems]] → [[03 - Strategic Themes and Rule Activation]] | 3 | How does the engine explain opening choices? (Case study) |
| 15 | [[01 - Rating Climb Roadmaps]] → [[02 - Defense and Swindling]] → [[03 - The 100 Position Test]] → [[04 - Puzzle Training Integration]] → [[05 - Android Puzzle App Architecture]] | 5 | How does the system train players and integrate into apps? |

---

## Chapter Directory

```
Explainable-Chess-Engine-Vault/
├── 00 - Vault Index.md                    ← You are here
├── 01-Foundations/                        (4 notes)
│   ├── 01 - Chess as a Zero-Sum Game.md
│   ├── 02 - Board Representation.md
│   ├── 03 - Move Generation.md
│   └── 04 - The Explainability Problem.md
├── 02-Search-Algorithms/                  (4 notes)
│   ├── 01 - Minimax Algorithm.md
│   ├── 02 - Negamax Formulation.md
│   ├── 03 - Alpha-Beta Pruning.md
│   └── 04 - Principal Variation Search (PVS).md
├── 03-Search-Accelerators/                (5 notes)
│   ├── 01 - Iterative Deepening.md
│   ├── 02 - Move Ordering.md
│   ├── 03 - Late Move Reductions (LMR).md
│   ├── 04 - Null Move Pruning (NMP).md
│   └── 05 - Quiescence Search.md
├── 04-Transposition-Tables-and-Zobrist/   (2 notes)
│   ├── 01 - Zobrist Hashing.md
│   └── 02 - Transposition Table Architecture.md
├── 05-Evaluation-Functions-and-Heuristics/ (7 notes)
│   ├── 01 - Static Evaluation Overview.md
│   ├── 02 - Material Evaluation.md
│   ├── 03 - Piece-Square Tables.md
│   ├── 04 - Pawn Structure Evaluation.md
│   ├── 05 - King Safety Evaluation.md
│   ├── 06 - Mobility and Piece Activity.md
│   └── 07 - Threats and Tactical Patterns.md
├── 06-Adaptive-Depth-Control/             (7 notes)
│   ├── 01 - The Depther Philosophy.md
│   ├── 02 - Root-Level Selectivity.md
│   ├── 03 - Depth Extension Rules.md
│   ├── 04 - Depth Reduction Rules.md
│   ├── 05 - Quiescence Termination Rules.md
│   ├── 06 - Safety and Control Rules.md
│   └── 07 - The Depth Rules Module (Code Architecture).md
├── 07-Chess-Psychology-and-Human-Thinking/ (6 notes)
│   ├── 01 - Human Chess Thinking Models.md
│   ├── 02 - Feeling for the Pieces.md
│   ├── 03 - Square Weakness and Outposts.md
│   ├── 04 - Prophylaxis.md
│   ├── 05 - The Six Chess Crimes.md
│   └── 06 - Tactical Blindness Patterns.md
├── 08-Rule-Based-Reasoning-Systems/       (5 notes)
│   ├── 01 - Rule Engine Architecture.md
│   ├── 02 - Chess Knowledge Representation.md
│   ├── 03 - Multi-Rule Decision Making.md
│   ├── 04 - Confidence Scoring and Rule Weighting.md
│   └── 05 - The Rule Module System (Code).md
├── 09-Explainable-AI-for-Chess/           (6 notes)
│   ├── 01 - Explainable AI (XAI) Overview.md
│   ├── 02 - Concept Bottleneck Models.md
│   ├── 03 - Post-Hoc Rationalization and Surrogate Models.md
│   ├── 04 - Move Explanation Architecture.md
│   ├── 05 - Audience-Adaptive Explanations.md
│   └── 06 - Rule Conflict Resolution in Explanations.md
├── 10-Natural-Language-Generation/        (5 notes)
│   ├── 01 - NLG for Chess Analysis Overview.md
│   ├── 02 - The Heuristic Delta Pipeline.md
│   ├── 03 - LLM Narrator Architecture.md
│   ├── 04 - Template-Based vs LLM-Based Generation.md
│   └── 05 - Explanation Quality Metrics.md
├── 11-Parameter-Tuning-and-Optimization/  (6 notes)
│   ├── 01 - The Tuning Problem.md
│   ├── 02 - Texel Tuning Method.md
│   ├── 03 - Credit Assignment Problem.md
│   ├── 04 - L1 Regularization and Sparsity.md
│   ├── 05 - Constrained Optimization.md
│   └── 06 - Feature Orthogonality Design.md
├── 12-Neuro-Symbolic-Integration/         (5 notes)
│   ├── 01 - Neuro-Symbolic Architecture Overview.md
│   ├── 02 - C++ Python Interfacing via Ctypes.md
│   ├── 03 - Declarative Rule Engine with Bitboards.md
│   ├── 04 - The Verbalization Pipeline.md
│   └── 05 - Combining Stockfish with Explanations.md
├── 13-Data-Pipeline-and-Feature-Engineering/ (4 notes)
│   ├── 01 - Data Pipeline Architecture.md
│   ├── 02 - Feature Extraction in C++.md
│   ├── 03 - Python PyTorch Optimization Engine.md
│   └── 04 - The Puzzle Database System.md
├── 14-Opening-Case-Study-Slav-Defense/    (3 notes)
│   ├── 01 - The Slav Defense Philosophy.md
│   ├── 02 - Main Line, Exchange, and Slow Systems.md
│   └── 03 - Strategic Themes and Rule Activation.md
└── 15-Training-Methodology-and-Puzzles/   (5 notes)
    ├── 01 - Rating Climb Roadmaps.md
    ├── 02 - Defense and Swindling.md
    ├── 03 - The 100 Position Test.md
    ├── 04 - Puzzle Training Integration.md
    └── 05 - Android Puzzle App Architecture.md
```

---

## Key Concepts Cross-Reference

| Concept | Primary Note | Related Notes |
|---------|-------------|---------------|
| Alpha-Beta Pruning | [[03 - Alpha-Beta Pruning]] | [[02 - Negamax Formulation]], [[02 - Move Ordering]] |
| Quiescence Search | [[05 - Quiescence Search]] | [[05 - Quiescence Termination Rules]], [[07 - Threats and Tactical Patterns]] |
| LMR | [[03 - Late Move Reductions (LMR)]] | [[04 - Depth Reduction Rules]], [[02 - Move Ordering]] |
| Depther Engine | [[01 - The Depther Philosophy]] | All of Chapter 06 |
| Chess Crimes | [[05 - The Six Chess Crimes]] | [[06 - Tactical Blindness Patterns]], [[04 - Depth Reduction Rules]] |
| Concept Bottleneck | [[02 - Concept Bottleneck Models]] | [[01 - Explainable AI (XAI) Overview]], [[02 - Chess Knowledge Representation]] |
| Heuristic Delta | [[02 - The Heuristic Delta Pipeline]] | [[04 - Move Explanation Architecture]], [[04 - The Verbalization Pipeline]] |
| Texel Tuning | [[02 - Texel Tuning Method]] | [[03 - Credit Assignment Problem]], [[04 - L1 Regularization and Sparsity]] |
| Bitboards | [[02 - Board Representation]] | [[03 - Declarative Rule Engine with Bitboards]], [[02 - Feature Extraction in C++]] |
| Rule Weighting | [[04 - Confidence Scoring and Rule Weighting]] | [[03 - Multi-Rule Decision Making]], [[01 - Rule Engine Architecture]] |
| Stockfish Layer | [[05 - Combining Stockfish with Explanations]] | [[03 - Post-Hoc Rationalization and Surrogate Models]], [[01 - Neuro-Symbolic Architecture Overview]] |

---

## Statistics

- **Total Notes:** 74
- **Total Words:** ~160,000
- **Chapters:** 15
- **Languages Used:** C++, Python, Java, SQL, XML
