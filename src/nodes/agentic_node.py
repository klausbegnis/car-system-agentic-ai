"""
File: agentic_node.py
Project: doutor-ia
Created: Thursday, 18th September 2025 5:23:35 pm
Author: Klaus

Copyright (c) 2025 Doutorie. All rights reserved.
"""

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.types import Command

from src.models.base._chat_model import ChatModel

from .base._node import Node


class AgenticNode(Node):
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

    def execute(
        self, state: StateGraph, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute the node.
        """
        pass
