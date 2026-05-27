"""
Interface design abstractions.
Defines processing contracts to enable robust, mockable, and easily extendable services.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class FileProcessor(ABC):
    """Generic interface for file operations and transformations."""

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Executes the specialized processing logic of the implementing service."""
        pass


class ContentValidator(ABC):
    """Generic interface for standard structural validations."""

    @abstractmethod
    def validate(self, filepath: str) -> bool:
        """Validates file contents against rules, returning True if valid."""
        pass