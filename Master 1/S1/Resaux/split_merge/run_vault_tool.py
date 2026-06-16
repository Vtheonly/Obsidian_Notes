#!/usr/bin/env python3
"""
Unified Vault Manager Command-Line Interface.
Orchestrates split, merge, validation, transformation, and renaming operations
by consuming the declarative config.yaml specifications.
"""

import os
import sys
import yaml
import argparse
from typing import Dict, Any

from vault_manager.logging import logger
from vault_manager.exceptions import VaultManagerException, ConfigurationError
from vault_manager.utils.file_ops import read_file_safely, write_file_safely, compress_directory_to_zip
from vault_manager.services.splitter import DynamicRegexParser
from vault_manager.services.merger import FlexibleMerger
from vault_manager.services.transformer import MermaidFixer
from vault_manager.services.validator import ObsidianQuizValidator
from vault_manager.services.renamer import MapRenamer, RegexPatternRenamer
from vault_manager.services.purge_emojis import EmojiPurgeService
from vault_manager.utils.file_ops import atomic_two_phase_rename


def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """Safely parses and loads the YAML configuration file."""
    if not os.path.exists(config_path):
        raise ConfigurationError(f"Target configuration file not found at: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        raise ConfigurationError(f"Failed parsing YAML configuration: {e}")


def handle_split(args, config: Dict[str, Any]) -> int:
    """Executes the split pipeline using configured regex parser strategies."""
    logger.section("Pipeline: Document Splitter")
    
    pipeline_name = args.pipeline
    split_configs = config.get("split", {})
    if pipeline_name not in split_configs:
        raise ConfigurationError(f"No split pipeline matching '{pipeline_name}' found in config.yaml")

    p_conf = split_configs[pipeline_name]
    input_file = p_conf.get("input_file", "Vault 1.md")
    output_dir = p_conf.get("output_dir", "Course")
    zip_name = p_conf.get("zip_name", "Course.zip")

    if not os.path.exists(input_file):
        logger.error(f"Target split source file not found: {input_file}")
        return 1

    content = read_file_safely(input_file)
    parser = DynamicRegexParser()
    
    logger.info(f"Parsing document '{input_file}' via regex strategies...")
    segments = parser.parse(content, p_conf)
    logger.success(f"Successfully parsed {len(segments)} segments.")

    # Clean up previous runs
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)

    # Write files
    for segment in segments:
        dest_folder = os.path.join(output_dir, segment.folder)
        dest_filepath = os.path.join(dest_folder, segment.filename)
        write_file_safely(dest_filepath, segment.content)

    logger.info(f"Packaging processed directory into '{zip_name}'...")
    compress_directory_to_zip(output_dir, zip_name, archive_prefix=output_dir)
    
    import shutil
    shutil.rmtree(output_dir)
    logger.success("Temporal directory cleared. Split transaction complete.")
    return 0


def handle_merge(args, config: Dict[str, Any]) -> int:
    """Executes the merge pipeline using non-destructive file collision strategies."""
    logger.section("Pipeline: Non-destructive Merger")

    pipeline_name = args.pipeline
    merge_configs = config.get("merge", {})
    if pipeline_name not in merge_configs:
        raise ConfigurationError(f"No merge pipeline matching '{pipeline_name}' found in config.yaml")

    m_conf = merge_configs[pipeline_name]
    input_file = m_conf.get("input_file", "Vault 1.md")
    workspace_path = m_conf.get("workspace_path", ".")
    backup_zip = m_conf.get("backup_zip", "Merged_Course.zip")

    if not os.path.exists(input_file):
        logger.error(f"Target source file for merge not found: {input_file}")
        return 1

    # First, split the incoming file into raw segments using the matching split configuration
    split_configs = config.get("split", {})
    if pipeline_name not in split_configs:
        raise ConfigurationError(f"Automatic splitting requires a matching split pipeline '{pipeline_name}'")
    
    p_conf = split_configs[pipeline_name]
    content = read_file_safely(input_file)
    parser = DynamicRegexParser()
    segments = parser.parse(content, p_conf)

    # Now, run the merge strategy
    merger = FlexibleMerger()
    logger.info(f"Merging {len(segments)} segments into workspace: '{workspace_path}'...")
    written_count = merger.merge(segments, workspace_path, m_conf)
    
    logger.success(f"Completed writing {written_count} files into the workspace.")
    return 0


def handle_fix_mermaid(args, config: Dict[str, Any]) -> int:
    """Executes the content transformer to repair broken Mermaid diagrams."""
    logger.section("Pipeline: Mermaid Reformatter")

    target_dir = args.directory
    if not os.path.exists(target_dir):
        logger.error(f"Target path does not exist: {target_dir}")
        return 1

    fixer = MermaidFixer()
    modified_count = 0

    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                content = read_file_safely(file_path)
                fixed_content = fixer.transform(content)
                if fixed_content != content:
                    logger.info(f"    - Cleaned and updated: {os.path.relpath(file_path, target_dir)}")
                    write_file_safely(file_path, fixed_content)
                    modified_count += 1

    logger.success(f"Mermaid formatting complete. Cleaned and saved {modified_count} files.")
    return 0


