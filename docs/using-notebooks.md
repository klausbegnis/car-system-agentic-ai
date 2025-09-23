# Using Notebooks

## Quick Start

1. **Open `notebooks/graph_execution.ipynb` in VS Code/Cursor**
2. **Select the `.venv` kernel**
3. **Run all cells to test the system**

## Setup

### VS Code/Cursor (Recommended)

1. Open the project in VS Code/Cursor
2. Open `graph_execution.ipynb`
3. Click "Select Kernel" → Choose `.venv (Python 3.12.3)`
4. Run the setup cell:

```python
exec(open('setup.py').read())
from notebooks import *
```

### JupyterLab

```bash
uv run jupyter lab
```

## Basic Usage

The notebook demonstrates the complete system:

```python
# Test the graph with different queries
human_query = "Quero viajar 300 km amanhã. Com o combustível que tenho dá para ir sem reabastecer?"
sync_result = test_graph(app, human_query)

# Or test trip recommendations
human_query = "Qual local você recomenda para eu viajar?"
sync_result = test_graph(app, human_query)
```

## Troubleshooting

- **Package not found**: Select correct kernel (`.venv`)
- **Import errors**: Run setup cell first
- **Environment issues**: Check `.env` file exists with `GOOGLE_API_KEY`
