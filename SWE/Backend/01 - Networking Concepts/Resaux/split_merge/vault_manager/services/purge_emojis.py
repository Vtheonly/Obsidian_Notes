#!/usr/bin/env python3
"""
Emoji Purging Service.
Implements IContentTransformer to remove all emoji characters from file content.
Supports recursive directory scanning with binary-safe file detection.
"""

import os
import re
from typing import List
from vault_manager.core.interfaces import IContentTransformer
from vault_manager.utils.file_ops import read_file_safely, write_file_safely
from vault_manager.logging import logger

# Comprehensive emoji regex covering all Unicode emoji ranges
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
    "\U0001F680-\U0001F6FF"  # Transport and Map
    "\U0001F700-\U0001F77F"  # Alchemical Symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000027BF"             # Dingbat arrow
    "\U0000FE00-\U0000FE0F"  # Variation Selectors
    "\U0000200D"             # Zero Width Joiner
    "\U00002600-\U000026FF"  # Misc Symbols
    "\U00002300-\U000023FF"  # Misc Technical
    "\U00002B50"             # Star
    "\U00002B05-\U00002B07"  # Arrows
    "\U00002934-\U00002935"  # Arrows
    "\U00003030"             # Wavy dash
    "\U000025AA-\U000025AB"  # Small squares
    "\U000025FB-\U000025FE"  # Medium squares
    "\U000025B6"             # Play button
    "\U000025C0"             # Reverse play
    "\U0000203C"             # Double exclamation
    "\U00002049"             # Exclamation question
    "\U00002139"             # Info
    "\U00002194-\U00002199"  # Arrows
    "\U000021A9-\U000021AA"  # Arrows
    "\U0000231A-\U0000231B"  # Watch, Hourglass
    "\U000023E9-\U000023F3"  # Media controls
    "\U000023F8-\U000023FA"  # Media controls
    "\U000024C2"             # Circled M
    "\U00002660"             # Spade
    "\U00002663"             # Club
    "\U00002665-\U00002666"  # Heart, Diamond
    "\U00002668"             # Hot springs
    "\U0000267B"             # Recycling
    "\U0000267F"             # Wheelchair
    "\U00002692-\U00002697"  # Tools
    "\U00002699"             # Gear
    "\U0000269B-\U0000269C"  # Atom, Fleur-de-lis
    "\U000026A0-\U000026A1"  # Warning, Zap
    "\U000026AA-\U000026AB"  # Circles
    "\U000026B0-\U000026B1"  # Coffin, Urn
    "\U000026BD-\U000026BE"  # Soccer, Baseball
    "\U000026C4-\U000026C5"  # Snowman, Sun
    "\U000026CE"             # Ophiuchus
    "\U000026CF-\U000026D4"  # Tools, No entry
    "\U000026E9-\U000026EA"  # Shinto, Church
    "\U000026F0-\U000026F5"  # Mountain, Sailboat
    "\U000026F7-\U000026FA"  # Skier, Tent
    "\U000026FD"             # Fuel pump
    "\U00002702"             # Scissors
    "\U00002705"             # Check mark
    "\U00002708-\U0000270D"  # Airplane, Writing hand
    "\U0000270F"             # Pencil
    "\U00002712"             # Black nib
    "\U00002714"             # Check mark
    "\U00002716"             # Cross mark
    "\U0000271D"             # Latin cross
    "\U00002721"             # Star of David
    "\U00002728"             # Sparkles
    "\U00002733-\U00002734"  # Eight spoked asterisk
    "\U00002744"             # Snowflake
    "\U00002747"             # Sparkle
    "\U0000274C"             # Cross mark
    "\U0000274E"             # Cross mark
    "\U00002753-\U00002755"  # Question marks
    "\U00002757"             # Exclamation
    "\U00002763-\U00002764"  # Heart exclamation, Heart
    "\U00002795-\U00002797"  # Plus, Minus, Divide
    "\U000027A1"             # Right arrow
    "\U00002934-\U00002935"  # Curved arrows
    "\U00002B05-\U00002B07"  # Arrows
    "\U00002B1B-\U00002B1C"  # Black/white squares
    "\U00002B55"             # Circle
    "\U0001F004"             # Mahjong
    "\U0001F0CF"             # Playing card
    "\U0001F170-\U0001F171"  # A/B buttons
    "\U0001F17E-\U0001F17F"  # O/P buttons
    "\U0001F18E"             # AB button
    "\U0001F191-\U0001F19A"  # Squared words
    "\U0001F1E0-\U0001F1FF"  # Regional indicators (flags)
    "\U0001F201-\U0001F202"  # Japanese symbols
    "\U0001F21A"             # Japanese "free"
    "\U0001F22F"             # Japanese "congratulations"
    "\U0001F232-\U0001F23A"  # Japanese symbols
    "\U0001F250-\U0001F251"  # Japanese symbols
    "\U000E0020-\U000E007F"  # Tags (flag sequences)
    "\U0000FE0F"             # Variation selector-16 (emoji presentation)
    "]+",
    flags=re.UNICODE
)


