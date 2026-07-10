# Analysis of the Original Quiz Prompt

> The original prompt is preserved verbatim in `04b_original_prompt_verbatim.md`
> (extracted from the user's `Quiz Structre.md` upload). This document analyses
> its weaknesses so the rewrite (`02_quiz_generation_prompt.md`) is fully
> justified and traceable.

## Original prompt — high-level structure

The original prompt contained the following sections, in order:

1. A preamble warning the AI to follow the format strictly.
2. A list of three supported question types.
3. A single example code block showing one question of each type.
4. A "Task Definition" describing the chapter folder structure and the 30-question
   requirement (10 TF + 10 MC + 10 Matching per file, 2 files per chapter).
5. A "Validation Requirement" mentioning a Python validation script in
   `split_merge/`.
6. A "Scaling Rule" extending the task to all chapters.
7. A "Final Requirement" telling the AI: "Do not generate content yet. Confirm
   understanding first and wait for execution mode."

## What was right about it

* It correctly identified the three question types.
* It included a single example that, on careful reading, does demonstrate all
  three types.
* It mentioned the validation script, signalling that format strictness
  mattered.
* It named the chapter folder convention (`Chapter 01/`) and the per-file
  question budget (30 = 10/10/10).

## What was wrong about it

### W1. Mixed concerns

The prompt conflated four distinct concerns:

* the **format specification** (the grammar of quiz files),
* the **task workflow** (how many files, what folder, when to confirm),
* the **validation requirement** (use the Python script),
* the **execution protocol** (do not generate yet, wait for the green light).

AI models have limited attention. When four concerns are interleaved, the
format spec — the most important concern — gets diluted. The rewrite isolates
the format spec into its own section (§A–F) and pushes workflow into a
separate "Execution" section at the end.

### W2. Ambiguity about quote depth

The original example showed `> [!question]` and `>> [!success]- Answer` but
never explained:

* Why some lines start with `>` and others with `>>`.
* That the answer callout MUST be at depth 2.
* That MC options MUST be at depth 1.
* That the matching divider line MUST be bare `>` (depth 1, no trailing
  space).

These are the single most common source of parser failures (see
`04_common_mistakes.md` Categories B and D). The rewrite makes the two depths
a top-level rule (§B of the prompt) and repeats them in every question-type
section.

### W3. No explanation of Group B's `n)`-starting letters

The original example showed `n)`, `o)`, `p)`, `q)` for Group B but did not
explain:

* That Group B always starts at `n` (not at `a`).
* Why (so the parser can tell the two groups apart).
* That this is a hard rule, not a stylistic choice.

The rewrite makes this explicit (§E of the prompt).

### W4. No explanation of the matching divider line

The original example included a bare `>` line between Group A and Group B and
between Group B and the Answer, but never called attention to it. Many AI
models either omit it or replace it with `>>`. The rewrite bolds this as a
CRITICAL rule.

### W5. No negative examples

The original prompt had only one positive example. It did not say "do not do
X." AI models are much better at avoiding mistakes when given explicit
forbidden patterns. The rewrite includes a 22-item "Forbidden patterns" list
(§F).

### W6. No self-check

The original prompt had no checklist. AI models benefit from a final
self-checklist because it forces them to re-verify before emitting. The
rewrite includes a 12-item self-check (§H).

### W7. The "confirm understanding" instruction backfired

The original prompt ended with "Do not generate content yet. Confirm
understanding first." This caused many AI models to reply with a multi-paragraph
confirmation of understanding — and then to never actually generate the files,
because the user's next message looked like a new conversation. The rewrite
removes this instruction entirely and tells the model to emit files directly
when invoked.

### W8. No mention of UTF-8 / line endings / trailing whitespace

These encoding-level details matter for the validator. The rewrite includes a
"Character & Encoding Rules" section in the spec doc
(`01_quiz_format_specification.md` §11).

### W9. The example was insufficiently varied

The original example showed exactly one question per type. It did not show:

* A TF question with `False` as the answer.
* An MC question where the correct answer is not `a)`.
* A matching question where the mappings are non-alphabetical (i.e. `a) -> p)`
  instead of `a) -> n)`).

The rewrite shows varied examples in the spec doc and in
`examples/good_quiz_example.md`.

### W10. No mention of what the parser does NOT check

The original prompt implied the validator checks everything. In fact it only
checks structure (see `01_quiz_format_specification.md` §10.7). The rewrite
documents this explicitly so the AI does not waste effort trying to satisfy
checks that do not exist.

## Summary of changes in the rewrite

| Concern | Original | Rewrite |
|---------|----------|---------|
| Format spec vs workflow | Interleaved | Separated |
| Quote depth rule | Implicit | Explicit (§B) |
| Group B `n)` rule | Implicit | Explicit (§E) |
| Matching divider line | Implicit | Bolded as CRITICAL (§E) |
| Negative examples | None | 22-item forbidden list (§F) |
| Self-check | None | 12-item checklist (§H) |
| Encoding rules | None | Full section (spec §11) |
| "Confirm understanding" | Present | Removed |
| Varied examples | 1 per type | Multiple, with non-trivial mappings |

The rewrite is longer than the original, but every additional line addresses a
specific failure mode observed in the corpus or implied by the validator's
regex rules.
