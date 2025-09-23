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
    try:
        needed_gas = distance / autonomy
        possible = needed_gas <= gas
        logger.info(
            f"🔧 Trip feasibility: needed_gas={needed_gas:.4f}, "
            f"available_gas={gas:.4f}, possible={possible}"
        )
        return possible
    except Exception as e:
        logger.error(f"❌ is_trip_possible error: {e}")
        raise
