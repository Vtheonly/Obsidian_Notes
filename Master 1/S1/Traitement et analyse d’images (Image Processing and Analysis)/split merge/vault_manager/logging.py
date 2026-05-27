"""
Traceable, colorized logging module for the Vault Manager system.
Supports uniform, structured terminal feedback that degrades gracefully on non-TTY environments.
"""

import sys

# ANSI Escape Sequences for clean terminal formatting
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"


class SystemLogger:
    """Manages robust stdout/stderr logging outputs for system operations."""

    def __init__(self, use_color: bool = True):
        # Disable colors if terminal output is redirected
        self.use_color = use_color and sys.stdout.isatty()

    def _format_message(self, prefix: str, color: str, msg: str) -> str:
        if self.use_color:
            return f"{color}{prefix} {msg}{COLOR_RESET}"
        return f"{prefix} {msg}"

    def info(self, msg: str):
        """Standard trace logs."""
        print(self._format_message("[*]", COLOR_CYAN, msg))

    def success(self, msg: str):
        """Log successful operations."""
        print(self._format_message("[✔]", COLOR_GREEN, msg))

    def warning(self, msg: str):
        """Log recoverable operational events."""
        print(self._format_message("[⚠]", COLOR_YELLOW, msg), file=sys.stderr)

    def error(self, msg: str):
        """Log unrecoverable failures."""
        print(self._format_message("[✗]", COLOR_RED, msg), file=sys.stderr)

    def section(self, title: str):
        """Prints formatted section headers."""
        border = "=" * 60
        print(f"\n{border}\n{title}\n{border}")


# Singleton logger instance
logger = SystemLogger()