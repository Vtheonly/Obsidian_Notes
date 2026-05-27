# Split & Merge Vault Tools (Refactored System)

An enterprise-grade, highly modular command-line application designed to process, split, merge, standardize, and validate your Obsidian vaults and study notes. 

The system operates around structured domain services, atomic file transactions, clean abstractions, and robust colorized console outputs.

---

## Folder Architecture

```text
split merge/
├── run_vault_tool.py          # Unified system execution portal (CLI Tool)
├── readme.md                 # System operational manual (This file)
└── vault_manager/             # Structural packages and domain classes
    ├── __init__.py
    ├── exceptions.py          # Decoupled domain exceptions
    ├── logging.py             # Traceable terminal color logger
    ├── core/
    │   ├── interfaces.py      # Abstract processing base designs
    │   └── models.py          # Domain data-structures
    ├── services/
    │   ├── splitter.py        # Splitting logic for Vault 1.md
    │   ├── merger.py          # Side-by-side vault merging module
    │   ├── mermaid_fixer.py   # Obsidian Mermaid syntax repair engine
    │   ├── quiz_validator.py  # Structured YAML metadata and callouts checker
    │   └── file_renamer.py    # Two-phase transaction-controlled file renamer
    └── utils/
        └── file_ops.py        # Centralized file I/O operations and directory managers