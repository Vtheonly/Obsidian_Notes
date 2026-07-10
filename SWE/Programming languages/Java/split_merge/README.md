# Part 2 — Split/Merge Tool Refactor

## What's in this folder

| Path | Purpose |
|------|---------|
| `01_refactor_documentation.md` | Full refactor documentation: original architecture, decisions, file-by-file change log, equivalence evidence. |
| `refactored_code/` | The refactored codebase, ready to drop into the project root. |
| `tests/` | Golden test suite (63 tests) that proves behavior equivalence with the original. |
| `README.md` | This file. |

## Quick summary

The refactor preserves **100% of the original behavior** while improving
readability and separation of concerns. Key changes:

1. CLI handlers extracted from `run_vault_tool.py` (333 lines) into
   `vault_manager/cli/handlers.py`. The entry point is now a thin
   116-line dispatcher.
2. `atomic_two_phase_rename` extracted from `utils/file_ops.py` into its
   own `services/rename_transaction.py` module. A backward-compat
   re-export shim keeps the original import path working.
3. Per-type classifiers extracted in `services/validator.py` from
   inline boolean expressions into named functions
   (`_is_true_false`, `_is_multiple_choice`, `_is_matching`).
4. Nested `save_current_segment` lifted to a `_flush_segment` static
   method in `services/splitter.py`.
5. Cryptic variable names renamed (`current_content` -> `current_body`).
6. Docstrings added throughout explaining non-obvious decisions (e.g.
   why the logger uses `[]` as the prefix for three severity levels).

## What was NOT changed

* No public class name, method signature, or function signature.
* No CLI argument or subcommand.
* No `config.yaml` schema.
* No regex pattern (validator, splitter, transformer, purge_emojis).
* No error message string.
* No log message string (including the `[]` prefix quirk).
* No exception type or hierarchy.
* No file written to disk (path or content).

## How to verify equivalence

```bash
cd tests/
python setup_workdirs.py                    # copies both codebases into tests/work/
CODEBASE_UNDER_TEST=original python -m pytest .      # 63 passed
CODEBASE_UNDER_TEST=refactored python -m pytest .    # 63 passed
```

Both runs must report `63 passed`. See `tests/README.md` for details.

## End-to-end CLI verification

Beyond the unit tests, each CLI command (`split`, `merge`, `fix-mermaid`,
`purge-emojis`, `validate`, `rename`) was run against identical inputs
on both codebases. The resulting file trees, file contents, stdout, and
stderr were compared byte-for-byte. All comparisons were identical
(modulo directory-name differences). See §5 of
`01_refactor_documentation.md` for the evidence table.

In particular, all 18 quiz files from the user's actual corpus
(`Quiz Sample.txt`) pass validation under BOTH codebases with identical
`stats` output (`{'true_false': 10, 'multiple_choice': 10, 'matching': 10}`
per file).
