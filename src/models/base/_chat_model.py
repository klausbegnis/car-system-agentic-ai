"""
File: _chat_model.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:26:25 pm
Author: Klaus

MIT License
"""

from abc import ABC, abstractmethod
from typing import Optional

from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class ChatModel(ABC):
    """
    Base class for all chat models.
    """

    def __init__(self, model: str, prompt: str):
        self.model = model
        self.prompt = prompt

    @abstractmethod
    def invoke(
        self, messages: Optional[list[BaseMessage]] = None
    ) -> BaseMessage:
        """
        Invoke the chat model.
        """
        pass

    @abstractmethod
    def stream(
        self, messages: Optional[list[BaseMessage]] = None
    ) -> BaseMessage:
        """
        Stream the chat model.
        """
        pass

    def set_structured_output(self, schema: BaseModel):
        """
        Set the structured output schema.
        """
        self.model = self.model.with_structured_output(schema, include_raw=True)
