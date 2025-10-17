"""
File: logger.py
Created: Thursday, 18th September 2025 5:44:26 pm
Author: Klaus

MIT License
"""

import logging
import os
from pathlib import Path
import sys
from typing import ClassVar, Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for log levels and file-specific colors."""

    # ANSI color codes for log levels
    LEVEL_COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }

    # Bold vivid colors for file names (avoiding log level colors)
    FILE_COLORS: ClassVar[list[str]] = [
        "\033[1;94m",  # Bold Bright Blue
        "\033[1;95m",  # Bold Bright Magenta
        "\033[1;34m",  # Bold Blue
        "\033[1;35m",  # Bold Magenta
        "\033[1;93m",  # Bold Bright Yellow (different from WARNING)
        "\033[1;91m",  # Bold Bright Red (different from ERROR)
    ]

    # Reset color
    RESET: ClassVar[str] = "\033[0m"

    # Additional colors for components
    TIMESTAMP_COLOR: ClassVar[str] = "\033[90m"  # Dark gray
    BRACKET_COLOR: ClassVar[str] = "\033[37m"  # White
    LINK_COLOR: ClassVar[str] = "\033[94m"  # Blue for links

    def __init__(self, *args, **kwargs):
        """Initialize the colored formatter."""
        super().__init__(*args, **kwargs)
        self._file_color_map: dict[str, str] = {}

    def _get_file_color(self, logger_name: str) -> str:
        """Get a consistent color for a specific file/module."""
        if logger_name not in self._file_color_map:
            # Use hash to get consistent color for same file
            color_index = hash(logger_name) % len(self.FILE_COLORS)
            color = self.FILE_COLORS[color_index]
            self._file_color_map[logger_name] = color
        return self._file_color_map[logger_name]

    def _create_file_link(self, logger_name: str, record) -> str:
        """Create a clickable file link if possible."""
        try:
            # Get file path and line number from the log record
            if hasattr(record, "pathname") and hasattr(record, "lineno"):
                file_path = record.pathname
                line_no = record.lineno

                # Convert to relative path if it's in the project
                try:
                    from pathlib import Path

                    abs_path = Path(file_path)
                    current_dir = Path.cwd()

                    # Try to get relative path for better IDE compatibility
                    try:
                        rel_path = abs_path.relative_to(current_dir)
                        # Use relative path format that IDEs recognize
                        file_ref = f"{rel_path}:{line_no}"
                    except ValueError:
                        # If not relative to current dir, use just filename
                        file_ref = f"{abs_path.name}:{line_no}"

                    return file_ref

                except Exception:
                    # Fallback to just the logger name
                    pass

            # Fallback: just return the logger name
            short_name = (
                logger_name.split(".")[-1]
                if "." in logger_name
                else logger_name
            )
            return short_name

        except Exception:
            return logger_name

    def format(self, record) -> str:
        """Format log record with colors and file links."""
        # Get colors
        level_color = self.LEVEL_COLORS.get(record.levelname, "")
        file_color = self._get_file_color(record.name)

        # Format timestamp with brackets and color
        timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
        colored_timestamp = (
            f"{self.BRACKET_COLOR}[{self.TIMESTAMP_COLOR}{timestamp}"
            f"{self.BRACKET_COLOR}]{self.RESET}"
        )

        # Create file link (filename:line) with file-specific color
        file_link = self._create_file_link(record.name, record)
        colored_file = (
            f"{self.BRACKET_COLOR}({file_color}{file_link}"
            f"{self.BRACKET_COLOR}){self.RESET}"
        )

        # Format level with color
        colored_level = f"{level_color}{record.levelname}{self.RESET}"

        # Format the message
        message = record.getMessage()

        # Combine everything
        formatted_message = (
            f"{colored_timestamp} {colored_file} {colored_level} | {message}"
        )

        return formatted_message


def _is_notebook_environment() -> bool:
    """Check if we're running in a Jupyter notebook environment."""
    try:
        # Check for IPython/Jupyter
        from IPython import get_ipython

        if get_ipython() is not None:
            return get_ipython().__class__.__name__ == "ZMQInteractiveShell"
    except ImportError:
        pass
    return False


