"""
File: _node.py
Project: doutor-ia
Created: Thursday, 18th September 2025 5:17:59 pm
Author: Klaus

Copyright (c) 2025 Doutorie. All rights reserved.
"""

from abc import abstractmethod

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
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
        self, state: StateGraph, config: RunnableConfig, *args, **kwargs
    ) -> Command:
        """
        Execute the node.
        """
        pass

    def __call__(
        self, state: StateGraph, config: RunnableConfig, *args, **kwargs
    ):
        """
        Execute the node.

        Args:
            state (StateGraph): _description_
            config (RunnableConfig): _description_
        """
        self.execute(state, config, *args, **kwargs)
