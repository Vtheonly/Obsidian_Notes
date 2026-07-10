"""
File-system utility module.

Provides safe, encoding-enforced helpers for reading, writing, backing up,
and zipping files. These are pure I/O utilities — transactional renames
(which involve rollback logic) live in
:mod:`vault_manager.services.rename_transaction` and are re-exported from
here for backward compatibility with the original import path.
"""

from __future__ import annotations

import os
import shutil
import zipfile

from vault_manager.exceptions import FileSystemError
from vault_manager.logging import logger


# ---------------------------------------------------------------------------
# Directory / file primitives
# ---------------------------------------------------------------------------

def ensure_directory(path: str) -> None:
    """Create ``path`` (and parents) if missing. Idempotent."""
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as exc:
        raise FileSystemError(f"Failed to create directory '{path}': {exc}")


def write_file_safely(filepath: str, content: str) -> None:
    """Write ``content`` to ``filepath`` as UTF-8, creating parent dirs."""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as exc:
        raise FileSystemError(
            f"Failed writing content to file '{filepath}': {exc}"
        )


def read_file_safely(filepath: str) -> str:
    """Read ``filepath`` as UTF-8. Raise :class:`FileSystemError` if missing."""
    if not os.path.exists(filepath):
        raise FileSystemError(f"Target file does not exist: {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        raise FileSystemError(
            f"Failed reading content from '{filepath}': {exc}"
        )


def create_backup(filepath: str) -> str:
    """Create a ``.bak`` copy next to ``filepath`` and return its path."""
    if not os.path.exists(filepath):
        raise FileSystemError(f"Cannot back up non-existent file: {filepath}")
    backup_path = filepath + ".bak"
    try:
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as exc:
        raise FileSystemError(
            f"Failed to copy '{filepath}' to backup '{backup_path}': {exc}"
        )


# ---------------------------------------------------------------------------
# Zip
# ---------------------------------------------------------------------------

def compress_directory_to_zip(
    base_path: str,
    zip_filepath: str,
    archive_prefix: str = "",
) -> None:
    """Zip every file under ``base_path`` into ``zip_filepath``.

    If ``archive_prefix`` is given, entries are stored as
    ``<archive_prefix>/<relative_path>``; otherwise they are stored at the
    root of the archive.
    """
    if not os.path.exists(base_path):
        raise FileSystemError(f"Folder to zip does not exist: {base_path}")
    try:
        with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _dirs, files in os.walk(base_path):
                for filename in files:
                    abs_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(abs_path, base_path)
                    if archive_prefix:
                        arcname = os.path.join(archive_prefix, rel_path)
                    else:
                        arcname = rel_path
                    zf.write(abs_path, arcname=arcname)
    except Exception as exc:
        raise FileSystemError(
            f"Failed to package archive zip at '{zip_filepath}': {exc}"
        )


# ---------------------------------------------------------------------------
# Backward-compat re-export
# ---------------------------------------------------------------------------
# The original ``file_ops`` module hosted ``atomic_two_phase_rename`` directly.
# It has been moved to ``vault_manager.services.rename_transaction`` for
# clearer separation of concerns, but is re-exported here so existing
# imports (`from vault_manager.utils.file_ops import atomic_two_phase_rename`)
# continue to work without code changes.

def atomic_two_phase_rename(target_dir: str, name_mapping):
    """Backward-compat shim. See :func:`rename_transaction.atomic_two_phase_rename`."""
    # Imported lazily to avoid a circular import at module-load time.
    from vault_manager.services.rename_transaction import (
        atomic_two_phase_rename as _impl,
    )
    return _impl(target_dir, name_mapping)