class EmojiPurgeService(IContentTransformer):
    """
    Removes all emoji characters from a string of content.
    Implements IContentTransformer for seamless integration into the Vault Manager pipeline.
    """

    def transform(self, content: str) -> str:
        """Applies emoji removal to the content, returning the cleaned string."""
        return EMOJI_PATTERN.sub('', content)

    @staticmethod
    def count_emojis(content: str) -> int:
        """Returns the total number of emoji characters in the content."""
        matches = EMOJI_PATTERN.findall(content)
        return sum(len(m) for m in matches)

    @staticmethod
    def is_text_file(filepath: str) -> bool:
        """
        Determines if a file is likely a text file by extension or content inspection.
        Skips binary files to avoid corruption.
        """
        text_extensions = {
            '.md', '.markdown', '.txt', '.text', '.log',
            '.html', '.htm', '.css', '.js', '.mjs', '.cjs', '.ts', '.tsx', '.jsx',
            '.json', '.xml', '.xhtml', '.svg', '.yaml', '.yml', '.toml',
            '.ini', '.cfg', '.conf', '.csv', '.tsv',
            '.py', '.pyw', '.rb', '.java', '.c', '.cpp', '.h', '.hpp', '.cs',
            '.go', '.rs', '.swift', '.kt', '.kts', '.scala', '.php', '.pl', '.pm',
            '.sh', '.bash', '.zsh', '.fish', '.bat', '.cmd', '.ps1',
            '.sql', '.graphql', '.gql',
            '.tex', '.bib', '.rst', '.adoc', '.org',
            '.env', '.gitignore', '.dockerignore', '.editorconfig',
            '.makefile', '.cmake', '.r', '.R', '.rmd', '.Rmd',
            '.lua', '.vim', '.el', '.clj', '.cljs', '.edn',
            '.sass', '.scss', '.less', '.styl',
            '.pug', '.jade', '.ejs', '.hbs', '.mustache', '.njk',
            '.vue', '.svelte', '.astro',
        }
        text_filenames = {
            'Makefile', 'Dockerfile', 'Vagrantfile', 'Gemfile', 'Rakefile',
            'README', 'LICENSE', 'CHANGELOG', 'CONTRIBUTING', 'AUTHORS',
            '.gitignore', '.dockerignore', '.env', '.editorconfig',
        }

        _, ext = os.path.splitext(filepath)
        basename = os.path.basename(filepath)

        if ext.lower() in text_extensions:
            return True
        if basename in text_filenames:
            return True
        # No extension — check if binary by looking for null bytes
        if not ext:
            try:
                with open(filepath, 'rb') as f:
                    chunk = f.read(1024)
                    return b'\x00' not in chunk
            except Exception:
                return False
        return False