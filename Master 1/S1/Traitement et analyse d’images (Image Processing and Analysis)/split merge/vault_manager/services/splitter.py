"""
Document Splitting Module.
Decoupled parser that parses a file based on dynamic strategies,
supporting any document structure or layout.
"""

import re
from typing import List, Dict, Any, Optional
from vault_manager.core.interfaces import IDocumentParser
from vault_manager.core.models import ParsedSegment
from vault_manager.exceptions import ParserError


class DynamicRegexParser(IDocumentParser):
    """
    Parses a document sequentially based on a configurable list of regular expressions.
    Perfect for adapting to any numbering schema (Chapter 1, 01, Section A, etc.).
    """

    def parse(self, content: str, options: Dict[str, Any]) -> List[ParsedSegment]:
        rules: List[Dict[str, str]] = options.get("rules", [])
        if not rules:
            raise ParserError("No parsing rules provided in options.")

        # Compile regex rules
        compiled_rules = []
        for rule in rules:
            try:
                compiled_rules.append({
                    "type": rule["type"],
                    "pattern": re.compile(rule["pattern"], re.MULTILINE),
                    "folder_format": rule.get("folder_format", ""),
                    "file_format": rule.get("file_format", "")
                })
            except Exception as e:
                raise ParserError(f"Invalid regex pattern '{rule.get('pattern')}': {e}")

        lines = content.split('\n')
        segments: List[ParsedSegment] = []
        
        current_folder = options.get("default_folder", "")
        current_file = options.get("default_file", "Introduction.md")
        current_content: List[str] = []

        def save_current_segment():
            if current_content or current_file != "Introduction.md":
                body = '\n'.join(current_content).strip()
                if body.endswith('---'):
                    body = body[:-3].strip()
                if body.startswith('---'):
                    body = body[3:].strip()
                segments.append(ParsedSegment(
                    folder=current_folder,
                    filename=current_file,
                    content=body
                ))

        for line in lines:
            matched = False
            for rule in compiled_rules:
                match = rule["pattern"].match(line)
                if match:
                    # Save previous segment
                    save_current_segment()
                    current_content = []

                    groups = match.groups()
                    group_dict = {f"g{i+1}": g.strip() for i, g in enumerate(groups) if g}
                    
                    # Add named matching groups if available
                    for k, v in match.groupdict().items():
                        group_dict[k] = v.strip()

                    # Interpolate folder format
                    if rule["folder_format"]:
                        try:
                            current_folder = rule["folder_format"].format(**group_dict)
                        except KeyError:
                            current_folder = rule["folder_format"]
                    
                    # Interpolate file format
                    if rule["file_format"]:
                        try:
                            current_file = rule["file_format"].format(**group_dict)
                        except KeyError:
                            current_file = rule["file_format"]
                    else:
                        current_file = "Section.md"
                        
                    if not current_file.endswith('.md'):
                        current_file += ".md"

                    current_content.append(line)
                    matched = True
                    break
            
            if not matched:
                current_content.append(line)

        # Save remaining content
        save_current_segment()
        return segments