"""
File: gemini.py
Project: doutor-ia
Created: Thursday, 18th September 2025 5:33:03 pm
Author: Klaus

Copyright (c) 2025 Doutorie. All rights reserved.
"""

from collections.abc import Iterator
from typing import Any, Optional

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.models.base._chat_model import ChatModel


class Gemini(ChatModel):
    """
    Gemini chat model.
    """

    def __init__(self, model: str, prompt: str, temperature: float = 0.0):
        """
        Start the gemini chat model.

        Args:
            model (str): The model to use.
        """
        super().__init__(model, prompt)
        self.model = ChatGoogleGenerativeAI(
            model=model, temperature=temperature
        )

    def invoke(
        self, messages: Optional[list[BaseMessage]] = None
    ) -> BaseMessage:
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
            return self.model.invoke(messages)
        raise ValueError("Messages are required")

    def stream(
        self, messages: Optional[list[BaseMessage]] = None
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
            return self.model.stream(messages)
        raise ValueError("Messages are required")
