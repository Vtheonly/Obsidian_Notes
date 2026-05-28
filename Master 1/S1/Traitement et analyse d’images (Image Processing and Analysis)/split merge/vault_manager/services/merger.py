"""
Non-destructive Vault Merging Engine.
Merges structured segments into target folders, preventing conflicts.
"""

import os
from typing import List, Dict, Any
from vault_manager.core.interfaces import IMergeStrategy
from vault_manager.core.models import ParsedSegment
from vault_manager.utils.file_ops import write_file_safely
from vault_manager.logging import logger


class FlexibleMerger(IMergeStrategy):
    """
    Implements non-destructive and custom mergers based on runtime options.
    Modes:
      - side_by_side: appends a suffix (e.g. ' (Vault 1).md') if file exists.
      - overwrite: replaces any existing file.
      - skip: retains original, skips new segment.
    """

    def merge(self, segments: List[ParsedSegment], target_dir: str, options: Dict[str, Any]) -> int:
        mode = options.get("merge_mode", "side_by_side")
        suffix = options.get("conflict_suffix", " (Vault 1)")
        written_count = 0

        for segment in segments:
            # Map clean relative destination path
            clean_folder = segment.folder.replace(':', '-').replace('/', '-')
            clean_filename = segment.filename.replace(':', '-').replace('/', '-')
            
            target_folder_path = os.path.join(target_dir, clean_folder)
            target_file_path = os.path.join(target_folder_path, clean_filename)

            if os.path.exists(target_file_path):
                if mode == "side_by_side":
                    base, ext = os.path.splitext(clean_filename)
                    conflicting_filename = f"{base}{suffix}{ext}"
                    target_file_path = os.path.join(target_folder_path, conflicting_filename)
                    logger.info(f"    - Collision detected. Staging side-by-side: {conflicting_filename}")
                elif mode == "skip":
                    logger.info(f"    - Collision detected. Skipping: {clean_filename}")
                    continue
                elif mode == "overwrite":
                    logger.info(f"    - Collision detected. Overwriting: {clean_filename}")

            write_file_safely(target_file_path, segment.content)
            written_count += 1

        return written_count