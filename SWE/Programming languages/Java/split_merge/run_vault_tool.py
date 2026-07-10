#!/usr/bin/env python3
"""
Unified Vault Manager command-line interface.

Entry point for the ``split``, ``merge``, ``fix-mermaid``, ``purge-emojis``,
``validate``, and ``rename`` subcommands. Each subcommand is implemented by
a handler in :mod:`vault_manager.cli.handlers`; this file only wires up
``argparse`` and dispatches to the selected handler.

Run ``python run_vault_tool.py --help`` for the list of subcommands.
"""

from __future__ import annotations

import argparse
import sys
import traceback

from vault_manager.cli.handlers import (
    handle_fix_mermaid,
    handle_merge,
    handle_purge_emojis,
    handle_rename,
    handle_split,
    handle_validate,
    load_yaml_config,
)
from vault_manager.exceptions import VaultManagerException
from vault_manager.logging import logger


def _build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argparse parser with all subcommands."""
    parser = argparse.ArgumentParser(
        description="Dynamic Obsidian Vault Management System"
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to the config.yaml file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands")

    # split -----------------------------------------------------------------
    split_p = subparsers.add_parser(
        "split", help="Split a file into directory segments"
    )
    split_p.add_argument(
        "pipeline", help="Name of the split pipeline from config.yaml"
    )
    split_p.set_defaults(func=handle_split)

    # merge -----------------------------------------------------------------
    merge_p = subparsers.add_parser(
        "merge", help="Merge structured files into a target workspace"
    )
    merge_p.add_argument(
        "pipeline", help="Name of the merge pipeline from config.yaml"
    )
    merge_p.set_defaults(func=handle_merge)

    # fix-mermaid -----------------------------------------------------------
    mermaid_p = subparsers.add_parser(
        "fix-mermaid", help="Fix formatting issues in Mermaid blocks"
    )
    mermaid_p.add_argument(
        "-d", "--directory", default=".", help="Root directory to scan"
    )
    mermaid_p.set_defaults(func=handle_fix_mermaid)

    # purge-emojis ----------------------------------------------------------
    purge_p = subparsers.add_parser(
        "purge-emojis",
        help="Remove all emoji characters from text files in a directory",
    )
    purge_p.add_argument(
        "-d", "--directory", default=".", help="Root directory to scan recursively"
    )
    purge_p.set_defaults(func=handle_purge_emojis)

    # validate --------------------------------------------------------------
    validate_p = subparsers.add_parser(
        "validate", help="Validate quiz structures and formatting"
    )
    validate_p.add_argument(
        "paths", nargs="*", default=[], help="Paths to check"
    )
    validate_p.set_defaults(func=handle_validate)

    # rename ----------------------------------------------------------------
    rename_p = subparsers.add_parser(
        "rename", help="Perform safe transactional renames"
    )
    rename_p.add_argument(
        "pipeline", help="Name of the rename pipeline from config.yaml"
    )
    rename_p.set_defaults(func=handle_rename)

    return parser


def main() -> int:
    """Application entry point. Returns a process exit code."""
    parser = _build_parser()
    args = parser.parse_args()

    try:
        config = load_yaml_config(args.config)
        return args.func(args, config)
    except VaultManagerException as exc:
        logger.error(f"System execution failed: {exc}")
        return 1
    except Exception as exc:
        logger.error(f"Unexpected system crash: {exc}")
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())
