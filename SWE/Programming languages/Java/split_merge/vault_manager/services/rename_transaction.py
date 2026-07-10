"""
Transactional two-phase rename helper.

A "two-phase" rename is the safe way to apply a batch of file renames that
may include swaps or cycles (e.g. ``a -> b`` and ``b -> a``). Naive
single-pass renames would either clobber files or fail mid-way, leaving
the directory in an inconsistent state.

Strategy
--------
**Phase 1 (staging):** rename every source file to a temporary name
(``<original>.temp_rename_staging_lock``). If any rename fails, roll back
the staging renames that already succeeded and abort.

**Phase 2 (commit):** rename every staged file to its final destination.
If any rename fails, roll back Phase 2 commits AND Phase 1 staging, then
re-raise.

Pre-flight checks (before Phase 1) catch:
  * source files that do not exist,
  * duplicate destination names,
  * destination files that already exist and are NOT in the mapping
    (which would otherwise be silently overwritten).
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple

from vault_manager.exceptions import FileSystemError, RenamingError
from vault_manager.logging import logger


# Suffix applied during Phase 1 staging. The long, distinctive name makes
# accidental collisions with real files effectively impossible.
TEMP_SUFFIX = ".temp_rename_staging_lock"


def _preflight_checks(target_dir: str, name_mapping: Dict[str, str]) -> None:
    """Validate that the mapping is safe to apply. Raise on any issue."""
    # All source files must exist on disk.
    missing_sources = [
        src for src in name_mapping
        if not os.path.exists(os.path.join(target_dir, src))
    ]
    if missing_sources:
        raise RenamingError(
            f"Pre-checks aborted. Missing target files: {missing_sources}"
        )

    # Destinations must be unique.
    destinations = list(name_mapping.values())
    if len(destinations) != len(set(destinations)):
        raise RenamingError(
            "Pre-checks aborted. Destination mapping contains duplicates."
        )

    # No destination may already exist on disk UNLESS it is also a source
    # being renamed (i.e. part of the mapping).
    unmapped_existing = [
        dst for dst in destinations
        if os.path.exists(os.path.join(target_dir, dst))
        and dst not in name_mapping
    ]
    if unmapped_existing:
        raise RenamingError(
            f"Pre-checks aborted. Unmapped target files already exist: "
            f"{unmapped_existing}"
        )


def _phase1_stage(
    target_dir: str, name_mapping: Dict[str, str]
) -> List[Tuple[str, str]]:
    """Rename every source to ``<source>{TEMP_SUFFIX}``. Return staging records."""
    staged: List[Tuple[str, str]] = []  # (original_name, temp_path)
    try:
        for src in name_mapping:
            original_path = os.path.join(target_dir, src)
            temp_path = os.path.join(target_dir, src + TEMP_SUFFIX)
            os.rename(original_path, temp_path)
            staged.append((src, temp_path))
    except Exception as exc:
        # Roll back already-staged files to their original names.
        logger.error(f"Error during phase 1 staging. Rolling back: {exc}")
        for src, temp_path in staged:
            original_path = os.path.join(target_dir, src)
            if os.path.exists(temp_path):
                os.rename(temp_path, original_path)
        raise FileSystemError(
            f"Renaming transaction aborted during Phase 1: {exc}"
        )
    return staged


def _phase2_commit(
    target_dir: str,
    name_mapping: Dict[str, str],
    staged: List[Tuple[str, str]],
) -> None:
    """Rename every staged file to its final destination."""
    committed: List[Tuple[str, str]] = []  # (temp_path, final_path)
    try:
        for src, temp_path in staged:
            dst = name_mapping[src]
            final_path = os.path.join(target_dir, dst)
            os.rename(temp_path, final_path)
            committed.append((temp_path, final_path))
            logger.info(f"    - Renamed: '{src}' -> '{dst}'")
    except Exception as exc:
        # Roll back Phase 2 commits first, then Phase 1 staging.
        logger.error(
            f"Error during Phase 2. Restoring database to original state: {exc}"
        )
        for temp_path, final_path in committed:
            if os.path.exists(final_path):
                os.rename(final_path, temp_path)
        for src, temp_path in staged:
            original_path = os.path.join(target_dir, src)
            if os.path.exists(temp_path):
                os.rename(temp_path, original_path)
        raise FileSystemError(
            f"Renaming transaction failed during Phase 2. State restored. "
            f"Reason: {exc}"
        )


def atomic_two_phase_rename(target_dir: str, name_mapping: Dict[str, str]) -> None:
    """Apply ``name_mapping`` to ``target_dir`` as a two-phase transaction.

    Args:
        target_dir: directory containing the source files.
        name_mapping: ``{old_name: new_name}`` dict. All names are relative
            to ``target_dir``.

    Raises:
        RenamingError: pre-flight checks failed (missing source, duplicate
            destination, conflicting existing file).
        FileSystemError: Phase 1 or Phase 2 failed mid-flight and the
            directory has been restored to its pre-transaction state.
    """
    _preflight_checks(target_dir, name_mapping)
    staged = _phase1_stage(target_dir, name_mapping)
    _phase2_commit(target_dir, name_mapping, staged)
