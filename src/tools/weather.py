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
def get_predicted_weather(location: str = "current location") -> str:
    """
    Get the predicted weather for a specific location.

    Args:
        location (str): The location to get weather for (default: current
        location)

    Returns:
        str: Weather prediction for the location
    """
    weather_options = [
        "ensolarado",
        "nublado",
        "chuvoso",
        "parcialmente nublado",
    ]
    predicted_weather = choice(weather_options)

    logger.info(f"🌤️ Getting weather for {location}: {predicted_weather}")

    return f"Previsão do tempo para {location}: {predicted_weather}"
