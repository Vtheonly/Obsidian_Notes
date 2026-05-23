#!/usr/bin/env python3
"""
Fix Mermaid diagrams in ALL Markdown files across the entire vault.

Problem: Obsidian's markdown pre-processor scans the entire file — including
inside ```mermaid blocks — for patterns like "1. " (digit + period + space)
and interprets them as ordered list syntax, producing:
    "Unsupported markdown: list"

This happens even inside quoted labels like:
    Step1["1. Edit/Create Python Class in models.py"]
And inside edge labels like:
    -->|1. HTTP Request|

Fix 1: Replace "N. " (digit-period-space) with "N: " (digit-colon-space)
       inside all ```mermaid ... ``` blocks.

Fix 2: Wrap unquoted node labels in double quotes:
       NodeID[Label]  →  NodeID["Label"]
       subgraph Name [Label]  →  subgraph Name["Label"]
"""

import re
import os
import shutil
from pathlib import Path

VAULT_DIR = "."  # Current directory (root of the vault)


def fix_subgraph_label(line: str) -> str:
    """subgraph Name [Label] → subgraph Name["Label"]"""
    return re.sub(
        r'^(\s*subgraph\s+\w+)\s+\[([^"([][^\]]*)\]',
        r'\1["\2"]',
        line
    )


def fix_node_label(line: str) -> str:
    """NodeID[Label] → NodeID["Label"] for unquoted labels."""
    return re.sub(
        r'(?<![a-zA-Z0-9_])([a-zA-Z_][a-zA-Z0-9_-]*)\[([^"([\]]+)\]',
        r'\1["\2"]',
        line
    )


def fix_numbered_prefixes(line: str) -> str:
    """
    Replace "N. " (digit-period-space) with "N: " (digit-colon-space)
    to break markdown list detection.
    """
    # Inside quoted strings:  "N. text"  →  "N: text"
    line = re.sub(r'"(\d)\.\s+', r'"\1: ', line)
    # Inside pipe-delimited edge/note labels:  |N. text|  →  |N: text|
    line = re.sub(r'\|(\d)\.\s+', r'|\1: ', line)
    return line


def fix_mermaid_block(block: str) -> str:
    """Apply all mermaid fixes to a single ```mermaid block."""
    lines = block.split('\n')
    fixed_lines = []
    for line in lines:
        line = fix_subgraph_label(line)
        line = fix_node_label(line)
        line = fix_numbered_prefixes(line)
        fixed_lines.append(line)
    return '\n'.join(fixed_lines)


def process_markdown(content: str) -> str:
    """Find all ```mermaid blocks and apply fixes."""
    def replace_mermaid(match):
        return fix_mermaid_block(match.group(0))

    return re.sub(
        r'```mermaid\n.*?```',
        replace_mermaid,
        content,
        flags=re.DOTALL
    )


def find_md_files(root_dir: str) -> list:
    """Recursively find all .md files, excluding hidden dirs and .git."""
    md_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories and .git
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '.git']
        for f in filenames:
            if f.endswith('.md'):
                md_files.append(os.path.join(dirpath, f))
    return sorted(md_files)


def main():
    if not os.path.isdir(VAULT_DIR):
        print(f"Error: Directory '{VAULT_DIR}' not found.")
        return

    md_files = find_md_files(VAULT_DIR)
    print(f"Found {len(md_files)} Markdown files to scan.")

    fixed_count = 0
    total_mermaid_blocks = 0
    fixed_files_list = []

    for filepath in md_files:
        rel_path = os.path.relpath(filepath, VAULT_DIR)

        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()

        fixed = process_markdown(original)

        # Count mermaid blocks
        blocks = re.findall(r'```mermaid\n.*?```', original, re.DOTALL)
        total_mermaid_blocks += len(blocks)

        if fixed != original:
            # Create backup
            backup_path = filepath + '.bak'
            shutil.copy2(filepath, backup_path)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed)

            fixed_count += 1
            fixed_files_list.append(rel_path)
            print(f"  ✓ {rel_path}")

    print(f"\nScanned {len(md_files)} files, found {total_mermaid_blocks} mermaid blocks total.")
    print(f"Modified: {fixed_count}/{len(md_files)} files.")

    if fixed_files_list:
        print("\nFixed files:")
        for f in fixed_files_list:
            print(f"  - {f}")

    print("\n--- What was done ---")
    print("  • Unquoted node labels:  Node[Label]  →  Node[\"Label\"]")
    print("  • Unquoted subgraph labels:  subgraph Name [Label]  →  subgraph Name[\"Label\"]")
    print("  • Numbered prefixes:  \"N. text\"  →  \"N: text\"  and  |N. text|  →  |N: text|")
    print("  • Backups saved as *.bak next to each modified file")


if __name__ == '__main__':
    main()