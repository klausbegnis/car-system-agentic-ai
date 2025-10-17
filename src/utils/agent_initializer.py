"""
File: agent_initializer.py
Project: Agentic AI example
Created: Thursday, 17th October 2025
Author: Klaus

MIT License
"""

from src.models.gemini import Gemini
from src.services.agent_registry import AgentRegistry
from src.tools.car import get_car_status
from src.tools.travel import recommend_locations
from src.tools.weather import get_predicted_weather
from src.utils.agent_card_loader import load_agent_cards_from_file
from src.utils.logger import get_logger
from src.utils.prompt_loader import load_prompt_from_markdown

logger = get_logger(__name__)


def initialize_external_agents(
    cards_path: str = "data/agent_cards.json",
) -> None:
    """Initialize external agents with their respective models.

    This function:
    1. Loads agent cards from the specified JSON file
    2. Loads prompts for each agent type
    3. Creates and registers models for each agent

    Args:
        cards_path: Path to the JSON file containing agent cards.
            Defaults to "data/agent_cards.json"

    Raises:
        ValueError: If required agent cards are not found
        FileNotFoundError: If cards file or prompts are not found
        Exception: For other initialization errors
    """
    try:
        # Clear existing registry
        AgentRegistry.clear()

        # Load cards
        agent_cards = load_agent_cards_from_file(cards_path)
        logger.debug(f"📥 Loaded {len(agent_cards)} agent cards")

        # Load prompts for specialized agents
        car_central_prompt = load_prompt_from_markdown("car_central")
        trip_planner_prompt = load_prompt_from_markdown("trip_planner")
        logger.debug("📝 Loaded agent prompts")

        # Initialize models and register with cards
        for card in agent_cards:
            if card.name == "AgenteDiagnosticoCarro":
                model = Gemini(
                    model="gemini-2.5-flash",
                    prompt=car_central_prompt,
                    agent_card=card,
                    tools=[get_car_status],
                )
                AgentRegistry.register(card, model)
                logger.debug("🚗 Registered car diagnostic agent")

            elif card.name == "AgentePlanejadorViagem":
                model = Gemini(
                    model="gemini-2.5-flash",
                    prompt=trip_planner_prompt,
                    agent_card=card,
                    tools=[recommend_locations, get_predicted_weather],
                )
                AgentRegistry.register(card, model)
                logger.debug("✈️ Registered trip planner agent")

        # Verify initialization
        registered_agents = AgentRegistry.list_cards()
        if len(registered_agents) != len(agent_cards):
            logger.warning("❌ Some agents were not registered")
            msg = (
                f"Expected {len(agent_cards)} agents, "
                f"but only {len(registered_agents)} were registered"
            )
            raise ValueError(msg)
        if not registered_agents:
            raise ValueError("No agents were registered successfully")

        logger.info("✅ All agents initialized successfully")

    except FileNotFoundError as e:
        logger.error(f"❌ Failed to find required file: {e}")
        raise
    except ValueError as e:
        logger.error(f"❌ Invalid agent configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Failed to initialize agents: {e}")
        raise
