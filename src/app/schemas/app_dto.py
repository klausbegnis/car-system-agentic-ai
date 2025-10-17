"""
File: app_dto.py
Project: Agentic AI example
Created: Thursday, 16th October 2025 9:11:27 pm
Author: Klaus

MIT License
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request schema for the chat endpoint.
    """

    message: str = Field(..., description="The query to chat about.")
    thread_id: str = Field(..., description="The thread for context tracking.")
