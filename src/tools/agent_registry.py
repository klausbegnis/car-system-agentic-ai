"""
File: agent_registry.py (tool)
Project: Agentic AI example
Author: Klaus

MIT License
"""

from __future__ import annotations

import json

from langchain_core.tools import tool

from src.services.agent_registry import AgentRegistry
from src.utils.logger import get_logger

logger = get_logger(__name__)


@tool
def list_registered_agents() -> str:
    """Lista agentes registrados (nome e descrição) como JSON."""
    cards = AgentRegistry.list_cards()
    payload = [{"name": c.name, "description": c.description} for c in cards]
    result = json.dumps(payload, ensure_ascii=False)
    logger.info(f"🗂️ list_registered_agents: {len(cards)} agentes")
    if payload:
        logger.debug(f"🗂️ list_registered_agents: primeiros={payload[:2]}")
    return result


@tool
def invoke_agent(agent_name: str, query: str) -> str:
    """Invoca um agente registrado pelo nome, com a consulta fornecida."""
    logger.info(
        f"🔁 invoke_agent: agent={agent_name!r}, query[:120]={query[:120]!r}"
    )
    result = AgentRegistry.invoke(agent_name, query)
    if isinstance(result, str):
        logger.info(f"🔁 invoke_agent: resposta len={len(result)}")
        logger.debug(
            f"🔁 invoke_agent: resposta_preview={result[:160]!r}"
        )
    return result
