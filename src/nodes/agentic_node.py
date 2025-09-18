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
        Execute the agentic node to analyze car problems.
        """
        from langchain_core.messages import HumanMessage

        # Get the last human message from state
        messages = state.get("messages", [])
        if not messages:
            return Command(
                update={
                    "error_message": "No messages found in state.",
                },
                next_node=self.routing_options.get("end", "END"),
            )

        # Find the last human message
        last_human_message = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_human_message = msg
                break

        if not last_human_message:
            return Command(
                update={
                    "error_message": "No human message found in conversation.",
                },
                next_node=self.routing_options.get("end", "END"),
            )

        try:
            # Use the model with its prompt to analyze the car problem
            response = self.model.invoke(messages=[last_human_message])

            # Extract the analysis content
            analysis_content = ""
            if hasattr(response, "content"):
                analysis_content = response.content
            elif isinstance(response, dict) and "content" in response:
                analysis_content = response["content"]
            else:
                analysis_content = str(response)

            # Return successful command with analysis
            return Command(
                update={
                    "analysis_result": {
                        "input": last_human_message.content,
                        "analysis": analysis_content,
                        "node": self.name,
                    },
                    "recommendations": [analysis_content],  # Simple rec
                    "processing_status": "analysis_completed",
                    "error_message": None,
                },
                next_node=self.routing_options.get("next_node", "END"),
            )

        except Exception as e:
            # Return error command
            return Command(
                update={
                    "error_message": f"Error in agentic analysis: {e!s}",
                },
                next_node=self.routing_options.get("end", "END"),
            )
