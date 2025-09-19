"""
File: structured_outputs.py
Project: Agentic AI example
Created: Thursday, 18th September 2025
Author: Klaus

MIT License
"""

from pydantic import BaseModel


class InputGuardRailOutput(BaseModel):
    """Output model for input guard rail checks."""

    is_valid: bool
    error_message: str | None = None
