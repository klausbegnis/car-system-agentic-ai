"""
File: reasoning_node.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:23:35 pm
Author: Klaus

MIT License
"""

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.models.base._chat_model import ChatModel
from src.utils.logger import get_logger

from .base._node import Node

logger = get_logger(__name__)


class ReasoningNode(Node):
    """
    Base class for all agentic nodes in the graph.
    """

    def __init__(
        self,
        routing_options: list[str],
        model: ChatModel,
        tools: list[str],
        name: str = "AgenticNode",
        description: str = "Default agentic node",
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
        self.tools = tools
        self.friendly_agents = []
        logger.info("ReasoningNode: Initialized")

    def execute(
        self, state: dict, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute the agentic node to analyze car problems.
        """
        logger.info("🧠 ReasoningNode: Starting execution")

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
        last_human_message = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_human_message = msg
                break

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
            logger.info("🤖 Invoking model for analysis...")
            # Use the model with its prompt to analyze the car problem
            response = self.model.invoke(messages=[last_human_message])

            # Extract the analysis content
            analysis_content = ""
            if hasattr(response, "content"):
                analysis_content = response.content
            elif isinstance(response, dict) and "content" in response:
                analysis_content = response["content"]
            else:
                analysis_content = str(response)

            logger.info(
                f"🚀 Routing to next_node: "
                f"{self.routing_options.get('next_node')}"
            )

            # Return successful command with analysis
            return Command(
                update={
                    "analysis_result": {
                        "input": last_human_message.content,
                        "analysis": analysis_content,
                        "node": self.name,
                    },
                    "recommendations": [analysis_content],  # Simple rec
                    "processing_status": "analysis_completed",
                    "error_message": None,
                },
                goto=self.routing_options.get("next_node", "END"),
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
