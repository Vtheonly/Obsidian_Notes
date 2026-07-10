"""
Document splitting service.

``DynamicRegexParser`` is a generic, configurable Markdown splitter. Given a
list of regular-expression rules and format strings, it walks the input
document line-by-line. Each time a rule matches, the current accumulated
content is flushed as a ``ParsedSegment`` (using the rule's interpolated
folder/file format strings), and accumulation restarts with the matched
line as the first entry.

This makes the parser adaptable to any heading scheme
(``# Chapter 1``, ``## 1.1 Topic``, ``Section A``, etc.) without code
changes — only the config.yaml rules change.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from vault_manager.core.interfaces import IDocumentParser
from vault_manager.core.models import ParsedSegment
from vault_manager.exceptions import ParserError


# Sentinel used by the default-segment guard. Lifted to module scope so it
# is not redefined on every call.
_DEFAULT_INTRO_FILENAME = "Introduction.md"


class DynamicRegexParser(IDocumentParser):
    """Parse a document sequentially using a configurable list of regexes."""

    def parse(
        self, content: str, options: Dict[str, Any]
    ) -> List[ParsedSegment]:
        """Parse ``content`` according to ``options['rules']``.

        Required option:
            rules: list of dicts with keys ``type``, ``pattern``,
                optional ``folder_format`` and ``file_format``.

        Optional options:
            default_folder: folder name used before the first rule match.
            default_file: filename used before the first rule match
                (default ``"Introduction.md"``).

        Returns:
            List of :class:`ParsedSegment` in document order.
        """
        compiled_rules = self._compile_rules(options.get("rules", []))

        lines = content.split("\n")
        segments: List[ParsedSegment] = []

        # State for the segment currently being accumulated.
        current_folder: str = options.get("default_folder", "")
        current_file: str = options.get("default_file", _DEFAULT_INTRO_FILENAME)
        current_body: List[str] = []

        for line in lines:
            matched_rule = self._find_matching_rule(line, compiled_rules)
            if matched_rule is not None:
                # Flush whatever was accumulated under the previous heading.
                self._flush_segment(
                    segments, current_folder, current_file, current_body
                )
                # Compute the new folder/file from the rule's format strings
                # and the match's capture groups, then start a fresh body
                # beginning with the matched line.
                current_folder, current_file = self._interpolate_targets(
                    matched_rule, line
                )
                current_body = [line]
            else:
                current_body.append(line)

        # Flush the trailing segment.
        self._flush_segment(segments, current_folder, current_file, current_body)
        return segments

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compile_rules(rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compile each rule's regex once for reuse. Raise on invalid input."""
        if not rules:
            raise ParserError("No parsing rules provided in options.")

        compiled: List[Dict[str, Any]] = []
        for rule in rules:
            try:
                compiled.append(
                    {
                        "type": rule["type"],
                        "pattern": re.compile(rule["pattern"], re.MULTILINE),
                        "folder_format": rule.get("folder_format", ""),
                        "file_format": rule.get("file_format", ""),
                    }
                )
            except Exception as exc:
                raise ParserError(
                    f"Invalid regex pattern '{rule.get('pattern')}': {exc}"
                )
        return compiled

    @staticmethod
    def _find_matching_rule(line: str, rules: List[Dict[str, Any]]):
        """Return the first rule whose pattern matches ``line``, or ``None``."""
        for rule in rules:
            if rule["pattern"].match(line):
                return rule
        return None

    @staticmethod
    def _interpolate_targets(rule: Dict[str, Any], line: str):
        """Compute (folder, file) for a matched line by interpolating groups."""
        match = rule["pattern"].match(line)
        # match is guaranteed non-None here (the rule was found by matching).

        # Build the substitution context. Numbered groups become g1, g2, ...;
        # named groups are also exposed by their name.
        groups = match.groups()
        context: Dict[str, str] = {
            f"g{i + 1}": (g.strip() if g else "")
            for i, g in enumerate(groups)
            if g
        }
        for name, value in match.groupdict().items():
            context[name] = value.strip() if value else ""

        # Interpolate folder format (fall back to literal on missing key).
        folder_format = rule["folder_format"]
        if folder_format:
            try:
                folder = folder_format.format(**context)
            except KeyError:
                folder = folder_format
        else:
            folder = ""

        # Interpolate file format (fall back to "Section.md" if absent,
        # then ensure a .md extension).
        file_format = rule["file_format"]
        if file_format:
            try:
                filename = file_format.format(**context)
            except KeyError:
                filename = file_format
        else:
            filename = "Section.md"

        if not filename.endswith(".md"):
            filename += ".md"

        return folder, filename

    @staticmethod
    def _flush_segment(
        segments: List[ParsedSegment],
        folder: str,
        filename: str,
        body_lines: List[str],
    ) -> None:
        """Append a ParsedSegment for the accumulated body, if non-trivial.

        Reproduces the original guard exactly: a segment is emitted only if
        either body is non-empty OR the filename differs from the default
        ``Introduction.md`` sentinel. The body is trimmed of leading/trailing
        whitespace and of leading/trailing ``---`` markers (to handle
        stray frontmatter fragments in the input).
        """
        # Original guard: skip the segment only when BOTH body is empty AND
        # filename is the default intro sentinel.
        if not body_lines and filename == _DEFAULT_INTRO_FILENAME:
            return

        body = "\n".join(body_lines).strip()
        if body.endswith("---"):
            body = body[:-3].strip()
        if body.startswith("---"):
            body = body[3:].strip()

        segments.append(
            ParsedSegment(folder=folder, filename=filename, content=body)
        )
