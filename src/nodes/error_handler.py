"""Error handler node"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.data_models.graph_state import CarSystemState
from src.models.base._chat_model import ChatModel
from src.nodes.base._node import Node


class ErrorHandlerNode(Node):
    """Error handler node to process errors and create user-friendly messages."""

    def __init__(self, model: ChatModel, routing_options: dict[str, str]):
        """
        Initialize the error handler node.

        Args:
            model: The chat model to use for error processing
            routing_options: Routing configuration for the node
        """
        super().__init__(
            name="ErrorHandler",
            description=(
                "Processes internal errors and creates user-friendly messages."
            ),
            routing_options=routing_options,
        )
        self.model = model

    def execute(
        self, state: CarSystemState, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute error handling and create user-friendly message.

        Args:
            state: Current graph state
            config: Runnable configuration

        Returns:
            Command with processed error message
        """
        error_message = state.get("error_message")

        if not error_message:
            # No error to process, this shouldn't happen but handle gracefully
            return Command(
                update={
                    "error_message": None,
                    "user_input": (
                        "Desculpe, ocorreu um problema inesperado. "
                        "Por favor, tente novamente."
                    ),
                },
                next_node=self.routing_options.get("end", "END"),
            )

        try:
            # Create messages for the model
            messages = [
                SystemMessage(content=self.error_processing_prompt),
                HumanMessage(
                    content=f"Erro técnico para processar: {error_message}"
                ),
            ]

            # Use the model to create a user-friendly message
            response = self.model.invoke(messages=messages)

            user_friendly_message = response.get("content", "")
            if not user_friendly_message:
                user_friendly_message = (
                    "Desculpe, ocorreu um problema. Por favor, tente "
                    "novamente ou entre em contato com o suporte."
                )

            return Command(
                update={
                    "error_message": None,  # Clear the technical error
                    "user_input": user_friendly_message,  # Store message
                    "processing_status": "error_processed",
                },
                next_node=self.routing_options.get("end", "END"),
            )

        except Exception:
            # Fallback if error processing itself fails
            return Command(
                update={
                    "error_message": None,
                    "user_input": (
                        "Desculpe, ocorreu um problema técnico. Nossa equipe "
                        "foi notificada e estamos trabalhando para resolver."
                    ),
                    "processing_status": "error_processing_failed",
                },
                next_node=self.routing_options.get("end", "END"),
            )
