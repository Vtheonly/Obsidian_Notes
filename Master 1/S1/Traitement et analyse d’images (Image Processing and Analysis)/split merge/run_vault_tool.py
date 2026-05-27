#!/usr/bin/env python3
"""
Vault Manager Command Line Interface.
Provides a unified interface to split documents, merge vaults side-by-side,
standardize Mermaid diagrams, validate quizzes, and rename files.
"""

import sys
import argparse
import os
from vault_manager.logging import logger
from vault_manager.exceptions import VaultManagerError
from vault_manager.services.splitter import VaultSplitter
from vault_manager.services.merger import VaultMerger
from vault_manager.services.mermaid_fixer import MermaidDiagramFixer
from vault_manager.services.quiz_validator import ObsidianQuizValidator
from vault_manager.services.file_renamer import VaultFileRenamer


def handle_split(args) -> int:
    """Invokes the splitting service."""
    logger.section("Document Split Process")
    splitter = VaultSplitter(output_dir=args.output_dir, zip_filepath=args.zip_name)
    splitter.execute(args.input_file)
    return 0


def handle_merge(args) -> int:
    """Invokes the non-destructive merging service."""
    logger.section("Side-by-Side Merging Process")
    merger = VaultMerger(workspace_path=args.workspace)
    merger.execute(vault_filepath=args.input_file, backup_zip_name=args.zip_name)
    return 0


def handle_fix_mermaid(args) -> int:
    """Invokes the Mermaid diagram standardization service."""
    logger.section("Mermaid Diagram Standardizer")
    fixer = MermaidDiagramFixer()
    fixer.execute(vault_root=args.directory)
    return 0


def handle_validate_quiz(args) -> int:
    """Invokes the quiz parsing and validation service."""
    logger.section("Quiz Syntax Callout Validation")
    validator = ObsidianQuizValidator()

    # Determine paths to validate
    paths_to_check = args.paths if args.paths else ["."]
    target_files = []

    for path in paths_to_check:
        if os.path.isfile(path) and path.endswith(".md"):
            target_files.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(".md"):
                        target_files.append(os.path.join(root, f))

    if not target_files:
        logger.warning("No markdown (.md) documents located to validate.")
        return 0

    success_count = 0
    for file in target_files:
        is_valid = validator.validate(file)
        if is_valid:
            success_count += 1

    total_files = len(target_files)
    logger.section("Validation Summary")
    logger.info(f"Files validated: {total_files}")
    logger.info(f"Passed:          {success_count}")
    logger.info(f"Failed:          {total_files - success_count}")

    return 0 if success_count == total_files else 1


def handle_rename(args) -> int:
    """Invokes the transactional sequential renamer."""
    logger.section("Sequential File Renamer")
    renamer = VaultFileRenamer()
    renamer.execute(mapping_type=args.type, target_dir=args.directory)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified system to split, merge, validate, and manage Obsidian notes directories."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-command to execute")

    # Split subparser
    split_parser = subparsers.add_parser("split", help="Split Vault 1.md into chapters and zip them")
    split_parser.add_argument("-i", "--input-file", default="Vault 1.md", help="Path to raw continuous markdown document")
    split_parser.add_argument("-o", "--output-dir", default="Course", help="Temporary directory to parse folders")
    split_parser.add_argument("-z", "--zip-name", default="Course.zip", help="Destination name of compressed zip")
    split_parser.set_defaults(func=handle_split)

    # Merge subparser
    merge_parser = subparsers.add_parser("merge", help="Merge Vault 1.md side-by-side with active folders")
    merge_parser.add_argument("-i", "--input-file", default="Vault 1.md", help="Path to raw continuous markdown document")
    merge_parser.add_argument("-w", "--workspace", default=".", help="Workspace target matching Obsidian root")
    merge_parser.add_argument("-z", "--zip-name", default="Merged_Course.zip", help="Output compressed zip archive")
    merge_parser.set_defaults(func=handle_merge)

    # Fix Mermaid subparser
    mermaid_parser = subparsers.add_parser("fix-mermaid", help="Fix Obsidian Mermaid formatting errors")
    mermaid_parser.add_argument("-d", "--directory", default=".", help="Root search directory to run fixes")
    mermaid_parser.set_defaults(func=handle_fix_mermaid)

    # Quiz validation subparser
    quiz_parser = subparsers.add_parser("validate-quiz", help="Validate Markdown quizzes")
    quiz_parser.add_argument("paths", nargs="*", default=[], help="File paths or folder directories to validate")
    quiz_parser.set_defaults(func=handle_validate_quiz)

    # Renaming subparser
    rename_parser = subparsers.add_parser("rename", help="Run transactional sequential file renames")
    rename_parser.add_argument("-t", "--type", choices=["oop", "automata"], required=True, help="Rename mapping category")
    rename_parser.add_argument("-d", "--directory", default=".", help="Target directory path containing files")
    rename_parser.set_defaults(func=handle_rename)

    args = parser.parse_args()

    try:
        return args.func(args)
    except VaultManagerError as v_err:
        logger.error(f"System operation failed: {v_err}")
        return 1
    except Exception as exc:
        logger.error(f"Unexpected system exception: {exc}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())