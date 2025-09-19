"""
File: _node.py
Project: Agentic AI example
Created: Thursday, 18th September 2025 5:17:59 pm
Author: Klaus

MIT License
"""

from abc import abstractmethod

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command


class Node:
    """
    Base class for all nodes in the graph.
    """

    def __init__(
        self, name: str, description: str, routing_options: dict[str, str]
    ):
        self.name = name
        self.description = description
        self.routing_options = routing_options

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{self.name}"

    @abstractmethod
    def execute(
        self, state: dict, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute the node.

        Args:
            state: The current state dictionary
            config: Runnable configuration
        """
        pass

    def __call__(self, state: dict, config: RunnableConfig, *args, **kwargs):
        """
        Execute the node.

        Args:
            state: The current state dictionary
            config: Runnable configuration
        """
        return self.execute(state, config, *args, **kwargs)
