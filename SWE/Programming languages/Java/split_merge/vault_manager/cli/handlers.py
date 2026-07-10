"""
Command handlers for the vault_manager CLI.

Each handler has the signature ``handle_X(args, config) -> int`` and
returns a process exit code (0 = success, non-zero = failure). They are
registered as argparse subparser callbacks by ``run_vault_tool.py``.

The handlers are deliberately thin: they parse ``args``, look up the
relevant pipeline config, and delegate to the service layer. All
business logic lives in ``vault_manager.services``.
"""

from __future__ import annotations

import os
import shutil
from typing import Any, Dict

from vault_manager.exceptions import ConfigurationError
from vault_manager.logging import logger
from vault_manager.services.merger import FlexibleMerger
from vault_manager.services.purge_emojis import EmojiPurgeService
from vault_manager.services.renamer import MapRenamer, RegexPatternRenamer
from vault_manager.services.rename_transaction import atomic_two_phase_rename
from vault_manager.services.splitter import DynamicRegexParser
from vault_manager.services.transformer import MermaidFixer
from vault_manager.services.validator import ObsidianQuizValidator
from vault_manager.utils.file_ops import (
    compress_directory_to_zip,
    read_file_safely,
    write_file_safely,
)


# ---------------------------------------------------------------------------
# Config loader
# ---------------------------------------------------------------------------

def load_yaml_config(config_path: str) -> Dict[str, Any]:
    """Parse and return the YAML config at ``config_path``.

    Raises :class:`ConfigurationError` if the file is missing or invalid.
    """
    if not os.path.exists(config_path):
        raise ConfigurationError(
            f"Target configuration file not found at: {config_path}"
        )
    import yaml
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as exc:
        raise ConfigurationError(f"Failed parsing YAML configuration: {exc}")


# ---------------------------------------------------------------------------
# Helpers shared across handlers
# ---------------------------------------------------------------------------

def _require_pipeline(
    pipeline_name: str,
    pipeline_configs: Dict[str, Any],
    section: str,
) -> Dict[str, Any]:
    """Look up a pipeline config by name. Raise ConfigurationError if missing."""
    if pipeline_name not in pipeline_configs:
        raise ConfigurationError(
            f"No {section} pipeline matching '{pipeline_name}' found in config.yaml"
        )
    return pipeline_configs[pipeline_name]


def _iter_markdown_files(target_dir: str):
    """Yield absolute paths of every ``.md`` file under ``target_dir``."""
    for root, _dirs, files in os.walk(target_dir):
        for filename in files:
            if filename.endswith(".md"):
                yield os.path.join(root, filename)


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

def handle_split(args, config: Dict[str, Any]) -> int:
    """Execute the split pipeline using the configured regex parser strategy."""
    logger.section("Pipeline: Document Splitter")

    p_conf = _require_pipeline(args.pipeline, config.get("split", {}), "split")
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

    # Clean up previous runs.
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Write each segment to disk.
    for segment in segments:
        dest_folder = os.path.join(output_dir, segment.folder)
        dest_filepath = os.path.join(dest_folder, segment.filename)
        write_file_safely(dest_filepath, segment.content)

    logger.info(f"Packaging processed directory into '{zip_name}'...")
    compress_directory_to_zip(output_dir, zip_name, archive_prefix=output_dir)

    shutil.rmtree(output_dir)
    logger.success("Temporal directory cleared. Split transaction complete.")
    return 0


def handle_merge(args, config: Dict[str, Any]) -> int:
    """Execute the merge pipeline using non-destructive collision strategies."""
    logger.section("Pipeline: Non-destructive Merger")

    m_conf = _require_pipeline(args.pipeline, config.get("merge", {}), "merge")
    input_file = m_conf.get("input_file", "Vault 1.md")
    workspace_path = m_conf.get("workspace_path", ".")

    if not os.path.exists(input_file):
        logger.error(f"Target source file for merge not found: {input_file}")
        return 1

    # First, split the incoming file into raw segments using the matching
    # split configuration (mirrors the original behaviour).
    p_conf = _require_pipeline(
        args.pipeline, config.get("split", {}), "split"
    )
    content = read_file_safely(input_file)
    parser = DynamicRegexParser()
    segments = parser.parse(content, p_conf)

    merger = FlexibleMerger()
    logger.info(
        f"Merging {len(segments)} segments into workspace: '{workspace_path}'..."
    )
    written_count = merger.merge(segments, workspace_path, m_conf)

    logger.success(f"Completed writing {written_count} files into the workspace.")
    return 0


def handle_fix_mermaid(args, config: Dict[str, Any]) -> int:
    """Execute the content transformer to repair broken Mermaid diagrams."""
    logger.section("Pipeline: Mermaid Reformatter")

    target_dir = args.directory
    if not os.path.exists(target_dir):
        logger.error(f"Target path does not exist: {target_dir}")
        return 1

    fixer = MermaidFixer()
    modified_count = 0

    for file_path in _iter_markdown_files(target_dir):
        content = read_file_safely(file_path)
        fixed_content = fixer.transform(content)
        if fixed_content != content:
            logger.info(
                f"    - Cleaned and updated: {os.path.relpath(file_path, target_dir)}"
            )
            write_file_safely(file_path, fixed_content)
            modified_count += 1

    logger.success(
        f"Mermaid formatting complete. Cleaned and saved {modified_count} files."
    )
    return 0


def handle_validate(args, config: Dict[str, Any]) -> int:
    """Invoke semantic validation checks on targeted Markdown files."""
    logger.section("Pipeline: Semantic Validator")

    target_paths = args.paths if args.paths else ["."]
    validator = ObsidianQuizValidator()

    files_to_check: list = []
    for path in target_paths:
        if os.path.isfile(path) and path.endswith(".md"):
            files_to_check.append(path)
        elif os.path.isdir(path):
            for root, _dirs, files in os.walk(path):
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
    """Execute a safe, transactional rename using the configured strategy."""
    logger.section("Pipeline: Safe Atomic Renamer")

    r_conf = _require_pipeline(args.pipeline, config.get("rename", {}), "rename")
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

    logger.info(
        f"Computing target naming mapping using strategy '{strategy_type}'..."
    )
    mapping = renamer.generate_mapping(current_files, r_conf)

    if not mapping:
        logger.warning("No matching files found to rename.")
        return 0

    logger.info(f"Initiating atomic transaction for {len(mapping)} files...")
    atomic_two_phase_rename(target_dir, mapping)
    logger.success("Renaming transactions committed safely.")
    return 0


def handle_purge_emojis(args, config: Dict[str, Any]) -> int:
    """Recursively remove emoji characters from text files in a directory."""
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
        # Skip hidden directories and common non-vault dirs.
        dirs[:] = [
            d for d in dirs
            if not d.startswith(".")
            and d not in ("node_modules", "__pycache__", "venv", ".venv")
        ]

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
                logger.info(
                    f"    - Purged {emoji_count} emoji chars from: {relpath}"
                )
            except Exception as exc:
                logger.warning(
                    f"    - Could not process '{os.path.basename(filepath)}': {exc}"
                )

    logger.success(
        f"Emoji purge complete. Scanned {files_scanned} files, "
        f"modified {files_modified}, removed {total_removed} emoji chars."
    )
    return 0
