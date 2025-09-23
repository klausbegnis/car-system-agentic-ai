"""
File: _chat_model.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:26:25 pm
Author: Klaus

MIT License
"""

from abc import ABC, abstractmethod

from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from src.data_models.agent_card import AgentCard
from src.utils.logger import get_logger


class ChatModel(ABC):
    """
    Base class for all chat models.
    """

    def __init__(
        self,
        model: str,
        prompt: str,
        agent_card: AgentCard | None = None,
        tools: list[BaseTool] | None = None,
    ):
        self.model = model
        self.prompt = prompt
        self.agent_card: AgentCard | None = agent_card
        self.tools: list[BaseTool] = tools or []
        self._logger = get_logger(__name__)
        self._original_model = None  # Keep reference to original model
        if self.tools:
            self.set_tools(self.tools)

    @abstractmethod
    def invoke(self, messages: list[BaseMessage] | None = None) -> BaseMessage:
        """
        Invoke the chat model.
        """
        pass

    @abstractmethod
    def stream(self, messages: list[BaseMessage] | None = None) -> BaseMessage:
        """
        Stream the chat model.
        """
        pass

    def set_structured_output(self, schema: BaseModel):
        """
        Set the structured output schema.
        """
        # Use original model if available, otherwise current model
        base_model = (
            self._original_model if self._original_model else self.model
        )

        # Apply structured output first
        structured_model = base_model.with_structured_output(
            schema, include_raw=True
        )

        # Then apply tools if we have them
        if self.tools:
            try:
                self.model = structured_model.bind_tools(self.tools)
            except Exception:
                self.model = structured_model
        else:
            self.model = structured_model

    def set_tools(self, tools: list[BaseTool] | None):
        """
        Bind tools to the underlying model, mirroring structured output binding.
        """
        self.tools = tools or []

        # Store original model reference if not already stored
        if self._original_model is None:
            self._original_model = self.model

        if hasattr(self.model, "bind_tools") and self.tools:
            from contextlib import suppress

            with suppress(Exception):
                self.model = self.model.bind_tools(self.tools)

    def invoke_with_tools(
        self, messages: list[BaseMessage], max_tool_iters: int = 5
    ) -> tuple[list[BaseMessage], str | None, str | None]:
        """
        Invoke once and iteratively fulfill tool calls if present.
        Returns updated messages and optional error message.
        """
        try:
            # Build tool map once
            try:
                tool_map = {t.name: t for t in (self.get_tools() or [])}
            except Exception:
                tool_map = {}

            # First invoke
            resp = self.invoke(messages)
            messages.append(resp)

            if not tool_map:
                return messages, None

            for _ in range(max_tool_iters):
                tool_calls = getattr(resp, "tool_calls", None)
                if not tool_calls:
                    # Try to extract final text
                    final_text = getattr(resp, "content", None)
                    return messages, final_text, None
                # Log only the tool names to avoid long lines
                try:
                    tool_names = [
                        getattr(c, "name", None) or c.get("name", "")
                        for c in tool_calls
                    ]
                except Exception:
                    tool_names = []
                self._logger.info(
                    "🧰 invoke_with_tools: tool_calls=%r", tool_names
                )
                for call in tool_calls:
                    name = getattr(call, "name", None) or call.get("name", "")
                    args = (
                        getattr(call, "args", None)
                        or call.get("args", {})
                        or {}
                    )
                    call_id = (
                        getattr(call, "id", None) or call.get("id", "") or ""
                    )
                    tool = tool_map.get(name)
                    if not tool:
                        self._logger.warning(
                            f"🧰 invoke_with_tools: tool not found: {name}"
                        )
                        messages.append(
                            ToolMessage(
                                name=name or "",
                                tool_call_id=call_id,
                                content=f"Tool '{name}' not found.",
                            )
                        )
                        continue
                    try:
                        result = tool.invoke(args)

                        messages.append(
                            ToolMessage(
                                name=name or "",
                                tool_call_id=call_id,
                                content=str(result),
                            )
                        )
                    except Exception as e:
                        messages.append(
                            ToolMessage(
                                name=name or "",
                                tool_call_id=call_id,
                                content=f"Tool '{name}' execution error: {e!s}",
                            )
                            )
                # Re-invoke after tools
                resp = self.invoke(messages)
                messages.append(resp)

            return (
                messages,
                None,
                "Max tool iterations reached without final answer.",
            )
        except Exception as e:
            return messages, None, f"Error during model execution: {e!s}"

    def has_tools(self) -> bool:
        return bool(self.tools)

    def get_tools(self) -> list[BaseTool]:
        return self.tools
