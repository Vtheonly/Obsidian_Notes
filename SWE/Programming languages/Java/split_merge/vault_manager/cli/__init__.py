"""
CLI subpackage — command handlers for the vault_manager tool.

Each ``handle_*`` function implements one CLI subcommand. They are kept
thin: parsing CLI args, loading the YAML config, and orchestrating the
service-layer calls. All business logic lives in ``vault_manager.services``.

The handlers are imported by ``run_vault_tool.py`` (the entry point) and
registered as ``argparse`` subparser callbacks.
"""

from vault_manager.cli.handlers import (
    handle_split,
    handle_merge,
    handle_fix_mermaid,
    handle_validate,
    handle_rename,
    handle_purge_emojis,
    load_yaml_config,
)

__all__ = [
    "handle_split",
    "handle_merge",
    "handle_fix_mermaid",
    "handle_validate",
    "handle_rename",
    "handle_purge_emojis",
    "load_yaml_config",
]
