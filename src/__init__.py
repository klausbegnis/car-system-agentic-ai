"""Source package."""

# Import modules
from . import services as _services
from . import utils as _utils

# Import classes directly and create namespaces
from .models.gemini import Gemini as GeminiModel
from .nodes.agentic_node import AgenticNode
from .nodes.input_guard_rail import InputGuardRail
from .nodes.error_handler import ErrorHandlerNode

# Create namespace objects
class models:
    GeminiModel = GeminiModel

class nodes:
    AgenticNode = AgenticNode
    InputGuardRail = InputGuardRail
    ErrorHandlerNode = ErrorHandlerNode

# Make modules available as namespaces
services = _services
utils = _utils

__all__ = ["models", "nodes", "services", "utils"]
