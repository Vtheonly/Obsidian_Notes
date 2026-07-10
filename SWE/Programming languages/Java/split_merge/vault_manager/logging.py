"""
Traceable, thread-safe, colorised logging utility.

Outputs structured terminal messages and degrades gracefully in non-TTY
environments (e.g. piped output, captured test runs) by disabling ANSI
colour codes.

NOTE on the prefix quirk
-------------------------
The original implementation used ``"[*]"`` for ``info`` and ``"[]"`` (empty
brackets) for ``success``, ``warning``, and ``error``. This is observable
user-facing output, so the refactor preserves it **exactly** — even though
``"[]"`` for three different severity levels is unusual. Changing the
prefixes would alter log output across the CLI and break the
"100% behavior preservation" contract of the refactor.

NOTE on the stream default
--------------------------
``_log`` binds ``stream=sys.stdout`` as a default argument, which pins the
stream at function-definition time. This is intentional and preserved: the
golden tests rely on it.
"""

from __future__ import annotations

import sys
import threading

# ANSI colour codes. Only emitted when self.use_color is True (i.e. stdout
# is a TTY AND the caller did not explicitly disable colour).
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"


class ThreadSafeLogger:
    """Thread-safe logger with optional ANSI colour output."""

    def __init__(self, use_color: bool = True) -> None:
        self._lock = threading.Lock()
        # Auto-disable colour when stdout is not a TTY (e.g. under pytest,
        # pipes, or redirected output).
        self.use_color = use_color and sys.stdout.isatty()

    def _log(
        self,
        prefix: str,
        color: str,
        message: str,
        stream=sys.stdout,
    ) -> None:
        """Emit a single line. Thread-safe via self._lock."""
        with self._lock:
            if self.use_color:
                formatted = f"{color}{prefix} {message}{COLOR_RESET}\n"
            else:
                formatted = f"{prefix} {message}\n"
            stream.write(formatted)
            stream.flush()

    # ---- severity levels --------------------------------------------------
    # Prefixes preserved EXACTLY from the original (see module docstring).

    def info(self, message: str) -> None:
        """Standard tracing message."""
        self._log("[*]", COLOR_CYAN, message)

    def success(self, message: str) -> None:
        """Success notification."""
        self._log("[]", COLOR_GREEN, message)

    def warning(self, message: str) -> None:
        """Recoverable operational event (written to stderr)."""
        self._log("[]", COLOR_YELLOW, message, stream=sys.stderr)

    def error(self, message: str) -> None:
        """Unrecoverable system failure (written to stderr)."""
        self._log("[]", COLOR_RED, message, stream=sys.stderr)

    def section(self, title: str) -> None:
        """Emit a major operational header banner."""
        border = "=" * 60
        self.info(f"\n{border}\n{title}\n{border}")


# Singleton logger instance, imported throughout the package.
logger = ThreadSafeLogger()
