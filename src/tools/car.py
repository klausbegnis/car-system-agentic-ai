"""
File: car.py
Project: Agentic AI example
Created: Friday, 19th September 2025 5:14:45 pm
Author: Klaus

MIT License
"""

from random import randint

from langchain_core.tools import tool

from src.utils.logger import get_logger

logger = get_logger(__name__)


@tool
def get_car_status() -> str:
    """Get the status of the car."""
    gas_liters = randint(25, 55)
    current_autonomy = randint(7, 12)
    logger.info(
        f"🔧 Getting car status: gas_liters={gas_liters}, "
        f"current_autonomy={current_autonomy}"
    )
    return (
        f"The car has {gas_liters} liters of gas and a current autonomy of "
        f"{current_autonomy} km/liters."
    )
