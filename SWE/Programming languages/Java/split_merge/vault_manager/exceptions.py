"""
Custom domain exceptions for the Vault Manager architecture.

Exception hierarchy:

    VaultManagerException                 (base, catch-all)
    ├── FileSystemError                   low-level I/O failures
    ├── ConfigurationError                invalid config.yaml schema
    ├── ParserError                       document parsing / tokenisation
    ├── ValidationError                   validation constraint violation
    ├── RenamingError                     unsafe rename / collision
    └── TransactionAborted                two-phase rename rolled back

All exceptions inherit from :class:`VaultManagerException`, so callers can
catch any vault-manager failure with a single ``except`` clause.
"""

from __future__ import annotations


class VaultManagerException(Exception):
    """Base exception for all vault_manager operations."""


class FileSystemError(VaultManagerException):
    """Raised when low-level filesystem or I/O operations fail."""


class ConfigurationError(VaultManagerException):
    """Raised when an invalid configuration schema is supplied."""


class ParserError(VaultManagerException):
    """Raised when parsing or tokenising a document fails."""


class ValidationError(VaultManagerException):
    """Raised when a validation constraint is violated."""


class RenamingError(VaultManagerException):
    """Raised when a rename operation encounters an unsafe state or collision."""


class TransactionAborted(VaultManagerException):
    """Raised when an in-flight transaction is aborted and rolled back."""