def handle_validate(args, config: Dict[str, Any]) -> int:
    """Invokes semantic validation checks on targeted markdown files."""
    logger.section("Pipeline: Semantic Validator")

    target_paths = args.paths if args.paths else ["."]
    validator = ObsidianQuizValidator()
    
    files_to_check = []
    for path in target_paths:
        if os.path.isfile(path) and path.endswith(".md"):
            files_to_check.append(path)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith(".md"):
                        files_to_check.append(os.path.join(root, f))

    if not files_to_check:
        logger.warning("No markdown (.md) documents located to validate.")
        return 0

    valid_count = 0
    for f in files_to_check:
        report = validator.validate(f)
        if report.is_valid:
            logger.success(f"Valid: {os.path.basename(f)}")
            logger.info(f"  - Stats: {report.stats}")
            valid_count += 1
        else:
            logger.error(f"Invalid: {os.path.basename(f)}")
            for line, err in report.errors:
                logger.error(f"    Line ~{line}: {err}")
            for line, warn in report.warnings:
                logger.warning(f"    Line ~{line}: {warn}")

    total = len(files_to_check)
    logger.section("Summary Report")
    logger.info(f"Validated files: {total}")
    logger.info(f"Passed:          {valid_count}")
    logger.info(f"Failed:          {total - valid_count}")

    return 0 if valid_count == total else 1


def handle_rename(args, config: Dict[str, Any]) -> int:
    """Executes safe, transactional renames using the target strategy."""
    logger.section("Pipeline: Safe Atomic Renamer")

    pipeline_name = args.pipeline
    rename_configs = config.get("rename", {})
    if pipeline_name not in rename_configs:
        raise ConfigurationError(f"No rename pipeline matching '{pipeline_name}' found in config.yaml")

    r_conf = rename_configs[pipeline_name]
    target_dir = r_conf.get("target_dir", ".")
    strategy_type = r_conf.get("strategy", "map")

    if not os.path.exists(target_dir):
        logger.error(f"Target directory does not exist: {target_dir}")
        return 1

    current_files = [f for f in os.listdir(target_dir) if f.endswith(".md")]

    if strategy_type == "map":
        renamer = MapRenamer()
    elif strategy_type == "regex_pattern":
        renamer = RegexPatternRenamer()
    else:
        raise ConfigurationError(f"Unknown renaming strategy: {strategy_type}")

    logger.info(f"Computing target naming mapping using strategy '{strategy_type}'...")
    mapping = renamer.generate_mapping(current_files, r_conf)

    if not mapping:
        logger.warning("No matching files found to rename.")
        return 0

    logger.info(f"Initiating atomic transaction for {len(mapping)} files...")
    atomic_two_phase_rename(target_dir, mapping)
    logger.success("Renaming transactions committed safely.")
    return 0


def handle_purge_emojis(args, config: Dict[str, Any]) -> int:
    """Executes recursive emoji removal from text files in a directory."""
    logger.section("Pipeline: Emoji Purge Service")

    target_dir = args.directory
    if not os.path.exists(target_dir):
        logger.error(f"Target path does not exist: {target_dir}")
        return 1

    purge_service = EmojiPurgeService()
    files_scanned = 0
    files_modified = 0
    total_removed = 0

    logger.info(f"Scanning directory '{target_dir}' for text files with emojis...")
    
    for root, dirs, files in os.walk(target_dir):
        # Skip hidden directories and common non-vault dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', '.venv')]
        
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            
            if not EmojiPurgeService.is_text_file(filepath):
                continue

            files_scanned += 1
            try:
                content = read_file_safely(filepath)
                emoji_count = EmojiPurgeService.count_emojis(content)
                if emoji_count == 0:
                    continue
                
                cleaned = purge_service.transform(content)
                write_file_safely(filepath, cleaned)
                files_modified += 1
                total_removed += emoji_count
                relpath = os.path.relpath(filepath, target_dir)
                logger.info(f"    - Purged {emoji_count} emoji chars from: {relpath}")
            except Exception as e:
                logger.warning(f"    - Could not process '{os.path.basename(filepath)}': {e}")

    logger.success(f"Emoji purge complete. Scanned {files_scanned} files, modified {files_modified}, removed {total_removed} emoji chars.")
    return 0


def main() -> int:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        description="Dynamic Obsidian Vault Management System"
    )
    parser.add_argument(
        "--config", default="config.yaml", help="Path to the config.yaml file"
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Sub-commands")

    # Split
    split_p = subparsers.add_parser("split", help="Split a file into directory segments")
    split_p.add_argument("pipeline", help="Name of the split pipeline from config.yaml")
    split_p.set_defaults(func=handle_split)

    # Merge
    merge_p = subparsers.add_parser("merge", help="Merge structured files into a target workspace")
    merge_p.add_argument("pipeline", help="Name of the merge pipeline from config.yaml")
    merge_p.set_defaults(func=handle_merge)

    # Fix Mermaid
    mermaid_p = subparsers.add_parser("fix-mermaid", help="Fix formatting issues in Mermaid blocks")
    mermaid_p.add_argument("-d", "--directory", default=".", help="Root directory to scan")
    mermaid_p.set_defaults(func=handle_fix_mermaid)

    # Purge Emojis
    purge_p = subparsers.add_parser("purge-emojis", help="Remove all emoji characters from text files in a directory")
    purge_p.add_argument("-d", "--directory", default=".", help="Root directory to scan recursively")
    purge_p.set_defaults(func=handle_purge_emojis)

    # Validate
    validate_p = subparsers.add_parser("validate", help="Validate quiz structures and formatting")
    validate_p.add_argument("paths", nargs="*", default=[], help="Paths to check")
    validate_p.set_defaults(func=handle_validate)

    # Rename
    rename_p = subparsers.add_parser("rename", help="Perform safe transactional renames")
    rename_p.add_argument("pipeline", help="Name of the rename pipeline from config.yaml")
    rename_p.set_defaults(func=handle_rename)

    args = parser.parse_args()

    try:
        config = load_yaml_config(args.config)
        return args.func(args, config)
    except VaultManagerException as ve:
        logger.error(f"System execution failed: {ve}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected system crash: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())