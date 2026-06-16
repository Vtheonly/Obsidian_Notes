"""
Custom domain exceptions for the Vault Manager architecture.
Used to enforce robust error handling and precise fault diagnostics.
"""

class VaultManagerException(Exception):
    """Base exception class for all vault manager operations."""
    pass


class FileSystemError(VaultManagerException):
    """Raised when low-level filesystem or I/O operations fail."""
    pass


class ConfigurationError(VaultManagerException):
    """Raised when invalid configuration schemas are supplied."""
    pass


class ParserError(VaultManagerException):
    """Raised when parsing or tokenizing document formats fails."""
    pass


class ValidationError(VaultManagerException):
    """Raised when validation constraints are violated."""
    pass


class RenamingError(VaultManagerException):
    """Raised when renaming operations encounter unsafe states or collisions."""
    pass


class TransactionAborted(VaultManagerException):
    """Raised when an active transaction is aborted and rolled back."""
    pass