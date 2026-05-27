"""
Mermaid Diagram Formatting Parser.
Fixes unquoted node/subgraph labels and prevents Obsidian's Markdown parser
from interpreting numeric diagram labels as ordered list elements.
"""

import os
import re
from typing import List
from vault_manager.core.interfaces import FileProcessor
from vault_manager.utils.file_ops import create_backup, write_file_safely
from vault_manager.logging import logger
from vault_manager.exceptions import FileOperationError


class MermaidDiagramFixer(FileProcessor):
    """
    Standardizes Mermaid formatting across vault markdown files.
    """

    def execute(self, vault_root: str = ".") -> None:
        """
        Scans all Markdown files recursively from the target directory,
        creates backups of modified files, and fixes syntax errors.
        """
        if not os.path.isdir(vault_root):
            raise FileOperationError(f"Target vault path is not a directory: {vault_root}")

        md_files = self._find_md_files(vault_root)
        logger.info(f"Scanning {len(md_files)} Markdown files for Mermaid diagrams...")

        modified_count = 0
        total_mermaid_blocks = 0
        modified_list: List[str] = []

        for filepath in md_files:
            rel_path = os.path.relpath(filepath, vault_root)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    original = f.read()
            except Exception as e:
                logger.warning(f"Failed to read file '{rel_path}': {e}")
                continue

            fixed = self._process_markdown(original)

            # Count total mermaid blocks
            blocks_found = re.findall(r'```mermaid\n.*?```', original, re.DOTALL)
            total_mermaid_blocks += len(blocks_found)

            if fixed != original:
                # Create backup copy before making modifications
                create_backup(filepath)
                write_file_safely(filepath, fixed)
                
                modified_count += 1
                modified_list.append(rel_path)
                logger.info(f"    - Cleaned: {rel_path}")

        logger.success(f"Scan complete. Found {total_mermaid_blocks} blocks. Modified {modified_count}/{len(md_files)} files.")

    def _process_markdown(self, content: str) -> str:
        """Finds and processes all Mermaid code blocks in a document."""
        def replace_block(match):
            return self._fix_mermaid_block(match.group(0))

        return re.sub(
            r'```mermaid\n.*?```',
            replace_block,
            content,
            flags=re.DOTALL
        )

    def _fix_mermaid_block(self, block: str) -> str:
        """Fixes syntax errors in a single Mermaid block."""
        lines = block.split('\n')
        fixed_lines = []
        for line in lines:
            line = self._fix_subgraph_label(line)
            line = self._fix_node_label(line)
            line = self._fix_numbered_prefixes(line)
            fixed_lines.append(line)
        return '\n'.join(fixed_lines)

    @staticmethod
    def _fix_subgraph_label(line: str) -> str:
        """Converts: subgraph Name [Label]  ->  subgraph Name[\"Label\"]"""
        return re.sub(
            r'^(\s*subgraph\s+\w+)\s+\[([^"([][^\]]*)\]',
            r'\1["\2"]',
            line
        )

    @staticmethod
    def _fix_node_label(line: str) -> str:
        """Wraps unquoted labels in quotes: NodeID[Label]  ->  NodeID[\"Label\"]"""
        return re.sub(
            r'(?<![a-zA-Z0-9_])([a-zA-Z_][a-zA-Z0-9_-]*)\[([^"([\]]+)\]',
            r'\1["\2"]',
            line
        )

    @staticmethod
    def _fix_numbered_prefixes(line: str) -> str:
        """
        Replaces 'N. ' with 'N: ' in labels to prevent them from being 
        interpreted as markdown list elements.
        """
        # Inside quoted labels: "N. text" -> "N: text"
        line = re.sub(r'"(\d)\.\s+', r'"\1: ', line)
        # Inside edge/note labels: |N. text| -> |N: text|
        line = re.sub(r'\|(\d)\.\s+', r'|\1: ', line)
        return line

    @staticmethod
    def _find_md_files(root_dir: str) -> List[str]:
        """Locates all Markdown files, skipping hidden files and git directories."""
        md_files = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude hidden and system paths
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '.git']
            for f in filenames:
                if f.endswith('.md'):
                    md_files.append(os.path.join(dirpath, f))
        return sorted(md_files)