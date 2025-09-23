"""
File: reasoning_node.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:23:35 pm
Author: Klaus

MIT License
"""

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from src.models.base._chat_model import ChatModel
from src.utils.logger import get_logger

from ._node import Node

logger = get_logger(__name__)


class NodeWithTools(Node):
    """Base node helper that can call tools and use their results inline.

    This class now exposes a helper method to run a model with optional tools.
    Concrete nodes should implement execute() and may call
    run_model_with_optional_tools().
    """

    def __init__(
        self,
        routing_options: dict[str, str],
        model: ChatModel,
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
        logger.info("NodeWithTools: Initialized")

    def _get_last_human_message(self, messages: list) -> HumanMessage | None:
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                return msg
        return None

    def run_model_with_optional_tools(
        self, messages: list
    ) -> tuple[list, str | None]:
        """Delegate to model.invoke_with_tools with unified behavior."""
        try:
            typed_messages: list[BaseMessage] = messages
            messages, _final_text, error = self.model.invoke_with_tools(
                typed_messages, max_tool_iters=5
            )
            # Keep signature compatibility: propagate error only
            return messages, error
        except Exception as e:
            logger.error(f"❌ Error running model with tools: {e}")
            return messages, f"Error during model execution: {e!s}"

    # Make execute abstract again; concrete nodes must implement it
    def execute(
        self, state: dict, config: RunnableConfig, *args, **kwargs
    ):
        """Abstract execute method for concrete nodes to implement."""
        raise NotImplementedError
