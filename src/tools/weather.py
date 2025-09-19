"""
File: provider.py
Project: Agentic AI example
Created: Friday, 19th September 2025 5:12:23 pm
Author: Klaus

MIT License
"""

from random import choice

from langchain_core.tools import tool

from src.utils.logger import get_logger

logger = get_logger(__name__)


@tool
def get_predicted_weather() -> str:
    """Get the predicted weather for the next day."""
    logger.info(
        f"🔧 Getting predicted weather: {choice(['sunny', 'cloudy', 'rainy'])}"
    )
    return choice(["sunny", "cloudy", "rainy"])
