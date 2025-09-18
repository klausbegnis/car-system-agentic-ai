"""State model for LangGraph"""

from typing import Optional, TypedDict

from langchain_core.messages import BaseMessage


class CarSystemState(TypedDict):
    """State schema for the car system agentic AI workflow"""

    # Messages to track conversation flow
    messages: list[BaseMessage]

    # User input and context
    user_input: Optional[str]

    # Car-related data
    car_data: Optional[dict]

    # Processing status
    current_node: Optional[str]
    processing_status: Optional[str]

    # Results and outputs
    analysis_result: Optional[dict]
    recommendations: Optional[list[str]]

    # Error handling
    error_message: Optional[str]

    # Additional context that might be needed
    context: Optional[dict]
