"""
File: setup.py
Project: doutor-ia
Created: Thursday, 18th September 2025 5:00:18 pm
Author: Klaus

Copyright (c) 2025 Doutorie. All rights reserved.
"""

from pathlib import Path
import sys

# Add project root to path (go up one level from notebooks/)
project_root = Path.cwd().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print("📁 Project path added! You can now: from notebooks import *")
