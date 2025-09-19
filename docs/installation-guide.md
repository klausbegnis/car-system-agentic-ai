# Installation Guide

This guide explains how to install and set up the Car System Agentic AI project. Choose between UV (recommended) or traditional pip installation.

## Prerequisites

- Python 3.9 or higher
- Git

## Installation Options

### Option 1: UV (Recommended)

UV provides faster dependency resolution and better environment management.

#### Installing UV

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

#### Project Setup with UV

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd car-system-agentic-ai
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   This will:
   - Create a virtual environment in `.venv/`
   - Install all project dependencies
   - Install the project in development mode

3. **Verify installation:**
   ```bash
   uv run python -c "import sys; sys.path.insert(0, 'src'); import services; print(f'Services version: {services.__version__}')"
   ```

### Option 2: Traditional pip

If you prefer using pip and virtual environments:

#### Project Setup with pip

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd car-system-agentic-ai
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Linux/macOS
   source .venv/bin/activate
   
   # On Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   pip install -e ".[dev]"  # For development dependencies
   ```

4. **Verify installation:**
   ```bash
   python -c "import sys; sys.path.insert(0, 'src'); import services; print(f'Services version: {services.__version__}')"
   ```
