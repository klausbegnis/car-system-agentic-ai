"""
File: __init__.py
Project: Agentic AI example
Created: Thursday, 18th September 2025
Author: Klaus

MIT License
"""

# Import modules
from . import services as _services
from . import utils as _utils

# Import classes directly and create namespaces
from .models.gemini import Gemini as GeminiModel
from .nodes.node_with_tools import NodeWithTools
from .data_models.graph_state import CarSystemState
from .nodes.input_guard_rail import InputGuardRail
from .nodes.output_guard_rail import OutputGuardRail


# Create namespace objects
class models:
    GeminiModel = GeminiModel


class nodes:
    NodeWithTools = NodeWithTools
    InputGuardRail = InputGuardRail
    OutputGuardRail = OutputGuardRail


# State schema
class schemas:
    CarSystemState = CarSystemState


# Make modules available as namespaces
services = _services
utils = _utils

__all__ = ["models", "nodes", "schemas", "services", "utils"]
