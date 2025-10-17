"""
File: factory.py
Project: Agentic AI example
Created: Thursday, 16th October 2025 9:13:00 pm
Author: Klaus

MIT License
"""

from langgraph.constants import END, START
from langgraph.graph import StateGraph

from src.data_models.graph_state import CarSystemState
from src.models.gemini import Gemini
from src.nodes.input_guard_rail import InputGuardRail
from src.nodes.output_guard_rail import OutputGuardRail
from src.nodes.reasoning_node import ReasoningNode
from src.tools.calculations import is_trip_possible
from src.tools.registry_interaction import invoke_agent, list_registered_agents
from src.utils.prompt_loader import load_prompt_from_markdown


def create_chat_graph() -> StateGraph:
    """Create a not compiled graph.

    Returns:
        StateGraph: The compiled chat graph.
    """
    # Load prompts for graph nodes
    input_guard_rail_prompt = load_prompt_from_markdown("input_guard_rail")
    reasoning_node_prompt = load_prompt_from_markdown("reasoning_node")
    output_guard_rail_prompt = load_prompt_from_markdown("output_guard_rail")
    # Input guard rail agent
    input_guard_rail_agent = Gemini(
        model="gemini-2.5-flash", prompt=input_guard_rail_prompt
    )
    # Reasoning agent (orchestration + quick feasibility)
    reasoning_agent = Gemini(
        model="gemini-2.5-flash",
        prompt=reasoning_node_prompt,
        tools=[list_registered_agents, invoke_agent, is_trip_possible],
    )
    # Output guard rail agent
    output_guard_rail_agent = Gemini(
        model="gemini-2.5-flash", prompt=output_guard_rail_prompt
    )

    # create the graph
    # node definition
    entrypoint = START
    input_guard_rail_name = "input_guard_rail"
    reasoning_node_name = "reasoning_node"
    output_guard_rail_name = "output_guard_rail"
    exit_zone = END

    input_guard_rail = InputGuardRail(
        routing_options={
            "next_node": reasoning_node_name,
            "end": output_guard_rail_name,
        },
        model=input_guard_rail_agent,
    )

    reasoning_node = ReasoningNode(
        routing_options={
            "next_node": output_guard_rail_name,
            "end": output_guard_rail_name,
        },
        model=reasoning_agent,
    )

    output_guard_rail = OutputGuardRail(
        routing_options={"end": exit_zone},
        model=output_guard_rail_agent,
    )

    # workflow
    workflow = StateGraph(state_schema=CarSystemState)
    workflow.add_node(input_guard_rail_name, input_guard_rail)
    workflow.add_node(reasoning_node_name, reasoning_node)
    workflow.add_node(output_guard_rail_name, output_guard_rail)
    workflow.add_edge(entrypoint, input_guard_rail_name)
    # Remove fixed edges - let nodes handle routing dynamically
    workflow.add_edge(output_guard_rail_name, exit_zone)
    return workflow
