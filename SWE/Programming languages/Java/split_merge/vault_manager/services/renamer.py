"""
Flexible sequential renaming services.

Two strategies are provided, both implementing :class:`IRenamingStrategy`:

* :class:`MapRenamer` — applies a strict old-name -> new-name dictionary
  provided in the config. Files not listed in the mapping are left alone.
* :class:`RegexPatternRenamer` — matches each existing filename against a
  configurable regex and interpolates capture groups into a format string
  to produce the new name. Useful when files follow a naming convention
  (e.g. ``Lesson 01 - Intro.md`` -> ``01. Intro.md``).

Both strategies return a ``{old_name: new_name}`` mapping that is then
applied atomically by :func:`vault_manager.services.rename_transaction.atomic_two_phase_rename`.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

from vault_manager.core.interfaces import IRenamingStrategy
from vault_manager.exceptions import RenamingError


class MapRenamer(IRenamingStrategy):
    """Map filenames using a strict old-name -> new-name dictionary."""

    def generate_mapping(
        self,
        current_files: List[str],
        options: Dict[str, Any],
    ) -> Dict[str, str]:
        """Return ``{old: new}`` for every key in the mapping that exists on disk."""
        mapping_dict: Dict[str, str] = options.get("mapping", {})
        if not mapping_dict:
            raise RenamingError("No mapping dictionary provided in options.")

        # Keep only files that exist in current_files (preserves original order
        # of the mapping_dict, which is insertion order in Python 3.7+).
        return {k: v for k, v in mapping_dict.items() if k in current_files}


class RegexPatternRenamer(IRenamingStrategy):
    """Generate new filenames by regex-matching the existing ones."""

    def generate_mapping(
        self,
        current_files: List[str],
        options: Dict[str, Any],
    ) -> Dict[str, str]:
        """Return ``{old: new}`` for every file whose name matches the pattern."""
        pattern_str = options.get("pattern", "")
        replacement_format = options.get("format", "")

        if not pattern_str or not replacement_format:
            raise RenamingError(
                "Pattern and format string are required for RegexPatternRenamer."
            )

        try:
            compiled_pattern = re.compile(pattern_str)
        except Exception as exc:
            raise RenamingError(f"Invalid regex pattern: {exc}")

        mapping: Dict[str, str] = {}
        for filename in current_files:
            match = compiled_pattern.match(filename)
            if not match:
                continue

            # Build the substitution context. Numbered groups become g1, g2, ...;
            # named groups are also exposed by their name.
            context: Dict[str, str] = {}
            for i, group in enumerate(match.groups()):
                if group is not None:
                    context[f"g{i + 1}"] = group.strip()
            for name, value in match.groupdict().items():
                if value is not None:
                    context[name] = value.strip()

            try:
                new_name = replacement_format.format(**context)
            except KeyError as ke:
                raise RenamingError(
                    f"Formatting failed for file '{filename}'. Missing key: {ke}"
                )

            # Preserve the .md extension if the original had it and the
            # replacement doesn't already end with .md.
            if not new_name.endswith(".md") and filename.endswith(".md"):
                new_name += ".md"

            mapping[filename] = new_name

        return mapping
