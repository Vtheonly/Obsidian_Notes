"""
System-wide File System Utility Module.
Handles transactional writing, back-ups, recursive file searches, and zipping.
"""

import os
import shutil
import zipfile
from typing import List, Dict, Optional
from vault_manager.exceptions import FileSystemError, RenamingError
from vault_manager.logging import logger


def ensure_directory(path: str) -> None:
    """Safely constructs directories if they do not exist."""
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        raise FileSystemError(f"Failed to create directory '{path}': {e}")


def write_file_safely(filepath: str, content: str) -> None:
    """Writes content into a target file path, enforcing UTF-8."""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise FileSystemError(f"Failed writing content to file '{filepath}': {e}")


def read_file_safely(filepath: str) -> str:
    """Reads content from a target file path, enforcing UTF-8."""
    if not os.path.exists(filepath):
        raise FileSystemError(f"Target file does not exist: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise FileSystemError(f"Failed reading content from '{filepath}': {e}")


def create_backup(filepath: str) -> str:
    """Generates a '.bak' copy next to the requested target file."""
    if not os.path.exists(filepath):
        raise FileSystemError(f"Cannot back up non-existent file: {filepath}")
    backup_path = filepath + ".bak"
    try:
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        raise FileSystemError(f"Failed to copy '{filepath}' to backup '{backup_path}': {e}")


def compress_directory_to_zip(base_path: str, zip_filepath: str, archive_prefix: str = "") -> None:
    """Compresses files inside a folder into a ZIP file."""
    if not os.path.exists(base_path):
        raise FileSystemError(f"Folder to zip does not exist: {base_path}")
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, base_path)
                    if archive_prefix:
                        arcname = os.path.join(archive_prefix, rel_path)
                    else:
                        arcname = rel_path
                    zf.write(file_path, arcname=arcname)
    except Exception as e:
        raise FileSystemError(f"Failed to package archive zip at '{zip_filepath}': {e}")


def atomic_two_phase_rename(target_dir: str, name_mapping: Dict[str, str]) -> None:
    """
    Executes a safe two-phase renaming process.
    Uses temporary names first to prevent collisions and support complex swaps.
    """
    missing_files = [f for f in name_mapping.keys() if not os.path.exists(os.path.join(target_dir, f))]
    if missing_files:
        raise RenamingError(f"Pre-checks aborted. Missing target files: {missing_files}")

    dest_names = list(name_mapping.values())
    if len(dest_names) != len(set(dest_names)):
        raise RenamingError("Pre-checks aborted. Destination mapping contains duplicates.")

    existing_unmapped_targets = [
        f for f in dest_names 
        if os.path.exists(os.path.join(target_dir, f)) and f not in name_mapping
    ]
    if existing_unmapped_targets:
        raise RenamingError(f"Pre-checks aborted. Unmapped target files already exist: {existing_unmapped_targets}")

    temp_suffix = ".temp_rename_staging_lock"
    phase1_completed: List[tuple] = []  # (original_name, temp_path)

    try:
        for old_name in name_mapping.keys():
            original_path = os.path.join(target_dir, old_name)
            temp_path = os.path.join(target_dir, old_name + temp_suffix)
            os.rename(original_path, temp_path)
            phase1_completed.append((old_name, temp_path))
    except Exception as e:
        logger.error(f"Error during phase 1 staging. Rolling back: {e}")
        for old_name, temp_path in phase1_completed:
            original_path = os.path.join(target_dir, old_name)
            if os.path.exists(temp_path):
                os.rename(temp_path, original_path)
        raise FileSystemError(f"Renaming transaction aborted during Phase 1: {e}")

    phase2_completed: List[tuple] = []  # (temp_path, final_path)
    try:
        for old_name, temp_path in phase1_completed:
            new_name = name_mapping[old_name]
            final_path = os.path.join(target_dir, new_name)
            os.rename(temp_path, final_path)
            phase2_completed.append((temp_path, final_path))
            logger.info(f"    - Renamed: '{old_name}' -> '{new_name}'")
    except Exception as e:
        logger.error(f"Error during Phase 2. Restoring database to original state: {e}")
        for temp_path, final_path in phase2_completed:
            if os.path.exists(final_path):
                os.rename(final_path, temp_path)
        for old_name, temp_path in phase1_completed:
            original_path = os.path.join(target_dir, old_name)
            if os.path.exists(temp_path):
                os.rename(temp_path, original_path)
        raise FileSystemError(f"Renaming transaction failed during Phase 2. State restored. Reason: {e}")