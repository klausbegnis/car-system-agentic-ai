"""
File: agent_registry.py
Project: Agentic AI example
Author: Klaus

MIT License
"""

from __future__ import annotations

from threading import RLock
from typing import ClassVar
import unicodedata

from langchain_core.messages import AIMessage, HumanMessage

from src.data_models.agent_card import AgentCard
from src.models.base._chat_model import ChatModel
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AgentRegistry:
    """In-memory registry of AgentCards (no pre-population)."""

    _name_to_card: ClassVar[dict[str, AgentCard]] = {}
    _name_to_model: ClassVar[dict[str, ChatModel]] = {}
    _lock: ClassVar[RLock] = RLock()

    @staticmethod
    def _normalize(name: str) -> str:
        try:
            s = unicodedata.normalize("NFKD", name)
            s = "".join(c for c in s if not unicodedata.combining(c))
        except Exception:
            s = name
        return "".join(
            ch for ch in s.lower() if ch.isalnum() or ch.isspace()
        ).strip()

    @classmethod
    def register(cls, card: AgentCard, model: ChatModel) -> None:
        """Register or replace an AgentCard and its associated model."""
        with cls._lock:
            cls._name_to_card[card.name] = card
            cls._name_to_model[card.name] = model

    @classmethod
    def get_card(cls, name: str) -> AgentCard | None:
        """Get an AgentCard by name, or None if not found."""
        with cls._lock:
            card = cls._name_to_card.get(name)
            if card:
                return card
            return cls._name_to_card.get(cls._normalize(name))

    @classmethod
    def get_model(cls, name: str) -> ChatModel | None:
        """Get a model by agent name, or None if not found."""
        with cls._lock:
            model = cls._name_to_model.get(name)
            if model:
                return model
            return cls._name_to_model.get(cls._normalize(name))

    @classmethod
    def list_cards(cls) -> list[AgentCard]:
        """Return a snapshot list of all registered AgentCards."""
        with cls._lock:
            # Deduplicate by canonical card.name (defensive)
            unique: dict[str, AgentCard] = {}
            for card in cls._name_to_card.values():
                if card and hasattr(card, "name"):
                    unique[card.name] = card
            return list(unique.values())

    @classmethod
    def clear(cls) -> None:
        """Remove all registered AgentCards."""
        with cls._lock:
            cls._name_to_card.clear()
            cls._name_to_model.clear()

    @classmethod
    def invoke(cls, agent_name: str, query: str) -> str:
        """Invoke the model associated with the agent by name.

        Executes a minimal tool-calling loop so delegated agents can
        call their own tools and return a final answer instead of an
        empty content with only tool calls.
        """
        logger = get_logger(__name__)
        logger.debug(
            "🧩 AgentRegistry.invoke: agent=%r, query[:120]=%r",
            agent_name,
            query[:120],
        )
        with cls._lock:
            model = cls._name_to_model.get(agent_name)
            if model is None:
                model = cls._name_to_model.get(cls._normalize(agent_name))
        if model is None:
            msg = f"Agente '{agent_name}' não encontrado."
            logger.warning("🧩 AgentRegistry.invoke: %s", msg)
            return msg

        # Use centralized tool loop on the delegated model
        messages = [HumanMessage(content=query)]
        messages, final_text, error = model.invoke_with_tools(messages)
        if error:
            logger.warning("🧩 AgentRegistry.invoke: %s", error)
        # If no final_text provided, fallback to scan
        if not final_text:
            for msg in reversed(messages):
                if isinstance(msg, AIMessage):
                    final_text = getattr(msg, "content", "")
                    break
        logger.debug(
            "🧩 AgentRegistry.invoke: resposta len=%d", len(final_text)
        )
        logger.debug(
            "🧩 AgentRegistry.invoke: resposta_preview=%r", final_text[:160]
        )
        return final_text
