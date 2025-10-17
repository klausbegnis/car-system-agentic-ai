"""
File: _chat_model.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:26:25 pm
Author: Klaus

MIT License
"""

from abc import ABC, abstractmethod
import os

from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from pydantic import BaseModel

from src.data_models.agent_card import AgentCard
from src.utils.logger import get_logger
from src.utils.stream import stream_if_available

logger = get_logger(__name__)


class ChatModel(ABC):
    """
    Base class for all chat models.
    """

    def __init__(
        self,
        prompt: str,
        agent_card: AgentCard | None = None,
        tools: list[BaseTool] | None = None,
    ):
        self.prompt = prompt
        self.agent_card: AgentCard | None = agent_card
        self.tools: list[BaseTool] = tools or []
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

    @abstractmethod
    def invoke_with_structured_output(self, schema: BaseModel):
        """
        Set the structured output schema.
        """
        pass

    @abstractmethod
    def set_tools(self, tools: list[BaseTool] | None):
        """
        Bind tools to the underlying model, mirroring structured output binding.
        """
        pass

    def invoke_with_tools(
        self,
        messages: list[BaseMessage],
        max_tool_iters: int | None = None,
        config: RunnableConfig | None = None,
    ) -> tuple[list[BaseMessage], str | None, str | None]:
        """
        Invoke once and iteratively fulfill tool calls if present.
        Returns updated messages and optional error message.
        """
        # Get max_tool_iters from environment variable or use default
        if max_tool_iters is None:
            max_tool_iters = int(os.getenv("MAX_TOOL_ITERS", "10"))

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
                return messages, None, None

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
                logger.debug("invoke_with_tools: tool_calls=%r", tool_names)
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
                        logger.warning(
                            f"invoke_with_tools: tool not found: {name}"
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
                        config = args.get("config", {})
                        stream_if_available(
                            config.get("stream_callback"),
                            f"Invocando ferramenta: {name}...",
                            type="reasoning",
                        )
                        result = tool.invoke(input=args, config=config)

                        messages.append(
                            ToolMessage(
                                name=name or "",
                                tool_call_id=call_id,
                                content=str(result),
                            )
                        )
                    except Exception as e:
                        error_msg = f"Tool '{name}' execution error: {e!s}"
                        logger.error(error_msg)
                        messages.append(
                            ToolMessage(
                                name=name or "",
                                tool_call_id=call_id,
                                content=error_msg,
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
