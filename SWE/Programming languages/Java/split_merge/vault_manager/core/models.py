"""
Domain models and structured data representations.

These dataclasses enforce static typing and encapsulate system-wide data
states passed between the CLI, services, and utils layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple


@dataclass
class ParsedSegment:
    """An extracted Markdown section ready to be written to disk.

    Attributes:
        folder: relative folder path (may contain ``/`` separators).
        filename: target filename (including extension).
        content: full file body (already stripped of leading/trailing
            ``---`` frontmatter markers if present in the segment).
        metadata: optional bag for parser-specific extras.
    """

    folder: str
    filename: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationReport:
    """Diagnostic snapshot returned by ``IValidationStrategy.validate``.

    Attributes:
        filepath: path that was validated.
        is_valid: overall pass/fail flag.
        errors: list of ``(line_number, message)`` tuples for hard errors.
        warnings: list of ``(line_number, message)`` tuples for soft warnings.
        stats: arbitrary counters (e.g. per-question-type counts).
    """

    filepath: str
    is_valid: bool
    errors: List[Tuple[int, str]] = field(default_factory=list)
    warnings: List[Tuple[int, str]] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)
