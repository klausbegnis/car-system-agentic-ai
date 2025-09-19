"""
File: input_guard_rail.py
Project: Agentic AI example
Created: Thursday, 18th September 2025
Author: Klaus

MIT License
"""

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.data_models.graph_state import CarSystemState
from src.data_models.structured_outputs import InputGuardRailOutput
from src.models.base._chat_model import ChatModel
from src.nodes.base._node import Node
from src.utils.logger import get_logger

logger = get_logger(__name__)


class InputGuardRail(Node):
    """Input guard rail node to validate input data."""

    def __init__(self, model: ChatModel, routing_options: dict[str, str]):
        """
        Initialize the input guard rail node.
        """
        super().__init__(
            name="InputGuardRail",
            description="Ensures input data meets specified criteria before "
            "processing.",
            routing_options=routing_options,
        )
        self.model = model
        logger.info("InputGuardRail: Initialized")

    def execute(
        self, state: CarSystemState, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute the input guard rail check.
        """
        logger.info("🛡️ InputGuardRail: Starting execution")

        # Implement validation logic here
        messages = state.get("messages", [])

        user_message = messages[-1] if messages else None
        if not (user_message):
            logger.warning("❌ No user message found in state")
            return Command(
                update={
                    "error_message": "No user message found.",
                },
                goto=self.routing_options["end"],  # Route to error handling
            )

        logger.info(f"📨 Processing message: {user_message.content[:100]}...")
        # Use the model to validate the input
        self.model.set_structured_output(InputGuardRailOutput)
        response = self.model.invoke(messages=[user_message])

        # With include_raw=True, response is a dict with 'parsed' and 'raw' keys
        if isinstance(response, dict):
            output = response.get("parsed")
        else:
            # Fallback for unexpected format
            output = response
        if isinstance(output, InputGuardRailOutput):
            logger.info(f"✅ Validation result: is_valid={output.is_valid}")
            if output.error_message:
                logger.info(f"⚠️ Error message: {output.error_message}")

            if output.is_valid:
                next_node = self.routing_options.get("next_node")
                logger.info(f"🚀 Routing to next_node: {next_node}")
                return Command(
                    update={
                        "processing_status": "input_validated",
                        "error_message": None,
                    },
                    goto=self.routing_options[
                        "next_node"
                    ],  # Proceed to next node
                )
            else:
                logger.info(
                    f"❌ Routing to end: {self.routing_options.get('end')}"
                )
                return Command(
                    update={
                        "error_message": output.error_message,
                    },
                    goto=self.routing_options["end"],  # Route to error handling
                )

        logger.error(f"❌ Invalid output type: {type(output)}")
        return Command(
            update={
                "error_message": "Invalid output from validation model.",
            },
            goto=self.routing_options["end"],  # Route to error handling
        )
