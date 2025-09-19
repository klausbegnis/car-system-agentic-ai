"""
File: output_guard_rail.py
Project: Agentic AI example
Created: Thursday, 18th September 2025
Author: Klaus

MIT License
"""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command

from src.data_models.graph_state import CarSystemState
from src.models.base._chat_model import ChatModel
from src.nodes.base._node import Node
from src.utils.logger import get_logger

logger = get_logger(__name__)


class OutputGuardRail(Node):
    """Output guard rail node to process final responses and ensure safety."""

    def __init__(self, model: ChatModel, routing_options: dict[str, str]):
        """
        Initialize the output guard rail node.

        Args:
            model: The chat model to use for response processing
            routing_options: Routing configuration for the node
        """
        super().__init__(
            name="OutputGuardRail",
            description=(
                "Processes final responses, handles errors, and ensures safety."
            ),
            routing_options=routing_options,
        )
        self.model = model
        logger.info("OutputGuardRail: Initialized")

    def execute(
        self, state: CarSystemState, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute output guard rail processing.

        Args:
            state: Current graph state
            config: Runnable configuration

        Returns:
            Command with final user message
        """
        logger.info("🛡️ OutputGuardRail: Starting execution")

        # Check for errors first
        error_message = state.get("error_message")
        if error_message:
            logger.warning(f"❌ Processing error: {error_message}")
            return self._process_error(error_message)

        # No errors - process successful analysis
        analysis_result = state.get("analysis_result")
        recommendations = state.get("recommendations", [])

        logger.info("✅ Processing successful analysis")

        if not analysis_result or not recommendations or not recommendations[0]:
            logger.warning("⚠️ No analysis result or recommendations found")
            return Command(
                update={
                    "messages": [
                        *state.get("messages", []),
                        AIMessage(
                            content=(
                                "Desculpe, não consegui processar sua "
                                "solicitação adequadamente. Por favor, tente "
                                "reformular sua pergunta sobre o problema do "
                                "seu carro."
                            )
                        ),
                    ],
                    "processing_status": "completed_no_analysis",
                },
                goto=self.routing_options.get("end", "END"),
            )

        return self._process_recommendations(
            analysis_result, recommendations, state
        )

    def _process_error(self, error_message: str) -> Command:
        """Process error and create user-friendly message."""
        logger.info("🔄 Processing error message for user")

        try:
            # Create context for error processing
            messages = [
                HumanMessage(
                    content=(
                        f"Transforme este erro técnico em uma mensagem "
                        f"amigável para o usuário: {error_message}"
                    )
                )
            ]

            response = self.model.invoke(messages=messages)

            # Extract content from response
            if hasattr(response, "content"):
                user_message = response.content
            elif isinstance(response, dict) and "content" in response:
                user_message = response["content"]
            else:
                user_message = str(response)

            if not user_message.strip():
                user_message = (
                    "Desculpe, ocorreu um problema técnico. "
                    "Por favor, tente novamente."
                )

            logger.info("✅ Error processed successfully")
            return Command(
                update={
                    "messages": [AIMessage(content=user_message)],
                    "error_message": None,
                    "processing_status": "error_processed",
                },
                goto=self.routing_options.get("end", "END"),
            )

        except Exception as e:
            logger.error(f"❌ Failed to process error: {e}")
            return Command(
                update={
                    "messages": [
                        AIMessage(
                            content=(
                                "Desculpe, ocorreu um problema técnico. "
                                "Nossa equipe foi notificada e estamos "
                                "trabalhando para resolver."
                            )
                        )
                    ],
                    "error_message": None,
                    "processing_status": "error_processing_failed",
                },
                goto=self.routing_options.get("end", "END"),
            )

    def _process_recommendations(
        self,
        analysis_result: dict,
        recommendations: list,
        state: CarSystemState,
    ) -> Command:
        """Process and validate recommendations for safety."""
        logger.info("🔍 Validating recommendations for safety")

        try:
            # Get the original user message
            messages = state.get("messages", [])
            original_message = ""
            if messages:
                original_message = messages[-1].content

            # Prepare content for safety check and formatting
            recommendation_text = recommendations[0] if recommendations else ""

            safety_check_prompt = (
                f"Analise esta recomendação sobre problemas automotivos e "
                f"verifique se há alguma informação perigosa, incorreta ou "
                f"que possa causar danos. Se houver problemas de segurança, "
                f"reformule a resposta de forma segura. Se estiver tudo bem, "
                f"formate a resposta de forma clara e amigável para o "
                f"usuário.\n\n"
                f"Pergunta original: {original_message}\n"
                f"Recomendação: {recommendation_text}\n\n"
                f"Responda diretamente ao usuário com a recomendação "
                f"(reformulada se necessário)."
            )

            messages_for_model = [HumanMessage(content=safety_check_prompt)]
            response = self.model.invoke(messages=messages_for_model)

            # Extract final message
            if hasattr(response, "content"):
                final_message = response.content
            elif isinstance(response, dict) and "content" in response:
                final_message = response["content"]
            else:
                final_message = str(response)

            if not final_message.strip():
                final_message = (
                    "Com base na sua descrição, recomendo que procure "
                    "um mecânico qualificado para uma avaliação adequada "
                    "do problema."
                )

            logger.info("✅ Recommendations processed and validated")
            logger.info(f"📤 Final message length: {len(final_message)} chars")

            return Command(
                update={
                    "messages": [
                        *state.get("messages", []),
                        AIMessage(content=final_message),
                    ],
                    "processing_status": "completed_successfully",
                },
                goto=self.routing_options.get("end", "END"),
            )

        except Exception as e:
            logger.error(f"❌ Failed to process recommendations: {e}")
            return Command(
                update={
                    "messages": [
                        *state.get("messages", []),
                        AIMessage(
                            content=(
                                "Com base na sua descrição, recomendo que "
                                "procure um mecânico qualificado para uma "
                                "avaliação adequada do problema."
                            )
                        ),
                    ],
                    "processing_status": "completed_with_fallback",
                },
                goto=self.routing_options.get("end", "END"),
            )
