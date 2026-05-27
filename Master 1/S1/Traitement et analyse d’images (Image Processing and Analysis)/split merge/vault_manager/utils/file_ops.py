"""
System-wide File System operations utility module.
Provides centralized atomic, safe, and highly robust zip/backup implementations.
"""

import os
import shutil
import zipfile
from typing import List, Dict, Set
from vault_manager.exceptions import FileOperationError, RenamingCollisionError
from vault_manager.logging import logger


def ensure_directory(path: str) -> None:
    """Safely constructs directories if they do not exist."""
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        raise FileOperationError(f"Failed to create directory '{path}': {e}")


def write_file_safely(filepath: str, content: str) -> None:
    """Safely writes content into a target file path, enforcing UTF-8."""
    try:
        ensure_directory(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        raise FileOperationError(f"Failed writing content to file '{filepath}': {e}")


def create_backup(filepath: str) -> str:
    """Generates a '.bak' copy next to the requested target file."""
    if not os.path.exists(filepath):
        raise FileOperationError(f"Cannot back up non-existent file: {filepath}")
    
    backup_path = filepath + ".bak"
    try:
        shutil.copy2(filepath, backup_path)
        return backup_path
    except Exception as e:
        raise FileOperationError(f"Failed to copy '{filepath}' to backup '{backup_path}': {e}")


def compress_directory_to_zip(base_path: str, zip_filepath: str, archive_folder_prefix: str = "") -> None:
    """
    Compresses files inside a folder into a ZIP file.
    
    Args:
        base_path: Directory path to scan and zip.
        zip_filepath: Destination zip file path.
        archive_folder_prefix: An optional directory prefix nested inside the zip file structure.
    """
    if not os.path.exists(base_path):
        raise FileOperationError(f"Folder to zip does not exist: {base_path}")

    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, base_path)
                    
                    if archive_folder_prefix:
                        arcname = os.path.join(archive_folder_prefix, rel_path)
                    else:
                        arcname = rel_path
                        
                    zf.write(file_path, arcname=arcname)
    except Exception as e:
        raise FileOperationError(f"Failed to package archive zip at '{zip_filepath}': {e}")


def atomic_two_phase_rename(target_dir: str, name_mapping: Dict[str, str]) -> None:
    """
    Executes a high-integrity, safe renaming process.
    Uses temp names first, then applies final names to guarantee zero filename collisions.
    Rolls back to the original state if any operations fail mid-transaction.
    """
    # 1. Pre-execution safety audits
    missing_files = []
    for old_name in name_mapping.keys():
        if not os.path.exists(os.path.join(target_dir, old_name)):
            missing_files.append(old_name)

    if missing_files:
        raise RenamingCollisionError(
            f"Pre-checks aborted. Missing the following target files: {missing_files}"
        )

    new_names = list(name_mapping.values())
    if len(new_names) != len(set(new_names)):
        raise RenamingCollisionError("Pre-checks aborted. Destination mapping is not unique.")

    existing_targets = []
    for target in new_names:
        if os.path.exists(os.path.join(target_dir, target)) and target not in name_mapping:
            existing_targets.append(target)

    if existing_targets:
        raise RenamingCollisionError(
            f"Pre-checks aborted. Target filenames already exist in system: {existing_targets}"
        )

    logger.info("Checks passed. Executing phase 1 (temporary staging)...")
    temp_suffix = ".temp_rename_staging_lock"
    phase1_completed: List[tuple] = []  # List of tuples: (original_path, staging_path)

    try:
        for old_name in name_mapping.keys():
            original_path = os.path.join(target_dir, old_name)
            staging_path = os.path.join(target_dir, old_name + temp_suffix)
            os.rename(original_path, staging_path)
            phase1_completed.append((old_name, staging_path))
    except Exception as e:
        logger.error(f"Collision or OS interrupt during staging. Rolling back: {e}")
        for old_name, staging_path in phase1_completed:
            original_path = os.path.join(target_dir, old_name)
            if os.path.exists(staging_path):
                os.rename(staging_path, original_path)
        raise FileOperationError(f"Renaming staged phase aborted. Changes rolled back. Reason: {e}")

    logger.info("Staging lock complete. Executing phase 2 (final renaming)...")
    phase2_completed: List[tuple] = []  # List of tuples: (staging_path, final_path)

    try:
        for old_name, staging_path in phase1_completed:
            new_name = name_mapping[old_name]
            final_path = os.path.join(target_dir, new_name)
            os.rename(staging_path, final_path)
            phase2_completed.append((staging_path, final_path))
            logger.info(f"    - Renamed: '{old_name}' -> '{new_name}'")
    except Exception as e:
        logger.error(f"Critical error during phase 2 execution. Attempting disaster recovery: {e}")
        # Revert phase 2 adjustments to staging files
        for staging_path, final_path in phase2_completed:
            if os.path.exists(final_path):
                os.rename(final_path, staging_path)
        # Restore phase 1 staging back to baseline old file paths
        for old_name, staging_path in phase1_completed:
            original_path = os.path.join(target_dir, old_name)
            if os.path.exists(staging_path):
                os.rename(staging_path, original_path)
        raise FileOperationError(f"Transactional execution failed. Full state rolled back. Reason: {e}")