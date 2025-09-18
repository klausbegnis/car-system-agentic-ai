"""Guard rail"""

from src.nodes.base._node import Node
from src.models.base._chat_model import ChatModel
from src.data_models.graph_state import CarSystemState
from langgraph.types import Command
from src.data_models.structured_outputs import InputGuardRailOutput
from langchain_core.runnables import RunnableConfig


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

    def execute(
        self, state: CarSystemState, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute the input guard rail check.
        """
        # Implement validation logic here
        messages = state.get("messages", [])
        user_message = messages[-1] if messages else None
        if not (user_message):
            return Command(
                update={
                    "error_message": "No user message found.",
                },
                next_node=self.routing_options[
                    "end"
                ],  # Route to error handling
            )
        # Use the model to validate the input
        self.model.set_structured_output(InputGuardRailOutput)
        response = self.model.invoke(messages=[user_message])
        output = response["parsed"]
        if isinstance(output, InputGuardRailOutput):
            if output.is_valid:
                return Command(
                    update={
                        "user_input": output.validated_input,
                        "error_message": None,
                    },
                    next_node=self.routing_options[
                        "next_node"
                    ],  # Proceed to next node
                )
            else:
                return Command(
                    update={
                        "error_message": output.error_message,
                    },
                    next_node=self.routing_options[
                        "end"
                    ],  # Route to error handling
                )
        return Command(
            update={
                "error_message": "Invalid output from validation model.",
            },
            next_node=self.routing_options["end"],  # Route to error handling
        )
