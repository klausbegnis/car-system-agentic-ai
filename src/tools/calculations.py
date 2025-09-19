"""
File: calculations.py
Project: Agentic AI example
Created: Friday, 19th September 2025 5:20:49 pm
Author: Klaus

MIT License
"""

from langchain_core.tools import tool

from src.utils.logger import get_logger

logger = get_logger(__name__)


@tool
def is_trip_possible(distance: float, autonomy: float, gas: float) -> bool:
    """Check if the trip is possible."""
    logger.info(
        f"🔧 Checking if trip is possible: distance={distance}, "
        f"autonomy={autonomy}, gas={gas}"
    )
    return distance / autonomy >= gas
