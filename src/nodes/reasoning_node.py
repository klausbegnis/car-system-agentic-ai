"""
File: reasoning_node.py
Project: Agentic AI example
Created: Tuesday, 23rd September 2025
Author: Klaus

MIT License
"""

from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.utils.logger import get_logger
from src.utils.stream import stream_if_available

from .base._node_with_tools import NodeWithTools

logger = get_logger(__name__)


class ReasoningNode(NodeWithTools):
    """Concrete node that performs reasoning with optional tools."""

    def execute(
        self, state: dict, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """Run reasoning, invoking tools only if requested by the model."""
        logger.info("ReasoningNode: Starting execution")

        stream_callback = state.get("stream_callback")
        stream_if_available(
            stream_callback,
            "Realizando análise...",
            type="reasoning",
        )

        messages = state.get("messages", [])
        if not messages:
            logger.warning("No messages found in state")
            return Command(
                update={"error_message": "No messages found in state."},
                goto=self.routing_options.get("end", "END"),
            )

        last_human_message = self._get_last_human_message(messages)
        if not last_human_message:
            logger.warning("No human message found in conversation")
            return Command(
                update={
                    "error_message": "No human message found in conversation.",
                },
                goto=self.routing_options.get("end", "END"),
            )

        logger.info(
            f"Processing message: {last_human_message.content[:100]}..."
        )

        stream_if_available(
            config.get("stream_callback"),
            "Listando agentes disponíveis...",
            type="reasoning",
        )

        # Store stream_callback in the node for use in
        # run_model_with_optional_tools
        self._current_state = state
        messages, error = self.run_model_with_optional_tools(messages, config)
        if error:
            return Command(
                update={"messages": messages, "error_message": error},
                goto=self.routing_options.get("end", "END"),
            )

        # Final message expected to be the last AIMessage
        final_ai = None
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                final_ai = msg
                break

        final_text = final_ai.content if isinstance(final_ai, AIMessage) else ""

        next_node = self.routing_options.get("next_node")
        logger.info(f"Routing to next_node: {next_node}")
        return Command(
            update={
                "messages": messages,
                "analysis_result": {
                    "input": last_human_message.content,
                    "analysis": final_text,
                    "node": self.name,
                },
                "recommendations": [final_text] if final_text else None,
                "processing_status": "analysis_completed",
                "error_message": None,
            },
            goto=next_node or "END",
        )
