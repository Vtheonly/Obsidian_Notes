"""
Abstract Interface Definitions.
Establishes clear behavioral contracts for all major processing layers,
ensuring complete decoupling from specific folder shapes or structures.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from vault_manager.core.models import ParsedSegment, ValidationReport


class IDocumentParser(ABC):
    """Interface for parsing monolithic markdown files into structured segments."""

    @abstractmethod
    def parse(self, content: str, options: Dict[str, Any]) -> List[ParsedSegment]:
        """Parses raw text into a list of structured document segments."""
        pass


class IContentTransformer(ABC):
    """Interface for modifying and cleaning file content."""

    @abstractmethod
    def transform(self, content: str) -> str:
        """Applies transformation logic to the content, returning the modified string."""
        pass


class IValidationStrategy(ABC):
    """Interface for validating file structures and syntax."""

    @abstractmethod
    def validate(self, filepath: str) -> ValidationReport:
        """Validates a file, returning a structured verification report."""
        pass


class IMergeStrategy(ABC):
    """Interface for merging extracted segments into existing file systems."""

    @abstractmethod
    def merge(self, segments: List[ParsedSegment], target_dir: str, options: Dict[str, Any]) -> int:
        """Merges parsed segments into a target folder path, returning files written count."""
        pass


class IRenamingStrategy(ABC):
    """Interface for implementing safe, collision-resistant renaming behaviors."""

    @abstractmethod
    def generate_mapping(self, current_files: List[str], options: Dict[str, Any]) -> Dict[str, str]:
        """Generates an old-to-new filename mapping based on target rules."""
        pass