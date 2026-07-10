# Dynamic Obsidian Vault Management System

A modular, professional-grade Python system designed to split, merge,
validate, clean, and sequentially rename files across any Obsidian note
architecture.

The system uses a **Strategy Pattern** combined with a central declarative
`config.yaml` file. No directory layout or formatting schema is hardcoded —
every pipeline is configured via named entries in the YAML, making the
system adaptable to any vault structure.

---

## Architecture

```
run_vault_tool.py                  ← CLI entry point (argparse wiring only)
└── vault_manager/
    ├── cli/
    │   └── handlers.py             ← one handle_* function per subcommand
    ├── core/
    │   ├── interfaces.py           ← ABCs: IDocumentParser, IMergeStrategy,
    │   │                             IValidationStrategy, IRenamingStrategy,
    │   │                             IContentTransformer
    │   └── models.py               ← ParsedSegment, ValidationReport dataclasses
    ├── services/
    │   ├── splitter.py             ← DynamicRegexParser
    │   ├── merger.py               ← FlexibleMerger (side_by_side / skip / overwrite)
    │   ├── validator.py            ← ObsidianQuizValidator
    │   ├── transformer.py          ← MermaidFixer, RegexReplacer
    │   ├── renamer.py              ← MapRenamer, RegexPatternRenamer
    │   ├── rename_transaction.py   ← atomic_two_phase_rename (rollback-safe)
    │   └── purge_emojis.py         ← EmojiPurgeService
    ├── utils/
    │   └── file_ops.py             ← read/write/backup/zip + re-export shim
    ├── exceptions.py               ← VaultManagerException hierarchy
    └── logging.py                  ← ThreadSafeLogger singleton
config.yaml                        ← declarative pipeline definitions
```

### Layering

* **core** — interfaces and dataclass models. No dependencies on services
  or utils.
* **services** — concrete implementations. Depends on core and utils.
* **utils** — pure filesystem primitives. Depends on exceptions and
  logging only.
* **cli** — thin handlers that parse CLI args, load YAML config, and
  delegate to services.

### Why `rename_transaction.py` is a separate module

The original `file_ops.py` mixed pure I/O utilities (`read_file_safely`,
`write_file_safely`, `compress_directory_to_zip`) with the much larger
two-phase transactional rename logic (which has its own pre-flight checks,
staging phase, commit phase, and rollback paths). Splitting them keeps
each module under 130 lines and makes the rollback logic easier to audit.
A backward-compat re-export shim in `file_ops.py` keeps the original
`from vault_manager.utils.file_ops import atomic_two_phase_rename`
import working unchanged.

---

## Capabilities

1. **Flexible Splitting (`split`)** — uses configurable regular expressions
   to split a single consolidated `.md` file (like `Vault 1.md`) into
   structured, nested folders and files.
2. **Context-Aware Merging (`merge`)** — intelligently merges new content
   into an active Obsidian workspace. Supports non-destructive merging
   (`side_by_side` creating `(Vault 1).md` copies), direct overrides, and
   skipping existing files.
3. **Mermaid Formatting Repair (`fix-mermaid`)** — standardises unquoted
   node labels, fixes unquoted subgraphs, and rewrites ordered-list
   triggers inside `` ```mermaid `` code blocks to prevent Obsidian parser
   conflicts.
4. **Semantic Quiz Validation (`validate`)** — audits frontmatter,
   `sources:` wikilinks, and Obsidian callouts (`[!question]`,
   `[!success]- Answer`, `[!example]`) in quiz notes.
5. **Transactional File Renaming (`rename`)** — executes dual-phase,
   atomic renames (staging files to temporary locks first). Supports both
   simple dictionary maps and dynamic RegEx pattern matching with variable
   padding.
6. **Emoji Purging (`purge-emojis`)** — recursively strips every Unicode
   emoji character from text files in a directory, with binary-safe file
   detection.

---

## Command Reference

Verify your configuration settings in `config.yaml` before running commands.

### 1. Split a Consolidated Vault

```bash
python run_vault_tool.py split image_processing_course
```

### 2. Merge Content Into Workspace

```bash
python run_vault_tool.py merge image_processing_course
```

### 3. Repair Mermaid Rendering Errors

```bash
python run_vault_tool.py fix-mermaid --directory "."
```

### 4. Validate Quiz Formats

```bash
python run_vault_tool.py validate "Academic/Deep Learning/Questions/Qs1.md"
```

### 5. Run Transactional Renaming

* **Map strategy (Java OOP notes):**
  ```bash
  python run_vault_tool.py rename java_oop
  ```
* **Pattern strategy (Automata / Turing Machine notes):**
  ```bash
  python run_vault_tool.py rename automata
  ```

### 6. Purge Emojis

```bash
python run_vault_tool.py purge-emojis --directory "."
```

---

## Tests

A comprehensive golden-test suite lives in `tests/`. It exercises every
public surface of the package and pins observable behaviour byte-for-byte.
See `tests/README.md` for usage.

```bash
CODEBASE_UNDER_TEST=refactored python -m pytest tests/
```
