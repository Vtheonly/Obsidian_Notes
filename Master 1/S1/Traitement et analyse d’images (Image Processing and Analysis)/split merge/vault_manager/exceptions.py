"""
Custom domain exceptions for the Vault Manager architecture.
Used to enforce structured error handling and distinct traceback separation.
"""

class VaultManagerError(Exception):
    """Base exception class for all vault manager operations."""
    pass


class FileOperationError(VaultManagerError):
    """Raised when file I/O, directory creations, or backups fail."""
    pass


class ParsingError(VaultManagerError):
    """Raised during document parsing, markdown decomposition, or extraction."""
    pass


class ValidationError(VaultManagerError):
    """Raised when an asset or quiz file violates formatting expectations."""
    pass


class RenamingCollisionError(VaultManagerError):
    """Raised when physical file renaming operations risk overwrites or collisions."""
    pass