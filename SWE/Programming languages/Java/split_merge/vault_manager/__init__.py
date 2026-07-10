"""
Vault Manager Package.
A modular, extensible system to process, partition, merge, validate, and
transform arbitrary Markdown vault structures.

The package is organised in three layers:

* ``vault_manager.core`` — abstract interfaces and dataclass models.
* ``vault_manager.services`` — concrete implementations of each service
  (splitter, merger, validator, renamer, transformer, purge, and the
  transactional rename helper).
* ``vault_manager.utils`` — generic file-system utilities shared across
  services.

A thin CLI dispatcher lives in ``vault_manager.cli``; the project entry
point is ``run_vault_tool.py``.
"""

__version__ = "2.0.0"
