"""Core abstractions module initializer."""

from vault_manager.core.interfaces import (
    IDocumentParser,
    IContentTransformer,
    IValidationStrategy,
    IMergeStrategy,
    IRenamingStrategy,
)
from vault_manager.core.models import ParsedSegment, ValidationReport

__all__ = [
    "IDocumentParser",
    "IContentTransformer",
    "IValidationStrategy",
    "IMergeStrategy",
    "IRenamingStrategy",
    "ParsedSegment",
    "ValidationReport",
]
