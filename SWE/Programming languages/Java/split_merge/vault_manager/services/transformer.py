"""
Content transformation services.

Two implementations of :class:`IContentTransformer` are provided:

* :class:`MermaidFixer` — repairs common formatting mistakes in
  ``mermaid`` code blocks so that Obsidian's Mermaid renderer accepts them.
  Specifically: quotes unquoted node labels, quotes unquoted subgraph
  labels, and rewrites ordered-list triggers inside quoted strings (to
  avoid Markdown pre-processing conflicts).
* :class:`RegexReplacer` — applies a list of ``find``/``replace`` regex
  pairs in order. Generic utility used by ad-hoc transformation pipelines.
"""

from __future__ import annotations

import re
from typing import Dict, List

from vault_manager.core.interfaces import IContentTransformer


# Match a ```mermaid ... ``` fenced code block (DOTALL so newlines are included).
_RE_MERMAID_BLOCK = re.compile(r"```mermaid\n.*?```", re.DOTALL)


class MermaidFixer(IContentTransformer):
    """Standardise and repair Obsidian Mermaid formatting."""

    def transform(self, content: str) -> str:
        """Apply the fixers to every ```mermaid``` block in ``content``."""
        return _RE_MERMAID_BLOCK.sub(
            lambda match: self._fix_block(match.group(0)),
            content,
        )

    @staticmethod
    def _fix_block(block: str) -> str:
        """Apply the three per-line fixers to a single Mermaid block."""
        fixed_lines = []
        for line in block.split("\n"):
            # 1. Quotify unquoted subgraph label:
            #    "subgraph Name [Label]" -> "subgraph Name[\"Label\"]"
            line = re.sub(
                r'^(\s*subgraph\s+\w+)\s+\[([^"([][^\]]*)\]',
                r'\1["\2"]',
                line,
            )
            # 2. Quotify unquoted node label:
            #    "Node[Label]" -> "Node[\"Label\"]"
            line = re.sub(
                r'(?<![a-zA-Z0-9_])([a-zA-Z_][a-zA-Z0-9_-]*)\[([^"([\]]+)\]',
                r'\1["\2"]',
                line,
            )
            # 3. Rewrite ordered-list triggers inside quoted strings to
            #    avoid Markdown pre-processing conflicts.
            line = re.sub(r'"(\d)\.\s+', r'"\1: ', line)
            line = re.sub(r'\|(\d)\.\s+', r'|\1: ', line)
            fixed_lines.append(line)
        return "\n".join(fixed_lines)


class RegexReplacer(IContentTransformer):
    """Apply a list of ``find``/``replace`` regex pairs in order."""

    def __init__(self, patterns: List[Dict[str, str]]):
        self.replacements = [
            (re.compile(p["find"]), p["replace"]) for p in patterns
        ]

    def transform(self, content: str) -> str:
        for pattern, replacement in self.replacements:
            content = pattern.sub(replacement, content)
        return content
