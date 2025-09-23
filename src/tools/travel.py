"""
File: travel.py
Project: Agentic AI example
Author: Klaus

MIT License
"""

from __future__ import annotations

from langchain_core.tools import tool

from src.utils.logger import get_logger

logger = get_logger(__name__)


@tool
def recommend_locations(query: str) -> list[dict[str, object]]:
    """Recomenda destinos com coordenadas e condições climáticas.

    Exemplo:
    {"name": "Florianópolis", "latitude": -27.5949, "longitude": -48.5482,
    "weather": "Ensolarado"}
    """
    logger.info(f"🌍 recommend_locations: query={query!r}")
    # Dados de demonstração; em produção, consultar APIs externas.
    recs = [
        {
            "name": "Florianópolis",
            "latitude": -27.5949,
            "longitude": -48.5482,
            "weather": "Ensolarado",
        },
        {
            "name": "São Paulo",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "weather": "Parcialmente nublado",
        },
        {
            "name": "Rio de Janeiro",
            "latitude": -22.9068,
            "longitude": -43.1729,
            "weather": "Ensolarado",
        },
    ]
    logger.info(f"🌍 recommend_locations: retornando {len(recs)} itens")
    logger.debug(
        f"🌍 recommend_locations: preview={recs[0] if recs else None}"
    )
    return recs
