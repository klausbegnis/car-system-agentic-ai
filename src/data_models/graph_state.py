"""
File: graph_state.py
Project: Agentic AI example
Created: Thursday, 18th September 2025
Author: Klaus

MIT License
"""

from typing import Annotated, Any, Optional, TypedDict

from langchain_core.messages import BaseMessage


class CarSystemState(TypedDict):
    """State schema for the car system agentic AI workflow"""

    messages: Annotated[list[BaseMessage], "append"]
    # Processing status
    processing_status: Optional[str]
    # Results and outputs
    analysis_result: Optional[dict]
    recommendations: Optional[list[str]]
    # Error handling
    error_message: Optional[str]
    # Stream callback for real-time updates
    stream_callback: Optional[Any]
