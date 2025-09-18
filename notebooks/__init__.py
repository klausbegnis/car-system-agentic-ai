"""
File: __init__.py
Project: doutor-ia
Created: Thursday, 18th September 2025 4:50:42 pm
Author: Klaus

Copyright (c) 2025 Doutorie. All rights reserved.
"""

import sys
from pathlib import Path

# Add both project root and src to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"

# Add project root to path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Add src to path
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import main package (only what exists)
import services  # type: ignore # noqa

# Make everything available for "from notebooks import *"
__all__ = [
    "services",
]
