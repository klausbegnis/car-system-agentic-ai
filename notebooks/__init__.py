"""
File: __init__.py
Project: doutor-ia
Created: Thursday, 18th September 2025 4:50:42 pm
Author: Klaus

Copyright (c) 2025 Doutorie. All rights reserved.
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Add both project root and src to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"

# Add project root to path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add src to path
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Load .env from project root
env_path = project_root / ".env"
load_dotenv(env_path)

# Import everything from src consistently
import src

# Create standardized namespaces
models = src.models
nodes = src.nodes
services = src.services
utils = src.utils

# Setup logging from src
logger = utils.get_logger(__name__)

logger.info(f"🔑 Environment loaded from: {env_path}")
api_key_status = "✅ Found" if os.getenv("GOOGLE_API_KEY") else "❌ Not found"
logger.info(f"🔑 GOOGLE_API_KEY: {api_key_status}")

# Make everything available for "from notebooks import *"
__all__ = [
    "models",
    "nodes", 
    "services",
    "utils",
    "logger",
]
