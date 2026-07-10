"""
Abstract interface definitions for the major processing layers.

Each interface establishes a behavioural contract that the corresponding
service implementation must satisfy. Decoupling interfaces from
implementations lets the CLI orchestrate services polymorphically (e.g.
``MapRenamer`` vs ``RegexPatternRenamer`` both satisfy ``IRenamingStrategy``).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from vault_manager.core.models import ParsedSegment, ValidationReport


class IDocumentParser(ABC):
    """Parses a monolithic Markdown file into structured segments."""

    @abstractmethod
    def parse(self, content: str, options: Dict[str, Any]) -> List[ParsedSegment]:
        """Parse raw text into a list of structured document segments."""


class IContentTransformer(ABC):
    """Modifies or cleans file content."""

    @abstractmethod
    def transform(self, content: str) -> str:
        """Apply transformation logic and return the modified string."""


class IValidationStrategy(ABC):
    """Validates file structure and syntax."""

    @abstractmethod
    def validate(self, filepath: str) -> ValidationReport:
        """Validate a file and return a structured verification report."""


class IMergeStrategy(ABC):
    """Merges extracted segments into an existing filesystem tree."""

    @abstractmethod
    def merge(
        self,
        segments: List[ParsedSegment],
        target_dir: str,
        options: Dict[str, Any],
    ) -> int:
        """Merge parsed segments into ``target_dir`` and return files written."""


class IRenamingStrategy(ABC):
    """Generates safe, collision-resistant filename mappings."""

    @abstractmethod
    def generate_mapping(
        self,
        current_files: List[str],
        options: Dict[str, Any],
    ) -> Dict[str, str]:
        """Generate an old-to-new filename mapping based on configured rules."""
