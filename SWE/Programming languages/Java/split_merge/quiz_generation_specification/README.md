# Part 1 — Quiz Documentation and Prompt Redesign

## What's in this folder

| File | Purpose |
|------|---------|
| `01_quiz_format_specification.md` | The definitive format spec. Forward this to any AI that needs to generate quiz files. |
| `02_quiz_generation_prompt.md` | The rewritten generation prompt. Paste the section between `--- BEGIN PROMPT ---` and `--- END PROMPT ---` into the AI as the system or first user message. |
| `03_format_cheatsheet.md` | One-page quick reference for humans. |
| `04_common_mistakes.md` | Full catalogue of common AI mistakes, grouped by category, with rule references. |
| `04b_original_prompt_analysis.md` | Analysis of the original prompt and justification for each change in the rewrite. |
| `examples/good_quiz_example.md` | A 30-question reference file that passes every rule in the spec. |
| `examples/bad_examples_annotated.md` | 22 invalid fragments with explanations and corrected versions. |
| `examples/empty_template.md` | A 30-question skeleton file ready to be filled in. |

## Recommended workflow

1. Read `01_quiz_format_specification.md` once to understand the format.
2. Keep `03_format_cheatsheet.md` open as a quick reference.
3. When generating a new chapter:
   - Paste the prompt from `02_quiz_generation_prompt.md` into the AI.
   - Provide the chapter number, title, source list, and topic areas.
   - Ask the AI to emit both `<Chapter XX>_Quiz_A.md` and
     `<Chapter XX>_Quiz_B.md`.
4. After generation, run the validator:
   ```bash
   python run_vault_tool.py validate "Quiz/Chapter XX/"
   ```
5. If the validator reports errors, cross-reference them with
   `04_common_mistakes.md` to identify the pattern, then ask the AI to
   regenerate the offending question with the corrected format.

## How the spec was reverse-engineered

The spec was derived from three sources:

1. **The 18-file quiz corpus** (`Quiz Sample.txt`). Every rule in the spec
   was cross-checked against multiple files in the corpus to confirm it is
   consistently applied.
2. **The validator's classification regexes** (`vault_manager/services/validator.py`).
   Each regex was translated into a human-readable rule. For example, the
   regex `>>\s*\[!success\]-\s*Answer` became rule CC-2 ("Every question
   MUST contain exactly one `>> [!success]- Answer` callout") and rule A1
   in the mistakes catalogue ("Missing `-` in the answer callout").
3. **The original prompt** (`Quiz Structre.md`). Used as a starting point;
   each ambiguity or omission in the original was addressed in the rewrite
   (see `04b_original_prompt_analysis.md`).

The spec is therefore not a creative reimagining of the format — it is a
faithful formalisation of the format the existing corpus already follows and
the validator already enforces.