def _should_use_colors(use_colors: bool) -> bool:
    """Determine if colors should be used based on environment."""
    if not use_colors:
        return False

    # Always use colors if explicitly requested and we detect any interactive
    # env
    # Check if we're in a notebook (notebooks support ANSI colors)
    if _is_notebook_environment():
        return True

    # Check if we're in a terminal
    if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
        return True

    # Check for common CI/terminal environment variables
    if any(env in os.environ for env in ["TERM", "COLORTERM", "FORCE_COLOR"]):
        return True

    # Check for Jupyter/IPython environment variables
    if any(
        env in os.environ for env in ["JPY_PARENT_PID", "JUPYTER_RUNTIME_DIR"]
    ):
        return True

    # Check for IPython/Jupyter in sys.modules (more reliable detection)
    if "IPython" in sys.modules or "ipykernel" in sys.modules:
        return True

    # Default to True for interactive environments
    return True


def _suppress_grpc_warnings() -> None:
    """Suppress gRPC and ALTS warnings from Google AI SDK."""
    import os
    import warnings

    # Set environment variables to suppress gRPC verbosity
    # (must be set before import)
    os.environ["GRPC_VERBOSITY"] = "ERROR"
    os.environ["GLOG_MINLOGLEVEL"] = "3"  # 3 = FATAL only
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    os.environ["GRPC_TRACE"] = ""
    os.environ["GRPC_VERBOSITY"] = "NONE"

    # Filter specific warning patterns
    warnings.filterwarnings("ignore", message=".*ALTS creds ignored.*")
    warnings.filterwarnings("ignore", message=".*Not running on GCP.*")
    warnings.filterwarnings("ignore", message=".*absl::InitializeLog.*")

    # Try to redirect stderr temporarily for gRPC initialization
    try:
        import contextlib
        import sys

        # Create a context manager to suppress stderr during imports
        @contextlib.contextmanager
        def suppress_stderr():
            with open(os.devnull, "w") as devnull:
                old_stderr = sys.stderr
                sys.stderr = devnull
                try:
                    yield
                finally:
                    sys.stderr = old_stderr

        # Store the context manager for potential use
        globals()["_suppress_stderr"] = suppress_stderr

    except Exception:
        pass


def setup_logging(
    level: str | None = None,
    log_file: Optional[str] = None,
    use_colors: bool = True,
) -> None:
    """
    Setup centralized logging configuration with colors.

    The log level is determined in the following order:
    1. PYTHONLOG environment variable
    2. LOG_LEVEL environment variable
    3. level parameter passed to this function
    4. Default to "INFO"

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        use_colors: Whether to use colored output (default: True)
    """
    # Determine log level from environment or parameter
    env_level = os.getenv("PYTHONLOG") or os.getenv("LOG_LEVEL")
    final_level = (env_level or level or "INFO").upper()

    # Validate log level
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if final_level not in valid_levels:
        print(f"Invalid log level '{final_level}', defaulting to INFO")
        final_level = "INFO"
    # Remove all existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)

    if _should_use_colors(use_colors):
        # Use colored formatter for environments that support colors
        console_formatter = ColoredFormatter()
    else:
        # Use plain formatter for environments without color support
        console_formatter = logging.Formatter(
            "[%(asctime)s] (%(name)s) %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(getattr(logging, final_level))

    # Configure root logger
    root_logger.setLevel(getattr(logging, final_level))
    root_logger.addHandler(console_handler)

    # Add file handler if specified (always without colors)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_formatter = logging.Formatter(
            "[%(asctime)s] (%(name)s) %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(getattr(logging, final_level))
        root_logger.addHandler(file_handler)

    # Log the selected level
    root_logger.debug(f"Logging initialized with level: {final_level}")

    # Set specific loggers to appropriate levels to reduce noise
    for logger_name in [
        "httpx",
        "urllib3",
        "requests",
        "langchain",
        "langgraph",
        "google",
        "google.auth",
        "google.api_core",
        "grpc",
        "absl",
    ]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)

    # Suppress gRPC/ALTS warnings specifically
    _suppress_grpc_warnings()


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the logger (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def suppress_google_warnings():
    """
    Utility function to suppress Google AI SDK warnings.

    Call this before creating GeminiModel instances to reduce noise.

    Example:
        from src.utils.logger import suppress_google_warnings
        suppress_google_warnings()
        model = GeminiModel(...)
    """
    _suppress_grpc_warnings()


# Initialize default logging on import
setup_logging()
