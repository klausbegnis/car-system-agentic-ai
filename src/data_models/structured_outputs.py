"""Structured outputs for LLM calls."""

from pydantic import BaseModel


class InputGuardRailOutput(BaseModel):
    """Output model for input guard rail checks."""
    is_valid: bool
    error_message: str | None = None
