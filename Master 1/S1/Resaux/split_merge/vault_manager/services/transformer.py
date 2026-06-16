"""
Content Transformation Module.
Parses, cleans, and standardizes document contents.
"""

import re
from typing import List, Dict, Any
from vault_manager.core.interfaces import IContentTransformer


class MermaidFixer(IContentTransformer):
    """
    Standardizes and repairs Obsidian Mermaid formatting errors.
    Fixes unquoted subgraphs, unquoted node labels, and ordered list conflicts.
    """

    def transform(self, content: str) -> str:
        def replace_mermaid(match):
            return self._fix_block(match.group(0))

        return re.sub(r'```mermaid\n.*?```', replace_mermaid, content, flags=re.DOTALL)

    def _fix_block(self, block: str) -> str:
        lines = block.split('\n')
        fixed_lines = []
        for line in lines:
            # 1. Fix unquoted subgraph label: subgraph Name [Label] -> subgraph Name["Label"]
            line = re.sub(r'^(\s*subgraph\s+\w+)\s+\[([^"([][^\]]*)\]', r'\1["\2"]', line)
            # 2. Fix unquoted node label: Node[Label] -> Node["Label"]
            line = re.sub(r'(?<![a-zA-Z0-9_])([a-zA-Z_][a-zA-Z0-9_-]*)\[([^"([\]]+)\]', r'\1["\2"]', line)
            # 3. Fix ordered list triggers to prevent Markdown pre-processing errors
            line = re.sub(r'"(\d)\.\s+', r'"\1: ', line)
            line = re.sub(r'\|(\d)\.\s+', r'|\1: ', line)
            fixed_lines.append(line)
        return '\n'.join(fixed_lines)


class RegexReplacer(IContentTransformer):
    """Applies arbitrary search-and-replace regular expression pipelines."""

    def __init__(self, patterns: List[Dict[str, str]]):
        self.replacements = []
        for p in patterns:
            self.replacements.append((re.compile(p["find"]), p["replace"]))

    def transform(self, content: str) -> str:
        for pattern, replacement in self.replacements:
            content = pattern.sub(replacement, content)
        return content