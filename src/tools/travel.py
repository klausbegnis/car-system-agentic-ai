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
    """
    Recomenda destinos com coordenadas, distância e condições climáticas.

    Args:
        query (str): Tipo de destino desejado (praia, montanha, cidade, etc.)

    Returns:
        list[dict]: Lista de destinos com informações detalhadas

    Exemplo:
    {"name": "Florianópolis", "latitude": -27.5949, "longitude": -48.5482,
    "distance_km": 300, "weather": "Ensolarado", "description": "Bela ilha..."}
    """
    logger.info(f"🌍 recommend_locations: query={query!r}")

    # Dados de demonstração com distâncias; em produção, consultar APIs externas
    recs = [
        {
            "name": "Florianópolis",
            "distance_km": 300,
            "weather": "Ensolarado",
            "description": "Bela ilha com praias e cultura açoriana",
            "travel_time": "3h30min",
            "type": "praia",
        },
        {
            "name": "Campos do Jordão",
            "distance_km": 180,
            "weather": "Parcialmente nublado",
            "description": "Cidade serrana com clima europeu e arquitetura",
            "travel_time": "2h15min",
            "type": "montanha",
        },
        {
            "name": "Santos",
            "distance_km": 80,
            "weather": "Ensolarado",
            "description": "Cidade litorânea com o maior porto da América",
            "travel_time": "1h20min",
            "type": "praia",
        },
        {
            "name": "Ouro Preto",
            "distance_km": 450,
            "weather": "Nublado",
            "description": "Cidade histórica colonial com arquitetura barroca",
            "travel_time": "5h30min",
            "type": "histórica",
        },
        {
            "name": "Ubatuba",
            "distance_km": 250,
            "weather": "Ensolarado",
            "description": "Paraíso ecológico com 100+ praias e Mata Atlântica",
            "travel_time": "3h00min",
            "type": "praia",
        },
    ]

    # Filtrar por tipo se especificado na query
    query_lower = query.lower()
    if (
        "praia" in query_lower
        or "mar" in query_lower
        or "litoral" in query_lower
    ):
        recs = [r for r in recs if r["type"] == "praia"]
    elif (
        "montanha" in query_lower
        or "serra" in query_lower
        or "frio" in query_lower
    ):
        recs = [r for r in recs if r["type"] == "montanha"]
    elif "históric" in query_lower or "cultur" in query_lower:
        recs = [r for r in recs if r["type"] == "histórica"]
    else:
        # Para queries genéricas, retornar uma variedade de tipos
        # Pegar 1 de cada tipo para diversificar
        praia_recs = [r for r in recs if r["type"] == "praia"][:1]
        montanha_recs = [r for r in recs if r["type"] == "montanha"][:1]
        historica_recs = [r for r in recs if r["type"] == "histórica"][:1]
        recs = praia_recs + montanha_recs + historica_recs

    # Limitar a 3 recomendações
    recs = recs[:3]

    logger.info(f"🌍 recommend_locations: retornando {len(recs)} destinos")
    logger.debug(
        f"🌍 recommend_locations: preview={recs[0]['name'] if recs else None}"
    )
    return recs
