"""
Domain models and structured value objects.
Promotes safe static typing and explicit object architectures.
"""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class ParsedSection:
    """Value object representing a parsed markdown page or subsection."""
    folder: str
    filename: str
    content: str


@dataclass
class QuizQuestionStats:
    """Encapsulates question classification results for a quiz document."""
    true_false: int = 0
    multiple_choice: int = 0
    matching: int = 0

    def total(self) -> int:
        """Computes structural sum of all questions classified."""
        return self.true_false + self.multiple_choice + self.matching


@dataclass
class QuizValidationResult:
    """Represents full diagnostic outputs of a single quiz evaluation."""
    filepath: str
    is_valid: bool
    stats: QuizQuestionStats = field(default_factory=QuizQuestionStats)
    errors: List[tuple] = field(default_factory=list)  # (line_number, error_message)
    warnings: List[tuple] = field(default_factory=list)  # (line_number, warning_message)