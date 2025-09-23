"""
File: agent_card_loader.py
Project: Agentic AI example
Author: Klaus

MIT License
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.data_models.agent_card import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)


def _coerce_capabilities(
    data: dict[str, Any] | None,
) -> AgentCapabilities | None:
    if not data:
        return None
    return AgentCapabilities(**data)


def _coerce_skills(
    data: list[dict[str, Any]] | None,
) -> list[AgentSkill] | None:
    if not data:
        return None
    return [AgentSkill(**item) for item in data]


def _coerce_card(obj: dict[str, Any]) -> AgentCard:
    payload = {**obj}
    payload["capabilities"] = _coerce_capabilities(payload.get("capabilities"))
    payload["skills"] = _coerce_skills(payload.get("skills"))
    return AgentCard(**payload)


def load_agent_cards_from_file(path: str | Path) -> list[AgentCard]:
    """
    Load agent cards from a file.

    Args:
        path: The path to the file containing the agent cards.

    Returns:
        list[AgentCard]: The loaded agent cards.

    Raises:
        ValueError: If the file does not contain a JSON list of agent cards.
    """
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Expected a JSON list of agent cards.")
    return [_coerce_card(item) for item in data]
