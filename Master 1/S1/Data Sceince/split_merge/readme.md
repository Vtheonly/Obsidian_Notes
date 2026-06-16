# Dynamic Obsidian Vault Management System

A highly modular, professional-grade Python system designed to split, merge, validate, clean, and sequentially rename files across any Obsidian note architecture. 

Rather than hardcoding directory or formatting schemas, the system uses a **Strategy Pattern** combined with a central declarative `config.yaml` file, making it adaptable to any vault structure.

---

## Capabilities

1. **Flexible Splitting (`split`):** Uses configurable Regular Expressions to split a single consolidated `.md` file (like `Vault 1.md`) into highly structured, nested folders and files.
2. **Context-Aware Merging (`merge`):** Intelligently merges new content into your active Obsidian workspace. Supports non-destructive merging (`side_by_side` creating `(Vault 1).md` copies), direct overrides, and skipping existing files.
3. **Mermaid Formatting Repair (`fix-mermaid`):** Automatically standardizes unquoted node labels, fixes unquoted subgraphs, and replaces ordered list triggers inside ` ```mermaid ` code blocks to prevent Obsidian parser conflicts.
4. **Semantic Quiz Validation (`validate`):** Audits frontmatter, HPO/MONDO ontologies, and Obsidian callouts (`[!question]`, `[!success]- Answer`, `[!example]`) in quiz notes.
5. **Transactional File Renaming (`rename`):** Executes dual-phase, atomic renames (staging files to temporary locks first). Supports both simple dictionary maps and dynamic RegEx pattern matching with variable padding.

---

## Command Reference

Verify your configuration settings in `config.yaml` before running commands.

### 1. Split a Consolidated Vault
To split a single file based on the `image_processing_course` regular expression rules:
```bash
python run_vault_tool.py split image_processing_course
```

### 2. Merge Content Into Workspace
To merge new sections into your active vault structure safely without overwriting your original notes:
```bash
python run_vault_tool.py merge image_processing_course
```

### 3. Repair Mermaid Rendering Errors
To recursively scan and standardise your Mermaid diagram labels:
```bash
python run_vault_tool.py fix-mermaid --directory "."
```

### 4. Validate Quiz Formats
To verify formatting and ontology identifiers in your study notes:
```bash
python run_vault_tool.py validate "Academic/Deep Learning/Questions/Qs1.md"
```

### 5. Run Transactional Renaming
* **Using Map Strategy (Java OOP notes):**
  ```bash
  python run_vault_tool.py rename java_oop
  ```
* **Using Pattern Strategy (Automata/Turing Machine notes):**
  ```bash
  python run_vault_tool.py rename automata