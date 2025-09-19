"""
File: reasoning_node.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:23:35 pm
Author: Klaus

MIT License
"""

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langgraph.types import Command

from src.models.base._chat_model import ChatModel
from src.utils.logger import get_logger

from .base._node import Node

logger = get_logger(__name__)


class NodeWithTools(Node):
    """Reasoning node that can call tools and use their results inline."""

    def __init__(
        self,
        routing_options: dict[str, str],
        model: ChatModel,
        tools: list[BaseTool] | None = None,
        name: str = "NodeWithTools",
        description: str = "Reasoning node with tool support",
    ):
        """
        Initialize the agentic node.

        Args:
            routing_options (list[str]): The routing options.
            model (BaseChatModel): The chat model to use.
            tools (list[str]): The tools to use.
            name (str, optional): The name of the node.
                Defaults to "AgenticNode".
            description (str, optional): The description of the node.
                Defaults to "Default agentic node".
        """
        super().__init__(name, description, routing_options)
        self.model = model
        self.tools: list[BaseTool] = tools or []
        self.friendly_agents = []
        logger.info("NodeWithTools: Initialized")

    def _get_last_human_message(self, messages: list) -> HumanMessage | None:
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                return msg
        return None

    def _bind_llm_with_tools(self):
        llm = getattr(self.model, "model", None)
        if llm is None:
            return None
        if self.tools:
            try:
                return llm.bind_tools(self.tools)
            except Exception:
                return llm
        return llm

    def _invoke_llm(self, llm, messages: list) -> AIMessage:
        # Prepend system prompt if available so the LLM sees tool instructions
        if getattr(self.model, "prompt", None):
            full_messages = [
                SystemMessage(content=self.model.prompt),
                *messages,
            ]
        else:
            full_messages = messages
        resp = llm.invoke(full_messages)
        if isinstance(resp, AIMessage):
            return resp
        content = getattr(resp, "content", str(resp))
        return AIMessage(content=content)

    def _run_tool(self, call) -> ToolMessage:
        # call may be dict-like with name/args/id
        name = getattr(call, "name", None) or call.get("name", "")
        args = getattr(call, "args", None) or call.get("args", {}) or {}
        call_id = getattr(call, "id", None) or call.get("id", "") or ""
        tool = next((t for t in self.tools if t.name == name), None)
        if tool is None:
            return ToolMessage(
                name=name or "",
                tool_call_id=call_id,
                content=f"Tool '{name}' not found.",
            )
        try:
            result = tool.invoke(args)
            return ToolMessage(
                name=name or "",
                tool_call_id=call_id,
                content=str(result),
            )
        except Exception as e:
            return ToolMessage(
                name=name or "",
                tool_call_id=call_id,
                content=f"Tool '{name}' execution error: {e!s}",
            )

    def execute(
        self, state: dict, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute the agentic node to analyze car problems.
        """
        logger.info("🧠 NodeWithTools: Starting execution")

        # Get the last human message from state
        messages = state.get("messages", [])

        if not messages:
            logger.warning("❌ No messages found in state")
            return Command(
                update={
                    "error_message": "No messages found in state.",
                },
                goto=self.routing_options.get("end", "END"),
            )

        # Find the last human message
        last_human_message = self._get_last_human_message(messages)

        if not last_human_message:
            logger.warning("❌ No human message found in conversation")
            return Command(
                update={
                    "error_message": "No human message found in conversation.",
                },
                goto=self.routing_options.get("end", "END"),
            )

        logger.info(
            f"📨 Processing message: {last_human_message.content[:100]}..."
        )

        try:
            llm = self._bind_llm_with_tools()
            if llm is None:
                return Command(
                    update={"error_message": "Model backend not available."},
                    goto=self.routing_options.get("end", "END"),
                )

            max_tool_iters = 5
            for _ in range(max_tool_iters):
                ai = self._invoke_llm(llm, messages)
                messages.append(ai)

                tool_calls = getattr(ai, "tool_calls", None)
                if tool_calls:
                    logger.debug(f"🔧 Detected tool calls: {tool_calls}")
                if not tool_calls:
                    # finalize
                    final_text = (
                        ai.content if hasattr(ai, "content") else str(ai)
                    )
                    logger.info(
                        f"🚀 Routing to next_node: "
                        f"{self.routing_options.get('next_node')}"
                    )
                    return Command(
                        update={
                            "messages": messages,
                            "analysis_result": {
                                "input": last_human_message.content,
                                "analysis": final_text,
                                "node": self.name,
                            },
                            "recommendations": [final_text],
                            "processing_status": "analysis_completed",
                            "error_message": None,
                        },
                        goto=self.routing_options.get("next_node", "END"),
                    )

                # execute tools and append tool messages
                for call in tool_calls:
                    tool_msg = self._run_tool(call)
                    messages.append(tool_msg)

            return Command(
                update={
                    "messages": messages,
                    "error_message": (
                        "Max tool iterations reached without final answer."
                    ),
                },
                goto=self.routing_options.get("end", "END"),
            )

        except Exception as e:
            logger.error(f"❌ Error in reasoning analysis: {e}")
            # Return error command
            return Command(
                update={
                    "error_message": f"Error in agentic analysis: {e!s}",
                },
                goto=self.routing_options.get("end", "END"),
            )
