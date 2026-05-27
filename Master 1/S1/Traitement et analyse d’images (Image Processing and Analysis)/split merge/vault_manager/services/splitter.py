"""
Unified Document Splitting Engine.
Integrates the parsing structures of split_vault.py and split_vault_1.py 
into a highly robust, unified processor.
"""

import os
import re
import shutil
from typing import List, Optional
from vault_manager.core.interfaces import FileProcessor
from vault_manager.core.models import ParsedSection
from vault_manager.utils.file_ops import write_file_safely, compress_directory_to_zip
from vault_manager.logging import logger
from vault_manager.exceptions import ParsingError


class VaultSplitter(FileProcessor):
    """
    Splits continuous Markdown documents into structured subfolders
    and cleanly separated individual Markdown files.
    """

    def __init__(self, output_dir: str = "Course", zip_filepath: str = "Course.zip"):
        self.output_dir = output_dir
        self.zip_filepath = zip_filepath
        self.parsed_sections: List[ParsedSection] = []

    def execute(self, vault_filepath: str) -> None:
        """
        Main runner.
        1. Validates the existence of the source file.
        2. Parses vault chapters, sections, and practice exercises.
        3. Writes organized assets to disk.
        4. Compresses outputs into a clean ZIP archive.
        5. Performs atomic cleanups.
        """
        if not os.path.exists(vault_filepath):
            raise ParsingError(f"Specified document target does not exist: {vault_filepath}")

        logger.info(f"Reading unified source vault document: '{vault_filepath}'...")
        try:
            with open(vault_filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            raise ParsingError(f"Failed reading vault markdown contents: {e}")

        # Ensure we start fresh
        self.parsed_sections.clear()

        # Parse contents
        self._parse_vault_content(content)

        if not self.parsed_sections:
            raise ParsingError("Zero sections or markdown files were resolved. Check header regex rules.")

        # Cleanup old output folders to avoid contamination
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        # Write parsed assets
        logger.info(f"Writing {len(self.parsed_sections)} extracted markdown files...")
        for section in self.parsed_sections:
            target_folder = os.path.join(self.output_dir, section.folder)
            target_path = os.path.join(target_folder, section.filename)
            write_file_safely(target_path, section.content)

        # ZIP output directory
        logger.info(f"Packaging assets into output archive: '{self.zip_filepath}'")
        compress_directory_to_zip(
            base_path=self.output_dir,
            zip_filepath=self.zip_filepath,
            archive_folder_prefix="Course"
        )

        # Remove raw artifacts
        logger.info(f"Cleaning up raw workspace directory '{self.output_dir}'")
        shutil.rmtree(self.output_dir)
        logger.success("Markdown document split process completed successfully.")

    def _parse_vault_content(self, content: str) -> None:
        """Parses the Markdown content line-by-line to identify and organize sections."""
        lines = content.split("\n")
        current_folder = ""
        current_file: Optional[str] = None
        current_content: List[str] = []

        for line in lines:
            # Match chapters, exercises, and standard sections
            chapter_match = re.match(r"^# Chapter (\d+)\.\s*(.+)$", line)
            exercises_match = re.match(r"^# Practice Exercises and Mathematical Derivations", line)
            section_match = re.match(r"^## (\d+)\.\s*(.+)$", line)
            exercise_match = re.match(r"^## Exercise (\d+):\s*(.+)$", line)
            vault_map_match = re.match(r"^## Vault Architecture & Directory Map", line)
            intro_match = line.startswith("# Course:")

            if chapter_match:
                # Store the current section before switching chapters
                if current_file:
                    self._add_section(current_folder, current_file, current_content)
                current_file = None
                current_content = []

                ch_num = chapter_match.group(1)
                ch_title = chapter_match.group(2).strip()
                current_folder = f"Chapter {ch_num}. {ch_title}"
                logger.info(f"    - Found Chapter: '{ch_num}. {ch_title}'")

            elif exercises_match:
                if current_file:
                    self._add_section(current_folder, current_file, current_content)
                current_file = None
                current_content = []
                current_folder = "Practice Exercises and Mathematical Derivations"
                logger.info("    - Found Exercises Header Section")

            elif section_match:
                if current_file:
                    self._add_section(current_folder, current_file, current_content)
                current_content = []

                sec_num = section_match.group(1)
                sec_title = self._sanitize_filename(section_match.group(2))
                current_file = f"{sec_num}. {sec_title}.md"
                current_content.append(line)

            elif exercise_match:
                if current_file:
                    self._add_section(current_folder, current_file, current_content)
                current_content = []

                ex_num = exercise_match.group(1)
                ex_title = self._sanitize_filename(exercise_match.group(2))
                current_file = f"Exercise {ex_num}. {ex_title}.md"
                current_content.append(line)

            elif vault_map_match:
                if current_file:
                    self._add_section(current_folder, current_file, current_content)
                current_content = []
                current_file = "Vault Architecture Map.md"
                current_folder = ""
                current_content.append(line)

            elif intro_match:
                if current_file:
                    self._add_section(current_folder, current_file, current_content)
                current_content = []
                current_file = "Introduction.md"
                current_folder = ""
                current_content.append(line)

            else:
                if current_file:
                    current_content.append(line)
                elif line.strip():
                    # Content before headers defaults to Introduction.md
                    current_file = "Introduction.md"
                    current_folder = ""
                    current_content.append(line)

        # Append last active parse blocks
        if current_file:
            self._add_section(current_folder, current_file, current_content)

    def _add_section(self, folder: str, filename: str, content_lines: List[str]) -> None:
        """Helper to sanitize and record a parsed section."""
        body = "\n".join(content_lines).strip()

        # Clean up leading/trailing '---' horizontal rules
        if body.endswith("---"):
            body = body[:-3].strip()
        if body.startswith("---"):
            body = body[3:].strip()

        # Place files under matching folders based on content properties if folder context is missing
        if not folder:
            if filename.startswith("Exercise 1"):
                folder = "Chapter 1. Image Fundamentals and Basic Notions"
            elif filename.startswith("Exercise 2"):
                folder = "Chapter 3. Image Segmentation"
            elif filename.startswith("Exercise 3"):
                folder = "Chapter 4. Image Super-Resolution"

        self.parsed_sections.append(ParsedSection(folder=folder, filename=filename, content=body))

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """Escapes OS incompatible characters."""
        return filename.replace("/", " - ").replace(":", " - ").strip()