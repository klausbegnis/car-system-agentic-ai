# Using Notebooks

This project is designed to be used primarily through Jupyter notebooks. This guide covers different ways to set up and work with notebooks in your development environment.

## Quick Start

The fastest way to get started is using the template notebook:

1. **Navigate to the notebooks directory:**
   ```bash
   cd notebooks/
   ```

2. **Open `template.ipynb` in your preferred environment**

3. **Run the setup cells to verify everything works**

## Notebook Setup Options

### Option 1: VS Code/Cursor (Recommended)

This is the most convenient way to work with the project:

#### Setup Steps

1. **Open your project in VS Code/Cursor**
2. **Create or open a `.ipynb` file**
3. **Select the correct kernel:**
   - Click "Select Kernel" in the top-right corner
   - Choose `.venv (Python 3.12.3)` (this is your project environment)
   - The kernel will show as "Recommended" if detected correctly

#### Testing Your Setup

```python
# First cell - Setup
exec(open('setup.py').read())

# Second cell - Import and test
from notebooks import *
print(f"✅ Services version: {services.__version__}")
```

#### VS Code Extensions (Recommended)

Install these extensions for the best experience:
- **Jupyter** - Official Jupyter support
- **Python** - Python language support
- **Ruff** - Code formatting and linting

### Option 2: JupyterLab/Notebook

#### With UV (Recommended):
```bash
# Start JupyterLab with your environment
uv run jupyter lab

# Or start Jupyter Notebook
uv run jupyter notebook
```

#### With pip:
```bash
# Make sure your virtual environment is activated
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install Jupyter in your environment (if not already installed)
pip install jupyter jupyterlab

# Start Jupyter
jupyter lab
# or
jupyter notebook
```

### Option 3: Google Colab

If using Google Colab, you'll need to install the package:

```python
# In a Colab cell
!git clone <repository-url>
%cd car-system-agentic-ai

# Setup path manually in Colab
import sys
sys.path.insert(0, '/content/car-system-agentic-ai/src')

# Test installation
import services
print(f"Services version: {services.__version__}")
```

## Notebook Workflow

### Standard Notebook Structure

Every notebook should start with this setup pattern:

```python
# Cell 1: Setup and Imports
exec(open('setup.py').read())

from notebooks import *
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage
from src.data_models.graph_state import CarSystemState

# Cell 2: Load Prompts
from src.utils.prompt_loader import get_prompt

output_guard_rail_prompt = get_prompt("output_guard_rail")
input_guard_rail_prompt = get_prompt("input_guard_rail") 
reasoning_node_prompt = get_prompt("reasoning_node")

# Cell 3: Model and Node Definitions
# Your model and node setup here...
```

### Working with the Project Modules

After running the setup, you have access to:

- **`models`** - AI models (GeminiModel, etc.)
- **`nodes`** - LangGraph nodes (InputGuardRail, ReasoningNode, OutputGuardRail)
- **`schemas`** - Data models and state schemas
- **`services`** - Core services and utilities
- **`utils`** - Utility functions and helpers
- **`logger`** - Centralized logging

### Example Usage

```python
# Create a model
reasoning_agent = models.GeminiModel(
    model="gemini-2.5-flash", 
    prompt=reasoning_node_prompt
)

# Create nodes
input_guard_rail = nodes.InputGuardRail(
    routing_options={"next_node": "reasoning_node", "end": "output_guard_rail"},
    model=input_guard_rail_agent,
)

# Create and run a graph
workflow = StateGraph(state_schema=schemas.CarSystemState)
workflow.add_node("input_guard_rail", input_guard_rail)
# ... add more nodes and edges

app = workflow.compile()
result = app.invoke(test_input)
```

## Troubleshooting Notebooks

### Common Issues

**Issue: Package not found**
- Make sure you selected the correct kernel (`.venv` environment)
- Restart the kernel: Kernel → Restart Kernel
- Verify the setup cell ran successfully

**Issue: Wrong Python version**
- Check kernel selection - should show your project's Python version
- In VS Code/Cursor, click "Select Kernel" and choose the `.venv` option

**Issue: Dependencies missing**
- Ensure you ran `uv sync` or `pip install -e ".[dev]"`
- Restart the kernel after installing new dependencies

**Issue: Import errors**
- Make sure you ran `exec(open('setup.py').read())` in the first cell
- Check that you're in the `notebooks/` directory
- Verify the project structure is intact

**Issue: Environment variables not loaded**
- Ensure `.env` file exists in the project root
- Check that `GOOGLE_API_KEY` is set correctly
- See [Environment Variables Guide](environment-variables.md) for detailed setup
- Restart the kernel after modifying `.env`

### Kernel Management

#### Selecting the Right Kernel

1. **In VS Code/Cursor:**
   - Click the kernel selector in the top-right
   - Choose the `.venv` environment
   - Should show Python version (e.g., "Python 3.12.3")

2. **In JupyterLab:**
   - Go to Kernel → Change Kernel
   - Select the kernel that matches your environment

3. **In Jupyter Notebook:**
   - Use Kernel → Change kernel
   - Choose the appropriate Python environment

#### Refreshing the Environment

If you install new packages or make changes:

```python
# Restart kernel and run setup again
exec(open('setup.py').read())
from notebooks import *
```
