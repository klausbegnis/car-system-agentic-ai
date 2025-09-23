"""
File: test_graph.py
Project: Agentic AI example
Created: Tuesday, 23rd September 2025 12:31:58 pm
Author: Klaus

MIT License
"""

import logging

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from src.data_models.graph_state import CarSystemState

logger = logging.getLogger(__name__)


def test_graph(app, human_query: str):
    """
    Test the graph execution synchronously.

    Args:
        app (compiled graph): The graph app
        human_query (str): The human query

    Returns:
        dict: The result of the graph execution
    """
    # Create a test state using CarSystemState
    test_input = CarSystemState(
        messages=[HumanMessage(content=human_query)],
        user_input=None,
        car_data=None,
        current_node=None,
        processing_status=None,
        analysis_result=None,
        recommendations=None,
        error_message=None,
        context=None,
    )

    config = RunnableConfig(config={"run_name": "car-system-agentic-ai"})

    print("🔧 Testing graph execution (synchronous)...")
    print(f"Input message: {test_input['messages'][0].content}")
    print("-" * 60)

    try:
        # Run the graph synchronously
        result = app.invoke(input=test_input, config=config)
        print("-" * 60)
        print("✅ Synchronous graph execution successful!")
        print("\n📊 Final State:")
        print("-" * 30)

        print("Pergunta original: ", result["messages"][0].content)
        print("Resposta: ", result["recommendations"][0])

        return result

    except Exception as e:
        print(f"❌ Error during synchronous execution: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback

        print(f"Traceback: {traceback.format_exc()}")
        return None
