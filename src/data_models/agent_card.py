"""
File: agent_card.py
Project: Agentic AI example
Created: Thursday, 18th September 2025
Author: Klaus

MIT License
"""

from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class AgentSkill(BaseModel):
    """Represents a skill exposed by an agent.

    This mirrors common A2A card concepts while staying minimal.
    """

    id: str = Field(..., description="Stable identifier for the skill")
    name: str = Field(..., description="Human-readable skill name")
    description: str | None = Field(
        default=None, description="What the skill does and when to use it"
    )


class AgentCapabilities(BaseModel):
    """Capabilities supported by the agent.

    Add flags here as needed (e.g., streaming, tools, images).
    """

    streaming: bool = Field(
        default=False, description="Supports streaming output"
    )
    tools: bool = Field(default=True, description="Agent can call tools")


class AgentCard(BaseModel):
    """Metadata describing a remote agent (A2A-style)."""

    name: str = Field(..., description="Agent name")
    description: str | None = Field(default=None, description="Agent purpose")
    version: str | None = Field(default=None, description="Version string")
    url: HttpUrl | None = Field(
        default=None, description="Public base URL of the agent if available"
    )
    capabilities: AgentCapabilities | None = Field(
        default=None, description="Agent capabilities"
    )
    skills: list[AgentSkill] | None = Field(
        default=None, description="List of skills offered by the agent"
    )
    tags: list[str] | None = Field(
        default=None, description="Free-form tags describing the agent"
    )

    extra: dict[str, object] | None = Field(
        default=None, description="Optional vendor-specific fields"
    )
