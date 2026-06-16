"""
Traceable, thread-safe, colorized logging utility.
Supports structured terminal output that degrades gracefully in non-TTY environments.
"""

import sys
import threading

COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"


class ThreadSafeLogger:
    """Provides thread-safe logging with dynamic colorization."""

    def __init__(self, use_color: bool = True):
        self._lock = threading.Lock()
        self.use_color = use_color and sys.stdout.isatty()

    def _log(self, prefix: str, color: str, message: str, stream=sys.stdout) -> None:
        with self._lock:
            if self.use_color:
                formatted = f"{color}{prefix} {message}{COLOR_RESET}\n"
            else:
                formatted = f"{prefix} {message}\n"
            stream.write(formatted)
            stream.flush()

    def info(self, message: str) -> None:
        """Standard tracing message."""
        self._log("[*]", COLOR_CYAN, message)

    def success(self, message: str) -> None:
        """Success notification."""
        self._log("[]", COLOR_GREEN, message)

    def warning(self, message: str) -> None:
        """Recoverable operational event."""
        self._log("[]", COLOR_YELLOW, message, stream=sys.stderr)

    def error(self, message: str) -> None:
        """Unrecoverable system failure."""
        self._log("[]", COLOR_RED, message, stream=sys.stderr)

    def section(self, title: str) -> None:
        """Formatted major operational header."""
        border = "=" * 60
        self.info(f"\n{border}\n{title}\n{border}")


# Singleton logger instance
logger = ThreadSafeLogger()