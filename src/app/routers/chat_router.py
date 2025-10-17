"""
File: chat_router.py
Project: Agentic AI example
Created: Thursday, 16th October 2025 9:08:54 pm
Author: Klaus

MIT License
"""

from asyncio import Queue

from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from starlette.responses import StreamingResponse

from src.app.schemas.app_dto import ChatRequest
from src.data_models.graph_state import CarSystemState
from src.graphs.factory import create_chat_graph
from src.utils.logger import get_logger
from src.utils.stream import Streamer

logger = get_logger(__name__)

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """
    Ask the chat model a question.

    Args:
        request (ChatRequest): The request containing the question.

    Returns:
        StreamingResponse: The streaming response containing the answer.
    """
    stream_queue = Queue()
    streamer = Streamer(stream_queue)

    graph = create_chat_graph().compile()
    config = RunnableConfig()
    state = CarSystemState(
        messages=[HumanMessage(content=request.message)],
        stream_callback=streamer,
    )

    return StreamingResponse(
        content=streamer.run_task(graph.invoke, state, config),
        media_type="text/event-stream",
    )
