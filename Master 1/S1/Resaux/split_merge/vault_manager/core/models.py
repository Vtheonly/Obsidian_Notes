"""
Domain models and structured data representations.
Enforces static typing and encapsulation of system-wide data states.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class ParsedSegment:
    """Encapsulates an extracted markdown file section ready for writing."""
    folder: str
    filename: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationReport:
    """Diagnostic metrics of a validated file."""
    filepath: str
    is_valid: bool
    errors: List[tuple] = field(default_factory=list)  # List of tuples (line_number, message)
    warnings: List[tuple] = field(default_factory=list)  # List of tuples (line_number, message)
    stats: Dict[str, int] = field(default_factory=dict)