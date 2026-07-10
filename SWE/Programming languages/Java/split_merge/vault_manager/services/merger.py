"""
Non-destructive vault merging service.

``FlexibleMerger`` writes parsed segments into a target directory, applying
a collision policy chosen by the caller:

* ``side_by_side`` (default) — keep the existing file; write the new one
  alongside with a suffix (e.g. `` (Vault 1)``) appended to the stem.
* ``skip`` — keep the existing file; do not write the new one.
* ``overwrite`` — replace the existing file with the new one.

Folder and filename strings are sanitised by replacing ``:`` and ``/``
with ``-`` before joining, so segments whose metadata contains those
characters do not escape the target directory.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

from vault_manager.core.interfaces import IMergeStrategy
from vault_manager.core.models import ParsedSegment
from vault_manager.logging import logger
from vault_manager.utils.file_ops import write_file_safely


# Default values for options not provided by the caller. Kept as module
# constants so the option keys and defaults are visible at a glance.
_DEFAULT_MODE = "side_by_side"
_DEFAULT_SUFFIX = " (Vault 1)"

# Characters that are unsafe in folder/file names. Replaced with a dash
# during the sanitisation pass.
_UNSAFE_FILENAME_CHARS = (":", "/")


def _sanitise(name: str) -> str:
    """Replace ``:`` and ``/`` with ``-`` so metadata cannot escape the target dir."""
    sanitised = name
    for char in _UNSAFE_FILENAME_CHARS:
        sanitised = sanitised.replace(char, "-")
    return sanitised


class FlexibleMerger(IMergeStrategy):
    """Merge parsed segments into a target directory using a collision policy."""

    def merge(
        self,
        segments: List[ParsedSegment],
        target_dir: str,
        options: Dict[str, Any],
    ) -> int:
        """Write ``segments`` into ``target_dir`` and return the count written.

        See module docstring for the supported ``options`` keys.
        """
        mode = options.get("merge_mode", _DEFAULT_MODE)
        suffix = options.get("conflict_suffix", _DEFAULT_SUFFIX)
        written_count = 0

        for segment in segments:
            clean_folder = _sanitise(segment.folder)
            clean_filename = _sanitise(segment.filename)

            target_folder_path = os.path.join(target_dir, clean_folder)
            target_file_path = os.path.join(target_folder_path, clean_filename)

            if os.path.exists(target_file_path):
                target_file_path = self._resolve_collision(
                    target_folder_path,
                    clean_filename,
                    mode,
                    suffix,
                )
                if target_file_path is None:
                    # ``skip`` mode returns None to signal "do not write".
                    continue

            write_file_safely(target_file_path, segment.content)
            written_count += 1

        return written_count

    @staticmethod
    def _resolve_collision(
        folder_path: str,
        filename: str,
        mode: str,
        suffix: str,
    ):
        """Apply the collision policy and return the (possibly new) target path.

        Returns ``None`` for ``skip`` mode (meaning "do not write").

        For an unknown ``mode`` the original code silently falls through to
        the original path (i.e. overwrite via ``write_file_safely``) WITHOUT
        emitting any log line. We preserve that exact behaviour: only the
        three known modes log a collision message; unknown modes log nothing.
        """
        if mode == "side_by_side":
            stem, ext = os.path.splitext(filename)
            new_filename = f"{stem}{suffix}{ext}"
            new_path = os.path.join(folder_path, new_filename)
            logger.info(
                f"    - Collision detected. Staging side-by-side: {new_filename}"
            )
            return new_path

        if mode == "skip":
            logger.info(f"    - Collision detected. Skipping: {filename}")
            return None

        if mode == "overwrite":
            logger.info(f"    - Collision detected. Overwriting: {filename}")
            return os.path.join(folder_path, filename)

        # Unknown mode: original behaviour is to fall through with no log
        # line and let write_file_safely overwrite the existing file.
        return os.path.join(folder_path, filename)
