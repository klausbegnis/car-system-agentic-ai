"""
File: stream.py
Project: Agentic AI example
Created: Thursday, 16th October 2025 9:36:58 pm
Author: Klaus

MIT License
"""

import asyncio
import concurrent.futures
from typing import Callable

from src.utils.logger import get_logger

logger = get_logger(__name__)

CONTINUE_STREAM_TYPES = ["chunk", "reasoning", "end"]


class Streamer:
    """
    Streamer class.
    """

    def __init__(self, queue: asyncio.Queue):
        """
        Initialize the streamer.

        Args:
            queue (Queue): The queue to use for streaming.
        """
        self._queue = queue
        self._timeout = 5
        self._max_retries = 5
        self._current_retries = 0
        self._task = None

    async def run_task(self, task: Callable, *args, **kwargs):
        """
        Run the task and stream the result to the queue.

        Args:
            task (Callable): The task to run.
            *args: The arguments to pass to the task.
            **kwargs: The keyword arguments to pass to the task.
        """
        try:
            # Start the graph execution in a separate task

            graph_task = asyncio.create_task(
                self._run_graph_task(task, *args, **kwargs)
            )

            # Stream from queue while graph is running
            while not graph_task.done():
                try:
                    # Check for queue messages (progress updates)
                    stream_json = await asyncio.wait_for(
                        self._queue.get(), timeout=0.1
                    )
                    yield f"data: {stream_json}\n\n"
                    if self.should_stop_streaming(stream_json):
                        break
                except asyncio.TimeoutError:
                    # No more data in queue, continue
                    pass

            # Wait for graph to complete
            await graph_task

            # Don't stream the final result (state) - it's already handled by
            # the nodes
            # The final result contains the complete state which should not be
            # streamed

        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: {{'type': 'error', 'message': '{e!s}'}}\n\n"

    async def _run_graph_task(self, task: Callable, *args, **kwargs):
        """Run the graph task and return the result."""
        try:
            # Run the graph in a thread pool to avoid blocking

            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Pass args and kwargs separately to the executor
                def run_with_config():
                    return task(*args, **kwargs)

                result = await loop.run_in_executor(executor, run_with_config)
            return result
        except Exception as e:
            logger.error(f"Graph execution error: {e}")
            raise

    def should_stop_streaming(self, stream_json: dict):
        """
        Should stop streaming.

        Args:
            stream_json (dict): The stream json.
        """
        if stream_json.get("type") in CONTINUE_STREAM_TYPES:
            return False
        return True

    def stream(self, text: str, type: str = "chunk"):
        """
        Stream the chunk to the queue.

        Args:
            text (str): The text to stream.
        """
        self._queue.put_nowait({"type": type, "data": text})


def stream_if_available(stream_callback, text: str, type: str = "chunk"):
    """
    Stream the text if the stream callback is available.
    """
    if stream_callback and hasattr(stream_callback, "stream"):
        try:
            stream_callback.stream(text, type)
        except Exception as e:
            # Log error but don't break the flow
            logger.error(f"Streaming error: {e}")
