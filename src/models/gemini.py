"""
File: gemini.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:33:03 pm
Author: Klaus

MIT License
"""

from collections.abc import Iterator
from typing import Any

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

from src.data_models.agent_card import AgentCard
from src.models.base._chat_model import ChatModel
from src.utils.logger import get_logger

logger = get_logger(__name__)


class Gemini(ChatModel):
    """
    Gemini chat model.
    """

    def __init__(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.0,
        agent_card: AgentCard | None = None,
        tools: list[BaseTool] | None = None,
    ):
        """
        Start the gemini chat model.

        Args:
            model (str): The model to use.
        """
        # Initialize the actual ChatGoogleGenerativeAI model first
        gemini_model = ChatGoogleGenerativeAI(
            model=model, temperature=temperature
        )

        # Call super().__init__ with the actual model instance
        super().__init__(model, prompt, agent_card=agent_card, tools=tools)
        self.model = gemini_model
        self._original_model = gemini_model  # Store original reference
        # Ensure tools are bound on the backend if provided
        if tools:
            try:
                self.set_tools(tools)
                tool_names = [t.name for t in tools]
                logger.info(
                    f"🔗 Gemini: tools bound -> {tool_names}"
                )
            except Exception as e:
                logger.warning(f"Gemini: failed to bind tools: {e}")
        if self.agent_card and self.agent_card.name:
            logger.info(
                f"🤖 GeminiModel: Initialized with model {model} "
                f"[agent={self.agent_card.name}]"
            )
        else:
            logger.info(f"🤖 GeminiModel: Initialized with model {model}")

    def invoke(self, messages: list[BaseMessage] | None = None) -> BaseMessage:
        """
        Invoke the gemini chat model.

        Args:
            messages (Optional[list[BaseMessage]], optional):
            The messages to use. Defaults to None.

        Raises:
            ValueError: Messages are required

        Returns:
            BaseMessage: The response from the gemini chat model.
        """
        if messages:
            # Add system prompt to messages if it exists
            if self.prompt:
                prompt_message = SystemMessage(content=self.prompt)
                full_messages = [prompt_message, *messages]
            else:
                full_messages = messages
            response = self.model.invoke(full_messages)

            # Log token usage based on response type
            try:
                if isinstance(response, dict) and "raw" in response:
                    # Structured output with include_raw=True
                    raw_response = response.get("raw")
                    if (
                        hasattr(raw_response, "usage_metadata")
                        and raw_response.usage_metadata
                    ):
                        logger.info(
                            f"🪙 Token usage: {raw_response.usage_metadata}"
                        )
                elif isinstance(response, BaseMessage):
                    # Direct AIMessage response
                    if (
                        hasattr(response, "usage_metadata")
                        and response.usage_metadata
                    ):
                        logger.info(
                            f"🪙 Token usage: {response.usage_metadata}"
                        )
            except Exception as e:
                logger.debug(f"Could not log token usage: {e}")

            return response
        raise ValueError("Messages are required")

    def stream(
        self, messages: list[BaseMessage] | None = None
    ) -> Iterator[Any]:
        """
        Stream the gemini chat model.

        Args:
            messages (Optional[list[BaseMessage]], optional):
            The messages to use. Defaults to None.

        Raises:
            ValueError: Messages are required

        Returns:
            Iterator[Any]: The response from the gemini chat model.
        """
        if messages:
            # Add system prompt to messages if it exists
            if self.prompt:
                from langchain_core.messages import SystemMessage

                prompt_message = SystemMessage(content=self.prompt)
                full_messages = [prompt_message, *messages]
            else:
                full_messages = messages
            return self.model.stream(full_messages)
        raise ValueError("Messages are required")
