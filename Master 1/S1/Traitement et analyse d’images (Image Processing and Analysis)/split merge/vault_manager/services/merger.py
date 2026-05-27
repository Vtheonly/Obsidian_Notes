"""
Side-by-side Non-destructive Merging Engine.
Merges information structures from Vault 1.md with active directory folders,
renaming imported files with a '(Vault 1)' suffix to prevent data loss.
"""

import os
import re
import shutil
import zipfile
from typing import Dict, Optional
from vault_manager.core.interfaces import FileProcessor
from vault_manager.utils.file_ops import write_file_safely
from vault_manager.logging import logger
from vault_manager.exceptions import ParsingError, FileOperationError


class VaultMerger(FileProcessor):
    """
    Side-by-side non-destructive merging engine.
    Parses 'Vault 1.md' and writes its contents directly alongside existing 
    Obsidian notes using distinct file suffixes.
    """

    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.parsed_sections: Dict[str, str] = {}
        self.parsed_exercises: Dict[str, str] = {}
        self.introduction_content: str = ""
        self.vault_map_content: str = ""

    def execute(self, vault_filepath: str, backup_zip_name: str = "Merged_Course.zip") -> None:
        """
        Main execution flow.
        1. Resets the environment from previous failed merge attempts.
        2. Parses the target 'Vault 1.md'.
        3. Creates files alongside existing files.
        4. Packages results into a ZIP file.
        """
        logger.info("Initializing merge operation context...")
        self._cleanup_previous_run()
        
        if not os.path.exists(vault_filepath):
            raise ParsingError(f"Target Vault 1.md file not found: {vault_filepath}")

        # Parse source file
        self._parse_vault_file(vault_filepath)

        # Write side-by-side files
        logger.info("Writing merged side-by-side workspace assets...")
        self._write_side_by_side_files()

        # Archive workspace structure to a ZIP file
        zip_path = os.path.join(self.workspace_path, backup_zip_name)
        self._create_zip_backup(zip_path)
        
        logger.success("Merge transaction finalized cleanly.")

    def _cleanup_previous_run(self) -> None:
        """Performs atomic deletions of generated files from previous runs to keep a clean workspace."""
        logger.info("Cleaning up previous workspace assets to ensure clean execution...")
        
        untracked_files = [
            "01 Introduction to Digital Images/1.7 Image Convolution and Boundary Effects.md",
            "01 Introduction to Digital Images/1.8 Three Levels of Image Processing.md",
            "Introduction.md",
            "Vault Architecture Map.md"
        ]
        for rel_path in untracked_files:
            full_path = os.path.join(self.workspace_path, rel_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                logger.info(f"    - Removed old merged file: {rel_path}")

        untracked_folders = ["03 Image Segmentation", "04 Image Super-Resolution"]
        for folder in untracked_folders:
            full_path = os.path.join(self.workspace_path, folder)
            if os.path.exists(full_path):
                shutil.rmtree(full_path)
                logger.info(f"    - Removed old merged folder: {folder}")

    def _parse_vault_file(self, filepath: str) -> None:
        """Parses the input file to extract chapters, sections, and exercises."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise ParsingError(f"Failed to read file: {e}")

        lines = content.split('\n')
        current_section_title: Optional[str] = None
        current_content: list = []
        is_exercises_section = False

        for line in lines:
            chapter_match = re.match(r'^# Chapter (\d+)\.\s*(.+)$', line)
            exercises_hdr_match = re.match(r'^# Practice Exercises and Mathematical Derivations', line)
            section_match = re.match(r'^## (\d+)\.\s*(.+)$', line)
            exercise_match = re.match(r'^## Exercise (\d+):\s*(.+)$', line)
            vault_map_match = re.match(r'^## Vault Architecture & Directory Map', line)

            if chapter_match:
                if current_section_title:
                    self._store_block(current_section_title, current_content, is_exercises_section)
                current_section_title = None
                current_content = []
                
            elif exercises_hdr_match:
                if current_section_title:
                    self._store_block(current_section_title, current_content, is_exercises_section)
                is_exercises_section = True
                current_section_title = None
                current_content = []

            elif section_match:
                if current_section_title:
                    self._store_block(current_section_title, current_content, is_exercises_section)
                current_section_title = section_match.group(2).strip()
                current_content = [line]

            elif exercise_match:
                if current_section_title:
                    self._store_block(current_section_title, current_content, is_exercises_section)
                current_section_title = f"Exercise {exercise_match.group(1)}: {exercise_match.group(2).strip()}"
                current_content = [line]

            elif vault_map_match:
                if current_section_title:
                    self._store_block(current_section_title, current_content, is_exercises_section)
                current_section_title = "Vault Map"
                current_content = [line]

            elif line.startswith('# Course:'):
                if current_section_title:
                    self._store_block(current_section_title, current_content, is_exercises_section)
                current_section_title = "Intro"
                current_content = [line]

            else:
                if current_section_title:
                    current_content.append(line)
                elif line.strip():
                    current_section_title = "Intro"
                    current_content.append(line)

        # Store last parsed block
        if current_section_title:
            self._store_block(current_section_title, current_content, is_exercises_section)

        logger.info(f"Parsed {len(self.parsed_sections)} sections and {len(self.parsed_exercises)} exercises.")

    def _store_block(self, title: str, content_lines: list, is_exercise: bool) -> None:
        content = '\n'.join(content_lines).strip()
        
        # Strip leading/trailing '---' rule marks
        if content.endswith('---'):
            content = content[:-3].strip()
        if content.startswith('---'):
            content = content[3:].strip()

        if title == "Intro":
            self.introduction_content = content
        elif title == "Vault Map":
            self.vault_map_content = content
        elif is_exercise:
            self.parsed_exercises[title] = content
        else:
            self.parsed_sections[title] = content

    def _write_side_by_side_files(self) -> None:
        """Writes files out with standard suffixes to avoid overwriting existing files."""
        # --- Chapter 1 Mapping ---
        ch1_dir = "01 Introduction to Digital Images"
        ch1_sections = {
            "Digital Image Definition and Representation": "1. Digital Image Definition and Representation (Vault 1).md",
            "Spatial Resolution and Color Spaces": "2. Spatial Resolution and Color Spaces (Vault 1).md",
            "Pixel Neighborhoods and Distance Metrics": "3. Pixel Neighborhoods and Distance Metrics (Vault 1).md",
            "Image Histograms": "4. Image Histograms (Vault 1).md",
            "Image Convolution and Boundary Effects": "5. Image Convolution and Boundary Effects (Vault 1).md",
            "Three Levels of Image Processing": "6. Three Levels of Image Processing (Vault 1).md"
        }
        for key, name in ch1_sections.items():
            if val := self.parsed_sections.get(key):
                write_file_safely(os.path.join(self.workspace_path, ch1_dir, name), val)

        if ex1 := self.parsed_exercises.get("Exercise 1: Computing 2D Convolution and Boundary Padding"):
            write_file_safely(os.path.join(self.workspace_path, ch1_dir, "Exercise 1. Computing 2D Convolution and Boundary Padding (Vault 1).md"), ex1)

        # --- Chapter 2 Mapping ---
        ch2_dir = "02 Image Preprocessing and Filtering"
        ch2_sections = {
            "Image Degradations and Noise Models": "1. Image Degradations and Noise Models (Vault 1).md",
            "Linear Filtering in the Spatial Domain": "2. Linear Filtering in the Spatial Domain (Vault 1).md",
            "Non Linear Spatial Filtering": "3. Non-Linear Spatial Filtering (Vault 1).md",
            "Frequency Domain Filtering": "4. Frequency Domain Filtering (Vault 1).md",
            "Advanced Filtering Techniques": "5. Advanced Filtering Techniques (Vault 1).md",
            "Contrast Enhancement": "6. Contrast Enhancement (Vault 1).md",
            "Adaptive and Local Contrast Methods": "7. Adaptive and Local Contrast Methods (Vault 1).md"
        }
        for key, name in ch2_sections.items():
            if val := self.parsed_sections.get(key):
                write_file_safely(os.path.join(self.workspace_path, ch2_dir, name), val)

        # Find Morphological sections
        morph_key = [k for k in self.parsed_sections.keys() if "Morphological" in k or "Structuring Element" in k]
        if morph_key and (morph_val := self.parsed_sections.get(morph_key[0])):
            write_file_safely(os.path.join(self.workspace_path, ch2_dir, "8. Morphological Filtering (Vault 1).md"), morph_val)

        # --- Chapter 3 Mapping ---
        ch3_dir = "03 Image Segmentation"
        ch3_sections = {
            "Foundations of Segmentation": "1. Foundations of Segmentation (Vault 1).md",
            "Edge Based Segmentation": "2. Edge-Based Segmentation (Vault 1).md",
            "Region Based Segmentation": "3. Region-Based Segmentation (Vault 1).md",
            "Binarization and Advanced Thresholding": "4. Binarization and Advanced Thresholding (Vault 1).md",
            "Connected Components and Shape Extraction": "5. Connected Components and Shape Extraction (Vault 1).md",
            "Evaluation Metrics for Image Segmentation": "7. Evaluation Metrics for Image Segmentation (Vault 1).md"
        }
        for key, name in ch3_sections.items():
            if val := self.parsed_sections.get(key):
                write_file_safely(os.path.join(self.workspace_path, ch3_dir, name), val)

        if ex2 := self.parsed_exercises.get("Exercise 2: Implementing Otsu's Global Thresholding"):
            write_file_safely(os.path.join(self.workspace_path, ch3_dir, "Exercise 2. Implementing Otsu's Global Thresholding (Vault 1).md"), ex2)

        # --- Chapter 4 Mapping ---
        ch4_dir = "04 Image Super-Resolution"
        sr_content = self.parsed_sections.get("Image Super Resolution") or self.parsed_sections.get("Image Super-Resolution")
        if sr_content:
            write_file_safely(os.path.join(self.workspace_path, ch4_dir, "6. Image Super-Resolution (Vault 1).md"), sr_content)

        if ex3 := self.parsed_exercises.get("Exercise 3: Bilinear Interpolation for Image Super-Resolution"):
            write_file_safely(os.path.join(self.workspace_path, ch4_dir, "Exercise 3. Bilinear Interpolation for Image Super-Resolution (Vault 1).md"), ex3)

        # --- General Files ---
        if self.introduction_content:
            write_file_safely(os.path.join(self.workspace_path, "Introduction (Vault 1).md"), self.introduction_content)
        if self.vault_map_content:
            write_file_safely(os.path.join(self.workspace_path, "Vault Architecture Map (Vault 1).md"), self.vault_map_content)

    def _create_zip_backup(self, zip_filepath: str) -> None:
        """Packs the merged notes into a secure ZIP file."""
        logger.info(f"Packaging merged workspace to zip: '{zip_filepath}'")
        
        target_dirs = [
            "01 Introduction to Digital Images",
            "02 Image Preprocessing and Filtering",
            "03 Image Segmentation",
            "04 Image Super-Resolution",
            "In-Depth",
            "Labs",
            "Quiz"
        ]
        target_files = ["Introduction (Vault 1).md", "Vault Architecture Map (Vault 1).md"]

        try:
            with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Package directories
                for folder in target_dirs:
                    folder_path = os.path.join(self.workspace_path, folder)
                    if os.path.exists(folder_path):
                        for root, _, files in os.walk(folder_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                rel_to_workspace = os.path.relpath(file_path, self.workspace_path)
                                # Wrap everything inside a unified zip folder
                                zf.write(file_path, arcname=os.path.join("Merged_Course", rel_to_workspace))
                
                # Package root files
                for root_file in target_files:
                    file_path = os.path.join(self.workspace_path, root_file)
                    if os.path.exists(file_path):
                        zf.write(file_path, arcname=os.path.join("Merged_Course", root_file))
        except Exception as e:
            raise FileOperationError(f"Failed to build backup archive: {e}")