"""
Flexible Sequential Renaming Service.
Supports map-based and regular-expression-based renaming strategies.
"""

import re
from typing import List, Dict, Any
from vault_manager.core.interfaces import IRenamingStrategy
from vault_manager.exceptions import RenamingError


class MapRenamer(IRenamingStrategy):
    """Maps filenames using a strict key-to-value dictionary configuration."""

    def generate_mapping(self, current_files: List[str], options: Dict[str, Any]) -> Dict[str, str]:
        mapping_dict: Dict[str, str] = options.get("mapping", {})
        if not mapping_dict:
            raise RenamingError("No mapping dictionary provided in options.")
        
        # Keep only files that exist in current selection
        return {k: v for k, v in mapping_dict.items() if k in current_files}


class RegexPatternRenamer(IRenamingStrategy):
    """Automatically parses and standardizes names using regex search and replacement patterns."""

    def generate_mapping(self, current_files: List[str], options: Dict[str, Any]) -> Dict[str, str]:
        pattern_str = options.get("pattern", "")
        replacement_format = options.get("format", "")
        
        if not pattern_str or not replacement_format:
            raise RenamingError("Pattern and format string are required for RegexPatternRenamer.")

        try:
            compiled_pattern = re.compile(pattern_str)
        except Exception as e:
            raise RenamingError(f"Invalid regex pattern: {e}")

        mapping: Dict[str, str] = {}
        for f in current_files:
            match = compiled_pattern.match(f)
            if match:
                groups = match.groups()
                group_dict = {f"g{i+1}": g.strip() for i, g in enumerate(groups) if g}
                for k, v in match.groupdict().items():
                    group_dict[k] = v.strip()

                try:
                    new_name = replacement_format.format(**group_dict)
                    if not new_name.endswith('.md') and f.endswith('.md'):
                        new_name += ".md"
                    mapping[f] = new_name
                except KeyError as ke:
                    raise RenamingError(f"Formatting failed for file '{f}'. Missing key: {ke}")

        return mapping