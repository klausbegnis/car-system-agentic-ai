"""
File: main.py
Project: Agentic AI example
Created: Wednesday, 15th October 2025 7:07:50 am
Author: Klaus

MIT License
"""

from fastapi import FastAPI

from src.app.routers.chat_router import router as chat_router
from src.utils.agent_initializer import initialize_external_agents
from src.utils.logger import get_logger

logger = get_logger(__name__)


def app_lifespan(app: FastAPI):
    """App lifespan for initializing agents and models."""
    try:
        # Initialize external agents
        initialize_external_agents()
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    yield


app = FastAPI(lifespan=app_lifespan)


@app.get("/")
def read_root():
    """
    Read the root endpoint.
    """
    return {"message": "AgenticAI application for trip planning."}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "car-system-agentic-ai",
        "version": "1.0.0",
    }


app.include_router(chat_router)
